import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "bot.py"
src=open(fn,"r",encoding="utf-8").read()
BAD='''        if not eid:
            bot.send_message(m.chat.id,"❌ Custom emoji nahi ha!"); return
        st=S(); pemd=st.setdefault("pem",{}); pemd[data["name"]]=eid; setS(st)
        states.pop(uid,None)
        bot.send_message(m.chat.id,f"✅ {data['name']} logo saved!")'''
GOOD='''        if not eid:
            bot.send_message(m.chat.id,"❌ Custom emoji nahi ha!"); return
        st=S(); pemd=st.setdefault("pem",{}); pemd[data["name"]]=eid; setS(st)
        states.pop(uid,None)
    bot.send_message(m.chat.id,f"✅ {data['name']} logo saved!")'''
if BAD in src:
    src=src.replace(BAD,GOOD)
    open(fn,"w",encoding="utf-8").write(src)
    try:
        py_compile.compile(fn,doraise=True)
        print("FIXED + SYNTAX OK:",fn)
    except Exception as e:
        print("STILL ERROR:",e)
else:
    print("PATTERN NOT FOUND - file already fixed or different")
