import yaml
import json
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
import hashlib

# TODO support more via liteLLM

class OpenAIClient:
    def __init__(self, config_file='config.yaml'):
        # 读取配置文件
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        self.api_key = config['api_key']
        self.cache_file = config.get('cache_file', 'cache.json')
        self.default_retry = config.get('default_retry', 3)

        # 加载缓存
        self.cache = self.load_cache()

        # 设置 OpenAI API 密钥
        openai.api_key = self.api_key

    def load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4)

    def generate_cache_key(self, **kwargs):
        # 生成缓存键，基于所有参数的哈希值
        data = json.dumps(kwargs, sort_keys=True).encode()
        return hashlib.sha256(data).hexdigest()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _request_openai(self, **kwargs):
        # 内部方法，实际请求 OpenAI API
        response = openai.ChatCompletion.create(**kwargs)
        return response

    def request(self, retry=None, **kwargs):
        if retry is None:
            retry = self.default_retry

        # 生成缓存键
        cache_key = self.generate_cache_key(**kwargs)

        # 检查缓存
        if cache_key in self.cache:
            print("Cache hit.")
            return self.cache[cache_key]

        # 设置重试次数
        max_attempts = retry + 1  # tenacity 的 stop_after_attempt 是最大尝试次数，包括第一次
        self._request_openai.retry.stop = stop_after_attempt(max_attempts)

        # 请求 OpenAI API
        print("Cache miss. Requesting OpenAI API...")
        response = self._request_openai(**kwargs)

        # 存入缓存
        self.cache[cache_key] = response
        self.save_cache()

        return response
