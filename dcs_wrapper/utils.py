# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:09:51 2018

@author: alvarna
"""


def app_dir(appname):
    import sys
    from os import path, environ
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains as searchin
        from AppKit import NSApplicationSupportDirectory as dirin
        from AppKit import NSUserDomainMask as maskin
        appdata = path.join(searchin(dirin, maskin, True)[0], appname)
    elif sys.platform == 'win32':
        appdata = path.join(environ['APPDATA'], appname)
    else:
        appdata = path.expanduser(path.join("~", "." + appname))
    return appdata
