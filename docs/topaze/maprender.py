import json,struct,re,os,sys,collections
from PIL import Image
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/'
hdr=open(R+'src/data/tilesets/headers.h').read()
met=open(R+'src/data/tilesets/metatiles.h').read()
def tsdir(name):
    m=re.search(r'gMetatiles_%s\[\] = INCBIN_U16\("([^"]+)/metatiles.bin"\)'%name[len('gTileset_'):],met)
    return R+m.group(1)+'/'
def pal(p):
    L=open(p).read().split(); n=int(L[2]); return [tuple(int(x) for x in L[3+3*k:6+3*k]) for k in range(n)]
_c={}
def loadts(name):
    if name in _c: return _c[name]
    d=tsdir(name)
    img=Image.open(d+'tiles.png').convert('P')
    pals=[]
    for i in range(16):
        p=d+'palettes/%02d.pal'%i
        pals.append(pal(p) if os.path.exists(p) else [(0,0,0)]*16)
    mt=struct.unpack('<%dH'%(os.path.getsize(d+'metatiles.bin')//2),open(d+'metatiles.bin','rb').read())
    _c[name]=(img,pals,mt); return _c[name]
def tile(P,S,t,p,hf,vf,pals):
    img=P[0] if t<640 else S[0]; idx=t if t<640 else t-640
    w=img.size[0]//8
    c=img.crop(((idx%w)*8,(idx//w)*8,(idx%w)*8+8,(idx//w)*8+8))
    o=Image.new('RGBA',(8,8)); px=o.load(); r=c.load()
    for y in range(8):
        for x in range(8):
            i=r[x,y]
            px[x,y]=(0,0,0,0) if i==0 else tuple(pals[p][i])+(255,)
    if hf:o=o.transpose(Image.FLIP_LEFT_RIGHT)
    if vf:o=o.transpose(Image.FLIP_TOP_BOTTOM)
    return o
def metatile(P,S,pals,m):
    mt=P[2] if m<640 else S[2]; i=m if m<640 else m-640
    e=mt[i*8:i*8+8]
    im=Image.new('RGBA',(16,16),tuple(pals[0][0])+(255,))
    for layer in (0,1):
        for k in range(4):
            v=e[layer*4+k]
            im.alpha_composite(tile(P,S,v&0x3ff,v>>12,v&0x400,v&0x800,pals),((k%2)*8,(k//2)*8))
    return im
def render(l,out,marg=0):
    P=loadts(l['primary_tileset']);S=loadts(l['secondary_tileset'])
    pals=[P[1][i] for i in range(7)]+[S[1][i] for i in range(7,13)]+[S[1][13],S[1][14],S[1][15]]
    w,h=l['width'],l['height']
    g=struct.unpack('<%dH'%(w*h),open(R+l['blockdata_filepath'],'rb').read())
    cache={};im=Image.new('RGB',(w*16,h*16))
    for y in range(h):
        for x in range(w):
            m=g[y*w+x]&0x3ff
            if m not in cache: cache[m]=metatile(P,S,pals,m)
            im.paste(cache[m].convert('RGB'),(x*16,y*16))
    im.save(out)
if __name__=='__main__':
    L={x['id']:x for x in json.load(open(R+'data/layouts/layouts.json'))['layouts'] if x.get('id')}
    for a in sys.argv[1:]:
        render(L[a],'/tmp/gx/maps/%s.png'%a)
