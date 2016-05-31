#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Facebook back-end
#
# Copyright (c) 2016    NorthernSec
# Copyright (c) 2016    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

import os
import sys
import time
import _thread
from datetime import datetime

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from specter import SpecterShell

if sys.version_info < (3, 0):
  from urllib import quote
else:
  from urllib.parse import quote
    
try:
  import fbchat
except:
  sys.exit("Please make sure you have all dependencies installed")

class FBackend(fbchat.Client):
  def __init__(self, fbid, pwd, user_agent=None, debug=False):
    super(self.__class__, self).__init__(fbid, pwd, user_agent=user_agent, debug=debug)
    self.gui = SpecterShell(self)
    self.gui.listen()
    self.start_listening()
    self.currentUser = None
    self.unread = []

  def start_listening(self):
    try:
      _thread.start_new_thread(self.listen, ())
    except KeyboardInterrupt:
      pass

  def userinput(self, message):
    if not message.strip(): return
    if message.startswith("/"): # It's probably a command
      command = message.split()[0][1:].lower()
      args = " ".join(message.split()[1:])
      if   command in ["quit"]:
        self.gui.stop()
        self.listening = False
      elif command in ["friends"]:
        friends = self.getUsers(args)
        if friends:
          self.gui.writeln("[Info] Friends matching the name:")
          for friend in friends: self.gui.writeln(" |- %s"%friend.name)
        else:
          self.gui.writeln("[Info] No matches")
      elif command in ["chat", "query", "join"]:
        if not args: self.gui.writeln("[Error] Chat with who?")
        else:
          found = False
          friends = self.getUsers(args)
          for friend in friends:
            if friend.type == "user":
              self.currentUser = str(friend.uid)
              found = True
              break
          if not found:
            self.gui.writeln("[Error] Could not find the friend you meant")
          else:
            self.gui.writeln("[Info] Current user changed to %s"%friend.name)
            if str(friend.uid) in self.unread: self.unread.remove(str(friend.uid))
            history = reversed(self.getThreadInfo(friend.uid, 0, 10))
            if history: self.gui.writeln("[Info] Loading history:")
            for message in history:
              if hasattr(message, "body"):
                mess = message.body if message.body else "[Attachment or image]"
                msgTime = message.timestamp_datetime
                if message.author.strip("fbid:") == str(friend.uid):
                  self.gui.writeln("[%s] << %s"%(msgTime, mess))
                else:
                  self.gui.writeln("[%s] >> %s"%(msgTime, mess))
            if history: self.gui.writeln("[Info] End of history")
    else:
      if self.currentUser:
        self.send(self.currentUser, message)
        n = datetime.now()
        self.gui.writeln("[%s:%s] >> %s"%(n.hour, n.minute, message))
      else:
        self.gui.writeln("[Error] Not in a chat with any user")
    self.gui.refresh()

  def on_message(self, mid, fbid, name, message, meta):
    if self.currentUser == fbid:
      fbtime = int(meta['delta']['messageMetadata']['timestamp'])/1000
      msgTime = datetime.fromtimestamp(fbtime).strftime("%H:%M")
      self.gui.writeln("[%s] << %s"%(msgTime, message))
      self.gui.refresh()
    elif not fbid in self.unread and fbid != str(self.uid):
      print((fbid, str(self.uid)))
      self.unread.append(fbid)
      name = name if name else "<Unknown user>"
      self.gui.writeln("[Info] New Message from %s"%name)
      self.gui.refresh()
