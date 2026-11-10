"""Offline tests for deduplicate_sources only."""
import pytest
from tools import TOOL_FUNCTIONS as T

def test_deduplicate_happy_path():
    items = [{'url': 'https://EXAMPLE.com/a?utm_source=x#top', 'title': 'First'},
             {'url': 'https://example.com/a', 'title': 'Second'},
             {'url': 'https://example.com/b', 'title': 'Third'}]
    r = T['deduplicate_sources'](items)
    assert r['items'] == [items[0], items[2]]
    assert (r['input_count'], r['item_count'], r['removed_count']) == (3, 2, 1)
    assert r['duplicates'] == [{'index': 1, 'kept_index': 0}]
    r['items'][0]['title'] = 'Changed'
    assert items[0]['title'] == 'First'


@pytest.mark.parametrize('items', [None, '', {}, [1], [{}], [{'url': ''}],
    [{'url': 1}], [{'url': 'file:///tmp/a'}], [{'url': 'https://u:p@example.com'}],
    [{'url': 'https://example.com:bad'}], [{'url': 'https://example.com'}] * 501])
def test_deduplicate_bad_input_from_model(items):
    r = T['deduplicate_sources'](items)
    assert r['error'] == 'ValueError' and 'items' not in r


def test_deduplicate_failure_returns_error_dict(monkeypatch):
    import tools.deduplicate.tool as module
    def fail(value):
        raise RuntimeError('normalization failed')
    monkeypatch.setattr(module, '_url_key', fail)
    assert T['deduplicate_sources']([{'url': 'https://example.com'}]) == {
        'tool': 'deduplicate_sources', 'error': 'RuntimeError', 'message': 'normalization failed'}


def test_deduplicate_keeps_distinct_content_urls():
    urls = ['https://example.com/a?id=1', 'https://example.com/a?id=2',
            'http://example.com/a?id=1', 'https://example.com/A?id=1',
            'https://example.com/a/?id=1']
    assert T['deduplicate_sources']([{'url': u} for u in urls])['item_count'] == len(urls)


def test_deduplicate_empty_list_is_valid():
    assert T['deduplicate_sources']([])['item_count'] == 0

