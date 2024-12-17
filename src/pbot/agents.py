import threading

def singleton(cls):
    _instance = {}
    _lock = threading.Lock()
    def wrapper(*args, **kwargs):
        if cls not in _instance:
            with _lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper

class BaseAgent:
    def __init__(self):
        self.msgs = []

class ThreadSafeList:
    def __init__(self):
        self.locals = threading.local()

    def _get_list(self):
        if not hasattr(self.locals, 'data'):
            self.locals.data = []
        return self.locals.data

    def append(self, item):
        lst = self._get_list()
        lst.append(item)

    def get_list(self):
        return self._get_list()

    def clear(self):
        self._get_list().clear()

    def __iter__(self):
        return iter(self._get_list())

    def __str__(self):
        return str(self._get_list())

    def __repr__(self):
        return f"ThreadSafeList({self._get_list()})"

class DataParallelAgent:
    def __init__(self):
        self.msgs = ThreadSafeList()
