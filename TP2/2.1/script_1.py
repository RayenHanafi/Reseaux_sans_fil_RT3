import platform
import subprocess
import re
import time
from datetime import datetime

def get_info_WINDOWS():
    try:
        out = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True) 
    except Exception as e:
        return None, f"Erreur netsh: {e}"
    ssid = re.findall(r"^\s*SSID\s*:\s*(.+)$", out, re.MULTILINE)
    signal = re.findall(r"^\s*Signal\s*:\s*(.+)$", out, re.MULTILINE)
    return ssid[0], signal[0] if ssid and signal else (None, None)
# Windows: retourne (ssid, signal) ou (None, erreur)
#this works fine





def main(pause=1.0):
    osname = platform.system()
    print(f"OS détecté: {osname}. Appuyez Ctrl+C pour quitter.\n")


    try:
        ssid = get_info_WINDOWS()[0]
        print(f"Test netsh of SSID:  {ssid or 'inconnu'}")
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            if osname == "Windows":
                ssid, signal = get_info_WINDOWS()
                if ssid is None and signal is None:
                    print(f"[{now}] Pas connecté ou netsh indisponible.")
                else:
                    print(f"[{now}] | Signal: {signal or 'inconnu'}")
            else:
                print(f"[{now}] OS non supporté par ce script: {osname}")
                break
            time.sleep(pause)
    except KeyboardInterrupt:
        print("\nArrêt demandé. Bye.")


if __name__ == "__main__":
    main()





