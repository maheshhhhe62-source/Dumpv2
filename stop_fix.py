import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
if "# STOP-FIX-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
miss=[]
def rep(old,new):
    global src
    if old in src: src=src.replace(old,new,1)
    else: miss.append(old[:40])
H1=r'''LIVE={}
def _partial_sender(jid,cid):
    # STOP-FIX-v1
    time.sleep(10)
    e=LIVE.pop(jid,None)
    if not e: return
    try:
        if e["kind"]=="parse":
            urls=uhq_filter(scope_filter(e["results"]))
            if urls:
                send_doc(cid,("\n".join(urls)+"\n").encode(),"urls_partial.txt")
                bot.send_message(cid,f"⏹️ PARTIAL PARSE\n{LINE}\n🔗 {len(urls)} URLs")
            else: bot.send_message(cid,"⏹️ STOPPED — koi URL nahi mila tha.")
        elif e["kind"]=="inject":
            vurls=[v["url"] for v in e["vuln"]]
            if vurls:
                send_doc(cid,("\n".join(vurls)+"\n").encode(),"vulnerable_urls.txt")
                bot.send_message(cid,f"⏹️ PARTIAL INJECT\n{LINE}\n🩸 {len(vurls)} | 🛡️ {len(e['nonev'])}")
            else: bot.send_message(cid,"⏹️ STOPPED — koi vuln nahi mila tha.")
        elif e["kind"]=="dump":
            if e["dumps"]:
                send_doc(cid,build_zip(e["dumps"]),"data_dump_partial.zip")
                bot.send_message(cid,f"⏹️ PARTIAL DUMP\n{LINE}\n💾 {len(e['dumps'])} sites")
            else: bot.send_message(cid,"⏹️ STOPPED — koi dump nahi aaya tha.")
    except Exception as ex:
        try: bot.send_message(cid,f"🐞 PARTIAL BUG: {type(ex).__name__}")
        except: pass
'''
rep("def turbo_parse(",H1+"def turbo_parse(")
rep('        results=list(seed); seen=set(seed); dorks=dorks[skip:]','        results=list(seed); seen=set(seed); dorks=dorks[skip:]\n        LIVE[jid]={"kind":"parse","results":results}')
rep('        urls=uhq_filter(scope_filter(dns_filter(results)))','        if stopped(jid):\n            clear_markup(cid,mid); jp_unreg(jid); LIVE.pop(jid,None); return\n        urls=uhq_filter(scope_filter(dns_filter(results)))')
rep('        vuln=[]; nonev=[]; done=[0]; last=[0.0]; details=[]; reqs=[0]; wafed=[0]; dbst={}; t0=time.time(); since_save=[0]','        vuln=[]; nonev=[]; done=[0]; last=[0.0]; details=[]; reqs=[0]; wafed=[0]; dbst={}; t0=time.time(); since_save=[0]\n        LIVE[jid]={"kind":"inject","vuln":vuln,"nonev":nonev}')
rep('        save_json(VULN_CACHE,vc); clear_markup(cid,mid); jp_unreg(jid)','        save_json(VULN_CACHE,vc); clear_markup(cid,mid); jp_unreg(jid)\n        if stopped(jid): LIVE.pop(jid,None); return')
rep('        ph=PH(uprox(uid)); dumps=[]; done=[0]; last=[0.0]; cur=["-"]; cached=[0]','        ph=PH(uprox(uid)); dumps=[]; done=[0]; last=[0.0]; cur=["-"]; cached=[0]\n        LIVE[jid]={"kind":"dump","dumps":dumps}')
rep('        juicy_found=[]','        if stopped(jid):\n            save_json(DUMP_CACHE,dc); clear_markup(cid,mid); jp_unreg(jid); LIVE.pop(jid,None); return\n        juicy_found=[]')
rep('        try: bot.edit_message_text("⏹️ STOPPED! Partial file aa rahi ha...",chat_id=cid,message_id=mid)\n        except: pass\n        return','        try: bot.edit_message_text("⏹️ STOPPED! Partial file aa rahi ha...",chat_id=cid,message_id=mid)\n        except: pass\n        threading.Thread(target=_partial_sender,args=(jid,cid),daemon=True).start()\n        return')
if miss:
    print("MISSING MARKERS:",miss); sys.exit(1)
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("STOP-FIX DONE - SYNTAX OK:",fn)
except Exception as e:
    print("STILL:",e)
