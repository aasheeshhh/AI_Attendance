import streamlit as st


def style_portal_cards():

    st.markdown(
        """
        <style>

        /* ---------- Portal Section ---------- */

        .st-key-portal_section {
            width: 900px !important;
            max-width: 900px !important;

            margin-left: auto !important;
            margin-right: auto !important;

            margin-top: -1rem !important;
        }


        /* ---------- Portal Columns ---------- */

        .st-key-portal_section [data-testid="stHorizontalBlock"] {
            width: 900px !important;
            max-width: 900px !important;

            margin-left: auto !important;
            margin-right: auto !important;

            gap: 2rem !important;
        }


        /* ---------- Portal Title ---------- */

        .portal-title {
            text-align: center !important;

            font-size: 1.45rem !important;
            font-weight: 600 !important;

            color: #1D1D1F !important;

            letter-spacing: -0.01em !important;

            margin: 0 0 0.75rem 0 !important;
        }


        /* ---------- Portal Cards ---------- */

        .st-key-teacher_card,
        .st-key-student_card {

            display: flex !important;

            flex-direction: column !important;

            align-items: center !important;

            justify-content: flex-start !important;

            width: 100% !important;

            height: 510px !important;

            box-sizing: border-box !important;

            padding: 1.5rem 1rem 1.25rem 1rem !important;

            background: rgba(255, 255, 255, 0.72) !important;

            border: 1px solid rgba(255, 255, 255, 0.9) !important;

            border-radius: 30px !important;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.06) !important;

            backdrop-filter: blur(12px) !important;

            -webkit-backdrop-filter: blur(12px) !important;

            transition:
                transform 0.25s ease,
                box-shadow 0.25s ease !important;
        }


        /* ---------- Card Hover ---------- */

        .st-key-teacher_card:hover,
        .st-key-student_card:hover {

            transform: translateY(-5px) !important;

            box-shadow:
                0 16px 40px rgba(0, 0, 0, 0.10) !important;
        }


        /* ---------- Image Area ---------- */

        .st-key-teacher_image,
        .st-key-student_image {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            flex: 1 1 auto !important;

            margin: 0 !important;

            padding: 0 !important;
        }


        /* ---------- Streamlit Image Wrapper ---------- */

        .st-key-teacher_image [data-testid="stImage"],
        .st-key-student_image [data-testid="stImage"] {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 !important;

            padding: 0 !important;
        }


        /* ---------- Images (aspect-ratio preserved: height-only) ---------- */

        .st-key-teacher_image [data-testid="stImage"] img,
        .st-key-student_image [data-testid="stImage"] img {

            display: block !important;

            margin-left: auto !important;

            margin-right: auto !important;

            height: 300px !important;

            width: auto !important;

            max-width: 100% !important;

            object-fit: contain !important;
        }


        /* ---------- Button Area ---------- */

        .st-key-teacher_button,
        .st-key-student_button {

            width: 225px !important;

            max-width: 225px !important;

            margin-left: auto !important;

            margin-right: auto !important;
        }


        /* ---------- Buttons ---------- */

        .st-key-teacher_button button,
        .st-key-student_button button {

            width: 100% !important;

            min-height: 46px !important;

            border-radius: 13px !important;

            font-size: 15px !important;

            font-weight: 500 !important;

            padding: 0.6rem 1rem !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        /* ---------- Button Hover ---------- */

        .st-key-teacher_button button:hover,
        .st-key-student_button button:hover {

            transform: translateY(-2px) !important;

            box-shadow:
                0 6px 16px rgba(0, 0, 0, 0.12) !important;
        }


        /* ---------- Responsive: Tablet ---------- */

        @media (max-width: 900px) {

            .st-key-portal_section {

                width: min(900px, calc(100vw - 40px)) !important;

                max-width: min(900px, calc(100vw - 40px)) !important;
            }


            .st-key-portal_section [data-testid="stHorizontalBlock"] {

                width: 100% !important;

                max-width: 100% !important;

                gap: 1rem !important;
            }


            .st-key-teacher_card,
            .st-key-student_card {

                height: 480px !important;
            }


            .st-key-teacher_image [data-testid="stImage"] img,
            .st-key-student_image [data-testid="stImage"] img {

                height: 250px !important;

                width: auto !important;

                max-width: 100% !important;
            }
        }


        /* ---------- Responsive: Mobile ---------- */

        @media (max-width: 650px) {

            .st-key-portal_section {

                width: calc(100vw - 30px) !important;

                max-width: calc(100vw - 30px) !important;
            }


            .st-key-portal_section [data-testid="stHorizontalBlock"] {

                flex-direction: column !important;

                gap: 1rem !important;
            }


            .st-key-teacher_card,
            .st-key-student_card {

                height: 450px !important;
            }


            .st-key-teacher_image [data-testid="stImage"] img,
            .st-key-student_image [data-testid="stImage"] img {

                height: 220px !important;

                width: auto !important;

                max-width: 100% !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )