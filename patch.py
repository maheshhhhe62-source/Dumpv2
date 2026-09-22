import sys, os
cands=[sys.argv[1]] if len(sys.argv)>1 else ["new.py","test.py","bot.py"]
fn=None
for c in cands:
    if os.path.exists(c): fn=c; break
if not fn:
    print("NO MAIN FILE FOUND - keep patch.py next to your bot file"); sys.exit(1)
src=open(fn,"r",encoding="utf-8").read()
if "def turbo_parse(" not in src or "# ============ INJECTOR v3" not in src:
    print("MARKERS NOT FOUND in",fn); sys.exit(1)
a=src.index("def turbo_parse(")
b=src.index("# ============ INJECTOR v3")
if "# LIVE-PARSER-v2" in src[a:b]:
    print("ALREADY PATCHED:",fn); sys.exit(0)
NEW=r'''def turbo_parse(cid,uid,mid,jid,dorks,engines,fresh,mode,threads=15):
    # LIVE-PARSER-v2
    try:
        proxies=hprox(uid); results=[]; seen=set(); done=[0]; estat={}; blocked=set(); reqs=[0]; t0=time.time(); cooldowns={}
        bump("parse"); bumpU(uid,"parse")
        if len(proxies)<sget("hunt_below",10):
            threading.Thread(target=turbo_hunt,args=(0,uid,0,0,150),kwargs={"silent":True},daemon=True).start()
        w=ew_get(); engines=sorted(engines,key=lambda e:-w.get(e,0))[:3]
        cs=max(1,int(sget("admin_chunk_size",5000)))
        chunks=[dorks[i:i+cs] for i in range(0,len(dorks),cs)]; tc=len(chunks)
        async def run():
            conn=aiohttp.TCPConnector(limit=threads+10,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)
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
                    last=[0.0]
                    while alive[0]:
                        await asyncio.sleep(2)
                        now=time.time()
                        if now-last[0]<2: continue
                        last[0]=now
                        et=" ".join(f"{EMO.get(k,'•')}{v}" for k,v in sorted(estat.items(),key=lambda x:-x[1]) if v)
                        rps=round(reqs[0]/max(1,now-t0),1)
                        blk=", ".join(sorted(blocked)) if blocked else "—"
                        try: bot.edit_message_text(f"🌐 SHADOW PARSER ⚡\n{LINE}\n🛡️ {len(act)} | ⚡ {rps} r/s | 🧵 {threads} Threads\n{bar(done[0],len(dorks))} {pct(done[0],len(dorks))}% ({done[0]}/{len(dorks)})\n🔗 URLs: {len(results)} | ⛔ {blk}\n🏆 {et}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
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
                            for pg in range(mode["pages"]):
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
                        results.extend(await fut)
                        done[0]+=1
                alive[0]=False
                try: ed.cancel()
                except: pass
        _run_on_loop(run())
        w2=ew_get()
        for k,v in estat.items():
            if v: w2[k]=w2.get(k,0)+1
        save_json(EW_FILE,w2)
        urls=uhq_filter(scope_filter(dns_filter(results)))
        clear_markup(cid,mid)
        blk=", ".join(sorted(blocked)) if blocked else "none"
        if blocked and set(engines)<=blocked:
            for a in admins():
                try: bot.send_message(a,f"🚨 ALL ENGINES BLOCKED\n{LINE}\n👤 {uid} | 🛡️ {len(proxies)} proxies")
                except: pass
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
open(fn,"w",encoding="utf-8").write(src[:a]+NEW+"\n"+src[b:])
print("PATCHED",fn,"- now run: python",fn)
