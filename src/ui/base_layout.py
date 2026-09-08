import streamlit as st


def style_base_layout():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        html,
        body,
        [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Segoe UI",
                sans-serif !important;
        }


        /* =====================================================
           APP BACKGROUND
        ===================================================== */

        .stApp {
            background: #080a12 !important;
            color: #f5f5f7 !important;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 12% 12%,
                    rgba(76, 86, 190, 0.42) 0%,
                    rgba(76, 86, 190, 0.18) 22%,
                    transparent 42%
                ),

                radial-gradient(
                    circle at 88% 20%,
                    rgba(125, 72, 180, 0.28) 0%,
                    rgba(125, 72, 180, 0.10) 24%,
                    transparent 45%
                ),

                radial-gradient(
                    circle at 50% 105%,
                    rgba(40, 70, 150, 0.30) 0%,
                    transparent 45%
                ),

                #080a12 !important;

            background-attachment: fixed !important;

            animation:
                backgroundMove
                18s
                ease-in-out
                infinite
                alternate;
        }


        [data-testid="stAppViewContainer"] > .main {
            background: transparent !important;
        }


        [data-testid="stMain"] {
            background: transparent !important;
        }


        /* =====================================================
           SUBTLE CENTER GLOW
        ===================================================== */

        [data-testid="stAppViewContainer"]::before {

            content: "";

            position: fixed;

            width: 500px;
            height: 500px;

            top: 40%;
            left: 50%;

            transform: translate(-50%, -50%);

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(75, 85, 180, 0.10),
                    transparent 70%
                );

            filter: blur(70px);

            pointer-events: none;

            z-index: 0;

            animation:
                centerGlow
                12s
                ease-in-out
                infinite
                alternate;
        }


        /* =====================================================
           BACKGROUND ANIMATIONS
        ===================================================== */

        @keyframes backgroundMove {

            0% {
                background-position:
                    0% 0%,
                    100% 0%,
                    50% 100%;
            }

            100% {
                background-position:
                    8% 6%,
                    92% 8%,
                    55% 92%;
            }
        }


        @keyframes centerGlow {

            0% {
                opacity: 0.6;

                transform:
                    translate(-50%, -50%)
                    scale(0.9);
            }

            100% {
                opacity: 1;

                transform:
                    translate(-45%, -55%)
                    scale(1.1);
            }
        }


        /* =====================================================
           HIDE STREAMLIT DEFAULT UI
        ===================================================== */

        #MainMenu,
        footer,
        header {
            visibility: hidden !important;
        }


        /* =====================================================
           MAIN CONTENT
        ===================================================== */

        .block-container {

            position: relative;

            z-index: 2;

            max-width: 1050px !important;

            padding-top: 5rem !important;

            padding-bottom: 4rem !important;

            padding-left: 3rem !important;

            padding-right: 3rem !important;
        }


        /* =====================================================
           TYPOGRAPHY
        ===================================================== */

        h1,
        h2,
        h3 {

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Segoe UI",
                sans-serif !important;

            color: #f5f5f7 !important;
        }


        h1 {

            font-size: 4.5rem !important;

            line-height: 1 !important;

            font-weight: 700 !important;

            letter-spacing: -4px !important;

            margin-top: 0 !important;

            margin-bottom: 0.7rem !important;

            animation:
                titleAppear
                0.8s
                cubic-bezier(0.22, 1, 0.36, 1);
        }


        @keyframes titleAppear {

            from {
                opacity: 0;

                transform:
                    translateY(18px)
                    scale(0.98);
            }

            to {
                opacity: 1;

                transform:
                    translateY(0)
                    scale(1);
            }
        }


        /* =====================================================
           SUBTITLE
        ===================================================== */

        .home-subtitle {

            color:
                rgba(245, 245, 247, 0.50) !important;

            font-size: 17px !important;

            font-weight: 400 !important;

            letter-spacing: -0.2px;

            margin-bottom: 3rem;

            animation:
                subtitleAppear
                0.8s
                0.12s
                cubic-bezier(0.22, 1, 0.36, 1);

            animation-fill-mode: both;
        }


        @keyframes subtitleAppear {

            from {
                opacity: 0;

                transform:
                    translateY(12px);
            }

            to {
                opacity: 1;

                transform:
                    translateY(0);
            }
        }


        /* =====================================================
           COLUMNS
        ===================================================== */

        [data-testid="column"] {

            position: relative;

            z-index: 3;
        }


        /* =====================================================
           PORTAL CARD ANIMATION
        ===================================================== */

        div.stButton {

            animation:
                cardAppear
                0.8s
                cubic-bezier(0.22, 1, 0.36, 1);

            animation-fill-mode: both;
        }


        [data-testid="column"]:first-child div.stButton {
            animation-delay: 0.18s;
        }


        [data-testid="column"]:last-child div.stButton {
            animation-delay: 0.28s;
        }


        @keyframes cardAppear {

            from {
                opacity: 0;

                transform:
                    translateY(25px)
                    scale(0.97);
            }

            to {
                opacity: 1;

                transform:
                    translateY(0)
                    scale(1);
            }
        }


        /* =====================================================
           GLASS PORTAL CARDS
        ===================================================== */

        div.stButton > button {

            width: 100% !important;

            height: 210px !important;

            min-height: 210px !important;

            padding: 2rem !important;

            border-radius: 24px !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.12) !important;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.085),
                    rgba(255, 255, 255, 0.035)
                ) !important;

            backdrop-filter:
                blur(28px)
                saturate(140%) !important;

            -webkit-backdrop-filter:
                blur(28px)
                saturate(140%) !important;

            color:
                rgba(255, 255, 255, 0.92) !important;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Segoe UI",
                sans-serif !important;

            font-size: 20px !important;

            font-weight: 600 !important;

            letter-spacing: -0.5px !important;

            box-shadow:
                0 20px 50px
                rgba(0, 0, 0, 0.25),

                inset 0 1px 0
                rgba(255, 255, 255, 0.08) !important;

            transition:
                transform 0.35s
                cubic-bezier(0.22, 1, 0.36, 1),

                background 0.35s ease,

                border-color 0.35s ease,

                box-shadow 0.35s ease !important;
        }


        /* =====================================================
           CARD HOVER
        ===================================================== */

        div.stButton > button:hover {

            transform:
                translateY(-8px) !important;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.12),
                    rgba(255, 255, 255, 0.05)
                ) !important;

            border-color:
                rgba(255, 255, 255, 0.20) !important;

            box-shadow:
                0 30px 70px
                rgba(0, 0, 0, 0.35),

                0 0 40px
                rgba(90, 100, 220, 0.10),

                inset 0 1px 0
                rgba(255, 255, 255, 0.12) !important;
        }


        /* =====================================================
           CARD PRESS
        ===================================================== */

        div.stButton > button:active {

            transform:
                translateY(-2px)
                scale(0.98) !important;
        }


        /* =====================================================
           BUTTON FOCUS
        ===================================================== */

        div.stButton > button:focus {

            outline: none !important;

            border-color:
                rgba(150, 150, 255, 0.30) !important;

            box-shadow:
                0 0 0 1px
                rgba(120, 120, 255, 0.15),

                0 25px 60px
                rgba(0, 0, 0, 0.30) !important;
        }


        /* =====================================================
           FOOTER
        ===================================================== */

        .home-footer {

            margin-top: 2rem;

            color:
                rgba(255, 255, 255, 0.28) !important;

            font-size: 12px !important;

            letter-spacing: 0.2px;

            text-align: center;

            animation:
                footerAppear
                1s
                0.4s
                ease;

            animation-fill-mode: both;
        }


        @keyframes footerAppear {

            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 700px) {

            .block-container {

                padding-top: 3rem !important;

                padding-left: 1.25rem !important;

                padding-right: 1.25rem !important;
            }


            h1 {

                font-size: 3.2rem !important;

                letter-spacing: -2.5px !important;
            }


            .home-subtitle {

                font-size: 15px !important;

                margin-bottom: 2rem;
            }


            div.stButton > button {

                height: 160px !important;

                min-height: 160px !important;

                border-radius: 20px !important;

                font-size: 18px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_home():
    pass


def style_background_dashboard():
    pass