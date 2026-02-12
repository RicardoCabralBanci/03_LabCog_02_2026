"""
transcrever_sessoes.py - Transcreve sessoes do Claude Code (.jsonl) para Markdown (.md)
Compara com transcricoes existentes em 03_Memoria/ e so transcreve as novas.
Uso: python transcrever_sessoes.py
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime


def find_claude_project_dir():
    """Auto-detecta a pasta de projetos do Claude para este repositorio."""
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return None

    # Descobre o diretorio do projeto a partir do cwd
    # Claude converte o path: C:\Lab_Cognitivo_Script -> C--Lab-Cognitivo-Script
    cwd = str(Path(__file__).resolve().parent.parent.parent)
    dir_name = cwd.replace(":", "-").replace("\\", "-").replace("/", "-").replace("_", "-")

    candidate = claude_projects / dir_name
    if candidate.exists():
        return candidate

    # Fallback: procura qualquer pasta com .jsonl
    for d in claude_projects.iterdir():
        if d.is_dir() and list(d.glob("*.jsonl")):
            return d

    return None


def get_transcribed_sessions(memoria_path):
    """Le os sessionIds das transcricoes existentes em 03_Memoria."""
    transcribed = set()
    if not memoria_path.exists():
        return transcribed

    for md_file in memoria_path.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                # Le apenas as primeiras 15 linhas (frontmatter)
                head = ""
                for i, line in enumerate(f):
                    if i > 15:
                        break
                    head += line
                match = re.search(r'sessionId:\s*"?([^"\n]+)"?', head)
                if match:
                    transcribed.add(match.group(1).strip())
        except Exception as e:
            print(f"  Aviso: Erro ao ler {md_file.name}: {e}")

    return transcribed


def parse_jsonl(jsonl_path):
    """Le um arquivo JSONL e retorna a lista de eventos e o sessionId."""
    events = []
    session_id = None

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                events.append(data)
                if not session_id and data.get("sessionId"):
                    session_id = data["sessionId"]
            except json.JSONDecodeError:
                continue

    return session_id, events


def format_tool_use(block):
    """Formata um bloco tool_use como markdown."""
    tool_name = block.get("name", "Tool")
    # Sanitizar todo o input antes de formatar
    input_data = json.loads(sanitize_secrets(json.dumps(block.get("input", {}), ensure_ascii=False)))

    if tool_name == "Bash":
        cmd = input_data.get("command", "")
        desc = input_data.get("description", "")
        desc_line = f" *{desc}*" if desc else ""
        return f"> **[{tool_name}]**{desc_line}\n> ```bash\n> {cmd}\n> ```\n"

    elif tool_name in ("Read", "Write"):
        file_path = input_data.get("file_path", "")
        return f"> **[{tool_name}]** `{file_path}`\n"

    elif tool_name == "Edit":
        file_path = input_data.get("file_path", "")
        old = input_data.get("old_string", "")[:100]
        return f"> **[{tool_name}]** `{file_path}` — alterando: `{old}...`\n"

    elif tool_name == "Grep":
        pattern = input_data.get("pattern", "")
        path = input_data.get("path", "")
        return f"> **[{tool_name}]** `{pattern}` em `{path}`\n"

    elif tool_name == "Glob":
        pattern = input_data.get("pattern", "")
        return f"> **[{tool_name}]** `{pattern}`\n"

    elif tool_name == "WebSearch":
        query = input_data.get("query", "")
        return f"> **[{tool_name}]** `{query}`\n"

    else:
        summary = json.dumps(input_data, ensure_ascii=False)
        if len(summary) > 300:
            summary = summary[:300] + "..."
        return f"> **[{tool_name}]** {summary}\n"


def clean_system_tags(text):
    """Remove tags de sistema do conteudo."""
    text = re.sub(r'<system-reminder>.*?</system-reminder>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-message>.*?</command-message>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-name>.*?</command-name>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-args>.*?</command-args>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-caveat>.*?</local-command-caveat>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-stdout>.*?</local-command-stdout>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-stderr>.*?</local-command-stderr>', '', text, flags=re.DOTALL)
    text = re.sub(r'<persisted-output>.*?</persisted-output>', '', text, flags=re.DOTALL)
    return text.strip()


# Padroes de segredos para sanitizacao
SECRET_PATTERNS = [
    (r'github_pat_[A-Za-z0-9_]{36,}', '[GITHUB_TOKEN_REDACTED]'),
    (r'ghp_[A-Za-z0-9]{36,}', '[GITHUB_TOKEN_REDACTED]'),
    (r'gho_[A-Za-z0-9]{36,}', '[GITHUB_OAUTH_REDACTED]'),
    (r'sk-[A-Za-z0-9]{20,}', '[API_KEY_REDACTED]'),
    (r'Bearer\s+[A-Za-z0-9\-._~+/]+=*', 'Bearer [TOKEN_REDACTED]'),
    (r'token["\s:=]+[A-Za-z0-9\-._~+/]{20,}', 'token: [TOKEN_REDACTED]'),
    (r'password["\s:=]+\S{8,}', 'password: [REDACTED]'),
]


def sanitize_secrets(text):
    """Remove tokens, chaves e credenciais do texto."""
    for pattern, replacement in SECRET_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def extract_user_text(content):
    """Extrai texto de uma mensagem do usuario (string ou array)."""
    if isinstance(content, str):
        return sanitize_secrets(clean_system_tags(content))
    elif isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return sanitize_secrets(clean_system_tags("\n".join(parts)))
    return ""


def extract_system_text(content):
    """Extrai texto de uma mensagem de sistema (tool result)."""
    if isinstance(content, str):
        return sanitize_secrets(clean_system_tags(content))
    elif isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "tool_result":
                    parts.append(block.get("content", str(block)))
                elif "text" in block:
                    parts.append(block["text"])
                else:
                    parts.append(str(block))
            else:
                parts.append(str(block))
        return sanitize_secrets(clean_system_tags("\n".join(parts)))
    return ""


def transcrever_sessao(events):
    """Transcreve uma lista de eventos em markdown formatado.

    Retorna (markdown_string, metadata_dict).
    """
    lines = []
    total_input_tokens = 0
    total_output_tokens = 0
    total_chars = 0
    seen_msg_ids = set()
    current_role = None

    for event in events:
        event_type = event.get("type")

        # Pular sidechains e tipos irrelevantes
        if event.get("isSidechain", False):
            continue
        if event_type in ("file-history-snapshot", "progress"):
            continue

        msg = event.get("message", {})

        # --- USUARIO ---
        if event_type == "user":
            text = extract_user_text(msg.get("content", ""))
            if not text:
                continue

            if current_role != "user":
                lines.append("\n---\n\n## Usuario\n")
                current_role = "user"

            lines.append(f"\n{text}\n")
            total_chars += len(text)

        # --- ASSISTENTE ---
        elif event_type == "assistant":
            content_blocks = msg.get("content", [])
            if not isinstance(content_blocks, list):
                continue

            # Contar tokens (apenas uma vez por message id)
            msg_id = msg.get("id", "")
            usage = msg.get("usage", {})
            if msg_id and msg_id not in seen_msg_ids and usage:
                total_input_tokens += usage.get("input_tokens", 0)
                total_input_tokens += usage.get("cache_creation_input_tokens", 0)
                total_input_tokens += usage.get("cache_read_input_tokens", 0)
                total_output_tokens += usage.get("output_tokens", 0)
                seen_msg_ids.add(msg_id)

            for block in content_blocks:
                if not isinstance(block, dict):
                    continue

                if block.get("type") == "text":
                    text = sanitize_secrets(clean_system_tags(block.get("text", ""))).strip()
                    if not text:
                        continue
                    if current_role != "assistant":
                        lines.append("\n---\n\n## Assistente\n")
                        current_role = "assistant"
                    lines.append(f"\n{text}\n")
                    total_chars += len(text)

                elif block.get("type") == "tool_use":
                    if current_role != "assistant":
                        lines.append("\n---\n\n## Assistente\n")
                        current_role = "assistant"
                    lines.append(f"\n{format_tool_use(block)}")

        # --- SISTEMA (tool results) ---
        elif event_type == "system":
            text = extract_system_text(msg.get("content", ""))
            if not text:
                continue
            lines.append(f"\n> **Resultado**:\n> ```\n{text}\n> ```\n")
            total_chars += len(text)

    # Encontrar primeiro timestamp
    first_ts = ""
    for e in events:
        ts = e.get("timestamp")
        if ts:
            first_ts = ts
            break

    try:
        dt = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
        data_str = dt.strftime("%Y-%m-%d")
        hora_str = dt.strftime("%H:%M")
    except Exception:
        data_str = "desconhecida"
        hora_str = "00h00"

    session_id = ""
    for e in events:
        if e.get("sessionId"):
            session_id = e["sessionId"]
            break

    total_tokens = total_input_tokens + total_output_tokens

    frontmatter = f"""---
sessionId: "{session_id}"
data: {data_str}
hora: "{hora_str}"
tokens_input: {total_input_tokens}
tokens_output: {total_output_tokens}
tokens_total: {total_tokens}
caracteres: {total_chars}
tags:
  - sessao
---"""

    header = f"# Sessao {data_str} {hora_str}"
    body = "".join(lines)

    meta = {
        "data": data_str,
        "hora": hora_str.replace(":", "h"),
        "tokens": total_tokens,
        "chars": total_chars,
    }

    return f"{frontmatter}\n{header}\n{body}", meta


def main():
    script_dir = Path(__file__).parent
    memoria_path = script_dir.parent / "03_Memoria"
    memoria_path.mkdir(exist_ok=True)

    project_dir = find_claude_project_dir()
    if not project_dir:
        print("[Transcricao] Pasta de projetos do Claude nao encontrada.")
        return

    print(f"[Transcricao] Fonte: {project_dir}")
    print(f"[Transcricao] Destino: {memoria_path}")

    transcribed = get_transcribed_sessions(memoria_path)
    print(f"[Transcricao] Sessoes ja transcritas: {len(transcribed)}")

    jsonl_files = sorted(project_dir.glob("*.jsonl"))
    new_count = 0

    for jsonl_file in jsonl_files:
        session_id, events = parse_jsonl(jsonl_file)

        if not session_id:
            continue

        if session_id in transcribed:
            continue

        print(f"[Transcricao] Transcrevendo: {session_id[:12]}...")

        md_content, meta = transcrever_sessao(events)

        filename = f"{meta['data']}_{meta['hora']}_tok{meta['tokens']}_chr{meta['chars']}.md"
        output_path = memoria_path / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"  -> {filename}")
        new_count += 1

    print(f"[Transcricao] Concluido. {new_count} nova(s) transcricao(oes).")


if __name__ == "__main__":
    main()
