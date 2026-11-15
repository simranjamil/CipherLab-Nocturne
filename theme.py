"""Dark navy + purple look for CipherLab (CSS and small HTML components)."""

import html

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
:root{
  --bg:#070B1A; --navy:#0C1233; --panel:rgba(17,23,56,.78); --panel-solid:#111838;
  --line:rgba(139,92,246,.26); --line-soft:rgba(148,163,255,.14);
  --p:#8B5CF6; --p2:#A78BFA; --p3:#C4B5FD; --text:#E8EAF8; --muted:#8E96C0;
  --good:#34D399; --bad:#FB7185; --warn:#FBBF24;
}
.stApp{
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  color:var(--text);
  background:
    radial-gradient(1100px 520px at 6% -8%, rgba(139,92,246,.22), transparent 60%),
    radial-gradient(900px 480px at 100% 0%, rgba(56,76,200,.24), transparent 58%),
    radial-gradient(900px 520px at 50% 115%, rgba(109,40,217,.16), transparent 60%),
    var(--bg);
}
[data-testid="stHeader"]{background:transparent;}
footer{visibility:hidden;}
.block-container{padding-top:2.2rem;padding-bottom:4rem;max-width:1200px;}
h1,h2,h3,h4{letter-spacing:-.01em;color:#F3F4FF;font-family:'Inter',system-ui,sans-serif;}
h3{margin-top:1.6rem;}
p,li,label,.stMarkdown{color:var(--text);}
[data-testid="stCaptionContainer"],small{color:var(--muted)!important;}
code,pre,[data-testid="stCode"] *{font-family:'JetBrains Mono',ui-monospace,Consolas,monospace!important;}
pre{background:rgba(7,10,30,.85)!important;border:1px solid var(--line-soft);border-radius:14px!important;}
code{color:var(--p3);}
::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:rgba(139,92,246,.35);border-radius:10px;}
::-webkit-scrollbar-track{background:transparent;}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0B1030 0%,#080C24 100%);
  border-right:1px solid var(--line);
}
[data-testid="stSidebar"] .block-container{padding-top:1rem;}
.nt-brand{display:flex;align-items:center;gap:12px;padding:6px 4px 14px;}
.nt-brand svg{width:38px;height:38px;filter:drop-shadow(0 4px 14px rgba(139,92,246,.6));}
.nt-brand b{display:block;font-size:1.25rem;font-weight:800;letter-spacing:-.02em;color:#fff;line-height:1.1;}
.nt-brand span{font-size:.68rem;letter-spacing:.16em;color:var(--muted);text-transform:uppercase;}
.nt-sep{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);margin:14px 0;}
[data-testid="stSidebar"] [role="radiogroup"]{gap:4px;}
[data-testid="stSidebar"] [role="radiogroup"] label{
  padding:10px 14px;border-radius:12px;border:1px solid transparent;transition:.15s;width:100%;cursor:pointer;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(139,92,246,.10);}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){
  background:linear-gradient(135deg,rgba(124,58,237,.32),rgba(79,70,229,.16));
  border-color:var(--line);box-shadow:0 4px 18px rgba(124,58,237,.18);
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child{display:none;}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-weight:600;font-size:.95rem;}

/* ---------- inputs ---------- */
div[data-baseweb="input"],div[data-baseweb="textarea"],div[data-baseweb="select"]>div{
  background:rgba(8,12,34,.9)!important;border:1px solid var(--line-soft)!important;border-radius:12px!important;
}
div[data-baseweb="input"]:focus-within,div[data-baseweb="textarea"]:focus-within{
  border-color:var(--p)!important;box-shadow:0 0 0 3px rgba(139,92,246,.25)!important;
}
.stTextInput input,.stTextArea textarea,.stNumberInput input{
  color:var(--text)!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:.92rem;
}
.stTextInput label,.stTextArea label,.stSelectbox label,.stRadio>label,.stSlider label,.stNumberInput label{
  font-weight:600;color:var(--p3)!important;
}

/* ---------- buttons ---------- */
.stButton>button,.stDownloadButton>button{
  width:100%;min-height:46px;border:0;border-radius:12px;font-weight:700;color:#fff;letter-spacing:.01em;
  background:linear-gradient(135deg,#7C3AED 0%,#8B5CF6 48%,#6366F1 100%);
  box-shadow:0 8px 24px rgba(124,58,237,.35);transition:all .18s ease;
}
.stButton>button:hover,.stDownloadButton>button:hover{
  transform:translateY(-1px);color:#fff;border:0;
  box-shadow:0 12px 32px rgba(139,92,246,.55);filter:brightness(1.08);
}
.stButton>button:active,.stDownloadButton>button:active{transform:translateY(0);}
.stButton>button p,.stDownloadButton>button p{color:#fff;}

/* ---------- tabs, expanders, tables, alerts ---------- */
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line-soft);}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:10px 10px 0 0;color:var(--muted);padding:10px 18px;font-weight:600;}
.stTabs [aria-selected="true"]{color:#fff;background:rgba(139,92,246,.14);}
.stTabs [data-baseweb="tab-highlight"]{background:linear-gradient(90deg,#8B5CF6,#C026D3);height:3px;}
[data-testid="stExpander"]{border:1px solid var(--line-soft)!important;border-radius:14px!important;background:rgba(17,23,56,.5);}
[data-testid="stDataFrame"]{border:1px solid var(--line-soft);border-radius:14px;overflow:hidden;}
[data-testid="stAlert"]{border-radius:14px;border:1px solid var(--line-soft);}
[data-testid="stMetric"]{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:14px 18px;}
[data-testid="stMetricLabel"] p{color:var(--muted);}

/* ---------- components ---------- */
.nt-hero{
  position:relative;overflow:hidden;padding:36px 40px;border-radius:26px;border:1px solid var(--line);
  background:linear-gradient(135deg,rgba(124,58,237,.26),rgba(30,41,120,.38) 55%,rgba(11,16,48,.7));
  box-shadow:0 20px 60px rgba(4,6,30,.6);
}
.nt-hero:before{content:"";position:absolute;right:-90px;top:-90px;width:340px;height:340px;border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,.38),transparent 66%);}
.nt-hero:after{content:"";position:absolute;left:30%;bottom:-140px;width:420px;height:260px;border-radius:50%;
  background:radial-gradient(circle,rgba(56,76,200,.30),transparent 68%);}
.nt-hero>*{position:relative;z-index:1;}
.nt-kicker{display:inline-block;padding:5px 14px;border-radius:999px;font-size:.72rem;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--p3);background:rgba(139,92,246,.16);border:1px solid var(--line);}
.nt-hero h1{font-size:3rem;font-weight:800;margin:.55rem 0 .4rem;line-height:1.05;
  background:linear-gradient(90deg,#fff 0%,#DDD6FE 45%,#A78BFA 100%);-webkit-background-clip:text;background-clip:text;color:transparent;}
.nt-hero p{max-width:640px;color:#C7CCEE;font-size:1.02rem;line-height:1.6;margin:0;}
.nt-page-head{margin-bottom:1.1rem;}
.nt-eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--p2);}
.nt-page-head h1{font-size:2.1rem;font-weight:800;margin:.15rem 0 .2rem;color:#fff;}
.nt-page-head p{color:var(--muted);margin:0;}
.nt-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0 6px;}
.nt-stat{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:16px 20px;backdrop-filter:blur(8px);}
.nt-stat span{display:block;font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);}
.nt-stat b{display:block;font-size:1.9rem;font-weight:800;color:#fff;margin:2px 0;}
.nt-stat i{font-style:normal;font-size:.8rem;color:var(--p3);}
.nt-pipe{display:flex;align-items:stretch;gap:10px;flex-wrap:wrap;margin:10px 0 6px;}
.nt-node{flex:1 1 150px;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:16px 18px;min-width:140px;}
.nt-node span{display:block;font-size:.66rem;font-weight:700;letter-spacing:.16em;color:var(--p2);}
.nt-node b{display:block;font-size:1.05rem;color:#fff;margin:4px 0 2px;}
.nt-node em{font-style:normal;font-size:.8rem;color:var(--muted);line-height:1.4;}
.nt-node.nt-io{flex:0 1 120px;background:rgba(8,12,34,.75);border-style:dashed;}
.nt-node.nt-sealed{background:linear-gradient(135deg,rgba(124,58,237,.14),rgba(17,23,56,.8));}
.nt-node.nt-sealed b{letter-spacing:.3em;color:var(--p3);}
.nt-arrow{display:flex;align-items:center;font-size:1.8rem;color:var(--p);font-weight:300;}
.nt-card{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:20px 24px;backdrop-filter:blur(8px);
  box-shadow:0 10px 40px rgba(2,4,20,.45);height:100%;}
.nt-card h4{margin:0 0 10px;font-size:1.05rem;color:#fff;}
.nt-chip{display:inline-block;padding:4px 12px;border-radius:999px;font-size:.78rem;font-weight:600;margin:2px 6px 2px 0;
  border:1px solid var(--line);background:rgba(139,92,246,.14);color:var(--p3);}
.nt-chip.ok{background:rgba(52,211,153,.12);border-color:rgba(52,211,153,.35);color:var(--good);}
.nt-chip.bad{background:rgba(251,113,133,.12);border-color:rgba(251,113,133,.35);color:var(--bad);}
.nt-chip.warn{background:rgba(251,191,36,.10);border-color:rgba(251,191,36,.35);color:var(--warn);}
.nt-check{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--line-soft);}
.nt-check:last-child{border-bottom:0;}
.nt-check .n{flex:0 0 28px;height:28px;border-radius:9px;background:rgba(139,92,246,.18);color:var(--p3);font-weight:700;
  display:flex;align-items:center;justify-content:center;font-size:.85rem;}
.nt-check .t{flex:1;font-size:.93rem;color:var(--text);}
.nt-check .t small{display:block;color:var(--muted)!important;font-size:.78rem;margin-top:1px;}
.nt-lock{text-align:center;padding:48px 24px;border-radius:24px;border:1px dashed var(--line);
  background:linear-gradient(135deg,rgba(124,58,237,.10),rgba(17,23,56,.7));}
.nt-lock .big{font-size:3rem;}
.nt-lock h3{margin:.4rem 0;color:#fff;}
.nt-lock p{color:var(--muted);max-width:520px;margin:0 auto;}
.nt-out{background:rgba(7,10,30,.85);border:1px solid var(--line);border-radius:16px;padding:16px 20px;
  font-family:'JetBrains Mono',monospace;font-size:1.02rem;letter-spacing:.12em;word-break:break-all;color:var(--p3);line-height:1.9;}
.nt-out .g{display:inline-block;margin-right:.7em;}
.nt-matrix{display:grid;gap:6px;margin:6px 0 4px;max-width:340px;}
.nt-cell{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;border-radius:10px;
  background:rgba(139,92,246,.14);border:1px solid var(--line);font-family:'JetBrains Mono',monospace;font-weight:600;color:#fff;font-size:.95rem;}
.nt-cell.dim{color:var(--p3);background:rgba(17,23,56,.8);}
.nt-note{font-size:.82rem;color:var(--muted);}
[data-testid="stWidgetLabel"] p{color:var(--p3)!important;font-weight:600;}
[data-testid="stAppDeployButton"],.stDeployButton{display:none!important;}
.nt-table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--line-soft);border-radius:14px;overflow:hidden;background:rgba(10,14,40,.7);}
.nt-table th{text-align:left;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--p2);padding:10px 14px;
  background:rgba(139,92,246,.10);border-bottom:1px solid var(--line-soft);}
.nt-table td{padding:10px 14px;border-bottom:1px solid var(--line-soft);font-family:'JetBrains Mono',monospace;font-size:.8rem;
  color:var(--text);word-break:break-all;vertical-align:top;line-height:1.5;}
.nt-table tr:last-child td{border-bottom:0;}
.nt-table td.n{width:52px;color:var(--p3);font-weight:600;}
.nt-table td.ct{color:var(--p3);}
@media (max-width:900px){.nt-stats{grid-template-columns:repeat(2,1fr);} .nt-hero h1{font-size:2.2rem;}}
</style>
"""

LOGO_SVG = (
    '<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="ntg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#C4B5FD"/><stop offset="1" stop-color="#6366F1"/></linearGradient></defs>'
    '<rect x="2" y="2" width="36" height="36" rx="11" fill="#12183F" stroke="url(#ntg)" stroke-width="1.6"/>'
    '<path d="M25.5 26.5A9.5 9.5 0 1 1 17 12.2a7.4 7.4 0 0 0 8.5 14.3z" fill="url(#ntg)"/>'
    '</svg>'
)


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def _e(text):
    return html.escape(str(text))


def brand(name, subtitle):
    st.markdown(
        f'<div class="nt-brand">{LOGO_SVG}<div><b>{_e(name)}</b><span>{_e(subtitle)}</span></div></div>',
        unsafe_allow_html=True,
    )


def sep():
    st.markdown('<div class="nt-sep"></div>', unsafe_allow_html=True)


def page_header(eyebrow, title, caption):
    st.markdown(
        f'<div class="nt-page-head"><div class="nt-eyebrow">{_e(eyebrow)}</div>'
        f'<h1>{_e(title)}</h1><p>{_e(caption)}</p></div>',
        unsafe_allow_html=True,
    )


def hero(kicker, title, text):
    st.markdown(
        f'<div class="nt-hero"><span class="nt-kicker">{_e(kicker)}</span>'
        f'<h1>{_e(title)}</h1><p>{_e(text)}</p></div>',
        unsafe_allow_html=True,
    )


def stats(items):
    cells = "".join(
        f'<div class="nt-stat"><span>{_e(label)}</span><b>{_e(value)}</b><i>{_e(sub)}</i></div>'
        for label, value, sub in items
    )
    st.markdown(f'<div class="nt-stats">{cells}</div>', unsafe_allow_html=True)


def pipeline(stages, sealed):
    parts = ['<div class="nt-pipe"><div class="nt-node nt-io"><span>INPUT</span><b>Plaintext</b></div>']
    for i, (name, desc) in enumerate(stages, 1):
        parts.append('<div class="nt-arrow">›</div>')
        if sealed:
            parts.append(
                f'<div class="nt-node nt-sealed"><span>STAGE {i}</span><b>● ● ● ●</b><em>🔒 sealed</em></div>'
            )
        else:
            parts.append(
                f'<div class="nt-node"><span>STAGE {i}</span><b>{_e(name)}</b><em>{_e(desc)}</em></div>'
            )
    parts.append('<div class="nt-arrow">›</div><div class="nt-node nt-io"><span>OUTPUT</span><b>Ciphertext</b></div></div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def chip(text, kind=""):
    return f'<span class="nt-chip {kind}">{_e(text)}</span>'


def chips(items):
    """items: list of (text, kind)."""
    st.markdown("".join(chip(t, k) for t, k in items), unsafe_allow_html=True)


def checklist(rows):
    """rows: list of (number, title, where, status_text, status_kind)."""
    body = "".join(
        f'<div class="nt-check"><div class="n">{n}</div><div class="t">{_e(title)}<small>{_e(where)}</small></div>'
        f'{chip(status, kind)}</div>'
        for n, title, where, status, kind in rows
    )
    st.markdown(f'<div class="nt-card"><h4>Blue Team deliverables</h4>{body}</div>', unsafe_allow_html=True)


def card(title, body):
    st.markdown(
        f'<div class="nt-card"><h4>{_e(title)}</h4><div class="nt-note">{_e(body)}</div></div>',
        unsafe_allow_html=True,
    )


def lock_card(title, text):
    st.markdown(
        f'<div class="nt-lock"><div class="big">🔒</div><h3>{_e(title)}</h3><p>{_e(text)}</p></div>',
        unsafe_allow_html=True,
    )


def cipher_blocks(text, group=5):
    groups = "".join(f'<span class="g">{_e(text[i:i + group])}</span>' for i in range(0, len(text), group))
    st.markdown(f'<div class="nt-out">{groups}</div>', unsafe_allow_html=True)


def pairs_table(rows):
    """rows: list of (number, plaintext, ciphertext) shown as a wrapped monospace table."""
    body = "".join(
        f'<tr><td class="n">{_e(n)}</td><td>{_e(p)}</td><td class="ct">{_e(c)}</td></tr>' for n, p, c in rows
    )
    st.markdown(
        '<table class="nt-table"><thead><tr><th>Pair</th><th>Plaintext</th><th>Ciphertext</th></tr></thead>'
        f'<tbody>{body}</tbody></table>',
        unsafe_allow_html=True,
    )


def matrix(rows, dim=False):
    n = len(rows[0])
    cls = "nt-cell dim" if dim else "nt-cell"
    cells = "".join(f'<div class="{cls}">{_e(v)}</div>' for row in rows for v in row)
    st.markdown(
        f'<div class="nt-matrix" style="grid-template-columns:repeat({n},1fr)">{cells}</div>',
        unsafe_allow_html=True,
    )
