from adbutils import adb
from .client import Client

adb.device_list()[0]
client = Client(device=adb.device_list()[0],
                max_width=1080,
                max_fps=20)

with Client() as client:
    breakpoint()
    client.stream_video()