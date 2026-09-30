# manga-vastai

English · [简体中文](README-zh.md) · [繁體中文](README-zh-tw.md)

Yonkoma (4-panel manga) generated on a rented Vast.ai GPU: the panels (koma) are
drawn by [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) on
WAI-illustrious-SDXL v13.0, and everything that is not drawing (frames, gutters,
speech balloons, dialogue) is computed in Python.

That split is the whole design, and it comes straight from the source
discussion: *"The panels and such, you don't have the model do those; you can
place them programmatically."* A diffusion model cannot spell Japanese and cannot
rule a straight border, but it is the only thing that can draw the picture. So it
draws the picture and nothing else, and the sweep negates `speech bubble, text,
border, comic panel` to keep it out of the parts it would only do badly.

The same discussion's other half is why the balloons are still *measured* rather
than hardcoded: *"If you only place them, the frame can end up floating a bit,
the contrast can end up standing out, so do the colour calculation around
that."* Placement and colour are sampled off each rendered koma. See "What is
measured" below.

## What comes out

The latest run, `m10_gijutsushi`, produced four works. They are a history of
technology set: Kuro picks up one tool and reasons her way to how it works. The
model drew the pictures; the frames, balloons and text are Python.

- `w37_kami`, "Paper": paper, 105 CE, Eastern Han
- `w38_katsuji`, "Rearranging": movable type, c. 1450, Mainz
- `w39_mizunomichi`, "The Water's Way": the Appian aqueduct, 312 BCE
- `w40_yuge`, "Pushed": steam, 1712, England

Each work was run at seven seeds, and one strip per work was chosen. The
candidate sheets show what that one strip was chosen out of: a row is a koma,
the columns are the seeds, 28 frames in all, raw (before lettering) and lettered
side by side, with the chosen anchor and its busyness score under each frame.

The generated images are not published in this repository (see "About this
repository").

## About this repository

This repository is a personal project of mine (manga-vastai), begun in June
2026, partially revised and reorganised into a publishable form, with the aim of
releasing a reproducible subset of it for the public benefit.

What is here now: the four work files of the history of technology set under
`works/`. The rest of the pipeline described below (the runner, the lettering and
page scripts, the shared cast file the works import) is being cleaned up and
will be added in stages, so the work files do not run on their own yet.

### License

Everything in this repository is licensed under the [MIT License](LICENSE).

### Disclaimer

The strips touch real history, and they compress it hard to fit four panels.
They follow the conventional popular account and are meant to send you looking
something up, so please do not cite them. `w37_kami` is the clearest case: it
dates itself to the 105 CE account of Cai Lun, but paper fragments survive from
the Western Han, and what that account credits him with is a cheap recipe of
bark, hemp rags and old fishing net rather than the invention itself. The work
file's own docstring says so. Rooms, tools and clothing are invented by the model
and reconstruct no particular place or period.

The characters are fictional and correspond to no living person.

Model weights are not redistributed here and the license above does not reach
them. WAI-illustrious-SDXL and the Illustrious/SDXL lineage beneath it carry
their own terms, which you should read before reusing the prompts to generate
anything of your own.

The code comes with no warranty of any kind. `run_full.sh` rents a GPU from a
third party and spends real money, so the API key, the bill and the teardown are
yours to watch: an instance that fails to stop keeps billing, which is what
`state/.vast_stranded_ids` exists to catch. This project has no affiliation with
Vast.ai, Hugging Face, leejet/stable-diffusion.cpp, or the authors of the model.

## Status

The first run was m1_smoke: two works, 40 images, generated, lettered and
assembled into 8 strips. Its purpose was to find out what a review UI would need
to show before writing one, so the browser review app is deliberately not built yet.

| | w1_kotatsu | w2_ice |
|---|---|---|
| title | "The Tail and the Kotatsu" | "Before It Melts" |
| character | white fox / long hair / knit (`a_fox_white`) | black cat / short hair / shirt (`c_cat_black`) |
| setting | winter, tatami, kotatsu, warm lamp | summer, wooden floor, fan, daylight |
| gag | a tail that will not fit under the kotatsu | a popsicle that melts faster than she eats it |
| hard part | one face across four shot distances | an object that changes state across four koma |

Runs m2 to m10 followed; the four works in `works/` come from m10.

## Layout

The full project layout. Only `works/` (the four m10 work files) is published
so far.

```
works/cast.py           Shiroko (white fox) and Kuro (black cat), defined once.
                        A work names a cast member rather than restating hair,
                        eyes and ears.
works/<slug>.py         the work: four koma and the dialogue on each. WRITE-ONCE
                        for the generation spec; `lines` are correctable, since
                        lettering is re-run from raw/ and never overwrites it.
scripts/
  run_full.sh             unattended: reuse-or-create pod, build, weights,
                          generate, fetch, tear down
  sweep.py                the runner; posts to sd-server, writes manifest.csv
  sweeps/<version>.py     WRITE-ONCE sweep configs. Each carries its reasoning
                          in its docstring; that docstring is the run's record
  letter.py               speech balloons + dialogue onto raw koma -> lettered/
  compose_page.py         four koma -> one yonkoma page with frames and gutters
  sheets.py               koma x alternatives grid, for choosing combinations
  remote/                 scripts that run ON the pod (build, weights, server)
datasets/               LoRA training sets, as selected (reproducibility)
state/                  .vast_instance_id, .vast_stranded_ids: rented-machine
                        bookkeeping, kept out of the work
outputs/runs/<run>/
  raw/                    exactly what the model returned. Never written again
  lettered/               raw + balloons
  pages/                  assembled strips, from raw/ and from lettered/
  sheets/                 the candidate grids
  manifest.csv            per image: work, koma, shot, style, seed, cfg, steps,
                          size, sampler, timing, full positive and negative
  lettering.csv           per balloon: chosen anchor and why, fill, ink, contrast
  pages.csv               per page: which koma files, sampled ink and paper
```

## Naming

Review in the browser comes after the first review pass, so until then the
filename is the index:

```
0007__w1_kotatsu__k3__mono__s2101__cfg4.5.png
 |     |           |    |      |      `- cfg
 |     |           |    |      `-------- seed
 |     |           |    `--------------- style: mono | pale_flat
 |     |           `-------------------- koma number within the strip
 |     `-------------------------------- work
 `-------------------------------------- generation index, run-unique
```

Lettered frames keep the source name and add `__lettered`. Pages are
`<work>__page__<style>__s<seed>__<lettered|raw>.png`. Every field is also a
column in `manifest.csv`, so the filenames are for the eye and the CSV is for
the tooling; neither is derived from the other at read time.

Both a raw and a lettered copy of every frame survive, and pages are built from
both. Raw is the expensive artifact (it needs a GPU and cannot be reproduced by
hand), while lettering is seconds of CPU, so lettering never overwrites and
never edits in place.

## What is measured

Two things are read off each rendered koma rather than fixed in advance, both
of them about a pasted-on element looking pasted on.

Where the balloon goes. Each balloon is placed in the emptiest of six candidate
positions, scored by mean gradient energy over the area it would cover. The
anchor written in the work file gets a discount, so it wins ties but loses to a
position that is genuinely clearer: the same line in a wide shot and in a
close-up does not have its space in the same place, and the work file is written
before any image exists. Balloons already placed in that koma are disqualifying
rather than merely expensive. `lettering.csv` records the chosen anchor, the
authored one, both busyness scores, and the runner-up.

What colour it is. Balloon fill is the local background pushed 90% toward white,
so a balloon on a dim kotatsu room is warm-white and one on a bright summer
floor is cool-white. Outline and text ink are sampled from the frame's own
darkest tone, then darkened until they clear a 7:1 contrast ratio against that
fill. Sampling matches the ink to the drawing, and the contrast floor keeps
the words readable. Page frames sample ink and paper across all four koma at
once, with a floor on how light the rule may be, so one pale panel cannot leave
the border reading as part of a drawing.

The balloon tail points at the centroid of the koma's gradient energy, which on
a single-subject frame lands on the character. It is a heuristic and it will be
wrong on a busy background; a face detector is the obvious upgrade and is not
worth building before the first review says the rest of this works.

## Typesetting

Vertical, right-to-left columns; a `\n` in a work file's line is a column break.
Kana are set in a serif face and kanji in a sans face, the "anti-gothic"
convention Japanese lettering actually uses; a single uniform font is the most
obvious tell of machine lettering. Long-vowel marks, brackets and ellipses are
rotated; small kana and the Japanese comma and full stop are offset within their
cell. Everything is drawn at 3x and downsampled.

Three balloon shapes: ellipse, jagged (shout), scalloped cloud (thought). All
three are filled and stroked as the union of their parts via mask arithmetic,
not part by part. That is the only way a cloud comes out as one continuous
scalloped line instead of a chain of visible rings, and the only way a tail
joins a jagged balloon without a notch.

## Running it

Once the scripts are published:

```sh
# generate (about 20 min from cold, ~$0.20 on an RTX 5090 Secure Cloud)
TEARDOWN=stop ./scripts/run_full.sh m1_smoke 40

# everything after this is local CPU, seconds
python3 scripts/letter.py       --run outputs/runs/m1_smoke
python3 scripts/compose_page.py --run outputs/runs/m1_smoke
python3 scripts/sheets.py       --run outputs/runs/m1_smoke --source raw

# build one page from four chosen koma
python3 scripts/compose_page.py --run outputs/runs/m1_smoke \
    --pick 0001 0006 0011 0036 --name w1_kotatsu__page__hand
```

`run_full.sh` reads `VAST_AI_API_KEY` from this project's `.env`, or from
`../stable-diffusion-cpp/.env` when there is none: one key in one file, one
place to revoke it. `TEARDOWN` is `stop` (keep the disk, next run skips the
8-minute build), `destroy` (ends all billing), or `none`.

`.vast_instance_id` is this project's own. It does not share an instance with
stable-diffusion-cpp, and both can hold a stopped disk at the same time.

## Inherited from stable-diffusion-cpp

`../stable-diffusion-cpp` (a separate, unpublished project) is where the
checkpoint, the negative prompt blocks and the pod orchestration were worked out
over ~14 runs. Carried over unchanged: WAI-illustrious-SDXL v13.0 with the
fp16-fix VAE, the anti-gloss and corrected-face negatives (the finding that moved
output out of the glossy AI register), cfg 4.5, euler_a/discrete,
sha256-verified weights from HF mirrors, and the write-once sweep-config rule.

Deliberately dropped: the Lap Pillow Invitation LoRA and the POV camera block.
Both are ear-cleaning ASMR cover-art furniture, and a POV lap-pillow gesture is
the opposite of what a koma needs.

Changed: 1024x768 instead of 16:9 (a koma is wider than tall, but not by 16:9,
and both are 64-aligned so sd.cpp does not silently round the request), and the
manifest carries `work`/`panel`/`shot` so an image can be put back into its
strip without parsing its name.

## Misc.

This repository is under construction and I'm currently working on it. The
scripts, the cast file and the remaining works will be added as they are
cleaned up, and this README will change with them.

## The web review port, when it happens

`../audio-novel-works/web` (another unpublished project) is the model: an Astro
SSR app whose only side effect is writing `picks.json`, which the render step
then reads. The structure maps onto manga almost one for one.

| audio-novel-works | manga equivalent |
|---|---|
| episode -> sections | work -> koma |
| SFX slot with 4 takes | koma with its 2 to 6 generated alternatives |
| `auto_pick` + `auto_reason` from measurements | the same, from the placement/colour scoring here |
| `picks.json` overrides, `mix_work.py` re-renders | picks override, `compose_page.py` re-renders |
| swap a take mid-playback, keep your position | swap a koma and re-render the strip in place |
| every reject kept and offered | `raw/` keeps every generation |

Two things do not map, and they are the reason the port waits for a review pass:

- Audio review is serial: you play a section and switch takes inside it. Manga
  review is parallel: four koma are visible at once and the judgement is about
  the whole strip. The layout is a grid instead of a timeline, and the "play"
  affordance has no equivalent.
- Audio has a hard split between what a measurement can decide (a broken take)
  and what only ears can (a better take). Here the measurements decide balloon
  placement, which is a decision the reviewer will want to *override per
  balloon*: drag it, or pick an anchor. That is an editing surface, and the audio
  app explicitly refused to build one. Whether it is needed is the main thing
  the first review should answer.
