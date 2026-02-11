# Motor SEW-EURODRIVE - DT71D4

> Motor de indução trifásico 0.37kW

📸 **Imagem**: 00027 (em `999. Imagens\`)

---

## Identificação

- **Modelo**: DT71D4/BMG/TH/ES1S
- **Fabricante**: SEW-EURODRIVE
- **SN**: 07050.1270135/1004
- **IP**: 55 (proteção)
- **IM**: B3 (montagem horizontal)
- **Rolamento**: 6203-2RS (sem lubrificação)

### 🔍 Decodificação do Modelo

```
DT  71  D4  /  BMG  /  TH  /  ES1S
│   │   │      │      │      │
│   │   │      │      │      └─ ES1S: Encoder Incremental Sin/Cos (para DT 71-100)
│   │   │      │      └──────── TH: Proteção Térmica via Termostato (bimetálico, 2.5kΩ)
│   │   │      └─────────────── BMG: Brake Motor com placa de amortecimento (freio)
│   │   └────────────────────── D4: Comprimento da carcaça + 4 polos
│   └────────────────────────── 71: Tamanho da carcaça IEC (71mm altura do eixo)
└────────────────────────────── DT: Série de motores trifásicos SEW
```

**Observações**:
- **BMG**: Freio eletromagnético (se instalado)
- **TH**: Monitoramento térmico integrado
- **ES1S**: Encoder para controle de posição/velocidade (se instalado)

⚠️ **Nota**: Verificar fisicamente se freio e encoder estão presentes no motor.

---

## Especificações Elétricas

### ⭐ Configuração DELTA (230V) - Recomendada

```
Tensão:      230V (Δ)
Corrente:    2.09 A
Frequência:  60 Hz
Potência:    0.37 kW
Rotação:     1710 RPM
```

### Configuração ESTRELA (400V)

```
Tensão:      400V (Y)
Corrente:    1.19 A
Frequência:  50 Hz
Potência:    0.30 kW
Rotação:     ~1420 RPM
```

---

## Características

- **Polos**: 4
- **Isolamento**: Classe F (155°C)
- **Temp. ambiente**: Máx 40°C
- **Ventilação**: Natural (sem ventilador)
- **Tipo**: Motor de indução padrão (**SEM encoder**)

---

## Para Parametrização do Inversor

```
Motor Type:           Induction
Feedback:             None
Tensão Nominal:       230V
Corrente Nominal:     2.09A
Frequência Base:      60Hz
Velocidade Nominal:   1710 RPM
Polos:                4
Potência:             0.37 kW (0.5 HP)
```

---

## Proteções Recomendadas

- I²t: 2.3A (110% nominal)
- Overcurrent: 6A
- Classe Térmica: F

---

## ⚠️ Pontos de Atenção

1. **Sem encoder** - Controle em malha aberta (V/Hz)
2. **Ventilação natural** - Evitar baixa rotação contínua (<30Hz)
3. **Isolamento Classe F** - Aguenta PWM do inversor

---

## Testes Antes de Conectar

- [ ] Isolamento (megôhmetro): > 10 MΩ esperado
- [ ] Resistência ôhmica: ~10-30Ω por fase
- [ ] Rotação livre: sem travamento

---

## Status

- [x] Especificações documentadas
- [x] Nomenclatura decodificada
- [ ] Testes de isolamento
- [ ] Cabeamento especificado
- [ ] Configuração definida (Δ recomendado)

---

## 📚 Fontes

- [SEW-EURODRIVE Nomenclature Guide](https://media.sew-eurodrive.com/sew_us/media/sew_eurodrive/training_resources/online_training/dtdv_gearmotor_nomenclature.pdf)
- [SEW Thermal Protection (TH/TF)](https://download.sew-eurodrive.com/download/html/31550207/en-EN/2958248587.html)
- [SEW Brake Systems (BMG)](https://media.sew-eurodrive.com/sew_us/media/sew_eurodrive/training_resources/online_training/bmg_brake_service_and_maintenance.pdf)
- [SEW Encoders (ES1S)](https://download.sew-eurodrive.com/download/pdf/22134204_G08.pdf)
