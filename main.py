import sys
import os
import time
import datetime
from navigators.navigator import Navigator
from utils.args import Args
from utils.utils import get_constants


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


def run_navigator(vc, navigator, endtime):
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
    constants, _ = get_constants()
    args = Args(constants)
    minutes = args.get_minutes()
    activity_depth = args.get_activity_depth()
    launch_name = args.get_app_name()
    vc = ViewClient(*ViewClient.connectToDeviceOrExit(verbose=True))
    navigator = Navigator(vc, "bofa")
    starttime = datetime.datetime.now()
    endtime = starttime + datetime.timedelta(minutes=minutes)
    run_navigator(vc, navigator)
