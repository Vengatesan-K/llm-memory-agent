import os
import sys
from dotenv import load_dotenv

# Set up paths
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

# Load environment variables
load_dotenv()

# Import after path configuration
from src.api.endpoints import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.endpoints:app",
        host="0.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[src_path],
    )
