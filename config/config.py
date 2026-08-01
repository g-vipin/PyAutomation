import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, env="default"):
        cfg_file = Path(__file__).parent / "config.json"
        with open(cfg_file) as f:
            all_cfg = json.load(f)

        if env not in all_cfg:
            available_envs = ", ".join(sorted(all_cfg))
            raise ValueError(f"Unknown test environment '{env}'. Available environments: {available_envs}")

        raw = all_cfg[env]
        self.env = env
        self.base_url = os.getenv("BASE_URL", self._expand_env(raw.get("base_url")))
        self.browser = os.getenv("BROWSER", raw.get("browser", "chrome")).lower()
        self.timeout = int(os.getenv("TIMEOUT", raw.get("timeout", 10)))
        self.headless = self._as_bool(os.getenv("HEADLESS", raw.get("headless", False)))
        self.remote = self._as_bool(os.getenv("REMOTE", raw.get("remote", False)))
        self.remote_url = os.getenv("REMOTE_URL", self._expand_env(raw.get("remote_url")))
        self.remote_type = raw.get("remote_type")
        self.platform = raw.get("platform", "web").lower()

        self.platform_version = raw.get("platform_version")
        self.device_name = raw.get("device_name")
        self.app_path = raw.get("app_path")
        self.ssh_host = self._expand_env(raw.get("ssh_host"))
        self.ssh_user = self._expand_env(raw.get("ssh_user"))
        self.ssh_password = self._expand_env(raw.get("ssh_password"))
        self.browserstack_user = self._expand_env(raw.get("user"))
        self.browserstack_key = self._expand_env(raw.get("key"))

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def _expand_env(value):
        if isinstance(value, str):
            return os.path.expandvars(value)
        return value

    @staticmethod
    def _as_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "y", "on"}
        return bool(value)
