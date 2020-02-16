#! /usr/bin/env python3


class MarmotBreeder:
    def __init__(self, provider):
        self.provider = provider
        self.marmots = []
        self.count_marmots()

    def count_marmots(self):
        import sys
        sys.path.append('ansible/hosts')
        from test_site_inventory import TestSiteInventory
        test_site = TestSiteInventory('./ansible/hosts/inventory')
        for k, v in test_site.hosts.items():
            if k is not '_meta':
                self.marmots.append(v['hosts'][0])

    def breed(self):
        self.provider.breed(self.marmots)


class DockerProvider:
    def __init__(self):
        import docker
        self.client = docker.from_env()

    def breed(self, marmots):
        print('\nBreeder is Docker\n')
        for container_name in marmots:
            try:
                self.client.containers.run("marmot_centos", name=container_name, detach=True, network='test-site-nw',
                                           privileged=True)
            except:
                print('container {0} is already running.'.format(container_name))


class AwsProvider:
    def __init__(self):
        pass

    def breed(self):
        pass


def main():
    provider = DockerProvider()
    breeder = MarmotBreeder(provider)
    breeder.breed()


if __name__ == '__main__':
    main()
