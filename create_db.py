import pandas as pd
import os

# Caminho do arquivo
dir_path = r"04. Arquivos e Projetos\03. Base_Dados_Maquinas"
file_path = os.path.join(dir_path, "DB_Maquinas.xlsx")

# Dados para a Tabela Pai (Famílias/Centros de Custo)
df_familias = pd.DataFrame({
    "ID_Familia": [1, 2, 3, 4],
    "Nome_Familia": ["Paletização", "Enchimento", "Transporte", "Embalagem"],
    "Centro_Custo_Code": ["CC-PAL", "CC-FIL", "CC-TRN", "CC-PCK"]
})

# Dados para a Tabela Filho (Modelos de Máquinas)
# Note que ID_Familia liga esta tabela à anterior
df_modelos = pd.DataFrame({
    "ID_Modelo": [101, 102, 201, 301, 401],
    "ID_Familia": [1, 1, 2, 3, 4], # 1=Paletização, 2=Enchimento...
    "Nome_Modelo": ["Innopal PB", "Innopal AS", "Innofill Glass", "Innoline", "Innopack Kisters"],
    "Descricao_Tecnica": ["Paletizador de alta velocidade", "Paletizador de eixo único", "Enchedora de vidro", "Transportadora de garrafas", "Empacotadora"]
})

# Criando o Excel com Writer para formatar como tabelas
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    # Escrever dados
    df_familias.to_excel(writer, sheet_name='Familias', index=False)
    df_modelos.to_excel(writer, sheet_name='Modelos', index=False)
    
    # Acessar o workbook e worksheets
    workbook = writer.book
    ws_familias = writer.sheets['Familias']
    ws_modelos = writer.sheets['Modelos']
    
    # Definir formato de tabela para Familias
    (max_row_f, max_col_f) = df_familias.shape
    column_settings_f = [{'header': column} for column in df_familias.columns]
    ws_familias.add_table(0, 0, max_row_f, max_col_f - 1, {
        'columns': column_settings_f,
        'name': 'tbl_Familias',
        'style': 'TableStyleMedium9'
    })
    
    # Definir formato de tabela para Modelos
    (max_row_m, max_col_m) = df_modelos.shape
    column_settings_m = [{'header': column} for column in df_modelos.columns]
    ws_modelos.add_table(0, 0, max_row_m, max_col_m - 1, {
        'columns': column_settings_m,
        'name': 'tbl_Modelos',
        'style': 'TableStyleMedium2'
    })

print(f"Banco de dados criado em: {file_path}")