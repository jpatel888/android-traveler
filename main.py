import sys
import os
import time
from navigator_list import Navigator
import datetime


try:
    for p in os.environ['PYTHONPATH'].split(':'):
        if not p in sys.path:
            sys.path.append(p)
except:
    pass

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient


"""

Example Command:

./septaNav --minutes 2 --activitydepth 3


"""


minutes = 4
print("Running septaNav for", minutes, "minutes with an activity depth of 3")
starttime = datetime.datetime.now()
endtime = starttime + datetime.timedelta(minutes=minutes)

def run_navigator(vc, navigator):
    while datetime.datetime.now() < endtime:
        try:
            current_package = Navigator.get_top_package_name()
            if "bofa" not in current_package:
                navigator.restart_app()
            else:
                current_activity = Navigator.get_top_activity_name()
                time.sleep(1)
                navigator.take_screenshot(current_activity)
                root_element = vc.dump()
                navigator.navigate(current_activity, current_package, root_element, vc.serialno)
        except:
            pass
        time.sleep(3)
    print(minutes, "minutes have passed, terminating septaNav")


if __name__ == '__main__':
    vc = ViewClient(*ViewClient.connectToDeviceOrExit(verbose=True))
    navigator = Navigator(vc, "bofa")
    run_navigator(vc, navigator)
