import subprocess
import os
import sys
from dotenv import load_dotenv, dotenv_values

load_dotenv()

DETECT_TEXT = os.getenv("DETECT_TEXT")
DETECT_TEXT = os.path.abspath(DETECT_TEXT)
LLM_PROCESSING = os.getenv("LLM_PROCESSING")

RECOGNIZE_TEXT = os.getenv("RECOGNIZE_TEXT")
RECOGNIZE_TEXT = os.path.abspath(RECOGNIZE_TEXT)
LLM_PROCESSING = os.path.abspath(LLM_PROCESSING)


subprocess.run([sys.executable, DETECT_TEXT], check=True)

subprocess.run([sys.executable, RECOGNIZE_TEXT], check=True)

subprocess.run([sys.executable, LLM_PROCESSING], check=True)

