import uuid

def generate_unique_email():
    """Генерирует уникальный email-адрес."""
    return f"temp_user_{uuid.uuid4()}@example.com"