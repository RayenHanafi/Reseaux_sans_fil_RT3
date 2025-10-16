import platform
import subprocess
import re
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

def get_info_WINDOWS():
    try:
        out = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            text=True,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        return None, None

    ssid = re.findall(r"^\s*SSID\s*:\s*(.+)$", out, re.MULTILINE)
    signal = re.findall(r"^\s*Signal\s*:\s*(.+)$", out, re.MULTILINE)

    # Make sure we return a tuple (ssid, signal) or (None, None)
    return (ssid[0].strip(), signal[0].strip()) if ssid and signal else (None, None)


def main():
    x_data, y_data = [], []
    fig, ax = plt.subplots()
    line, = ax.plot_date(x_data, y_data, '-')
    plt.title("Signal WiFi en temps réel")
    plt.xlabel("Time") 
    plt.ylabel("Signal (%)")
    plt.ylim(0, 100) 

    # date formatting on x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) #hours:minutes:seconds
    fig.autofmt_xdate()  # rotate labels

    def update(frame):
        osname = platform.system()

        if osname == "Windows":
            info = get_info_WINDOWS()
        else:
            print("OS non supporté pour l'instant.")
            info = (None, None)

        #  handle if info = (None, None)
        signal_str = info[1]
        signal = 0

        if signal_str:
            # remove percent sign and whitespace, then check
            tmp = signal_str.replace('%', '').strip()
            if tmp.isdigit():
                signal = int(tmp)
            else:
                signal = 0

        if signal == 0:
            print("Pas connecté ou netsh indisponible / signal invalide.")

        # append and update plot
        x_data.append(datetime.now())
        y_data.append(signal)

        # keep only last 300 points to avoid memory growth
        MAX_POINTS = 300
        if len(x_data) > MAX_POINTS:
            del x_data[: len(x_data) - MAX_POINTS]
            del y_data[: len(y_data) - MAX_POINTS]

        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

        return line,

    animation = FuncAnimation(fig, update, interval=500)
    plt.show()


if __name__ == "__main__":
    main()


# Script for now works on windows only
# To do: add linux support, clean upcode , error handling