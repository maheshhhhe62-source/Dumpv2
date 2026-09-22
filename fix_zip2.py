import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
BAD='+\x22\n\x22.join('
GOOD='+ "\\n".join('
n=src.count(BAD)
src=src.replace(BAD,GOOD)
BAD2='(\x22\n\x22.join('
GOOD2='("\\n".join('
n+=src.count(BAD2)
src=src.replace(BAD2,GOOD2)
open(fn,"w",encoding="utf-8").write(src)
print("REPAIRED SPOTS:",n)
try:
    py_compile.compile(fn,doraise=True)
    print("SYNTAX OK:",fn)
except Exception as e:
    print("STILL ERROR:",e)
