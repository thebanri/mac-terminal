# Writes a recorded stream of frames to the terminal and records how long
# Terminal.app took to take it: cat returns once the pty has drained.
import os, sys, time
path, out = sys.argv[1], sys.argv[2]
data = open(path, "rb").read()
t = time.time()
fd = sys.stdout.fileno()
view = memoryview(data)
while view:
    n = os.write(fd, view[:65536])
    view = view[n:]
os.fsync(fd) if False else None
dt = time.time() - t
with open(out, "a") as f:
    f.write("%s %d bytes %.2f s %.2f MB/s %.1f frames/s\n" % (os.path.basename(path), len(data), dt, len(data) / dt / 1e6, 150 / dt))
