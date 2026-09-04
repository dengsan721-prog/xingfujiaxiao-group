import importlib.util
import json
import re
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "build_child_growth_docs.py"
OUT = ROOT / "demo" / "index.html"
LOGO_SOURCE = ROOT / "demo" / "assets" / "xingfu-yizhan-logo-source.png"
LOGO_OUT = ROOT / "demo" / "assets" / "xingfu-yizhan-logo.png"
SOURCE_AUDIO_IDS = {
    "9": 368, "8": 367, "76": 601, "214": 840, "221": 851, "364": 1081,
    "171": 746, "835": 2097, "1610": 3522, "1608": 3515, "1135": 2828,
    "115": 663, "119": 669, "332": 1031, "113": 661, "345": 1053,
    "248": 897, "286": 958, "361": 1076, "229": 866, "282": 952,
    "197": 812, "446": 1232, "984": 2463, "1232": 3002, "1522": 3396,
    "1587": 3487, "1510": 3372, "51": 559, "74": 599, "178": 775,
    "562": 1444, "815": 2052, "936": 2335, "1065": 2647, "1345": 3158,
    "1366": 3189, "1446": 3289, "1483": 3338, "1604": 3511, "982": 2455,
    "1593": 3495, "100": 639, "112": 657, "118": 668, "160": 732,
    "124": 678, "126": 682, "317": 1008, "1125": 2802, "1338": 3151,
    "1339": 3152, "1424": 3263, "1466": 3317, "1478": 3331, "1583": 3483,
    "57": 569, "204": 825, "231": 869, "295": 972, "1391": 3223,
    "1495": 3354, "1527": 3401, "11": 424, "141": 703, "501": 1340,
    "1138": 2831, "1143": 2838, "1475": 3328, "1609": 3521,
}


def load_docs():
    spec = importlib.util.spec_from_file_location("child_growth_docs", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    docs = module.DOCS
    for item in docs:
        for index, day in enumerate(item["days"]):
            day["roles"] = module.ROLE_SETS[index % len(module.ROLE_SETS)]
            match = re.search(r"第(\d+)条", day["src"])
            if match and match.group(1) in SOURCE_AUDIO_IDS:
                audio_id = SOURCE_AUDIO_IDS[match.group(1)]
                day["sourceUrl"] = (
                    "https://www.dachun.tv/pages/home/audioDetail/audioDetail"
                    f"?audioId={audio_id}&order=desc&promoteId=15"
                )
    return docs


def render():
    LOGO_OUT.parent.mkdir(parents=True, exist_ok=True)
    if LOGO_SOURCE.exists():
        shutil.copyfile(LOGO_SOURCE, LOGO_OUT)
        image = Image.open(LOGO_OUT).convert("RGBA")
        bbox = image.getbbox()
        if bbox:
            image.crop(bbox).save(LOGO_OUT)
    data = json.dumps(load_docs(), ensure_ascii=False, indent=2)
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>董事长（孩子）长成记 群发助手</title>
  <style>
    :root {{
      --ink: #1d1d1f;
      --muted: #6e6e73;
      --line: #d2d2d7;
      --panel: rgba(255, 255, 255, 0.9);
      --bg: #f5f5f7;
      --brand: #0a84ff;
      --brand-dark: #0067c5;
      --green: #35a936;
      --warm: #f97316;
      --soft: #f0f7ff;
      --shadow: 0 20px 55px rgba(0, 0, 0, 0.08);
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(180deg, #ffffff 0, #f5f5f7 330px, #f5f5f7 100%);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      line-height: 1.55;
    }}
    button, select {{
      font: inherit;
    }}
    .app {{
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }}
    header {{
      background: rgba(251, 251, 253, 0.8);
      backdrop-filter: saturate(180%) blur(18px);
      border-bottom: 1px solid var(--line);
      padding: 16px 28px;
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .topline {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: center;
      max-width: 1280px;
      margin: 0 auto;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 16px;
      min-width: 0;
    }}
    .brand-card {{
      display: flex;
      align-items: center;
      gap: 16px;
      min-width: 0;
    }}
    .brand-copy {{
      min-width: 0;
    }}
    .logo {{
      width: 252px;
      height: 78px;
      object-fit: contain;
      flex: 0 0 auto;
      border-radius: 4px;
    }}
    h1 {{
      margin: 0;
      font-size: 24px;
      letter-spacing: 0;
      font-weight: 700;
    }}
    .status {{
      color: var(--muted);
      font-size: 14px;
      white-space: nowrap;
    }}
    main {{
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 28px 38px;
      display: grid;
      grid-template-columns: 250px minmax(0, 1fr) 310px;
      gap: 18px;
    }}
    aside, .content, .preview {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(14px);
    }}
    aside {{
      padding: 14px;
      align-self: start;
      position: sticky;
      top: 86px;
    }}
    .content {{
      min-width: 0;
      overflow: hidden;
    }}
    .preview {{
      padding: 16px;
      align-self: start;
      position: sticky;
      top: 86px;
    }}
    .label {{
      color: var(--muted);
      font-size: 13px;
      margin: 0 0 7px;
    }}
    select {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      padding: 9px 10px;
      margin-bottom: 14px;
    }}
    .days {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }}
    .day-btn {{
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      cursor: pointer;
      transition: background 160ms ease, color 160ms ease, border 160ms ease;
    }}
    .day-btn.active {{
      background: var(--brand);
      border-color: var(--brand);
      color: #fff;
      font-weight: 700;
    }}
    .copy-row {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .quick-actions {{
      background: rgba(255, 255, 255, 0.72);
      position: sticky;
      top: 112px;
      z-index: 5;
      backdrop-filter: saturate(180%) blur(14px);
    }}
    .copy-btn {{
      border: 1px solid var(--brand);
      background: var(--brand);
      color: #fff;
      border-radius: 6px;
      padding: 8px 11px;
      cursor: pointer;
      min-height: 36px;
      font-weight: 700;
    }}
    .copy-btn.secondary {{
      color: var(--brand-dark);
      background: #fff;
    }}
    .copy-btn:active, .day-btn:active {{
      transform: translateY(1px);
    }}
    .message {{
      padding: 26px;
      white-space: pre-wrap;
      font-size: 16px;
      overflow-wrap: anywhere;
    }}
    .message h2 {{
      margin: 0 0 14px;
      font-size: 28px;
      letter-spacing: 0;
      line-height: 1.22;
    }}
    .message .source {{
      color: var(--muted);
      margin-bottom: 16px;
      font-size: 14px;
    }}
    .source-line {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 10px 12px;
      border: 1px solid #e5e5ea;
      border-radius: 8px;
      background: #fbfbfd;
    }}
    .source-link {{
      flex: 0 0 auto;
      color: #fff;
      background: var(--green);
      border: 1px solid var(--green);
      border-radius: 999px;
      padding: 5px 10px;
      text-decoration: none;
      font-weight: 800;
      font-size: 13px;
    }}
    .section {{
      border-top: 1px solid var(--line);
      padding: 15px 0;
    }}
    .section-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 6px;
    }}
    .section:first-of-type {{
      border-top: 0;
    }}
    .section-title {{
      font-weight: 800;
    }}
    .copy-section-btn {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--brand-dark);
      cursor: pointer;
      padding: 4px 8px;
      font-size: 13px;
      white-space: nowrap;
      font-weight: 700;
    }}
    ol {{
      margin: 7px 0 0 22px;
      padding: 0;
    }}
    li {{
      margin: 3px 0;
    }}
    .preview h2 {{
      margin: 0 0 8px;
      font-size: 18px;
    }}
    .preview p {{
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 14px;
    }}
    .mini-list {{
      display: grid;
      gap: 7px;
    }}
    .mini-day {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px 9px;
      background: #fff;
      cursor: pointer;
      text-align: left;
      font-size: 14px;
      line-height: 1.35;
    }}
    .mini-day.active {{
      background: var(--soft);
      border-color: #9ab6f5;
      color: var(--brand-dark);
      font-weight: 700;
    }}
    .toast {{
      position: fixed;
      right: 24px;
      bottom: 24px;
      background: #1f2937;
      color: #fff;
      border-radius: 6px;
      padding: 10px 13px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 160ms ease;
      z-index: 20;
    }}
    .toast.show {{
      opacity: 1;
    }}
    @media (max-width: 980px) {{
      header {{
        position: static;
      }}
      .topline {{
        align-items: flex-start;
        flex-direction: column;
      }}
      .status {{
        white-space: normal;
      }}
      main {{
        grid-template-columns: 1fr;
        padding: 16px;
      }}
      .quick-actions {{
        top: 0;
      }}
      aside, .preview {{
        position: static;
      }}
      .days {{
        grid-template-columns: repeat(7, 1fr);
      }}
    }}
    @media (max-width: 560px) {{
      header {{
        padding: 15px 16px;
      }}
      .brand-card {{
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
      }}
      .logo {{
        width: min(100%, 330px);
        height: auto;
      }}
      h1 {{
        font-size: 20px;
      }}
      .source-line {{
        align-items: flex-start;
        flex-direction: column;
      }}
      .days {{
        grid-template-columns: repeat(4, 1fr);
      }}
      .copy-btn {{
        width: 100%;
      }}
      .message {{
        padding: 16px;
        font-size: 15px;
      }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <div class="topline">
        <div class="brand brand-card">
          <img class="logo" src="assets/xingfu-yizhan-logo.png" alt="幸福驿站">
          <div class="brand-copy">
            <h1>董事长（孩子）长成记 群发助手</h1>
          </div>
        </div>
        <div class="status" id="status">选择主题和天数，复制后发群</div>
      </div>
    </header>
    <main>
      <aside>
        <p class="label">主题</p>
        <select id="themeSelect"></select>
        <p class="label">天数</p>
        <div class="days" id="dayButtons"></div>
      </aside>
      <section class="content">
        <div class="copy-row quick-actions">
          <button class="copy-btn" id="copyFull">复制当天全文</button>
          <button class="copy-btn secondary" id="copySignin">只复制签到</button>
          <button class="copy-btn secondary" id="copyGame">只复制小游戏</button>
          <button class="copy-btn secondary" id="copyHomework">只复制作业</button>
        </div>
        <article class="message" id="message"></article>
      </section>
      <section class="preview">
        <h2 id="themeTitle"></h2>
        <p id="themeCore"></p>
        <div class="mini-list" id="dayList"></div>
      </section>
    </main>
  </div>
  <div class="toast" id="toast">已复制</div>
  <script>
    const DATA = {data};

    const themeSelect = document.querySelector("#themeSelect");
    const dayButtons = document.querySelector("#dayButtons");
    const dayList = document.querySelector("#dayList");
    const message = document.querySelector("#message");
    const status = document.querySelector("#status");
    const themeTitle = document.querySelector("#themeTitle");
    const themeCore = document.querySelector("#themeCore");
    const toast = document.querySelector("#toast");
    let currentTheme = 0;
    let currentDay = 0;

    function dayText(day, number) {{
      return [
        `第 ${{number}} 天  ${{day.title}}`,
        ``,
        `【参考文稿】${{day.src}}`,
        day.sourceUrl ? `【原文链接】${{day.sourceUrl}}` : ``,
        `【今日小角色】${{day.roles}}`,
        `【今天签到】${{day.signin}}`,
        `【今天 1 分钟】${{day.minute}}`,
        `【5 个可以聊的话题】`,
        ...day.topics.map((topic, index) => `${{index + 1}}. ${{topic}}`),
        `【群里互动小游戏】${{day.game}}`,
        `【今天小作业】${{day.homework}}`,
        `【教练收口】今天不用做完美小孩，只要完成一个小动作。完成的人在群里发“我完成了”，没完成的人也可以发“我明天继续”，我们看见每一点真实的努力。`
      ].join("\\n");
    }}

    function render() {{
      const theme = DATA[currentTheme];
      const day = theme.days[currentDay];
      themeTitle.textContent = theme.subtitle;
      themeCore.textContent = theme.core;
      status.textContent = `${{theme.subtitle}} · 第 ${{currentDay + 1}} 天`;
      message.innerHTML = `
        <h2>第 ${{currentDay + 1}} 天  ${{escapeHtml(day.title)}}</h2>
        <div class="source source-line">
          <span>参考文稿：${{escapeHtml(day.src)}}</span>
          ${{day.sourceUrl ? `<a class="source-link" href="${{escapeHtml(day.sourceUrl)}}" target="_blank" rel="noopener">去听原文</a>` : ""}}
        </div>
        ${{section("roles", "今日小角色", day.roles)}}
        ${{section("signin", "今天签到", day.signin)}}
        ${{section("minute", "今天 1 分钟", day.minute)}}
        <div class="section">
          <div class="section-head"><div class="section-title">5 个可以聊的话题</div><button class="copy-section-btn" data-copy-key="topics">复制</button></div>
          <ol>${{day.topics.map(t => `<li>${{escapeHtml(t)}}</li>`).join("")}}</ol>
        </div>
        ${{section("game", "群里互动小游戏", day.game)}}
        ${{section("homework", "今天小作业", day.homework)}}
        ${{section("closing", "教练收口", "今天不用做完美小孩，只要完成一个小动作。完成的人在群里发“我完成了”，没完成的人也可以发“我明天继续”，我们看见每一点真实的努力。")}}
      `;
      message.querySelectorAll("[data-copy-key]").forEach(button => {{
        button.addEventListener("click", () => copySection(button.dataset.copyKey));
      }});
      [...dayButtons.children].forEach((button, index) => button.classList.toggle("active", index === currentDay));
      [...dayList.children].forEach((button, index) => button.classList.toggle("active", index === currentDay));
    }}

    function section(key, title, body) {{
      return `<div class="section"><div class="section-head"><div class="section-title">${{title}}</div><button class="copy-section-btn" data-copy-key="${{key}}">复制</button></div><div>${{escapeHtml(body)}}</div></div>`;
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
      }}[char]));
    }}

    async function copyText(text) {{
      let copied = false;
      if (navigator.clipboard && window.isSecureContext) {{
        try {{
          await navigator.clipboard.writeText(text);
          copied = true;
        }} catch (error) {{
          copied = false;
        }}
      }}
      if (!copied) {{
        const helper = document.createElement("textarea");
        helper.value = text;
        helper.setAttribute("readonly", "");
        helper.style.position = "fixed";
        helper.style.left = "-9999px";
        document.body.appendChild(helper);
        helper.select();
        copied = document.execCommand("copy");
        document.body.removeChild(helper);
      }}
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 1000);
    }}

    function copyPart(kind) {{
      const day = DATA[currentTheme].days[currentDay];
      const number = currentDay + 1;
      const parts = {{
        full: dayText(day, number),
        signin: `【今天签到】${{day.signin}}`,
        game: `【群里互动小游戏】${{day.game}}`,
        homework: `【今天小作业】${{day.homework}}`
      }};
      copyText(parts[kind]);
    }}

    function moduleText(day, key) {{
      const closing = "今天不用做完美小孩，只要完成一个小动作。完成的人在群里发“我完成了”，没完成的人也可以发“我明天继续”，我们看见每一点真实的努力。";
      const parts = {{
        roles: `【今日小角色】${{day.roles}}`,
        signin: `【今天签到】${{day.signin}}`,
        minute: `【今天 1 分钟】${{day.minute}}`,
        topics: [`【5 个可以聊的话题】`, ...day.topics.map((topic, index) => `${{index + 1}}. ${{topic}}`)].join("\\n"),
        game: `【群里互动小游戏】${{day.game}}`,
        homework: `【今天小作业】${{day.homework}}`,
        closing: `【教练收口】${{closing}}`
      }};
      return parts[key];
    }}

    function copySection(key) {{
      const day = DATA[currentTheme].days[currentDay];
      copyText(moduleText(day, key));
    }}

    DATA.forEach((theme, index) => {{
      const option = document.createElement("option");
      option.value = index;
      option.textContent = theme.subtitle;
      themeSelect.appendChild(option);
    }});

    for (let i = 0; i < 14; i++) {{
      const button = document.createElement("button");
      button.className = "day-btn";
      button.textContent = i + 1;
      button.addEventListener("click", () => {{
        currentDay = i;
        render();
      }});
      dayButtons.appendChild(button);
    }}

    function renderDayList() {{
      dayList.innerHTML = "";
      DATA[currentTheme].days.forEach((day, index) => {{
        const button = document.createElement("button");
        button.className = "mini-day";
        button.textContent = `第 ${{index + 1}} 天：${{day.title}}`;
        button.addEventListener("click", () => {{
          currentDay = index;
          render();
        }});
        dayList.appendChild(button);
      }});
    }}

    themeSelect.addEventListener("change", event => {{
      currentTheme = Number(event.target.value);
      currentDay = 0;
      renderDayList();
      render();
    }});
    document.querySelector("#copyFull").addEventListener("click", () => copyPart("full"));
    document.querySelector("#copySignin").addEventListener("click", () => copyPart("signin"));
    document.querySelector("#copyGame").addEventListener("click", () => copyPart("game"));
    document.querySelector("#copyHomework").addEventListener("click", () => copyPart("homework"));

    renderDayList();
    render();
  </script>
</body>
</html>
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    render()
