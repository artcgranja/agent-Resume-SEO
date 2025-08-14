def main():
    from pathlib import Path
    import mimetypes
    from app.agents import seo_agent

    files_dir = Path(__file__).resolve().parent / "file"
    allowed_exts = {".pdf", ".txt", ".md", ".csv", ".html", ".xml", ".rtf", ".py", ".js", ".docx"}
    # MIME types permitidos pelo agno.media.File.valid_mime_types
    ext_to_allowed_mime = {
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".md": "text/md",
        ".csv": "text/csv",
        ".html": "text/html",
        ".xml": "text/xml",
        ".rtf": "text/rtf",
        ".py": "text/x-python",
        ".js": "text/javascript",  # ou "application/x-javascript"
    }

    file_dicts = []
    for path in files_dir.iterdir():
        if not path.is_file() or path.suffix.lower() not in allowed_exts:
            continue
        data = path.read_bytes()
        # Use somente MIME types aceitos; se não houver mapeamento aceito, omita o mime_type
        mime_type = ext_to_allowed_mime.get(path.suffix.lower())
        file_entry = {"content": data, "name": path.name}
        if mime_type:
            file_entry["mime_type"] = mime_type
        file_dicts.append(file_entry)

    seo_agent.print_response(
        "Reescreva o currículo para otimizar meu SEO.",
        files=file_dicts,
        stream=True,
        show_full_reasoning=True,
        show_tool_calls=True,
    )


if __name__ == "__main__":
    main()
