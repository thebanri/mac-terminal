# Block glyphs in colour, alternating rows, to see whether they fill a cell.
import sys, time
w = sys.stdout.write
w("\x1b[2J\x1b[H")
for label, ch in [("full", "█"), ("full", "█"), ("upper", "▀"), ("upper", "▀"), ("lower", "▄"), ("lower", "▄")]:
    w("%-6s\x1b[38;2;255;0;0m\x1b[48;2;0;0;255m%s\x1b[0m\r\n" % (label, ch * 30))
for i in range(6):
    w("u%d    \x1b[38;2;%sm\x1b[48;2;0;0;0m%s\x1b[0m\r\n" % (i, "255;255;0" if i % 2 else "0;255;0", "▀" * 30))
w("text: The quick brown fox jumps over the lazy dog. gjpqy ÇĞİÖŞÜ\r\n")
sys.stdout.flush()
import os
time.sleep(float(os.environ.get("HOLD", 30)))
