import json

import dns


class DNSManager:
    def __init__(self, ui):
        self.ui = ui
        try:
            with open("dns_profiles.json", "r", encoding="utf-8") as f:
                self.profiles = json.load(f)
        except FileNotFoundError:
            self.default_dns()
            self.profiles = {
                "403 Online": ["10.202.10.202", "10.202.10.102"],
                "SheCan": ["178.22.122.100", "185.51.200.2"],
                "Google": ["8.8.8.8", "8.8.4.4"],
                "Cloudflare": ["1.1.1.1", "1.0.0.1"],
            }

        self.ui.profile_selector.addItems(self.profiles.keys())
        self.ui.set_button.clicked.connect(self.on_set_dns)
        self.ui.clear_button.clicked.connect(self.on_clear_dns)

        interface = self.ui.interface_selector.currentText()
        self.set_label(interface)
        self.update_interfaces()

    def default_dns(self):
        with open("dns_profiles.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "403 Online": ["10.202.10.202", "10.202.10.102"],
                    "SheCan": ["178.22.122.100", "185.51.200.2"],
                    "Google": ["8.8.8.8", "8.8.4.4"],
                    "Cloudflare": ["1.1.1.1", "1.0.0.1"],
                },
                f,
            )

    def update_interfaces(self):
        current_interfaces = [
            self.ui.interface_selector.itemText(i)
            for i in range(self.ui.interface_selector.count())
        ]
        new_interfaces = dns.get_network_interfaces()

        # Add new interfaces
        for interface in new_interfaces:
            if interface not in current_interfaces:
                self.ui.interface_selector.addItem(interface)

        # Remove non-existent interfaces
        for interface in current_interfaces:
            if interface not in new_interfaces:
                index = self.ui.interface_selector.findText(interface)
                if index >= 0:
                    self.ui.interface_selector.removeItem(index)

    def get_profile_name(self, dns):
        for name, configs in self.profiles.items():
            if dns in configs:
                return f"✅ {name}"
        return dns

    def set_label(self, interface):
        self.update_interfaces()
        self.ui.status_label.setText(self.get_profile_name(dns.get_dns(interface)))

    def on_set_dns(self):
        interface = self.ui.interface_selector.currentText()
        profile = self.ui.profile_selector.currentText()
        dns_servers = self.profiles[profile]
        dns.change_dns(interface, *dns_servers)
        self.set_label(interface)

    def on_clear_dns(self):
        interface = self.ui.interface_selector.currentText()
        dns.clear_dns(interface)
        self.set_label(interface)
