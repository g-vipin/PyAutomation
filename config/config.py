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
        raw = all_cfg.get(env, {})
        self.base_url = os.getenv("BASE_URL", raw.get("base_url"))
        self.browser = os.getenv("BROWSER", raw.get("browser", "chrome"))
        self.headless = raw.get("headless", False)
        self.remote = raw.get("remote", False)
        self.remote_url = raw.get("remote_url") or os.getenv("REMOTE_URL")
        self.platform_version = raw.get("platform_version")
        self.device_name = raw.get("device_name")
        self.app_path = raw.get("app_path")
        self.ssh_host = raw.get("ssh_host")
        self.ssh_user = raw.get("ssh_user")
        self.ssh_password = raw.get("ssh_password")
