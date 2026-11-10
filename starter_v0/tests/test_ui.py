"""Offline CP5 tests. Scripted providers are not live evaluation evidence."""
import json
from pathlib import Path

import pytest
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS
from ui_backend import new_session, run_turn, resolve_send, save_transcript, export_transcript


class Scripted:
    default_model = 'fake-test-model'

    def __init__(self, responses):
        self.responses = iter(responses)
        self.seen = []

    def complete(self, messages, tools, **kwargs):
        self.seen.append(list(messages))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def session():
    return new_session('openrouter', 'fake-test-model', 'offline-test')


def test_tool_then_answer_and_transcript(tmp_path):
    s = session()
    provider = Scripted([
        ModelResponse(None, [ToolCall('deduplicate_sources', {'items': [
            {'url': 'https://example.com/a'}, {'url': 'https://example.com/a#x'}]})]),
        ModelResponse('Còn một nguồn.', []),
    ])
    turn = run_turn(s, 'Bỏ nguồn trùng', provider)
    assert turn['status'] == 'answered'
    assert turn['tool_events'][0]['result']['item_count'] == 1
    assert 'TOOL_RESULTS_JSON' in provider.seen[1][-1]['content']
    saved = json.loads(save_transcript(s, tmp_path).read_text(encoding="utf-8"))
    assert saved['turns'][0]['assistant_text'] == 'Còn một nguồn.'
    assert saved['prompt_hash'] and saved['tools_hash']
    assert saved['source'] == 'streamlit_ui'


def test_clarification_and_followup_keep_context():
    s = session()
    provider = Scripted([
        ModelResponse(None, [ToolCall('clarify', {'question': 'Tài khoản nào?'})]),
        ModelResponse('Đã nhận tài khoản.', []),
    ])
    assert run_turn(s, 'Lấy tweet', provider)['status'] == 'waiting_for_user'
    run_turn(s, 'sama', provider)
    assert any('Tài khoản nào?' in m['content'] for m in provider.seen[-1])


def test_model_cannot_send_without_button_and_button_sends_once(monkeypatch):
    sent = []
    monkeypatch.setitem(TOOL_FUNCTIONS, 'send', lambda **kw: sent.append(kw) or {'status': 'sent'})
    s = session()
    p = Scripted([ModelResponse(None, [ToolCall('send', {'text': 'Bản tin A', 'confirmed': True})])])
    assert run_turn(s, 'Gửi bản tin', p)['status'] == 'waiting_for_confirmation'
    assert sent == []
    assert resolve_send(s, True)['status'] == 'sent'
    assert sent == [{'text': 'Bản tin A', 'confirmed': True}]
    with pytest.raises(ValueError):
        resolve_send(s, True)
    assert len(sent) == 1


def test_cancel_never_executes_send(monkeypatch):
    def forbidden(**kwargs):
        pytest.fail('send must not execute')
    monkeypatch.setitem(TOOL_FUNCTIONS, 'send', forbidden)
    s = session()
    s['pending_send'] = 'Do not send'
    assert resolve_send(s, False)['status'] == 'cancelled'
    assert s['pending_send'] is None


def test_provider_error_preserves_partial_tools_and_redacts_key(monkeypatch):
    monkeypatch.setenv('OPENROUTER_API_KEY', 'secret-test-12345')
    s = session()
    p = Scripted([ModelResponse(None, [ToolCall('deduplicate_sources', {'items': []})]),
                  RuntimeError('Bad key secret-test-12345')])
    result = run_turn(s, 'test', p)
    assert result['status'] == 'provider_error'
    assert result['tool_events'][0]['result']['item_count'] == 0
    assert 'secret-test-12345' not in json.dumps(export_transcript(s))


def test_tool_failure_is_visible():
    s = session()
    p = Scripted([ModelResponse(None, [ToolCall('deduplicate_sources', {'items': None})]),
                  ModelResponse('Input sai.', [])])
    result = run_turn(s, 'bad input', p)
    assert result['tool_events'][0]['result']['error'] == 'ValueError'


def test_limit_stops_loop():
    s = session()
    p = Scripted([ModelResponse(None, [ToolCall('unknown', {})])] * 4)
    assert run_turn(s, 'loop', p)['status'] == 'max_tool_rounds'
    assert len(p.seen) == 4


def test_sessions_are_isolated():
    one, two = session(), session()
    run_turn(one, 'hello', Scripted([ModelResponse('hi', [])]))
    assert two['turns'] == [] and one['transcript_id'] != two['transcript_id']


def test_streamlit_chat_and_reset(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    import providers
    import ui_backend
    monkeypatch.setenv('OPENROUTER_API_KEY', 'fake-offline-key')
    # chat.py loads .env when imported; tests never use a real provider.
    monkeypatch.setattr(providers, 'make_provider', lambda _: Scripted([ModelResponse('Xin chào từ test.', [])]))
    save = ui_backend.save_transcript
    monkeypatch.setattr(ui_backend, 'save_transcript', lambda s: save(s, tmp_path))
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run()
    assert not app.exception
    app.chat_input[0].set_value('Xin chào').run()
    assert not app.exception
    assert any('Xin chào từ test.' in item.value for item in app.markdown)
    assert len(list(tmp_path.glob('*.transcript.json'))) == 1
    next(b for b in app.button if b.label == 'Hội thoại mới').click().run()
    assert not app.exception
    assert 'research_session' not in app.session_state


def test_streamlit_send_preview_and_cancel(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    import providers
    import ui_backend
    monkeypatch.setenv('OPENROUTER_API_KEY', 'fake-offline-key')
    monkeypatch.setattr(providers, 'make_provider', lambda _: Scripted([
        ModelResponse(None, [ToolCall('send', {'text': 'Nội dung cần duyệt', 'confirmed': True})])]))
    save = ui_backend.save_transcript
    monkeypatch.setattr(ui_backend, 'save_transcript', lambda s: save(s, tmp_path))
    sent = []
    monkeypatch.setitem(TOOL_FUNCTIONS, 'send', lambda **kw: sent.append(kw) or {'status': 'sent'})
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run()
    app.chat_input[0].set_value('Gửi bản tin').run()
    assert not app.exception
    assert app.chat_input[0].disabled
    assert any('Nội dung cần duyệt' in x.value for x in app.code)
    next(b for b in app.button if b.label == 'Hủy gửi').click().run()
    assert not app.exception and sent == []
    assert not app.chat_input[0].disabled


def test_streamlit_missing_key_blocks_submission(monkeypatch):
    from streamlit.testing.v1 import AppTest
    monkeypatch.delenv('OPENROUTER_API_KEY', raising=False)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run()
    assert not app.exception
    assert app.chat_input[0].disabled
    assert any('OPENROUTER_API_KEY' in x.value for x in app.warning)
