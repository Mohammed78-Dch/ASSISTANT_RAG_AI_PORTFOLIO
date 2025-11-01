import re
from .config import RESUME_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def chunk_resume_data(resume_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Splits resume by # and ## headings, preserving hierarchy and overlapping lines between chunks.
    """
    chunks = []
    lines = resume_text.split('\n')
    buffer = []

    current_h1 = ""
    current_h2 = ""

    def flush_buffer():
        if not buffer:
            return
        start = 0
        while start < len(buffer):
            end = min(start + chunk_size, len(buffer))
            chunk_lines = buffer[start:end]
            chunk_text = "\n".join(chunk_lines).strip()
            if chunk_text:
                prefix = ""
                if current_h1:
                    prefix += f"{current_h1}\n"
                if current_h2:
                    prefix += f"{current_h2}\n"
                chunks.append(f"{prefix}{chunk_text}")
            if end == len(buffer):
                break
            start = end - overlap  
        buffer.clear()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('##'):
            flush_buffer()
            current_h2 = line
        elif line.startswith('#'):
            flush_buffer()
            current_h1 = line
            current_h2 = ""
        else:
            buffer.append(line)

    flush_buffer()
    return [c for c in chunks if c.strip()]


if __name__ == "__main__":
    with open(RESUME_PATH, 'r', encoding='utf-8') as f:
        resume_text = f.read()

    chunks = chunk_resume_data(resume_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    print(f"Generated {len(chunks)} chunks.\n")
    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print('-' * 20)
