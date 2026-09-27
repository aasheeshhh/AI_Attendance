import streamlit as st


def footer_home():
    st.markdown(
        """
        <style>
        .ai-attendance-footer {
            margin-top: 4.5rem;
            margin-bottom: 2.5rem;
            padding: 0;
            text-align: center;
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Helvetica Neue",
                Arial,
                sans-serif;
        }

        .ai-attendance-footer p {
            margin: 0;
            padding: 0;
            color: #86868B !important;
            font-weight: 400;
            letter-spacing: -0.01em;
            line-height: 1.5;
        }

        .ai-attendance-footer .footer-primary {
            font-size: 12.5px !important;
            margin-bottom: 0.35rem;
        }

        .ai-attendance-footer .footer-copy {
            font-size: 12px !important;
            margin-bottom: 0.25rem;
        }

        .ai-attendance-footer .footer-tech {
            font-size: 11px !important;
            opacity: 0.85;
        }
        </style>

        <div class="ai-attendance-footer">
            <p class="footer-primary">AI Attendance • Smart Attendance Management</p>
            <p class="footer-copy">© 2026 AI Attendance</p>
            <p class="footer-tech">Built with Python &amp; Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
