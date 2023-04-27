def Singleton(cls):
    _instance = {}

    def _singleton_wrapper(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton_wrapper