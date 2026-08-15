import socket


def force_ipv4() -> None:
    """On this network IPv6 connections hang forever; force IPv4 for the whole process."""
    original = socket.getaddrinfo

    def ipv4_only(*args, **kwargs):
        return [ai for ai in original(*args, **kwargs) if ai[0] == socket.AF_INET]

    socket.getaddrinfo = ipv4_only
