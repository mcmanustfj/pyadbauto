import subprocess

def get_point():
    event_proc = subprocess.Popen(['adb', 'shell', 'getevent -l'], stdout=subprocess.PIPE)
    started = False
    x, y = -1, -1
    i = 0
    if not event_proc.stdout:
        raise RuntimeError('No output detected')
    for line in iter(event_proc.stdout.readline, ''):
        i += 1
        line = line.decode('utf-8')
        if not line.startswith('/dev/input/event'):
            continue
        event_name, event_type, event_value = line.split()[-3:]
        if not started:
            if event_type =='BTN_TOUCH' and event_value == 'DOWN':
                started = True
                continue
            else:
                continue
        if event_type == 'ABS_MT_POSITION_X':
            x = int(event_value, 16)
        if event_type == 'ABS_MT_POSITION_Y':
            y = int(event_value, 16)
        if event_type == 'BTN_TOUCH' and event_value == 'UP':
            event_proc.kill()
            return x, y
        if i > 500:
            event_proc.kill()
            raise RuntimeError('Tap took too long')
        

if __name__ == '__main__':
    print(get_point())