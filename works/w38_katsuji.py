# -*- coding: utf-8 -*-
"""Work 38 -- 「ならべかえる」. Kuro, 技術史. Movable type.

WRITE-ONCE. See w37_kami.py for the set's shape.

The insight Kuro reaches is the one that actually matters and is not the one
people usually name. Printing from a carved block was old; what movable type
changes is that the pieces come apart and go back in a different order, so one
set of type prints anything. She gets there by holding a single piece and then
a handful, which is a hand-scale encounter rather than an explanation.

Deliberately not in the strip: that Gutenberg was not first. 畢昇 had clay type
around 1040 and the Korean 直指 was printed with metal type in 1377, seventy
years earlier -- but "who was first" is a fact to be told, while "these come
apart" is something a co-walker can discover in her hands. The caption carries
the anchor and nothing argues with it.
"""

from cast import work

WORK = work(
    slug="w38_katsuji", title="ならべかえる", byline="4コマ 技術史 · クロ",
    cast="kuro",
    scene="wooden room, workbench, daylight from a window, bright daylight, "
          "clear day, indoors",
    panels=[
        dict(k=1, shot="medium shot, upper body, from front, eye level",
             action="holding one small metal block between finger and thumb, "
                    "looking at it closely",
             expr="open eyes, closed mouth, curious",
             lines=[dict(text="１４５０年ごろ\nマインツ", kind="box", anchor="tl"),
                    dict(text="ちいさい", kind="speech", anchor="tr")]),
        dict(k=2, shot="close-up, face, from front, eye level",
             action="pressing the small metal block down onto a sheet of paper "
                    "on the bench",
             expr="closed eyes, concentrating, closed mouth",
             lines=[dict(text="ぎゅっ", kind="speech", anchor="tr")]),
        dict(k=3, shot="close-up, face, from front, eye level",
             action="looking down at the single mark printed on the paper",
             expr="wide eyes, closed mouth, surprised",
             lines=[dict(text="ついた", kind="shout", anchor="tl")]),
        dict(k=4, shot="medium shot, upper body, from front, eye level",
             action="sitting close to the viewer holding a handful of small "
                    "metal blocks in both cupped hands",
             expr="open eyes, closed mouth, dawning realization",
             lines=[dict(text="ばらばらになる\nってことは", kind="speech", anchor="tr"),
                    dict(text="……なんども\nならべかえられる", kind="thought", anchor="bl")]),
    ])
