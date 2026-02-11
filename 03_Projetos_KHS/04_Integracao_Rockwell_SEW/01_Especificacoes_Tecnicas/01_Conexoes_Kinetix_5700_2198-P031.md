# Conexões do Kinetix 5700 DC-Bus Power Supply (2198-P031)

> **Referência**: Rockwell Automation Publication 2198-IN009
> **Data**: 2026-02-11
> **Status**: Diagrama oficial identificado - pronto para conexão

---

## Diagrama do Módulo 2198-P031

![Diagrama de Conectores do Kinetix 5700](../../../999.%20Imagens/00032.%20P031_Conections.png)

*Figura: Vista frontal, superior e inferior do módulo 2198-P031 com conectores identificados*

---

## Mapa Completo de Conectores (Referência da Imagem)

| Item | Conector | Localização | Prioridade |
|------|----------|-------------|------------|
| **12** | Ground Terminal | Frontal (inferior) | 🔴 **CRÍTICO** |
| **16** | AC Input Power (IPD) | Inferior | 🔴 **ESSENCIAL** |
| **15** | 24V Control Input Power (CP) | Superior (laranja) | 🔴 **ESSENCIAL** |
| **11** | Contactor Enable (CED) | Frontal (inferior) | 🔴 **ESSENCIAL** |
| **14** | DC Bus (DC) | Superior | 🔴 **ESSENCIAL** |
| **13** | Shunt Resistor (RC) | Superior | 🟡 Opcional |
| **1** | Digital Inputs (IOD) | Frontal (topo) | 🟡 Opcional |
| **2** | Ethernet PORT1 (RJ45) | Frontal | 🟡 Comunicação |
| **3** | Ethernet PORT2 (RJ45) | Frontal | 🟡 Comunicação |
| **7** | LCD Display | Frontal | ℹ️ Informativo |
| **8** | Navigation Buttons | Frontal | ℹ️ Interface |
| **17** | Cooling Fan | Inferior | ⚙️ Automático |

---

---

## 🔧 GUIA PASSO A PASSO DE CONEXÃO

### ⚠️ ANTES DE COMEÇAR
- ✅ Desligue TODA a alimentação elétrica
- ✅ Confirme ausência de tensão com multímetro
- ✅ Use EPIs adequados (luvas isolantes)
- ✅ Siga procedimentos LOTO da empresa

---

## Conexões Necessárias para Ligar o Inversor

### PASSO 1️⃣: Aterramento (Item 12 - Ground Terminal)
**📍 Localização**: Parte frontal inferior do módulo

**O que conectar:**
- Cabo flexível trançado (braided ground strap)
- Conectar ao barramento de terra do painel/armário

**Especificações:**
- Conexão de baixa impedância
- Aperto firme no terminal

**⚠️ FAZER PRIMEIRO - Base de toda segurança elétrica!**

---

### PASSO 2️⃣: Alimentação de Controle 24V DC (Item 15 - CP)
**📍 Localização**: Superior do módulo (conector laranja destacado)

**O que conectar:**
- **Positivo (+)**: 24V DC da fonte de alimentação
- **Negativo (-)**: 0V (comum) da fonte

**Especificações:**
- Tensão: 24V DC estabilizada
- Corrente típica: 1-2A (verificar no manual)
- **SEM ISSO O MÓDULO NÃO LIGA A LÓGICA DE CONTROLE**

**Como identificar:**
- É o conector "Shared-bus 24V Input Wiring Connector" destacado em laranja na imagem
- Geralmente tem marcação de polaridade (+/-)

---

### PASSO 3️⃣: Habilitação do Contator (Item 11 - CED)
**📍 Localização**: Parte frontal inferior

**O que conectar:**
- Contatos do relé de habilitação do sistema
- Conectado em SÉRIE com bobina do contator AC principal

**Função:**
- Quando o módulo está pronto, fecha esses contatos
- Permite energizar o contator AC que alimenta o IPD
- É um circuito de segurança (safety interlock)

**Esquema de ligação:**
```
24V DC ──→ [Botão Start] ──→ [CED] ──→ [Bobina Contator AC] ──→ 0V
```

**⚠️ IMPORTANTE:**
- Verificar se é normalmente aberto (NA) ou normalmente fechado (NF) no manual
- Geralmente é NA (fecha quando módulo está OK)

---

### PASSO 4️⃣: Alimentação AC Trifásica (Item 16 - IPD)
**📍 Localização**: Parte inferior do módulo

**O que conectar:**
- **L1, L2, L3**: Fases do sistema trifásico 380-480V AC
- **OBRIGATÓRIO**: Passar por **contator trifásico** antes

**Especificações:**
- **Tensão**: 324-528 Vac (3 fases)
- **Corrente**: 31.6A contínua
- **Cabo**: Mínimo 6 mm² (10 AWG), cobre 75°C
- **Sequência de fases**: Verificar no manual (pode ser importante)

**Diagrama de ligação:**
```
Proteção (Disjuntor) → Contator AC → IPD (L1, L2, L3)
                            ↑
                      Controle via CED
```

**⚠️ NUNCA conectar direto da rede - sempre através do contator!**

---

### PASSO 5️⃣: Barramento DC (Item 14 - DC Bus)
**📍 Localização**: Superior do módulo

**O que conectar:**
- Cabos que vão para o servo drive que aciona o motor SEW
- **DC+** e **DC-** (barramento positivo e negativo)

**Função:**
- O módulo 2198-P031 converte AC→DC e fornece no barramento
- Vários drives podem compartilhar o mesmo barramento DC

**Para o seu caso (motor SEW):**
- Precisa de um **servo drive Kinetix** separado entre o DC bus e o motor
- O 2198-P031 sozinho NÃO aciona motor - só fornece DC

**Especificações:**
- Tensão DC: ~540-800V DC (depende da tensão AC de entrada)
- Cabo dimensionado para corrente do motor

---

### CONEXÕES OPCIONAIS (podem ficar para depois)

#### Item 13 - Shunt Resistor (RC)
**Função:** Dissipação de energia durante frenagem regenerativa
**Quando usar:** Se o motor freiar rapidamente (energia retorna ao barramento)
**Seu caso:** Provavelmente não necessário inicialmente

#### Item 1 - Digital Inputs (IOD)
**Função:** Sinais de controle digitais (start, stop, reset, etc)
**Quando usar:** Para integração com PLC ou painel de controle
**Seu caso:** Pode ficar para comissionamento avançado

#### Item 2 e 3 - Ethernet (PORT1/PORT2)
**Função:** Comunicação EtherNet/IP com PLC ou supervisório
**Quando usar:** Integração com sistema de automação
**Seu caso:** Não essencial para testes iniciais

---

## ⚠️ OBSERVAÇÃO CRÍTICA SOBRE O SISTEMA

**O módulo 2198-P031 é um DC BUS SUPPLY, NÃO um servo drive completo!**

Isso significa:
- ✅ Ele converte AC (380V trifásico) → DC (540-800V DC)
- ✅ Ele fornece energia DC no barramento
- ❌ Ele **NÃO controla motor diretamente**

**Para acionar o motor SEW, você precisa de:**
```
[Rede AC] → [2198-P031 DC Supply] → [Servo Drive Kinetix] → [Motor SEW]
                                      (exemplo: 2198-H015)
```

**Verificar:**
- Você tem um **servo drive Kinetix** adicional (série 2198-Hxxx ou 2198-Dxxx)?
- Se SIM: O DC bus (item 14) conecta ao servo drive
- Se NÃO: Precisará adquirir um servo drive compatível

---

## Sequência de Instalação Recomendada

### Preparação
1. ✅ **Desligar toda alimentação** e confirmar ausência de tensão com multímetro
2. ✅ **Verificar ferramentas e EPIs** (chaves, multímetro, luvas isolantes)

### Conexões (na ordem)
3. **PASSO 1**: Aterramento (Item 12)
4. **PASSO 2**: Alimentação 24V DC (Item 15 - CP)
5. **PASSO 3**: Controle do contator (Item 11 - CED)
6. **PASSO 4**: Alimentação AC trifásica (Item 16 - IPD)
7. **PASSO 5**: Barramento DC para servo drive (Item 14 - DC)

### Verificação
8. ✅ **Revisar todas conexões** (aperto, polaridade, bitola)
9. ✅ **Verificar contator** está no circuito de AC
10. ✅ **Medir resistência de aterramento** (< 1 ohm)

### Energização (CUIDADO)
11. ⚡ **Ligar fonte 24V DC primeiro**
12. ⚡ **Verificar display LCD** acende (se houver)
13. ⚡ **Energizar AC** (através do contator)
14. ⚡ **Observar LEDs de status** (módulo deve ficar pronto)

---

## Links de Referência para Download dos Manuais

**Documentação Oficial da Rockwell Automation:**

- [Kinetix 5700 DC-bus Power Supply - Installation Instructions (PDF)](https://literature.rockwellautomation.com/idc/groups/literature/documents/in/2198-in009_-en-p.pdf)
- [Kinetix 5700 Servo Drive Product Profile](https://literature.rockwellautomation.com/idc/groups/literature/documents/pp/2198-pp002_-en-p.pdf)
- [User Manual - ManualsLib](https://www.manualslib.com/manual/2429350/Rockwell-Automation-Allen-Bradley-Kinetix-5700.html)
- [Installation Instructions Manual - ManualsLib](https://www.manualslib.com/manual/1593804/Rockwell-Automation-Allen-Bradley-Kinetix-5700-Series.html)
- [Drives in Common Bus Configurations](https://literature.rockwellautomation.com/idc/groups/literature/documents/at/motion-at007_-en-p.pdf)

---

---

## 📋 CHECKLIST DE VERIFICAÇÃO PRÉ-ENERGIZAÇÃO

**Antes de ligar pela primeira vez:**

### Verificações Elétricas
- [ ] **Item 12 (Ground)**: Aterramento instalado com cabo trançado
- [ ] **Item 15 (CP)**: 24V DC conectado com polaridade correta
- [ ] **Item 11 (CED)**: Controle do contator instalado em série
- [ ] **Item 16 (IPD)**: AC trifásico passa por contator antes do módulo
- [ ] **Item 14 (DC)**: Barramento DC conectado ao servo drive (se houver)
- [ ] Todos os terminais bem apertados (sem fios soltos)
- [ ] Cabos com bitola adequada (mínimo 6mm² para AC)

### Verificações Mecânicas
- [ ] Módulo fixado firmemente no painel
- [ ] Ventilador (Item 17) livre de obstruções
- [ ] Não há ferramentas ou objetos dentro do painel
- [ ] Tampa do painel fechada (se aplicável)

### Verificações de Segurança
- [ ] Proteção (disjuntor/fusível) dimensionada corretamente
- [ ] Contator AC está acessível para desligamento
- [ ] EPIs disponíveis (luvas, óculos, capacete)
- [ ] Área sinalizada (trabalho em eletricidade)

---

## ❓ DÚVIDA CRÍTICA PARA RESOLVER

**Você tem um SERVO DRIVE Kinetix além do DC Supply?**

O módulo na imagem (2198-P031) só fornece energia DC. Para acionar o motor SEW, você precisa de um módulo adicional tipo:
- **2198-H015** (servo drive 1.5kW)
- **2198-H025** (servo drive 2.5kW)
- **2198-D012** (servo drive compacto)

**Verificar:**
1. Olhe se tem outro módulo Kinetix no painel além do 2198-P031
2. Se sim, tire foto para identificarmos
3. Se não, precisaremos planejar a aquisição

---

## 📸 Próximos Passos

- [ ] **Tirar fotos das conexões atuais** em cada conector
- [ ] **Identificar se há servo drive** além do DC supply
- [ ] **Medir tensão da fonte 24V DC** disponível
- [ ] **Verificar esquema elétrico** do painel (se houver)
- [ ] **Download do manual completo** Publication 2198-IN009
- [ ] **Documentar estado atual** antes de qualquer mudança

---

## Notas de Segurança

⚠️ **ATENÇÃO:**
- Sempre desenergizar o sistema antes de trabalhar nas conexões
- Utilizar EPIs adequados (luvas isolantes classe apropriada)
- Verificar ausência de tensão com multímetro antes de tocar em terminais
- Seguir procedimentos LOTO (Lockout/Tagout) da empresa
- Consultar eletricista qualificado se houver dúvidas

---

## Informações do Equipamento

**Inversor:** Rockwell Allen-Bradley Kinetix 5700
- **Modelo**: 2198-P031
- **Tipo**: DC Bus Supply
- **Corrente**: 31.6A
- **Entrada**: 324-528 Vac (3 fases)
- **Plant**: 1100
- **Ano**: 2018

**Motor:** SEW-EURODRIVE
- **Tipo**: DT71D4/BMG/TH/ES1S
- **Potência**: 0.37kW @ 60Hz
- **Tensão**: 230Δ / 400Y V
- **Corrente**: 2.09A / 1.19A
- **Rotação**: 1710 RPM

---

## 📷 Referências de Imagens

- `999. Imagens\00025. InversorRockwell_Plaquinha.jpeg` - Placa de identificação do inversor
- `999. Imagens\00026. InversorRockwell.jpeg` - Vista frontal dos inversores Kinetix 5700
- `999. Imagens\00027. SEW.jpeg` - Placa de identificação do motor SEW
- `999. Imagens\00032. P031_Conections.png` - **Diagrama oficial de conectores do 2198-P031**
