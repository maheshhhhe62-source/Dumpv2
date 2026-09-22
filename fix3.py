import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
M3=r'''LANG_MODS={"en":["buy","cheap","best","top","review","discount","online","price","shop","sale"],"hi":["खरीदें","सस्ता","best","कीमत","ऑनलाइन","दाम","रीव्यू","खरीद"],"zh":["购买","便宜","最好","价格","在线","评论","促销","商城"],"es":["comprar","barato","mejor","precio","online","oferta","reseñas","tienda"],"ar":["شراء","رخيص","أفضل","سعر","اونلاين","خصم","مراجعة","متجر"],"fr":["acheter","pas cher","meilleur","prix","en ligne","promo","avis","boutique"],"pt":["comprar","barato","melhor","preço","online","oferta","avaliações","loja"],"ru":["купить","дешево","лучший","цена","онлайн","скидка","отзывы","магазин"],"id":["beli","murah","terbaik","harga","online","diskon","ulasan","toko"],"de":["kaufen","billig","beste","preis","online","rabatt","bewertung","shop"],"ja":["購入","安い","最高","価格","オンライン","割引","レビュー","ショップ"],"tr":["satın al","ucuz","en iyi","fiyat","online","indirim","yorum","mağaza"],"ko":["구매","저렴","최고","가격","온라인","할인","리뷰","쇼핑"],"it":["compra","economico","migliore","prezzo","online","sconto","recensioni","negozio"],"nl":["kopen","goedkoop","beste","prijs","online","korting","winkel","review"],"pl":["kup","tani","najlepszy","cena","online","promocja","opinie","sklep"],"vi":["mua","rẻ","tốt nhất","giá","online","giảm giá","đánh giá","cửa hàng"],"th":["ซื้อ","ถูก","ดีที่สุด","ราคา","ออนไลน์","ส่วนลด","รีวิว","ร้าน"],"bn":["কিনুন","সস্তা","সেরা","দাম","অনলাইন","ছাড়","রিভিউ","দোকান"],"fa":["خرید","ارزان","بهترین","قیمت","آنلاین","تخفیف","بررسی","فروشگاه"]}
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
'''
if "def km_lang_mk(" not in src:
    src=src.replace("# ============ CAPTCHA SOLVER",M3+"# ============ CAPTCHA SOLVER",1)
CB=r'''elif d=="km:gap":
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
                states[uid]=("km_count",{"kws":st[1]["kws"],"langs":st[1]["langs"]})
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
                states[uid]=("km_amount",{"kws":kws,"langs":langs})
                bot.send_message(cid,"✏️ Kitne? (1-10000):"); return
            states.pop(uid,None)
            threading.Thread(target=run_km,args=(cid,uid,kws,int(d[4:]),langs)).start()
    '''
MI=r'''elif name=="km_kw":
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
    '''
st_cb='elif d=="km:gap":' if 'elif d=="km:gap":' in src else 'elif d=="menu:km":'
ia=src.index(st_cb); ib=src.index('elif d=="menu:gen":')
src=src[:ia]+CB+src[ib:]
ia=src.index('elif name=="km_kw":'); ib=src.index('elif name=="gen_kw":')
src=src[:ia]+MI+src[ib:]
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("FIX3 DONE + SYNTAX OK:",fn)
except Exception as e:
    print("STILL ERROR:",e)
