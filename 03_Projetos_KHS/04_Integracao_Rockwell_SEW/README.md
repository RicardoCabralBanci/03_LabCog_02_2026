# Integração Inversor Rockwell + Motor SEW

> Projeto de parametrização e comissionamento de inversor Rockwell Allen-Bradley Kinetix 5700 com motor SEW-EURODRIVE (configuração atípica).

## 🎯 Objetivo

Documentar e executar a integração de:
- **Inversor**: Rockwell Allen-Bradley Kinetix 5700 (DC Bus Supply)
- **Motor**: SEW-EURODRIVE DT71D4 (0.37kW)

## 📋 Status do Projeto

- [x] Identificação dos equipamentos
- [x] Coleta de especificações técnicas
- [ ] Análise de compatibilidade completa
- [ ] Mapeamento de parâmetros
- [ ] Parametrização do inversor
- [ ] Testes iniciais
- [ ] Comissionamento
- [ ] Documentação final

## 🔧 Equipamentos

### Inversor Rockwell Kinetix 5700
- **Modelo**: 2198-P031 (DC Bus Supply)
- **Entrada**: 324-528 Vac (3Φ)
- **Saída DC**: 498-747 Vdc, 31.6A pico
- **Ano**: 2018

### Motor SEW DT71D4
- **Potência**: 0.37kW (60Hz) / 0.30kW (50Hz)
- **Tensão**: 230V(Δ) / 400V(Y)
- **Corrente**: 2.09A / 1.19A
- **RPM**: 1710

## 📂 Estrutura do Projeto

```
04_Integracao_Rockwell_SEW/
├── 01_Especificacoes_Tecnicas/    # Datasheets, specs, análise
├── 02_Parametrizacao/             # Parâmetros e configuração
├── 03_Testes_Comissionamento/     # Procedimentos e resultados
├── 04_Documentacao/               # Guias de operação
└── 99_Referencias/                # Materiais de apoio
```

## ⚠️ Pontos Críticos

1. **DC Bus Supply**: O Kinetix 5700 é apenas a fonte DC - precisa de módulo servo drive
2. **Compatibilidade**: Motor de indução com sistema servo (verificar viabilidade)
3. **Tensão**: Confirmar configuração adequada (Δ ou Y)
4. **Parâmetros**: Ajuste fino necessário para motor não-nativo

## 🚀 Próximos Passos

1. Identificar módulo servo drive conectado ao DC Bus
2. Verificar compatibilidade servo drive + motor de indução
3. Definir estratégia de controle (V/Hz ou vetorial)
4. Mapear parâmetros críticos
5. Elaborar procedimento de testes

## 📚 Documentação

- **Especificações**: `01_Especificacoes_Tecnicas/SPECS_Equipamentos.md`
- **Contexto do Projeto**: `CLAUDE.md`

## 🖼️ Referências Visuais

Imagens armazenadas em `C:\LabCogKHS_CLI\999. Imagens\`:
- `00025. InversorRockwell_Plaquinha.jpeg`
- `00026. InversorRockwell.jpeg`
- `00027. SEW.jpeg`

---

**Data de Início**: 2026-02-10
**Responsável**: LabCogKHS
**Status**: 🟡 Em Planejamento
