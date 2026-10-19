# A still for each clip: the liveliest of 9 sampled frames (skips fades and dark title moments).
import subprocess, sys, io
from pathlib import Path
from PIL import Image, ImageStat
for mp4 in sorted(Path('docs/media/clips').glob('*.mp4')):
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4]))
    best = None
    for i in range(1, 10):
        jpg = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(d * i / 10), '-i', mp4, '-frames:v', '1', '-f', 'image2', '-c:v', 'mjpeg', '-q:v', '4', '-'])
        im = Image.open(io.BytesIO(jpg)); st = ImageStat.Stat(im.convert('L'))
        score = st.stddev[0] + st.mean[0] * .5
        if not best or score > best[0]: best = (score, jpg)
    mp4.with_suffix('.jpg').write_bytes(best[1])
