"""
One-time patch: add canvas-based compression to swapPhoto() on every page that's
still missing it (the wellness-*.html pages and coaches.html already have this;
this brings the remaining 32 gym-site pages up to the same standard).

Finds the swapPhoto function by brace-balance (not a fixed line range, since the
function body differs slightly page to page), then:
  1. Replaces `var dataUrl = ev.target.result;` with a canvas resize+compress step
     (max 1200px long edge, JPEG quality 0.78 — same target as coaches.html)
  2. Closes the new raw.onload wrapper and adds `raw.src = ev.target.result;`
     right before the existing `reader.readAsDataURL(file);` trigger

Leaves everything else in the function (whatever varies per page — banner-show
lines, single- vs multi-line `if(img)`, etc.) completely untouched.
"""
import re
import sys

FILES = """amanda.html athletes.html blog-TEMPLATE.html blog-amanda-kobus-coach-ballito.html
blog-ballito-community-raises-funds-st-lukes.html blog-bjj-beginners-ballito.html
blog-cold-plunge-sauna-ballito.html blog-efc-134-amanda-lino-title-defence.html
blog-efc-134-amanda-lino-vs-juliet-chukwu.html blog-genesis-athlete-recovery-ballito.html
blog-iv-drip-therapy-ballito.html blog-mma-training-ballito.html
blog-powerlifting-women-ballito.html blog-robin-jj-williams-physio-ballito.html
blog-womens-self-defence-workshop-ballito.html blog-youth-mma-training-ballito.html
contact.html events.html index.html recovery.html
training-bjj-ballito.html training-bootcamp-ballito.html training-boxing-ballito.html
training-kickboxing-ballito.html training-kids-bjj-ballito.html training-kids-boxing-ballito.html
training-mma-ballito.html training-olympic-boxing-ballito.html training-personal-training-ballito.html
training-powerlifting-ballito.html training-womens-boxing-ballito.html training.html""".split()

DATAURL_RE = re.compile(r'[ \t]*var dataUrl\s*=\s*ev\.target\.result;\r?\n')

COMPRESS_PREAMBLE = (
    "      /* Compress via canvas before embedding — target ≤200KB at quality 0.78 */\n"
    "      var raw = new Image();\n"
    "      raw.onload = function() {\n"
    "        var MAX = 1200;\n"
    "        var w = raw.width, h = raw.height;\n"
    "        if (w > MAX) { h = Math.round(h * MAX / w); w = MAX; }\n"
    "        var canvas = document.createElement('canvas');\n"
    "        canvas.width = w; canvas.height = h;\n"
    "        canvas.getContext('2d').drawImage(raw, 0, 0, w, h);\n"
    "        var dataUrl = canvas.toDataURL('image/jpeg', 0.78);\n"
)

CLOSE_RE = re.compile(r'([ \t]*)\};\r?\n([ \t]*)reader\.readAsDataURL\(file\);')

def find_function_span(text, start_idx):
    brace_open = text.index('{', start_idx)
    depth = 0
    i = brace_open
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return start_idx, i + 1
        i += 1
    raise ValueError("unbalanced braces")

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'function swapPhoto\(slotId\)\s*\{', text)
    if not m:
        return 'NO_SWAPPHOTO'

    start, end = find_function_span(text, m.start())
    func = text[start:end]

    if 'canvas' in func:
        return 'ALREADY_HAS_COMPRESSION'

    if not DATAURL_RE.search(func):
        return 'PATTERN_NOT_FOUND (dataUrl line)'
    if not CLOSE_RE.search(func):
        return 'PATTERN_NOT_FOUND (close line)'

    new_func = DATAURL_RE.sub(COMPRESS_PREAMBLE, func, count=1)

    def close_repl(cm):
        indent_outer = cm.group(1)
        indent_inner = cm.group(2)
        return (f"{indent_outer}  }};\n"
                f"{indent_outer}  raw.src = ev.target.result;\n"
                f"{indent_outer}}};\n"
                f"{indent_inner}reader.readAsDataURL(file);")

    new_func = CLOSE_RE.sub(close_repl, new_func, count=1)

    new_text = text[:start] + new_func + text[end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    return 'PATCHED'

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    for fname in FILES:
        try:
            if dry_run:
                with open(fname, 'r', encoding='utf-8') as f:
                    text = f.read()
                m = re.search(r'function swapPhoto\(slotId\)\s*\{', text)
                if not m:
                    print(f'{fname}: NO_SWAPPHOTO')
                    continue
                start, end = find_function_span(text, m.start())
                func = text[start:end]
                has_dataurl = bool(DATAURL_RE.search(func))
                has_close = bool(CLOSE_RE.search(func))
                print(f'{fname}: dataUrl_line={has_dataurl} close_line={has_close} already_compressed={"canvas" in func}')
            else:
                result = patch_file(fname)
                print(f'{fname}: {result}')
        except Exception as e:
            print(f'{fname}: ERROR {e}')
