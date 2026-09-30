# -*- coding: utf-8 -*-
"""Work 39 -- 「みずのみち」. Kuro, 技術史. A Roman aqueduct runs on gravity.

WRITE-ONCE. See w37_kami.py for the set's shape. Roman, but the subject is the
mechanism -- a slope -- so it belongs with 技術史 and not with 世界史.

What Kuro discovers by walking beside the channel is that nothing is pushing the
water. No pump, no wheel, no animal: the whole system is a slope held to within
a fraction of a degree over tens of kilometres, and the water simply falls the
entire way. The Aqua Appia of 312 BCE was mostly underground, which is the part
people miss -- the arches everyone pictures are the exception, used to carry the
line across a dip and keep the fall constant.

She reaches it by following the water, which is a walk rather than a lecture,
and by putting her hand in it, which is hand-scale. The caption carries the date
and nothing else.
"""

from cast import work

WORK = work(
    slug="w39_mizunomichi", title="みずのみち", byline="4コマ 技術史 · クロ",
    cast="kuro",
    scene="stone water channel, narrow aqueduct, open countryside, "
          "bright daylight, clear day, outdoors",
    panels=[
        dict(k=1, shot="medium shot, upper body, from side, eye level",
             action="standing beside a narrow stone channel with water "
                    "running along it, looking down at the water",
             expr="open eyes, closed mouth, curious",
             lines=[dict(text="前３１２年\nアッピア水道", kind="box", anchor="tl"),
                    dict(text="ながれてる", kind="speech", anchor="tr")]),
        dict(k=2, shot="medium shot, full body, from side, eye level",
             action="walking along beside the stone channel, following the "
                    "water with her eyes",
             expr="open eyes, closed mouth, concentrating",
             lines=[dict(text="どこまで\nつづくの", kind="speech", anchor="tl")]),
        dict(k=3, shot="close-up, face, from front, eye level",
             action="crouching, one hand held in the running water",
             expr="closed eyes, calm, light smile",
             lines=[dict(text="つめたい", kind="speech", anchor="tr")]),
        dict(k=4, shot="medium shot, upper body, from side, eye level",
             action="standing close to the viewer looking back along the "
                    "stone channel toward the hills",
             expr="open eyes, closed mouth, dawning realization",
             lines=[dict(text="だれも\nおしてない", kind="speech", anchor="tr"),
                    dict(text="……ずっと\nくだってるんだ", kind="thought", anchor="bl")]),
    ])
