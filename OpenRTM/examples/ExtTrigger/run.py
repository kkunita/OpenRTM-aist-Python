#!/usr/bin/env python
# -*- Python -*-

#
# @file run.py
# @brief ExtTrigger example startup script
# @date $Date: 2007/10/26 $
#
# Copyright (c) 2003-2007 Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#          Task-intelligence Research Group,
#          Intelligent System Research Institute,
#          National Institute of Industrial Science (AIST), Japan
#          All rights reserved.
#

import sys,os,platform
import time
import commands

nsport="2809"
sysinfo = platform.uname()
hostname= sysinfo[1]
plat=sys.platform

if plat == "win32":
    os.system("start python ..\\..\\rtm-naming\\rtm-naming.py")
    os.system("start python ConsoleIn.py")
    os.system("start python Consoleout.py")
    time.sleep(1)
    os.system("python Connector.py")

else:
    status,term=commands.getstatusoutput("which kterm")
    if status != 0:
        status,term=commands.getstatusoutput("which xterm")

    if status != 0:
        status,term=commands.getstatusoutput("which uxterm")

    if status != 0:
        status,term=commands.getstatusoutput("which gnome-terminal")

    if status != 0:
        print "No terminal program (kterm/xterm/gnome-terminal) exists."
        exit

    os.system("python ../../rtm-naming/rtm-naming.py")
    os.system('%s -e python ConsoleIn.py &'%term)
    os.system('%s -e python ConsoleOut.py &'%term)
    time.sleep(1)
    os.system("python Connector.py")