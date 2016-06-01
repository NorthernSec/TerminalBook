============
TerminalBook
============

This project enables you to chat with people on Facebook from within the
 comfort of your terminal. The project is pure Python3, as are most of
  our projects, and relies on two dependencies:

  * **Specter**, a curses wrapper
  * **fbchat**, the library that we use for handling the connection

Installation
============

To install the dependencies, simply run `pip3 install -r requirements.txt`
 as root.

To run the main project, run `python3 ./bin/client.py`

How to Log in
=============

All you need to log in, is your facebook ID or e-mail and your password.
 You can find your Facebook ID by going to your own profile on Facebook,
  and copying everything after the slash (e.g. facebook.com/youruserid).

Options:
--------

You can use the `./etc/client.ini` file to store your credentials and
 "favorite browser". By default, the browser is "Firefox 45 on Ubuntu".
 We do not recommend to store your password, as this is in plain text,
 but adding your user ID and browser (if wanted) can speed up log-in.

These options are:

 * **fbid**       - for your Facebook ID or e-mail
 * **password**   - for your password (Again, not recommended)
 * **user agent** - for your preferred user agent string

Licencing
=========

This software is licensed under the "Original BSD License".
```
  (C) 2015  NorthernSec		https://github.com/NorthernSec
  (c) 2015  Pieter-Jan Moreels	https://github.com/pidgeyl
```
