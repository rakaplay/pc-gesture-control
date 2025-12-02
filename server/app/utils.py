# app/utils.py
import socket
import requests

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=1)
        return True
    except requests.ConnectionError:
        return False

def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return True
        except OSError:
            return False