import logging
import socket
import codecs
import json
from powerchart.autokey_cipher import encrypt_message, decrypt_message

_LOGGER = logging.getLogger(__name__)


# https://github.com/sausheong/hs1xxplug/blob/master/hs110.go

class RequestCodes(object):
    ON = b'AAAAKtDygfiL/5r31e+UtsWg1Iv5nPCR6LfEsNGlwOLYo4HyhueT9tTu36Lfog=='
    OFF = b'AAAAKtDygfiL/5r31e+UtsWg1Iv5nPCR6LfEsNGlwOLYo4HyhueT9tTu3qPeow=='
    INFO = b'AAAAI9Dw0qHYq9+61/XPtJS20bTAn+yV5o/hh+jK8J7rh+vLtpbr'
    POWER_CONSOMPTION = b'AAAAJNDw0rfav8uu3P7Ev5+92r/LlOaD4o76k/6buYPtmPSYuMXlmA=='


class SmartPlug(object):
    """Class to access TPLink Switch.
    Usage example when used as library:
    p = SmartPlug("192.168.1.105")
    # change state of plug
    p.state = "OFF"
    p.state = "ON"
    # query and print current state of plug
    print(p.state)
    Note:
    The library references the same structure as defined for the D-Link Switch
    """

    def __init__(self, ip):
        """Create a new SmartPlug instance identified by the IP."""
        self.ip = ip
        self.port = 9999
        self._error_report = False

    @property
    def state(self):
        """Get the device state (i.e. ON or OFF)."""
        response = self.hs100_status()
        if response is None:
            return 'unknown'
        elif response == 0:
            return "OFF"
        elif response == 1:
            return "ON"
        else:
            _LOGGER.warning("Unknown state %s returned" % str(response))
            return 'unknown'

    @state.setter
    def state(self, value):
        """Set device state.
        :type value: str
        :param value: Future state (either ON or OFF)
        """
        if value.upper() == 'ON':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            on_str = ('0000002ad0f281f88bff9af7d5'
                      'ef94b6c5a0d48bf99cf091e8b7'
                      'c4b0d1a5c0e2d8a381f286e793'
                      'f6d4eedfa2dfa2')
            data = codecs.decode(on_str, 'hex_codec')
            s.send(data)
            s.close()

        elif value.upper() == 'OFF':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            off_str = ('0000002ad0f281f88bff9af7d5'
                       'ef94b6c5a0d48bf99cf091e8b7'
                       'c4b0d1a5c0e2d8a381f286e793'
                       'f6d4eedea3dea3')
            data = codecs.decode(off_str, 'hex_codec')
            s.send(data)
            s.close()

        else:
            raise TypeError("State %s is not valid." % str(value))

    def hs100_status(self):
        """Query HS100 for relay status."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        skip = 4
        code = 171
        response = ""
        data = encrypt_message('{"system":{"get_sysinfo":{}}}')
        print(data)
        s.send(data)
        reply = s.recv(4096)
        s.shutdown(1)
        s.close()

        print(decrypt_message(reply))


