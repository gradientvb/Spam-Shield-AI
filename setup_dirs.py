import os
import sys

# Create routers directory
routers_dir = r"c:\Users\vaibh\OneDrive\Desktop\SpamShield\routers"
os.makedirs(routers_dir, exist_ok=True)

print(f"Created directory: {routers_dir}")
print(f"Directory exists: {os.path.exists(routers_dir)}")
