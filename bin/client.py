#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Facebook Client executable
#   Covers the initiation of the Facebook Client
#
# Copyright (c) 2016    NorthernSec
# Copyright (c) 2016    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

import getpass
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from lib.ConfigReader import ConfigReader as Conf
from lib.FBackend     import FBackend

if __name__ == '__main__':
  conf=Conf(os.path.join(runPath, "../etc/client.ini"))
  # First try to read from the config
  fbid=conf.read("Client", "fbid",       "")
  pwd =conf.read("Client", "password",   "")
  ua  =conf.read("Client", "user agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0")
  # Ask the user if we're missing anything
  if not fbid: fbid=input("Facebook user ID: ")
  else:        print("Logging in with stored user: %s"%fbid)
  if not pwd:  pwd =getpass.getpass("Facebook password: ")
  # Set user agent to None to allow the client to choose a random one
  if not ua:   ua = None
  # Start client
  client = FBackend(fbid, pwd, user_agent=ua, debug=False)
  try:
    while True:
      pass
  except KeyboardInterrupt:
    client.gui.stop()
    print("Stopped the Facabook client")
