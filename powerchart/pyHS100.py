import json
import logging
import socket

from powerchart.autokey_cipher import encrypt_message, decrypt_message

_LOGGER = logging.getLogger(__name__)


class SmartPlug(object):
    """Class to access TPLink Switch.
    Usage example when used as library:
    p = SmartPlug("192.168.1.105")
    # change state of plug
    # query and print current state of plug
    print(p.state)
    Note:
    The library references the same structure as defined for the D-Link Switch
    """

    def __init__(self, ip):
        """Create a new SmartPlug instance identified by the IP."""
        self.ip = ip
        self.port = 9999

    def send_message(self, message: str) -> json:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            data = encrypt_message(message)
            s.send(data)
            reply = s.recv(4096)

        return decrypt_message(reply).decode('utf-8')

    @property
    def system_info(self):
        """Query HS110 for system info."""
        return self.send_message('{"system":{"get_sysinfo":{}}}')

    @property
    def cloud_info(self):
        return self.send_message('{"cnCloud":{"get_info":{}}}')

    @property
    def emeter_realtime(self):
        return self.send_message('{"emeter":{"get_realtime":{}}}')

    def emeter_daily(self, month: int , year: int) -> json:
        command = '{{"emeter":{{"get_daystat":{{"month": {0},"year": {1}}}}}}}'.format(month, year)
        return self.send_message(command)
