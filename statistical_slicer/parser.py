from lib import _data
from language import Tokens
from typing import List

def parse(s: _data.get('str', str)) -> List[_data.get('Tokens', Tokens)]:
    _data.param('s', s, pos=1, last=True)
    token_string = _data.set('token_string', _data.ret(_data.call(_data.get('list', list))()))
    for c in _data.set('c', _data.get('s', s)):
        if _data.test(_data.get('c', c) == '<'):
            with _data:
                _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).DEC_POINTER, pos=1)))
        else:
            with _data:
                if _data.test(_data.get('c', c) == '>'):
                    with _data:
                        _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).INC_POINTER, pos=1)))
                else:
                    with _data:
                        if _data.test(_data.get('c', c) == '+'):
                            with _data:
                                _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).INC_VALUE, pos=1)))
                        else:
                            with _data:
                                if _data.test(_data.get('c', c) == '-'):
                                    with _data:
                                        _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).INC_VALUE, pos=1)))
                                else:
                                    with _data:
                                        if _data.test(_data.get('c', c) == '.'):
                                            with _data:
                                                _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).OUTPUT, pos=1)))
                                        else:
                                            with _data:
                                                if _data.test(_data.get('c', c) == ','):
                                                    with _data:
                                                        _data.ret(_data.call(_data.get('token_string', token_string).append)(_data.arg(_data.get('Tokens', Tokens).INPUT, pos=1)))
                                                else:
                                                    with _data:
                                                        raise _data.ret(_data.call(_data.get('ValueError', ValueError))(_data.arg(f"Wrong token {_data.get('c', c)}", pos=1)))
    return _data.set('<parse() return value>', _data.get('token_string', token_string))