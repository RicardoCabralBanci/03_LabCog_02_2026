# 04_Integracao_Rockwell_SEW

## Contexto do Projeto

Projeto de integração **Inversor Rockwell Allen-Bradley Kinetix 5700** com **Motor SEW-EURODRIVE** (ambos equipamentos antigos).

**Situação**: Configuração atípica - normalmente inversores Danfoss são usados com motores SEW, OGD, Rockwell e Siemens. Este projeto documenta a parametrização e comissionamento de um inversor Rockwell alimentando motor SEW.

## Equipamentos

### Inversor Rockwell Allen-Bradley
- **Modelo**: Kinetix 5700
- **Cat**: 2198-P031
- **Tipo**: DC Bus Supply 31.6A
- **Entrada**: 324-528 Vac (3 fases)
- **Plant**: 1100
- **Ano**: 2018

### Motor SEW-EURODRIVE
- **Tipo**: DT71D4/BMG/TH/ES1S
- **IM**: B3
- **IP**: 55
- **Potência**: 0.37kW (60Hz) / 0.30kW (50Hz)
- **Tensão**: 230Δ / 400Y (V)
- **Corrente**: 2.09A / 1.19A
- **Rotação**: 1710 RPM
- **Frequência**: 50/60 Hz
- **Número**: 6203-2RS

## Estrutura

```
04_Integracao_Rockwell_SEW/
├── CLAUDE.md                          # << ESTE ARQUIVO
├── README.md                          # Visão geral e guia rápido
├── 01_Especificacoes_Tecnicas/        # Datasheets, manuais, specs
├── 02_Parametrizacao/                 # Parâmetros do inversor, setup
├── 03_Testes_Comissionamento/         # Procedimentos, resultados, logs
├── 04_Documentacao/                   # Guias de operação, troubleshooting
└── 99_Referencias/                    # Links, imagens, anotações
```

## Referências de Imagens

- `999. Imagens\00025. InversorRockwell_Plaquinha.jpeg` - Placa de identificação do inversor
- `999. Imagens\00026. InversorRockwell.jpeg` - Vista frontal dos inversores Kinetix 5700
- `999. Imagens\00027. SEW.jpeg` - Placa de identificação do motor SEW

## Objetivo

Documentar todo o processo de:
1. Análise de compatibilidade elétrica
2. Parametrização do inversor Kinetix 5700 para o motor SEW
3. Comissionamento e testes
4. Procedimentos de operação e manutenção
5. Troubleshooting e casos especiais

## Notas

- Equipamentos antigos: pode haver limitações de documentação
- Integração atípica: requer atenção especial aos parâmetros
- Documentar tudo para casos futuros similares
