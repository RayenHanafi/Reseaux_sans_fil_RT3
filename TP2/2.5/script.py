import subprocess
import re

def scan_wifi_networks():
    command = "netsh wlan show networks mode=bssid"
    wifi_data = subprocess.check_output(command, text=True, encoding='utf-8', errors='ignore')

    ssid_blocks = re.split(r'\nSSID\s+\d+\s*:', wifi_data)[1:]
    networks = []

    for block in ssid_blocks:
        ssid_match = re.match(r'(.*)', block.strip())
        signal_match = re.search(r'Signal\s*:\s*(\d+)%', block)

        ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
        signal = int(signal_match.group(1)) if signal_match else 0

        networks.append({'name': ssid, 'signal': signal})

    return networks

def find_strongest_network(networks):
    return max(networks, key=lambda n: n['signal'], default=None)

def should_switch(current_signal, new_signal, threshold=15):
    return new_signal > current_signal + threshold

def connect_to_network(network_name):
    command = f'netsh wlan connect name="{network_name}"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.returncode == 0

if __name__ == "__main__":
    networks = scan_wifi_networks()
    if networks:
        print("Networks found:")
        for n in networks:
            print(f"  {n['name']} - {n['signal']}%")

        strongest = find_strongest_network(networks)
        print(f"\nStrongest network: {strongest['name']} ({strongest['signal']}%)")

        current_signal = 50
        if should_switch(current_signal, strongest['signal']):
            print(f"Should switch from {current_signal}% to {strongest['signal']}%")
        else:
            print("No need to switch")
    else:
        print("No networks found or error")
