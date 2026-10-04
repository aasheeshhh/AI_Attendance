"""
Dashboard - Direct Transfer from pixel-perfect-snap-8916/src/routes/index.tsx
Exact layout: PageHeader + 4 StatCards + TrendChart + AIInsight + QuickActions + AttendanceTable
"""

import streamlit as st
from datetime import datetime
from src.ui.reference_components import (
    apply_reference_base_styles,
    render_topbar,
    render_sidebar,
    render_page_header,
    render_stat_card,
    render_panel,
    render_status_badge,
    render_avatar,
    render_main_content_area,
    REFERENCE_COLORS,
    REFERENCE_SHADOWS,
    REFERENCE_RADIUS,
)
from src.database.db import (
    get_all_students,
    get_all_subjects,
    get_teacher_subjects,
    get_all_attendance_logs,
)


def reference_dashboard_screen(teacher_data):
    """
    Render dashboard exactly matching reference/src/routes/index.tsx
    """

    apply_reference_base_styles()

    # Initialize navigation state
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Dashboard"

    # Render TopBar
    render_topbar(
        app_title="AI Attendance",
        user_name=teacher_data.get('name', 'Teacher'),
        user_role="Teacher"
    )

    # Render Sidebar
    render_sidebar(
        active_page=st.session_state.nav_page,
        on_page_change=lambda page: setattr(st.session_state, 'nav_page', page)
    )

    # Main content area
    render_main_content_area()

    # Load data
    students = get_all_students() or []
    subjects = get_teacher_subjects(teacher_data['teacher_id']) or []
    logs = get_all_attendance_logs() or []

    # Calculate stats for today
    today = datetime.now().date()
    today_logs = [log for log in logs if log.get('timestamp') and log['timestamp'].date() == today]

    total_students = len(students)
    present_today = sum(1 for log in today_logs if log.get('is_present'))
    attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0
    late_arrivals = sum(1 for log in today_logs if log.get('status') == 'late')

    # PageHeader with date pill
    date_str = datetime.now().strftime("%A, %B %d")
    render_page_header(
        title="Dashboard",
        subtitle="Overview of today's attendance and key metrics",
        date_pill=f"📅 {date_str}"
    )

    # 4 StatCards in row (exact reference layout)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            icon="👥",
            label="Total Students",
            value=str(total_students),
            hint="Across all classes"
        )

    with col2:
        render_stat_card(
            icon="✓",
            label="Present Today",
            value=str(present_today),
            hint=f"Out of {total_students} total"
        )

    with col3:
        render_stat_card(
            icon="📊",
            label="Attendance Rate",
            value=f"{attendance_rate:.0f}%",
            hint="Today's attendance",
            trend="up" if attendance_rate >= 75 else "down"
        )

    with col4:
        render_stat_card(
            icon="🕐",
            label="Late Arrivals",
            value=str(late_arrivals),
            hint="After 9:00 AM"
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 2-column layout: TrendChart + AIInsight + QuickActions | Today's Attendance
    left_col, right_col = st.columns([2, 1], gap="medium")

    with left_col:
        # TrendChart Panel with Segmented control (reference style)
        st.markdown(f"""
            <div class="ref-panel">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>
                        <div class="ref-panel-title">Attendance Trend</div>
                        <div class="ref-panel-subtitle">Last 7 days average</div>
                    </div>
                    <div style="display: flex; gap: 4px; background: {REFERENCE_COLORS['secondary']}; padding: 4px; border-radius: 10px;">
                        <button style="padding: 6px 14px; border-radius: 7px; font-size: 12.5px; font-weight: 500; background: {REFERENCE_COLORS['card']}; border: none; color: {REFERENCE_COLORS['primary']}; box-shadow: {REFERENCE_SHADOWS['control']};">7D</button>
                        <button style="padding: 6px 14px; border-radius: 7px; font-size: 12.5px; font-weight: 500; background: transparent; border: none; color: {REFERENCE_COLORS['muted_foreground']};">30D</button>
                        <button style="padding: 6px 14px; border-radius: 7px; font-size: 12.5px; font-weight: 500; background: transparent; border: none; color: {REFERENCE_COLORS['muted_foreground']};">All</button>
                    </div>
                </div>

                <!-- Simple trend visualization -->
                <div style="height: 180px; display: flex; align-items: flex-end; gap: 12px; padding: 20px 0;">
                    <div style="flex: 1; height: 75%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 85%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 70%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 90%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 88%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 92%; background: linear-gradient(to top, oklch(0.6 0.2 256 / 0.2), oklch(0.6 0.2 256 / 0.05)); border-radius: 6px 6px 0 0;"></div>
                    <div style="flex: 1; height: 95%; background: linear-gradient(to top, oklch(0.6 0.2 256), oklch(0.6 0.2 256 / 0.4)); border-radius: 6px 6px 0 0;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # AIInsight Card (exact reference style)
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, oklch(0.6 0.2 256 / 0.08), oklch(0.7 0.18 280 / 0.05));
                border: 1px solid {REFERENCE_COLORS['border']};
                border-radius: {REFERENCE_RADIUS['3xl']};
                padding: 20px;
                box-shadow: {REFERENCE_SHADOWS['panel']};
            ">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <div style="width: 32px; height: 32px; border-radius: 10px; background: linear-gradient(135deg, oklch(0.6 0.2 256), oklch(0.7 0.18 280)); display: flex; align-items: center; justify-content: center; font-size: 16px;">✨</div>
                    <div style="font-size: 15px; font-weight: 600; color: {REFERENCE_COLORS['primary']};">AI Attendance Insights</div>
                </div>
                <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: {REFERENCE_COLORS['muted_foreground']}; line-height: 1.8;">
                    <li>Overall attendance is trending upward this week (+5%)</li>
                    <li>BCA-A has the highest attendance rate at 94%</li>
                    <li>Consider following up with 3 students below 75% threshold</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Quick Actions (reference style)
        st.markdown(f"""
            <div class="ref-panel">
                <div class="ref-panel-title">Quick Actions</div>
                <div style="display: flex; gap: 12px; margin-top: 16px;">
                    <button style="
                        flex: 1;
                        padding: 12px;
                        background: {REFERENCE_COLORS['card']};
                        border: 1px solid {REFERENCE_COLORS['border']};
                        border-radius: {REFERENCE_RADIUS['lg']};
                        font-size: 13px;
                        font-weight: 500;
                        color: {REFERENCE_COLORS['primary']};
                        cursor: pointer;
                        transition: all 150ms;
                        box-shadow: {REFERENCE_SHADOWS['control']};
                    " onmouseover="this.style.background='{REFERENCE_COLORS['secondary']}'" onmouseout="this.style.background='{REFERENCE_COLORS['card']}'">
                        📸 Face Attendance
                    </button>
                    <button style="
                        flex: 1;
                        padding: 12px;
                        background: {REFERENCE_COLORS['card']};
                        border: 1px solid {REFERENCE_COLORS['border']};
                        border-radius: {REFERENCE_RADIUS['lg']};
                        font-size: 13px;
                        font-weight: 500;
                        color: {REFERENCE_COLORS['primary']};
                        cursor: pointer;
                        transition: all 150ms;
                        box-shadow: {REFERENCE_SHADOWS['control']};
                    " onmouseover="this.style.background='{REFERENCE_COLORS['secondary']}'" onmouseout="this.style.background='{REFERENCE_COLORS['card']}'">
                        🎤 Voice Attendance
                    </button>
                    <button style="
                        flex: 1;
                        padding: 12px;
                        background: {REFERENCE_COLORS['card']};
                        border: 1px solid {REFERENCE_COLORS['border']};
                        border-radius: {REFERENCE_RADIUS['lg']};
                        font-size: 13px;
                        font-weight: 500;
                        color: {REFERENCE_COLORS['primary']};
                        cursor: pointer;
                        transition: all 150ms;
                        box-shadow: {REFERENCE_SHADOWS['control']};
                    " onmouseover="this.style.background='{REFERENCE_COLORS['secondary']}'" onmouseout="this.style.background='{REFERENCE_COLORS['card']}'">
                        📊 View Reports
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        # Today's Attendance Table (reference AttendanceTable.tsx style)
        st.markdown(f"""
            <div class="ref-panel">
                <div class="ref-panel-title">Today's Attendance</div>
                <div class="ref-panel-subtitle">{present_today} present · {len(today_logs) - present_today} absent</div>

                <div style="margin-top: 16px;">
        """, unsafe_allow_html=True)

        # Display recent attendance logs (max 6 for dashboard)
        recent_logs = today_logs[:6] if today_logs else []

        if recent_logs:
            for log in recent_logs:
                student = next((s for s in students if s['student_id'] == log.get('student_id')), None)
                if student:
                    status = "present" if log.get('is_present') else "absent"
                    if log.get('status') == 'late':
                        status = "late"

                    time_str = log['timestamp'].strftime("%I:%M %p") if log.get('timestamp') else "—"

                    st.markdown(f"""
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 12px;
                            padding: 10px 0;
                            border-bottom: 1px solid {REFERENCE_COLORS['border']};
                        ">
                            {render_avatar(student['name'], 32)}
                            <div style="flex: 1; min-width: 0;">
                                <div style="font-size: 13px; font-weight: 500; color: {REFERENCE_COLORS['primary']};">{student['name']}</div>
                                <div style="font-size: 11.5px; color: {REFERENCE_COLORS['muted_foreground']};">{time_str}</div>
                            </div>
                            {render_status_badge(status)}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: center; padding: 32px 0; color: {REFERENCE_COLORS['muted_foreground']}; font-size: 13px;">
                    No attendance recorded yet today
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # Close main content area
    st.markdown("</div>", unsafe_allow_html=True)

    # Handle navigation via Streamlit's native button clicks in sidebar placeholder
    # (JavaScript postMessage is not reliable in Streamlit, using session state + rerun)

    # Temporary navigation buttons at bottom for testing
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    nav_cols = st.columns(8)
    pages = ["Dashboard", "Attendance", "Students", "Classes", "Analytics", "Reports", "Settings", "Student Portal"]

    for i, page in enumerate(pages):
        with nav_cols[i]:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.nav_page = page
                st.rerun()
