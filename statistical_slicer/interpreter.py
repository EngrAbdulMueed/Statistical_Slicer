from lib import _data
from language import Tokens
from language.parser import parse

def interpret(program: _data.get('str', str), input_stream: _data.get('bytes', bytes)) -> _data.get('bytes', bytes):
    _data.param('program', program, pos=1)
    _data.param('input_stream', input_stream, pos=2, last=True)
    token_string = _data.set('token_string', _data.ret(_data.call(_data.get('parse', parse))(_data.arg(_data.get('program', program), pos=1))))
    output_stream = _data.set('output_stream', b'')
    mem = _data.set('mem', {0: 0})
    ptr = _data.set('ptr', 0)
    pos = _data.set('pos', 0)
    while _data.test(_data.get('pos', pos) < _data.ret(_data.call(_data.get('len', len))(_data.arg(_data.get('token_string', token_string), pos=1)))):
        with _data:
            if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).INC_VALUE):
                with _data:
                    _data.get('mem', mem)[_data.get('ptr', ptr)] += _data.augment('mem', 1)
                    pos += _data.augment('pos', 1)
            else:
                with _data:
                    if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).DEC_VALUE):
                        with _data:
                            _data.get('mem', mem)[_data.get('ptr', ptr)] -= _data.augment('mem', 1)
                            pos += _data.augment('pos', 1)
                    else:
                        with _data:
                            if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).INC_POINTER):
                                with _data:
                                    ptr += _data.augment('ptr', 1)
                                    pos += _data.augment('pos', 1)
                            else:
                                with _data:
                                    if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).DEC_POINTER):
                                        with _data:
                                            ptr -= _data.augment('ptr', 1)
                                            pos += _data.augment('pos', 1)
                                    else:
                                        with _data:
                                            if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).OUTPUT):
                                                with _data:
                                                    output_stream += _data.ret(_data.call(_data.get('mem', mem)[_data.get('ptr', ptr)].to_bytes)(_data.arg(1, pos=1), _data.arg('little', pos=2)))
                                                    pos += _data.augment('pos', 1)
                                            else:
                                                with _data:
                                                    if _data.test(_data.get('token_string', token_string)[_data.get('pos', pos)] == _data.get('Tokens', Tokens).INPUT):
                                                        with _data:
                                                            (_data.get('mem', mem)[_data.get('ptr', ptr)], input_stream) = _data.set('mem', _data.set('input_stream', (_data.get('input_stream', input_stream)[0], _data.get('input_stream', input_stream)[1:]), loads=(_data.get('ptr', ptr), _data.get('mem', mem))))
                                                            pos += _data.augment('pos', 1)
            if _data.test(_data.get('ptr', ptr) not in _data.get('mem', mem)):
                with _data:
                    _data.get('mem', mem)[_data.get('ptr', ptr)] = _data.set('mem', 0, loads=(_data.get('ptr', ptr), _data.get('mem', mem)))
    return _data.set('<interpret() return value>', _data.get('output_stream', output_stream))