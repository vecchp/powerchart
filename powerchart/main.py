from powerchart.pyHS100 import SmartPlug

p = SmartPlug("192.168.1.101")
p.hs100_status()

#print(codecs.decode(RequestCodes.INFO, 'base64_codec'))
#print(p.encrypt('{"system":{"get_sysinfo":{}}}'))