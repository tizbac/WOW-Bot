# -*- coding: utf-8 -*-
import os
import string
import math
import zlib
import sys
import time
from colors import *
from struct import *
from OpCodes import *
from MovementFlags import *
PLAYER = 0
GAMEOBJECT = 1
NPC = 2
UPDATETYPE_VALUES               = 0
UPDATETYPE_MOVEMENT             = 1
UPDATETYPE_CREATE_OBJECT        = 2
UPDATETYPE_CREATE_OBJECT2       = 3
UPDATETYPE_OUT_OF_RANGE_OBJECTS = 4
UPDATETYPE_NEAR_OBJECTS         = 5
UPDATEFLAG_NONE         = 0x00
UPDATEFLAG_SELF         = 0x01
UPDATEFLAG_TRANSPORT    = 0x02
UPDATEFLAG_FULLGUID     = 0x04
UPDATEFLAG_LOWGUID      = 0x08
UPDATEFLAG_HIGHGUID     = 0x10
UPDATEFLAG_LIVING       = 0x20
UPDATEFLAG_HASPOSITION  = 0x40
MOVEMENTFLAG_NONE           = 0x00000000
TYPEID_OBJECT        = 0
TYPEID_ITEM          = 1
TYPEID_CONTAINER     = 2
TYPEID_UNIT          = 3
TYPEID_PLAYER        = 4
TYPEID_GAMEOBJECT    = 5
TYPEID_DYNAMICOBJECT = 6
TYPEID_CORPSE        = 7
TYPEID_AIGROUP       = 8
TYPEID_AREATRIGGER   = 9
sizes = {0: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 8: 2, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 19, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 6, 46: 1, 47: 1, 48: 56, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 72, 104: 14, 118: 14, 132: 14, 146: 1, 147: 2, 149: 1, 150: 1, 151: 1, 152: 1, 153: 1, 154: 1, 155: 1, 156: 1, 157: 1, 158: 1, 159: 1, 160: 1, 161: 1, 162: 1, 163: 1, 164: 1, 165: 1, 166: 1, 167: 1, 168: 1, 169: 1, 170: 1, 171: 1, 172: 1, 173: 1, 174: 1, 175: 1, 176: 1, 177: 1, 178: 1, 179: 1, 180: 1, 181: 1, 182: 1, 183: 1, 184: 1, 185: 1, 186: 7, 193: 7, 200: 7, 207: 1, 208: 1, 209: 1, 210: 1, 211: 1, 212: 1, 213: 1, 214: 1, 215: 1, 216: 1, 217: 1, 218: 7, 225: 7, 232: 1, 233: 1, 234: 2, 236: 1, 237: 1, 238: 1, 239: 1, 240: 1, 241: 1, 242: 1, 243: 1, 244: 1, 245: 1, 246: 1, 247: 1, 248: 1, 249: 1, 250: 1, 251: 1, 252: 1, 253: 1, 254: 1, 255: 1, 256: 1, 257: 1, 258: 1, 259: 1, 260: 1, 261: 1, 262: 1, 263: 1, 264: 1, 265: 1, 266: 1, 267: 1, 268: 1, 269: 1, 270: 1, 271: 1, 272: 1, 273: 1, 274: 1, 275: 1, 276: 1, 277: 1, 278: 1, 279: 1, 280: 1, 281: 1, 282: 1, 283: 1, 284: 1, 285: 1, 286: 1, 287: 1, 288: 1, 289: 1, 290: 1, 291: 1, 292: 1, 293: 1, 294: 1, 295: 1, 296: 1, 297: 1, 298: 1, 299: 1, 300: 1, 301: 1, 302: 1, 303: 1, 304: 1, 305: 1, 306: 1, 307: 1, 308: 1, 309: 1, 310: 1, 311: 1, 312: 1, 313: 1, 314: 1, 315: 1, 316: 1, 317: 1, 318: 1, 319: 1, 320: 1, 321: 1, 322: 1, 323: 1, 324: 1, 325: 1, 326: 1, 327: 1, 328: 1, 329: 1, 330: 1, 331: 1, 332: 1, 333: 1, 334: 1, 335: 1, 336: 1, 337: 1, 338: 1, 339: 1, 340: 1, 341: 1, 342: 1, 343: 1, 344: 2, 346: 12, 358: 1, 359: 1, 360: 2, 362: 12, 374: 1, 375: 1, 376: 2, 378: 12, 390: 1, 391: 1, 392: 2, 394: 12, 406: 1, 407: 1, 408: 2, 410: 12, 422: 1, 423: 1, 424: 2, 426: 12, 438: 1, 439: 1, 440: 2, 442: 12, 454: 1, 455: 1, 456: 2, 458: 12, 470: 1, 471: 1, 472: 2, 474: 12, 486: 1, 487: 1, 488: 2, 490: 12, 502: 1, 503: 1, 504: 2, 506: 12, 518: 1, 519: 1, 520: 2, 522: 12, 534: 1, 535: 1, 536: 2, 538: 12, 550: 1, 551: 1, 552: 2, 554: 12, 566: 1, 567: 1, 568: 2, 570: 12, 582: 1, 583: 1, 584: 2, 586: 12, 598: 1, 599: 1, 600: 2, 602: 12, 614: 1, 615: 1, 616: 2, 618: 12, 630: 1, 631: 1, 632: 2, 634: 12, 646: 1, 647: 1, 648: 1, 649: 1, 650: 46, 696: 32, 728: 56, 784: 14, 798: 24, 822: 64, 886: 36, 922: 2, 924: 2, 926: 1, 927: 1, 928: 384, 1312: 1, 1313: 1, 1314: 1, 1315: 1, 1316: 1, 1317: 1, 1318: 1, 1319: 1, 1320: 1, 1321: 1, 1322: 1, 1323: 1, 1324: 7, 1331: 1, 1332: 128, 1460: 1, 1461: 1, 1462: 7, 1469: 7, 1476: 7, 1483: 1, 1484: 1, 1485: 1, 1486: 1, 1487: 1, 1488: 1, 1489: 1, 1490: 12, 1502: 12, 1514: 1, 1515: 1, 1516: 1, 1517: 1, 1518: 1, 1519: 1, 1520: 24, 1544: 18, 1562: 1, 1563: 1, 1564: 1, 1565: 1, 1566: 1, 1567: 25}

def unpackguid(data):
  guid = 0
  guidmark = ord(data[0])
  j = 1
  for i in range(0,8):
    if guidmark & (1 << i):
      bit = ord(data[j])
      j += 1
      guid |= bit << i*8;
  return (guid,data[j:])
def unpackbignumber(data):
  n = 0
  i = 0
  for c in data:
    n += pow(16,i)*(ord(c)&0xF)
    i+=1
    n += pow(16,i)*((ord(c)>>4)&0xF)
    i+=1
  return n
def packbignumber(n,l=32):
  s = ""
  i = 0
  while i < l:
    x = n >> 8*i
    s = s + chr(x&255)
    i+=1
  return s
def tobin(bn,blocks=-1):
  s = ""
  bits = int(math.log(bn,2)) if blocks == -1 else blocks*32
  for i in range(0,bits+1):
    s += str((bn >> (bits-i)) & 1)
  return s
def parseoutofrangeobjblock(s_):
  #print "Out of range objects"
  guids = []
  
  s = str(s_)
  guidcount = unpack("I",s[:4])[0]
  s = s[4:]
  for i in range(0,guidcount):
    s = s[1:]
    guids.append(unpack("Q",s[:8])[0])
    s = s[8:]
  return guids,s

def parsemovementupdate(s_):
  guid = 0
  data = dict()
  s = str(s_)
  guid = unpack("Q",s[:8])[0]
  s = s[8:]
  flags = ord(s[0])
  s = s[1:]
  #print tobin(flags,1)
  if (flags & UPDATEFLAG_LIVING ):
    data["flags2"] = unpack("I",s[:4])[0]
    s = s[4:]
    s = s[1:]
    data["time"] = unpack("I",s[:4])[0]
    s = s[4:]
  if flags & UPDATEFLAG_HASPOSITION:
    x,y,z,o = unpack("ffff",s[:16])
    s = s[16:]
    data["pos"] = x,y,z,o
  if "flags2" in data:
    if data["flags2"] & MOVEMENTFLAG_ONTRANSPORT:
      s = s[28:] # Sticazzi dei transport x ora
    if data["flags2"] & (MOVEMENTFLAG_SWIMMING | MOVEMENTFLAG_FLYING2):
      data["pitch"] = unpack("f",s[:4])[0]
      s = s[4:]
    data["falltime"] = unpack("I",s[:4])[0]
    s = s[4:]
    if data["flags2"] & MOVEMENTFLAG_JUMPING:
      s = s[16:]
    if data["flags2"] & MOVEMENTFLAG_SPLINE:
      s = s[4:]
    speeds = unpack("ffffffff",s[:4*8])
    s = s[4*8:]
    data["speeds"] = speeds
  if flags & UPDATEFLAG_LOWGUID:
    #print "Lowguid"
    s = s[4:]
  if flags & UPDATEFLAG_HIGHGUID:
    #print "Highguid"
    s = s[4:]
  if flags & UPDATEFLAG_FULLGUID:
    #print "Fullguid"
    s = s[1:]
  if flags & UPDATEFLAG_TRANSPORT:
    #print "Transport"
    s = s[4:]
  #print "Movement: guid "+str(guid),data
  return guid,data,s
def parsevaluesupdate(s_):
  #print "Values update"
  values = dict()
  guid = 0
  s = str(s_)
  #print "%x" % ord(s[0])
  s = s[1:]
  
  guid = unpack("Q",s[:8])[0]
  s = s[8:]
  umblockcount = ord(s[0])
  s = s[1:]
  mask = unpackbignumber(s[:umblockcount<<2])
  
  #print umblockcount<<2,tobin(mask,umblockcount)
  s = s[umblockcount<<2:]
  j = 0
  for i in range(0,2000):
    if (mask >> i) & 1:
      values[i] = unpack("I",s[:4])[0]
      s = s[4:]

  return guid,values,s
def parsecreateobject(s_):
  #print "Create: %x"%ord(s_[0])
  s = str(s_)
  s = s[1:]
  guid = unpack("Q",s[:8])[0]
  #print guid
  s = s[8:]
  typeid = ord(s[0])
  #print "%x"%typeid
  s = s[1:]
  guid,data,s = parsemovementupdate(s_[1:9]+s)
  guid,values,s = parsevaluesupdate(s_[:9]+s)
  #print guid
  return guid,typeid,data,values,s
objectnames = {TYPEID_AIGROUP : "<AI Group>" , TYPEID_AREATRIGGER : "<Area Trigger>" , TYPEID_CONTAINER : "<Container>", TYPEID_CORPSE : "<Corpse>", TYPEID_DYNAMICOBJECT : "<Dynamic Object>", TYPEID_GAMEOBJECT : "<GameObject>", TYPEID_ITEM : "<Item>" , TYPEID_OBJECT : "<Object>", TYPEID_PLAYER : "<Player>", TYPEID_UNIT : "<Unit>"}
def tofloat(iv):
  data = pack("I",iv)
  return unpack("f",data)[0]
def toint64(v1,v2):
  data = pack("II",v1,v2)
  return unpack("Q",data)[0]
class WorldObject:
  def __init__(self,guid,t,x,y,z,o,name=""):
    debug("Creazione di un %s con guid %i"%(objectnames[t],guid))
    self.t = t
    self.guid = guid
    self.x = float(x)
    self.y = float(y)
    self.z = float(z)
    self.o = float(o)
    self.name = ""
    self.values = dict()
  def mergevalues(self,v):
    for x in v:
      self.values[x] = v[x]
  def getplayerrangedcritpercentage(self):
    if 1322 in self.values:
      return tofloat(self.values[1322])
    else:
      return None
  def getunitcreatedbyspell(self):
    if 167 in self.values:
      return self.values[167]
    else:
      return None
  def getunitfieldpetnumber(self):
    if 160 in self.values:
      return self.values[160]
    else:
      return None
  def getunitfieldattackpowermods(self):
    a = []
    for x in range(211,212):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem6creator(self):
    if 424 in self.values and 425 in self.values:
      return toint64(self.values[424],self.values[425])
    else:
      return None
  def getplayervisibleitem2properties(self):
    a = []
    for x in range(374,375):
      if x in self.values:
	a.append(x)
    return a
  def getunitmodcastspeed(self):
    if 166 in self.values:
      return tofloat(self.values[166])
    else:
      return None
  def getplayernextlevelxp(self):
    if 927 in self.values:
      return self.values[927]
    else:
      return None
  def getplayervisibleitem10pad(self):
    if 503 in self.values:
      return self.values[503]
    else:
      return None
  def getplayercharacterpoints1(self):
    if 1312 in self.values:
      return self.values[1312]
    else:
      return None
  def getplayercharacterpoints2(self):
    if 1313 in self.values:
      return self.values[1313]
    else:
      return None
  def getplayerfieldkills(self):
    a = []
    for x in range(1514,1515):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldaura(self):
    a = []
    for x in range(48,104):
      if x in self.values:
	a.append(x)
    return a
  def getcorpsefieldfacing(self):
    if 10 in self.values:
      return tofloat(self.values[10])
    else:
      return None
  def getitemfielditemtextid(self):
    if 57 in self.values:
      return self.values[57]
    else:
      return None
  def getplayervisibleitem160(self):
    a = []
    for x in range(586,598):
      if x in self.values:
	a.append(x)
    return a
  def getunitdynamicflags(self):
    if 164 in self.values:
      return self.values[164]
    else:
      return None
  def getunitfieldpersuaded(self):
    if 18 in self.values:
      return tofloat(self.values[18])
    else:
      return None
  def getunitchannelspell(self):
    if 165 in self.values:
      return self.values[165]
    else:
      return None
  def getplayervisibleitem120(self):
    a = []
    for x in range(522,534):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectpadding(self):
    if 25 in self.values:
      return self.values[25]
    else:
      return None
  def getplayervisibleitem14properties(self):
    a = []
    for x in range(566,567):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldrangedattackpowermods(self):
    a = []
    for x in range(214,215):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem140(self):
    a = []
    for x in range(554,566):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldduration(self):
    a = []
    for x in range(15,34):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem5creator(self):
    if 408 in self.values and 409 in self.values:
      return toint64(self.values[408],self.values[409])
    else:
      return None
  def getplayerquestlog241(self):
    if 336 in self.values:
      return self.values[336]
    else:
      return None
  def getplayerquestlog242(self):
    if 337 in self.values:
      return self.values[337]
    else:
      return None
  def getunitfieldcharmedby(self):
    if 10 in self.values:
      return tofloat(self.values[10])
    else:
      return None
  def getplayerduelarbiter(self):
    if 234 in self.values and 235 in self.values:
      return toint64(self.values[234],self.values[235])
    else:
      return None
  def getplayerquestlog224(self):
    if 331 in self.values:
      return self.values[331]
    else:
      return None
  def getplayerquestlog222(self):
    if 329 in self.values:
      return self.values[329]
    else:
      return None
  def getplayerquestlog223(self):
    a = []
    for x in range(330,331):
      if x in self.values:
	a.append(x)
    return a
  def getunitfielddisplayid(self):
    if 152 in self.values:
      return self.values[152]
    else:
      return None
  def getcorpsefielditem(self):
    a = []
    for x in range(15,34):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem18properties(self):
    a = []
    for x in range(630,631):
      if x in self.values:
	a.append(x)
    return a
  def getunittrainingpoints(self):
    a = []
    for x in range(170,171):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldbytes(self):
    a = []
    for x in range(1486,1487):
      if x in self.values:
	a.append(x)
    return a
  def getdynamicobjectcaster(self):
    if 6 in self.values and 7 in self.values:
      return toint64(self.values[6],self.values[7])
    else:
      return None
  def getdynamicobjectradius(self):
    if 10 in self.values:
      return tofloat(self.values[10])
    else:
      return None
  def getobjectfieldscalex(self):
    if 4 in self.values:
      return tofloat(self.values[4])
    else:
      return None
  def getunitfieldnativedisplayid(self):
    if 153 in self.values:
      return self.values[153]
    else:
      return None
  def getplayervisibleitem100(self):
    a = []
    for x in range(490,502):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog201(self):
    if 320 in self.values:
      return self.values[320]
    else:
      return None
  def getplayerquestlog202(self):
    if 321 in self.values:
      return self.values[321]
    else:
      return None
  def getplayerquestlog203(self):
    a = []
    for x in range(322,323):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog204(self):
    if 323 in self.values:
      return self.values[323]
    else:
      return None
  def getunitfieldpetnextlevelexp(self):
    if 163 in self.values:
      return self.values[163]
    else:
      return None
  def getplayerfieldwatchedfactionindex(self):
    if 1519 in self.values:
      return self.values[1519]
    else:
      return None
  def getitemfieldowner(self):
    if 6 in self.values and 7 in self.values:
      return toint64(self.values[6],self.values[7])
    else:
      return None
  def getcorpsefielddynamicflags(self):
    if 38 in self.values:
      return self.values[38]
    else:
      return None
  def getgameobjectdisplayid(self):
    if 8 in self.values and 9 in self.values:
      return toint64(self.values[8],self.values[9])
    else:
      return None
  def getplayerquestlog93(self):
    a = []
    for x in range(278,279):
      if x in self.values:
	a.append(x)
    return a
  def getplayerreststateexperience(self):
    if 1460 in self.values:
      return self.values[1460]
    else:
      return None
  def getdynamicobjectposz(self):
    if 13 in self.values:
      return tofloat(self.values[13])
    else:
      return None
  def getdynamicobjectposy(self):
    if 12 in self.values:
      return tofloat(self.values[12])
    else:
      return None
  def getdynamicobjectposx(self):
    if 11 in self.values:
      return tofloat(self.values[11])
    else:
      return None
  def getplayervisibleitem1creator(self):
    if 344 in self.values and 345 in self.values:
      return toint64(self.values[344],self.values[345])
    else:
      return None
  def getdynamicobjectfacing(self):
    if 14 in self.values:
      return self.values[14]
    else:
      return None
  def getplayervisibleitem4creator(self):
    if 392 in self.values and 393 in self.values:
      return toint64(self.values[392],self.values[393])
    else:
      return None
  def getplayerfieldvanitypetslot1(self):
    a = []
    for x in range(886,922):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectanimprogress(self):
    if 24 in self.values:
      return self.values[24]
    else:
      return None
  def getplayerfieldmoddamagedoneneg(self):
    a = []
    for x in range(1469,1476):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldcharm(self):
    if 6 in self.values and 7 in self.values:
      return toint64(self.values[6],self.values[7])
    else:
      return None
  def getgameobjectposy(self):
    if 16 in self.values:
      return tofloat(self.values[16])
    else:
      return None
  def getgameobjectposx(self):
    a = []
    for x in range(15,34):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectposz(self):
    if 17 in self.values:
      return tofloat(self.values[17])
    else:
      return None
  def getplayerfieldhonorcurrency(self):
    if 1562 in self.values:
      return self.values[1562]
    else:
      return None
  def getgameobjectdynflags(self):
    if 19 in self.values:
      return self.values[19]
    else:
      return None
  def getplayervisibleitem17properties(self):
    a = []
    for x in range(614,615):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldmoddamagedonepct(self):
    a = []
    for x in range(1476,1483):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldbuybacktimestamp1(self):
    a = []
    for x in range(1502,1514):
      if x in self.values:
	a.append(x)
    return a
  def getunitvirtualitemslotdisplay(self):
    if 37 in self.values:
      return self.values[37]
    else:
      return None
  def getplayerguildtimestamp(self):
    if 243 in self.values:
      return self.values[243]
    else:
      return None
  def getplayervisibleitem12creator(self):
    if 520 in self.values and 521 in self.values:
      return toint64(self.values[520],self.values[521])
    else:
      return None
  def getunitfieldhealth(self):
    if 22 in self.values:
      return self.values[22]
    else:
      return None
  def getunitfieldresistances(self):
    a = []
    for x in range(186,193):
      if x in self.values:
	a.append(x)
    return a
  def getplayerxp(self):
    if 926 in self.values:
      return self.values[926]
    else:
      return None
  def getcontainerfieldnumslots(self):
    if 60 in self.values:
      return self.values[60]
    else:
      return None
  def getplayervisibleitem4properties(self):
    a = []
    for x in range(406,407):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldpackslot1(self):
    a = []
    for x in range(696,728):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog234(self):
    if 335 in self.values:
      return self.values[335]
    else:
      return None
  def getplayerquestlog233(self):
    a = []
    for x in range(334,335):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog232(self):
    if 333 in self.values:
      return self.values[333]
    else:
      return None
  def getplayerquestlog231(self):
    if 332 in self.values:
      return self.values[332]
    else:
      return None
  def getplayerquestlog211(self):
    if 324 in self.values:
      return self.values[324]
    else:
      return None
  def getplayerquestlog213(self):
    a = []
    for x in range(326,327):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog212(self):
    if 325 in self.values:
      return self.values[325]
    else:
      return None
  def getplayerquestlog214(self):
    if 327 in self.values:
      return self.values[327]
    else:
      return None
  def getplayerfieldbankbagslot1(self):
    a = []
    for x in range(784,798):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectartkit(self):
    if 23 in self.values:
      return self.values[23]
    else:
      return None
  def getunitfieldpetnametimestamp(self):
    if 161 in self.values:
      return self.values[161]
    else:
      return None
  def getplayercritpercentage(self):
    if 1321 in self.values:
      return tofloat(self.values[1321])
    else:
      return None
  def getplayervisibleitem7creator(self):
    if 440 in self.values and 441 in self.values:
      return toint64(self.values[440],self.values[441])
    else:
      return None
  def getplayerquestlog254(self):
    if 343 in self.values:
      return self.values[343]
    else:
      return None
  def getplayerquestlog251(self):
    if 340 in self.values:
      return self.values[340]
    else:
      return None
  def getplayerquestlog253(self):
    a = []
    for x in range(342,343):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog252(self):
    if 341 in self.values:
      return self.values[341]
    else:
      return None
  def getplayervisibleitem11creator(self):
    if 504 in self.values and 505 in self.values:
      return toint64(self.values[504],self.values[505])
    else:
      return None
  def getunitfieldcreatedby(self):
    if 14 in self.values:
      return self.values[14]
    else:
      return None
  def getcontaineralignpad(self):
    a = []
    for x in range(61,62):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectflags(self):
    if 9 in self.values:
      return self.values[9]
    else:
      return None
  def getplayervisibleitem18creator(self):
    if 616 in self.values and 617 in self.values:
      return toint64(self.values[616],self.values[617])
    else:
      return None
  def getunitfieldmaxhealthmodifier(self):
    if 232 in self.values:
      return tofloat(self.values[232])
    else:
      return None
  def getunitfieldpadding(self):
    if 233 in self.values:
      return self.values[233]
    else:
      return None
  def getplayervisibleitem1properties(self):
    a = []
    for x in range(358,359):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectfaction(self):
    if 20 in self.values:
      return self.values[20]
    else:
      return None
  def getunitfieldminoffhanddamage(self):
    if 157 in self.values:
      return tofloat(self.values[157])
    else:
      return None
  def getplayerselfresspell(self):
    if 1488 in self.values:
      return self.values[1488]
    else:
      return None
  def getunitfieldchannelobject(self):
    if 20 in self.values:
      return self.values[20]
    else:
      return None
  def getplayervisibleitem17pad(self):
    if 615 in self.values:
      return self.values[615]
    else:
      return None
  def getunitfieldrangedattackpowermultiplier(self):
    if 215 in self.values:
      return tofloat(self.values[215])
    else:
      return None
  def getunitnpcemotestate(self):
    if 169 in self.values:
      return self.values[169]
    else:
      return None
  def getitemfieldcreator(self):
    if 10 in self.values:
      return tofloat(self.values[10])
    else:
      return None
  def getplayeroffhandcritpercentage(self):
    if 1323 in self.values:
      return tofloat(self.values[1323])
    else:
      return None
  def getunitfieldposstat4(self):
    if 180 in self.values:
      return self.values[180]
    else:
      return None
  def getplayerspellcritpercentage1(self):
    a = []
    for x in range(1324,1331):
      if x in self.values:
	a.append(x)
    return a
  def getunitvirtualiteminfo(self):
    a = []
    for x in range(40,46):
      if x in self.values:
	a.append(x)
    return a
  def getplayerexpertise(self):
    if 1319 in self.values:
      return self.values[1319]
    else:
      return None
  def getplayervisibleitem13pad(self):
    if 551 in self.values:
      return self.values[551]
    else:
      return None
  def getunitfieldmountdisplayid(self):
    if 154 in self.values:
      return self.values[154]
    else:
      return None
  def getunitfieldsummonedby(self):
    if 12 in self.values:
      return tofloat(self.values[12])
    else:
      return None
  def getunitfieldposstat2(self):
    if 178 in self.values:
      return self.values[178]
    else:
      return None
  def getplayervisibleitem14creator(self):
    if 552 in self.values and 553 in self.values:
      return toint64(self.values[552],self.values[553])
    else:
      return None
  def getgameobjectlevel(self):
    if 22 in self.values:
      return self.values[22]
    else:
      return None
  def getplayervisibleitem6pad(self):
    if 439 in self.values:
      return self.values[439]
    else:
      return None
  def getunitfieldcombatreach(self):
    if 151 in self.values:
      return tofloat(self.values[151])
    else:
      return None
  def getplayerfieldtodaycontribution(self):
    if 1515 in self.values:
      return self.values[1515]
    else:
      return None
  def getunitfieldattackpowermultiplier(self):
    if 212 in self.values:
      return tofloat(self.values[212])
    else:
      return None
  def getcorpsefieldflags(self):
    if 37 in self.values:
      return self.values[37]
    else:
      return None
  def getplayertrackcreatures(self):
    if 1314 in self.values:
      return self.values[1314]
    else:
      return None
  def getunitfieldrangedattackpower(self):
    if 213 in self.values:
      return self.values[213]
    else:
      return None
  def getplayervisibleitem9properties(self):
    a = []
    for x in range(486,487):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldmaxoffhanddamage(self):
    if 158 in self.values:
      return tofloat(self.values[158])
    else:
      return None
  def getunitfieldpower2(self):
    if 24 in self.values:
      return self.values[24]
    else:
      return None
  def getunitfieldmaxhealth(self):
    if 28 in self.values:
      return self.values[28]
    else:
      return None
  def getunitfieldbasehealth(self):
    if 208 in self.values:
      return self.values[208]
    else:
      return None
  def getunitfieldflags2(self):
    if 47 in self.values:
      return self.values[47]
    else:
      return None
  def getplayershieldblock(self):
    if 1331 in self.values:
      return self.values[1331]
    else:
      return None
  def getcorpsefieldguild(self):
    if 36 in self.values:
      return self.values[36]
    else:
      return None
  def getplayerdodgepercentage(self):
    if 1317 in self.values:
      return tofloat(self.values[1317])
    else:
      return None
  def getunitfieldresistancebuffmodsnegative(self):
    a = []
    for x in range(200,207):
      if x in self.values:
	a.append(x)
    return a
  def getobjectfieldpadding(self):
    if 5 in self.values:
      return self.values[5]
    else:
      return None
  def getunitfieldpower4(self):
    if 26 in self.values:
      return self.values[26]
    else:
      return None
  def getunitfieldpower5(self):
    if 27 in self.values:
      return self.values[27]
    else:
      return None
  def getunitfieldbytes0(self):
    if 36 in self.values:
      return self.values[36]
    else:
      return None
  def getunitfieldbytes1(self):
    a = []
    for x in range(159,160):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldbytes2(self):
    a = []
    for x in range(209,210):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldpower1(self):
    if 23 in self.values:
      return self.values[23]
    else:
      return None
  def getunitfieldpowercostmultiplier(self):
    a = []
    for x in range(225,232):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldcontained(self):
    if 8 in self.values and 9 in self.values:
      return toint64(self.values[8],self.values[9])
    else:
      return None
  def getunitfieldmaxpower5(self):
    if 33 in self.values:
      return self.values[33]
    else:
      return None
  def getunitfieldmaxpower4(self):
    if 32 in self.values:
      return self.values[32]
    else:
      return None
  def getunitfieldmaxpower1(self):
    if 29 in self.values:
      return self.values[29]
    else:
      return None
  def getunitfieldmaxpower3(self):
    if 31 in self.values:
      return self.values[31]
    else:
      return None
  def getunitfieldmaxpower2(self):
    if 30 in self.values:
      return self.values[30]
    else:
      return None
  def getplayerfieldarenacurrency(self):
    if 1563 in self.values:
      return self.values[1563]
    else:
      return None
  def getplayerfieldmaxlevel(self):
    if 1566 in self.values:
      return self.values[1566]
    else:
      return None
  def getplayervisibleitem5pad(self):
    if 423 in self.values:
      return self.values[423]
    else:
      return None
  def getplayervisibleitem7properties(self):
    a = []
    for x in range(454,455):
      if x in self.values:
	a.append(x)
    return a
  def getcontainerfieldslot1(self):
    a = []
    for x in range(62,134):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldnegstat1(self):
    if 182 in self.values:
      return self.values[182]
    else:
      return None
  def getunitfieldnegstat0(self):
    if 181 in self.values:
      return self.values[181]
    else:
      return None
  def getunitfieldnegstat3(self):
    if 184 in self.values:
      return self.values[184]
    else:
      return None
  def getunitfieldnegstat2(self):
    if 183 in self.values:
      return self.values[183]
    else:
      return None
  def getunitfieldnegstat4(self):
    if 185 in self.values:
      return self.values[185]
    else:
      return None
  def getplayerquestlog11(self):
    if 244 in self.values:
      return self.values[244]
    else:
      return None
  def getplayerfieldpvpmedals(self):
    if 1489 in self.values:
      return self.values[1489]
    else:
      return None
  def getplayervisibleitem3creator(self):
    if 376 in self.values and 377 in self.values:
      return toint64(self.values[376],self.values[377])
    else:
      return None
  def getunitfieldbasemana(self):
    if 207 in self.values:
      return self.values[207]
    else:
      return None
  def getplayerfieldbankslot1(self):
    a = []
    for x in range(728,784):
      if x in self.values:
	a.append(x)
    return a
  def getdynamicobjectbytes(self):
    if 8 in self.values and 9 in self.values:
      return toint64(self.values[8],self.values[9])
    else:
      return None
  def getplayerquestlog94(self):
    if 279 in self.values:
      return self.values[279]
    else:
      return None
  def getplayerquestlog92(self):
    if 277 in self.values:
      return self.values[277]
    else:
      return None
  def getplayervisibleitem9pad(self):
    if 487 in self.values:
      return self.values[487]
    else:
      return None
  def getplayerexploredzones1(self):
    a = []
    for x in range(1332,1460):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog91(self):
    if 276 in self.values:
      return self.values[276]
    else:
      return None
  def getplayerquestlog52(self):
    if 261 in self.values:
      return self.values[261]
    else:
      return None
  def getplayerquestlog53(self):
    a = []
    for x in range(262,263):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog51(self):
    if 260 in self.values:
      return self.values[260]
    else:
      return None
  def getplayerquestlog54(self):
    if 263 in self.values:
      return self.values[263]
    else:
      return None
  def getgameobjectfacing(self):
    if 18 in self.values:
      return tofloat(self.values[18])
    else:
      return None
  def getplayerquestlog74(self):
    if 271 in self.values:
      return self.values[271]
    else:
      return None
  def getplayerquestlog71(self):
    if 268 in self.values:
      return self.values[268]
    else:
      return None
  def getplayerquestlog72(self):
    if 269 in self.values:
      return self.values[269]
    else:
      return None
  def getplayerquestlog73(self):
    a = []
    for x in range(270,271):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldstackcount(self):
    if 14 in self.values:
      return self.values[14]
    else:
      return None
  def getcorpsefieldparty(self):
    if 8 in self.values and 9 in self.values:
      return toint64(self.values[8],self.values[9])
    else:
      return None
  def getplayervisibleitem8creator(self):
    if 456 in self.values and 457 in self.values:
      return toint64(self.values[456],self.values[457])
    else:
      return None
  def getplayerquestlog244(self):
    if 339 in self.values:
      return self.values[339]
    else:
      return None
  def getdynamicobjectspellid(self):
    if 9 in self.values:
      return self.values[9]
    else:
      return None
  def getplayervisibleitem3properties(self):
    a = []
    for x in range(390,391):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog14(self):
    if 247 in self.values:
      return self.values[247]
    else:
      return None
  def getunitfieldbaseattacktime(self):
    a = []
    for x in range(147,149):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog12(self):
    if 245 in self.values:
      return self.values[245]
    else:
      return None
  def getplayerquestlog13(self):
    a = []
    for x in range(246,247):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldlifetimehonorablekills(self):
    if 1517 in self.values:
      return self.values[1517]
    else:
      return None
  def getunitfieldattackpower(self):
    if 210 in self.values:
      return self.values[210]
    else:
      return None
  def getunitfieldaurastate(self):
    if 146 in self.values:
      return self.values[146]
    else:
      return None
  def getplayervisibleitem19pad(self):
    if 647 in self.values:
      return self.values[647]
    else:
      return None
  def getplayerquestlog31(self):
    if 252 in self.values:
      return self.values[252]
    else:
      return None
  def getplayerquestlog32(self):
    if 253 in self.values:
      return self.values[253]
    else:
      return None
  def getplayerquestlog33(self):
    a = []
    for x in range(254,255):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog34(self):
    if 255 in self.values:
      return self.values[255]
    else:
      return None
  def getplayervisibleitem13creator(self):
    if 536 in self.values and 537 in self.values:
      return toint64(self.values[536],self.values[537])
    else:
      return None
  def getplayerquestlog172(self):
    if 309 in self.values:
      return self.values[309]
    else:
      return None
  def getplayerquestlog173(self):
    a = []
    for x in range(310,311):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog171(self):
    if 308 in self.values:
      return self.values[308]
    else:
      return None
  def getplayerquestlog174(self):
    if 311 in self.values:
      return self.values[311]
    else:
      return None
  def getplayerfieldmoddamagedonepos(self):
    a = []
    for x in range(1462,1469):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldresistancebuffmodspositive(self):
    a = []
    for x in range(193,200):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem2creator(self):
    if 360 in self.values and 361 in self.values:
      return toint64(self.values[360],self.values[361])
    else:
      return None
  def getplayerquestlog154(self):
    if 303 in self.values:
      return self.values[303]
    else:
      return None
  def getplayerquestlog151(self):
    if 300 in self.values:
      return self.values[300]
    else:
      return None
  def getplayerquestlog152(self):
    if 301 in self.values:
      return self.values[301]
    else:
      return None
  def getplayerquestlog153(self):
    a = []
    for x in range(302,303):
      if x in self.values:
	a.append(x)
    return a
  def getcorpsefieldbytes2(self):
    a = []
    for x in range(35,36):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjectstate(self):
    if 14 in self.values:
      return self.values[14]
    else:
      return None
  def getplayerquestlog191(self):
    if 316 in self.values:
      return self.values[316]
    else:
      return None
  def getplayerquestlog192(self):
    if 317 in self.values:
      return self.values[317]
    else:
      return None
  def getplayervisibleitem7pad(self):
    if 455 in self.values:
      return self.values[455]
    else:
      return None
  def getplayerquestlog194(self):
    if 319 in self.values:
      return self.values[319]
    else:
      return None
  def getcorpsefieldposy(self):
    if 12 in self.values:
      return tofloat(self.values[12])
    else:
      return None
  def getcorpsefieldposx(self):
    if 11 in self.values:
      return tofloat(self.values[11])
    else:
      return None
  def getcorpsefieldposz(self):
    if 13 in self.values:
      return tofloat(self.values[13])
    else:
      return None
  def getplayerchosentitle(self):
    if 648 in self.values:
      return self.values[648]
    else:
      return None
  def getplayerquestlog221(self):
    if 328 in self.values:
      return self.values[328]
    else:
      return None
  def getplayervisibleitem60(self):
    a = []
    for x in range(426,438):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldmodhealingdonepos(self):
    if 1483 in self.values:
      return self.values[1483]
    else:
      return None
  def getplayervisibleitem9creator(self):
    if 472 in self.values and 473 in self.values:
      return toint64(self.values[472],self.values[473])
    else:
      return None
  def getunitfieldpetexperience(self):
    if 162 in self.values:
      return self.values[162]
    else:
      return None
  def getplayerquestlog134(self):
    if 295 in self.values:
      return self.values[295]
    else:
      return None
  def getplayerquestlog132(self):
    if 293 in self.values:
      return self.values[293]
    else:
      return None
  def getplayerquestlog133(self):
    a = []
    for x in range(294,295):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog131(self):
    if 292 in self.values:
      return self.values[292]
    else:
      return None
  def getplayerquestlog111(self):
    if 284 in self.values:
      return self.values[284]
    else:
      return None
  def getplayerquestlog112(self):
    if 285 in self.values:
      return self.values[285]
    else:
      return None
  def getplayerquestlog113(self):
    a = []
    for x in range(286,287):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog114(self):
    if 287 in self.values:
      return self.values[287]
    else:
      return None
  def getdynamicobjectcasttime(self):
    a = []
    for x in range(15,34):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldgiftcreator(self):
    if 12 in self.values:
      return tofloat(self.values[12])
    else:
      return None
  def getunitfieldfactiontemplate(self):
    a = []
    for x in range(35,36):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldmodmanaregen(self):
    if 1564 in self.values:
      return tofloat(self.values[1564])
    else:
      return None
  def getcorpsefieldpad(self):
    if 39 in self.values:
      return self.values[39]
    else:
      return None
  def getplayervisibleitem20(self):
    a = []
    for x in range(362,374):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem10properties(self):
    a = []
    for x in range(502,503):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldenchantment(self):
    if 22 in self.values:
      return self.values[22]
    else:
      return None
  def getunitfieldposstat0(self):
    if 176 in self.values:
      return self.values[176]
    else:
      return None
  def getunitfieldstat4(self):
    if 175 in self.values:
      return self.values[175]
    else:
      return None
  def getplayervisibleitem15pad(self):
    if 583 in self.values:
      return self.values[583]
    else:
      return None
  def getunitfieldstat0(self):
    if 171 in self.values:
      return self.values[171]
    else:
      return None
  def getunitfieldstat1(self):
    if 172 in self.values:
      return self.values[172]
    else:
      return None
  def getunitfieldstat2(self):
    if 173 in self.values:
      return self.values[173]
    else:
      return None
  def getunitfieldstat3(self):
    if 174 in self.values:
      return self.values[174]
    else:
      return None
  def getgameobjectrotation(self):
    if 10 in self.values:
      return tofloat(self.values[10])
    else:
      return None
  def getplayervisibleitem80(self):
    a = []
    for x in range(458,470):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldmaxdurability(self):
    if 59 in self.values:
      return self.values[59]
    else:
      return None
  def getplayerskillinfo11(self):
    a = []
    for x in range(928,1312):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog193(self):
    a = []
    for x in range(318,319):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem19creator(self):
    if 632 in self.values and 633 in self.values:
      return toint64(self.values[632],self.values[633])
    else:
      return None
  def getplayerquestlog84(self):
    if 275 in self.values:
      return self.values[275]
    else:
      return None
  def getplayerquestlog83(self):
    a = []
    for x in range(274,275):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog82(self):
    if 273 in self.values:
      return self.values[273]
    else:
      return None
  def getplayerquestlog81(self):
    if 272 in self.values:
      return self.values[272]
    else:
      return None
  def getunitfieldpowercostmodifier(self):
    a = []
    for x in range(218,225):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog43(self):
    a = []
    for x in range(258,259):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog42(self):
    if 257 in self.values:
      return self.values[257]
    else:
      return None
  def getplayerquestlog41(self):
    if 256 in self.values:
      return self.values[256]
    else:
      return None
  def getplayerquestlog44(self):
    if 259 in self.values:
      return self.values[259]
    else:
      return None
  def getplayerquestlog144(self):
    if 299 in self.values:
      return self.values[299]
    else:
      return None
  def getplayerduelteam(self):
    if 242 in self.values:
      return self.values[242]
    else:
      return None
  def getplayerfieldmodtargetphysicalresistance(self):
    if 1485 in self.values:
      return self.values[1485]
    else:
      return None
  def getplayerquestlog21(self):
    if 248 in self.values:
      return self.values[248]
    else:
      return None
  def getplayerquestlog23(self):
    a = []
    for x in range(250,251):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog22(self):
    if 249 in self.values:
      return self.values[249]
    else:
      return None
  def getplayerquestlog24(self):
    if 251 in self.values:
      return self.values[251]
    else:
      return None
  def getplayerfieldyesterdaycontribution(self):
    if 1516 in self.values:
      return self.values[1516]
    else:
      return None
  def getplayervisibleitem8properties(self):
    a = []
    for x in range(470,471):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem4pad(self):
    if 407 in self.values:
      return self.values[407]
    else:
      return None
  def getplayerquestlog64(self):
    if 267 in self.values:
      return self.values[267]
    else:
      return None
  def getplayerfieldcombatrating1(self):
    a = []
    for x in range(1520,1544):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog61(self):
    if 264 in self.values:
      return self.values[264]
    else:
      return None
  def getcorpsefieldbytes1(self):
    a = []
    for x in range(34,35):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog63(self):
    a = []
    for x in range(266,267):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog62(self):
    if 265 in self.values:
      return self.values[265]
    else:
      return None
  def getitemfieldpropertyseed(self):
    if 55 in self.values:
      return self.values[55]
    else:
      return None
  def getplayervisibleitem1pad(self):
    if 359 in self.values:
      return self.values[359]
    else:
      return None
  def getplayervisibleitem11pad(self):
    if 519 in self.values:
      return self.values[519]
    else:
      return None
  def getplayerfieldmodmanaregeninterrupt(self):
    if 1565 in self.values:
      return tofloat(self.values[1565])
    else:
      return None
  def getplayervisibleitem15creator(self):
    if 568 in self.values and 569 in self.values:
      return toint64(self.values[568],self.values[569])
    else:
      return None
  def getunitfieldpower3(self):
    if 25 in self.values:
      return self.values[25]
    else:
      return None
  def getplayervisibleitem12pad(self):
    if 535 in self.values:
      return self.values[535]
    else:
      return None
  def getplayertrackresources(self):
    if 1315 in self.values:
      return self.values[1315]
    else:
      return None
  def getplayerflags(self):
    if 236 in self.values:
      return self.values[236]
    else:
      return None
  def getitemfieldrandompropertiesid(self):
    if 56 in self.values:
      return self.values[56]
    else:
      return None
  def getplayerquestlog141(self):
    if 296 in self.values:
      return self.values[296]
    else:
      return None
  def getplayerquestlog143(self):
    a = []
    for x in range(298,299):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog142(self):
    if 297 in self.values:
      return self.values[297]
    else:
      return None
  def getplayerammoid(self):
    if 1487 in self.values:
      return self.values[1487]
    else:
      return None
  def getobjectfieldentry(self):
    if 3 in self.values:
      return self.values[3]
    else:
      return None
  def getplayerquestlog181(self):
    if 312 in self.values:
      return self.values[312]
    else:
      return None
  def getplayerquestlog183(self):
    a = []
    for x in range(314,315):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog182(self):
    if 313 in self.values:
      return self.values[313]
    else:
      return None
  def getplayerfieldkeyringslot1(self):
    a = []
    for x in range(822,886):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog184(self):
    if 315 in self.values:
      return self.values[315]
    else:
      return None
  def getplayerquestlog163(self):
    a = []
    for x in range(306,307):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog162(self):
    if 305 in self.values:
      return self.values[305]
    else:
      return None
  def getplayerquestlog161(self):
    if 304 in self.values:
      return self.values[304]
    else:
      return None
  def getunitfieldauralevels(self):
    a = []
    for x in range(118,132):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldlevel(self):
    a = []
    for x in range(34,35):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem18pad(self):
    if 631 in self.values:
      return self.values[631]
    else:
      return None
  def getplayerquestlog164(self):
    if 307 in self.values:
      return self.values[307]
    else:
      return None
  def getplayervisibleitem50(self):
    a = []
    for x in range(410,422):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldcoinage(self):
    if 1461 in self.values:
      return self.values[1461]
    else:
      return None
  def getobjectfieldcreatedby(self):
    if 6 in self.values and 7 in self.values:
      return toint64(self.values[6],self.values[7])
    else:
      return None
  def getitemfielddurability(self):
    if 58 in self.values:
      return self.values[58]
    else:
      return None
  def getcorpsefieldowner(self):
    if 6 in self.values and 7 in self.values:
      return toint64(self.values[6],self.values[7])
    else:
      return None
  def getplayervisibleitem70(self):
    a = []
    for x in range(442,454):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog124(self):
    if 291 in self.values:
      return self.values[291]
    else:
      return None
  def getplayerquestlog123(self):
    a = []
    for x in range(290,291):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog122(self):
    if 289 in self.values:
      return self.values[289]
    else:
      return None
  def getplayerquestlog121(self):
    if 288 in self.values:
      return self.values[288]
    else:
      return None
  def getplayerquestlog101(self):
    if 280 in self.values:
      return self.values[280]
    else:
      return None
  def getunitfieldmindamage(self):
    if 155 in self.values:
      return tofloat(self.values[155])
    else:
      return None
  def getplayerquestlog103(self):
    a = []
    for x in range(282,283):
      if x in self.values:
	a.append(x)
    return a
  def getplayerquestlog102(self):
    if 281 in self.values:
      return self.values[281]
    else:
      return None
  def getplayerquestlog104(self):
    if 283 in self.values:
      return self.values[283]
    else:
      return None
  def getplayerfielddailyquests1(self):
    a = []
    for x in range(1567,1592):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem16creator(self):
    if 584 in self.values and 585 in self.values:
      return toint64(self.values[584],self.values[585])
    else:
      return None
  def getplayervisibleitem16pad(self):
    if 599 in self.values:
      return self.values[599]
    else:
      return None
  def getplayerparrypercentage(self):
    if 1318 in self.values:
      return tofloat(self.values[1318])
    else:
      return None
  def getobjectfieldguid(self):
    if 0 in self.values and 1 in self.values:
      return toint64(self.values[0],self.values[1])
    else:
      return None
  def getplayervisibleitem6properties(self):
    a = []
    for x in range(438,439):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem17creator(self):
    if 600 in self.values and 601 in self.values:
      return toint64(self.values[600],self.values[601])
    else:
      return None
  def getunitfieldtarget(self):
    if 16 in self.values:
      return unpack("Q",pack("II",self.values[16],self.values[17]))[0]
    else:
      return None
  def getplayervisibleitem2pad(self):
    if 375 in self.values:
      return self.values[375]
    else:
      return None
  def getplayervisibleitem11properties(self):
    a = []
    for x in range(518,519):
      if x in self.values:
	a.append(x)
    return a
  def getgameobjecttypeid(self):
    if 21 in self.values:
      return self.values[21]
    else:
      return None
  def getplayervisibleitem10(self):
    a = []
    for x in range(346,358):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldauraapplications(self):
    a = []
    for x in range(132,146):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem14pad(self):
    if 567 in self.values:
      return self.values[567]
    else:
      return None
  def getplayerfieldknowntitles(self):
    if 924 in self.values and 925 in self.values:
      return toint64(self.values[924],self.values[925])
    else:
      return None
  def getplayervisibleitem30(self):
    a = []
    for x in range(378,390):
      if x in self.values:
	a.append(x)
    return a
  def getplayerblockpercentage(self):
    if 1316 in self.values:
      return tofloat(self.values[1316])
    else:
      return None
  def getplayervisibleitem170(self):
    a = []
    for x in range(602,614):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldrangedattacktime(self):
    if 149 in self.values:
      return self.values[149]
    else:
      return None
  def getplayervisibleitem19properties(self):
    a = []
    for x in range(646,647):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem10creator(self):
    if 488 in self.values and 489 in self.values:
      return toint64(self.values[488],self.values[489])
    else:
      return None
  def getunitfieldsummon(self):
    if 8 in self.values and 9 in self.values:
      return toint64(self.values[8],self.values[9])
    else:
      return None
  def getunitnpcflags(self):
    if 168 in self.values:
      return self.values[168]
    else:
      return None
  def getplayervisibleitem130(self):
    a = []
    for x in range(538,550):
      if x in self.values:
	a.append(x)
    return a
  def getplayerguildrank(self):
    if 238 in self.values:
      return self.values[238]
    else:
      return None
  def getunitfieldposstat1(self):
    if 177 in self.values:
      return self.values[177]
    else:
      return None
  def getitemfieldspellcharges(self):
    if 16 in self.values:
      return tofloat(self.values[16])
    else:
      return None
  def getunitfieldposstat3(self):
    if 179 in self.values:
      return self.values[179]
    else:
      return None
  def getplayervisibleitem3pad(self):
    if 391 in self.values:
      return self.values[391]
    else:
      return None
  def getplayervisibleitem12properties(self):
    a = []
    for x in range(534,535):
      if x in self.values:
	a.append(x)
    return a
  def getcorpsefielddisplayid(self):
    if 14 in self.values:
      return self.values[14]
    else:
      return None
  def getplayervisibleitem150(self):
    a = []
    for x in range(570,582):
      if x in self.values:
	a.append(x)
    return a
  def getitemfieldflags(self):
    if 21 in self.values:
      return self.values[21]
    else:
      return None
  def getplayerfieldarenateaminfo11(self):
    a = []
    for x in range(1544,1562):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem190(self):
    a = []
    for x in range(634,646):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem16properties(self):
    a = []
    for x in range(598,599):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem40(self):
    a = []
    for x in range(394,406):
      if x in self.values:
	a.append(x)
    return a
  def getplayerbytes(self):
    a = []
    for x in range(239,240):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem180(self):
    a = []
    for x in range(618,630):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem8pad(self):
    if 471 in self.values:
      return self.values[471]
    else:
      return None
  def getunitfieldauraflags(self):
    a = []
    for x in range(104,118):
      if x in self.values:
	a.append(x)
    return a
  def getplayerbytes2(self):
    a = []
    for x in range(240,241):
      if x in self.values:
	a.append(x)
    return a
  def getplayerbytes3(self):
    a = []
    for x in range(241,242):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem13properties(self):
    a = []
    for x in range(550,551):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldmaxdamage(self):
    if 156 in self.values:
      return tofloat(self.values[156])
    else:
      return None
  def getplayerfieldpad0(self):
    if 649 in self.values:
      return self.values[649]
    else:
      return None
  def getunitfieldmaxrangeddamage(self):
    if 217 in self.values:
      return tofloat(self.values[217])
    else:
      return None
  def getplayervisibleitem110(self):
    a = []
    for x in range(506,518):
      if x in self.values:
	a.append(x)
    return a
  def getplayervisibleitem5properties(self):
    a = []
    for x in range(422,423):
      if x in self.values:
	a.append(x)
    return a
  def getplayerguildid(self):
    if 237 in self.values:
      return self.values[237]
    else:
      return None
  def getplayerfieldmodtargetresistance(self):
    if 1484 in self.values:
      return self.values[1484]
    else:
      return None
  def getplayerquestlog243(self):
    a = []
    for x in range(338,339):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldbuybackprice1(self):
    a = []
    for x in range(1490,1502):
      if x in self.values:
	a.append(x)
    return a
  def getobjectfieldtype(self):
    if 2 in self.values:
      return self.values[2]
    else:
      return None
  def getplayervisibleitem15properties(self):
    a = []
    for x in range(582,583):
      if x in self.values:
	a.append(x)
    return a
  def getplayeroffhandexpertise(self):
    if 1320 in self.values:
      return self.values[1320]
    else:
      return None
  def getunitfieldboundingradius(self):
    if 150 in self.values:
      return tofloat(self.values[150])
    else:
      return None
  def getunitfieldflags(self):
    if 46 in self.values:
      return self.values[46]
    else:
      return None
  def getplayerfieldinvslothead(self):
    a = []
    for x in range(650,696):
      if x in self.values:
	a.append(x)
    return a
  def getunitfieldminrangeddamage(self):
    if 216 in self.values:
      return tofloat(self.values[216])
    else:
      return None
  def getplayerfarsight(self):
    if 922 in self.values and 923 in self.values:
      return toint64(self.values[922],self.values[923])
    else:
      return None
  def getplayervisibleitem90(self):
    a = []
    for x in range(474,486):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldvendorbuybackslot1(self):
    a = []
    for x in range(798,822):
      if x in self.values:
	a.append(x)
    return a
  def getplayerfieldbytes2(self):
    a = []
    for x in range(1518,1519):
      if x in self.values:
	a.append(x)
    return a

def parseupdateobject(world,data):
  #debug("UpdateObject %d bytes"%len(data))
  #time.sleep(10.0)
  s2 = str(data)  
  blockcount = unpack("I",s2[:4])[0]
  s2 = s2[4:]
  hastransport = bool(ord(s2[0]))
  s2 = s2[1:]
  #print "%d Blocks, hasTransport = %s" % (blockcount,str(hastransport))
  
  while len(s2) > 0:
    utype = ord(s2[0])
    s2 = s2[1:]
    #print "***",utype
    if utype == UPDATETYPE_OUT_OF_RANGE_OBJECTS:
      guids, s2 = parseoutofrangeobjblock(s2)
      for g in guids:
	world.delobject(g)
    if utype == UPDATETYPE_VALUES:
      guid,values, s2 = parsevaluesupdate(s2)
      world.getobject(guid).mergevalues(values)
      if 'updateobjectcb' in dir(world.wowist):
	world.wowist.updateobjectcb(guid,world)
    if utype == UPDATETYPE_MOVEMENT:
      guid,data,s2 = parsemovementupdate(s2)
      world.getobject(guid).x = data["pos"][0]
      world.getobject(guid).y = data["pos"][1]
      world.getobject(guid).z = data["pos"][2]
      world.getobject(guid).o = data["pos"][3]
      world.wowinst.updatetarget()
    if utype == UPDATETYPE_CREATE_OBJECT or utype == UPDATETYPE_CREATE_OBJECT2:
      guid,typeid,data,values,s2 = parsecreateobject(s2)
      if "pos" in data:
	inst = WorldObject(guid,typeid,data["pos"][0],data["pos"][1],data["pos"][2],data["pos"][3])
      else:
	inst = WorldObject(guid,typeid,0.0,0.0,0.0,0.0)
      
      world.addtoworld(inst)
      world.getobject(guid).mergevalues(values)
      if 'createobjectcb' in dir(world.wowist):
	world.wowist.createobjectcb(guid,world)
    if utype == UPDATETYPE_NEAR_OBJECTS:
      print "near"
      #time.sleep(100.0)

fc = 0

class World:
  def __init__(self,WOWIst):
    self.wowist = WOWIst
    self.objects = { TYPEID_AIGROUP : dict() , TYPEID_AREATRIGGER : dict(), TYPEID_CONTAINER : dict() , TYPEID_CORPSE : dict() , TYPEID_DYNAMICOBJECT : dict() , TYPEID_GAMEOBJECT : dict() , TYPEID_ITEM : dict() , TYPEID_ITEM : dict(), TYPEID_OBJECT : dict() , TYPEID_PLAYER : dict(), TYPEID_UNIT : dict() }
    self.objectsbyguid = dict()
  def addtoworld(self,obj):
    self.objects[obj.t][obj.guid] = obj
    self.objectsbyguid[obj.guid] = obj
  def getobject(self,guid):
    if guid in self.objectsbyguid:
      return self.objectsbyguid[guid]
  def delobject(self,guid):
    if guid in self.objectsbyguid:
      del self.objects[self.objectsbyguid[guid].t][guid]
      del self.objectsbyguid[guid]
  def handlecompressedupdateobject(self,data):
    origdatasize = unpack("I",data[:4])
    origdata = zlib.decompress(data[4:])
    if origdatasize != len(origdata):
      error("Dimensione update object compresso non valida")
    self.handleplainupdateobject(str(origdata))
  def handleplainupdateobject(self,data_):
    #global fc
    #f = open("UO%d.raw"%fc,"wb")
    #f.write(data_)
    #f.close()
    #fc += 1
    parseupdateobject(self,str(data_))