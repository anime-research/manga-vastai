# manga-vastai

[English](README.md) · [简体中文](README-zh.md) · 繁體中文

在 Vast.ai 上租用 GPU 生成的四格漫畫：每一格（koma）的圖由 [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) 搭配 WAI-illustrious-SDXL v13.0 畫出來，其餘不屬於「畫」的部分，也就是框線、格間留白、對話框和台詞，全部用 Python 計算。

這個分工就是整個設計的核心，直接來自最初的那段討論：*「格子那種東西不用交給模型，可以用程式擺上去。」* 擴散模型拼不出日文，也畫不出筆直的框線，但能畫出圖的只有它。所以只讓它畫圖，並在 sweep 的負向提示詞裡放進 `speech bubble, text, border, comic panel`，讓它遠離那些它只會做壞的部分。

同一段討論的另一半，說明了對話框為何仍然要*量測*而不是寫死：*「只是擺上去的話，框可能會有點浮，對比也可能會浮出來，所以那一帶的顏色要計算一下。」* 位置和顏色都是從每一張算好的格子上取樣決定的。詳見下面的「量測了什麼」。

## 產出了什麼

最新一次執行 `m10_gijutsushi` 產出了四部作品。這是技術史系列：Kuro（小黑）拿起一件工具，自己一路想通它的原理。圖出自模型，框線、對話框和文字出自 Python。

- `w37_kami`，「紙」：紙，公元 105 年，東漢
- `w38_katsuji`，「重新排列」：活字印刷，約 1450 年，美因茲
- `w39_mizunomichi`，「水的路」：阿庇亞水道，公元前 312 年
- `w40_yuge`，「被推動」：蒸汽，1712 年，英格蘭

每部作品各跑了七個 seed，每部挑出一條。候選表顯示這一條是從哪些裡面挑出來的：一列是一格，橫向是各個 seed，一共 28 張，嵌字前（raw）和嵌字後並排，每一張下方標出選中的錨點和它的擁擠度分數。

生成的圖片沒有收錄在這個儲存庫中（見「關於這個儲存庫」）。

## 關於這個儲存庫

這個儲存庫是我的個人專案（manga-vastai），始於 2026 年 6 月，經過部分修訂並整理成可公開的形式，目的是為了公共利益，釋出其中可重現的一部分。

目前收錄的內容：`works/` 下的技術史系列四個作品檔。下面描述的其餘流程（執行器、嵌字與排版腳本、作品所匯入的共用角色檔）正在整理中，會分階段加入，所以作品檔目前還無法單獨執行。

### 授權條款

本儲存庫的所有內容皆採用 [MIT 授權條款](LICENSE)。

### 免責聲明

這些條漫涉及真實歷史，並且為了塞進四格而大幅壓縮。它們依循通俗的一般說法，目的是讓你自己去查證，所以請不要引用它們。`w37_kami` 是最明顯的例子：它把時間定在公元 105 年蔡倫的記載，但西漢時期就有紙的殘片留存，而那段記載歸功於他的，是以樹皮、麻布碎料和舊漁網做成的廉價配方，而不是紙的發明本身。作品檔自己的 docstring 也這樣寫。房間、工具和服裝都由模型虛構，並未重現任何特定的地點或時代。

角色皆為虛構，與任何在世人物無關。

本儲存庫不轉發模型權重，上述授權條款也不涵蓋它們。WAI-illustrious-SDXL 及其底層的 Illustrious/SDXL 系列有各自的條款，重複使用提示詞生成任何你自己的東西之前，請先閱讀。

程式碼不附帶任何形式的擔保。`run_full.sh` 會向第三方租用 GPU 並花費真實的金錢，所以 API 金鑰、帳單和關機都要你自己留意：沒能停止的執行個體會持續計費，`state/.vast_stranded_ids` 就是為了抓出這種情況而存在。本專案與 Vast.ai、Hugging Face、leejet/stable-diffusion.cpp 以及該模型的作者均無關聯。

## 狀態

第一次執行是 m1_smoke：兩部作品、40 張圖，完成生成、嵌字並組成 8 條條漫。它的目的是在動手寫審閱介面之前，先弄清楚那個介面需要顯示什麼，所以瀏覽器審閱應用刻意還沒做。

| | w1_kotatsu | w2_ice |
|---|---|---|
| 標題 | 「尾巴與暖桌」 | 「在融化之前」 |
| 角色 | 白狐 / 長髮 / 針織衫 (`a_fox_white`) | 黑貓 / 短髮 / 襯衫 (`c_cat_black`) |
| 場景 | 冬天、榻榻米、暖桌、暖色燈 | 夏天、木地板、電風扇、日光 |
| 笑點 | 塞不進暖桌的尾巴 | 融化得比她吃得還快的冰棒 |
| 難點 | 同一張臉橫跨四種鏡頭距離 | 一個物件在四格之間改變狀態 |

之後又跑了 m2 到 m10；`works/` 裡的四部作品出自 m10。

## 目錄結構

完整的專案結構。目前只公開了 `works/`（m10 的四個作品檔）。

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

瀏覽器審閱要等第一輪審閱之後才會做，在那之前，檔名就是索引：

```
0007__w1_kotatsu__k3__mono__s2101__cfg4.5.png
 |     |           |    |      |      `- cfg
 |     |           |    |      `-------- seed
 |     |           |    `--------------- style: mono | pale_flat
 |     |           `-------------------- koma number within the strip
 |     `-------------------------------- work
 `-------------------------------------- generation index, run-unique
```

嵌字後的格子沿用原始檔名並加上 `__lettered`。頁面的檔名是 `<work>__page__<style>__s<seed>__<lettered|raw>.png`。每個欄位同時也是 `manifest.csv` 的一欄，所以檔名是給人看的，CSV 是給工具用的；讀取時兩者都不從對方推導。

每一格的 raw 版和嵌字版都會保留，頁面也會分別由兩者組成。raw 是昂貴的產物（需要 GPU，無法用手重現），而嵌字只要幾秒的 CPU，所以嵌字永遠不會覆寫，也不會就地修改。

## 量測了什麼

有兩件事是從每一張算好的格子上讀出來，而不是事先固定的，兩者都是為了避免貼上去的元素看起來像是貼上去的。

對話框放在哪裡。每個對話框會放在六個候選位置中最空的那一個，評分方式是它將覆蓋的區域內的平均梯度能量。作品檔裡寫的錨點會獲得折扣，所以平手時它會勝出，但遇到真正更空的位置就會輸：同一句台詞在遠景和特寫中，可用的空間並不在同一個地方，而作品檔是在任何圖片存在之前寫的。同一格中已經放好的對話框會直接取消該位置的資格，而不只是提高成本。`lettering.csv` 記錄了選中的錨點、作者指定的錨點、兩者的擁擠度分數，以及第二名。

它是什麼顏色。對話框的填色是把局部背景往白色推 90%，所以放在昏暗暖桌房間裡的對話框是暖白，放在明亮夏日地板上的是冷白。外框和文字的墨色取自該格本身最暗的色調，再加深到與填色的對比達到 7:1 為止。取樣讓墨色貼合畫面，對比下限則讓文字保持可讀。頁面框線會一次對全部四格取樣墨色和紙色，並限制框線最淺能到多淺，這樣某一格偏淡時，框線也不會看起來像是畫的一部分。

對話框的尾巴指向該格梯度能量的重心，在只有單一主體的畫面上會落在角色身上。這是經驗法則，在背景雜亂時會出錯；臉部偵測器是明顯的升級方向，但在第一輪審閱確認其餘部分可行之前，不值得去做。

## 排版

直書，由右至左分欄；作品檔台詞中的 `\n` 代表換欄。假名用襯線字體，漢字用無襯線字體，這是日本漫畫嵌字實際使用的「反哥德體」慣例；整篇只用一種字體，是機器嵌字最明顯的破綻。長音符號、括號和刪節號會旋轉；小寫假名和日文的逗號、句號會在字格內偏移。全部先以 3 倍大小繪製再縮小。

三種對話框形狀：橢圓、鋸齒（喊叫）、雲朵狀（心聲）。三者都透過遮罩運算，以各部件的聯集來填色和描邊，而不是逐一處理各部件。只有這樣，雲朵才會是一條連續的波浪線，而不是一串看得見的圓圈；尾巴接上鋸齒對話框時也才不會出現缺口。

## 執行方式

等腳本公開之後：

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

`run_full.sh` 會從本專案的 `.env` 讀取 `VAST_AI_API_KEY`，沒有的話就從 `../stable-diffusion-cpp/.env` 讀取：一把金鑰放在一個檔案裡，要撤銷也只有一個地方。`TEARDOWN` 可以是 `stop`（保留磁碟，下次執行可跳過 8 分鐘的建置）、`destroy`（結束所有計費）或 `none`。

`.vast_instance_id` 是本專案自己的。它不與 stable-diffusion-cpp 共用執行個體，兩者可以同時各保有一個已停止的磁碟。

## 沿用自 stable-diffusion-cpp

`../stable-diffusion-cpp`（另一個未公開的專案）是經過約 14 次執行，摸索出模型檢查點、負向提示詞區塊和 pod 編排的地方。原封不動沿用的有：WAI-illustrious-SDXL v13.0 搭配 fp16-fix VAE、抗光澤與臉部修正的負向提示詞（這個發現讓產出擺脫了油亮的 AI 感）、cfg 4.5、euler_a/discrete、從 HF 鏡像取得並以 sha256 驗證的權重，以及 sweep 設定只寫一次的規則。

刻意捨棄的有：Lap Pillow Invitation LoRA 和 POV 鏡頭區塊。兩者都是掏耳朵 ASMR 封面圖的配備，而 POV 的膝枕姿勢正好與一格漫畫所需要的相反。

更改的有：用 1024x768 取代 16:9（一格是橫的，但沒有橫到 16:9，而且兩個尺寸都對齊 64，sd.cpp 就不會悄悄把請求的尺寸四捨五入），以及 manifest 帶有 `work`/`panel`/`shot`，不必解析檔名就能把圖片放回它所屬的條漫。

## 其他

這個儲存庫仍在建置中，我目前正在進行。腳本、角色檔和其餘作品會在整理好之後陸續加入，這份 README 也會隨之更新。

## 網頁審閱工具，等做的時候

`../audio-novel-works/web`（另一個未公開的專案）就是範本：一個 Astro SSR 應用，唯一的副作用是寫出 `picks.json`，再由算圖步驟讀取。它的結構幾乎可以一對一對應到漫畫。

| audio-novel-works | 漫畫中的對應 |
|---|---|
| episode -> sections | 作品 -> 格 |
| 有 4 個 take 的音效欄位 | 有 2 到 6 張生成候選的格 |
| 由量測得出的 `auto_pick` + `auto_reason` | 相同，由這裡的位置與顏色評分得出 |
| `picks.json` 覆寫，`mix_work.py` 重新算出 | picks 覆寫，`compose_page.py` 重新算出 |
| 播放中途換 take，保留播放位置 | 換掉一格，就地重新算出整條 |
| 保留並提供每一個落選 | `raw/` 保留每一次生成 |

有兩件事無法對應，這也是這個工具要等一輪審閱之後才做的原因：

- 音訊審閱是循序的：播放一個段落，在其中切換 take。漫畫審閱是平行的：四格同時可見，判斷的對象是整條。版面是網格而不是時間軸，「播放」這個操作也沒有對應。
- 音訊在「量測能決定的」（壞掉的 take）和「只有耳朵能決定的」（更好的 take）之間有明確的界線。這裡由量測決定對話框的位置，而審閱者會想要*逐一覆寫每個對話框*：拖動它，或選一個錨點。那是一個編輯介面，而音訊應用明確拒絕做這種東西。是否需要它，正是第一輪審閱最主要要回答的問題。
