import time
from typing import Any, Dict, Optional

import streamlit as st

from backend.workflow import WorkflowManager

st.set_page_config(page_title="启发式学习助手", layout="wide")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    body {background: radial-gradient(circle at 18% 20%, #eef2ff, #f9fbff 30%, #ffffff 65%);}    
    .hero {padding:16px 18px; border-radius:18px; background:linear-gradient(120deg,#e8eeff,#f8fbff); border:1px solid #e5eaf5; box-shadow:0 10px 26px rgba(31,69,138,0.08);} 
    .hero h1 {margin:0; font-size:24px; color:#1a2d52;} 
    .hero p {margin:6px 0 0 0; color:#3b4b68;}
    .flow {display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-top:10px;}
    .flow-step {padding:8px 12px; border-radius:10px; border:1px solid #e4e8f0; background:#fff; box-shadow:0 4px 14px rgba(0,0,0,0.04); min-width:170px;}
    .flow-title {font-weight:800; color:#1f2f4d; font-size:14px;}
    .flow-status {margin-top:2px; font-size:12px; color:#4a5770;}
    .flow-step.ok {border-color:#c3e7d5; background:#f4fbf7;}
    .flow-step.pending {border-color:#f1d9a9; background:#fff9ed;}
    .flow-step.fail {border-color:#f1c0c0; background:#fff5f5;}
    .flow-arrow {font-size:18px; color:#7b89a6; font-weight:700;}
    .card {padding:16px 16px; border-radius:14px; border:1px solid #e5eaf0; background:#fff; box-shadow:0 6px 18px rgba(0,0,0,0.05); margin-top:12px;}
    .section-title {font-weight:800; font-size:16px; margin-bottom:6px; color:#1c2f47;}
    .dialog-line {padding:10px 12px; border-radius:10px; margin-bottom:8px; line-height:1.6; border:1px solid #e7edf5;}
    .dialog-teacher {background:#eef8f0; color:#1f5d2f;}
    .dialog-student {background:#f5f0ff; color:#3d2b70;}
    .dialog-plain {background:#f8fafc; color:#30405a;}
    .chat-wrap {padding:10px 10px; background:linear-gradient(180deg,#f7f9ff,#ffffff); border-radius:14px; border:1px solid #e7ecf6;}
    .chat-row {display:flex; gap:10px; align-items:flex-end; margin:10px 0;}
    .chat-row.user {flex-direction:row-reverse;}
    .chat-avatar {width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px;}
    .chat-avatar.user {background:#e6f4ff; color:#1b5ea6;}
    .chat-avatar.ai {background:#eef7ee; color:#1f6b3a;}
    .chat-bubble {max-width:78%; padding:10px 12px; border-radius:14px; line-height:1.6; border:1px solid #e7edf5; background:#ffffff; box-shadow:0 4px 10px rgba(31,69,138,0.06);}
    .chat-bubble.user {background:#eef5ff; border-top-right-radius:6px;}
    .chat-bubble.ai {background:#f6fff7; border-top-left-radius:6px;}
    .chat-meta {font-size:12px; color:#6b778c; margin:2px 6px;}
    .chat-header {display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:6px;}
    .chat-title {font-weight:800; color:#1c2f47;}
    .chat-badge {font-size:12px; padding:2px 8px; border-radius:999px; background:#eaf2ff; color:#2d4f8c; border:1px solid #d6e2ff;}
    .history-item {padding:8px 10px; border-bottom:1px dashed #e5e8ef;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helpers ----------

def stream_text(container, text: str, delay: float = 0.03, chunk_size: int = 14) -> None:
    if not text:
        return
    placeholder = container.empty()
    buffer = ""
    for i in range(0, len(text), chunk_size):
        buffer += text[i : i + chunk_size]
        placeholder.markdown(buffer)
        time.sleep(delay)
    placeholder.markdown(buffer)


def stream_dialog_lines(container, text: str, delay: float = 0.05) -> None:
    container.empty()
    if not text:
        return
    placeholder = container.empty()
    html = ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        lower = ln.lower()
        role_class = "dialog-plain"
        if lower.startswith("老师") or lower.startswith("教師") or lower.startswith("teacher"):
            role_class = "dialog-teacher"
        elif lower.startswith("学生") or lower.startswith("student"):
            role_class = "dialog-student"
        content = ln.split(":", 1)[1].strip() if ":" in ln else ln
        html += f"<div class='dialog-line {role_class}'>{content}</div>"
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(delay)


def _chat_rows(question: str, answer: str) -> str:
    rows = ""
    if question:
        rows += (
            "<div class='chat-row user'>"
            "<div class='chat-avatar user'>我</div>"
            f"<div class='chat-bubble user'>{question}</div>"
            "</div>"
            "<div class='chat-meta' style='text-align:right;'>用户提问</div>"
        )
    parts = [p.strip() for p in (answer or "").split("\n\n") if p.strip()] or ([] if not answer else [answer])
    for part in parts:
        rows += (
            "<div class='chat-row ai'>"
            "<div class='chat-avatar ai'>AI</div>"
            f"<div class='chat-bubble ai'>{part}</div>"
            "</div>"
        )
    return rows


def stream_explanation_chat_history(
    container,
    blocks,
    current_question: Optional[str] = None,
    current_answer: Optional[str] = None,
    delay: float = 0.03,
) -> None:
    """Render explanation as a single chat history, appending new messages below previous ones."""
    container.empty()
    placeholder = container.empty()
    header = (
        "<div class='chat-header'>"
        "<div class='chat-title'>用户与AI对话</div>"
        "<div class='chat-badge'>已审核</div>"
        "</div>"
    )
    wrap_start = "<div class='chat-wrap'>"
    wrap_end = "</div>"
    history_html = "".join(
        _chat_rows(block.get("question", ""), block.get("explanation", "")) for block in blocks
    )
    if not current_answer:
        placeholder.markdown(header + wrap_start + history_html + wrap_end, unsafe_allow_html=True)
        return

    current_user = _chat_rows(current_question or "", "")
    ai_prefix = (
        "<div class='chat-row ai'>"
        "<div class='chat-avatar ai'>AI</div>"
        "<div class='chat-bubble ai'>"
    )
    ai_suffix = "</div></div>"
    buffer = ""
    for i in range(0, len(current_answer), 16):
        buffer += current_answer[i : i + 16]
        placeholder.markdown(
            header + wrap_start + history_html + current_user + ai_prefix + buffer + ai_suffix + wrap_end,
            unsafe_allow_html=True,
        )
        time.sleep(delay)
    placeholder.markdown(
        header + wrap_start + history_html + current_user + ai_prefix + buffer + ai_suffix + wrap_end,
        unsafe_allow_html=True,
    )


def render_flow(container, steps) -> None:
    html = "<div class='flow'>"
    for idx, step in enumerate(steps):
        tone_class = {"pending": "pending", "ok": "ok", "fail": "fail"}.get(step.get("tone"), "pending")
        html += (
            f"<div class='flow-step {tone_class}'>"
            f"<div class='flow-title'>{step.get('title')}</div>"
            f"<div class='flow-status'>{step.get('status')}</div>"
            "</div>"
        )
        if idx < len(steps) - 1:
            html += "<div class='flow-arrow'>→</div>"
    html += "</div>"
    container.markdown(html, unsafe_allow_html=True)


# ---------- State ----------
if "workflow_manager" not in st.session_state:
    st.session_state["workflow_manager"] = WorkflowManager()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "dialog_done" not in st.session_state:
    st.session_state["dialog_done"] = False
if "content_blocks" not in st.session_state:
    st.session_state["content_blocks"] = []  # list of {dialog, explanation, question}
if "flow_steps" not in st.session_state:
    st.session_state["flow_steps"] = []

# ---------- Layout ----------
st.markdown(
    "<div class='hero'><h1>启发式学习助手</h1><p>分阶段生成 · 审核通过后展示 · 首问含对话，之后仅输出解释</p></div>",
    unsafe_allow_html=True,
)

flow_bar = st.empty()

def reset_flow(show_dialog: bool) -> None:
    step2_status = "等待中" if show_dialog else "本轮跳过"
    st.session_state["flow_steps"] = [
        {"title": "1. 提示词优化", "status": "等待中", "tone": "pending"},
        {"title": "2. 引入对话（仅首轮）", "status": step2_status, "tone": "pending"},
        {"title": "3. 详细解释", "status": "等待中", "tone": "pending"},
    ]
    render_flow(flow_bar, st.session_state["flow_steps"])


def update_flow_step(index: int, status: str, tone: str) -> None:
    st.session_state["flow_steps"][index]["status"] = status
    st.session_state["flow_steps"][index]["tone"] = tone
    render_flow(flow_bar, st.session_state["flow_steps"])


reset_flow(show_dialog=not st.session_state["dialog_done"])

dialog_section = st.container()
explain_section = st.container()

with dialog_section:
    # show past reviewed dialog blocks
    for block in st.session_state["content_blocks"]:
        st.markdown("<div class='card'><div class='section-title'>引入对话</div>", unsafe_allow_html=True)
        dialog_box_prev = st.empty()
        if block.get("dialog"):
            dialog_box_prev.markdown("", unsafe_allow_html=True)
            dialog_box_prev.markdown("", unsafe_allow_html=True)
            stream_dialog_lines(dialog_box_prev, block.get("dialog", ""), delay=0)
        st.markdown("</div>", unsafe_allow_html=True)

with explain_section:
    st.markdown("<div class='card'><div class='section-title'>用户与AI详细解释对话</div>", unsafe_allow_html=True)
    explain_box = st.empty()
    stream_explanation_chat_history(
        explain_box,
        st.session_state["content_blocks"],
        delay=0,
    )
    st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("输入问题：首轮展示对话+解释，后续仅展示解释（均需审核通过）")

if user_input:
    if not user_input.strip():
        st.warning("请输入有效问题。")
        st.stop()

    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    show_dialog = not st.session_state["dialog_done"]
    reset_flow(show_dialog=show_dialog)

    with dialog_section:
        st.markdown("<div class='card'><div class='section-title'>引入对话</div>", unsafe_allow_html=True)
        dialog_box = st.empty()
        st.markdown("</div>", unsafe_allow_html=True)


    captured: Dict[str, Any] = {}

    def progress_callback(event: Dict[str, Any]) -> None:
        etype = event.get("type")
        if etype == "optimize_start":
            update_flow_step(0, "进行中…", "pending")
        elif etype == "optimize_done":
            captured["optimized_prompt"] = event.get("prompt", "")
            update_flow_step(0, "完成", "ok")
        elif etype == "dialog_generation_start" and show_dialog:
            update_flow_step(1, f"生成中 (第{event.get('attempt', 1)}次)…", "pending")
        elif etype == "dialog_generation_done" and show_dialog:
            captured["dialog_content"] = event.get("content", "")
        elif etype == "dialog_review_start" and show_dialog:
            update_flow_step(1, f"审核中 (第{event.get('attempt', 1)}次)…", "pending")
        elif etype == "dialog_review_done" and show_dialog:
            if event.get("passed"):
                update_flow_step(1, "审核通过", "ok")
                stream_dialog_lines(dialog_box, captured.get("dialog_content", ""))
            else:
                update_flow_step(1, "未通过，重试…", "pending")
        elif etype == "dialog_stop" and show_dialog:
            update_flow_step(1, "多次未通过", "fail")
        elif etype == "explanation_generation_start":
            update_flow_step(2, f"生成中 (第{event.get('attempt', 1)}次)…", "pending")
        elif etype == "explanation_generation_done":
            captured["explanation_content"] = event.get("content", "")
        elif etype == "explanation_review_start":
            update_flow_step(2, f"审核中 (第{event.get('attempt', 1)}次)…", "pending")
        elif etype == "explanation_review_done":
            if event.get("passed"):
                update_flow_step(2, "审核通过，展示中…", "ok")
            else:
                update_flow_step(2, "未通过，重试…", "pending")
        elif etype == "explanation_stop":
            update_flow_step(2, "多次未通过", "fail")
        elif etype == "final_success":
            captured["final_content"] = event.get("content", "")
            update_flow_step(2, "审核通过，展示完成", "ok")
            if show_dialog:
                stream_dialog_lines(dialog_box, captured.get("dialog_content", ""))
                st.session_state["dialog_done"] = True
            stream_explanation_chat_history(
                explain_box,
                st.session_state["content_blocks"],
                current_question=user_input,
                current_answer=captured["final_content"],
                delay=0.025,
            )
            st.session_state["content_blocks"].append(
                {
                    "dialog": captured.get("dialog_content", "") if show_dialog else "",
                    "explanation": captured.get("final_content", ""),
                    "question": user_input,
                }
            )
        elif etype == "final_failed":
            update_flow_step(2, "审核未通过", "fail")

    explanation_history = "\n\n".join(
        [block.get("explanation", "").strip() for block in st.session_state["content_blocks"] if block.get("explanation")]
    )

    with st.spinner("工作流执行中…"):
        result = st.session_state["workflow_manager"].process_request(
            user_input,
            explanation_history=explanation_history,
            progress_callback=progress_callback,
        )

    if result.get("error"):
        update_flow_step(2, f"发生错误：{result['error']}", "fail")
    else:
        final_reply = captured.get("final_content") or result.get("final_content") or ""
        if final_reply:
            st.session_state["chat_history"].append({"role": "assistant", "content": final_reply})

