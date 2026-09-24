import streamlit as st
from pathlib import Path


def header_home():

    logo_path = (
        Path(__file__).resolve().parent.parent.parent
        / "assets"
        / "logo.png"
    )

    st.markdown(
        """
        <style>

        .home-header-space {
            margin-top: 35px;
            margin-bottom: 45px;
        }

        .home-title {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Helvetica Neue",
                Arial,
                sans-serif !important;

            color: #1D1D1F !important;

            font-size: 3.2rem !important;

            font-weight: 700 !important;

            letter-spacing: -0.035em !important;

            line-height: 1 !important;

            white-space: nowrap !important;

            margin: 0 !important;

            padding: 0 !important;
        }

        [data-testid="stImage"] img {
            width: 50px !important;
            height: 50px !important;
            object-fit: contain !important;
            mix-blend-mode: multiply !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="home-header-space"></div>',
        unsafe_allow_html=True
    )

    left, logo_col, title_col, right = st.columns(
        [2.5, 0.9, 4.8, 2.5]
    )

    with logo_col:

        st.image(
            str(logo_path)
        )

    with title_col:

        st.markdown(
            '<div class="home-title">AI Attendance</div>',
            unsafe_allow_html=True
        )