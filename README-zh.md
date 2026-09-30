# manga-vastai

[English](README.md) · 简体中文 · [繁體中文](README-zh-tw.md)

在 Vast.ai 上租用 GPU 生成的四格漫画：每一格（koma）的图由 [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) 搭配 WAI-illustrious-SDXL v13.0 画出来，其余不属于“画”的部分，也就是边框、格间留白、对话框和台词，全部用 Python 计算。

这个分工就是整个设计的核心，直接来自最初的那段讨论：*“格子那种东西不用交给模型，可以用程序摆上去。”* 扩散模型拼不出日文，也画不出笔直的边框，但能画出图的只有它。所以只让它画图，并在 sweep 的负向提示词里放进 `speech bubble, text, border, comic panel`，让它远离那些它只会做坏的部分。

同一段讨论的另一半，说明了对话框为什么仍然要*测量*而不是写死：*“只是摆上去的话，框可能会有点浮，对比也可能会浮出来，所以那一带的颜色要计算一下。”* 位置和颜色都是从每一张生成好的格子上采样决定的。详见下面的“测量了什么”。

## 产出了什么

最新一次运行 `m10_gijutsushi` 产出了四部作品。这是技术史系列：Kuro（小黑）拿起一件工具，自己一路想通它的原理。图出自模型，边框、对话框和文字出自 Python。

- `w37_kami`，“纸”：纸，公元 105 年，东汉
- `w38_katsuji`，“重新排列”：活字印刷，约 1450 年，美因茨
- `w39_mizunomichi`，“水的路”：阿庇亚水道，公元前 312 年
- `w40_yuge`，“被推动”：蒸汽，1712 年，英格兰

每部作品各跑了七个 seed，每部挑出一条。候选表显示这一条是从哪些里面挑出来的：一行是一格，横向是各个 seed，一共 28 张，嵌字前（raw）和嵌字后并排，每一张下方标出选中的锚点和它的拥挤度分数。

生成的图片没有收录在这个仓库中（见“关于这个仓库”）。

## 关于这个仓库

这个仓库是我的个人项目（manga-vastai），始于 2026 年 6 月，经过部分修订并整理成可公开的形式，目的是为了公共利益，发布其中可复现的一部分。

目前收录的内容：`works/` 下的技术史系列四个作品文件。下面描述的其余流程（运行器、嵌字与排版脚本、作品所导入的共用角色文件）正在整理中，会分阶段加入，所以作品文件目前还无法单独运行。

### 许可证

本仓库的所有内容均采用 [MIT 许可证](LICENSE)。

### 免责声明

这些条漫涉及真实历史，并且为了塞进四格而大幅压缩。它们遵循通俗的一般说法，目的是让你自己去查证，所以请不要引用它们。`w37_kami` 是最明显的例子：它把时间定在公元 105 年蔡伦的记载，但西汉时期就有纸的残片留存，而那段记载归功于他的，是用树皮、麻布碎料和旧渔网做成的廉价配方，而不是纸的发明本身。作品文件自己的 docstring 也是这么写的。房间、工具和服装都由模型虚构，并未重现任何特定的地点或时代。

角色均为虚构，与任何在世人物无关。

本仓库不分发模型权重，上述许可证也不涵盖它们。WAI-illustrious-SDXL 及其底层的 Illustrious/SDXL 系列有各自的条款，在复用提示词生成任何你自己的东西之前，请先阅读。

代码不附带任何形式的担保。`run_full.sh` 会向第三方租用 GPU 并花费真实的金钱，所以 API 密钥、账单和关机都要你自己留意：没能停止的实例会持续计费，`state/.vast_stranded_ids` 就是为了发现这种情况而存在的。本项目与 Vast.ai、Hugging Face、leejet/stable-diffusion.cpp 以及该模型的作者均无关联。

## 状态

第一次运行是 m1_smoke：两部作品、40 张图，完成生成、嵌字并组成 8 条条漫。它的目的是在动手写审阅界面之前，先弄清楚那个界面需要显示什么，所以浏览器审阅应用刻意还没有做。

| | w1_kotatsu | w2_ice |
|---|---|---|
| 标题 | “尾巴与被炉” | “在融化之前” |
| 角色 | 白狐 / 长发 / 针织衫 (`a_fox_white`) | 黑猫 / 短发 / 衬衫 (`c_cat_black`) |
| 场景 | 冬天、榻榻米、被炉、暖色灯 | 夏天、木地板、电风扇、日光 |
| 笑点 | 塞不进被炉的尾巴 | 化得比她吃得还快的冰棍 |
| 难点 | 同一张脸横跨四种镜头距离 | 一个物体在四格之间改变状态 |

之后又跑了 m2 到 m10；`works/` 里的四部作品出自 m10。

## 目录结构

完整的项目结构。目前只公开了 `works/`（m10 的四个作品文件）。

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

## 命名

浏览器审阅要等第一轮审阅之后才会做，在那之前，文件名就是索引：

```
0007__w1_kotatsu__k3__mono__s2101__cfg4.5.png
 |     |           |    |      |      `- cfg
 |     |           |    |      `-------- seed
 |     |           |    `--------------- style: mono | pale_flat
 |     |           `-------------------- koma number within the strip
 |     `-------------------------------- work
 `-------------------------------------- generation index, run-unique
```

嵌字后的格子沿用原始文件名并加上 `__lettered`。页面的文件名是 `<work>__page__<style>__s<seed>__<lettered|raw>.png`。每个字段同时也是 `manifest.csv` 的一列，所以文件名是给人看的，CSV 是给工具用的；读取时两者都不从对方推导。

每一格的 raw 版和嵌字版都会保留，页面也会分别由两者组成。raw 是昂贵的产物（需要 GPU，无法手工复现），而嵌字只要几秒的 CPU，所以嵌字永远不会覆盖，也不会原地修改。

## 测量了什么

有两件事是从每一张生成好的格子上读出来的，而不是事先固定的，两者都是为了避免贴上去的元素看起来像是贴上去的。

对话框放在哪里。每个对话框会放在六个候选位置中最空的那一个，评分方式是它将覆盖的区域内的平均梯度能量。作品文件里写的锚点会获得折扣，所以平局时它会胜出，但遇到真正更空的位置就会输：同一句台词在远景和特写中，可用的空间并不在同一个地方，而作品文件是在任何图片存在之前写的。同一格中已经放好的对话框会直接取消该位置的资格，而不只是提高代价。`lettering.csv` 记录了选中的锚点、作者指定的锚点、两者的拥挤度分数，以及第二名。

它是什么颜色。对话框的填充色是把局部背景往白色推 90%，所以放在昏暗被炉房间里的对话框是暖白，放在明亮夏日地板上的是冷白。外框和文字的墨色取自该格本身最暗的色调，再加深到与填充色的对比度达到 7:1 为止。采样让墨色贴合画面，对比度下限则让文字保持可读。页面边框会一次对全部四格采样墨色和纸色，并限制边框最浅能到多浅，这样某一格偏淡时，边框也不会看起来像是画的一部分。

对话框的尾巴指向该格梯度能量的重心，在只有单一主体的画面上会落在角色身上。这是经验法则，在背景杂乱时会出错；人脸检测器是明显的升级方向，但在第一轮审阅确认其余部分可行之前，不值得去做。

## 排版

竖排，从右到左分栏；作品文件台词中的 `\n` 表示换栏。假名用衬线字体，汉字用无衬线字体，这是日本漫画嵌字实际使用的“反哥特体”惯例；通篇只用一种字体，是机器嵌字最明显的破绽。长音符号、括号和省略号会旋转；小写假名和日文的逗号、句号会在字格内偏移。全部先以 3 倍大小绘制再缩小。

三种对话框形状：椭圆、锯齿（喊叫）、云朵状（心声）。三者都通过遮罩运算，以各部件的并集来填充和描边，而不是逐一处理各部件。只有这样，云朵才会是一条连续的波浪线，而不是一串看得见的圆圈；尾巴接上锯齿对话框时也才不会出现缺口。

## 运行方式

等脚本公开之后：

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

`run_full.sh` 会从本项目的 `.env` 读取 `VAST_AI_API_KEY`，没有的话就从 `../stable-diffusion-cpp/.env` 读取：一个密钥放在一个文件里，要吊销也只有一个地方。`TEARDOWN` 可以是 `stop`（保留磁盘，下次运行可跳过 8 分钟的构建）、`destroy`（结束所有计费）或 `none`。

`.vast_instance_id` 是本项目自己的。它不与 stable-diffusion-cpp 共用实例，两者可以同时各保留一个已停止的磁盘。

## 沿用自 stable-diffusion-cpp

`../stable-diffusion-cpp`（另一个未公开的项目）是经过约 14 次运行，摸索出模型检查点、负向提示词块和 pod 编排的地方。原封不动沿用的有：WAI-illustrious-SDXL v13.0 搭配 fp16-fix VAE、抗光泽与面部修正的负向提示词（这个发现让产出摆脱了油亮的 AI 感）、cfg 4.5、euler_a/discrete、从 HF 镜像获取并经 sha256 校验的权重，以及 sweep 配置只写一次的规则。

刻意舍弃的有：Lap Pillow Invitation LoRA 和 POV 镜头块。两者都是采耳 ASMR 封面图的配置，而 POV 的膝枕姿势恰好与一格漫画所需要的相反。

更改的有：用 1024x768 取代 16:9（一格是横的，但没有横到 16:9，而且两个尺寸都对齐 64，sd.cpp 就不会悄悄把请求的尺寸取整），以及 manifest 带有 `work`/`panel`/`shot`，不必解析文件名就能把图片放回它所属的条漫。

## 其他

这个仓库仍在建设中，我目前正在进行。脚本、角色文件和其余作品会在整理好之后陆续加入，这份 README 也会随之更新。

## 网页审阅工具，等做的时候

`../audio-novel-works/web`（另一个未公开的项目）就是范本：一个 Astro SSR 应用，唯一的副作用是写出 `picks.json`，再由渲染步骤读取。它的结构几乎可以一一对应到漫画。

| audio-novel-works | 漫画中的对应 |
|---|---|
| episode -> sections | 作品 -> 格 |
| 有 4 个 take 的音效槽位 | 有 2 到 6 张生成候选的格 |
| 由测量得出的 `auto_pick` + `auto_reason` | 相同，由这里的位置与颜色评分得出 |
| `picks.json` 覆盖，`mix_work.py` 重新渲染 | picks 覆盖，`compose_page.py` 重新渲染 |
| 播放中途换 take，保留播放位置 | 换掉一格，原地重新渲染整条 |
| 保留并提供每一个落选 | `raw/` 保留每一次生成 |

有两件事无法对应，这也是这个工具要等一轮审阅之后才做的原因：

- 音频审阅是串行的：播放一个段落，在其中切换 take。漫画审阅是并行的：四格同时可见，判断的对象是整条。版面是网格而不是时间轴，“播放”这个操作也没有对应。
- 音频在“测量能决定的”（坏掉的 take）和“只有耳朵能决定的”（更好的 take）之间有明确的界线。这里由测量决定对话框的位置，而审阅者会想要*逐一覆盖每个对话框*：拖动它，或选一个锚点。那是一个编辑界面，而音频应用明确拒绝做这种东西。是否需要它，正是第一轮审阅最主要要回答的问题。
