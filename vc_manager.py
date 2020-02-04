import sys
import os


class VCManager:
    def __init__(self):
        self.vc = None

    def reconnect(self):
        try:
            for p in os.environ['PYTHONPATH'].split(':'):
                if p not in sys.path:
                    sys.path.append(p)
        except:
            pass
        try:
            sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
        except:
            pass
        from com.dtmilano.android.viewclient import ViewClient
        self.vc = ViewClient(*ViewClient.connectToDeviceOrExit(verbose=True))

    def get_root_view(self):
        return self.vc.getRoot()
