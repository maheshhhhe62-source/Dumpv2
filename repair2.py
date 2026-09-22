import sys, py_compile
fn=sys.argv[1] if len(sys.argv)>1 else "new.py"
src=open(fn,"r",encoding="utf-8").read()
bad='def clean_href\ndef clean_href('
if bad in src:
    src=src.replace(bad,'def clean_href(',1)
    open(fn,"w",encoding="utf-8").write(src)
    print("REPAIRED duplicate def")
else:
    print("NO DUPLICATE - already clean")
try:
    py_compile.compile(fn,doraise=True)
    print("SYNTAX OK:",fn)
except Exception as e:
    print("STILL ERROR:",e)
