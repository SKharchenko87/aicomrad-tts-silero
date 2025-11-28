import re
from typing import List

def split_text(text: str, max_length: int = 1000) -> List[str]:
    """
    Splits text into chunks ensuring no chunk exceeds max_length.
    Tries to split by sentences first, then by words if necessary.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by sentence endings (.!?)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
        else:
            # If current chunk is not empty, add it to chunks
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            # If the sentence itself is longer than max_length, split by words
            if len(sentence) > max_length:
                words = sentence.split(' ')
                for word in words:
                    if len(current_chunk) + len(word) + 1 <= max_length:
                        if current_chunk:
                            current_chunk += " " + word
                        else:
                            current_chunk = word
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = word
            else:
                current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
