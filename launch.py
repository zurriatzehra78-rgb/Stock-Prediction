import subprocess
import sys
import os

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, "index.py")
    
    # Run streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", index_path]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()