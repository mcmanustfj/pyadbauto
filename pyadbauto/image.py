from time import sleep
import scrcpy
from adbutils import adb
import numpy as np
import cv2 



def match_image(image, template_file, threshold=0.8):
    if not isinstance(template_file, str):
        template_file = template_file.__fspath__()
    template = cv2.imread(template_file)
    if template is None:
        raise FileNotFoundError(f"Could not find {template_file}")
    w, h = template.shape[:-1]
    res: np.ndarray = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    return loc[::-1]

def match_image_point(image, template, threshold=0.8) -> tuple[int, int] | None:
    xs, ys = match_image(image, template, threshold)
    if len(xs) == 0:
        return None
    return int(np.median(xs)), int(np.median(ys))

if __name__ == "__main__":
    adb.device_list()[0]
    client = scrcpy.Client(device=adb.device_list()[0],
                        max_width=1080,
                        max_fps=20,
                        )
    client.start(threaded=True)

    try:
        while True:
            frame = client.last_frame
            if frame is not None:
                cv2.imshow("viz", frame)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        client.stop()
        cv2.destroyAllWindows()
        print("Stopped")
        exit(0)