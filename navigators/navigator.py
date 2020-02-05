from collections import defaultdict
from adb.adb_interactor import ADBInteractor
import os
import time


class Navigator:
    def __init__(self, vc, package_name):
        self.vc = vc
        self.olid = "oid_10011443679"
        self.password = "T0gether"
        self.package_name = package_name
        self.last_activity_name = None
        self.visited_map = defaultdict(lambda: None)
        self.adb = ADBInteractor()

    def press_back_until_in_app(self, device_serial):
        seconds_between = 0.5
        while not (self.adb.in_app() or seconds_between <= 0.06):
            seconds_between -= 0.05
            self.adb.press_back_button()
            print(seconds_between)
            time.sleep(seconds_between)
        if not self.adb.in_app():
            self.adb.restart(device_serial)

    def blacklisted(self, text, content_description):
        blacklist = ["Transfer", "Bill Pay", "Deposit Checks", "Menu", "Go back to previous screen", "Sign Out Button"]
        for black in blacklist:
            if black in text or black in content_description:
                return True
        return False

    def sequential_click(self, current_activity_name, new_view_list):
        """
        will need to eventually use params to traverse tree
        :param stored_root_element:
        :param new_root_element:
        :return:
        """
        # traverse stored_root_element and get all leaf views in list
        # traverse new_root_element and get all leaf views in list
        # for each in stored,
        view_length = max(len(new_view_list), len(self.visited_map[current_activity_name]))
        idx = 0
        touched = False
        for stored_view, new_view in zip(self.visited_map[current_activity_name][:view_length], new_view_list[:view_length]):
            if not hasattr(stored_view, 'clicked'):
                if not self.blacklisted(new_view.map['text'], new_view.map['content-desc']):
                    view_print_data = new_view.map['text'] if new_view.map['text'] else new_view.map['content-desc']
                    print("  View Found:", "\"" + view_print_data + "\"")
                    new_view.touch()
                    touched = True
                    self.visited_map[current_activity_name][idx].clicked = True
                    break
            idx += 1
        if touched:
            time.sleep(3)
            self.take_screenshot(current_activity_name)
            self.post_touched()

    def post_touched(self):
        if "SignOutActivity" in Navigator.get_top_activity_name():
            views = self.vc.dump()
            views[2].touch()
        elif "MobileHomePageActivity" in Navigator.get_top_activity_name():
            time.sleep(2)
        elif "MainActivity" not in Navigator.get_top_activity_name():
            self.adb.press_back_button()

    def find_and_click_next(self, current_activity_name, view_list):
        view_list = [v for v in view_list if len(v.children) == 0]
        print("Attempting Next View Click")
        if self.visited_map[current_activity_name] is None:
            self.visited_map[current_activity_name] = view_list
        stored_view_list = self.visited_map[current_activity_name]
        if self.view_hierarchy_child_changed(stored_view_list, view_list):
            print("  View Hierarchy Changed..")
        else:
            print("  View Hierarchy Not Changed..")
        self.sequential_click(current_activity_name, view_list)

    def navigate(self, current_activity_name, current_package, view_list, device_serial):
        print("Nav Run Again")
        if "MobileHomePageActivity" in current_activity_name:
            print("Exception Activity Found: MobileHomePageActivity")
            print("   Exception Action: login_to_bofa_app")
            self.log_in()
            time.sleep(7)
            return
        elif "SignOutActivity" in current_activity_name:
            views = self.vc.dump()
            views[2].touch()
            return
        if current_activity_name == self.last_activity_name:
            # self.handle_no_activity_change()
            # TODO: need to prioritize new views on click and remember the click created new views
            self.find_and_click_next(current_activity_name, view_list)
        elif self.package_name not in current_package:
            return
            #self.press_back_until_in_app(device_serial)
        else:  # We're in the bofa app in a different activity
            self.find_and_click_next(current_activity_name, view_list)
        self.last_activity_name = current_activity_name

    def log_in(self):
        try:
            print("  Entering Online ID")
            self.vc.findViewById("com.infonow.bofa.test:id/et_signin_olid").setText(self.olid)
            print("  Entering Passcode")
            self.vc.findViewById("com.infonow.bofa.test:id/et_signin_passcode").setText(self.password)
            self.adb.press_back_button()
            print("  Signing In")
            self.vc.findViewById("com.infonow.bofa.test:id/btn_signin_continue").touch()
        except:
            pass

    def view_hierarchy_child_changed(self, last_hierarchy_child, this_hierarchy_child):
        if len(last_hierarchy_child) != len(this_hierarchy_child):
            return True
        for old_child, new_child in zip(last_hierarchy_child, this_hierarchy_child):
            if self.view_hierarchy_child_changed(old_child.children, new_child.children):
                return True
        return False

    def take_screenshot(self, activity_name):
        self.adb.take_screenshot(activity_name)

    def restart_app(self):
        self.adb.restart(self.vc.serialno)

    @staticmethod
    def get_top_package_name():
        return os.popen('adb shell "dumpsys activity | grep top-activity"').read().split(" ")[-2]

    @staticmethod
    def get_top_activity_name():
        return os.popen('adb shell dumpsys window windows | grep -E "mCurrentFocus"').read().strip().split(" ")[-1]
