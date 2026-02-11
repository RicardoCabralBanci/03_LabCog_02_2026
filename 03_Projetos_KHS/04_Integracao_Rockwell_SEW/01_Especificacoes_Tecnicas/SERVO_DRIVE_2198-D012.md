# Servo Drive - 2198-D012-ERS3

> **Módulo DIREITO (SER B)** - Controla o motor

📸 **Imagens**: 00028, 00030 (em `999. Imagens\`)
📋 **Detalhes completos**: Ver `TABELAS_Especificacoes_Oficiais.md`

---

## Identificação

- **Modelo**: 2198-D012-ERS3
- **Função**: Servo Drive Dual-Axis (usando 1 eixo)
- **SN**: 67842654
- **Data**: 2019/01/07
- **MAC**: 00:00:BC:BC:D6:4D

**Decodificação**:
- **D** = Série econômica
- **012** = 1.7kW @ 240V / 3.4kW @ 480V
- **ERS3** = EtherNet/IP + Safety (STO)

---

## Especificações Essenciais

### Entrada (DC Bus)
```
Tensão:   276-747V DC
Corrente: 5.3 A_DC
```

### Saída (Motor)
```
Tensão:     0-480V AC (3Φ)
Corrente:   5.0A contínuo / 12.5A pico (1s)
Potência:   1.7kW @ 240V / 3.4kW @ 480V
PWM:        4 kHz
```

### Comunicação
- EtherNet/IP (10/100 Mbps)
- Safe Torque-Off (SIL 2)
- 2 eixos independentes (usando apenas 1)

---

## Compatibilidade com Motor SEW 0.37kW

| Parâmetro | Servo Drive | Motor SEW | Margem |
|-----------|-------------|-----------|---------|
| Potência | 1.7 kW | 0.37 kW | **4.6x** ✅ |
| Corrente | 5.0 A | 2.09 A | **2.4x** ✅ |
| Tensão | 0-480V | 230V | ✅ OK |

**Resultado**: Muito sobre-dimensionado = excelente margem

---

## ⚠️ QUESTÃO CRÍTICA

### Suporta Motor de Indução?

**Problema**:
- Drive = Otimizado para **servo motores** (com encoder)
- Motor SEW = **Motor de indução** (sem encoder)

**Precisamos verificar**:
1. Se tem modo "Induction Motor" ou "Open Loop"
2. Parâmetros V/Hz disponíveis
3. Operação sem feedback

**Onde buscar**: Manuais 2198-UM002, 2198-RM001, 2198-AT002

---

## Próximos Passos

1. ⚠️ Baixar manuais Rockwell
2. ⚠️ Verificar suporte a motor de indução
3. [ ] Definir estratégia de parametrização
4. [ ] Fazer backup da configuração atual
5. [ ] Comissionar

---

## Status

- [x] Identificado
- [x] Especificações validadas
- [x] Compatibilidade elétrica OK
- [ ] **Compatibilidade com indução - PENDENTE**
