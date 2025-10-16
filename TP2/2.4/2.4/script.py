import subprocess
import re


def scan_wifi_networks():

    command = "netsh wlan show networks mode=bssid"
    wifi_data = subprocess.check_output(command, text=True)

    # lines = wifi_data.split('\n')

    networks = []

    ssid = re.findall(r"SSID\s*\d*\s*:\s*(.+)", wifi_data, re.MULTILINE)
    authentication = re.findall(r"^\s*Authentication\s*:\s*(.+)$", wifi_data, re.MULTILINE)
    bssid = re.findall(r"^\s*BSSID\s*:\s*(.+)$", wifi_data, re.MULTILINE)
    signal = re.findall(r"Signal\s*:\s*(\d+)%", wifi_data, re.MULTILINE)
    channel = re.findall(r"^\s*Channel\s*:\s*(.+)$", wifi_data, re.MULTILINE)
    
    network_count = len(ssid)
    if network_count == 0:
        return []  # No networks found
    for i in range(network_count):
        networks.append({
            'name': ssid[i].strip() if i < len(ssid) else 'Unknown',
            'security': authentication[i].strip() if i < len(authentication) else 'Unknown',
            'mac': bssid[i].strip() if i < len(bssid) else 'Unknown',
            'signal': int(signal[i].replace('%', '').strip()) if i < len(signal) else 0,
            'channel': channel[i].strip() if i < len(channel) else 'Unknown'
        })

    return networks

print(scan_wifi_networks())