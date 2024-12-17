import threading

from core import RoleCtx, append_msg
from agents import BaseAgent, singleton
from utils import pretty_print_nested

@singleton
class MyAgent(BaseAgent):
    def __init__(self):
        self.msgs = []

    @append_msg('msgs')
    def greeting(self, system_instructions, user_inputs):
        with RoleCtx('system'):
            yield f"You are a helpful assistant, please follow: {system_instructions}."
        with RoleCtx('user'):
            yield user_inputs

def worker():
    agent = MyAgent()
    msgs = agent.greeting('You are pbot', 'hello')
    print(pretty_print_nested(msgs))

# Number of threads
num_threads = 3

# Create and start threads
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=())
    threads.append(t)
    t.start()
    import time
    time.sleep(3)

# Wait for all threads to finish
for t in threads:
    t.join()
