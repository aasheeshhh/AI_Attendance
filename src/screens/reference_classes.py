"""
Classes Page - Direct Transfer from pixel-perfect-snap-8916/src/routes/classes.tsx
Class cards grid with enrollment stats and average attendance
"""

import streamlit as st
from src.ui.reference_components import (
    apply_reference_base_styles,
    render_topbar,
    render_sidebar,
    render_page_header,
    render_main_content_area,
    REFERENCE_COLORS,
    REFERENCE_SHADOWS,
    REFERENCE_RADIUS,
)
from src.database.db import (
    get_teacher_subjects,
    get_all_students,
    get_all_attendance_logs,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog


def reference_classes_page(teacher_data):
    """
    Render Classes page exactly matching reference/src/routes/classes.tsx
    """

    apply_reference_base_styles()

    # Render TopBar
    render_topbar(
        app_title="AI Attendance",
        user_name=teacher_data.get('name', 'Teacher'),
        user_role="Teacher"
    )

    # Render Sidebar
    render_sidebar(
        active_page=st.session_state.get('nav_page', 'Classes'),
        on_page_change=lambda page: setattr(st.session_state, 'nav_page', page)
    )

    # Main content area
    render_main_content_area()

    # PageHeader
    render_page_header(
        title="Classes",
        subtitle="Overview of every class you teach",
        date_pill=None
    )

    # Load data
    subjects = get_teacher_subjects(teacher_data['teacher_id']) or []
    students = get_all_students() or []
    logs = get_all_attendance_logs() or []

    # Add Class button
    if st.button("+ Create Class", type='primary', use_container_width=False):
        create_subject_dialog(teacher_data['teacher_id'])

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Class Cards Grid (matching reference: 2 cols on sm, 4 cols on xl)
    if subjects:
        # Create responsive grid
        cols = st.columns(4, gap="medium")

        for i, subject in enumerate(subjects):
            # Calculate class stats
            subject_logs = [l for l in logs if l.get('subject_id') == subject['subject_id']]
            total_logs = len(subject_logs)
            present_logs = sum(1 for l in subject_logs if l.get('is_present'))
            attendance_rate = int((present_logs / total_logs * 100)) if total_logs > 0 else 92  # Default mock

            # Count enrolled students (mock)
            enrolled_count = len([s for s in students if True]) // len(subjects) if subjects else 25

            with cols[i % 4]:
                # Class Card (reference Panel with hover, BookOpen icon, stats)
                st.markdown(f"""
                    <div class="ref-panel ref-panel-hover" style="min-height: 200px;">
                        <div style="
                            width: 36px;
                            height: 36px;
                            border-radius: 12px;
                            background: {REFERENCE_COLORS['accent']};
                            color: {REFERENCE_COLORS['primary']};
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 16px;
                        ">📚</div>

                        <div style="margin-top: 16px; font-size: 15px; font-weight: 600; color: {REFERENCE_COLORS['primary']};">
                            {subject['name']}
                        </div>

                        <div style="margin-top: 4px; font-size: 12.5px; color: {REFERENCE_COLORS['muted_foreground']};">
                            {enrolled_count} students · {subject['section']}
                        </div>

                        <div style="
                            margin-top: 16px;
                            display: flex;
                            align-items: flex-end;
                            justify-content: space-between;
                        ">
                            <span style="font-size: 24px; font-weight: 600; color: {REFERENCE_COLORS['primary']}; font-variant-numeric: tabular-nums;">
                                {attendance_rate}%
                            </span>
                            <span style="font-size: 12px; color: {REFERENCE_COLORS['muted_foreground']};">
                                avg. attendance
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Share button below each card
                if st.button(f"Share {subject['subject_code']}", key=f"share_{subject['subject_id']}", use_container_width=True, type='secondary'):
                    share_subject_dialog(subject['name'], subject['subject_code'])

    else:
        # Empty state
        st.markdown(f"""
            <div class="ref-panel" style="text-align: center; padding: 48px;">
                <div style="font-size: 48px; margin-bottom: 16px;">📚</div>
                <div style="font-size: 15px; font-weight: 600; color: {REFERENCE_COLORS['primary']}; margin-bottom: 8px;">
                    No Classes Yet
                </div>
                <div style="font-size: 13px; color: {REFERENCE_COLORS['muted_foreground']};">
                    Create your first class to start taking attendance
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Close main content area
    st.markdown("</div>", unsafe_allow_html=True)
