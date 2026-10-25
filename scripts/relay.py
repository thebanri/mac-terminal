# Runs a program in a pty inside Terminal.app, passes its output through
# untouched (and to out.bin), and types a script of keys into it.
import fcntl, os, pty, select, struct, sys, termios, time, tty

rows, cols = int(os.environ.get("ROWS", 40)), int(os.environ.get("COLS", 140))
sys.stdout.buffer.write(b"\x1b[8;%d;%dt" % (rows, cols))  # resize the window
sys.stdout.flush()
time.sleep(1.5)
ws = fcntl.ioctl(0, termios.TIOCGWINSZ, b"\0" * 8)
pid, fd = pty.fork()
if pid == 0:
    os.execvp(sys.argv[1], sys.argv[1:])
fcntl.ioctl(fd, termios.TIOCSWINSZ, ws)
tty.setraw(0)
log = open(os.environ.get("OUT", "out.bin"), "wb")
start = time.time()
# (from, to, every, bytes): Enter on the title, stand, walk, turn, stand.
plan = [(4, 4.1, 1, b"\r"), (10, 16, 0.05, b"w"), (16, 22, 0.05, b"e"), (30, 30.1, 1, b"\x1b")]
last = {}
while True:
    t = time.time() - start
    if t > 34:
        break
    for i, (a, b, every, keys) in enumerate(plan):
        if a <= t < b and t - last.get(i, -9) >= every:
            os.write(fd, keys)
            last[i] = t
    r, _, _ = select.select([fd, 0], [], [], 0.01)
    if fd in r:
        try:
            data = os.read(fd, 65536)
        except OSError:
            break
        if not data:
            break
        os.write(1, data)
        log.write(data)
    if 0 in r:
        os.write(fd, os.read(0, 4096))  # the terminal's answers to the probe
log.close()
