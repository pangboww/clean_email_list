__author__ = 'pangboww'

import urllib2
# from TorCtl import TorCtl
#
# proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
# opener = urllib2.build_opener(proxy_support)
#
# def newId():
#     conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="your_password")
#     conn.send_signal("NEWNYM")
#
# for i in range(0, 10):
#     print "case "+str(i+1)
#     newId()
#     proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
#     urllib2.install_opener(opener)
#     print(urllib2.urlopen("http://www.ifconfig.me/ip").read())


from stem import Signal
from stem.control import Controller

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
opener = urllib2.build_opener(proxy_support)

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
urllib2.install_opener(opener)
print(urllib2.urlopen("http://www.ifconfig.me/ip").read())