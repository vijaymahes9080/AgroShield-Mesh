import subprocess
import os
import shutil

cwd = r"d:\current project\zz"
dist_temp = r"C:\Users\vijay\.gemini\antigravity-ide\brain\e2f968eb-e56d-46fa-b1c1-8d468cd2e3a0\gh_dist"

def run(cmd):
    print("RUN:", cmd)
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print("ERR:", res.stderr.strip())
    return res.returncode

# 1. Checkout orphan branch
run("git checkout --orphan gh-pages")

# 2. Clear stage
run("git rm -rf .")

# 3. Copy dist contents into root
for item in os.listdir(dist_temp):
    s = os.path.join(dist_temp, item)
    d = os.path.join(cwd, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copyfile(s, d)

# 4. Create .nojekyll
with open(os.path.join(cwd, ".nojekyll"), "w") as f:
    f.write("")

# 5. Add, commit, push
run("git add -A")
run('git commit -m "deploy: publish frontend production distribution to GitHub Pages"')
run("git push -u origin gh-pages --force")

# 6. Return to main
run("git checkout main")
print("Returned to main branch successfully!")
