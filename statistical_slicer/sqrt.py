from lib import _data
def square_root(x):
    _data.param('x', x, pos=1, last=True)
    approx = _data.set('approx', None)
    guess = _data.set('guess', _data.get('x', x) / 2)
    while _data.test(_data.get('approx', approx) != _data.get('guess', guess)):
        with _data:
            approx = _data.set('approx', _data.get('guess', guess))
            guess = _data.set('guess', (_data.get('approx', approx) + _data.get('x', x) / _data.get('approx', approx)) / 2)
    return _data.set('<square_root() return value>', _data.get('approx', approx))