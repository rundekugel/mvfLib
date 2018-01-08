#!/usr/bin/env python
#$Id: $

"""
sample 
how to read a track with omronmagstripe.py
"""

import omronmagstripe
import time
import sys

def main(comportname):
  o1 = omronmagstripe.COmronmag(comportname)
  if not o1.isOpen():
    print("unable to open serial port")
    return
  o1.waitForInsert()
  print("wait 2 seconds for a magstripe card to be inserted.")
  time.sleep(2)
  print("reading track2...")
  r = o1.readTrack(2)
  print("content:")
  print r
  print("response:")
  print o1.checkResponse()
  return
  
#start:
#windows:
comportname = "com11"
#linux:
comportname = "/dev/ttyACM0" 
#or
#comportname = "/dev/ttyUSB0"

if len(sys.argv) >1:
  comportname = sys.argv[1]
main(comportname)

# end of file
