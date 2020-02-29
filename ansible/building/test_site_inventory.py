#! /usr/bin/env python3

from dynamic_inventory import DynamicInventory
import json
import argparse


class TestSiteInventory(DynamicInventory):
    def __init__(self, inventory_path):
        super().__init__(inventory_path)
        self.make_test_site_inventory()

    def make_test_site_inventory(self):
        self.make_dynamic_inventory()


if __name__ == '__main__':
    inventory_path = TestSiteInventory.get_args().path
    test_site = TestSiteInventory(inventory_path)
    # test_site.make_test_site_inventory()
    print(json.dumps(test_site.hosts, indent=4, sort_keys=True))
