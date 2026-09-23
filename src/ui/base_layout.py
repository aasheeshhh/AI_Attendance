import streamlit as st


def style_background_home():
    st.markdown("""
    <style>
        .stApp {
            background: #F5F5F7 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
    <style>
        .stApp {
            background: #F5F5F7 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
    <style>

    /* System font */

    * {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                     "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    }


    /* Hide Top Bar of Streamlit */

    #MainMenu, footer, header {
        visibility: hidden;
    }


    /* Main Layout */

    .block-container {
        padding-top: 1.5rem !important;
    }


    /* Main Headings */

    h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                     "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;

        color: #1D1D1F !important;

        font-weight: 700 !important;

        font-size: 3.5rem !important;

        line-height: 1.1 !important;

        margin-bottom: 0rem !important;

        letter-spacing: -0.025em !important;
    }


    /* Normal Text */

    body {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif !important;

        color: #424245 !important;
    }


    .stMarkdown,
    .stText,
    p,
    label {
        color: #424245 !important;

        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif !important;
    }


    /* Buttons */

    button {
        border-radius: 12px !important;

        background: #1D1D1F !important;

        color: #FFFFFF !important;

        padding: 10px 20px !important;

        border: none !important;

        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif !important;

        font-weight: 500 !important;

        transition: all 0.2s ease-in-out !important;

        box-shadow: none !important;
    }


    button[kind="secondary"] {
        border-radius: 12px !important;

        background: #1D1D1F !important;

        color: #FFFFFF !important;

        padding: 10px 20px !important;

        border: none !important;

        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif !important;

        font-weight: 500 !important;

        transition: all 0.2s ease-in-out !important;

        box-shadow: none !important;
    }


    button[kind="tertiary"] {
        border-radius: 12px !important;

        background: #1D1D1F !important;

        color: #FFFFFF !important;

        padding: 10px 20px !important;

        border: none !important;

        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Helvetica Neue", Arial, sans-serif !important;

        font-weight: 500 !important;

        transition: all 0.2s ease-in-out !important;

        box-shadow: none !important;
    }


    /* Force Button Text */

    button p,
    button span,
    button div {
        color: #FFFFFF !important;
    }


    /* Button Hover */

    button:hover {
        background: #2C2C2E !important;

        transform: translateY(-1px) !important;

        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
    }


    </style>
    """, unsafe_allow_html=True)