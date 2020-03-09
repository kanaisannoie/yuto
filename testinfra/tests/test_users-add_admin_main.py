import pytest


class TestClass:
    ADMIN_USER = 'jkanai'

    def test_add_admin_user(self, host):
        passwd = host.file("/etc/passwd")
        assert passwd.contains(self.ADMIN_USER)
        assert passwd.user == "root"
        assert passwd.group == "root"
        assert passwd.mode == 0o644
