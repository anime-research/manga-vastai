# -*- coding: utf-8 -*-
"""Work 37 -- 「かみ」. Kuro, 技術史. Paper made from rags and bark.

WRITE-ONCE. See w1_kotatsu.py.

First of the 技術史 set, and a different genre from everything before it: the
reader is meant to come away knowing something. 技術史 and 世界史 are two
subjects, not one theme with two flavours, so they are two sets with their own
sweep configs -- this one asks how a thing works, w41-w44 ask how things moved
between peoples. The shape follows the review's
instruction that Kuro is a co-walker rather than a 解説役 -- she does not explain
anything to anyone. She meets one tangible object, handles it, and works it out,
and the reader works it out beside her.

That constraint is also what keeps the genre inside what the model draws well.
An explainer strip would need historical settings and machinery, which m1-m9
established it renders badly and inconsistently; a girl holding a sheet of paper
up to the light is the same ordinary, hand-scale pose that every high-graded
work in this project is built on. The history lives in the lettering, which is
deterministic, and in one caption box carrying the anchor the character has no
reason to say aloud.

The history: paper predates 蔡倫 -- fragments survive from the 前漢 -- and what
the 105 CE account credits him with is a *recipe*, bark and hemp rags and old
fishing nets, that made it cheap. That is the beat Kuro arrives at: not that
paper was invented, but that it stopped being precious.
"""

from cast import work

WORK = work(
    slug="w37_kami", title="かみ", byline="4コマ 技術史 · クロ",
    cast="kuro",
    scene="wooden room, workbench, daylight from a window, bright daylight, "
          "clear day, indoors",
    panels=[
        dict(k=1, shot="medium shot, upper body, from front, eye level",
             action="holding a single sheet of paper up toward the window "
                    "with both hands, looking at it",
             expr="open eyes, closed mouth, curious",
             lines=[dict(text="１０５年ごろ\n後漢", kind="box", anchor="tl"),
                    dict(text="うすい", kind="speech", anchor="tr")]),
        dict(k=2, shot="close-up, face, from front, eye level",
             action="holding the sheet of paper close to her face, "
                    "examining it",
             expr="open eyes, closed mouth, concentrating",
             lines=[dict(text="……せんいだ", kind="speech", anchor="tr")]),
        dict(k=3, shot="medium shot, upper body, from front, eye level",
             action="holding a bundle of old cloth rags in one hand and the "
                    "sheet of paper in the other, comparing them",
             expr="wide eyes, closed mouth, surprised",
             lines=[dict(text="これが\nこれに？", kind="shout", anchor="tl")]),
        dict(k=4, shot="medium shot, upper body, from front, eye level",
             action="sitting close to the viewer beside a tall stack of paper, "
                    "one hand resting on it",
             expr="closed eyes, content, light smile",
             lines=[dict(text="ぼろきれで\nつくれるなら", kind="speech", anchor="tr"),
                    dict(text="……いくらでも\nかける", kind="thought", anchor="bl")]),
    ])
