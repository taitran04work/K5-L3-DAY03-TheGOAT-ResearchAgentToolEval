"""Run from starter_v0: python -m streamlit run app.py"""
import json
import os

import streamlit as st

from providers import make_provider
from ui_backend import new_session, run_turn, resolve_send, save_transcript, export_transcript, redact

st.set_page_config(page_title='Research Desk', page_icon='🔎', layout='wide')
st.markdown('''<style>
.block-container {max-width: 1080px; padding-top: 2rem;}
[data-testid="stSidebar"] {background: #f2f5f8;}
[data-testid="stChatMessage"] {border: 1px solid #e5e9f0; border-radius: 12px;}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    st.title('🔎 Research Desk')
    st.caption('DAY 03 · RESEARCH AGENT')
    active = 'research_session' in st.session_state
    provider_name = st.selectbox('Provider', ['openrouter', 'openai', 'anthropic', 'gemini', 'ollama'], disabled=active)
    model_name = st.text_input('Model (trống = mặc định của repo)', disabled=active)
    version = st.text_input('Nhãn phiên bản', value='ui-dev', disabled=active)
    st.caption('Nhãn chỉ để ghi log. Chọn v3 khi đã tích hợp đúng bản v3 của nhóm.')
    env_names = {'openrouter': 'OPENROUTER_API_KEY', 'openai': 'OPENAI_API_KEY',
                 'anthropic': 'ANTHROPIC_API_KEY', 'gemini': 'GEMINI_API_KEY'}
    key_name = env_names.get(provider_name)
    ready = not key_name or bool(os.getenv(key_name))
    if ready:
        st.success('Sẵn sàng thử kết nối' if key_name else 'Dùng Ollama trên máy chủ chạy UI')
    else:
        st.warning(f'Chưa có {key_name}. Điền starter_v0/.env rồi khởi động lại UI.')
    if st.button('Hội thoại mới', use_container_width=True):
        st.session_state.pop('research_session', None)
        st.session_state.pop('save_error', None)
        st.rerun()
    st.caption('Hội thoại mới mở lại cấu hình. Log đã lưu trên máy chủ vẫn được giữ.')

st.title('Tìm hiểu. Đối chiếu. Tổng hợp.')
st.write('Tra cứu nguồn, đọc tài liệu và tổng hợp thông tin trong một cuộc hội thoại.')

session = st.session_state.get('research_session')
if session:
    a, b, c = st.columns(3)
    a.metric('Lượt hội thoại', len(session['turns']))
    b.metric('Tool events', sum(len(t['tool_events']) for t in session['turns']))
    c.metric('Phiên bản', session['version'])
    with st.expander('Thông tin phiên & tải transcript'):
        st.code(session['artifact_version'])
        st.caption(f"Provider: {session['provider']} · Model: {session['model']}")
        st.download_button('Tải transcript JSON',
                           json.dumps(export_transcript(session), ensure_ascii=False, indent=2, default=str),
                           file_name=session['transcript_id'] + '.transcript.json', mime='application/json')
    for turn in session['turns']:
        with st.chat_message('user'):
            st.write(turn['user'])
        with st.chat_message('assistant'):
            st.markdown(turn['assistant_text'])
            st.caption(turn['status'])
            if turn.get('error'):
                st.error(turn['error'])
            if turn['tool_events'] or turn['rounds']:
                with st.expander('Tool calls & kết quả'):
                    st.json({'rounds': turn['rounds'], 'tool_events': turn['tool_events']})
else:
    st.info('Chọn provider ở bên trái, rồi nhập câu hỏi bên dưới. API key được đọc từ .env trên máy chạy app.')
    with st.expander('Câu hỏi mẫu', expanded=True):
        st.markdown('- Tin tức AI hôm nay có gì nổi bật?\n- Lấy các bài đăng mới nhất giúp tôi.\n- Chỉ loại nguồn trùng trong danh sách: [{"url":"https://example.com/a?utm_source=x"},{"url":"https://example.com/a"}]')


def persist_and_refresh(current):
    try:
        save_transcript(current)
        st.session_state.pop('save_error', None)
    except OSError:
        st.session_state['save_error'] = 'Chưa lưu được transcript trên máy chủ. Dùng nút tải JSON để giữ bản sao.'
    st.rerun()


if st.session_state.get('save_error'):
    st.warning(st.session_state['save_error'])
pending = session is not None and session['pending_send'] is not None
if pending:
    st.warning('Chờ xác nhận gửi tới Telegram đã cấu hình cho nhóm.')
    st.code(redact(session['pending_send']), language=None)
    yes, no = st.columns(2)
    if yes.button('Xác nhận gửi đúng nội dung này', type='primary', use_container_width=True):
        with st.spinner('Đang gửi…'):
            resolve_send(session, True)
        persist_and_refresh(session)
    if no.button('Hủy gửi', use_container_width=True):
        resolve_send(session, False)
        persist_and_refresh(session)

user_text = st.chat_input('Bạn muốn tìm hiểu điều gì?', disabled=bool(pending) or not ready)
if user_text:
    try:
        if session is None:
            provider = make_provider(provider_name)
            session = new_session(provider_name, model_name.strip() or getattr(provider, 'default_model', None), version.strip() or 'ui-dev')
            st.session_state['research_session'] = session
        else:
            provider = make_provider(session['provider'])
        with st.spinner('Agent đang xử lý yêu cầu…'):
            run_turn(session, user_text, provider)
    except Exception as exc:
        st.error(redact(f'Không thể bắt đầu phiên: {type(exc).__name__}: {exc}'))
    else:
        persist_and_refresh(session)
