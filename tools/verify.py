#!/usr/bin/env python3
"""Check the actual invitation payload, local links and QR reproducibility offline."""
import base64
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'config/channel.json').read_text())
url = config['invite_url']

def varint(buf, pos):
    value = shift = 0
    while True:
        byte = buf[pos]
        pos += 1
        value |= (byte & 127) << shift
        if not byte & 128:
            return value, pos
        shift += 7
        assert shift < 64, 'Invalid protobuf varint'

def fields(buf):
    result = []
    pos = 0
    while pos < len(buf):
        tag, pos = varint(buf, pos)
        number, wire = tag >> 3, tag & 7
        if wire == 0:
            value, pos = varint(buf, pos)
        elif wire == 2:
            size, pos = varint(buf, pos)
            value = buf[pos:pos + size]
            assert len(value) == size
            pos += size
        elif wire == 5:
            value = int.from_bytes(buf[pos:pos + 4], 'little')
            pos += 4
        else:
            raise AssertionError(f'Unsupported wire type {wire}')
        result.append((number, wire, value))
    assert pos == len(buf)
    return result

fragment = urlsplit(url).fragment
payload = base64.urlsafe_b64decode(fragment + '=' * (-len(fragment) % 4))
channel_set = fields(payload)
assert len(channel_set) == 1 and channel_set[0][:2] == (1, 2), 'Expected one ChannelSettings, no LoRaConfig'
channel = {number: value for number, wire, value in fields(channel_set[0][2])}
assert channel[3].decode() == config['name'] == 'Koeln'
assert len(channel[2]) == 32
assert base64.b64encode(channel[2]).decode() == config['public_psk_base64']
assert channel[4] == 2, 'Field 4 is ID=2, not the channel role'
assert channel.get(5, 0) == channel.get(6, 0) == 0
assert urlsplit(url).query == 'add=true'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.invites, self.inputs = set(), [], [], {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate ID: {a["id"]}'
            self.ids.add(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.links.append(a[key])
        if 'data-invite' in a:
            self.invites.append(a['href'])
        if tag == 'input':
            self.inputs[a.get('id')] = a.get('value')

page = Page()
page.feed((ROOT / 'index.html').read_text())
assert len(page.invites) == 2 and all(link == url for link in page.invites)
assert page.inputs['invite-url'] == url
assert page.inputs['public-key'] == config['public_psk_base64']
for link in page.links:
    target = urlsplit(link)
    if target.scheme or target.netloc:
        continue
    if target.path:
        assert not target.path.startswith('/'), f'Project Pages needs relative URLs: {link}'
        assert (ROOT / unquote(target.path)).is_file(), f'Missing file: {link}'
    elif target.fragment:
        assert unquote(target.fragment) in page.ids, f'Missing anchor: {link}'
assets = [ROOT / 'assets/koeln-qr.svg', ROOT / 'assets/koeln-qr.png']
before = [p.read_bytes() for p in assets]
subprocess.run([sys.executable, str(ROOT / 'tools/generate_qr.py')], check=True)
assert before == [p.read_bytes() for p in assets], 'QR assets did not match generator/config'
print('OK: exact invitation, AES-256 key, payload semantics, QR assets, relative links and anchors.')
