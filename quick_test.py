import sys
print("Python version:", sys.version)

# Try to import all required modules
try:
    import requests
    print("✅ requests module installed")
    
    import pandas as pd
    print("✅ pandas module installed")
    
    import fastapi
    print("✅ fastapi module installed")
    
    print("\nAll modules are installed correctly!")
    
except ImportError as e:
    print(f"❌ Missing module: {e}")
    print("\nRun: pip install requests pandas fastapi uvicorn")