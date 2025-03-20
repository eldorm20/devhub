# filepath: /workspaces/devhub/backend/tests/conftest.py
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
