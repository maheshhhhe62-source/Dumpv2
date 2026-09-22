import sys, os
cands=[sys.argv[1]] if len(sys.argv)>1 else ["bot.py","new.py","test.py"]
fn=None
for c in cands:
    if os.path.exists(c): fn=c; break
if not fn:
    print("NO MAIN FILE"); sys.exit(1)
src=open(fn,"r",encoding="utf-8").read()
if "# RESUME-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
line=None
for L in ("states={}; JOBS={}; LAST={}; AUTO={}; AUTO_LOCK=threading.Lock(); RATE_LIMITS={}",
          "states={}; JOBS={}; LAST={}; AUTO={}; AUTO_LOCK=threading.Lock()"):
    if L in src: line=L; break
m2='def auto_loop(uid,cid,limit):\n    AUTO[uid]={"stop":False,"done":0,"limit":min(limit,100)}'
m3="threading.Thread(target=sched_loop,daemon=True).start()"
if not line or m2 not in src or m3 not in src:
    print("MARKERS NOT FOUND in",fn); sys.exit(1)
INS1='''# ============ 💾 RESUME SYSTEM (restart-safe) ============
# RESUME-v1
LAST_FILE=P("last_cache.json"); AUTO_FILE=P("auto_persist.json")
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
src=src.replace(line,line+"\n"+INS1,1)
src=src.replace(m2,'def auto_loop(uid,cid,limit,start_done=0):\n    AUTO[uid]={"stop":False,"done":int(start_done),"limit":min(limit,100)}',1)
INS3='''threading.Thread(target=sched_loop,daemon=True).start()
def _resume_auto():
    time.sleep(12)
    d=load_json(AUTO_FILE,{})
    for u,v in d.items():
        try:
            if v.get("done",0)<v.get("limit",0):
                try: bot.send_message(int(u),"🔄 Bot wapas online — AUTO pilot resume ho gaya!")
                except: pass
                threading.Thread(target=auto_loop,args=(int(u),int(u),v["limit"],v["done"])).start()
        except: pass
    try: bot.send_message(OWNER_ID,"🌑 SHADOW X back online — resume system active.")
    except: pass
threading.Thread(target=_resume_auto,daemon=True).start()
'''
src=src.replace(m3,INS3,1)
open(fn,"w",encoding="utf-8").write(src)
print("PATCHED",fn,"- resume system welded")
