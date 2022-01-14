import sys
from PySide2 import QtWidgets, QtGui
from pypresence import Presence
from json import load as jsload
from time import sleep
from threading import Thread

with open('settings.json', 'r') as r:
    settings = jsload(r)


def activity():
    RPC = Presence(settings["app_id"])

    RPC.connect()

    print("Connecting to discord RPC")

    sleep(5)

    activity_settings = settings["activity"]

    try:
        RPC.update(state=activity_settings["state"],
                   details=activity_settings["details"],
                   large_image=activity_settings["large_image"],
                   buttons=activity_settings["buttons"])
        while True:
            input("Rich presence is updated!")
    except KeyboardInterrupt:
        RPC.close()
        print("Disconnecting")
        sys.exit(0)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Discord Activity')
        menu = QtWidgets.QMenu(parent)

        menu.setStyleSheet("""
        QMenu {
        background-color : #222;
        color : #fff;
        }
        
        QMenu::item:selected {
        background-color : rgb(47, 41, 41);
        }
        
        """)
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())

        menu.addSeparator()
        self.setContextMenu(menu)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    Thread(target=main).start()
    activity()
