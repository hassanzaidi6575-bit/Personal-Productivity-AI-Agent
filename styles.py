"""
styles.py
---------
Central theme + CSS for the Personal Productivity AI Agent dashboard.
"""

import streamlit as st


# ----------------------------------------------------------------------
# Design tokens
# ----------------------------------------------------------------------

COLORS = {
    "bg": "#0F1117",
    "surface": "#171A23",
    "surface_alt": "#1E212C",
    "border": "#2A2E3A",
    "text": "#E8E9ED",
    "text_muted": "#9198A8",

    "primary": "#6C5CE7",
    "primary_soft": "rgba(108, 92, 231, 0.15)",

    "success": "#2ECC71",
    "success_soft": "rgba(46, 204, 113, 0.15)",

    "warning": "#F5A623",
    "warning_soft": "rgba(245, 166, 35, 0.15)",

    "danger": "#EB5757",
    "danger_soft": "rgba(235, 87, 87, 0.15)",

    "info": "#4FA8F5",
    "info_soft": "rgba(79, 168, 245, 0.15)",
}



STATUS_STYLES = {

    "completed": ("success", "✅ Completed"),
    "done": ("success", "✅ Completed"),

    "in_progress": ("info", "🔄 In Progress"),

    "pending": ("warning", "🕒 Pending"),
    "todo": ("warning", "🕒 Pending"),

    "overdue": ("danger", "⚠ Overdue"),

    "cancelled": ("danger", "✖ Cancelled"),

}



PRIORITY_STYLES = {

    "high": ("danger", "🔺 High"),

    "medium": ("warning", "◆ Medium"),

    "low": ("info", "▽ Low"),

}





def inject_global_styles():

    st.markdown(

        f"""

<style>


/* ---------------------------
   GLOBAL
----------------------------*/


html, body, [class*="css"] {{

    font-family:
    'Inter',
    'Segoe UI',
    sans-serif;

}}



.stApp {{

    background-color:
    {COLORS['bg']};

    color:
    {COLORS['text']};

}}



#MainMenu,
header,
footer {{

    visibility:hidden;

}}




/* ---------------------------
   SIDEBAR
----------------------------*/


section[data-testid="stSidebar"] {{

    background-color:
    {COLORS['surface']};

    border-right:
    1px solid {COLORS['border']};

}}




/* ---------------------------
   CARDS
----------------------------*/


.app-card {{

    background-color:
    {COLORS['surface']};

    border:
    1px solid {COLORS['border']};

    border-radius:
    14px;

    padding:
    22px 24px;

    margin-bottom:
    18px;

}}



.app-card:hover {{

    border-color:
    {COLORS['primary']};

}}





/* ---------------------------
   STAT CARDS
----------------------------*/


.stat-card {{

    background-color:
    {COLORS['surface']};

    border:
    1px solid {COLORS['border']};

    border-radius:
    14px;

    padding:
    20px;

}}



.stat-label {{

    color:
    {COLORS['text_muted']};

    font-size:
    14px;

    font-weight:
    600;

}}



.stat-value {{

    font-size:
    36px;

    font-weight:
    700;

}}





/* ---------------------------
   TASKS
----------------------------*/


.task-title {{

    font-size:
    19px;

    font-weight:
    700;

    color:
    {COLORS['text']};

    margin-bottom:
    10px;

}}



.task-desc {{

    color:
    {COLORS['text_muted']};

    font-size:
    16px;

    line-height:
    1.7;

    margin:
    12px 0;

}}



.task-meta {{

    color:
    {COLORS['text_muted']};

    font-size:
    14px;

    margin-top:
    12px;

    border-top:
    1px solid {COLORS['border']};

    padding-top:
    12px;

}}





/* ---------------------------
   BADGES
----------------------------*/


.badge {{

    display:inline-block;

    padding:
    5px 12px;

    border-radius:
    999px;

    font-size:
    13px;

    font-weight:
    600;

}}



.badge-success {{

background:
{COLORS['success_soft']};

color:
{COLORS['success']};

}}



.badge-warning {{

background:
{COLORS['warning_soft']};

color:
{COLORS['warning']};

}}



.badge-danger {{

background:
{COLORS['danger_soft']};

color:
{COLORS['danger']};

}}



.badge-info {{

background:
{COLORS['info_soft']};

color:
{COLORS['info']};

}}





/* ---------------------------
   HEADINGS
----------------------------*/


.section-title {{

    font-size:
    24px;

    font-weight:
    750;

    color:
    {COLORS['text']};

}}



.section-subtitle {{

    color:
    {COLORS['text_muted']};

    font-size:
    16px;

    margin-bottom:
    22px;

}}






/* ---------------------------
   CHAT
----------------------------*/


.chat-row {{

    display:flex;

    margin-bottom:
    16px;

}}



.chat-row.user {{

    justify-content:flex-end;

}}



.chat-row.agent {{

    justify-content:flex-start;

}}




.chat-bubble {{

    max-width:
    75%;

    padding:
    16px 20px;

    border-radius:
    16px;

    font-size:
    17px;

    line-height:
    1.7;

}}




.chat-bubble.user {{

    background:
    {COLORS['primary']};

    color:white;

}}



.chat-bubble.agent {{

    background:
    {COLORS['surface_alt']};

    border:
    1px solid {COLORS['border']};

    color:
    {COLORS['text']};

}}



.chat-label {{

    font-size:
    13px;

    color:
    {COLORS['text_muted']};

    margin-bottom:
    6px;

}}





/* ---------------------------
   BUTTONS
----------------------------*/


.stButton>button {{

    border-radius:
    10px;

    background:
    {COLORS['surface_alt']};

    color:
    {COLORS['text']};

    font-weight:
    600;

}}



.stButton>button:hover {{

    border-color:
    {COLORS['primary']};

    color:
    {COLORS['primary']};

}}





/* ---------------------------
   INPUTS
----------------------------*/


.stTextInput>div>div>input,

.stTextArea textarea {{

    background:
    {COLORS['surface_alt']};

    color:
    {COLORS['text']};

    border-radius:
    10px;

    border:
    1px solid {COLORS['border']};

    font-size:
    16px;

}}



hr {{

border-color:
{COLORS['border']};

}}



</style>

""",

unsafe_allow_html=True,

    )







def badge(text: str, kind: str = "primary"):

    return f'<span class="badge badge-{kind}">{text}</span>'






def status_badge(status: str):

    kind, label = STATUS_STYLES.get(

        str(status).lower().replace(" ", "_"),

        ("info", str(status).title())

    )

    return badge(label, kind)






def priority_badge(priority: str):

    kind, label = PRIORITY_STYLES.get(

        str(priority).lower(),

        ("info", str(priority).title())

    )

    return badge(label, kind)