"""
VentureAI - Business Intelligence Platform
Single-file Streamlit app powered by Ollama.

SETUP:
    pip install streamlit requests
    ollama pull llama3.2        (or any model)
    ollama serve                (run in a separate terminal)
    streamlit run venture_ai.py
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VentureAI - Business Advisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Embedded CSS ──────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
:root{--blk:#080808;--blk2:#101010;--blk3:#181818;--blk4:#202020;
  --ylw:#FFD700;--ylw2:#FFC200;--ydim:rgba(255,215,0,.10);--yglow:rgba(255,215,0,.05);
  --wht:#F5F5F5;--wdim:rgba(245,245,245,.65);
  --bdr:rgba(255,215,0,.20);--bdrd:rgba(255,255,255,.07);
  --grn:#22C55E;--red:#EF4444;}
.stApp{background:var(--blk)!important;color:var(--wht)!important;font-family:'DM Sans',sans-serif!important;}
.main .block-container{padding:1.5rem 2rem 5rem!important;max-width:1180px;}
section[data-testid="stSidebar"]{background:var(--blk2)!important;border-right:1px solid var(--bdr)!important;}
section[data-testid="stSidebar"]>div{padding:0!important;}
.vlogo{padding:1.8rem 1.5rem 1.4rem;text-align:center;border-bottom:1px solid var(--bdrd);}
.vlogo-icon{font-size:2.4rem;filter:drop-shadow(0 0 14px rgba(255,215,0,.55));}
.vlogo-text{font-family:'Bebas Neue',sans-serif;font-size:2.1rem;letter-spacing:5px;color:var(--ylw);line-height:1;margin-top:.2rem;}
.vlogo-sub{font-size:.58rem;letter-spacing:2.5px;text-transform:uppercase;color:rgba(245,245,245,.35);margin-top:.25rem;}
.vstatus{display:flex;align-items:center;gap:.5rem;margin:.8rem 1rem;padding:.45rem .9rem;border-radius:6px;font-size:.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.vonline{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);color:var(--grn);}
.voffline{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);color:var(--red);}
.vdot{width:6px;height:6px;border-radius:50%;background:currentColor;animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
.vsec{padding:.6rem 1.5rem .25rem;font-size:.62rem;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,215,0,.45);font-weight:700;}
section[data-testid="stSidebar"] .stButton>button{background:transparent!important;border:1px solid var(--bdrd)!important;color:var(--wdim)!important;border-radius:7px!important;font-size:.83rem!important;font-weight:500!important;padding:.52rem .9rem!important;text-align:left!important;transition:all .18s ease!important;margin:.12rem .9rem!important;width:calc(100% - 1.8rem)!important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:var(--ydim)!important;border-color:var(--bdr)!important;color:var(--ylw)!important;transform:translateX(4px)!important;}
.vstats{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;padding:.4rem 1rem;}
.vstat{background:var(--yglow);border:1px solid var(--bdrd);border-radius:8px;padding:.7rem .4rem;text-align:center;}
.vstatn{font-family:'Bebas Neue',sans-serif;font-size:1.9rem;color:var(--ylw);line-height:1;}
.vstatl{font-size:.58rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--wdim);margin-top:.15rem;}
.vfoot{padding:.9rem 1.5rem;font-size:.62rem;color:rgba(245,245,245,.25);text-align:center;line-height:1.8;border-top:1px solid var(--bdrd);margin-top:.8rem;}
.vheader{display:flex;align-items:center;gap:1.2rem;padding:1.4rem 1.8rem;margin-bottom:1.8rem;background:linear-gradient(135deg,var(--blk3),var(--blk2));border:1px solid var(--bdr);border-radius:12px;position:relative;overflow:hidden;}
.vheader::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--ylw),transparent);}
.vhicon{font-size:2.4rem;filter:drop-shadow(0 0 8px rgba(255,215,0,.35));}
.vhtitle{font-family:'Bebas Neue',sans-serif!important;font-size:1.95rem!important;letter-spacing:3.5px!important;color:var(--wht)!important;margin:0!important;padding:0!important;line-height:1.05!important;}
.vhsub{font-size:.8rem!important;color:var(--wdim)!important;margin:.25rem 0 0!important;}
.vhdate{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--ylw);opacity:.6;letter-spacing:1px;white-space:nowrap;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--blk3)!important;border:1px solid var(--bdrd)!important;border-radius:8px!important;color:var(--wht)!important;font-family:'DM Sans',sans-serif!important;font-size:.87rem!important;transition:border-color .18s!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:var(--ylw)!important;box-shadow:0 0 0 1px rgba(255,215,0,.18)!important;}
.stSelectbox>div>div{background:var(--blk3)!important;border:1px solid var(--bdrd)!important;border-radius:8px!important;color:var(--wht)!important;}
.stSelectbox>div>div:hover{border-color:var(--ylw)!important;}
.stTextInput label,.stTextArea label,.stSelectbox label,.stSlider label,.stNumberInput label{color:var(--wdim)!important;font-size:.76rem!important;font-weight:600!important;letter-spacing:.6px!important;text-transform:uppercase!important;}
.stButton>button[kind="primary"]{background:var(--ylw)!important;color:var(--blk)!important;border:none!important;border-radius:8px!important;font-weight:700!important;font-size:.85rem!important;letter-spacing:1.2px!important;text-transform:uppercase!important;padding:.65rem 1.4rem!important;transition:all .18s ease!important;}
.stButton>button[kind="primary"]:hover{background:var(--ylw2)!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(255,215,0,.28)!important;}
.main .stButton>button:not([kind="primary"]){background:var(--blk3)!important;border:1px solid var(--bdrd)!important;color:var(--wdim)!important;border-radius:8px!important;font-size:.78rem!important;padding:.48rem .8rem!important;transition:all .18s!important;}
.main .stButton>button:not([kind="primary"]):hover{border-color:var(--bdr)!important;color:var(--ylw)!important;background:var(--ydim)!important;}
.stMarkdown h1,.stMarkdown h2{color:var(--ylw)!important;font-family:'Bebas Neue',sans-serif!important;letter-spacing:2.5px!important;}
.stMarkdown h3{color:var(--wht)!important;font-weight:700!important;}
.stMarkdown strong{color:var(--ylw)!important;}
.stMarkdown code{background:var(--blk4)!important;color:var(--ylw)!important;font-family:'JetBrains Mono',monospace!important;border-radius:4px!important;padding:.1em .4em!important;font-size:.83em!important;}
.stMarkdown blockquote{border-left:3px solid var(--ylw)!important;background:var(--yglow)!important;padding:.7rem 1rem!important;border-radius:0 6px 6px 0!important;margin:.7rem 0!important;}
.vchatintro{background:var(--yglow);border:1px solid var(--bdr);border-radius:10px;padding:.9rem 1.2rem;font-size:.86rem;color:var(--wdim);margin-bottom:1.2rem;line-height:1.65;}
.vmsg{margin:.7rem 0;padding:.95rem 1.2rem;border-radius:10px;line-height:1.65;font-size:.87rem;}
.vuser{background:var(--ydim);border:1px solid var(--bdr);border-left:3px solid var(--ylw);}
.vai{background:var(--blk3);border:1px solid var(--bdrd);border-left:3px solid rgba(245,245,245,.15);}
.vmsglbl{font-size:.62rem;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:.35rem;color:var(--wdim);}
.vuser .vmsglbl{color:var(--ylw);}
.vmsgbody{color:var(--wht);white-space:pre-wrap;}
.vpagefoot{display:flex;justify-content:space-between;align-items:center;padding:1rem 0;margin-top:3rem;border-top:1px solid var(--bdrd);font-size:.62rem;letter-spacing:.8px;color:rgba(245,245,245,.22);text-transform:uppercase;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--blk2);}
::-webkit-scrollbar-thumb{background:rgba(255,215,0,.28);border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:var(--ylw);}
.stNumberInput>div>div>input{background:var(--blk3)!important;border:1px solid var(--bdrd)!important;color:var(--wht)!important;border-radius:8px!important;}
.stChatInput>div{background:var(--blk3)!important;border:1px solid var(--bdr)!important;border-radius:10px!important;}
.stChatInput input{color:var(--wht)!important;background:transparent!important;}
hr{border-color:var(--bdrd)!important;}
p,li{color:var(--wdim);}
.diagbox{background:#110d00;border:1px solid #ffd70055;border-radius:10px;padding:1rem 1.2rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#FFD700;margin:.5rem 1rem;line-height:1.8;}
.tip-box{background:var(--yglow);border:1px solid var(--bdr);border-radius:8px;padding:.7rem 1rem;font-size:.78rem;color:var(--wdim);margin-bottom:1rem;}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
OLLAMA_BASE   = "http://localhost:11434"
OLLAMA_GEN    = f"{OLLAMA_BASE}/api/generate"
OLLAMA_TAGS   = f"{OLLAMA_BASE}/api/tags"
DEFAULT_MODEL = "llama3.2"

# Recommended fast models in order of preference
FAST_MODELS = ["phi3", "phi3:mini", "gemma2:2b", "gemma:2b", "tinyllama", "llama3.2:1b", "llama3.2", "mistral"]

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in [("chat_history", []), ("current_mode", "startup_ideas"),
              ("generated_content", {}), ("model", DEFAULT_MODEL)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Ollama Helpers ────────────────────────────────────────────────────────────
def check_ollama():
    try:
        return requests.get(OLLAMA_TAGS, timeout=4).status_code == 200
    except Exception:
        return False

def get_models():
    try:
        data  = requests.get(OLLAMA_TAGS, timeout=4).json()
        names = [m["name"] for m in data.get("models", [])]
        # Sort: put known fast models first
        def sort_key(n):
            for i, fm in enumerate(FAST_MODELS):
                if n.startswith(fm):
                    return i
            return 99
        names.sort(key=sort_key)
        return names if names else [DEFAULT_MODEL]
    except Exception:
        return [DEFAULT_MODEL]

def stream_ollama(prompt: str, system: str = ""):
    """
    Proper streaming generator for st.write_stream().
    Yields text chunks as they arrive from Ollama.
    Falls back to a clear error string on failure.
    """
    combined = f"{system}\n\n{prompt}" if system else prompt
    payload  = {
        "model":   st.session_state.model,
        "prompt":  combined,
        "stream":  True,
        "options": {
            "num_predict": 1024,   # cap tokens so it doesn't run forever
            "temperature": 0.7,
        },
    }
    try:
        with requests.post(OLLAMA_GEN, json=payload, stream=True, timeout=180) as r:
            r.raise_for_status()
            for raw_line in r.iter_lines():
                if raw_line:
                    try:
                        chunk = json.loads(raw_line).get("response", "")
                        if chunk:
                            yield chunk
                    except json.JSONDecodeError:
                        continue

    except requests.exceptions.ConnectionError:
        yield (
            "\n\n**Cannot connect to Ollama.**\n\n"
            "Open a terminal and run: `ollama serve`\n"
            "Then click the button again."
        )
    except requests.exceptions.Timeout:
        yield (
            "\n\n**Timeout.** Try a faster model.\n\n"
            "Run: `ollama pull phi3` then select **phi3** in the sidebar."
        )
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        body = e.response.text[:300]
        if code == 404:
            yield f"\n\n**Model `{st.session_state.model}` not found.**\n\nRun: `ollama pull {st.session_state.model}`"
        else:
            yield f"\n\n**HTTP {code} Error:** `{body}`"
    except Exception as e:
        yield f"\n\n**Error:** `{type(e).__name__}: {e}`"


def run_stream(prompt: str, system: str, label: str = "Response"):
    """Stream response into a Streamlit container using write_stream."""
    st.markdown(f"### {label}")
    # st.write_stream() handles the generator correctly — shows text as it arrives
    result = st.write_stream(stream_ollama(prompt, system))
    st.session_state.generated_content[f"result_{int(time.time())}"] = result


def call_ollama_sync(prompt: str, system: str = "") -> str:
    """Non-streaming call, used only for the chat module to get full text back."""
    return "".join(stream_ollama(prompt, system))


# ── System Prompts (kept SHORT to reduce token count & latency) ───────────────
SP = {
"startup_ideas": (
    "You are VentureAI, a startup advisor. Be concise and direct. "
    "For each idea: name, problem, solution, market, revenue model, key risks, estimated cost. "
    "Use markdown headers. Max 400 words per idea."
),
"market_analysis": (
    "You are VentureAI, a market analyst. Be concise. "
    "Cover: market size estimate, top 3 trends, top 3 competitors, target customers, entry strategy. "
    "Use markdown headers. Be specific with numbers. Max 600 words total."
),
"business_plan": (
    "You are VentureAI, a business plan consultant. Be concise. "
    "Write a structured plan: Executive Summary, Product, Market, Team, Revenue Model, "
    "Financial Projections (Year 1-3), Funding Ask. Use markdown. Max 700 words."
),
"pitch_deck": (
    "You are VentureAI, a pitch coach. Be concise. "
    "Outline each slide: title, 3 bullet points of key content. "
    "Include: Problem, Solution, Market, Traction, Team, Ask. Max 500 words."
),
"financial_model": (
    "You are VentureAI, a startup CFO. Be concise. "
    "Provide: revenue projections table (Year 1-3), unit economics (CAC/LTV/margin), "
    "break-even point, burn rate estimate. Use tables. Max 500 words."
),
"advisor_chat": (
    "You are VentureAI, a startup advisor. Give direct, actionable advice. "
    "Be concise — max 300 words. End with 3 concrete next steps."
),
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="vlogo">
      <div class="vlogo-icon">&#9889;</div>
      <div class="vlogo-text">VentureAI</div>
      <div class="vlogo-sub">Business Intelligence Platform</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    ollama_ok = check_ollama()
    cls = "vonline" if ollama_ok else "voffline"
    txt = "Ollama Connected" if ollama_ok else "Ollama Offline"
    st.markdown(f'<div class="vstatus {cls}"><span class="vdot"></span>{txt}</div>', unsafe_allow_html=True)

    if not ollama_ok:
        st.markdown("""
        <div class="diagbox">
        &#9888; OLLAMA NOT RUNNING<br><br>
        Open terminal and run:<br>
        <strong>ollama serve</strong>
        </div>""", unsafe_allow_html=True)

    models = get_models()
    st.session_state.model = st.selectbox("Model", models, index=0,
        help="Smaller models (phi3, gemma2:2b) are 3-5x faster than llama3.2")

    # Speed tip
    current = st.session_state.model
    is_fast = any(current.startswith(fm) for fm in FAST_MODELS[:5])
    if not is_fast and ollama_ok:
        st.markdown("""
        <div class="diagbox" style="font-size:.7rem;">
        &#9889; For faster responses:<br>
        <code>ollama pull phi3</code><br>
        Then select <strong>phi3</strong> above.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="vsec">Tools</div>', unsafe_allow_html=True)

    TOOLS = [
        ("startup_ideas",   "&#128161;  Startup Ideas"),
        ("market_analysis", "&#128202;  Market Analysis"),
        ("business_plan",   "&#128203;  Business Plan"),
        ("pitch_deck",      "&#127919;  Pitch Deck"),
        ("financial_model", "&#128176;  Financial Model"),
        ("advisor_chat",    "&#129504;  AI Advisor Chat"),
    ]
    for key, label in TOOLS:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.current_mode = key
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="vsec">Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="vstats">
      <div class="vstat"><div class="vstatn">{len(st.session_state.generated_content)}</div><div class="vstatl">Analyses</div></div>
      <div class="vstat"><div class="vstatn">{len(st.session_state.chat_history)}</div><div class="vstatl">Messages</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("&#128465;  Clear Session", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.generated_content = {}
        st.rerun()

    st.markdown("""
    <div class="vfoot">
      Powered by <strong>Ollama</strong> + <strong>Streamlit</strong><br>
      VentureAI &copy; 2026
    </div>""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
mode = st.session_state.current_mode
HEADERS = {
    "startup_ideas":   ("&#128161;", "Startup Idea Generator",  "Discover high-potential business opportunities tailored to your skills and market"),
    "market_analysis": ("&#128202;", "Market Analysis Engine",  "Deep-dive market research and competitive intelligence for your industry"),
    "business_plan":   ("&#128203;", "Business Plan Builder",   "Generate investor-ready business plans with professional structure"),
    "pitch_deck":      ("&#127919;", "Pitch Deck Advisor",      "Craft a compelling investor narrative that wins funding rounds"),
    "financial_model": ("&#128176;", "Financial Model Studio",  "Build realistic projections and understand your unit economics"),
    "advisor_chat":    ("&#129504;", "AI Advisor Chat",         "Your personal entrepreneurship advisor, available 24/7"),
}
icon, title, subtitle = HEADERS[mode]
st.markdown(f"""
<div class="vheader">
  <div class="vhicon">{icon}</div>
  <div>
    <div class="vhtitle">{title}</div>
    <div class="vhsub">{subtitle}</div>
  </div>
  <div class="vhdate">{datetime.now().strftime("%b %d, %Y")}</div>
</div>""", unsafe_allow_html=True)

if not ollama_ok:
    st.error("Ollama is not running. Open a terminal, run `ollama serve`, then click any button.")

# =============================================================================
# MODULE: STARTUP IDEAS
# =============================================================================
if mode == "startup_ideas":
    c1, c2 = st.columns(2)
    with c1:
        industry = st.selectbox("Industry / Sector", [
            "Technology & SaaS","FinTech","HealthTech","EdTech","E-Commerce",
            "Sustainability & CleanTech","FoodTech","Real Estate",
            "HR & Future of Work","AI & Automation","Consumer Goods",
            "Entertainment & Media","Logistics","Agriculture","Legal Tech","Other",
        ])
        skills = st.text_input("Your Skills / Expertise", placeholder="e.g. software dev, marketing, finance...")
    with c2:
        budget = st.selectbox("Startup Budget", [
            "Bootstrapped (< $10K)","Small ($10K-$50K)","Medium ($50K-$200K)","Funded ($200K+)",
        ])
        target = st.selectbox("Target Market", ["B2B","B2C","B2B2C","Government","Non-profit"])
    trend = st.text_input("Trend or Problem to Solve (optional)", placeholder="e.g. AI tools, mental health, logistics...")

    cg, cr = st.columns([3, 1])
    with cg: gen_btn = st.button("&#9889; Generate Startup Ideas", type="primary", use_container_width=True)
    with cr: rnd_btn = st.button("&#127922; Surprise Me", use_container_width=True)

    if gen_btn or rnd_btn:
        if rnd_btn:
            prompt = "Give 3 creative, unexpected startup ideas for underserved niches in 2025. Be specific and brief."
        else:
            prompt = (
                f"Give 3 startup ideas for:\n"
                f"Industry: {industry} | Skills: {skills or 'General'} | "
                f"Budget: {budget} | Market: {target} | Focus: {trend or 'open'}\n\n"
                "For each: name, problem, solution, market size, revenue model, first step."
            )
        run_stream(prompt, SP["startup_ideas"], label="Generated Startup Ideas")

# =============================================================================
# MODULE: MARKET ANALYSIS
# =============================================================================
elif mode == "market_analysis":
    c1, c2 = st.columns(2)
    with c1:
        biz = st.text_input("Business / Product", placeholder="e.g. Online tutoring platform for adults...")
        geo = st.selectbox("Target Geography", [
            "Global","North America","Europe","Asia-Pacific",
            "India","Southeast Asia","Latin America","Middle East & Africa",
        ])
    with c2:
        atype = st.selectbox("Analysis Type", [
            "Full Market Analysis","Competitive Landscape","Customer Segmentation",
            "Market Entry Strategy","TAM/SAM/SOM Sizing","SWOT Analysis",
        ])
        horizon = st.selectbox("Market Horizon", [
            "Current (2025)","1-2 years","3-5 years","5-10 years",
        ])
    comps = st.text_input("Known Competitors (optional)", placeholder="e.g. Coursera, Udemy...")

    if st.button("&#128202; Run Market Analysis", type="primary", use_container_width=True):
        if not biz:
            st.warning("Please enter a business or product to analyze.")
        else:
            prompt = (
                f"{atype} for: {biz}\n"
                f"Geography: {geo} | Horizon: {horizon} | "
                f"Competitors: {comps or 'identify top 3'}"
            )
            run_stream(prompt, SP["market_analysis"], label="Market Analysis Report")

# =============================================================================
# MODULE: BUSINESS PLAN
# =============================================================================
elif mode == "business_plan":
    c1, c2 = st.columns(2)
    with c1:
        cname = st.text_input("Company Name", placeholder="e.g. NovaTech Solutions")
        desc  = st.text_area("Business Description", placeholder="What does your business do?", height=100)
    with c2:
        stage = st.selectbox("Business Stage", ["Idea Stage","Pre-Revenue","Early Revenue","Growth Stage","Scaling"])
        fund  = st.selectbox("Funding Goal", [
            "Bootstrapped","$50K-$250K (Angel)","$250K-$1M (Pre-seed)","$1M-$5M (Seed)","$5M+ (Series A)",
        ])
    c3, c4 = st.columns(2)
    with c3: usp  = st.text_input("Unique Value Proposition", placeholder="What makes you different?")
    with c4: team = st.text_input("Team", placeholder="e.g. 2 founders: 1 tech, 1 business")

    if st.button("&#128203; Generate Business Plan", type="primary", use_container_width=True):
        if not cname or not desc:
            st.warning("Please enter a company name and description.")
        else:
            prompt = (
                f"Business plan for {cname}.\n"
                f"What: {desc}\nStage: {stage} | Funding: {fund}\n"
                f"USP: {usp or 'TBD'} | Team: {team or 'founding team'}"
            )
            run_stream(prompt, SP["business_plan"], label=f"Business Plan: {cname}")

# =============================================================================
# MODULE: PITCH DECK
# =============================================================================
elif mode == "pitch_deck":
    c1, c2 = st.columns(2)
    with c1:
        sname    = st.text_input("Startup Name", placeholder="e.g. HealthFlow")
        oneliner = st.text_input("One-liner", placeholder="e.g. The Airbnb for storage spaces")
        problem  = st.text_area("Problem", placeholder="What problem are you solving?", height=80)
    with c2:
        solution = st.text_area("Solution", placeholder="How do you solve it?", height=80)
        traction = st.text_input("Traction", placeholder="e.g. 500 beta users, $10K MRR...")
        inv_type = st.selectbox("Investor Type", [
            "Angel Investors","Seed VC","Series A VC","Corporate VC","Accelerator (YC, TechStars)",
        ])

    if st.button("&#127919; Build Pitch Strategy", type="primary", use_container_width=True):
        if not sname:
            st.warning("Please enter your startup name.")
        else:
            prompt = (
                f"Pitch deck for {sname} targeting {inv_type}.\n"
                f"One-liner: {oneliner or 'TBD'}\n"
                f"Problem: {problem or 'TBD'} | Solution: {solution or 'TBD'}\n"
                f"Traction: {traction or 'pre-traction'}"
            )
            run_stream(prompt, SP["pitch_deck"], label=f"Pitch Strategy: {sname}")

# =============================================================================
# MODULE: FINANCIAL MODEL
# =============================================================================
elif mode == "financial_model":
    c1, c2 = st.columns(2)
    with c1:
        biz_model = st.selectbox("Business Model", [
            "SaaS / Subscription","Marketplace / Platform","E-Commerce / Product",
            "Service / Agency","Freemium","Advertising","Licensing","Transaction Fee",
        ])
        price   = st.text_input("Price Point", placeholder="e.g. $29/month")
        cac     = st.text_input("Estimated CAC", placeholder="e.g. $50 per customer")
    with c2:
        growth  = st.slider("Monthly Growth %", 0, 50, 10)
        init_u  = st.number_input("Initial Users (Month 1)", min_value=0, value=100, step=10)
        op_cost = st.text_input("Monthly Operating Costs", placeholder="e.g. $5,000/month")

    if st.button("&#128176; Build Financial Model", type="primary", use_container_width=True):
        prompt = (
            f"Financial model for {biz_model} startup.\n"
            f"Price: {price or 'TBD'} | CAC: {cac or 'estimate'} | "
            f"Month-1 users: {init_u} | Monthly growth: {growth}% | "
            f"Monthly costs: {op_cost or 'estimate'}"
        )
        run_stream(prompt, SP["financial_model"], label="Financial Model & Projections")

# =============================================================================
# MODULE: ADVISOR CHAT
# =============================================================================
elif mode == "advisor_chat":
    st.markdown("""
    <div class="vchatintro">
      <strong>Ask me anything about entrepreneurship</strong> — validating ideas, raising funding,
      building teams, pricing, marketing, legal structure, scaling, and more.
    </div>""", unsafe_allow_html=True)

    QUICK = [
        "How do I validate my startup idea?",
        "When should I quit my job to start?",
        "How do I get my first 100 customers?",
        "Best legal structure for a startup?",
        "How to negotiate with investors?",
        "Key metrics to track early on?",
    ]
    st.markdown("**&#9889; Quick Questions:**")
    qc = st.columns(3)
    for i, qp in enumerate(QUICK):
        with qc[i % 3]:
            if st.button(qp, key=f"q{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": qp})
                resp = "".join(stream_ollama(qp, SP["advisor_chat"]))
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()

    st.markdown("---")

    # Show existing history
    for msg in st.session_state.chat_history:
        cls  = "vuser" if msg["role"] == "user" else "vai"
        lbl  = "You" if msg["role"] == "user" else "&#9889; VentureAI"
        body = (msg["content"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
        st.markdown(f"""
        <div class="vmsg {cls}">
          <div class="vmsglbl">{lbl}</div>
          <div class="vmsgbody">{body}</div>
        </div>""", unsafe_allow_html=True)

    # New message input — stream directly into chat
    user_input = st.chat_input("Ask your advisor anything...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Show user message immediately
        st.markdown(f"""
        <div class="vmsg vuser">
          <div class="vmsglbl">You</div>
          <div class="vmsgbody">{user_input.replace('<','&lt;').replace('>','&gt;')}</div>
        </div>""", unsafe_allow_html=True)

        # Build context from last 4 turns
        ctx = "\n".join([
            f"{'User' if m['role']=='user' else 'Advisor'}: {m['content']}"
            for m in st.session_state.chat_history[-4:]
        ])
        prompt = f"Context:\n{ctx}\n\nAnswer this: {user_input}"

        st.markdown('<div class="vmsg vai"><div class="vmsglbl">&#9889; VentureAI</div>', unsafe_allow_html=True)
        resp = st.write_stream(stream_ollama(prompt, SP["advisor_chat"]))
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.chat_history.append({"role": "assistant", "content": resp})

    if st.session_state.chat_history:
        if st.button("&#128465; Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ── Page Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="vpagefoot">
  <span>&#9889; VentureAI Business Intelligence Platform</span>
  <span>Powered by Ollama &middot; Streamlit</span>
  <span>Validate AI advice with domain experts.</span>
</div>""", unsafe_allow_html=True)
