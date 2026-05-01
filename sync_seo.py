import shutil, os

SRC = r'C:\Users\HP\Desktop\Maddog Web design pages\.claude\worktrees\priceless-bardeen-61b48b'
DST = r'C:\Users\HP\Desktop\Maddog Web design pages'

files = [
    'blog-cold-plunge-sauna-ballito.html',
    'blog-bjj-beginners-ballito.html',
    'blog-powerlifting-women-ballito.html',
    'blog-iv-drip-therapy-ballito.html',
    'blog-mma-training-ballito.html',
    'blog-efc-134-amanda-lino-vs-juliet-chukwu.html',
    'blog-ballito-community-raises-funds-st-lukes.html',
    'sitemap.xml',
    'robots.txt',
]

for f in files:
    src = os.path.join(SRC, f)
    dst = os.path.join(DST, f)
    shutil.copy2(src, dst)
    print(f'Synced: {f}')

print('Done.')
