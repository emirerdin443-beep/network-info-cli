import unittest
from unittest.mock import patch

import network_info


class TestNetworkInfo(unittest.TestCase):
    @patch("network_info.os.listdir", return_value=["eth0", "lo"])
    def test_get_interfaces(self, mock_listdir):
        self.assertEqual(network_info.get_interfaces(), ["eth0", "lo"])

    @patch("network_info.Path.read_text", return_value="UP\n")
    def test_get_interface_state(self, mock_read_text):
        self.assertEqual(network_info.get_interface_state("eth0"), "UP")

    @patch("network_info.Path.read_text", return_value="aa:bb:cc:dd:ee:ff\n")
    def test_get_mac_address(self, mock_read_text):
        self.assertEqual(network_info.get_mac_address("eth0"), "aa:bb:cc:dd:ee:ff")

    @patch("network_info.run_command")
    def test_get_ip_addresses(self, mock_run_command):
        mock_run_command.return_value = (
            "2: eth0    inet 192.168.1.10/24 brd 192.168.1.255 scope global eth0\n"
            "2: eth0    inet6 fe80::1234/64 scope link"
        )
        ipv4, ipv6 = network_info.get_ip_addresses("eth0")
        self.assertEqual(ipv4, ["192.168.1.10"])
        self.assertEqual(ipv6, ["fe80::1234"])

    @patch("network_info.Path.read_text", return_value="nameserver 1.1.1.1\nnameserver 8.8.8.8\n")
    def test_get_dns_servers(self, mock_read_text):
        self.assertEqual(network_info.get_dns_servers(), ["1.1.1.1", "8.8.8.8"])


if __name__ == "__main__":
    unittest.main()
