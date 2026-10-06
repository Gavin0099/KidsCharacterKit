# 角色繪圖與動畫流程的 GitHub 重用評估

評估日期：2026-10-06。這是工具選型研究，尚未安裝第三方 skill、執行其腳本或變更已核定的生成輸入與 gate。以下效益是閱讀原始文件與程式後的工程判斷，尚未對 KidsCharacterKit 素材做實測。

目前建議：保留現有生成與證據 gate，以 `sprite-pipeline` 的動作流程為參考，優先評估 `hatch-pet` 中授權明確的預覽與驗證工具。只補這個角色庫需要的規格轉接，不建立另一套通用生成平台。

| 來源 | 可重用內容 | 適用 slice | 對本專案的判斷 |
|---|---|---|---|
| [OpenAI game-studio / sprite-pipeline](https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio/skills/sprite-pipeline/SKILL.md) | 已核准 seed、一次生成整段 strip、整段共用 scale、anchor、首幀鎖回、預覽 | 03C1、03C2 | 最貼近最低動作包；採工作方法。此次查到 root 與 game-studio 路徑未見 LICENSE，先不直接複製程式；GitHub 可讀不等於重用授權已確認。 |
| [OpenAI hatch-pet](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/SKILL.md) | 非像素畫風、每個狀態參考同一角色、contact sheet、動畫預覽、atlas 驗證 | 03B 檢查、03C1、03C2 | 選取必要工具，保留其 [Apache-2.0 LICENSE](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/LICENSE.txt) 與來源；不用整套 Codex pet 規格。 |
| [Aseprite](https://github.com/aseprite/aseprite)／[CLI](https://github.com/aseprite/docs/blob/main/cli.md) | 手工 frame/layer/tag、PNG sequence、sheet 與 JSON 匯出 | 03C1、03C2 | 若要手工微調可用；主要面向像素畫，並非目前 Soft Handmade 2.5D 的必需依賴。官方程式受 EULA 約束，不能當成一般 MIT/GPL 工具直接 vendoring。 |
| [rembg](https://github.com/danielgatis/rembg) | 批次去背、alpha matting | 03B 的有底色素材補救 | 現有 PNG 已有真 alpha，預設不跑。去背會變更輸出像素，必須另存 derivative。程式 MIT，但模型權重各有授權，不能由程式授權推定素材權利。 |
| [ComfyUI IPAdapter Plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus) | 參考圖條件控制與範例 workflow | 大量姿勢探索的備案 | 不放進眼前 critical path。需要模型／環境管理，不能保證精確 identity；維護者自 2025-04-14 宣告 maintenance-only。FaceID portrait 路線未證明適用貓、恐龍、Robot。 |

## 原始碼顯示的適配缺口

`sprite-pipeline` 的 [normalize_sprite_strip.py](https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio/scripts/normalize_sprite_strip.py) 已共用 scale，但每幀依 alpha bbox 裁切再置中／貼底，並以 NEAREST 縮放。這裡的 bottom-center 是圖形外框，不是我們需要的腳底接觸點：尾巴、放大鏡或伸手改變外框，就可能移動角色。首幀直接鎖回原圖時，也要確認與其餘幀的縮放、pivot 一致。套用時需明確的語意 ground anchor、預留動作空間，以及適用非像素畫的縮放／透明邊緣檢查。

`hatch-pet` 的 [extract_strip_frames.py](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/scripts/extract_strip_frames.py) 有 stable-slot 分支可借鏡；其他分支會逐幀 fit，而且預設移除綠色 chroma key。薄荷綠恐龍需要避免這個預設。其 192×208 cell、8×9 atlas、九種狀態和 pet.json 是特定產品規格，不能帶進我們的 1024 raster／引擎中立 animation contract。透明區 RGB 歸零只可在交付 derivative 明確記錄；canonical originals 的 hash 不改。

## 建議接到既有 slice 的方式

1. **03B1／03B2**：沿用 identity、輸入 hash、生成預算、Owner 視覺核准與 Style Bible；外部 skill 不會替代這些決定。A3 的 source-locked 高光修正是本次明確授權的局部問題，不需要引入去背或另一套模型。
2. **03B**：用成熟影像函式庫處理確定性的 delivery derivative；每項操作保留 source/output hash、參數與工具版本。先確認角色視覺比例和 ground anchor，不能各自塞滿 canvas。
3. **03C**：規格先表達 action、各幀時間、loop、ground anchor、prop socket／layer／handoff；atlas 是可選匯出，不綁 pet 格式或特定引擎。
4. **03C1**：model-sheet gate 通過後，以已核准 seed 一次產出 2–4 key poses／短 strip；點心保持獨立。每段由同一 master 參考，不逐幀重新 text-to-image。
5. **03C2**：重用 contact sheet／動畫預覽的方式，再在消費端測試角色不跳位、不變比例、腳底接觸與點心交接。Python 工具通過不等於遊戲 motion feel 通過。

導入時固定來源 commit、保留 LICENSE／notice、記錄修改，再用 Cat／Dino 的實際 fixture 驗證。現在可以先重用流程與預覽方法；是否引入完整模型系統，等既有路線有實際無法解決的產量或一致性問題再決定。
