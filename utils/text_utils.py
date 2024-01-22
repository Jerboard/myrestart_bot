

def get_cut_text(max_len: int, text: str) -> str:
    if len(text) > max_len:
        return f'{text[:max_len]}...'
    else:
        return text
