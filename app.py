import streamlit as st

from reviewer import review_code

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Custom CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background: radial-gradient(circle at 10% 0%, #1a1f3c 0%, #0e1117 45%, #0a0c11 100%);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #14182c 0%, #0e1117 100%);
            border-right: 1px solid rgba(148, 130, 255, 0.12);
        }

        /* Hero header */
        .hero {
            padding: 2.2rem 2rem;
            border-radius: 20px;
            background: linear-gradient(120deg, rgba(124, 92, 255, 0.18), rgba(56, 189, 248, 0.12));
            border: 1px solid rgba(148, 130, 255, 0.25);
            margin-bottom: 1.6rem;
        }
        .hero h1 {
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(90deg, #a78bfa, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p {
            color: #9ca3af;
            margin-top: 0.4rem;
            font-size: 1rem;
        }

        /* Cards */
        .card {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
        }
        .card h4 {
            margin-top: 0;
            font-weight: 700;
            font-size: 1.05rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card ul {
            margin: 0.4rem 0 0 0;
            padding-left: 1.2rem;
        }
        .card li {
            color: #d1d5db;
            margin-bottom: 0.45rem;
            line-height: 1.5;
        }
        .empty-note {
            color: #6b7280;
            font-style: italic;
        }

        /* Score badge */
        .score-wrap {
            display: flex;
            align-items: center;
            gap: 1.4rem;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
        }
        .score-circle {
            width: 92px;
            height: 92px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            font-weight: 800;
            color: white;
            flex-shrink: 0;
        }
        .score-summary h4 {
            margin: 0 0 0.3rem 0;
            font-weight: 700;
            color: #e5e7eb;
        }
        .score-summary p {
            margin: 0;
            color: #9ca3af;
            line-height: 1.5;
        }

        /* Badge pills for tags */
        .pill {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.4rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.04);
            border-radius: 10px 10px 0 0;
            padding: 0.55rem 1rem;
            color: #9ca3af;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(124, 92, 255, 0.22) !important;
            color: #e5e7eb !important;
        }

        div.stButton > button {
            background: linear-gradient(90deg, #7c5cff, #38bdf8);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-weight: 700;
            width: 100%;
        }
        div.stButton > button:hover {
            opacity: 0.9;
            color: white;
        }

        textarea, .stTextArea textarea {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
LANGUAGES = [
    "python", "javascript", "typescript", "java", "c", "c++", "c#",
    "go", "rust", "php", "ruby", "kotlin", "swift", "sql",
]

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    language = st.selectbox("Language", LANGUAGES, index=0)

    st.markdown("---")
    uploaded_file = st.file_uploader(
        "Upload a code file (optional)",
        type=None,
        help="Or paste code directly in the editor.",
    )

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🧠 AI Code Review Assistant</h1>
        <p>Paste your code and get an instant, structured review — bugs, security,
        performance, readability, best practices, and a fully refactored version.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Code input
# --------------------------------------------------------------------------
default_code = ""
if uploaded_file is not None:
    try:
        default_code = uploaded_file.read().decode("utf-8")
    except Exception:
        st.warning("Couldn't decode the uploaded file as text.")

code_input = st.text_area(
    "Paste your code here",
    value=default_code,
    height=320,
    placeholder="def add(a, b):\n    return a + b",
    label_visibility="collapsed",
)

col_a, col_b = st.columns([1, 5])
with col_a:
    run_review = st.button("🔍 Review Code", use_container_width=True)

# --------------------------------------------------------------------------
# Run review
# --------------------------------------------------------------------------
if run_review:
    if not code_input.strip():
        st.error("Please paste or upload some code first.")
    else:
        with st.spinner("Analyzing your code..."):
            try:
                result = review_code(code_input, language)
                st.session_state["review_result"] = result
            except Exception as e:
                st.session_state["review_result"] = None
                st.error(f"Something went wrong while running the review: {e}")

# --------------------------------------------------------------------------
# Display results
# --------------------------------------------------------------------------
result = st.session_state.get("review_result")

if result:
    score = result.quality_score
    if score >= 80:
        score_color = "#22c55e"
    elif score >= 50:
        score_color = "#f59e0b"
    else:
        score_color = "#ef4444"

    st.markdown(
        f"""
        <div class="score-wrap">
            <div class="score-circle" style="background:{score_color};">{score}</div>
            <div class="score-summary">
                <h4>Overall Quality Score</h4>
                <p>{result.summary or "No summary provided."}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def render_list_card(title, icon, items, color):
        if items:
            list_html = "".join(f"<li>{item}</li>" for item in items)
            body = f"<ul>{list_html}</ul>"
        else:
            body = '<p class="empty-note">Nothing to report — looks good here.</p>'
        st.markdown(
            f"""
            <div class="card">
                <h4 style="color:{color};">{icon} {title}</h4>
                {body}
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Findings", "🛠️ Refactored Code", "📄 Documentation", "⏱️ Complexity"]
    )

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            render_list_card("Bugs", "🐞", result.bugs, "#f87171")
            render_list_card("Best Practices", "✅", result.best_practices, "#34d399")
        with c2:
            render_list_card("Readability Improvements", "📖", result.readability_improvements, "#60a5fa")

    with tab2:
        st.markdown("#### Fully Refactored Code")
        if result.refactored_code:
            st.code(result.refactored_code, language=language)
        else:
            st.info("No refactored code was returned.")

    with tab3:
        st.markdown("#### Documentation / Docstrings")
        if result.documentation:
            st.markdown(result.documentation)
        else:
            st.info("No documentation was returned.")

    with tab4:
        st.markdown("#### Time Complexity")
        st.markdown(
            f"""
            <div class="card">
                <h4 style="color:#a78bfa;">⏱️ Estimated Complexity</h4>
                <p style="color:#d1d5db; font-family:'JetBrains Mono', monospace; font-size:1.1rem;">
                    {result.time_complexity or "Not specified"}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="card" style="text-align:center; padding:2.5rem;">
            <p style="color:#6b7280; margin:0;">
                Paste some code above and click <b>Review Code</b> to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )