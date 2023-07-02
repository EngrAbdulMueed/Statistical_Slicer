from lib import _data
def middle(x, y, z):
    _data.param('x', x, pos=1)
    _data.param('y', y, pos=2)
    _data.param('z', z, pos=3, last=True)
    if _data.test(_data.get('y', y) < _data.get('z', z)):
        with _data:
            if _data.test(_data.get('x', x) < _data.get('y', y)):
                with _data:
                    return _data.set('<middle() return value>', _data.get('y', y))
            else:
                with _data:
                    if _data.test(_data.get('x', x) < _data.get('z', z)):
                        with _data:
                            return _data.set('<middle() return value>', _data.get('y', y))
    else:
        with _data:
            if _data.test(_data.get('x', x) > _data.get('y', y)):
                with _data:
                    return _data.set('<middle() return value>', _data.get('y', y))
            else:
                with _data:
                    if _data.test(_data.get('x', x) > _data.get('z', z)):
                        with _data:
                            return _data.set('<middle() return value>', _data.get('x', x))
    return _data.set('<middle() return value>', _data.get('z', z))