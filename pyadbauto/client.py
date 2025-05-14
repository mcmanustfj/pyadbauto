from time import sleep, time
from typing import Any
import cv2
from numpy import dtype, integer, ndarray
import scrcpy
from . import image


class Client:
    client: scrcpy.Client

    def __init__(self, **kwargs):
        self.client = scrcpy.Client(**kwargs)

    def __enter__(self):
        self.client.start(threaded=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    def start(self, threaded=True, daemon_threaded=False):
        self.client.start(threaded=threaded, daemon_threaded=daemon_threaded)

    def stop(self):
        self.client.stop()

    def __del__(self):
        self.client.stop()
        cv2.destroyAllWindows()

    def tap(self, x, y):
        self.client.control.touch(x, y, scrcpy.ACTION_DOWN)
        sleep(0.01)
        self.client.control.touch(x, y, scrcpy.ACTION_UP)

    def swipe(self, x1, y1, x2, y2, duration=0.1):
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        breakpoints = 10
        segment_length = distance / breakpoints
        segment_duration = duration / breakpoints

        self.client.control.swipe(x1, y1, x2, y2, segment_length, segment_duration)

    def image_match(self, template, threshold=0.8):
        return image.match_image_point(self.client.last_frame, template, threshold)

    def wait_for_image(
        self, template, threshold=0.8, timeout=3, disappear=False, error=True
    ):
        start = time()
        while time() - start < timeout:
            match = self.image_match(template, threshold)
            if match is not None and not disappear:
                return match
            if match is None and disappear:
                return
            sleep(0.1)
        if disappear and error:
            raise TimeoutError(f"Image {template} did not disappear in {timeout} s")
        if error:
            raise TimeoutError(f"Could not find image {template} in {timeout} s")

    def last_frame(self) -> ndarray[Any, dtype[integer]]:
        if self.client.last_frame is None:
            raise ValueError("No frame available")
        return self.client.last_frame

    def stream_video(self):
        try:
            while True:
                frame = self.client.last_frame
                if frame is not None:
                    cv2.imshow("viz", frame)
                cv2.waitKey(1)
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
