import copy


def chunker(segments: list, min_words: int = 15, max_words: int = 75, max_time_sec: float = 45,
                         overlap_segments: int = 2) -> list:
    chunks = []
    current_chunk_segments = []
    current_word_count = 0

    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue

        current_chunk_segments.append(seg)
        current_word_count += len(text.split())


        current_duration = current_chunk_segments[-1]["end"] - current_chunk_segments[0]["start"]

        is_semantic_boundary = text.endswith(('.', '?', '!', '\n'))

        if (current_word_count >= max_words) or \
                (current_duration >= max_time_sec) or \
                (current_word_count >= min_words and is_semantic_boundary):
            chunk_text = " ".join([s["text"].strip() for s in current_chunk_segments])
            chunks.append({
                "start": current_chunk_segments[0]["start"],
                "end": current_chunk_segments[-1]["end"],
                "text": chunk_text
            })
            overlap_size=min(overlap_segments,len(current_chunk_segments)-1)
            overlap_slice = current_chunk_segments[-overlap_size:] if overlap_size > 0 else []
            current_chunk_segments = copy.deepcopy(overlap_slice)
            current_word_count = sum(len(s["text"].strip().split()) for s in current_chunk_segments)

    if current_chunk_segments and current_word_count > 0:
        chunk_text = " ".join([s["text"].strip() for s in current_chunk_segments])
        chunks.append({
            "start": current_chunk_segments[0]["start"],
            "end": current_chunk_segments[-1]["end"],
            "text": chunk_text
        })

    return chunks