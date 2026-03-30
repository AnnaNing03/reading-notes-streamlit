import streamlit as st
from datetime import date

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(
    page_title="私の书房",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. 极致精修 CSS
# ==========================================
st.markdown(
    """
<style>
    /* 隐藏 Streamlit 默认 UI 元素 */
    [data-testid="stSidebar"], section[data-testid="stSidebarNav"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 全局背景 */
    .stApp {
        background-color: #FDFCF8;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 512px !important;
    }

    /* 书架容器 */
    .bookshelf {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        justify-content: center;
        padding: 20px 10px 12px;
        position: relative;
    }
    .bookshelf::after {
        content: '';
        display: block;
        width: 100%;
        height: 10px;
        background: linear-gradient(180deg, #C4A882 0%, #A8865C 40%, #8B6E47 100%);
        border-radius: 0 0 4px 4px;
        box-shadow: 0 4px 8px rgba(100, 70, 40, 0.25);
        position: absolute;
        bottom: -2px;
        left: 0;
    }

    /* 书本卡片（竖立书脊样式） */
    .book-card {
        width: 110px;
        min-height: 160px;
        border-radius: 4px 10px 10px 4px;
        padding: 16px 10px 12px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 6px;
        box-shadow: 3px 3px 8px rgba(80, 50, 20, 0.18), inset -2px 0 4px rgba(0,0,0,0.06);
        border-left: 5px solid rgba(0,0,0,0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
        position: relative;
    }
    .book-card:hover {
        transform: translateY(-6px);
        box-shadow: 4px 8px 16px rgba(80, 50, 20, 0.25), inset -2px 0 4px rgba(0,0,0,0.06);
    }
    .book-title {
        font-size: 0.85em;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.3;
        word-break: break-all;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .book-author {
        font-size: 0.65em;
        color: rgba(255,255,255,0.8);
        margin-top: 2px;
    }
    .book-count {
        font-size: 0.6em;
        color: rgba(255,255,255,0.7);
        letter-spacing: 1px;
        margin-top: auto;
        padding-top: 6px;
        border-top: 1px solid rgba(255,255,255,0.2);
        width: 100%;
    }

    /* 笔记气泡样式 */
    .note-bubble {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 4px 20px 20px 20px;
        margin-bottom: 16px;
        border-left: 4px solid #D4A373;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.03);
    }

    /* 统计卡片 */
    .stats-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(140, 111, 86, 0.08);
        text-align: center;
        border: 1px solid #EAE2D6;
    }
    .stats-number {
        font-size: 28px;
        font-weight: 700;
        color: #582F0E;
    }
    .stats-label {
        font-size: 12px;
        color: #BCB4A8;
        letter-spacing: 1px;
    }

    /* 个人中心卡片 */
    .profile-card {
        background: white;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(140, 111, 86, 0.08);
        border: 1px solid #EAE2D6;
        margin-bottom: 16px;
    }

    /* 海报预览 */
    .poster-preview {
        background: linear-gradient(135deg, #FDFCF8 0%, #f0e6d3 100%);
        border-radius: 20px;
        padding: 28px 24px;
        margin: 12px 0;
        border: 1px solid #EAE2D6;
    }

    /* 表单元素圆角 */
    .stButton > button {
        border-radius: 12px !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 12px !important;
        border-color: #EAE2D6 !important;
    }

    /* 认证页面样式 */
    .auth-header {
        text-align: center;
        padding: 40px 0 20px;
    }
    .auth-header h1 {
        font-size: 24px;
        color: #582F0E;
        margin-top: 12px;
    }
    .auth-header p {
        color: #8C6F56;
        font-size: 14px;
    }

    /* 空状态 */
    .empty-state {
        text-align: center;
        padding: 60px 0;
        color: #BCB4A8;
    }
    .empty-state .icon {
        font-size: 48px;
        opacity: 0.4;
    }
    .empty-state p {
        font-size: 14px;
        margin-top: 12px;
    }

    /* 节标签 */
    .section-label {
        font-size: 11px;
        color: #BCB4A8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. 导入工具模块
# ==========================================
from utils.auth import check_auth, get_user_email, get_user_id, login, logout, register
from utils.database import (
    create_book,
    create_note,
    delete_note,
    fetch_books,
    fetch_books_for_year,
    fetch_note_by_id,
    fetch_notes,
    fetch_notes_for_book,
    fetch_years,
)
from utils.poster import POSTER_STYLES, create_poster_image, generate_poster_content

# ==========================================
# 4. Session State 初始化
# ==========================================
if "page" not in st.session_state:
    st.session_state["page"] = "书架"
if "user" not in st.session_state:
    st.session_state["user"] = None


def navigate(page: str, **kwargs: object) -> None:
    """导航到指定页面"""
    st.session_state["page"] = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


# ===================================================================
# 5. 认证页面（登录/注册）
# ===================================================================
def show_auth_page() -> None:
    st.markdown(
        '<div class="auth-header">'
        '<div style="font-size:48px;">📖</div>'
        "<h1>私の书房</h1>"
        "<p>记录你的阅读感悟</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(["登录", "注册"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("邮箱", placeholder="请输入邮箱", key="login_email")
            password = st.text_input(
                "密码", type="password", placeholder="请输入密码", key="login_pw"
            )
            submitted = st.form_submit_button("登录", use_container_width=True)
            if submitted:
                if email and password:
                    ok, err = login(email, password)
                    if ok:
                        st.rerun()
                    else:
                        st.error(f"登录失败: {err}")
                else:
                    st.warning("请填写邮箱和密码")

    with tab_register:
        with st.form("register_form"):
            email = st.text_input("邮箱", placeholder="请输入邮箱", key="reg_email")
            password = st.text_input(
                "密码",
                type="password",
                placeholder="请输入密码（至少6位）",
                key="reg_pw",
            )
            submitted = st.form_submit_button("注册", use_container_width=True)
            if submitted:
                if email and password:
                    if len(password) < 6:
                        st.warning("密码至少需要6位")
                    else:
                        ok, err = register(email, password)
                        if ok:
                            st.success("注册成功！")
                            st.rerun()
                        else:
                            st.error(f"注册失败: {err}")
                else:
                    st.warning("请填写邮箱和密码")


# ===================================================================
# 6. 导航栏
# ===================================================================
def show_navigation() -> None:
    """显示顶部导航栏"""
    current = st.session_state.get("page", "书架")
    pages = [
        ("📚 书架", "书架"),
        ("✏️ 记录", "添加"),
        ("🎨 总结", "总结"),
        ("👤 我的", "个人"),
    ]

    cols = st.columns(len(pages))
    for col, (label, page_name) in zip(cols, pages):
        with col:
            btn_type = "primary" if current == page_name else "secondary"
            if st.button(label, key=f"nav_{page_name}", use_container_width=True, type=btn_type):
                # Clear sub-page state when navigating
                st.session_state.pop("current_book", None)
                st.session_state.pop("poster_content", None)
                st.session_state.pop("poster_book", None)
                navigate(page_name)


# ===================================================================
# 7. 页面 A: 我的书架
# ===================================================================
def show_bookshelf() -> None:
    st.markdown(
        "<h2 style='text-align:center; color:#582F0E;'>我的私藏书架</h2>",
        unsafe_allow_html=True,
    )

    user_id = get_user_id()

    # 添加书本表单
    with st.expander("➕ 添加新书到书架", expanded=False):
        with st.form("add_book_form"):
            new_book_name = st.text_input("书名 *", placeholder="请输入书名")
            new_book_author = st.text_input("作者", placeholder="请输入作者（选填）")
            if st.form_submit_button("添加到书架", use_container_width=True):
                if not new_book_name or not new_book_name.strip():
                    st.warning("请输入书名")
                else:
                    ok = create_book(
                        user_id,
                        new_book_name.strip(),
                        new_book_author.strip() if new_book_author else "",
                    )
                    if ok:
                        st.success(f"《{new_book_name.strip()}》已加入书架")
                        st.rerun()

    books = fetch_books(user_id)

    if not books:
        st.markdown(
            '<div class="empty-state">'
            '<div class="icon">📚</div>'
            "<p>书架空空如也</p>"
            '<p style="font-size:12px;">点击上方「➕ 添加新书」开始吧</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        return

    # 书本配色方案（循环使用）
    book_colors = [
        "#8B4513",  # 棕褐色
        "#2F4F4F",  # 暗石板灰
        "#800020",  # 勃良第红
        "#1B4332",  # 深绿
        "#3B3B6D",  # 暗蓝
        "#704214",  # 赫色
        "#5C4033",  # 深咖啡
        "#4A0E4E",  # 深紫
    ]

    # 渲染书架
    books_html = ""
    for i, book in enumerate(books):
        color = book_colors[i % len(book_colors)]
        author_html = (
            f'<div class="book-author">{book["author"]}</div>'
            if book.get("author")
            else ""
        )
        books_html += f"""<div class="book-card" style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);" data-book-idx="{i}">
            <div class="book-title">《{book['book_name']}》</div>
            {author_html}
            <div class="book-count">{book['count']} 条感悟</div>
        </div>"""

    st.markdown(
        f'<div class="bookshelf">{books_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")  # 间距

    # 用 Streamlit 按钮实现点击进入（小字按钮）
    cols = st.columns(min(len(books), 4))
    for i, book in enumerate(books):
        with cols[i % min(len(books), 4)]:
            if st.button(
                f"打开《{book['book_name']}》",
                key=f"book_btn_{i}",
                use_container_width=True,
            ):
                navigate("详情", current_book=str(book["book_name"]))


# ===================================================================
# 8. 页面 B: 书籍详情页
# ===================================================================
def show_book_detail() -> None:
    book_name: str = st.session_state.get("current_book", "")
    user_id = get_user_id()

    if not book_name:
        st.warning("未选择书籍")
        if st.button("返回书架"):
            navigate("书架")
        return

    # 顶部导航
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← 返回书架", key="back_shelf"):
            navigate("书架")
    with col2:
        if st.button("🎨 生成海报", key="gen_poster_btn"):
            with st.spinner("正在用 AI 生成海报文案..."):
                book_notes = fetch_notes_for_book(user_id, book_name)
                if not book_notes:
                    st.error("未找到该书的笔记")
                else:
                    poster_content = generate_poster_content(book_name, book_notes)
                    if poster_content:
                        st.session_state["poster_content"] = poster_content
                        st.session_state["poster_book"] = book_name
                        st.rerun()

    st.markdown(
        f"<h3 style='color:#582F0E; margin-bottom:4px;'>📖 {book_name}</h3>",
        unsafe_allow_html=True,
    )

    # 显示海报（如果已生成）
    poster_content = st.session_state.get("poster_content")
    if poster_content and st.session_state.get("poster_book") == book_name:
        _show_poster_result(poster_content, book_name)

    # 记录区
    with st.expander("🖋️ 记录此刻灵感", expanded=False):
        with st.form("add_note_detail_form"):
            new_quote = st.text_area("摘抄金句 *", placeholder="记录下触动你的句子...")
            new_thought = st.text_area("我的感悟 *", placeholder="写下你的思考...")
            note_date = st.date_input("日期", value=date.today())
            if st.form_submit_button("保存记录", use_container_width=True):
                if not new_quote or not new_quote.strip():
                    st.warning("请输入摘抄金句")
                elif not new_thought or not new_thought.strip():
                    st.warning("请输入你的感悟")
                else:
                    ok = create_note(
                        user_id,
                        book_name,
                        new_quote.strip(),
                        new_thought.strip(),
                        note_date,
                    )
                    if ok:
                        st.success("已编入笔记")
                        st.rerun()

    # 笔记流
    notes = fetch_notes(user_id, book_name=book_name)
    if not notes:
        st.markdown(
            '<div class="empty-state">'
            '<div class="icon">📝</div>'
            "<p>还没有笔记</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"<p style='color:#BCB4A8; font-size:0.85em; margin-bottom:12px;'>"
        f"共 {len(notes)} 条感悟</p>",
        unsafe_allow_html=True,
    )

    for note in notes:
        st.markdown(
            f"""<div class="note-bubble">
                <div style="color:#BCB4A8; font-size:0.8em; margin-bottom:8px;">{note['date']}</div>
                <div style="font-style:italic; color:#333; margin-bottom:10px; line-height:1.6;">
                    「 {note['sentence']} 」</div>
                <div style="font-size:0.9em; color:#666; border-top:1px solid #F5F5F5;
                    padding-top:8px;">💡 {note['thought']}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("🗑️ 删除", key=f"del_{note['id']}", use_container_width=True):
            if delete_note(note["id"], user_id):
                st.success("已删除")
                st.rerun()


def _show_poster_result(poster_content: dict, book_name: str) -> None:
    """展示海报预览和下载按钮"""
    st.markdown("#### 📄 海报预览")
    st.markdown(
        f"""<div class="poster-preview">
            <h3 style="text-align:center; font-family:Georgia,serif;
                color:#582F0E; margin-bottom:4px;">{poster_content.get('title', '')}</h3>
            <p style="text-align:center; font-size:12px; color:#BCB4A8;">
                《{book_name}》</p>
            <div style="background:rgba(255,255,255,0.6); border-radius:12px;
                padding:16px; margin:20px 0; text-align:center;">
                <p style="font-style:italic; font-family:Georgia,serif;
                    font-size:14px; color:#333;">
                    "{poster_content.get('quote', '')}"</p>
            </div>
            <p class="section-label">整体感悟</p>
            <p style="font-size:13px; color:#333; line-height:1.6;">
                {poster_content.get('summary', '')}</p>
            <p class="section-label" style="margin-top:16px;">思考精华</p>
            <p style="font-size:13px; color:#333; font-family:Georgia,serif;
                font-weight:500;">{poster_content.get('insight', '')}</p>
            <hr style="border:none; border-top:1px solid rgba(0,0,0,0.08);
                margin:20px 0 12px;">
            <p style="text-align:center; font-size:11px; color:#BCB4A8;">
                私の书房 · 用阅读丈量世界</p>
        </div>""",
        unsafe_allow_html=True,
    )

    # 生成可下载图片
    with st.spinner("正在生成海报图片..."):
        img_bytes = create_poster_image(
            poster_content,
            book_name,
            date.today().isoformat(),
        )
        st.download_button(
            label="📥 下载海报图片",
            data=img_bytes,
            file_name=f"{book_name}-读书海报.png",
            mime="image/png",
            use_container_width=True,
        )

    if st.button("关闭海报", use_container_width=True, key="close_poster"):
        st.session_state.pop("poster_content", None)
        st.session_state.pop("poster_book", None)
        st.rerun()


# ===================================================================
# 9. 页面 C: 添加笔记
# ===================================================================
def show_add_note() -> None:
    st.markdown(
        "<h2 style='text-align:center; color:#582F0E;'>记录此刻灵感</h2>",
        unsafe_allow_html=True,
    )

    user_id = get_user_id()

    with st.form("add_note_form"):
        book_name = st.text_input("作品 *", placeholder="请输入作品名称")
        sentence = st.text_area(
            "摘抄金句 *", placeholder="记录下触动你的句子...", height=120
        )
        thought = st.text_area(
            "我的感悟 *", placeholder="写下你的思考和感悟...", height=120
        )
        note_date = st.date_input("日期", value=date.today())
        submitted = st.form_submit_button("保存笔记", use_container_width=True)

        if submitted:
            if not book_name or not book_name.strip():
                st.warning("请输入书名")
            elif not sentence or not sentence.strip():
                st.warning("请输入摘抄金句")
            elif not thought or not thought.strip():
                st.warning("请输入你的感悟")
            else:
                ok = create_note(
                    user_id,
                    book_name.strip(),
                    sentence.strip(),
                    thought.strip(),
                    note_date,
                )
                if ok:
                    st.success("保存成功！")
                    navigate("书架")


# ===================================================================
# 10. 页面 D: 读书总结（AI 海报生成）
# ===================================================================
def show_summary() -> None:
    st.markdown(
        "<h2 style='text-align:center; color:#582F0E;'>读书总结</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#BCB4A8; font-size:13px; margin-bottom:20px;'>"
        "选择一本书，AI 为你生成精美读书海报</p>",
        unsafe_allow_html=True,
    )

    user_id = get_user_id()
    books = fetch_books(user_id)

    if not books:
        st.markdown(
            '<div class="empty-state">'
            '<div class="icon">🎨</div>'
            "<p>还没有读书记录</p>"
            '<p style="font-size:12px;">先去添加笔记，再来生成总结海报</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        return

    book_names = [str(b["book_name"]) for b in books]

    # 选择书籍
    selected_book = st.selectbox(
        "📖 选择书籍",
        book_names,
        key="summary_book_select",
        format_func=lambda x: f"《{x}》",
    )

    # 选择时间跨度
    time_options = {
        "全部": None,
        "最近一周": "week",
        "最近一个月": "month",
        "最近一年": "year",
    }
    selected_time_label = st.selectbox(
        "📅 时间范围",
        list(time_options.keys()),
        key="summary_time_select",
    )
    time_range = time_options[selected_time_label]

    # 选择风格
    style_names = list(POSTER_STYLES.keys())
    selected_style = st.selectbox(
        "🎨 海报风格",
        style_names,
        key="summary_style_select",
    )

    # 显示该书在选定时间范围内的笔记数
    if selected_book:
        preview_notes = fetch_notes_for_book(user_id, selected_book, time_range)
        st.markdown(
            f"<p style='color:#8C6F56; font-size:13px;'>"
            f"《{selected_book}》{selected_time_label}共有 <b>{len(preview_notes)}</b> 条笔记</p>",
            unsafe_allow_html=True,
        )

        if len(preview_notes) == 0:
            st.info("该时间范围内没有笔记，请调整时间范围或先添加笔记")
        else:
            if st.button("✨ 生成读书海报", use_container_width=True, type="primary"):
                with st.spinner("AI 正在为你生成海报文案..."):
                    poster_content = generate_poster_content(
                        selected_book, preview_notes, selected_style
                    )
                    if poster_content:
                        st.session_state["summary_poster_content"] = poster_content
                        st.session_state["summary_poster_book"] = selected_book
                        st.session_state["summary_poster_style"] = selected_style
                        st.rerun()

    # 显示已生成的海报
    poster_content = st.session_state.get("summary_poster_content")
    poster_book = st.session_state.get("summary_poster_book")
    if poster_content and poster_book:
        st.markdown("---")
        _show_poster_result(poster_content, poster_book)

        if st.button("关闭海报", use_container_width=True, key="close_summary_poster"):
            st.session_state.pop("summary_poster_content", None)
            st.session_state.pop("summary_poster_book", None)
            st.session_state.pop("summary_poster_style", None)
            st.rerun()


# ===================================================================
# 11. 页面 E: 个人中心
# ===================================================================
def show_profile() -> None:
    st.markdown(
        "<h2 style='text-align:center; color:#582F0E;'>个人中心</h2>",
        unsafe_allow_html=True,
    )

    email = get_user_email()
    user_id = get_user_id()

    # 用户信息卡
    st.markdown(
        f"""<div class="profile-card">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:56px; height:56px; background:#F0EDE5;
                    border-radius:50%; display:flex; align-items:center;
                    justify-content:center; font-size:24px;">👤</div>
                <div>
                    <div style="font-size:14px; font-weight:600;
                        color:#582F0E;">私の书房用户</div>
                    <div style="font-size:12px; color:#BCB4A8;
                        margin-top:4px;">📧 {email}</div>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # 统计概览
    books = fetch_books(user_id)
    total_notes = sum(int(b["count"]) for b in books)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stats-card">'
            f'<div class="stats-number">{len(books)}</div>'
            f'<div class="stats-label">本书</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stats-card">'
            f'<div class="stats-number">{total_notes}</div>'
            f'<div class="stats-label">条笔记</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # 间距

    if st.button("退出登录", use_container_width=True, type="primary"):
        logout()
        st.session_state["page"] = "书架"
        st.rerun()

    # 关于
    st.markdown(
        """<div class="profile-card" style="margin-top:16px;">
            <h4 style="font-size:14px; font-weight:600; color:#582F0E;
                margin-bottom:12px;">关于</h4>
            <p style="font-size:12px; color:#8C6F56; line-height:1.6;">
                私の书房是一款帮助你记录阅读感悟的应用。你可以摘抄书中的精彩语句，
                记录自己的想法，还能利用 AI 生成精美的读书海报，分享你的阅读体验。
            </p>
        </div>""",
        unsafe_allow_html=True,
    )


# ===================================================================
# 12. 主路由
# ===================================================================
if not check_auth():
    show_auth_page()
else:
    page = st.session_state.get("page", "书架")

    # 详情页不显示导航栏（有自己的返回按钮）
    if page != "详情":
        show_navigation()

    if page == "书架":
        show_bookshelf()
    elif page == "详情":
        show_book_detail()
    elif page == "添加":
        show_add_note()
    elif page == "总结":
        show_summary()
    elif page == "个人":
        show_profile()
    else:
        show_bookshelf()
