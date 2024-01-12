import sys
from pathlib import Path
import time
import uvicorn

# Get the absolute path of the directory containing this script
current_file = Path(__file__).resolve()
parent_directory = current_file.parent
project_directory = parent_directory.parent

sys.path.insert(0, str(project_directory))

from api.app import create_app
from api.config import settings

api = create_app(settings)

if __name__ == "__main__":
    time.sleep(10)
    uvicorn.run("asgi:api", host="0.0.0.0", port=8000, reload=True)
