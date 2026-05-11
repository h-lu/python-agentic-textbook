from datetime import date

def is_valid_date(text: str) -> bool:
    try:
        date.fromisoformat(text.strip())
        return True
    except ValueError:
        return False

def get_menu_choice(raw: str, valid: set[str]) -> str | None:
    choice = raw.strip()
    return choice if choice in valid else None

def clean_content(text: str) -> str:
    return " ".join(text.strip().split())
