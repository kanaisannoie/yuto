import getpass
from fabric import Connection, Config
from invoke import task
import argparse


class DistroBase:
    def __init__(self):
        self.copy_files = [
            {
                'src': '../keys/ansible-yuto.pub',
                'dst': '/home/ansible-yuto/.ssh/authorized_keys'
            }
        ]


class RHEL(DistroBase):
    def __init__(self):
        super().__init__()
        self.command_list = [
            'sudo useradd ansible-yuto -m -d /home/ansible-yuto -u 60000',
            'echo "ansible-yuto"|passwd --stdin ansible-yuto',
            'usermod -aG wheel ansible-yuto',
            'echo "ansible-yuto ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible-yuto',
            'mkdir -p /home/ansible-yuto/.ssh',
            'chmod 700 /home/ansible-yuto/.ssh',
            'chown -R ansible-yuto:ansible-yuto /home/ansible-yuto/',
            'chmod 600 /home/ansible-yuto/.ssh/authorized_keys'
        ]
        self.username = 'root'


class CentOS7(RHEL):
    def __init__(self):
        super().__init__()


def init(c, distro):
    try:
        for file_dict in distro.copy_files:
            c.put(file_dict['src'], file_dict['dst'])

        for command in distro.command_list:
            c.run(command)
    except:
        print('some error has detected')
    finally:
        print('user ansible-yuto is ready.')


# def init(c):
#    config = Config()
#    # c = Connection(host='localhost', port='10022', user="root",
#    #               connect_kwargs={'password': 'root'})
#    # c = Connection(host=host_properties['hostname'],
#    #               user=host_properties['user'],
#    #               connect_kwargs=host_properties['misc'])
#    print(c)
#
#    try:
#        c.run('sudo useradd ansible-yuto -m -d /home/ansible-yuto -u 60000')
#        c.run('echo "ansible-yuto"|passwd --stdin ansible-yuto')
#        c.run('usermod -aG wheel ansible-yuto')
#        c.run('echo "ansible-yuto ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible-yuto')
#        c.run('mkdir -p /home/ansible-yuto/.ssh')
#        c.run('chmod 700 /home/ansible-yuto/.ssh')
#        c.put('../keys/ansible-yuto.pub', '/home/ansible-yuto/.ssh/authorized_keys')
#        c.run('chown -R ansible-yuto:ansible-yuto /home/ansible-yuto/')
#        c.run('chmod 600 /home/ansible-yuto/.ssh/authorized_keys')
#    except:
#        print('some error has detected')
#    finally:
#        print('user ansible-yuto is ready.')


@task
def ship(c):
    config = Config()
    c = Connection(host='192.168.1.23', user="root",
                   connect_kwargs={'password': 'password'})

    try:
        c.run('userdel --force --remove ansible-yuto')
        c.run('rm -f /etc/sudoers.d/ansible-yuto')
    except:
        pass
    finally:
        print('user ansible-yuto is deleted.')


if __name__ == '__main__':
    distro = CentOS7()
    # host_properties = {
    #        'hostname': 'localhost',
    #        'port': 10022,
    #        'user': 'root',
    #        'misc': {'password': 'root'}
    # sudo_pass = getpass.getpass("What's your sudo password?")
    # config = Config(overrides={'sudo': {'password': sudo_pass}})
    # c = Connection(host='172.31.38.210', port=22, user="ec2-user",
    #               config=config)
    c = Connection(host='192.168.1.31', port=22, user=distro.username, connect_kwargs={"password": "password"})
    init(c, distro)
