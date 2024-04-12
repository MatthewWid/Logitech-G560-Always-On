# 💡 Logitech G560 Always-On

A small program that fixes an issue with the Logitech Lightsync G560 desktop speakers where the backlights will turn off after five minutes of audio activity, even if you have "Turn off lighting after user inactivity" disabled in the Logitech GHUB settings.

This is a long-standing issue [that has been continually reported](https://www.reddit.com/r/LogitechG/comments/dupf7c/g560_backlightspeakers_turning_off_after/) for years by dozens of users, yet has still not been fixed (unrelated: Logitech is a company worth almost $14b with over 3,100 employees).

This program serves as as simple workaround for those affected users that emits an inaudible tone to the speakers at regular fixed intervals, keeping the backlights from turning off due to inactivity.

## Usage

This is a Windows-only application.

1. [Install Python](https://www.python.org/downloads/) (minimum version 3.8+).

2. Install dependencies.

    ```
    pip install -r requirements.txt
    ```

3. Locate your device ID (typically `Logitech G560 Gaming Speakers`).

    ```
    py ./src/main.py --list-devices
    ```

    You might see duplicate devices in the list. Any should work.

4. Start the program, giving the device ID or name of your speakers.

    ```
    py ./src/main.py --output-device <ID>
    ```

The program will appear in your system tray and stay open indefinitely. Right-click the icon in the system tray and select 'Quit' to close.

---

Use `py ./src/main.py --help` for a list of additional commands and configuration options.

```
usage: Logitech G560 Always-On [-h] [-l] [-o OUTPUT_DEVICE] [-a AMPLITUDE] [-f FREQUENCY] [-d DURATION] [-i INTERVAL]

Keeps the Logitech G560 speakers on at all times.

options:
  -h, --help            show this help message and exit
  -l, --list-devices    list all devices with 'G560' in their display name.
  -o OUTPUT_DEVICE, --output-device OUTPUT_DEVICE
                        output device (numeric ID or substring)
  -a AMPLITUDE, --amplitude AMPLITUDE
                        amplitude (default: 0.1)
  -f FREQUENCY, --frequency FREQUENCY
                        frequency in Hz (default: 40)
  -d DURATION, --duration DURATION
                        duration (in seconds) to emit tone for (default: 0.1)
  -i INTERVAL, --interval INTERVAL
                        interval (in seconds) between tone being played (default: 240)
```

## License

This project is licensed under the [MIT license](https://opensource.org/license/mit/).
