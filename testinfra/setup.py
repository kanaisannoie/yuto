import yaml
import sys
import os

ANSIBLE_DIR = '../ansible/'
TEST_CODE_DIR = 'tests/'


def main():
    with open(ANSIBLE_DIR + 'site.yml', 'r') as f:
        lines = yaml.load(f)

    roles = [i for i in lines if 'roles' in i.keys()][0]


    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
