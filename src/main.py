import sys
import time
import argparse
import numpy as np
import sounddevice as sd
import soundfile as sf
from infi.systray import SysTrayIcon


def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(prog="Logitech G560 Always-On",
                                 description="Keeps the Logitech G560 speakers on at all times.")
parser.add_argument("-l", "--list-devices",
                    action="store_true", help="list all devices with 'G560' in their display name.")
parser.add_argument("-o", "--output-device", type=int_or_str,
                    help="output device (numeric ID or substring)")
parser.add_argument("-a", "--amplitude", type=float,
                    default=0.1, help="amplitude (default: %(default)s)")
parser.add_argument("-f", "--frequency", type=float, default=22,
                    help="frequency in Hz (default: %(default)s)")
parser.add_argument("-d", "--duration", type=float, default=0.1,
                    help="duration (in seconds) to emit tone for (default: %(default)s)")
parser.add_argument("-i", "--interval", type=float, default=180,
                    help="interval (in seconds) between tone being played (default: %(default)s)")
args, remaining_args = parser.parse_known_args()

if args.list_devices:
    for device in sd.query_devices():
        if "G560" in device["name"]:
            print(device["index"], device["name"])
    parser.exit(0)

if not args.output_device:
    print("Device ID is required\n")
    parser.print_help()
    parser.exit(1)

sd.default.device = 1, 22
sd.default.samplerate = 44100
sd.default.channels = 2


def play_tone():
    print(time.strftime("%X %x"), "|",
          f"Emitting tone to device {args.output_device} at {args.frequency}Hz and {args.amplitude} amplitude for {args.duration}s")

    start_index = 0

    try:
        samplerate = sd.query_devices(args.output_device, "output")[
            "default_samplerate"]

        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)

            nonlocal start_index

            t = (start_index + np.arange(frames)) / samplerate
            t = t.reshape(-1, 1)

            outdata[:] = args.amplitude * \
                np.sin(2 * np.pi * args.frequency * t)

            start_index += frames

        with sd.OutputStream(device=args.output_device, channels=1, callback=callback, samplerate=samplerate):
            time.sleep(args.duration)
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        parser.exit(0)
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))
        parser.exit(1)


print("Logitech G560 Always-On")
print("Device:", args.output_device)
print("Amplitude:", args.amplitude)
print("Frequency (Hz):", args.frequency)
print("Duration (Seconds):", args.duration)
print("Interval (Seconds):", args.interval)

interrupted = False


def on_quit_callback():
    print("Quit command issued")
    global interrupted
    interrupted = True


systray = SysTrayIcon("icon.ico", "Logitech G560 Always-On",
                      on_quit=on_quit_callback)
systray.start()

while True:
    if interrupted:
        print("Exiting program")
        break

    play_tone()
    time.sleep(args.interval)
