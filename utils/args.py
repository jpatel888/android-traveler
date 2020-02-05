import argparse


class Args:
    def __init__(self, constants):
        parser = argparse.ArgumentParser()
        for argument in constants.arguments:
            parser.add_argument(argument.name,
                                help=argument.help,
                                default=argument.default,
                                required=argument.required)
        self.args_namespace = parser.parse_args()

    def __str__(self):
        return str(self.args_namespace)

    def get_minutes(self):
        if not self.args_namespace.minutes:
            return float('inf')
        return float(self.args_namespace.minutes)

    def get_activity_depth(self):
        if not self.args_namespace.activitydepth:
            return float('inf')
        return float(self.args_namespace.activitydepth)

    def get_app_name(self):
        return self.args_namespace.package_start_name
