#! /usr/bin/env python3

import configparser
import json
import inspect


class DynamicInventory:
    def __init__(self, inventory_path):
        self.hosts = {
            "_meta": {"hostvars": {}}
        }
        self.test_site_hosts = self.hosts
        self.static_inventory = configparser.ConfigParser(allow_no_value=True)
        self.static_inventory.read(inventory_path, 'UTF-8')
        self.make_dynamic_inventory()

    def make_dynamic_inventory(self):
        for group_name in self.static_inventory.sections():
            self.hosts[group_name] = {}
            self.hosts[group_name]["hosts"] = []
            for key in self.static_inventory[group_name]:
                self.hosts[group_name]["hosts"].append(key)
                if inspect.stack()[1][3] == 'make_test_site_inventory':
                    break
            self.hosts[group_name]["vars"] = {}

    @staticmethod
    def get_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--path',
                            help='relative path to ansible static inventory file. e.g. "./ansible/hosts/inventory"',
                            default="./hosts/inventory")
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store_true')
        args = parser.parse_args()
        return args


if __name__ == '__main__':
    inventory_path = DynamicInventory.get_args().path
    di = DynamicInventory(inventory_path)
    di.make_dynamic_inventory()
    print(json.dumps(di.hosts, indent=4, sort_keys=True))
