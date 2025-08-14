def main():
    from pathlib import Path
    from uuid import uuid4
    from app.agents.orchestrator import Orchestrator

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

    session_id = str(uuid4())
    orchestrator = Orchestrator(session_id)

    # Initial message
    initial_message = "┃ Poderia analisar meu curriculo, como um avaliador generico para saber se esta no bom caminho "
    
    # Use run_with_files if files are found, otherwise use regular run
    if file_dicts:
        orchestrator.run_with_files(initial_message, file_dicts)
    else:
        orchestrator.run(initial_message)

    while True:
        input_ = input("user: ")
        if input_ == "exit":
            break
        orchestrator.run(input_)

if __name__ == "__main__":
    main()