
def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """
    text = the full text we want to split
    chunk_size = how many characters in one chunk
    overlap = how many characters repeat between chunks (keeps context at the edges)
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip() != "":
            chunks.append(chunk)

        start = end - overlap

    return chunks