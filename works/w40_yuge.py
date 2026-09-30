# -*- coding: utf-8 -*-
"""Work 40 -- 「おされた」. Kuro, 技術史. Steam has force.

WRITE-ONCE. See w37_kami.py for the set's shape.

A rattling kettle lid is the smallest honest version of the thing, and Kuro
learns it the only way a co-walker can: she holds the lid down and it pushes
back against her hand. That is a fact she can obtain with her body, which is the
whole test for whether a topic belongs in this series.

The caption anchors Newcomen's 1712 engine rather than Watt, because Watt did
not invent the steam engine -- he added a separate condenser in 1769 and made an
existing machine efficient enough to matter. Kuro does not say any of that; the
strip earns only the sentence she can reach by pressing on a lid, and the date
in the corner is left to do the rest.
"""

from cast import work

WORK = work(
    slug="w40_yuge", title="おされた", byline="4コマ 技術史 · クロ",
    cast="kuro",
    scene="wooden room, iron stove, kettle, daylight from a window, "
          "bright daylight, clear day, indoors",
    panels=[
        dict(k=1, shot="medium shot, upper body, from side, eye level",
             action="standing beside a stove watching a kettle, steam rising "
                    "from its spout",
             expr="open eyes, closed mouth, curious",
             lines=[dict(text="１７１２年\nイングランド", kind="box", anchor="tl"),
                    dict(text="わいてる", kind="speech", anchor="tr")]),
        dict(k=2, shot="close-up, face, from side, eye level",
             action="leaning closer to the kettle, watching its lid",
             expr="open eyes, closed mouth, concentrating",
             lines=[dict(text="ふたが\nうごいてる", kind="speech", anchor="tl")]),
        dict(k=3, shot="close-up, face, from front, eye level",
             action="one hand pressing down on the kettle lid",
             expr="wide eyes, surprised, closed mouth",
             lines=[dict(text="あっ", kind="shout", anchor="tr")]),
        dict(k=4, shot="medium shot, upper body, from front, eye level",
             action="standing close to the viewer looking at her own open "
                    "palm, the kettle still steaming behind her",
             expr="open eyes, closed mouth, dawning realization",
             lines=[dict(text="おされた", kind="speech", anchor="tr"),
                    dict(text="……ゆげって\nちからなんだ", kind="thought", anchor="bl")]),
    ])
