"""Pixel sprites for 앙천이타 — single source of truth.
Writes sprites.json (embedded into the game) and exports .aseprite + .png into ../assets/."""
import json, os
from PIL import Image
from aseprite import write_aseprite

PAL = {
    'k': '#2a1a12', 'h': '#3a2a24', 'f': '#efc49a', 'e': '#1b1418', 'm': '#8b2b2b', 's': '#4c8ae0',
    'p': '#2f3a52', 'w': '#e8f4ff', 'W': '#b8d8f0', 'y': '#f3c34f', 'R': '#d9443a', 'q': '#c9d7b0',
    'g': '#9aa3ad', 'b': '#7a4a22', 'c': '#f1ece0',
}
SPR = {
    # lying on the back, mouth on top of the head (spit leaves from there)
    'lying': ['......kk..................', '....kkffk.................', '..kkfmmffk................',
              '.khhffeffkkkkkkkkkkkkkkk..', 'khhhffffffssssssssppppppk.', 'khhhhffffkssssssssppppppkk',
              '.khhhhhkkssssssssspppppppk', '..kkkkk.kkkkkkkkkkkkkkkkk.'],
    'standing': ['..kkkkk...', '.khhhhhk..', '.khffffk..', '.kfeffek..', '.kffmffk..', '..kffffk..',
                 '.kssssssk.', 'ksssssssk.', 'kfssssssfk', 'kfssssssfk', '.kssssssk.', '.kppppppk.',
                 '.kppkkppk.', '.kpk..kpk.', '.kpk..kpk.', '.kpk..kpk.', 'kkkk..kkkk'],
    'person': ['..kkkk..', '.khhhhk.', '.kfefek.', '.kfmmfk.', '..kffk..', '.kssssk.', 'kfssssfk', 'kfssssfk',
               '.kssssk.', '.kppppk.', '.kpkkpk.', '.kk..kk.'],
    'spit': ['..w..', '.wWw.', 'wWWWw', 'wWWWw', '.www.'],
    'mega': ['......k.', '....kkyk', '..kkyyyk', 'kkyyyyyk', 'kkyyyyyk', '..kkyyyk', '....kkyk', '......k.'],
    'drum': ['.kkkkkk.', 'kccccccK'.replace('K', 'k'), 'kggggggk', 'kRRyyRRk', 'kRRRRRRk', 'kRyRRyRk', 'kRRRRRRk', '.kkkkkk.'],
    'flag': ['kkkkkkk.', 'kyyyyyyk', 'kyyyyyyk', 'kkkkkkk.', 'k.......', 'k.......', 'k.......', 'k.......', 'k.......', 'k.......'],
    'mop': ['..k..', '..b..', '..b..', '..b..', '..b..', '..b..', '..b..', 'kkkkk', 'ccccc', 'c.c.c'],
}
# audience types = palette swaps of one person
KINDS = {
    'base':     {},
    'roommate': {'s': '#7fb069'},
    'office':   {'s': '#f1ece0', 'p': '#2a2a30'},             # tie drawn in code
    'hoodie':   {'s': '#5a5a6a', 'h': '#5a5a6a'},             # 키보드 워리어
    'reporter': {'s': '#c9a26a'},                              # camera drawn in code
    'fan':      {'s': '#e5484d'},
    'supporter': {'s': '#f3c34f'},                             # plain flag drawn in code
    'bot':      {'f': '#9aa3ad', 's': '#4c8ae0', 'h': '#6b6b75'},
    'ai':       {'f': '#c9d7e8', 'h': '#6b6b75', 's': '#6a4aa0', 'p': '#3a3460'},  # visor and antenna drawn in code
}
SPIT = ['#dff0ff', '#cfd6dc', '#e5484d', '#f3c34f', '#f08a4a', '#4c8ae0', '#b07cff']   # per venue

def img(name, swap=None):
    rows = SPR[name]; im = Image.new('RGBA', (len(rows[0]), len(rows)))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '.': continue
            h = (swap or {}).get(ch) or PAL[ch]
            im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im

if __name__ == '__main__':
    for n, rows in SPR.items(): assert len(set(map(len, rows))) == 1, (n, [len(r) for r in rows])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump({'pal': PAL, 'spr': SPR, 'kinds': KINDS, 'spit': SPIT}, open(os.path.join(here, 'sprites.json'), 'w'), ensure_ascii=False)
    out = os.path.join(here, '..', 'assets'); os.makedirs(out + '/aseprite', exist_ok=True); os.makedirs(out + '/png', exist_ok=True)
    pal = [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for h in PAL.values()]
    for n in SPR:
        if n in ('person', 'spit'): continue
        im = img(n); write_aseprite(f'{out}/aseprite/{n}.aseprite', [im], palette=pal)
        im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(f'{out}/png/{n}_x4.png')
    frames = [img('person', sw) for sw in KINDS.values()]
    write_aseprite(f'{out}/aseprite/audience.aseprite', frames, [200] * len(frames), [(k, i, i) for i, k in enumerate(KINDS)], pal)
    sheet = Image.new('RGBA', (8 * len(frames), 12)); [sheet.paste(f, (8 * i, 0)) for i, f in enumerate(frames)]
    sheet.resize((sheet.width * 4, 48), Image.NEAREST).save(f'{out}/png/audience_sheet_x4.png')
    spits = [img('spit', {'w': c, 'W': c}) for c in SPIT]
    write_aseprite(f'{out}/aseprite/spit.aseprite', spits, [150] * 7, [('venues', 0, 6)], pal)
    f1 = Image.new('RGBA', (26, 17)); f1.paste(img('lying'), (0, 9)); f2 = Image.new('RGBA', (26, 17)); f2.paste(img('standing'), (8, 0))
    write_aseprite(f'{out}/aseprite/stand_up.aseprite', [f1, f2], [600, 600], [('standup', 0, 1)], pal)
    print('sprites ok')
