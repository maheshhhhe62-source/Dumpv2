import sys, os, json
cands=[sys.argv[1]] if len(sys.argv)>1 else ["new.py","test.py","bot.py"]
fn=None
for c in cands:
    if os.path.exists(c): fn=c; break
if not fn:
    print("NO MAIN FILE FOUND"); sys.exit(1)
src=open(fn,"r",encoding="utf-8").read()
if "def send_doc(" not in src or "def html_report(" not in src:
    print("MARKERS NOT FOUND in",fn); sys.exit(1)
a=src.index("def send_doc(")
b=src.index("def html_report(")
if "# GH-VAULT-v1" in src[a:b]:
    print("ALREADY PATCHED:",fn)
else:
    NEW=r'''# ============ 🌐 GH VAULT (BIG FILES → WEBSITE) ============
GH_CFG=P("gh_config.json")
def gh_conf(): return load_json(GH_CFG,{})
def gh_upload(uid,data,name):
    # GH-VAULT-v1
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
    # GH-VAULT-v1
    minb=int(gh_conf().get("min_kb",500) or 0)*1024
    if uid and minb and len(data)>=minb:
        link=gh_upload(uid,data,name)
        if link:
            try: bot.send_message(cid,f"📦 {name} | {len(data)//1024} KB\n🌐 Site pe upload ho gaya!\n🔗 {link}\n♻️ Purani file hat gayi — sirf nayi wali hai.")
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
'''
    open(fn,"w",encoding="utf-8").write(src[:a]+NEW+src[b:])
    print("PATCHED",fn)
if not os.path.exists("gh_config.json"):
    open("gh_config.json","w").write(json.dumps({"token":"","repo":"","min_kb":500,"site":""},indent=1))
    print("CREATED gh_config.json — fill token+repo (see below)")
print("""
================ SETUP (one time) ================
1. github.com → New repository → name: shadow-vault → PUBLIC → Create
2. Repo me "Add file → Upload files" → index.html upload karo
3. Settings → Pages → Source: Deploy from branch → main → Save (1 min wait)
4. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   → Generate new token → scope: [x] repo → copy token
5. Termux me gh_config.json kholo:
   nano gh_config.json
   "token": "apna_token_yahan"
   "repo": "apna_username/shadow-vault"
   "min_kb": 500        (is size se badi file site pe jayegi)
   "site": ""           (optional: netlify link yahan daalo agar site wahan host ki)
6. python new.py   (jo file patch hui ho)
==================================================
Flow: user 50k/100k generate karega → bot site pe upload → user ko LINK
→ user ka purana result auto-delete, sirf naya dikhega. Har user ka apna slot.
""")
