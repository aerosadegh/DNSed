import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

from manager import DNSManager
from ui import DNSManagerUI, resource_path


def show_tool():
    ui.show()


def on_tray_icon_activated(reason):
    if reason == QSystemTrayIcon.DoubleClick:
        show_tool()


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
ui = DNSManagerUI()
manager = DNSManager(ui)

# Tray
icon = QIcon(resource_path("assets/tray.png"))

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

menu = QMenu()
option1 = QAction("Show Tool")
option1.triggered.connect(show_tool)
menu.addAction(option1)

quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

tray.activated.connect(on_tray_icon_activated)

tray.setContextMenu(menu)
#################################


def main():

    app.setStyleSheet(
        """
        QWidget {
    background-color: #333;
    color: #fff;
}
QPushButton {
    background-color: #555;
    border: none;
    padding: 5px;
    margin: 5px;
    border-radius: 10px;  /* Smooth the edges */
}
QPushButton:hover {
    background-color: #777;
}
QComboBox {
    background-color: #555;
    border: none;
    padding: 5px;
    margin: 5px;
}
QComboBox QAbstractItemView {
    background-color: #555;
    color: #fff;
}

    """
    )

    show_tool()

    # Move the window to the upper right corner
    screen_resolution = app.desktop().screenGeometry()
    ui.move(screen_resolution.width() - ui.width(), 0)

    app.exec_()


if __name__ == "__main__":
    main()
