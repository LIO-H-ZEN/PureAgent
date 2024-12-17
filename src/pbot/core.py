import threading

_local = threading.local()

class RoleCtx:
    def __init__(self, role):
        assert role in ['system', 'user', 'assistant'], 'only supports system/user/assistant'
        self.role = role

    def __enter__(self):
        _local.role = self.role

    def __exit__(self, exc_type, exc_value, traceback):
        del _local.role

def append_msg(attribute_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            messages = getattr(self, attribute_name, None)
            gen = func(self, *args, **kwargs)
            for content in gen:
                role = getattr(_local, 'role', 'unknown')
                messages.append({'role': role, 'content': content})
            return messages
        return wrapper
    return decorator

