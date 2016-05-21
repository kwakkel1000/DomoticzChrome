from __future__ import print_function
import time
import sys
import logging
import json
import codecs
import urllib
#from urllib.request import urlopen
#from urllib.parse import urlencode

import pychromecast
import pychromecast.controllers.youtube as youtube

domoticz = "http://10.0.10.184:8080"


if '--show-debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)

cast = pychromecast.get_chromecast()

class mediaListener:
    domurl="http://10.0.10.184:8080"
    device=106
    def __init__(self, domoticzurl, deviceno):
        self.domurl = domoticzurl
        self.device=deviceno
        self.oldPlayerStatus = 'NONE'

    def new_media_status(self, status):
        print("mediaListener")
        print(status)
        if (self.oldPlayerStatus != status.player_state):
            self.oldPlayerStatus = status.player_state
            if status.player_state == "PLAYING" or status.player_state == "BUFFERING":
                
                data = urllib.urlopen(self.domurl+"/json.htm?type=command&param=switchlight&idx="+self.device+"&switchcmd=on")
            else :
                data = urllib.urlopen(self.domurl+"/json.htm?type=command&param=switchlight&idx="+self.device+"&switchcmd=off")
            print(data)
            self.storeVariable('ChromeState', new_state)

    def storeVariable(self,name, value):
        value = urllib.urlencode({'vvalue':value, 'vname':name, 'vtype':2})
        d = urllib.urlopen(self.domurl+'/json.htm?type=command&param=updateuservariable&'+value)
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(d))
        if (obj['status'] == 'ERR'):
            d = urllib.urlopen(self.domurl+'/json.htm?type=command&param=saveuservariable&'+value)

listener = mediaListener(domoticz, 106)

cast.media_controller.register_status_listener(listener)

while (1):
    time.sleep(1)
    pass
