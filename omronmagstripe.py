#!/usr/bin/python
#$Id: $

"""
python lib for reading magstripe card with 
3S4YR-MVFW(DL)-0 Series Hybrid Card Reader/Writer
not finished, not tested
written by lifesim.de
donations: btc:14sb3XcNVWuQgqRx5RVE8sLazz82fAWx3j
"""

import serial

_version = "0.0.1"

def hex2(byte):
  r = hex(byte)
  r = r[2:]
  if byte <0x10:
    r = "0" +r
  return r
  
def dumpHex(data):
  r=""
  for d in data:
    r += hex2(d) +" "
  return r 

def bytes2str(bytes):
  r=""
  for b in bytes:
    r+= chr(b)
  return r
  
class COmronmag:
  _ser = 0
  logEnabled = 1
  timeout=2 #seconds
  
  def __init__(self,comportname):
    self.addLog("init..."),
    self._ser = serial.Serial(comportname, timeout=self.timeout)
    if self.isOpen():
      self._ser.setRTS(1)
      self._ser.setDTR(0)
      self.addLog("done.")
    else:
      self.addLog("can't open port.")
    
  def __del__(self):
    self.addLog("closeing...")
    self.close()
    self.addLog("bye.")
    
  def close(self):
   if self._ser != 0:
     self._ser.close()
   
  def openCom(self, comportname='old'):
   if comportname != 'old':
    self._ser.port=comportname
   self._ser.open()
   
  def _read(self, maxbytes = 99, verbose=0):
    r = self._ser.read(maxbytes)
    if verbose >0:
      print("RX:" +r)
    return r

  def clearRXBuf(self, verbose=0):
    self._ser.timeout=0.1
    r =self._read(verbose- 1)
    self._ser.timeout=self.timeout
    return r
    
  def isOpen(self):
    return self._ser.isOpen()
   
  def addLog(self, text):
    if self.logEnabled:
      print(text)
   
  def _write(self, data, verbose =0):
    if verbose:
      print("TX:"+ dumpHex(data))
    return self._ser.write(bytes2str(data))
  
  def _packFrame(self, data):
    pre=[0x10, 0x02]
    suf =[0x10, 0x03]
    data = [0x43] + data
    c=suf[1]
    for d in data:
      c ^= d
    checksum = c
    f= pre + data + suf + [checksum]
    return f
    
  def sendCmd(self, cmds, verbose = 0):
    d=self._packFrame(cmds)
    r=self._write(d, verbose)
    return r
    
  def eject(self, verbose=0):
    cmd_eject = [0x33, 0x30]
    self.sendCmd(cmd_eject, verbose)
    r = self._read(2, verbose)
    r= self._write([0x10,5], verbose)    
    return r
    
  def EjectReset(self, verbose=0):
    cmd_ejectReset = [0x30, 0x31]
    return self.sendCmd(cmd_ejectReset, verbose)

  def waitForInsert(self, verbose=0):
    self.sendCmd([0x3a, 0x30], verbose)
    r = self._read(2, verbose)
    r= self._write([0x10,5], verbose)
    return
    
  def readTrack(self, tracknum, verbose=0):
    cmd_readTrack = [0x36]
    if tracknum <1 or tracknum > 3 :
      self.addLog("wrong Tracknumber!")
      return ""
    self.clearRXBuf(verbose)
    r = self.sendCmd(cmd_readTrack+ [0x30 +tracknum], verbose)
    r = self._read(2, verbose)
    r= self._write([0x10,5], verbose)
    r= self._read(99, verbose)
    return r[7:-3]

  def writeTrack(self, tracknum, data, verbose=0):
    cmd_writeTrack = [0x37]
    if tracknum <1 or tracknum > 3 :
      self.addLog("wrong Tracknumber!")
      return ""
    self.clearRXBuf(verbose)
    r = self.sendCmd(cmd_writeTrack+ [0x30 +tracknum]+ data, verbose)
    r= self._read(99, verbose)
    return r

    
  def resetHW(self, verbose=0):
    cmd_reset = [0,0]
    r = self.sendCmd(cmd_reset, verbose)
    r= self._read(99, verbose)
    return r

  def checkResponse(self, rxdata=[], verbose=0):
    r=rxdata
    if r == []:
      r = self._read(99, verbose)
    
    if r==bytes2str([0x10,0x02,0x4e]) :
      return "C/R: Neg. response"
    if r==bytes2str([0x10,0x20,0x50]) :
      return "C/R: Pos. response"
    if r==bytes2str([0x10,0x06]) :
      return "Ack"
    if r==bytes2str([0x10,0x15]) :
      return "Nak"
    if r==bytes2str([0x10,0x05]) :
      return "DLE_ENQ"
    return ""
    
    
# end of file

