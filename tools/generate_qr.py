#!/usr/bin/env python3
"""Generate both checked-in QR assets offline. Python 3.9+, no installation."""
import html
import json
from pathlib import Path
import struct
import zlib
from vendor.qrcodegen import QrCode

ROOT = Path(__file__).resolve().parents[1]
URL = json.loads((ROOT / 'config/channel.json').read_text())['invite_url']
qr = QrCode.encode_text(URL, QrCode.Ecc.MEDIUM)
border, scale = 4, 10  # Standard four-module quiet zone; no logo obscures modules.
side = qr.get_size() + border * 2
path = ' '.join(
    f'M{x + border},{y + border}h1v1h-1z'
    for y in range(qr.get_size()) for x in range(qr.get_size()) if qr.get_module(x, y)
)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side} {side}" shape-rendering="crispEdges">
<title>Meshtastic Koeln: Einladungslink</title><desc>{html.escape(URL)}</desc>
<path fill="#fff" d="M0 0h{side}v{side}H0z"/><path fill="#000" d="{path}"/>
</svg>
'''
(ROOT / 'assets/koeln-qr.svg').write_text(svg)

# Grayscale PNG, made with standard-library primitives to avoid imaging dependencies.
pixels = bytearray()
for py in range(side * scale):
    pixels.append(0)  # PNG filter: None
    for px in range(side * scale):
        pixels.append(0 if qr.get_module(px // scale - border, py // scale - border) else 255)

def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)

png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('>IIBBBBB', side * scale, side * scale, 8, 0, 0, 0, 0))
png += chunk(b'IDAT', zlib.compress(pixels, 9)) + chunk(b'IEND', b'')
(ROOT / 'assets/koeln-qr.png').write_bytes(png)
print(f'QR assets generated: {qr.get_size()} modules, {side * scale}px PNG, ECC M or higher.')
