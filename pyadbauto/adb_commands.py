import subprocess

def adb_shell(cmd):
    return subprocess.run(['adb', 'shell', cmd], stdout=subprocess.PIPE).stdout.decode('utf-8')

def swipe(x1, y1, x2, y2, duration=200):
    adb_shell(f'input swipe {x1} {y1} {x2} {y2} {duration}')

def tap(x, y):
    adb_shell(f'input tap {x} {y}')

def keyevent(key):
    adb_shell(f'input keyevent {key}')


def screencap() -> bytes:
    return subprocess.run(['adb', 'exec-out', "screencap -p"], stdout=subprocess.PIPE).stdout