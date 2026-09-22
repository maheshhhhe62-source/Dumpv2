import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
if "# FILE-TTL-v1" in src:
    print("ALREADY PATCHED:",fn); sys.exit(0)
miss=[]
def rep(old,new):
    global src
    if old in src: src=src.replace(old,new,1)
    else: miss.append(old[:50])
H=r'''# ============ 🗑️ FILE AUTO-CLEANUP (TTL) ============
# FILE-TTL-v1
def _file_cleanup_loop():
    while True:
        time.sleep(600)
        try:
            ttl=int(sget("file_ttl_hours",24))
            if ttl<=0: continue
            now=int(time.time()); cutoff=now-ttl*3600
            if not os.path.exists(FILES_DIR): continue
            for ud in os.listdir(FILES_DIR):
                udir=os.path.join(FILES_DIR,ud)
                ip=os.path.join(udir,"index.json")
                if not os.path.isdir(udir) or not os.path.exists(ip): continue
                idx=load_json(ip,[]); keep=[]; changed=False
                for e in idx:
                    if e.get("t",now)<cutoff:
                        changed=True
                        try: os.remove(os.path.join(udir,e["f"]))
                        except: pass
                    else: keep.append(e)
                if changed: save_json(ip,keep)
        except: pass
threading.Thread(target=_file_cleanup_loop,daemon=True).start()
'''
rep("def turbo_parse(",H+"def turbo_parse(")
rep('    mk.row(btn("🌀 RotProxy "+("ON" if sget("rot_proxy") else "OFF"),"adm:rot"),btn("⬅️ Back","back"))','    mk.row(btn("🌀 RotProxy "+("ON" if sget("rot_proxy") else "OFF"),"adm:rot"),btn(f"🗑️ TTL: {sget(\'file_ttl_hours\',24)}h","adm:ttl"))\n    mk.row(btn("⬅️ Back","back"))')
rep('    if d=="autostop":','''    if d=="adm:ttl":
        with STATES_LOCK: states[uid]=("set_ttl",{})
        bot.send_message(cid,f"🗑️ FILE AUTO-DELETE\\n{LINE}\\nHours likho (1-8760)\\n0 = off (kabhi delete nahi)\\nCurrent: {sget('file_ttl_hours',24)}h"); return
    if d=="autostop":''')
rep('    elif name=="set_autoint":','''    elif name=="set_ttl":
        try:
            val=max(0,min(8760,int(text.strip())))
            st=S(); st["file_ttl_hours"]=val; setS(st)
            with STATES_LOCK: states.pop(uid,None)
            bot.send_message(m.chat.id,"✅ File TTL: "+("OFF" if val==0 else str(val)+"h"))
        except: bot.send_message(m.chat.id,"❌ number likho")
    elif name=="set_autoint":''')
if miss:
    print("MISSING MARKERS:",miss); sys.exit(1)
open(fn,"w",encoding="utf-8").write(src)
try:
    py_compile.compile(fn,doraise=True)
    print("TTL PATCH DONE - SYNTAX OK:",fn)
except Exception as e:
    print("STILL:",e)
