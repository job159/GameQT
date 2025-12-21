from pathlib import Path

def project_root() -> Path:
    # src/utils/paths.py -> 回到專案根目錄
    return Path(__file__).resolve().parents[2]

def pic_dir() -> Path:
    return project_root() / "pic"
