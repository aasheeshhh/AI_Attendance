import streamlit as st


def apply_home_style():
    """Apply the warm glass design used by the home screen."""
    st.markdown(
        """
        <style>
        /* Global */
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                "SF Pro Text", "Segoe UI", sans-serif !important;
        }

        #MainMenu, footer, header {
            visibility: hidden !important;
        }

        /* Background */
        .stApp,
        [data-testid="stAppViewContainer"] {
            color: #F5F1E8 !important;
            background:
                radial-gradient(ellipse 55% 50% at 12% 5%, rgba(149, 138, 106, 0.18), transparent 70%),
                radial-gradient(ellipse 45% 55% at 93% 92%, rgba(102, 94, 70, 0.20), transparent 72%),
                linear-gradient(135deg, #151512 0%, #1C1B17 52%, #171713 100%) !important;
            background-size: 115% 115%, 120% 120%, 100% 100% !important;
            background-attachment: fixed !important;
            animation: move-background 18s ease-in-out infinite alternate;
        }

        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stMain"],
        .main .block-container {
            background: transparent !important;
        }

        @keyframes move-background {
            from { background-position: 0% 0%, 100% 100%, 0 0; }
            to { background-position: 8% 4%, 92% 95%, 0 0; }
        }

        /* Layout */
        .block-container {
            max-width: 1020px !important;
            padding: clamp(2.5rem, 8vh, 6.25rem) clamp(1.25rem, 5vw, 3.5rem) 3.5rem !important;
            animation: show-page 700ms ease-out both;
        }

        @keyframes show-page {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Header */
        .brand-header {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .brand-logo-frame {
            width: 46px;
            height: 46px;
            overflow: hidden;
            border: 1px solid rgba(245, 241, 232, 0.5);
            border-radius: 14px;
            background: #F5F1E8;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.32);
        }

        .brand-logo-frame img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .brand-name {
            color: #F5F1E8;
            font-size: 1.15rem;
            font-weight: 600;
            letter-spacing: -0.035em;
        }

        /* Hero */
        .home-hero {
            margin: clamp(3rem, 9vh, 7rem) 0 2.75rem;
            text-align: center;
        }

        .home-eyebrow {
            margin: 0 0 0.9rem;
            color: rgba(245, 241, 232, 0.58);
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .home-title {
            margin: 0;
            color: #F5F1E8;
            font-size: clamp(2rem, 4.2vw, 3.25rem);
            font-weight: 600;
            letter-spacing: -0.055em;
            line-height: 1.08;
        }

        .home-subtitle {
            margin: 1rem 0 0;
            color: rgba(245, 241, 232, 0.58);
            font-size: 1.02rem;
            line-height: 1.5;
        }

        /* Shared portal surface */
        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(245, 241, 232, 0.16) !important;
            border-radius: 30px !important;
            background: rgba(245, 241, 232, 0.08) !important;
            box-shadow: 0 20px 55px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.10) !important;
            backdrop-filter: blur(26px) saturate(120%);
            -webkit-backdrop-filter: blur(26px) saturate(120%);
            animation: show-card 800ms 140ms ease-out both;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor)::before {
            position: absolute;
            inset: 0;
            content: "";
            pointer-events: none;
            background: linear-gradient(135deg, rgba(245, 241, 232, 0.07), transparent 38%);
            transition: background 280ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        .portal-container-anchor {
            height: 0;
            overflow: hidden;
        }

        @keyframes show-card {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .portal-copy {
            padding: 0.75rem 0 1.2rem;
        }

        .portal-label {
            margin: 0 0 0.35rem;
            color: #F5F1E8;
            font-size: 1.35rem;
            font-weight: 600;
            letter-spacing: -0.04em;
        }

        .portal-description {
            margin: 0;
            color: rgba(245, 241, 232, 0.58);
            font-size: 0.9rem;
            line-height: 1.45;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"] {
            min-height: 242px;
            padding: 1.9rem !important;
            border-radius: 22px;
            transition: transform 260ms ease, background 260ms ease, box-shadow 260ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"] + [data-testid="column"] {
            border-left: 1px solid rgba(245, 241, 232, 0.13);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"]:hover {
            transform: translateY(-3px);
            background: rgba(245, 241, 232, 0.045);
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.14);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) div.stButton > button {
            width: 100% !important;
            min-height: 58px !important;
            border: 1px solid rgba(245, 241, 232, 0.16) !important;
            border-radius: 15px !important;
            color: #F5F1E8 !important;
            background: rgba(245, 241, 232, 0.08) !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.07) !important;
            font-size: 0.93rem !important;
            font-weight: 550 !important;
            transition: transform 260ms ease, background 260ms ease, border-color 260ms ease, box-shadow 260ms ease !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"]:hover div.stButton > button,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) div.stButton > button:hover {
            border-color: rgba(245, 241, 232, 0.28) !important;
            background: rgba(149, 138, 106, 0.28) !important;
            box-shadow: 0 10px 22px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.13) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) div.stButton > button:active {
            transform: scale(0.985) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) div.stButton > button:focus-visible {
            outline: 2px solid #958A6A !important;
            outline-offset: 3px !important;
        }

        /* Footer and mobile */
        .home-footer {
            margin: 2rem 0 0;
            color: rgba(245, 241, 232, 0.42);
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-align: center;
        }

        @media (max-width: 700px) {
            .block-container { padding-top: 2rem !important; }
            .home-hero { margin: 3.75rem 0 2rem; }

            [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) {
                border-radius: 24px !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"] {
                min-height: auto;
                padding: 1.45rem !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:has(.portal-container-anchor) [data-testid="column"] + [data-testid="column"] {
                border-top: 1px solid rgba(245, 241, 232, 0.13);
                border-left: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
