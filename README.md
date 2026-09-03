# Network Info CLI

A lightweight command-line tool for displaying network interface, IP address, DNS, route, and connection information.

## Features

* List network interfaces
* Display IPv4 and IPv6 addresses
* Show MAC addresses
* Display default routes
* Show DNS configuration
* Display network connection status
* Human-readable terminal output
* Linux-focused CLI

## Usage

```bash
python3 network_info.py
```

Example:

```text
Network Information
===================

Interfaces:
  lo
    IPv4: 127.0.0.1
    Status: UP

  eth0
    IPv4: 192.168.1.25
    MAC: XX:XX:XX:XX:XX:XX
    Status: UP

Default Route:
  Gateway: 192.168.1.1
  Interface: eth0

DNS:
  1.1.1.1
  8.8.8.8
```

## Requirements

* Python 3.10+
* Linux
* Python standard library

No external Python packages are required.

## Project Status

Early development.

## License

This project is licensed under the Apache License 2.0.
