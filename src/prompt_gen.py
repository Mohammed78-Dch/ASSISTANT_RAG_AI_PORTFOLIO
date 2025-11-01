def build_prompt(query: str, retrieved_chunks: list, cv_person_name: str = "the candidate") -> str:
    """
    Builds a RAG prompt for querying a person's CV with structured responses.

    Args:
        query (str): User's question.
        retrieved_chunks (list[str] or list[tuple[str, float]]): Chunks retrieved from FAISS or other sources.
        cv_person_name (str): Name of the person whose CV is queried.

    Returns:
        str: A full LLM prompt.
    """
    # Extract text if tuples are provided
    chunk_texts = [c[0] if isinstance(c, tuple) else c for c in retrieved_chunks]

    # Remove duplicates while preserving order
    seen = set()
    unique_chunks = []
    for chunk in chunk_texts:
        if chunk not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk)

    # Categorize chunks
    categories = {"Experience": [], "Projects": [], "Skills & Education": [], "Other": []}
    for chunk in unique_chunks:
        header_line = chunk.split("\n", 1)[0].strip()
        if header_line.startswith("## Project") or header_line.lower().startswith("project"):
            categories["Projects"].append(chunk)
        elif header_line.startswith("##") or "Experience" in header_line:
            categories["Experience"].append(chunk)
        elif "Skills" in header_line or "Education" in header_line:
            categories["Skills & Education"].append(chunk)
        else:
            categories["Other"].append(chunk)

    # Build context section
    context_text = ""
    for cat_name, chunks_list in categories.items():
        if chunks_list:
            context_text += f"\n### {cat_name} Context:\n"
            for c in chunks_list:
                context_text += f"- {c}\n"

    # System instructions
    system_prompt = f"""
You are an AI assistant for {cv_person_name}'s professional portfolio.
Your task is to answer user questions **based ONLY on the provided context**.
Rules:
- Use structured and factual answers only.
- For projects, provide titles and objectives; highlight achievements in bullet points.
- Emphasize skills and technologies in **bold** where relevant.
- Resolve pronouns using context.
- If asked for a list of projects, present all retrieved projects using their title and short description.
- Use phrasing like "Applied [Skill] in …" when describing skill usage in projects.
"""

    # Optional example
    examples = f"""
### Example:
Q: What is {cv_person_name}'s experience with AI?
A:
- Designed and deployed AI-based solutions.
- Built data pipelines for analytics and ML models.
- Implemented automation tools to improve workflow efficiency.
"""

    # Combine into full prompt
    full_prompt = f"""{system_prompt}

{examples}

### CONTEXTS:
{context_text}

### USER QUESTION:
{query}

### FINAL ANSWER:"""

    return full_prompt
