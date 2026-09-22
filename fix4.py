import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
PENG=r'''elif d.startswith("peng:"):
        with STATES_LOCK: st=states.pop(uid,None)
        if not st or st[0]!="parse_engine": return
        eng=d[5:]; fresh=st[1].get("fresh",""); threads=st[1].get("threads",15)
        pages=st[1].get("pages",1); workers=st[1].get("workers",40)
        engines=ALL_ENGINES if eng=="all" else [eng]
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid,"⏳ STARTING...",reply_markup=stop_markup(jid))
        threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,st[1]["dorks"],engines,fresh,mode,threads,pages,workers)).start()
    '''
PAR=r'''elif name=="parse_threads":
        try: th=int(text.strip())
        except: th=0
        if not (1<=th<=30):
            bot.send_message(m.chat.id,"❌ 1 to 30 only!"); return
        with STATES_LOCK:
            data["threads"]=th; states[uid]=("parse_pages",data)
        set_cur(uid,"parse_pages")
        bot.send_message(m.chat.id,"📄 Pages (1-5):",reply_markup=back_row(types.InlineKeyboardMarkup()))
    elif name=="parse_pages":
        try: pg=int(text.strip())
        except: pg=0
        if not (1<=pg<=5):
            bot.send_message(m.chat.id,"❌ 1-5!"); return
        with STATES_LOCK:
            data["pages"]=pg; states[uid]=("parse_workers",data)
        set_cur(uid,"parse_workers")
        bot.send_message(m.chat.id,"👷 Workers (1-100):",reply_markup=back_row(types.InlineKeyboardMarkup()))
    elif name=="parse_workers":
        try: wk=int(text.strip())
        except: wk=0
        if not (1<=wk<=100):
            bot.send_message(m.chat.id,"❌ 1-100!"); return
        with STATES_LOCK:
            data["workers"]=wk; states[uid]=("parse_engine",data)
        set_cur(uid,"parse_eng")
        mk=types.InlineKeyboardMarkup()
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
        bot.send_message(m.chat.id,f"🔗 {len(data['dorks'])} dorks | 🧵 {data['threads']} | 📄 {data['pages']} | 👷 {data['workers']}\n1) Fresh  2) Engine:",reply_markup=mk)
    '''
ia=src.index('elif d.startswith("peng:")'); ib=src.index('elif d=="menu:inject":')
src=src[:ia]+PENG+src[ib:]
ia=src.index('elif name=="parse_threads":'); ib=src.index('elif name=="dump_urls":')
src=src[:ia]+PAR+src[ib:]
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("FINAL FIX DONE - SYNTAX 100% OK:",fn)
except Exception as e:
    print("STILL:",e)
