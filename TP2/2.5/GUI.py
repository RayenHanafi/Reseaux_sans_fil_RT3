# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from script import scan_wifi_networks, find_strongest_network, connect_to_network


class WifiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Signal Scanner")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Title
        title = tk.Label(root, text="📡 WiFi Network Scanner", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # Treeview (table)
        columns = ("SSID", "Signal")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
        self.tree.heading("SSID", text="Network Name (SSID)")
        self.tree.heading("Signal", text="Signal Strength (%)")
        self.tree.column("SSID", width=250)
        self.tree.column("Signal", width=150, anchor="center")
        self.tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_networks, width=12)
        self.refresh_btn.grid(row=0, column=0, padx=10)

        self.connect_btn = tk.Button(btn_frame, text="🔗 Connect", command=self.connect_selected, width=12)
        self.connect_btn.grid(row=0, column=1, padx=10)

        # Info label
        self.info_label = tk.Label(root, text="", font=("Segoe UI", 10))
        self.info_label.pack(pady=5)

        # Initial load
        self.refresh_networks()

    def refresh_networks(self):
        """Refresh the list of Wi-Fi networks"""
        self.tree.delete(*self.tree.get_children())
        networks = scan_wifi_networks()

        if not networks:
            messagebox.showwarning("No Networks", "No WiFi networks found.")
            return

        strongest = find_strongest_network(networks)
        for net in networks:
            tag = "strongest" if net == strongest else ""
            self.tree.insert("", "end", values=(net['name'], f"{net['signal']}%"), tags=(tag,))

        # Highlight strongest
        self.tree.tag_configure("strongest", background="#d9fdd3")
        self.info_label.config(
            text=f"Strongest: {strongest['name']} ({strongest['signal']}%)"
        )

    def connect_selected(self):
        """Try connecting to the selected Wi-Fi network"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showinfo("Select a Network", "Please select a network to connect.")
            return

        network_name = self.tree.item(selected)['values'][0]
        success = connect_to_network(network_name)
        if success:
            messagebox.showinfo("Connected", f"✅ Connected to {network_name}")
        else:
            messagebox.showerror("Connection Failed", f"❌ Could not connect to {network_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WifiGUI(root)
    root.mainloop()