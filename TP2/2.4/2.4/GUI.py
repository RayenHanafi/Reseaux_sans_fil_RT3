import tkinter as tk
from tkinter import ttk
from script import scan_wifi_networks  # IMPORT YOUR CORE LOGIC


class WiFiScannerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        """Setup all GUI elements"""
        self.root.title("🌐 WiFi Network Scanner")
        self.root.geometry("700x600")
        self.root.configure(bg='white')

        # Create styles for progress bars
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Header
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="WiFi Network Scanner",
                 font=('Arial', 20, 'bold'), fg='white', bg='#4CAF50').pack(expand=True)

        # Button frame
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.pack(fill='x', pady=10)

        # Scan button
        scan_btn = tk.Button(button_frame, text="🔍 Scan Networks",
                             command=self.scan_wifi_gui, font=('Arial', 12, 'bold'),
                             bg='#2196F3', fg='white', padx=20, pady=10)
        scan_btn.pack(side='left', padx=10)

        # Refresh button
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh",
                                command=self.scan_wifi_gui, font=('Arial', 12),
                                bg='#FF9800', fg='white', padx=20, pady=10)
        refresh_btn.pack(side='left', padx=10)

        # Results area with scrollbar
        self.setup_results_area()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to scan networks")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='sunken',
                              anchor='w', font=('Arial', 9), bg='lightgray')
        status_bar.pack(fill='x', side='bottom')

    def setup_results_area(self):
        """Setup the scrollable results area"""
        results_container = tk.Frame(self.root, bg='white')
        results_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Canvas and scrollbar for results
        self.canvas = tk.Canvas(results_container, bg='white')
        scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # This is our results frame that we'll use to display networks
        self.results_frame = self.scrollable_frame

    def scan_wifi_gui(self):
        """GUI version that uses the core logic"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Show scanning message
        scanning_label = tk.Label(self.results_frame, text="🔍 Scanning for WiFi networks...",
                                  font=('Arial', 12, 'bold'), fg='blue')
        scanning_label.pack(pady=10)
        self.root.update()

        # USE YOUR CORE LOGIC FUNCTION
        networks = scan_wifi_networks()

        if networks is None:
            error_label = tk.Label(self.results_frame, text=" No networks detected",
                                   font=('Arial', 11, 'bold'), fg='red')
            error_label.pack(pady=10)
            return

        # Remove scanning message
        scanning_label.destroy()

        # Display networks using the data from core logic
        for i, network in enumerate(networks, 1):
            # Create a frame for each network
            network_frame = tk.Frame(self.results_frame, relief='groove', bd=2,
                                     bg='#f0f0f0', padx=10, pady=10)
            network_frame.pack(fill='x', padx=5, pady=5)

            # Network header
            header_frame = tk.Frame(network_frame, bg='#e0e0e0')
            header_frame.pack(fill='x')

            tk.Label(header_frame, text=f" Network #{i}",
                     font=('Arial', 12, 'bold'), bg='#e0e0e0').pack(side='left')
            tk.Label(header_frame, text=network['name'], font=('Arial', 12, 'bold'),
                     fg='blue', bg='#e0e0e0').pack(side='left', padx=(10, 0))

            # Security
            info_frame = tk.Frame(network_frame, bg='#f0f0f0')
            info_frame.pack(fill='x', pady=2)
            tk.Label(info_frame, text=" Security:", font=('Arial', 9, 'bold'),
                     bg='#f0f0f0').pack(side='left')
            tk.Label(info_frame, text=network['security'], font=('Arial', 9),
                     fg='darkgreen', bg='#f0f0f0').pack(side='left', padx=(5, 0))

            # MAC Address
            info_frame = tk.Frame(network_frame, bg='#f0f0f0')
            info_frame.pack(fill='x', pady=2)
            tk.Label(info_frame, text=" MAC:", font=('Arial', 9, 'bold'),
                     bg='#f0f0f0').pack(side='left')
            tk.Label(info_frame, text=network['mac'], font=('Arial', 9),
                     fg='darkgreen', bg='#f0f0f0').pack(side='left', padx=(5, 0))

            # Signal with progress bar
            info_frame = tk.Frame(network_frame, bg='#f0f0f0')
            info_frame.pack(fill='x', pady=2)
            tk.Label(info_frame, text="Signal:", font=('Arial', 9, 'bold'),
                     bg='#f0f0f0').pack(side='left')

            # Signal value with color
            signal_value = network['signal']
            color = 'green' if signal_value > 70 else 'orange' if signal_value > 40 else 'red'
            tk.Label(info_frame, text=f"{signal_value}%", font=('Arial', 9, 'bold'),
                     fg=color, bg='#f0f0f0').pack(side='left', padx=(5, 10))

            # Progress bar for signal strength
            progress = ttk.Progressbar(info_frame, orient='horizontal',
                                       length=150, mode='determinate')
            progress.pack(side='left')
            progress['value'] = signal_value

            # Style the progress bar based on signal strength
            if signal_value > 70:
                self.style.configure("green.Horizontal.TProgressbar", background='green')
                progress.configure(style="green.Horizontal.TProgressbar")
            elif signal_value > 40:
                self.style.configure("orange.Horizontal.TProgressbar", background='orange')
                progress.configure(style="orange.Horizontal.TProgressbar")
            else:
                self.style.configure("red.Horizontal.TProgressbar", background='red')
                progress.configure(style="red.Horizontal.TProgressbar")

            # Channel
            info_frame = tk.Frame(network_frame, bg='#f0f0f0')
            info_frame.pack(fill='x', pady=2)
            tk.Label(info_frame, text=" Channel:", font=('Arial', 9, 'bold'),
                     bg='#f0f0f0').pack(side='left')
            tk.Label(info_frame, text=network['channel'], font=('Arial', 9),
                     fg='purple', bg='#f0f0f0').pack(side='left', padx=(5, 0))


# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiScannerGUI(root)
    root.mainloop()