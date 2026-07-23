from pathlib import Path
import json

def load_following_data(file_path: Path) -> list[dict]:
    """Load TikTok following data from a JSON export file."""
    
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data