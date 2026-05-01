import shutil, os

SRC = r'C:\Users\HP\Desktop\Maddog Web design pages\.claude\worktrees\priceless-bardeen-61b48b'
DST = r'C:\Users\HP\Desktop\Maddog Web design pages'

files = ['index.html', 'recovery.html', 'pricing.html']

for f in files:
    shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
    print(f'Synced: {f}')
