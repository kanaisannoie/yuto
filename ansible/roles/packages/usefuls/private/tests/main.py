import pytest


class TestClass:
    # test targets
    targets = [
        "git",
        "fish",
        "tmux",
        "tig"
    ]

    @pytest.mark.parametrize("name", targets)
    def test_packages(self, host, name):
        pkg = host.package(name)
        assert pkg.is_installed
        # assert pkg.version.startswith(version)
