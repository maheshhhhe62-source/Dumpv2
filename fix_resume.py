import sys
fn=sys.argv[1] if len(sys.argv)>1 else "bot.py"
src=open(fn,"r",encoding="utf-8").read()
BAD="threading.Thread(target=sched_loop,daemon=True).start()\ndef _resume_auto():"
if BAD not in src:
    print("NO BROKEN BLOCK - file theek ha"); sys.exit(0)
s=src.index("def _resume_auto():")
e=src.index("threading.Thread(target=_resume_auto,daemon=True).start()")
e+=len("threading.Thread(target=_resume_auto,daemon=True).start()")
block=src[s:e]
src=src[:s]+src[e:]
m=src.index('if __name__=="__main__":')
src=src[:m]+block+"\n\n"+src[m:]
open(fn,"w",encoding="utf-8").write(src)
print("FIXED",fn,"- resume block moved to module level")
