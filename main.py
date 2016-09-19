from powerchart.pyHS100 import SmartPlug

p = SmartPlug("192.168.1.101")
#print(p.system_info)
#print(p.cloud_info)
#print(p.emeter_realtime)
print(p.emeter_daily(8,2016))
#print(codecs.decode(RequestCodes.INFO, 'base64_codec'))
#print(p.encrypt('{"system":{"get_sysinfo":{}}}'))