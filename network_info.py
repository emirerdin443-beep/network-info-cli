#!/usr/bin/env python3

import argparse
import os
import re
import socket
import subprocess
from pathlib import Path


def run_command(command):
    """Run a system command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return ""


def get_interfaces():
    """Return available network interfaces."""
    try:
        return sorted(
            name
            for name in os.listdir("/sys/class/net")
            if name
        )
    except OSError:
        return []


def get_interface_state(interface):
    """Return the state of an interface."""
    path = Path(f"/sys/class/net/{interface}/operstate")

    try:
        return path.read_text().strip().upper()
    except OSError:
        return "UNKNOWN"


def get_mac_address(interface):
    """Return the MAC address of an interface."""
    path = Path(f"/sys/class/net/{interface}/address")

    try:
        return path.read_text().strip()
    except OSError:
        return "UNKNOWN"


def get_ip_addresses(interface):
    """Return IPv4 and IPv6 addresses using the ip command."""
    output = run_command(
        ["ip", "-o", "addr", "show", "dev", interface]
    )

    ipv4 = []
    ipv6 = []

    for line in output.splitlines():
        match = re.search(r"\binet\s+([0-9.]+)/", line)
        if match:
            ipv4.append(match.group(1))

        match = re.search(r"\binet6\s+([0-9a-fA-F:]+)/", line)
        if match:
            ipv6.append(match.group(1))

    return ipv4, ipv6


def get_default_routes():
    """Return default IPv4 and IPv6 routes."""
    routes = []

    for command in (
        ["ip", "-4", "route", "show", "default"],
        ["ip", "-6", "route", "show", "default"],
    ):
        output = run_command(command)

        for line in output.splitlines():
            parts = line.split()

            gateway = None
            interface = None

            if "via" in parts:
                gateway = parts[parts.index("via") + 1]

            if "dev" in parts:
                interface = parts[parts.index("dev") + 1]

            routes.append({
                "gateway": gateway or "direct",
                "interface": interface or "unknown",
            })

    return routes


def get_dns_servers():
    """Return DNS servers from resolv.conf."""
    servers = []

    try:
        content = Path("/etc/resolv.conf").read_text()

        for line in content.splitlines():
            line = line.strip()

            if line.startswith("nameserver "):
                server = line.split()[1]

                if server not in servers:
                    servers.append(server)

    except OSError:
        pass

    return servers


def get_hostname():
    """Return the system hostname."""
    try:
        return socket.gethostname()
    except OSError:
        return "unknown"


def print_interface(interface):
    """Print information about a network interface."""
    ipv4, ipv6 = get_ip_addresses(interface)

    print(f"  {interface}")
    print(f"    Status: {get_interface_state(interface)}")
    print(f"    MAC:    {get_mac_address(interface)}")

    if ipv4:
        print("    IPv4:")
        for address in ipv4:
            print(f"      {address}")
    else:
        print("    IPv4:   None")

    if ipv6:
        print("    IPv6:")
        for address in ipv6:
            print(f"      {address}")
    else:
        print("    IPv6:   None")

    print()


def print_routes():
    """Print default network routes."""
    routes = get_default_routes()

    print("Default Routes")
    print("--------------")

    if not routes:
        print("  None")
        print()
        return

    for route in routes:
        print(f"  Gateway:   {route['gateway']}")
        print(f"  Interface: {route['interface']}")
        print()


def print_dns():
    """Print configured DNS servers."""
    servers = get_dns_servers()

    print("DNS Servers")
    print("-----------")

    if not servers:
        print("  None")
    else:
        for server in servers:
            print(f"  {server}")

    print()


def show_network_info():
    """Display complete network information."""
    print("Network Information")
    print("===================")
    print()

    print(f"Hostname: {get_hostname()}")
    print()

    print("Network Interfaces")
    print("-------------------")

    interfaces = get_interfaces()

    if not interfaces:
        print("  No interfaces found")
        print()
    else:
        for interface in interfaces:
            print_interface(interface)

    print_routes()
    print_dns()


def show_interfaces_only():
    """Display only network interfaces."""
    interfaces = get_interfaces()

    if not interfaces:
        print("No network interfaces found.")
        return

    for interface in interfaces:
        print_interface(interface)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Display network interfaces, IP addresses, "
            "DNS, routes, and connection information."
        )
    )

    parser.add_argument(
        "-i",
        "--interfaces",
        action="store_true",
        help="Show network interfaces only",
    )

    parser.add_argument(
        "-r",
        "--routes",
        action="store_true",
        help="Show default routes only",
    )

    parser.add_argument(
        "-d",
        "--dns",
        action="store_true",
        help="Show DNS servers only",
    )

    args = parser.parse_args()

    if args.interfaces:
        show_interfaces_only()
    elif args.routes:
        print_routes()
    elif args.dns:
        print_dns()
    else:
        show_network_info()


if __name__ == "__main__":
    main()
