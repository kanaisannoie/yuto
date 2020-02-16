#!/usr/bin/env python3

import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

ANSIBLE_DIR = './ansible/'
SERVERSPEC_DIR = './serverspec/'


class PropertiesHolder:

    def __init__(self):
        self.organized = []
        PROPERTITES_FILE = './serverspec/master-inventory.yml'
        with open(PROPERTITES_FILE, 'r') as f:
            self.raw = yaml.safe_load(f)
        self.make_organized()

    def make_organized(self):
        for k, v in self.raw.items():
            host_attribs = {}
            host_attribs["hostname"] = v[":hostname"]
            host_attribs["ip"] = v[":ip"]
            host_attribs["group"] = v[":group"]
            self.organized.append(host_attribs)


class TemplateBase:
    def __init__(self, properties):
        self.properties = properties
        self.items = []
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        self.tpl = env.get_template(self.TEMPLATE_FILE)

    def write(self):
        rendered = self.tpl.render({'items': self.items})
        with open(self.TARGET_FILE, 'w') as f:
            f.write(rendered)


class SshConfig(TemplateBase):
    def __init__(self, properties):
        self.TEMPLATE_FILE = './bin/ssh_config.j2'
        self.TARGET_FILE = './ansible/ssh_config'
        super().__init__(properties)
        self.items = self.properties.organized
        self.write()
        shutil.copyfile(self.TARGET_FILE, './serverspec/ssh_config')


class AnsibleInventory(TemplateBase):
    def __init__(self, properties):
        self.TEMPLATE_FILE = './bin/inventory.j2'
        self.TARGET_FILE = './ansible/hosts/inventory'
        super().__init__(properties)
        self.organize()
        self.write()

    def organize(self):
        self.items = []
        t = {}
        for hostset in self.properties.organized:
            group_name = hostset["group"]
            if group_name not in t:
                t.setdefault(group_name)
                t[group_name] = []
            t[group_name].append(hostset["hostname"])

        for k, v in t.items():
            item_dict = {}
            item_dict["group"] = k
            item_dict["hosts"] = v
            self.items.append(item_dict)


class HostVars(TemplateBase):
    def __init__(self, properties):
        self.TEMPLATE_FILE = './bin/host_vars.j2'
        self.TARGET_FILE = './ansible/playbooks/host_vars/host_vars.yml'
        super().__init__(properties)
        self.make_host_vars()

    def make_host_vars(self):
        for hostset in self.properties.organized:
            self.items = []
            hostname = hostset["hostname"]
            self.items.append({"hostname": hostname})
            self.write()
            os.rename(self.TARGET_FILE, ANSIBLE_DIR + 'playbooks/host_vars/' + hostname + '.yml')


class GroupVars(TemplateBase):
    def __init__(self, properties):
        super().__init__(properties)

    # make group_vars.yml


class docker_ssh_config(TemplateBase):
    # class for making ssh_config for docker test.
    pass


def main():
    properties = PropertiesHolder()
    print('raw properties:\n', properties.raw)
    print('\norganized properties:\n', properties.organized)
    ssh_config = SshConfig(properties)
    inventory = AnsibleInventory(properties)
    host_vars = HostVars(properties)


if __name__ == '__main__':
    main()
