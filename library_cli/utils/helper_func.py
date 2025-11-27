import uuid

def generate_barcode():
    return uuid.uuid4().hex[:12]  # 12-char unique code

def generate_barcode_using_book_id(book_id, copy_index):
    return f"{book_id:06d}{copy_index:04d}"


def to_enum(enum_class, value: str):
    if isinstance(value, enum_class):
        return value

    if not isinstance(value, str):
        raise ValueError(f"Expected string or {enum_class.__name__}, got {type(value)}")

    normalized = value.strip().lower().replace(" ", "_")

    for member in enum_class:
        if member.value.lower() == normalized or member.name.lower() == normalized:
            return member

    raise ValueError(f"'{value}' is not a valid {enum_class.__name__}")
