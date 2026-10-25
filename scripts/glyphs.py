# Prints block glyphs in colour to see how Terminal.app sizes them, then
# turns on mouse reporting and records what the terminal sends.
import os, sys, time, select, tty
w = sys.stdout.write
w("\x1b[8;24;80t\x1b[2J\x1b[H"); sys.stdout.flush(); time.sleep(1)
def row(label, ch, fg="255;0;0", bg="0;0;255"):
    w("%-8s\x1b[38;2;%sm\x1b[48;2;%sm%s\x1b[0m  \x1b[38;2;%sm\x1b[48;2;%sm%s\x1b[0m\r\n" % (label, fg, bg, ch * 20, fg, bg, ch * 20))
for label, ch in [("upper", "▀"), ("upper", "▀"), ("lower", "▄"), ("lower", "▄"), ("full", "█"), ("full", "█"), ("space", " "), ("left", "▌"), ("sext", "🬂"), ("quad", "▀▄")]:
    row(label, ch)
w("\r\nupper alternating rows:\r\n")
for i in range(4):
    row("u%d" % i, "▀", "255;255;0" if i % 2 else "0;255;0", "0;0;0")
w("lower alternating rows:\r\n")
for i in range(4):
    row("l%d" % i, "▄", "255;255;0" if i % 2 else "0;255;0", "0;0;0")
sys.stdout.flush()
tty.setraw(0)
w("\x1b[?1000h\x1b[?1002h\x1b[?1003h\x1b[?1006h"); sys.stdout.flush()
log = open(os.environ["OUT"], "wb")
end = time.time() + 25
while time.time() < end:
    r, _, _ = select.select([0], [], [], 0.1)
    if r:
        log.write(os.read(0, 4096)); log.flush()
w("\x1b[?1003l\x1b[?1002l\x1b[?1000l\x1b[?1006l"); sys.stdout.flush()
