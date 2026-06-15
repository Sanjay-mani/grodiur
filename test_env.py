import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
print("BASE_DIR:", BASE_DIR)

# Simulate what settings.py does
load_dotenv()
print("Without explicit path, RAZORPAY_KEY_ID:", os.environ.get('RAZORPAY_KEY_ID'))

env_path = BASE_DIR / '.env'
load_dotenv(env_path)
print("With explicit path, RAZORPAY_KEY_ID:", os.environ.get('RAZORPAY_KEY_ID'))
