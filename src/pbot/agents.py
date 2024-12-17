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
