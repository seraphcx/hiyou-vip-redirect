# -*- coding: utf-8 -*-
"""
官网课程页装配脚本（跑一次即可，重复跑是幂等的）

做两件事：
1) 给 index.html 的导航加一个「课程」入口
2) 生成 courses.html —— 整份 CSS 直接继承 index.html，所以视觉绝不跑偏；
   只在其后追加一小段课程卡片专用的补充样式。

课程文件 course-parent.html 需要另行从
  261012家长课程/_publish/course-parent.html
复制（或本脚本在你放好之后就不再管它）。
"""
import io
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(ROOT, "index.html")
OUT = os.path.join(ROOT, "courses.html")
SRC_COURSE = os.path.join(
    os.path.dirname(ROOT), "261012家长课程", "_publish", "course-parent.html")

src = io.open(IDX, encoding="utf-8").read()

# ── 1) 首页加「课程」导航 ────────────────────────────────────
NAV_NEW = '        <a href="courses.html">课程</a>\n'
NAV_ANCHOR = '        <a href="#contact">联系我</a>\n'
if 'href="courses.html"' in src:
    print("· index.html 已有「课程」入口，跳过")
else:
    if NAV_ANCHOR not in src:
        raise SystemExit("没找到「联系我」导航项，index.html 结构可能变了，请人工确认")
    src = src.replace(NAV_ANCHOR, NAV_NEW + NAV_ANCHOR, 1)
    with io.open(IDX, "w", encoding="utf-8") as f:
        f.write(src)
    print("✓ index.html 已加入「课程」导航入口")

# ── 2) 抽出首页的整份 head（含全部 CSS 与 CSP）─────────────
head = src.split("<head>", 1)[1].split("</head>", 1)[0]
head = head.replace("<title>赵星｜自我介绍</title>",
                    "<title>课程｜星星老师</title>")

EXTRA_CSS = """
    /* ── 课程页补充样式（其余全部继承首页） ─────────── */
    .nav a.is-current { color: #fffaf1; background: var(--navy); }
    .nav a.is-current:hover,
    .nav a.is-current:focus-visible { color: #fffaf1; background: var(--navy); }
    .course-list { display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
    .course-card { position: relative; background: var(--white);
      border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 24px;
      box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 8px; }
    .course-card .lock { width: 38px; height: 38px; border-radius: 50%; background: var(--navy);
      display: grid; place-items: center; margin-bottom: 6px; }
    .course-card .lock svg { width: 19px; height: 19px; }
    .course-card b { color: var(--orange); font-size: .82rem; letter-spacing: .08em; font-weight: 950; }
    .course-card h3 { margin: 0; color: var(--navy); font-size: 1.32rem; font-weight: 950; line-height: 1.35; }
    .course-card p { margin: 0; color: var(--muted); font-size: .95rem; line-height: 1.75; }
    .course-card .go { margin-top: auto; padding-top: 16px; }
    .course-meta { font-size: .82rem !important; color: var(--olive) !important; }
    .course-note { font-size: .82rem !important; }
    .back-home { display: inline-block; margin-top: 26px; font-weight: 800; }
"""
head = head.replace("  </style>", EXTRA_CSS + "  </style>")

BODY = """<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <span class="brand-mark" aria-hidden="true"></span>
        <span>星星老师</span>
      </div>
      <nav class="nav" aria-label="页面导航">
        <a href="index.html#story">我是谁</a>
        <a href="index.html#path">经历路径</a>
        <a href="index.html#human">HUMAN</a>
        <a href="index.html#projects">现在在做</a>
        <a href="index.html#value">我能带来</a>
        <a href="courses.html" class="is-current" aria-current="page">课程</a>
        <a href="index.html#contact">联系我</a>
      </nav>
    </div>
  </header>

  <section id="courses" class="reveal">
    <div class="section-head">
      <div>
        <div class="section-kicker">课程</div>
        <h2>已上线的课程。</h2>
        <p>
          这里的课程不是录播视频，而是可以一边读一边动手的互动页面：每一步都给出处，
          每一讲都留下「今晚就能做的一件事」。目前开放一门给家长的课。
        </p>
      </div>
    </div>

    <div class="course-list">
      <article class="course-card">
        <span class="lock" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none">
          <rect x="4" y="10.5" width="16" height="10.5" rx="2.4" fill="#F8EFDA"></rect>
          <path d="M8 10.5V7.8a4 4 0 1 1 8 0v2.7" stroke="#F8EFDA" stroke-width="2" stroke-linecap="round"></path>
          <circle cx="12" cy="15.6" r="1.5" fill="#E95A2A"></circle></svg></span>
        <b>家长课 · 2026</b>
        <h3>孩子是不是一个人？</h3>
        <p>
          给走中高考这条路的家长。八讲：从一个两万年没换过说明书的大脑，到这台筛选机器怎么运转，
          再到你今晚就能做的四步。全部论点与数据都给出处，可逐条核查。
        </p>
        <p class="course-meta">约 40 分钟读完 · 11 个互动组件 · 34 条理论依据</p>
        <div class="go"><a class="primary-link" href="course-parent.html">用账号进入 →</a></div>
        <p class="course-note">本课程内容已加密，需要用户名与密码；账号由星星老师发放。</p>
      </article>
    </div>

    <p class="back-home"><a href="index.html">← 回到首页</a></p>
  </section>

  <script>
    (function () {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      document.querySelectorAll(".reveal").forEach(function (n) { observer.observe(n); });
    })();
  </script>
</body>
</html>
"""

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("<!doctype html>\n<html lang=\"zh-CN\">\n<head>" + head + "</head>\n" + BODY)
print("✓ 已生成", OUT, os.path.getsize(OUT), "bytes")

# ── 3) 把加密课件搬进网站目录 ────────────────────────────────
if os.path.exists(SRC_COURSE):
    dst = os.path.join(ROOT, "course-parent.html")
    shutil.copy2(SRC_COURSE, dst)
    print("✓ 已复制加密课件 ->", dst, os.path.getsize(dst), "bytes")
else:
    print("! 找不到加密课件：", SRC_COURSE)
