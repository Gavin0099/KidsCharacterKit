# Character Style Bible v1

**狀態：Owner 已核准 v1 作畫規格與精確三角色參考集合。日期：2026-10-06。**
[核准紀錄](../concepts/kck-03b2/evidence/2026-10-06-owner-v1-approval.json) 保留問題、原文回覆與 review-candidate SHA-256。
本文件延續 [Style Bible v0](character-style-bible.md) 的已核准方向，成為後續作畫規格；
[representation contract](character-representation-contract.md) 與 [GOVERNANCE.md](../GOVERNANCE.md) 繼續約束 delivery／權利／驗收。
文件核准不代表 model sheets 或整個 03B2 已完成。

Owner 在看過修正後 lineup 後回覆「有 風格比較一治了」，確認風格比較一致。
[回覆紀錄](../concepts/kck-03b1/evidence/2026-10-06-lineup-style-feedback.json)
保留原文與當時的確認範圍。Owner 隨後另行明確回覆「核准 v1 與參考集合，繼續 Cat／Dinosaur model sheets」，
接受 identity、同一世界、64px 辨識與本文件規格；Cat／修正 Robot 現為 approved_reference，production／權利仍未核准。

## 1. 視覺方向與精確參考

**Soft Handmade 2.5D：平面色塊、受控手作紋理、輕微體積，友善而清楚。**
參考原圖的輪廓、表情和色彩角色；使用三角色 lineup 檢查共通畫風。
並排圖與黑色輪廓圖只供 QA，生成時傳入個別原圖。

| 角色 | v1 精確參考 | 現行狀態／用途 |
|---|---|---|
| Cat | [Cat B1-B](../concepts/kck-03b1/outputs/Cat-B1B-attempt-01.png) | `cat-concept-01`，approved_reference；identity 來源 `cat-02` |
| Dinosaur | [修正 A3](../concepts/kck-03b1/outputs/A3-v2d-attempt-01-highlight-corrected.png) | `dinosaur-concept-03`，已核准 Dinosaur style key；identity 來源 `dinosaur-01` |
| Robot | [修正 Robot](../concepts/kck-03b1/outputs/Robot-B1B-attempt-01-highlight-corrected.png) | `robot-concept-02`，approved_reference；identity 來源 `robot-01` |

每個檔案的 raw／RGBA hash、原生尺寸、概念 provenance 與狀態在
[基準索引](../concepts/kck-03b2/style-bible-v1-reference-set.json) 固定。
這是作畫參考集合，不是新 character manifest、selected master 或 production。
原始 A3／Robot 失敗圖、A4 失敗圖與所有修正紀錄繼續保留。

## 2. 共通 rendering 規格

| 項目 | 作畫要求 | 檢查方式 |
|---|---|---|
| 外框 | 深暖棕色、閉合清楚，保留輕微手繪變化；在角色各自輪廓上維持一致的視覺重量 | 原生尺寸查斷線／硬邊，64px 查辨識度；不沿用未量測的百分比當門檻 |
| 色塊與體積 | 保留各角色的身份色，以清楚底色、柔和陰影與小範圍高光表現體積 | 白／黑／棋盤背景檢查；避免讓大面積漸層掩蓋色塊 |
| 紋理 | 細紙感／彩鉛粒子，依參考圖控制強度；輪廓與臉部符號在縮小後仍清楚 | 同格式 PNG 在原生尺寸及 64px 視覺檢查；不使用有損 WebP 紋理數值替代原圖 |
| 光源 | 畫面左上；眼睛大高光位於眼睛的左上區域，柔和陰影向右下 | 各角色眼型內檢查方向；不得把 Dinosaur 的數值容差直接套到 Cat／Robot |
| 表面 | 輕微體積、柔和邊界；不新增塑膠鏡面效果或場景光源 | 對照 individual references 和三角色 lineup |
| 背景／陰影 | 真正透明；角色檔不烘焙地板、場景、投影、白邊或底色 | 真 alpha、透明邊緣及白／黑背景人工檢查；corner alpha 不能單獨證明無 matte |

沒有足夠量測依據的 outline%、grain opacity%、head/body 比例維持為 v0
探索資訊，不升格成 v1 硬門檻。此版以固定參考、可觀察要求和 Owner
視覺驗收為依據；若之後新增數值 gate，須另附量測方法與核准紀錄。

## 3. 眼睛：共通方向，保留角色眼型

| 角色 | 保留 | v1 規格 |
|---|---|---|
| Cat | 棕色 iris、可見眼白、大而圓的眼睛，保留表情辨識 | 大高光在左上、小高光在右下；不改成 Dinosaur 的純深色眼球 |
| Dinosaur | 大深棕眼睛；既有 V2 identity 和高光 gate | 大高光＋小高光；V2 大高光 `x=.30–.40, y=.20–.35` 仍只適用這個 Dinosaur 規格 |
| Robot | 較小的深色橢圓眼睛、原有臉部比例 | **核准例外：每眼保留一個左上大高光**，與目前修正圖一致 |

Robot 單高光已由 Owner 在本次 v1 review 明確核准。原探索
[shared rendering brief](kck-03b1-brief.md#shared-rendering-rules-starting-brief)
寫過雙高光；v0 的探索參數允許 1–2 個，但未核准成正式規則。
本次以獨立核准紀錄更新 Robot 規格，不把先前的風格回覆當成豁免。Dinosaur 既有 gate 不變。
Robot 的修正只移動原來的大高光，沒有新增小高光。

## 4. Palette 與角色 identity locks

以各原圖的身份色為基準；紋理、陰影與高光不是額外的新皮膚配色。
此版不把單點抽色當作所有像素必須相等的 RGB gate，也不重染既有素材。

| 角色 | 身份色 | 必須保留的辨識元素 |
|---|---|---|
| Cat | 暖橘、奶油色、粉紅內耳／肉墊／臉頰，深暖棕眼睛與外框 | 圓臉、虎斑色塊、鬍鬚、小鼻、笑口與舌頭、抬掌與肉墊、長彎尾、短腳；本張保持坐姿 |
| Dinosaur | 薄荷綠、奶油肚、柔黃背棘、桃色臉頰，深暖棕眼睛與外框 | 大頭短身、背棘、肚上兩條弧線、尾巴、腳、放大鏡；不因拿點心而刪除放大鏡 |
| Robot | 冷灰、藍手／藍靴、紅色天線端與臉頰；胸前四色 | 方頭、側面平面、兩支天線、長分節四肢、外抬手姿、矩形笑口與舌頭；胸前左上藍圓、右上黃三角、左下紅圓、右下綠矩形 |

比例分別跟隨各自參考。Robot 長四肢、方頭與童畫性格是已存在的明確例外；
保留 Dinosaur 大頭短身與 Cat 坐姿，不把三者調成同一種身材。
視角轉換時記錄角色左右側，不以簡單鏡像改變道具、抬掌或胸前按鈕次序。
目前單視角沒有顯示的背面／側面特徵，在 model-sheet 階段以 candidate
提出；不能宣稱已由本張圖證實。

## 5. Model-sheet 規格與順序

每個將製作 authored animation 或 3D 的角色需要六張個別圖：

| 圖 | 要驗證的資訊 |
|---|---|
| front | 正面 anatomy、臉部符號、左右側與道具位置 |
| three-quarter | 與參考圖接續的體積、頭身比例及遮擋 |
| side | 鼻口／頭身深度、尾巴／背棘／手腳的側面形狀 |
| back | 斑紋／背棘／天線／身體接合，補足目前看不到的部分 |
| happy | 同一比例／眼型下的開心表情；記錄是否閉眼，不新增角色 redesign |
| confused | 同一 anatomy 下的困惑表情；不依賴文字或額外物件 |

先完成 Cat 和 Dinosaur 的 sheet，以支撐 snack minimum pack。
Robot 靜態 lineup 已納入視覺規格；Robot 的六張 sheet 在需要它的 authored
動作或 3D 前完成，不讓 Robot motion／3D 擋住點心快遞。
此交付順序已核准，六張要求本身不降低。

每張以同一個核准參考與核准的 v1 為基礎，保留一份原始輸出、exact
instruction、來源／輸出 hash、tool metadata 與人工驗收紀錄。
不把含文字的 model-sheet 拼版當作生成 seed；拼版只作 QA。
不得逐張 fit 後偽稱比例相同；使用明確尺寸參考與共同 review scale。
新 sheet 先維持 candidate，Owner 接受後才可作 authored motion 的基準。

完成 Style Bible 文件核准與完成角色 sheets 是不同里程碑。
目前沒有任何 sheet，也沒有 model-sheet gate PASS。任何新的生成仍須
遵守當階段的授權／失敗停止條件；不重設 Dinosaur 已耗盡的 v2d 預算。

## 6. 與 delivery／motion 的界線

v1 作畫規格不選定新的 production master，也不修改既有五個 source-app
asset records。[representation contract](character-representation-contract.md)
仍定義 master、delivery 與 ground anchor。

- 正式 raster 為 1024×1024 PNG RGBA；safe margin／anchor／scale 遵守
  [asset-spec.md](asset-spec.md)，由 03B 留下實際 transformation 證據。
- 語意 ground anchor 由腳底接觸點或支撐底線量測，不以 alpha 最低點推算。
- `visual_scale` 仍未決；此 lineup 的共同預覽倍率不代表核准角色實際大小。
- 新風格概念如何成為 versioned selected master，要先補明確選擇與 provenance
  規則；不得覆寫 source-app originals。
- 點心保持獨立 prop。放大鏡、點心 socket／layer／handoff 要在 motion
  contract 定義；目前不預設把放大鏡拿掉或把點心烘焙進角色。
- 程式 bob／squash／rotation 由 consuming app 實作。Authored 2–4 key poses
  仍需要適用角色的核准 model sheets，APNG／contact sheet 僅作 QA。

本文件不產出 production、動畫或 3D，不更改 manifest availability。
所有 rights 欄位維持 pending／unknown。

## 7. Owner acceptance 與下一個里程碑

供 review 的實際素材：

- [三角色正常尺寸／白黑底](../artifacts/qa/2026-10-06-b1c-corrected-lineup/contact-sheet.png)
- [64px 彩色](../artifacts/qa/2026-10-06-b1c-corrected-lineup/small-64.png)
- [64px 黑色輪廓](../artifacts/qa/2026-10-06-b1c-corrected-lineup/silhouette-64.png)

Owner 已明確核准 Cat 與修正 Robot 的 identity／參考用途、三角色 shared-world
與 64px 辨識、§2–5 的 v1 作畫規格（含 Robot 單高光例外與 sheets 順序）。
已核准的 Dinosaur style key 不重開選擇；失敗紀錄不刪除。

文件與參考集合已核准，接著準備 Cat／Dinosaur model sheets；每張仍有自己的
人工驗收。正式 raster 的 selected-master／`visual_scale`／anchor 決定和
production 核准仍在 03B，文件核准不替代它們。
