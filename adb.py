import os
from datetime import datetime


class ADB:
    def __init__(self):
        self.restart_cmd = "adb -s {{device}} shell am start -S com.infonow.bofa.test/.Launcher"
        self.screen_cap_commands = [
            "adb shell screencap -p /sdcard/screen_{{activity_name}}_{{dt}}.png",
            "adb pull /sdcard/screen_{{activity_name}}_{{dt}}.png",
            "adb shell rm /sdcard/screen_{{activity_name}}_{{dt}}.png"
        ]

    def take_screenshot(self, activity_name):
        activity_name = activity_name.replace("/", ".")
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y..%H.%M.%S")
        for cmd in self.screen_cap_commands:
            _ = os.popen(cmd.replace("{{activity_name}}", activity_name).replace("{{dt}}", dt_string)).read()
        old = "screen_{{activity_name}}_{{dt}}.png".replace("{{activity_name}}", activity_name).replace("{{dt}}", dt_string)
        new = "screenshots/" + old
        os.rename(old, new)

    def restart(self, device_name):
        print("Killing Possible Processes")
        print("Starting App")
        _ = os.popen(self.restart_cmd.replace("{{device}}", device_name)).read()

    def in_app(self):
        pass

    def press_back_button(self):
        print("  Sending back code")
        os.system("adb shell input keyevent 4")

    def kill_app_and_restart(self):
        pass
