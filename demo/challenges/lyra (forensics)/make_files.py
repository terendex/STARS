"""Regenerates the player downloads for the demo's Lyra stars, using only the standard library.

Run this after changing a flag, then push the files with scripts\\demo.ps1 sync.
"""
import pathlib
import random
import struct
import zlib

ROOT = pathlib.Path(__file__).resolve().parent


def write(star, name, data):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def png(width, height, pixels):
    rows = b"".join(
        b"\x00" + bytes(pixels[y * width * 3 : (y + 1) * width * 3]) for y in range(height)
    )
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


# RR Lyrae: a black sky with the flag written in a colour one step brighter than
# black. Paint's fill bucket, or any brightness slider, shows it. The text is in
# capitals with no look-alike characters, because players read it off an image.
FLAG = "STARS{RR_LYRAE_HIDES_IN_THE_DARK}"
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "{": ["00110", "00100", "00100", "01000", "00100", "00100", "00110"],
    "}": ["01100", "00100", "00100", "00010", "00100", "00100", "01100"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
}
WIDTH, HEIGHT, SCALE = 960, 540, 4
TEXT = (8, 8, 8)
text_width = len(FLAG) * 6 * SCALE
left, top = (WIDTH - text_width) // 2, (HEIGHT - 7 * SCALE) // 2
pixels = bytearray(WIDTH * HEIGHT * 3)
for index, char in enumerate(FLAG):
    for row, bits in enumerate(FONT[char]):
        for column, bit in enumerate(bits):
            if bit == "1":
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        x = left + index * 6 * SCALE + column * SCALE + dx
                        y = top + row * SCALE + dy
                        pixels[(y * WIDTH + x) * 3 : (y * WIDTH + x) * 3 + 3] = bytes(TEXT)
# A few visible stars, kept clear of the text so they can't hide a letter.
rng = random.Random("rr-lyrae")
for _ in range(160):
    x, y = rng.randrange(WIDTH), rng.randrange(HEIGHT)
    if top - 12 <= y <= top + 7 * SCALE + 12 and left - 12 <= x <= left + text_width + 12:
        continue
    level = rng.randint(90, 255)
    pixels[(y * WIDTH + x) * 3 : (y * WIDTH + x) * 3 + 3] = bytes((level, level, min(255, level + 30)))
write("rr-lyrae", "rr_lyrae.png", png(WIDTH, HEIGHT, pixels))


# Delta Lyrae: the flag is in the PDF's metadata (its Subject), not on the page.
# The metadata is stored as hex, so searching the file in a text editor doesn't
# find it. A PDF viewer's Document properties does.
FLAG = "STARS{d3lt4_lyr43_m3t4d4t4}"
stream = b"\n".join(
    [
        b"BT /F1 20 Tf 72 720 Td (Lyra Survey: Observation Report) Tj ET",
        b"BT /F1 12 Tf 72 690 Td (Target: Delta Lyrae) Tj ET",
        b"BT /F1 12 Tf 72 670 Td (Delta Lyrae is a wide pair of stars in the constellation Lyra.) Tj ET",
        b"BT /F1 12 Tf 72 650 Td (Both stars were measured on three clear nights.) Tj ET",
        b"BT /F1 12 Tf 72 620 Td (End of report.) Tj ET",
    ]
)


def pdf_text(text):
    return b"<" + text.encode().hex().upper().encode() + b">"


objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
    b"/Resources << /Font << /F1 5 0 R >> >> >>",
    b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Title %s /Author %s /Subject %s /Keywords %s >>"
    % (
        pdf_text("Lyra Survey: Delta Lyrae"),
        pdf_text("Lyra Survey Team"),
        pdf_text(f"Archive key: {FLAG}"),
        pdf_text("Lyra, double star, survey"),
    ),
]
pdf = b"%PDF-1.4\n"
offsets = []
for number, body in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf += b"%d 0 obj\n%s\nendobj\n" % (number, body)
xref = len(pdf)
pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
for offset in offsets:
    pdf += b"%010d 00000 n \n" % offset
pdf += b"trailer\n<< /Size %d /Root 1 0 R /Info 6 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
    len(objects) + 1,
    xref,
)
write("delta-lyrae", "delta_lyrae_report.pdf", pdf)
