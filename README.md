# 💡 Logitech G560 Always-On

A small program that fixes an issue with the Logitech Lightsync G560 desktop speakers where the backlights will turn off after five minutes of audio activity, even if you have "Turn off lighting after user inactivity" disabled in the Logitech GHUB settings.

This is a long-standing issue [that has been continually reported](https://www.reddit.com/r/LogitechG/comments/dupf7c/g560_backlightspeakers_turning_off_after/) for years by dozens of users, yet has still not been fixed (unrelated: Logitech is a company worth almost $14b with over 3,100 employees).

This program serves as as simple workaround for those affected users that emits an inaudible tone to the speakers at regular fixed intervals, keeping the backlights from turning off due to inactivity.

## Usage

This is a Windows-only application.

1. [Install Python](https://www.python.org/downloads/) (minimum version 3.8+).

2. Install dependencies.

    ```bash
    pip install -r requirements.txt
    ```

3. Run.

    ```bash
    py ./src/main.py
    ```

The program will appear in your system tray and stay open indefinitely. Right-click the icon in the system tray and select 'Quit' to close.

If your device could not be automatically detected, you can use `--list-devices` and `--list-host-apis` to retrieve a list of devices and corresponding audio host APIs.

```bash
py ./src/main.py --list-devices --list-host-apis
```

Choose the device whose ID is contained in the device ID list of either the Windows DirectSound or MME audio host APIs, then pass its ID to  `--output-device`.

```bash
py ./src/main.py --output-device <ID>
```

---

Use `py ./src/main.py --help` for a list of additional commands and configuration options.

```
usage: Logitech G560 Always-On [-h] [-l] [--list-host-apis] [-o OUTPUT_DEVICE] [-a AMPLITUDE] [-f FREQUENCY] [-d DURATION] [-i INTERVAL]

Keeps the Logitech G560 speakers on at all times.

options:
  -h, --help            show this help message and exit
  -l, --list-devices    list all devices with 'G560' in their display name.
  --list-host-apis      list all sound host APIs.
  -o OUTPUT_DEVICE, --output-device OUTPUT_DEVICE
                        output device ID. If not given, will attempt to automatically detect device ID.
  -a AMPLITUDE, --amplitude AMPLITUDE
                        amplitude (default: 0.1)
  -f FREQUENCY, --frequency FREQUENCY
                        frequency in Hz (default: 22)
  -d DURATION, --duration DURATION
                        duration (in seconds) to emit tone for (default: 0.1)
  -i INTERVAL, --interval INTERVAL
                        interval (in seconds) between tone being played (default: 180)
```

## License

This project is licensed under the [MIT license](https://opensource.org/license/mit/).
