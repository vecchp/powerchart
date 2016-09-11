from pyHS100 import SmartPlug, RequestCodes
import codecs
p = SmartPlug("192.168.1.101")
print(p.hs100_status())

#print(codecs.decode(RequestCodes.INFO, 'base64_codec'))
#print(p.encrypt('{"system":{"get_sysinfo":{}}}'))