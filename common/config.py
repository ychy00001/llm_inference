# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    rootdir = os.path.dirname(sys.executable)
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    rootdir = os.path.dirname(bundle_dir)

load_dotenv(os.path.join(rootdir, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "text-ada-001")
OPENAI_CHARACTER_DESC = os.getenv("OPENAI_CHARACTER_DESC", "")
OPENAI_SESSION_MAX_TOKENS = os.getenv("OPENAI_SESSION_MAX_TOKENS", 1000)

APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = os.getenv("APP_PORT", "5000")
