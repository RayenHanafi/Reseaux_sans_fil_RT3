import subprocess
import re

def scan_wifi_networks():
    command = "netsh wlan show networks mode=bssid"
    wifi_data = subprocess.check_output(command, text=True, encoding='utf-8', errors='ignore')

    # Split by "SSID " blocks
    ssid_blocks = re.split(r'\nSSID\s+\d+\s*:', wifi_data)[1:]

    networks = []
    for block in ssid_blocks:
        ssid_match = re.search(r'^(.*?)\n', block.strip())
        ssid = ssid_match.group(1).strip() if ssid_match else 'Unknown'

        auth = re.search(r'Authentication\s*:\s*(.+)', block)
        bssid = re.search(r'BSSID\s*\d*\s*:\s*(.+)', block)
        signal = re.search(r'Signal\s*:\s*(\d+)%', block)
        channel = re.search(r'Channel\s*:\s*(.+)', block)

        networks.append({
            'name': ssid,
            'security': auth.group(1).strip() if auth else 'Unknown',
            'mac': bssid.group(1).strip() if bssid else 'Unknown',
            'signal': int(signal.group(1)) if signal else 0,
            'channel': channel.group(1).strip() if channel else 'Unknown'
        })

    return networks

if __name__ == "__main__":
    for net in scan_wifi_networks():
        print(net)
