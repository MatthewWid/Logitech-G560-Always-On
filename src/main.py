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
parser.add_argument("--list-host-apis", action="store_true",
                    help="list all sound host APIs.")
parser.add_argument("-o", "--output-device", type=int_or_str,
                    help="output device ID. If not given, will attempt to automatically detect device ID.")
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
            print(device["name"])
            print("\tDevice ID:", device["index"])
            print("\tHost API ID:", device["hostapi"])
            print("\tSample Rate (Hz):", device["default_samplerate"])
            print("\tMaximum Channels (Input / Output):",
                  device["max_input_channels"], "/", device["max_output_channels"])

    if not args.list_host_apis:
        parser.exit(0)

if args.list_host_apis:
    for host_api in sd.query_hostapis():
        print(host_api["name"])
        print("\tDevice IDs:", host_api["devices"])
        print("\tDefault Device IDs (Input / Output):",
              host_api["default_input_device"], "/", host_api["default_output_device"])

    parser.exit(0)


def detect_device() -> int | None:
    host_apis = sd.query_hostapis()

    directsound = next(
        host_api for host_api in host_apis if "DirectSound" in host_api["name"])
    mme = next(
        host_api for host_api in host_apis if "MME" in host_api["name"])

    if not directsound and not mme:
        print("Could not automatically detect device: Neither DirectSound nor MME host APIs could be found\n")
        return None

    devices = [device for device in sd.query_devices()
               if "G560" in device["name"]]

    if directsound:
        for device in devices:
            if (device["index"] in directsound["devices"]):
                return device["index"]

    if mme:
        for device in devices:
            if (device["index"] in mme["devices"]):
                return device["index"]

    print("Could not automatically detect device: Device not found under DirectSound or MME host API device list\n")

    return None


output_device_id = args.output_device or detect_device()

if not output_device_id:
    print("No device found\n")
    parser.print_help()
    parser.exit(1)

sd.default.device = None, output_device_id
sd.default.samplerate = 44100
sd.default.channels = 2


def play_tone():
    print(time.strftime("%X %x"), "|",
          f"Emitting tone to device {output_device_id} at {args.frequency}Hz and {args.amplitude} amplitude for {args.duration}s")

    start_index = 0

    try:
        samplerate = sd.query_devices(output_device_id, "output")[
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

        with sd.OutputStream(device=output_device_id, channels=1, callback=callback, samplerate=samplerate):
            time.sleep(args.duration)
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        parser.exit(0)
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))
        parser.exit(1)


print("Logitech G560 Always-On")
print("\tDevice ID:", output_device_id)
print("\tAmplitude:", args.amplitude)
print("\tFrequency (Hz):", args.frequency)
print("\tDuration (Seconds):", args.duration)
print("\tInterval (Seconds):", args.interval)
print("\n")

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
