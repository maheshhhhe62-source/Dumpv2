import sys
fn=sys.argv[1] if len(sys.argv)>1 else "bot.py"
src=open(fn,"r",encoding="utf-8").read()
m=src.find('if __name__=="__main__":')
if m==-1:
    print("NO __main__ FOUND"); sys.exit(1)
head=src[:m].rstrip()+"\n\n"
RESUME='''# ============ RESUME SYSTEM (restart-safe) ============
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
def _resume_auto():
    time.sleep(12)
    d=load_json(AUTO_FILE,{})
    for u,v in d.items():
        try:
            if v.get("done",0)<v.get("limit",0):
                try: bot.send_message(int(u),"🔄 Bot wapas online — AUTO resume!")
                except: pass
                threading.Thread(target=auto_loop,args=(int(u),int(u),v["limit"])).start()
        except: pass
    try: bot.send_message(OWNER_ID,"🌑 SHADOW X back online — resume active.")
    except: pass
'''
if "def _resume_auto():" not in head:
    head+=RESUME+"\n"
TAIL='''if __name__=="__main__":
    print("🌑 SHADOW X — FINAL TAIL starting...")
    if "check_resources" in globals():
        try: check_resources()
        except: pass
    if "job_cleanup_loop" in globals():
        threading.Thread(target=job_cleanup_loop,daemon=True).start()
    threading.Thread(target=sched_loop,daemon=True).start()
    if "_resume_auto" in globals():
        threading.Thread(target=_resume_auto,daemon=True).start()
    while True:
        try: bot.infinity_polling(timeout=30)
        except KeyboardInterrupt: print("🛑 Stopped."); break
        except Exception as e: print("⚠️ Restart:",e); time.sleep(5)
'''
open(fn,"w",encoding="utf-8").write(head+TAIL)
print("REBUILT TAIL:",fn,"- damaged section amputated")
