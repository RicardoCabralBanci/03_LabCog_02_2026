-- 10. DB SQLite/schema.sql
-- Arquitetura do Gerador de Manuais KHS

-- Projetos principais
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sap_number TEXT UNIQUE NOT NULL,
    project_name TEXT,
    revision TEXT DEFAULT '00',
    machine_type TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Catálogo de Módulos (Seções de Word)
CREATE TABLE IF NOT EXISTS manual_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_type TEXT NOT NULL,
    section_name TEXT NOT NULL,
    file_path_template TEXT NOT NULL,
    default_order INTEGER,
    description TEXT
);

-- Composição do Manual (Relação N:N)
CREATE TABLE IF NOT EXISTS project_composition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    section_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 0,
    custom_order INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (section_id) REFERENCES manual_sections(id)
);

-- Parâmetros Técnicos
CREATE TABLE IF NOT EXISTS technical_parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_type TEXT NOT NULL,
    category TEXT,
    param_key TEXT NOT NULL,
    unit TEXT,
    description TEXT
);

-- Valores dos Parâmetros por Projeto
CREATE TABLE IF NOT EXISTS project_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    param_id INTEGER NOT NULL,
    value TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (param_id) REFERENCES technical_parameters(id)
);
