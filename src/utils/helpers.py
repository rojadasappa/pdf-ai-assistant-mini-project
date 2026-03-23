def format_docs(docs) -> str:
    blocks = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "n/a")
        blocks.append(f"[source={src}, page={page}]\n{d.page_content}")
    return "\n\n".join(blocks)
