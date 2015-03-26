#!/usr/bin/env python3

import requests
import json
import sys
from gi.repository import Notify
from time import sleep

class Commentator(object):
    """docstring for Commentator"""
    def __init__(self):
        super(Commentator, self).__init__()
        self.url="http://www.espncricinfo.com/netstorage/656493.json?xhr=1"
        Notify.init("Commenter")
        self.lastcommid=0

    def sendmessage(self, title, message):
        comment = Notify.Notification.new(title, message, "dialog-information")
        comment.show()
        return

    def fetchcomment(self, url):
        try:
            print("fetching..")
            r=requests.get(url,timeout=5)
        except requests.exceptions.Timeout:
            print("Timed out")
            return ""
        if r.status_code is 200:
            return r.text
        else:
            return ""

    def parsejson(self, jsondata):
        if jsondata!="":
            data=json.loads(jsondata)
            return data

    def getlastball(self, data):
        comms=data["comms"]
        over=comms[0]["ball"]
        lastball=over[0]
        return lastball

    def getscore(self, data):
        inn=data["centre"]["common"]["innings"]
        return inn

    def notify(self, data):
        lastball=self.getlastball(data)
        inn=self.getscore(data)
        try:
            if lastball["comms_id"]!=self.lastcommid:
                self.sendmessage("%s %s/%s %s (%s)" % (lastball["event"],inn["runs"],inn["wickets"],lastball["players"],inn["overs"]),lastball["text"])
                self.lastcommid=lastball["comms_id"]
            else:
                print("not notifying")
                print("%s %s/%s %s (%s): %s"% (lastball["event"],inn["runs"],inn["wickets"],lastball["players"],inn["overs"],lastball["text"]))
        except KeyError:
            print("Keyerror")


    def run(self):
        while True:
            jsondata=self.fetchcomment(self.url)
            if jsondata!="":
                data=self.parsejson(jsondata)
                self.notify(data)
            sleep(15)

    def quit(self):
        print("Qutting")
        sys.exit()

try:
    indiaaus=Commentator()
    indiaaus.run()
except KeyboardInterrupt:
    indiaaus.quit()
except Exception as e:
    print(e)
    indiaaus=Commentator()
    indiaaus.run()
