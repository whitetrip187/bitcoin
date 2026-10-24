import hashlib,struct,subprocess,sys
d=lambda b:hashlib.sha256(hashlib.sha256(b).digest()).digest()
def push(b): return (bytes([len(b)]) if len(b)<76 else b'\x4c'+bytes([len(b)]))+b
def tx(msg,outscript):
    ss=b'\x04\xff\xff\x00\x1d'+b'\x01\x04'+push(msg.encode())
    t=struct.pack('<i',1)+b'\x01'+b'\x00'*32+b'\xff'*4+bytes([len(ss)])+ss+b'\xff'*4
    t+=b'\x01'+struct.pack('<q',50*10**8)+bytes([len(outscript)])+outscript+b'\x00'*4
    return d(t)
def mine(msg,outscript,ntime,bits,nproc=8):
    while True:
        r=mine1(msg,outscript,ntime,bits,nproc)
        if r: return (ntime,)+r
        ntime+=1
def mine1(msg,outscript,ntime,bits,nproc=8):
    mr=tx(msg,outscript)
    hdr=struct.pack('<i',1)+b'\x00'*32+mr+struct.pack('<II',ntime,bits)
    ps=[subprocess.Popen(['./miner',hdr.hex(),'%x'%bits,str(i),str(nproc)],stdout=subprocess.PIPE,text=True) for i in range(nproc)]
    import select
    res=None
    live=[p.stdout for p in ps]
    while res is None and live:
        r,_,_=select.select(live,[],[])
        for f in r:
            l=f.readline().strip()
            if l and l!='NONE': res=l;break
            live.remove(f)
    if res is None: return None
    for p in ps: p.kill()
    n,h=res.split(); return int(n),h,mr[::-1].hex()
if __name__=='__main__':
    sat=bytes.fromhex('4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac')
    print(mine("The Times 03/Jan/2009 Chancellor on brink of second bailout for banks",sat,1296688602,0x207fffff))
