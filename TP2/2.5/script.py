import subprocess
import re

def scan_wifi_networks():

    command = "netsh wlan show networks mode=bssid"
    wifi_data = subprocess.check_output(command, text=True)

    networks = []

    print(wifi_data)

    ssid = re.findall(r"SSID\s*\d*\s*:\s*(.+)", wifi_data)
    signal = re.findall(r"Signal\s*:\s*(\d+)%", wifi_data)

    
    network_count = len(ssid)
    if network_count == 0:
        return []  # No networks found
    for i in range(network_count):
        networks.append({
            'name': ssid[i].strip() if i < len(ssid) else 'Unknown',
            'signal': int(signal[i].replace('%', '').strip()) if i < len(signal) else 0,
        })
    
    return networks

def find_strongest_network(networks):
    """Find the network with highest signal strength"""
    if not networks:
        return None
    
    strongest = networks[0]
    for network in networks:
        if network['signal'] > strongest['signal']:
            strongest = network
    
    return strongest

def should_switch(current_signal, new_signal, threshold=15):
    """Decide if we should switch to a better network"""
    return new_signal > current_signal + threshold

def connect_to_network(network_name):
    """Connect to a specific WiFi network"""
    command = f'netsh wlan connect name="{network_name}"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.returncode == 0

# Test the functions
if __name__ == "__main__":
    networks = scan_wifi_networks()
    if networks:
        print("Networks found:")
        for network in networks:
            print(f"  {network['name']} - {network['signal']}%")
        
        strongest = find_strongest_network(networks)
        print(f"\nStrongest network: {strongest['name']} ({strongest['signal']}%)")
        
        # Test switching logic
        current_signal = 50  # Example current signal
        if should_switch(current_signal, strongest['signal']):
            print(f"Should switch from {current_signal}% to {strongest['signal']}%")
        else:
            print("No need to switch")
    else:
        print("No networks found or error")