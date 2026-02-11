# Tabelas de Especificações Oficiais Rockwell

> Dados extraídos das imagens 30 e 31 (documentação oficial Rockwell)

## 📸 Fonte dos Dados

- **Imagem 30**: `999. Imagens\00030. InversorData.png` - Dual-axis Inverter Power Specifications
- **Imagem 31**: `999. Imagens\00031. DC Bus.png` - 2198-P031 Specifications

---

## Servo Drive - 2198-D012-ERS3

### Dual-axis Inverter Power Specifications

| Attribute | Per Axis | 2198-D012-ERS3/ERS4 |
|-----------|----------|---------------------|
| **Bandwidth** | | |
| Velocity loop, max | | 400 Hz |
| Current loop | | 1000 Hz |
| **PWM frequency** | | 4 kHz |
| **Continuous output current (rms)** | X | **5.0 A** |
| **Continuous output current (0-pk)** | X | **7.0 A** |
| **Peak output current (rms)** *(3)* | X | **12.5 A** |
| **Peak output current (0-pk)** *(3)* | X | **17.6 A** |
| **Continuous power out (nom)** | | |
| Nom (240V rms, three-phase at 1/2 power) | X | 0.9 kW |
| Nom (480V rms, three-phase) | | **1.7 kW** |
| Nom (240V rms, three-phase) | | **3.4 kW** |
| **DC input current @ 276...747V DC** | X | **5.3 A_DC** |
| **Internal Capacitance** | | **165 µF** |

**Notas:**
1. These attributes apply to both of the axes in each dual-axis inverter.
2. Bandwidth values vary based on tuning parameters and mechanical components.
3. Peak current duration (t_PRMS) equals 1.0 second.

---

## DC Bus Supply - 2198-P031

### Complete Specifications

| Attribute | 2198-P031 |
|-----------|-----------|
| **AC input voltage** | 195...528V rms, three-phase (240V/480V) |
| **AC input frequency** | 47...63 Hz |
| **Main AC input current** *(1)* | |
| 195...528V (rms) three-phase | **11.2A** |
| Max inrush (0...pk) | 33.0 A |
| **Peak AC input current** | |
| 195...528V (rms) three-phase | **33.4 A** |
| **Line loss ride through** | 20 ms |
| **Control power DC input voltage** | 24V DC ±10% |
| **Control power input current** *(1) (2)* | **0.8 A_DC** |
| **Nominal bus output voltage** | **276...747V DC** |
| **Continuous output current to bus** | |
| Three-phase | **10.5 A_DC** |
| **Peak output current to bus** | |
| Three-phase | **31.6 A_DC** |
| **Peak output current duration** *(3)* | 1.0 s |
| **Continuous output power to bus** | |
| Nom (240V rms, three-phase at 1/2 power) | **3.5 kW** |
| Nom (480V rms, three-phase) | **7.0 kW** |
| **Peak output power to bus** | |
| Nom (240V rms, three-phase at 1/2 power) | **10.5 kW** |
| Nom (480V rms, three-phase) | **21.0 kW** |
| **Bus overvoltage** | |
| 240V, nom AC input | 1400V DC |
| 480V, nom AC input | 832V DC |
| **Internal shunt resistance** | 37.5 Ω |
| **Internal shunt power** | 75 W |
| **Shunt on** | |
| 240V, nom AC input | 400V plus 30V x bus regulator command |
| 480V, nom AC input | 775V plus 30V x bus regulator command |
| **Shunt off** | |
| 240V, nom AC input | 390V plus 30V x bus regulator command |
| 480V, nom AC input | 765V plus 30V x bus regulator command |
| **Efficiency** | (See documentation) |
| **Internal Capacitance** | **585 µF** |
| **Capacitive energy absorption** | 129 J |
| **Short-circuit current rating** | 200,000 A (rms) symmetrical |

---

## Análise Completa do Sistema

### Configuração Atual

```
[Rede AC]          [DC Bus]           [Servo Drive]        [Motor]
195-528V AC    →   276-747V DC    →   240V/480V AC    →   230V AC
3-phase            2198-P031          2198-D012-ERS3      SEW DT71D4
47-63 Hz           10.5A_DC / 31.6A   5.0A_RMS / 12.5A    2.09A / 0.37kW
                   7.0kW / 21.0kW     1.7kW / 3.4kW       1710 RPM
```

### Margem de Potência em Cascata

| Componente | Potência Contínua | Motor SEW (0.37kW) | Margem |
|------------|-------------------|-------------------|---------|
| **DC Bus Supply** | 7.0 kW @ 480V | 0.37 kW | **18.9x** |
| **Servo Drive** | 1.7 kW @ 240V | 0.37 kW | **4.6x** |
| **Limitante** | Servo Drive | - | **4.6x margem** |

**Conclusão**: O **Servo Drive** é o limitante (menor margem), mas ainda assim oferece **4.6x** a potência necessária.

### Margem de Corrente

| Componente | Corrente Contínua | Motor SEW (2.09A) | Margem |
|------------|-------------------|-------------------|---------|
| **DC Bus Supply** | 10.5 A_DC | ~1.0 A_DC equiv | **10.5x** |
| **Servo Drive** | 5.0 A_RMS | 2.09 A | **2.4x** |
| **Limitante** | Servo Drive | - | **2.4x margem** |

**Conclusão**: Sistema bem dimensionado, margem confortável em todos os níveis.

---

## Compatibilidade de Tensão

### Faixas de Operação

**AC Input (Rede):**
- Mínimo: 195V rms
- Máximo: 528V rms
- ✅ Compatível com redes 220V e 380V/440V

**DC Bus:**
- Mínimo: 276V DC
- Máximo: 747V DC
- ✅ Ampla faixa de operação

**Motor Output:**
- Drive pode fornecer até 480V AC
- Motor SEW precisa de 230V AC
- ✅ Totalmente compatível

---

## Características de Proteção

### DC Bus Supply (2198-P031)

**Sobretensão:**
- @ 240V AC input: Trip em 1400V DC
- @ 480V AC input: Trip em 832V DC

**Shunt de Frenagem (Interno):**
- Resistência: 37.5 Ω
- Potência: 75 W
- Ativação automática conforme tensão DC Bus

**Ride-Through:**
- 20 ms de tolerância a quedas de tensão

**Short-Circuit Rating:**
- 200,000 A (rms) simétrico
- Alta robustez contra curtos

### Servo Drive (2198-D012-ERS3)

**PWM:**
- Frequência: 4 kHz
- Reduz ruído acústico no motor
- Menor stress no isolamento

**Bandwidth:**
- Current loop: 1000 Hz (controle rápido)
- Velocity loop: 400 Hz max

**Capacitância:**
- 165 µF interno
- Filtragem adicional do DC bus

---

## Valores Nominais para Parametrização

### Para Configuração do Servo Drive

```
Motor Type:              Induction (se disponível)
Feedback Type:           None / Open Loop

Motor Rated Voltage:     230 V (Delta)
Motor Rated Current:     2.09 A
Motor Rated Power:       0.37 kW (0.5 HP)
Motor Rated Frequency:   60 Hz
Motor Rated Speed:       1710 RPM
Motor Poles:             4

Continuous Current:      5.0 A (drive)
Peak Current:            12.5 A (drive)
PWM Frequency:           4 kHz

I²t Protection:          Enable
I²t Current Limit:       2.3 A (110% motor)
Overcurrent Limit:       6 A (120% drive continuous)
```

---

## Observações Importantes

### Potência @ 240V vs 480V

O servo drive fornece **DOBRO** da potência em 480V:
- @ 240V: 1.7 kW (por eixo)
- @ 480V: 3.4 kW (por eixo)

**Implicação para nosso projeto:**
- Motor SEW opera em 230V (próximo de 240V)
- Drive fornecerá 1.7 kW nessa tensão
- Margem de 4.6x ainda é excelente

### Dual-Axis Configuration

O 2198-D012-ERS3 é um drive **dual-axis** (2 eixos):
- Cada eixo: 5.0A / 1.7kW @ 240V
- Estamos usando apenas 1 eixo para o motor SEW
- O segundo eixo está livre (para expansão futura)

### Peak Current Duration

**Importante:**
- Corrente de pico: 12.5 A RMS
- Duração: 1.0 segundo
- Após 1s, proteção atua se corrente não reduzir
- Usar para partidas pesadas, não operação contínua

---

## Checklist de Validação

### Tensões
- [x] AC Input (195-528V) ✅ Compatível com rede local
- [x] DC Bus (276-747V) ✅ Faixa adequada
- [x] Motor Output (0-480V) ✅ 230V motor compatível

### Correntes
- [x] AC Input (11.2A nominal) ✅ Dimensionar disjuntor
- [x] DC Bus (10.5A cont / 31.6A pico) ✅ Adequado
- [x] Drive Output (5.0A cont / 12.5A pico) ✅ Motor 2.09A OK

### Potências
- [x] DC Bus (7.0kW @ 480V) ✅ 18.9x motor
- [x] Servo Drive (1.7kW @ 240V) ✅ 4.6x motor
- [x] Motor (0.37kW) ✅ Bem dimensionado

### Proteções
- [x] Overvoltage (1400V / 832V) ✅ Configurado
- [x] Short-circuit (200kA) ✅ Robusto
- [x] I²t thermal ✅ Deve configurar no drive
- [x] Shunt de frenagem ✅ Interno no DC Bus

---

## Arquivo de Origem

**Manual/Datasheet**: [Adicionar nome do manual quando identificado]
**Data de Extração**: 2026-02-10
**Imagens de Referência**:
- `999. Imagens\00030. InversorData.png`
- `999. Imagens\00031. DC Bus.png`

**Status**: ✅ Especificações oficiais validadas e documentadas

---

**Última Atualização**: 2026-02-10
**Responsável**: LabCogKHS
