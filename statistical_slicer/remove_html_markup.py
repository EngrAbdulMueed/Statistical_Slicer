from lib import _data
def remove_html_markup(s: _data.get('str', str)):
    _data.param('s', s, pos=1, last=True)
    tag = _data.set('tag', False)
    quote = _data.set('quote', False)
    out = _data.set('out', '')
    for c in _data.set('c', _data.get('s', s)):
        if _data.test(_data.get('c', c) == '<' and (not _data.get('quote', quote))):
            with _data:
                tag = _data.set('tag', True)
        else:
            with _data:
                if _data.test(_data.get('c', c) == '>' and (not _data.get('quote', quote))):
                    with _data:
                        tag = _data.set('tag', False)
                else:
                    with _data:
                        if _data.test(_data.get('c', c) == '"' or (_data.get('c', c) == "'" and _data.get('tag', tag))):
                            with _data:
                                quote = _data.set('quote', not _data.get('quote', quote))
                        else:
                            with _data:
                                if _data.test(not _data.get('tag', tag)):
                                    with _data:
                                        out = _data.set('out', _data.get('out', out) + _data.get('c', c))
    return _data.set('<remove_html_markup() return value>', _data.get('out', out))