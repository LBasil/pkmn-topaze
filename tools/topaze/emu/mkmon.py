import struct
RAW=bytes.fromhex("ba ba 9f 3e c1 99 56 ff bd c2 bb cc c7 bb c8 be bf cc 02 02 bb bb bb bb ff ff ff 00 5b 44 00 00 7f 23 c9 c1 b7 23 c9 c1 7b 6f c9 c1 7b 23 c8 c1 7b 23 c9 c1 7b 23 c9 c1 71 23 e4 c1 4f 23 c9 c1 58 0b d0 c1 7b 7b cc e3 6c 73 0e c5 7b 23 c9 c1 00 00 00 00 06 ff 16 00 16 00 0b 00 0b 00 0d 00 0c 00 0b 00")
def make(species, nick=None, level=6):
    b=bytearray(RAW)
    pid,oid=struct.unpack('<II',b[:8]); key=pid^oid
    d=bytearray(b[32:80])
    for i in range(0,48,4):
        w=struct.unpack('<I',d[i:i+4])[0]^key; d[i:i+4]=struct.pack('<I',w)
    order=[ 'GAEM','GAME','GEAM','GEMA','GMAE','GMEA','AGEM','AGME','AEGM','AEMG','AMGE','AMEG','EGAM','EGMA','EAGM','EAMG','EMGA','EMAG','MGAE','MGEA','MAGE','MAEG','MEGA','MEAG'][pid%24]
    gi=order.index('G')*12
    d[gi:gi+2]=struct.pack('<H',species)
    ck=sum(struct.unpack('<24H',bytes(d)))&0xffff
    b[28:30]=struct.pack('<H',ck)
    for i in range(0,48,4):
        w=struct.unpack('<I',d[i:i+4])[0]^key; d[i:i+4]=struct.pack('<I',w)
    b[32:80]=d
    b[84]=level
    return bytes(b)
def writes(addr,data): return ['write %08x %02x'%(addr+i,x) for i,x in enumerate(data)]
def exp_of(hexbytes):
    b=bytes.fromhex(hexbytes)
    pid,oid=struct.unpack('<II',b[:8]); key=pid^oid
    d=bytearray(b[32:80])
    for i in range(0,48,4):
        w=struct.unpack('<I',d[i:i+4])[0]^key; d[i:i+4]=struct.pack('<I',w)
    order=['GAEM','GAME','GEAM','GEMA','GMAE','GMEA','AGEM','AGME','AEGM','AEMG','AMGE','AMEG','EGAM','EGMA','EAGM','EAMG','EMGA','EMAG','MGAE','MGEA','MAGE','MAEG','MEGA','MEAG'][pid%24]
    gi=order.index('G')*12
    return struct.unpack('<HHI',d[gi:gi+8])
