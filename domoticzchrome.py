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
#import pychromecast.controllers.youtube as youtube

domoticz = "http://10.0.10.197:8080"


if '--show-debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)

cast = pychromecast.get_chromecast()

class mediaListener:
    domurl="http://10.0.10.197:8080"
    device=120
    def __init__(self, domoticzurl, deviceno):
        self.domurl = domoticzurl
        self.device=deviceno
        self.oldPlayerStatus = 'NONE'

    def requestJson(self, requesturl):
        print("requestJson")
        print(self.domurl+"/json.htm?type=command&param="+requesturl)
        data = urllib.urlopen(self.domurl+"/json.htm?type=command&param="+requesturl)
        return data

    def storeVariable(self,name, value):
        value = urllib.urlencode({'vvalue':value, 'vname':name, 'vtype':2})
        data = self.requestJson("updateuservariable&"+value)
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(data))
        if (obj['status'] == 'ERR'):
            data = self.requestJson("updateuservariable&"+value)

    def new_media_status(self, status):
        print("mediaListener")
        print(status)
        if (self.oldPlayerStatus != status.player_state):
            print("new state")
            self.oldPlayerStatus = status.player_state
            requesturl = "switchlight&idx="+str(self.device)+"&switchcmd="
            if status.player_state == "PLAYING" or status.player_state == "BUFFERING":
                requesturl += "On"
            else :
                requesturl += "Off"
            data = self.requestJson(requesturl)
            self.storeVariable('ChromeState', status.player_state)

listener = mediaListener(domoticz, 120)

cast.media_controller.register_status_listener(listener)

while (1):
    time.sleep(1)
    pass
