import pytest


class TestClass:
    # test targets
    targets = [
        "bash-completion",
        "tcpdump",
        "lsof",
        "jq",
        "mlocate",
        "unzip",
        "tree"
    ]

    @pytest.mark.parametrize("name", targets)
    def test_packages(self, host, name):
        pkg = host.package(name)
        assert pkg.is_installed
        # assert pkg.version.startswith(version)
