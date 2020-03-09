import yaml
import sys
import shutil
from pathlib import Path

CURRENT_DIR = Path()
ANSIBLE_DIR = Path('../ansible')
ROLES_DIR = Path('roles')
TEST_CODE_DIR = Path('tests')
TEST_FILE = Path('main.py')
MAIN_PLAYBOOK = Path('site.yml')


def main():
    with open(ANSIBLE_DIR / MAIN_PLAYBOOK, 'r') as f:
        lines = yaml.load(f, Loader=yaml.FullLoader)
    roles = lines[0]["roles"]

    for r in roles:
        role = Path(r)
        src = ANSIBLE_DIR / ROLES_DIR / role / TEST_CODE_DIR / TEST_FILE
        dst_filename = "test_" + str(role).replace('/', '-') + "_" + str(TEST_FILE)
        dst = CURRENT_DIR / TEST_CODE_DIR / Path(dst_filename)

        try:
            shutil.copyfile(src, dst)
            print("copy the {} role's test to testinfra.".format(str(role)))
        except OSError as e:
            print("There is no test in {} role.".format(str(role)))

    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
