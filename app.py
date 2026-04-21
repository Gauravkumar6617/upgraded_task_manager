import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Task Manager",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — dark industrial / utilitarian
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Page title ── */
.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #f0f0f0;
    border-left: 4px solid #c8f135;
    padding-left: 1rem;
    margin-bottom: 0.2rem;
}
.page-sub {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 2.5rem;
    padding-left: 1.25rem;
    font-family: 'Space Mono', monospace;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c8f135;
    margin-bottom: 0.8rem;
    margin-top: 2rem;
}

/* ── Task card ── */
.task-card {
    background: #161616;
    border: 1px solid #252525;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    transition: border-color 0.15s;
}
.task-card:hover { border-color: #3a3a3a; }

.task-id {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    min-width: 28px;
    margin-top: 3px;
}
.task-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: #e8e8e8;
    flex: 1;
}
.task-desc {
    font-size: 0.8rem;
    color: #777;
    margin-top: 2px;
}
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    padding: 2px 8px;
    border-radius: 2px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-done   { background: #1a2e0a; color: #c8f135; border: 1px solid #2d4a0f; }
.badge-todo   { background: #1a1a2e; color: #7b9fff; border: 1px solid #2a2a4a; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
    border-color: #c8f135 !important;
    box-shadow: 0 0 0 1px #c8f13530 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #c8f135 !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.45rem 1.1rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* delete button variant */
button[kind="secondary"] {
    background: #1e0a0a !important;
    color: #ff6b6b !important;
    border: 1px solid #3a1a1a !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    border-radius: 4px !important;
}

/* ── Number input ── */
.stNumberInput > div > div > input {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr { border-color: #1e1e1e; margin: 2rem 0; }

/* ── Status bar ── */
.status-bar {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.status-online { color: #c8f135; }
.status-offline { color: #ff6b6b; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #333;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    border: 1px dashed #1e1e1e;
    border-radius: 6px;
}

/* ── Toast-like alerts ── */
.stAlert {
    background: #161616 !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────
def api_get(path):
    try:
        r = requests.get(f"{API_BASE}{path}", timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the backend running?"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return None, str(e)

def api_post(path, payload):
    try:
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return None, str(e)

def api_put(path, payload):
    try:
        r = requests.put(f"{API_BASE}{path}", json=payload, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return None, str(e)

def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", timeout=5)
        r.raise_for_status()
        return True, None
    except requests.exceptions.HTTPError as e:
        return False, f"HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return False, str(e)

def check_health():
    try:
        r = requests.get(f"{API_BASE}/", timeout=2)
        return r.status_code == 200
    except:
        return False


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────
def render_task_card(task):
    done = task.get("completed", False)
    badge = '<span class="badge badge-done">done</span>' if done else '<span class="badge badge-todo">todo</span>'
    desc_html = f'<div class="task-desc">{task.get("description", "")}</div>' if task.get("description") else ""
    st.markdown(f"""
    <div class="task-card">
        <div class="task-id">#{task['id']:03d}</div>
        <div style="flex:1">
            <div class="task-title">{task['title']}</div>
            {desc_html}
        </div>
        {badge}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="page-title">✦ Task Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">connected to FastAPI · slowapi rate-limited</div>', unsafe_allow_html=True)

# API status bar
online = check_health()
status_dot = '<span class="status-online">● ONLINE</span>' if online else '<span class="status-offline">● OFFLINE</span>'
tasks_data, _ = api_get("/tasks/?limit=1000")
count = len(tasks_data) if tasks_data else 0
st.markdown(f"""
<div class="status-bar">
    <span>API {status_dot}</span>
    <span>{API_BASE}/tasks</span>
    <span>{count} task(s) total</span>
    <span>{datetime.now().strftime("%H:%M:%S")}</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LAYOUT: two columns
# ─────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")


# ══════════════════════════════════════════════
# LEFT — Task list
# ══════════════════════════════════════════════
with left:
    st.markdown('<div class="section-label">// all tasks</div>', unsafe_allow_html=True)

    # Filter
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        search = st.text_input("Search", placeholder="filter by title…", label_visibility="collapsed")
    with filter_col2:
        status_filter = st.selectbox("Status", ["All", "Todo", "Done"], label_visibility="collapsed")

    tasks_data, err = api_get("/tasks/?limit=1000")

    if err:
        st.error(err)
    elif not tasks_data:
        st.markdown('<div class="empty-state">no tasks yet.<br/>create one →</div>', unsafe_allow_html=True)
    else:
        filtered = tasks_data
        if search:
            filtered = [t for t in filtered if search.lower() in t["title"].lower()]
        if status_filter == "Done":
            filtered = [t for t in filtered if t.get("completed")]
        elif status_filter == "Todo":
            filtered = [t for t in filtered if not t.get("completed")]

        if not filtered:
            st.markdown('<div class="empty-state">no tasks match the filter.</div>', unsafe_allow_html=True)
        else:
            for task in filtered:
                render_task_card(task)

    # ── DELETE section ──
    st.markdown('<div class="section-label">// delete task</div>', unsafe_allow_html=True)
    del_col1, del_col2 = st.columns([2, 1])
    with del_col1:
        del_id = st.number_input("Task ID to delete", min_value=1, step=1, label_visibility="collapsed", placeholder="task id…")
    with del_col2:
        if st.button("DELETE", key="delete_btn"):
            ok, err = api_delete(f"/tasks/{int(del_id)}")
            if ok:
                st.success(f"Task #{int(del_id)} deleted.")
                st.rerun()
            else:
                st.error(err)


# ══════════════════════════════════════════════
# RIGHT — Create / Update
# ══════════════════════════════════════════════
with right:

    # ── CREATE ──
    st.markdown('<div class="section-label">// new task</div>', unsafe_allow_html=True)
    with st.container():
        new_title = st.text_input("Title", placeholder="Task title…", key="new_title")
        new_desc  = st.text_area("Description", placeholder="Optional description…", key="new_desc", height=80)
        new_done  = st.checkbox("Mark as completed", key="new_done")

        if st.button("CREATE TASK", key="create_btn"):
            if not new_title.strip():
                st.warning("Title is required.")
            else:
                payload = {
                    "title": new_title.strip(),
                    "description": new_desc.strip() or None,
                    "completed": new_done,
                }
                result, err = api_post("/tasks/", payload)
                if result:
                    st.success(f"Created task #{result['id']}!")
                    st.rerun()
                else:
                    st.error(err)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── UPDATE ──
    st.markdown('<div class="section-label">// update task</div>', unsafe_allow_html=True)
    upd_id    = st.number_input("Task ID", min_value=1, step=1, key="upd_id", placeholder="task id…")
    upd_title = st.text_input("New title", placeholder="Updated title…", key="upd_title")
    upd_desc  = st.text_area("New description", placeholder="Updated description…", key="upd_desc", height=70)
    upd_done  = st.checkbox("Completed", key="upd_done")

    if st.button("UPDATE TASK", key="update_btn"):
        if not upd_title.strip():
            st.warning("Title is required.")
        else:
            payload = {
                "title": upd_title.strip(),
                "description": upd_desc.strip() or None,
                "completed": upd_done,
            }
            result, err = api_put(f"/tasks/{int(upd_id)}", payload)
            if result:
                st.success(f"Task #{result['id']} updated!")
                st.rerun()
            else:
                st.error(err)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── RATE LIMIT INFO ──
    st.markdown('<div class="section-label">// rate limits</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.68rem; color:#444; line-height:2;">
        GET  /tasks    →  30 / min<br>
        POST /tasks    →  10 / min<br>
        PUT  /tasks/:id →  10 / min<br>
        DELETE /tasks/:id →   5 / min
    </div>
    """, unsafe_allow_html=True)