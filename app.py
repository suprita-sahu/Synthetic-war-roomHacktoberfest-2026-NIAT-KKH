import streamlit as st
import re
import time
from engine import war_room_graph

st.set_page_config(
    page_title="Synthetic War Room",
    page_icon="⚔️",
    layout="wide"
)

# Native, understated styling
st.markdown("""
<style>
    :root {
        color-scheme: light;
        --canvas: #f5f5f7;
        --surface: #ffffff;
        --ink: #1d1d1f;
        --secondary: #6e6e73;
        --line: #e5e5ea;
        --blue: #b8d8ff;
        --blue-ink: #315d8a;
        --blue-soft: #f1f7ff;
    }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp,
    [data-testid="stAppViewContainer"] {
        background: var(--canvas);
        color: var(--ink);
    }

    header[data-testid="stHeader"] {
        background: rgba(245, 245, 247, 0.9);
        backdrop-filter: blur(16px);
    }

    header[data-testid="stHeader"] button {
        color: var(--secondary);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: #fbfbfd;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--secondary);
    }

    h1 {
        color: var(--ink);
        font-size: clamp(2rem, 4vw, 2.8rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.055em !important;
        line-height: 1.08 !important;
        margin-bottom: 0.35rem !important;
    }

    h2, h3, label, [data-testid="stMarkdownContainer"] {
        color: var(--ink);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--secondary);
        font-size: 1rem;
    }

    .hero-card {
        padding: 1.25rem 1.4rem;
        margin: 1.35rem 0 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.045);
        border-radius: 18px;
        background: var(--surface);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.035), 0 12px 30px rgba(0, 0, 0, 0.025);
    }

    .hero-card h3 {
        margin: 0 0 0.35rem;
        color: var(--ink);
        font-size: 1rem;
        font-weight: 650;
        letter-spacing: -0.02em;
    }

    .hero-card p {
        margin: 0;
        max-width: 760px;
        color: var(--secondary);
        font-size: 0.95rem;
        line-height: 1.55;
    }

    .metric-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.42rem 0.72rem;
        margin-bottom: 0.75rem;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--surface);
        color: var(--secondary);
        font-size: 0.73rem;
        font-weight: 650;
        letter-spacing: 0.025em;
    }

    .badge-defender { background: #f0f6ff; border-color: #dceaff; color: #1764b0; }
    .badge-attacker { background: #fff4f2; border-color: #ffe0db; color: #b54735; }
    .badge-moderator { background: #effaf3; border-color: #d6f1df; color: #287a43; }

    [data-testid="stTextAreaRootElement"] {
        border: 1px solid #e2e2e7 !important;
        border-radius: 12px !important;
        background: var(--surface) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.035);
    }

    .stTextArea textarea,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        background: var(--surface) !important;
        color: var(--ink) !important;
        box-shadow: none !important;
    }

    .stTextArea textarea {
        border: 0 !important;
        outline: none !important;
        padding: 0.85rem 0.95rem;
        line-height: 1.55;
    }

    [data-testid="stTextAreaRootElement"]:focus-within {
        border-color: #cbdced !important;
        box-shadow: 0 0 0 3px rgba(203, 220, 237, 0.35);
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border-color: #cbdced !important;
        box-shadow: 0 0 0 3px rgba(203, 220, 237, 0.35) !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        min-height: 2.8rem;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: background-color 120ms ease, transform 120ms ease;
    }

    .stButton > button[kind="primary"] {
        border: 1px solid #c7e0ff !important;
        background: #dcecff !important;
        color: var(--blue-ink) !important;
        box-shadow: 0 2px 5px rgba(93, 145, 203, 0.12);
    }

    .stButton > button[kind="primary"] [data-testid="stMarkdownContainer"],
    .stButton > button[kind="primary"] p {
        color: var(--blue-ink) !important;
    }

    .stButton > button[kind="primary"]:hover {
        border-color: #c1dcff !important;
        background: #cfe4ff !important;
        transform: translateY(-1px);
    }

    .stDownloadButton > button {
        border: 1px solid #d2d2d7 !important;
        background: var(--surface) !important;
        color: var(--blue-ink) !important;
    }

    .stDownloadButton > button:hover {
        border-color: #b8d5ff !important;
        background: var(--blue-soft) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: #9ccaff;
        border-color: #9ccaff;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background: #9ccaff;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.025);
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--surface);
    }

    [data-testid="stStatusWidget"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--surface);
    }

    [data-testid="stProgress"] > div > div {
        background-color: #b8d8ff;
    }

    hr {
        border-color: var(--line);
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1.5rem 1rem 2.5rem;
        }

        .hero-card {
            padding: 1rem;
            margin: 1rem 0 1.25rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Preset Scenarios
with st.sidebar:
    st.header("Settings")
    st.markdown("**Model:** Google Gemma 2 (2B-IT) via Ollama")
    rounds = st.slider("Debate Rounds", min_value=1, max_value=3, value=1)
    st.divider()
    st.subheader("Scenarios")
    presets = {
        "Custom": "",
        "Web3 Escrow Vulnerability": "An escrow smart-contract system where buyers and sellers resolve disputes via 3 community-elected stakers.",
        "Zero-Trust Auth Policy": "A passwordless microservices auth gateway storing rolling session tokens in client localStorage with 1-hour expiration.",
        "Autonomous Refund Agent": "An automated AI customer-care agent permitted to grant instant chargeback refunds under $50 without human sign-off."
    }

    def load_scenario():
        st.session_state.proposal_input = presets[st.session_state.scenario_choice]

    st.selectbox(
        "Pick Scenario:",
        list(presets.keys()),
        key="scenario_choice",
        on_change=load_scenario
    )

st.title("Synthetic War Room")
st.caption("Adversarial design review, powered by Google Gemma 2.")
st.markdown('''
<div class="hero-card">
    <h3>Threat briefing</h3>
    <p>Stress-test product ideas, architectures, and trust boundaries with an adversarial review loop designed to surface exploitable assumptions before launch.</p>
</div>
''', unsafe_allow_html=True)

proposal_input = st.text_area(
    "Startup idea or system design",
    key="proposal_input",
    placeholder="Describe any startup idea, product concept, architecture, or feature you want reviewed...",
    height=140,
    help="Enter your own idea, or choose a preset from the sidebar. The review is based on the text in this field."
)
start_btn = st.button("Run stress test", type="primary", use_container_width=True)

if start_btn and not proposal_input.strip():
    st.warning("Add a startup idea or design above before starting the review.")

if start_btn and proposal_input.strip():
    initial_state = {
        "topic": proposal_input,
        "round": 1,
        "max_rounds": rounds,
        "architect_points": [],
        "adversary_critiques": [],
        "current_defense": "",
        "current_attack": "",
        "final_verdict": ""
    }

    st.divider()
    status_box = st.status("Initializing review...", expanded=True)

    expected_words = {
        "architect": 240,
        "adversary": 180,
        "moderator": 260
    }
    agent_labels = {
        "architect": "Architect · Gemma 2",
        "adversary": "Red team · Gemma 2",
        "moderator": "Auditor · Gemma 2"
    }
    progress_widgets = {}
    eta_widgets = {}
    started_at = {}
    output_text = {}
    active_body = None
    last_painted = 0.0

    with st.container(border=True):
        st.markdown("#### Live model progress")
        progress_columns = st.columns(3)
        for agent, column in zip(agent_labels, progress_columns):
            with column:
                st.caption(agent_labels[agent])
                progress_widgets[agent] = st.progress(0, text="Waiting")
                eta_widgets[agent] = st.empty()
        st.caption("Completion percentage and remaining time are estimates based on typical response length and the current output rate.")

    col_alpha, col_beta = st.columns(2)
    with col_alpha:
        st.markdown('<span class="metric-badge badge-defender">Defender · Agent Alpha</span>', unsafe_allow_html=True)
        alpha_slot = st.container()

    with col_beta:
        st.markdown('<span class="metric-badge badge-attacker">Red team · Agent Beta</span>', unsafe_allow_html=True)
        beta_slot = st.container()

    report_slot = st.container()
    agent_slots = {"architect": alpha_slot, "adversary": beta_slot}
    final_output = None
    current_round = 1

    for mode, chunk in war_room_graph.stream(initial_state, stream_mode=["custom", "updates"]):
        if mode == "custom":
            agent = chunk["agent"]

            if chunk["event"] == "start":
                started_at[agent] = time.monotonic()
                output_text[agent] = ""
                active_body = None
                progress_widgets[agent].progress(0, text="Starting")
                eta_widgets[agent].caption("Waiting for first tokens…")
                status_box.update(label=f"{agent_labels[agent]} is generating…", state="running")

                if agent == "moderator":
                    with report_slot:
                        st.divider()
                        st.markdown('<span class="metric-badge badge-moderator">Auditor report</span>', unsafe_allow_html=True)
                        st.subheader("Hardened Production Specification")
                        active_body = st.empty()
                else:
                    avatar = "🛡️" if agent == "architect" else "🎯"
                    heading = "Proposal" if agent == "architect" else "Exploits & Failure Modes"
                    with agent_slots[agent]:
                        with st.chat_message("assistant" if agent == "architect" else "user", avatar=avatar):
                            st.markdown(f"**Round {current_round} {heading}**")
                            active_body = st.empty()

            elif chunk["event"] == "token":
                output_text[agent] += chunk["text"]
                now = time.monotonic()
                word_count = len(output_text[agent].split())
                elapsed = now - started_at[agent]
                progress = min(word_count / expected_words[agent], 0.95)
                percent = int(progress * 100)
                progress_widgets[agent].progress(progress, text=f"~{percent}% · generating")

                if word_count >= 3 and elapsed > 0:
                    words_per_second = word_count / elapsed
                    remaining_words = max(expected_words[agent] - word_count, 0)
                    eta_seconds = int(remaining_words / words_per_second)
                    eta_widgets[agent].caption(f"About {eta_seconds}s remaining · {word_count} words shown")
                else:
                    eta_widgets[agent].caption(f"Estimating time · {word_count} words shown")

                if active_body is not None and (now - last_painted >= 0.12 or "\n" in chunk["text"]):
                    active_body.markdown(output_text[agent])
                    last_painted = now

            elif chunk["event"] == "done":
                progress_widgets[agent].progress(1.0, text="100% · complete")
                eta_widgets[agent].caption(f"Complete · {len(output_text[agent].split())} words displayed")
                if active_body is not None:
                    active_body.markdown(output_text[agent])

        elif mode == "updates" and "moderator" in chunk:
            final_output = chunk["moderator"]
            current_round = final_output["round"]
            if final_output["round"] <= rounds:
                status_box.update(label=f"Round {final_output['round']} · Preparing next pass", state="running")
            else:
                status_box.update(label="Review complete", state="complete")

    if final_output and final_output.get("final_verdict"):
        report = final_output["final_verdict"]
        with report_slot:
            st.download_button(
                label="Export report",
                data=f"# Hardened Audit Report\n\n**Topic:** {proposal_input}\n\n---\n\n{report}",
                file_name="hardened_spec.md",
                mime="text/markdown"
            )