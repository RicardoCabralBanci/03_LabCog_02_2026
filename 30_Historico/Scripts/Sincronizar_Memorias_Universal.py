import os
import json
import glob
import re
from pathlib import Path

# Configuração da Raiz de Busca (Onde estão todas as pastas de hash)
ROOT_TMP_DIR = r"C:\Users\ricar\.gemini\tmp"
DEST_DIR = r"C:\LabCogKHS_CLI\30_Historico"

def sanitize_filename(text):
    return re.sub(r'[\\/*?:\"<>|]', "", text)

def safe_str(data):
    try:
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=2, ensure_ascii=False)
        return str(data)
    except:
        return "[Erro de Conversão]"

def get_session_start_time(json_data):
    """Extrai a data de início para ordenação."""
    try:
        start_time_str = json_data.get("startTime")
        if start_time_str:
            return start_time_str
    except:
        pass
    return "9999-99-99"

def json_to_markdown(json_data, index_num):
    try:
        session_id = str(json_data.get("sessionId", "unknown"))
        start_time = str(json_data.get("startTime", "Tempo desconhecido"))
        
        md_content = f"# 📓 Sessão {index_num:05d} - {start_time}\n"
        md_content += f"**ID da Sessão**: `{session_id}`\n\n---\n\n"
        
        messages = json_data.get("messages", [])
        for msg in messages:
            try:
                m_type = str(msg.get("type", "unknown")).upper()
                content = str(msg.get("content", ""))
                timestamp = str(msg.get("timestamp", ""))
                
                icon = "👤" if m_type == "USER" else "🤖"
                md_content += f"## {icon} {m_type} - {timestamp}\n\n"
                
                # Pensamentos
                thoughts = msg.get("thoughts", [])
                if isinstance(thoughts, list) and thoughts:
                    md_content += "<details>\n<summary>💭 Ver Pensamentos</summary>\n\n"
                    for thought in thoughts:
                        subj = safe_str(thought.get('subject', 'Insight'))
                        desc = safe_str(thought.get('description', ''))
                        md_content += f"> **{subj}**: {desc}\n\n"
                    md_content += "</details>\n\n"
                
                md_content += f"{content}\n\n"
                
                # Ferramentas
                tool_calls = msg.get("toolCalls", [])
                if isinstance(tool_calls, list) and tool_calls:
                    md_content += "<details>\n<summary>🛠️ Ferramentas</summary>\n\n"
                    for tool in tool_calls:
                        name = safe_str(tool.get("name", "tool"))
                        args = safe_str(tool.get("args", {}))
                        md_content += f"**Ação**: `{name}`\n```json\n{args}\n```\n"
                        
                        results = tool.get("result", [])
                        if isinstance(results, list):
                            for res in results:
                                f_res = res.get("functionResponse", {{}})
                                resp_data = f_res.get("response", "Sem resposta.")
                                resp_str = safe_str(resp_data)
                                md_content += f"**Resultado**:\n```text\n{resp_str}\n```\n\n"
                    md_content += "</details>\n\n"
                
                md_content += "---\n\n"
            except Exception as msg_e:
                md_content += f"\n\n> [!] Erro ao processar mensagem: {msg_e}\n\n---\n\n"
                
        return md_content
    except Exception as e:
        return f"Erro Crítico na Conversão: {e}"

def sync():
    if not os.path.exists(DEST_DIR): os.makedirs(DEST_DIR)
    
    # 1. Busca Recursiva Global
    print(f"Varrendo todas as subpastas em: {ROOT_TMP_DIR}")
    
    # Procura por qualquer arquivo session-*.json dentro de qualquer subpasta 'chats' dentro de qualquer hash
    # Padrão: ROOT / * / chats / session-*.json
    search_pattern = os.path.join(ROOT_TMP_DIR, "*", "chats", "session-*.json")
    json_files = glob.glob(search_pattern)
    
    sessions_data = []
    print(f"Encontrados {len(json_files)} arquivos de sessão em todo o histórico.")
    
    for j_path in json_files:
        try:
            with open(j_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                start_time = get_session_start_time(data)
                sessions_data.append({
                    'path': j_path,
                    'data': data,
                    'start_time': start_time
                })
        except Exception as e:
            print(f" [!] Erro ao ler {os.path.basename(j_path)}: {e}")

    # 2. Ordenação Cronológica Universal
    sessions_data.sort(key=lambda x: x['start_time'])
    
    print(f"Sessões ordenadas. Gerando histórico unificado...")

    # 3. Geração
    count_new = 0
    total_sessions = len(sessions_data)
    
    for index, session in enumerate(sessions_data):
        try:
            seq_num = index + 1
            data = session['data']
            sid = str(data.get("sessionId", "unknown"))
            date_p = str(data.get("startTime", "0000-00-00")).split("T")[0]
            
            filename = sanitize_filename(f"{seq_num:05d}. {date_p}_Sessao_{sid[:8]}.md")
            dest_path = os.path.join(DEST_DIR, filename)
            
            should_create = False
            if not os.path.exists(dest_path):
                should_create = True
            else:
                if os.path.getmtime(session['path']) > os.path.getmtime(dest_path):
                    should_create = True
            
            if should_create:
                print(f" [{seq_num}/{total_sessions}] Gerando: {filename}")
                markdown = json_to_markdown(data, seq_num)
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                count_new += 1
            
        except Exception as e:
            print(f" [!] Erro ao gerar sessão {index}: {e}")

    print(f" [√] Sincronização Universal Concluída. {count_new} arquivos processados.")

if __name__ == "__main__":
    sync()
