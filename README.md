# DNSed

DNSed is a Python tool for managing DNS settings on Windows. It enables quick DNS switching, clearing of DNS settings, and retrieval of network interfaces. Ideal for both network administrators and casual users.

## Build .exe file
```
pyinstaller --noconfirm --onefile --windowed --icon ".\dnsed\assets\app.ico" --name "DNSed" --add-data ".\dnsed\assets;assets/"  ".\dnsed\main.py"
```

NOTE: Run the widget as Administrator
