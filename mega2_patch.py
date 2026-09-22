import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
if "# TRIAL-ROT-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
miss=[]
def rep(old,new):
    global src
    if old in src: src=src.replace(old,new,1)
    else: miss.append(old[:50])
H=r'''def grant_trial(uid):
    # TRIAL-ROT-v1
    try:
        th=int(sget("trial_hours",24))
        u=U(uid)
        if th==0 or u.get("trial_used") or has_license(uid): return
        now=time.time()
        exp=now+3153600000 if th==-1 else now+th*3600
        setU(uid,{"admin_lic":exp,"trial_used":True})
        try: bot.send_message(uid,f"🎁 TRIAL ACTIVATED\n{LINE}\n⏳ "+("LIFETIME access! Enjoy." if th==-1 else f"{th} hours access."))
        except: pass
    except: pass
def mk_eng(data):
    mk=types.InlineKeyboardMarkup()
    sel=data.get("engs",[])
    codes=ALL_ENGINES
    for i in range(0,len(codes),3):
        mk.row(*[btn(("✅" if c in sel else "")+EMO.get(c,"•")+" "+c.upper(),"peng_t:"+c) for c in codes[i:i+3]])
    mk.row(btn("🌍 All","peng_t:all"),btn("🔄 Clear","peng_t:none"))
    mk.row(btn("🕐 24h","fresh:d"),btn("📆 Week","fresh:w"),btn("🌐 All-Time","fresh:"))
    mk.row(sbtn("🚀 RUN","peng_run","success"))
    back_row(mk)
    return mk
'''
rep("def turbo_parse(",H+"def turbo_parse(")
rep('    mk.row(btn("😎 Emoji "+("PREMIUM" if sget("emoji_mode","normal")=="premium" else "NORMAL"),"adm:emo"),btn("⬅️ Back","back"))','    mk.row(btn("😎 Emoji "+("PREMIUM" if sget("emoji_mode","normal")=="premium" else "NORMAL"),"adm:emo"),btn(f"🎁 Trial: {sget(\'trial_hours\',24)}h","adm:trial"))\n    mk.row(btn("🌀 RotProxy "+("ON" if sget("rot_proxy") else "OFF"),"adm:rot"),btn("⬅️ Back","back"))')
rep('    if d=="autostop":','''    if d=="adm:trial":
        with STATES_LOCK: states[uid]=("set_trial",{})
        bot.send_message(cid,f"🎁 TRIAL HOURS\\n{LINE}\\nNumber likho (1-87600) ya 'life' = lifetime\\n0 = trial off\\nCurrent: {sget('trial_hours',24)}h"); return
    if d=="adm:rot":
        with STATES_LOCK: states[uid]=("set_rot",{})
        bot.send_message(cid,f"🌀 ROTATING PROXY\\n{LINE}\\nFormat: http://user:pass@host:port\\n(webshare ka http endpoint, port 80)\\n'off' = band"); return
    if d=="autostop":''')
rep('        setU(uid,{"joined":True}); qualify_ref(uid); send_main(cid,uid); return','        setU(uid,{"joined":True}); grant_trial(uid); qualify_ref(uid); send_main(cid,uid); return')
rep('    if sget("channels",[]) and missing_channels(uid): join_screen(m.chat.id,uid); return\n    send_main(m.chat.id,uid)','    if sget("channels",[]) and missing_channels(uid): join_screen(m.chat.id,uid); return\n    grant_trial(uid)\n    send_main(m.chat.id,uid)')
rep('''        mk=types.InlineKeyboardMarkup()
        mk.row(sbtn("🌐 All Engines","peng:all","success"))
        mk.row(btn(f"{EMO['ddg']} DDG","peng:ddg"),btn(f"{EMO['bing']} Bing","peng:bing"))
        mk.row(btn(f"{EMO['yahoo']} Yahoo","peng:yahoo"),btn(f"{EMO['brave']} Brave","peng:brave"))
        mk.row(btn(f"{EMO['mojeek']} Mojeek","peng:mojeek"),btn(f"{EMO['ecosia']} Ecosia","peng:ecosia"))
        mk.row(btn(f"{EMO['ask']} Ask","peng:ask"),btn(f"{EMO['yep']} Yep","peng:yep"))
        mk.row(btn(f"{EMO['google']} Google","peng:google"),btn(f"{EMO['yandex']} Yandex","peng:yandex"))
        mk.row(btn(f"{EMO['aol']} AOL","peng:aol"),btn(f"{EMO['seekx']} SeekX","peng:seekx"))
        mk.row(btn(f"{EMO['mws']} MyWebSearch","peng:mws"))
        mk.row(btn("🕐 24h","fresh:d"),btn("📆 Week","fresh:w"),btn("🌐 All","fresh:"))
        back_row(mk)
        bot.send_message(m.chat.id,f"🔗 {len(data['dorks'])} dorks | 🧵 {data['threads']} | 📄 {data['pages']} | 👷 {data['workers']}\\n1) Fresh  2) Engine:",reply_markup=mk)''','''        mk=mk_eng(data)
        bot.send_message(m.chat.id,f"🔗 {len(data['dorks'])} dorks | 🧵 {data['threads']} | 📄 {data['pages']} | 👷 {data['workers']}\\n🎯 Engines toggle karo (multiple) + Fresh, phir RUN:",reply_markup=mk)''')
rep('''    elif d.startswith("peng:"):
        with STATES_LOCK: st=states.pop(uid,None)
        if not st or st[0]!="parse_engine": return
        eng=d[5:]; fresh=st[1].get("fresh",""); threads=st[1].get("threads",15)
        pages=st[1].get("pages",1); workers=st[1].get("workers",40)
        engines=ALL_ENGINES if eng=="all" else [eng]
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid,"⏳ STARTING...",reply_markup=stop_markup(jid))
        threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,st[1]["dorks"],engines,fresh,mode,threads,pages,workers)).start()''','''    elif d.startswith("peng_t:"):
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="parse_engine":
            c=d[7:]
            if c=="all": st[1]["engs"]=list(ALL_ENGINES)
            elif c=="none": st[1]["engs"]=[]
            else:
                if c in st[1]["engs"]: st[1]["engs"].remove(c)
                else: st[1]["engs"].append(c)
            try: bot.edit_message_text(f"🎯 {len(st[1]['engs'])} engines selected | Fresh: {st[1].get('fresh','') or 'all'}\\nTap = toggle, phir RUN:",chat_id=cid,message_id=mid,reply_markup=mk_eng(st[1]))
            except: pass
        return
    elif d=="peng_run":
        with STATES_LOCK: st=states.pop(uid,None)
        if not st or st[0]!="parse_engine": return
        engines=st[1].get("engs") or ["ddg","bing"]
        fresh=st[1].get("fresh",""); threads=st[1].get("threads",15)
        pages=st[1].get("pages",1); workers=st[1].get("workers",40)
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid,"⏳ STARTING...",reply_markup=stop_markup(jid))
        threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,st[1]["dorks"],engines,fresh,mode,threads,pages,workers)).start()''')
rep('        proxies=hprox(uid)','        proxies=hprox(uid); rot=sget("rot_proxy","")')
rep('        if len(proxies)<sget("hunt_below",10):\n            threading.Thread(target=turbo_hunt,args=(0,uid,0,0,150),kwargs={"silent":True},daemon=True).start()','        if not rot and len(proxies)<sget("hunt_below",10):\n            threading.Thread(target=turbo_hunt,args=(0,uid,0,0,150),kwargs={"silent":True},daemon=True).start()')
rep('            conn=aiohttp.TCPConnector(limit=wks+10,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)','            conn=aiohttp.TCPConnector(limit=wks+10,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True,force_close=bool(rot))')
rep('            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=5)) as s:','            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=5),proxy=(rot if rot else None)) as s:')
rep('                    px=random.choice(act) if act else None','                    px=(None if rot else (random.choice(act) if act else None))')
rep('        HSEM={}','        HSEM={}; rot=sget("rot_proxy","")')
rep('            conn=aiohttp.TCPConnector(limit=threads+10,limit_per_host=20,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)','            conn=aiohttp.TCPConnector(limit=threads+10,limit_per_host=20,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True,force_close=bool(rot))')
rep('            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=to)) as s:','            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=to),proxy=(rot if rot else None)) as s:')
rep('    elif name=="set_autoint":','''    elif name=="set_trial":
        t=text.strip(); st=S()
        if t.lower() in ("life","lifetime"): st["trial_hours"]=-1
        else:
            try: st["trial_hours"]=max(0,min(87600,int(t)))
            except: bot.send_message(m.chat.id,"❌ number ya 'life'"); return
        setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id,"✅ Trial: "+("LIFETIME" if st["trial_hours"]==-1 else str(st["trial_hours"])+"h (0=off)"))
    elif name=="set_rot":
        t=text.strip(); st=S()
        if t.lower()=="off": st["rot_proxy"]=""
        else: st["rot_proxy"]=t if t.startswith("http") else "http://"+t
        setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id,"✅ RotProxy: "+("ON 🌀 har request naya IP" if st["rot_proxy"] else "OFF"))
    elif name=="set_autoint":''')
if miss:
    print("MISSING MARKERS:",miss); sys.exit(1)
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("MEGA2 DONE - SYNTAX OK:",fn)
except Exception as e:
    print("STILL:",e)
