# Conexões do Kinetix 5700 Servo Drive (2198-D012)

> **Referência**: Rockwell Automation Publication 2198-UM002
> **Data**: 2026-02-11
> **Status**: ⏳ Aguardando diagrama oficial - estrutura preparada

---

## 📋 SOBRE ESTE DOCUMENTO

Este documento está sendo preparado para documentar as conexões do **servo drive 2198-D012**.

**Próximos passos:**
1. ✅ Manuais localizados
2. ⏳ Aguardando imagem do diagrama de conexões
3. ⏳ Identificação completa dos conectores
4. ⏳ Orientações passo a passo de instalação

---

## Diagrama do Módulo 2198-D012 (Dual-axis Inverter)

![Diagrama de Conectores do Kinetix 5700 D012](../../../999.%20Imagens/00033..png)

*Figura: Vista frontal, superior e inferior do módulo 2198-Dxxx-ERSx (dual-axis inverter) com conectores identificados*

**Nota**: Imagem mostra modelo D006-ERSx, mas a estrutura de conectores é idêntica ao D012.

---

## O que é o 2198-D012?

**Tipo**: Servo Drive Dual-Axis (Inversor de Dois Eixos)

**Função no Sistema:**
```
[2198-P031] ──DC Bus──> [2198-D012] ──AC Motor──> [Motor SEW]
 DC Supply               Servo Drive              0.37kW
```

**Diferença do P031:**
- **P031**: Converte AC da rede → DC no barramento (fonte de energia)
- **D012**: Recebe DC do barramento → controla motor (drive de acionamento)

---

## Mapa Completo de Conectores (Referência da Imagem)

### 🔴 Conectores ESSENCIAIS (necessários para funcionar)

| Item | Conector | Localização | Função |
|------|----------|-------------|--------|
| **2** | Ground Lug | Frontal (inferior) | 🔴 **CRÍTICO** - Aterramento |
| **19** | DC Bus (DC) | Superior | 🔴 **ESSENCIAL** - Recebe DC do P031 |
| **20** | 24V Control Power (CP) | Superior | 🔴 **ESSENCIAL** - Alimentação controle |
| **22** | Motor Power (MP) - A | Inferior | 🔴 **ESSENCIAL** - Saída motor Eixo A |
| **23** | Motor Power (MP) - B | Inferior | 🔴 **ESSENCIAL** - Saída motor Eixo B |
| **3** | Motor Feedback (MF) - A | Frontal | 🔴 **ESSENCIAL** - Encoder Eixo A |
| **4** | Motor Feedback (MF) - B | Frontal | 🔴 **ESSENCIAL** - Encoder Eixo B |

### 🟡 Conectores OPCIONAIS (para funcionalidades avançadas)

| Item | Conector | Localização | Função |
|------|----------|-------------|--------|
| **7** | Digital Inputs (IOD) - A | Frontal | 🟡 Sinais controle Eixo A |
| **8** | Digital Inputs (IOD) - B | Frontal | 🟡 Sinais controle Eixo B |
| **5** | Universal Feedback (UFB) - A | Frontal | 🟡 Encoder alternativo A |
| **6** | Universal Feedback (UFB) - B | Frontal | 🟡 Encoder alternativo B |
| **21** | Motor Brake (BC) - A | Inferior | 🟡 Freio motor Eixo A |
| **24** | Motor Brake (BC) - B | Inferior | 🟡 Freio motor Eixo B |
| **18** | Safe Torque-Off (STO) | Superior | 🟡 Segurança funcional |
| **9** | Ethernet PORT1 (RJ45) | Frontal | 🟡 EtherNet/IP |
| **10** | Ethernet PORT2 (RJ45) | Frontal | 🟡 EtherNet/IP |

### ℹ️ Elementos Informativos e Mecânicos

| Item | Elemento | Localização | Descrição |
|------|----------|-------------|-----------|
| **1** | Motor Cable Clamp | Frontal (base) | Fixação dos cabos |
| **11** | Zero-stack Mounting Tab | Frontal (topo) | Montagem empilhada |
| **12** | Module Status Indicator | Frontal | LED de status |
| **13** | Network Status Indicator | Frontal | LED rede |
| **14** | LCD Display | Frontal | Display informativo |
| **15** | Navigation Push Buttons | Frontal | Botões navegação |
| **16** | Link Speed Status | Frontal | LED velocidade rede |
| **17** | Link/Activity Status | Frontal | LED atividade rede |
| **25** | Cooling Fan | Inferior | Ventilação automática |

---

## 🔧 GUIA PASSO A PASSO DE CONEXÃO

### ⚠️ ANTES DE COMEÇAR
- ✅ Desligue TODA a alimentação elétrica
- ✅ Confirme ausência de tensão com multímetro
- ✅ Use EPIs adequados (luvas isolantes)
- ✅ Siga procedimentos LOTO da empresa
- ✅ Verifique que o **2198-P031 está instalado e funcionando**

---

## Conexões Necessárias para Acionar o Motor SEW

### PASSO 1️⃣: Aterramento (Item 2 - Ground Lug)
**📍 Localização**: Frontal, parte inferior do módulo

**O que conectar:**
- Cabo flexível trançado (braided ground strap)
- Conectar ao mesmo barramento de terra do painel (igual ao P031)

**Especificações:**
- Conexão de baixa impedância
- Aperto firme com torque adequado
- **Mesmo potencial de terra** do P031

**⚠️ FAZER PRIMEIRO - Base de toda segurança elétrica!**

---

### PASSO 2️⃣: Barramento DC (Item 19 - DC Bus)
**📍 Localização**: Superior do módulo

**O que conectar:**
- **DC+** e **DC-** vindos do 2198-P031 (Item 14 do P031)
- Usar conectores shared-bus apropriados

**Especificações:**
- Tensão: 540-800V DC (fornecida pelo P031)
- Corrente: Dimensionar para potência total dos motores
- Cabo: Mínimo calculado pela corrente (motor 0.37kW ≈ 2-3A DC)

**⚠️ ATENÇÃO - ALTA TENSÃO DC:**
- Pode ter até 800V DC!
- Aguardar 5 minutos após desligar para descarga de capacitores
- Usar multímetro para confirmar 0V antes de tocar

**Função:**
- Recebe energia DC para converter em AC variável trifásico

---

### PASSO 3️⃣: Alimentação de Controle (Item 20 - CP 24V)
**📍 Localização**: Superior do módulo

**O que conectar:**
- **Positivo (+)**: 24V DC da mesma fonte usada no P031
- **Negativo (-)**: 0V (comum) da fonte

**Especificações:**
- Tensão: 24V DC estabilizada (±10%)
- Corrente típica: 2-3A (consultar manual específico)
- **Mesma fonte** usada no Item 15 do P031

**⚠️ SEM ISSO O DRIVE NÃO LIGA A LÓGICA DE CONTROLE!**

**Verificação:**
- LED Item 12 (Module Status) deve acender quando 24V aplicado

---

### PASSO 4️⃣: Saída para Motor (Item 22 ou 23 - Motor Power)
**📍 Localização**: Inferior do módulo

**Para o Motor SEW (Eixo único):**
- Use **Item 22 (MP-A)** ou **Item 23 (MP-B)** - escolha um eixo
- Conectar **U, V, W** ao motor SEW

**Especificações do Motor SEW:**
- Tensão: 230Δ / 400Y (V)
- Corrente: 2.09A / 1.19A
- Potência: 0.37kW @ 60Hz
- Rotação: 1710 RPM

**Cabo de Motor:**
- Tipo: Cabo blindado específico para servo (recomendado Rockwell)
- Bitola: AWG 14-16 (1.5-2.5mm²) para 0.37kW
- Comprimento máximo: Verificar manual (geralmente 50-100m)

**⚠️ IMPORTANTE:**
- Verificar se motor está em **400Y** (estrela) para uso com drive
- **NÃO conectar em 230Δ** - drive fornece tensão de fase!
- Usar Item 1 (Motor Cable Clamp) para fixar cabo

**Configuração do Motor:**
```
Motor SEW placa: 230Δ / 400Y
Para drive: Usar 400Y (estrela)
Tensão fase-neutro: ~230V
Tensão fase-fase: 400V
```

---

### PASSO 5️⃣: Encoder (Item 3 ou 4 - Motor Feedback MF)
**📍 Localização**: Frontal do módulo

**Para o Motor SEW:**
- Conectar no **Item 3 (MF-A)** se usar eixo A, ou
- Conectar no **Item 4 (MF-B)** se usar eixo B

**Verificar se Motor SEW tem Encoder:**
- Olhar placa do motor: procurar por "TH" ou "ES1S" (pode indicar encoder)
- Verificar se há cabo adicional saindo do motor
- Encoder típico: incremental (A, B, Z) ou absoluto

**Se NÃO tiver encoder:**
- Motor pode operar em modo **V/F (Volts/Hertz)**
- Controle de velocidade em malha aberta
- Sem controle preciso de posição

**Se TEM encoder:**
- Necessário para controle vetorial
- Controle preciso de velocidade e torque
- Consultar pinout do encoder do motor SEW

**Alternativamente (Item 5 ou 6 - UFB):**
- Universal Feedback pode aceitar outros tipos de encoder
- Resolver, sin/cos, EnDat, etc.

---

### PASSO 6️⃣ (OPCIONAL): Freio do Motor (Item 21 ou 24 - BC)
**📍 Localização**: Inferior do módulo

**Se motor SEW tiver freio eletromagnético:**
- Conectar no **Item 21 (BC-A)** ou **Item 24 (BC-B)**
- Drive controla abertura/fechamento automático

**Verificar motor:**
- Procurar por "BRG" ou "BR" na placa (indica brake/freio)
- Freio típico: 24V DC ou 90V DC
- Configurar parâmetros do drive para controle do freio

**Se motor NÃO tem freio:**
- Deixar desconectado
- Não é necessário para aplicação horizontal simples

---

---

## ⚠️ OBSERVAÇÃO: Drive DUAL-AXIS (Dois Eixos)

**O 2198-D012 pode controlar ATÉ 2 MOTORES simultaneamente!**

### Configuração no Seu Caso (Motor SEW único):

```
┌─────────────────────────────────────────┐
│        2198-D012 (Dual-Axis)            │
│                                         │
│  EIXO A                    EIXO B       │
│  ┌─────────┐              ┌─────────┐  │
│  │ MP-A(22)│──────>       │ MP-B(23)│  │
│  │ MF-A(3) │   Motor      │ MF-B(4) │  │
│  │ BC-A(21)│    SEW       │ BC-B(24)│  │
│  │ IOD-A(7)│   0.37kW     │ IOD-B(8)│  │
│  └─────────┘              └─────────┘  │
│      ✅ USADO              ❌ NÃO USADO  │
└─────────────────────────────────────────┘
```

**Escolha UM eixo para usar:**
- **Recomendado: Eixo A** (conectores Item 22, 3, 21, 7)
- Deixe Eixo B desconectado (ou use para motor futuro)

**Vantagem:**
- Pode adicionar um segundo motor no futuro
- Compartilha o mesmo DC bus
- Economia de espaço (2 drives em 1 módulo)

---

### CONEXÕES OPCIONAIS (podem ficar para depois)

#### Item 7/8 - Digital I/O (IOD)
**Função:** Sinais de controle digitais
- Enable/disable drive
- Start/stop comandos
- Reset de falhas
- Sinais de alarme/status

**Quando usar:**
- Integração com PLC
- Painel de controle local
- Intertravamentos de segurança

**Seu caso:** Pode ficar para comissionamento avançado

---

#### Item 9/10 - Ethernet (PORT1/PORT2)
**Função:** Comunicação EtherNet/IP
- Controle pelo PLC via rede
- Monitoramento supervisório
- Diagnóstico remoto

**Quando usar:**
- Sistema de automação integrado
- SCADA/HMI remoto

**Seu caso:** Não essencial para testes iniciais

---

#### Item 18 - Safe Torque-Off (STO)
**Função:** Segurança funcional SIL 2/PLd
- Desabilita torque do motor instantaneamente
- Função de segurança certificada
- Independente do controle principal

**Quando usar:**
- Requisitos de segurança funcional
- Máquinas com risco de movimento perigoso
- Certificações CE/NR12

**Seu caso:**
- Verificar se é requisito de segurança
- Pode ser necessário conectar em série com circuito de emergência

---

#### Item 21/24 - Motor Brake (BC)
**Função:** Controle de freio eletromagnético
- Abre freio antes de movimento
- Fecha freio ao parar
- Controle automático sincronizado

**Quando usar:**
- Aplicações verticais (elevação)
- Motor com freio de estacionamento
- Quando parada precisa sem deriva

**Seu caso:**
- ✅ **VERIFICAR**: Motor SEW tem freio?
- Olhar placa: se tiver "BRG" ou "BR" = tem freio
- Se NÃO tem, deixar desconectado

---

## ⚠️ OBSERVAÇÃO IMPORTANTE

**Integração com o Sistema:**

```
┌─────────────┐      DC Bus      ┌─────────────┐      U,V,W      ┌──────────┐
│ 2198-P031   │─────────────────>│ 2198-D012   │────────────────>│ Motor    │
│ DC Supply   │  540-800V DC     │ Servo Drive │  AC Variável    │ SEW      │
│             │                  │             │  0-400V @ 60Hz  │ 0.37kW   │
└─────────────┘                  └─────────────┘                 └──────────┘
      ↑                                 ↑                              ↑
   380V 3Φ                           24V DC                       Encoder?
```

**Verificar:**
- [x] Temos 2198-P031 (DC Supply) ✅
- [x] Temos 2198-D012 (Servo Drive) ✅ (a confirmar com imagem)
- [x] Temos Motor SEW ✅
- [ ] Motor SEW tem encoder? 🔍 Verificar
- [ ] Temos cabo de motor adequado? 🔍 Verificar

---

## Sequência de Instalação Recomendada

### Preparação
1. ✅ **P031 já instalado e testado** (pré-requisito)
2. ✅ **Desligar toda alimentação** do sistema
3. ✅ **Verificar ferramentas e EPIs**

### Conexões (na ordem)
4. **PASSO 1**: Aterramento do D012
5. **PASSO 2**: Barramento DC (P031 → D012)
6. **PASSO 3**: Alimentação 24V DC
7. **PASSO 4**: Cabos do motor (U, V, W)
8. **PASSO 5**: Encoder (se houver)

### Verificação
9. ✅ **Revisar todas conexões** (aperto, polaridade, bitola)
10. ✅ **Verificar isolamento** dos cabos do motor
11. ✅ **Medir resistência de aterramento**

### Energização (CUIDADO)
12. ⚡ **Ligar fonte 24V DC**
13. ⚡ **Verificar LEDs de status** do D012
14. ⚡ **Energizar P031** (AC trifásico)
15. ⚡ **Observar barramento DC** está disponível
16. ⚡ **Habilitar D012** via parâmetros/HMI

---

## 📋 CHECKLIST COMPLETO DE VERIFICAÇÃO PRÉ-ENERGIZAÇÃO

**Antes de ligar pela primeira vez:**

### ✅ Verificações Elétricas do D012

**Conexões Essenciais:**
- [ ] **Item 2 (Ground)**: Aterramento instalado com cabo trançado
- [ ] **Item 19 (DC Bus)**: DC+/DC- conectados do P031 (Item 14)
- [ ] **Item 20 (CP)**: 24V DC conectado com polaridade correta (+/-)
- [ ] **Item 22 (MP-A)** ou **Item 23 (MP-B)**: Motor power conectado (U, V, W)
- [ ] **Item 3 (MF-A)** ou **Item 4 (MF-B)**: Encoder conectado (se motor tiver)
- [ ] **Item 1**: Cabos fixados no motor cable clamp
- [ ] Todos os terminais bem apertados (torque adequado)

**Conexões Opcionais (se aplicável):**
- [ ] **Item 21/24 (BC)**: Freio conectado (se motor tiver freio)
- [ ] **Item 18 (STO)**: Safe torque-off (se requisito de segurança)
- [ ] **Item 7/8 (IOD)**: Entradas digitais (se usar controle por PLC)
- [ ] **Item 9/10**: Ethernet conectada (se usar comunicação)

---

### ✅ Verificações do Motor SEW

**Inspeção Visual:**
- [ ] Verificar placa do motor: tensão nominal 230Δ / 400Y
- [ ] **CRÍTICO**: Confirmar jumpers em configuração **400Y (estrela)**
- [ ] Verificar se há encoder: cabo adicional saindo do motor
- [ ] Verificar se há freio: procurar "BRG" ou "BR" na placa
- [ ] Motor está fixado mecanicamente de forma segura
- [ ] Eixo do motor gira livre (sem travamentos)

**Medições Elétricas:**
- [ ] Medir resistência entre fases U-V, V-W, W-U (deve ser balanceado ±5%)
- [ ] Medir isolamento fase-terra com megôhmetro (> 1MΩ @ 500V)
- [ ] Verificar continuidade do PE (terra) do motor
- [ ] Se tem encoder: verificar resistência dos pinos (consultar datasheet SEW)

**Valores Esperados:**
- Resistência entre fases: ~10-50Ω (depende do motor 0.37kW)
- Isolamento > 1MΩ (novo) ou > 0.5MΩ (usado mas OK)
- Terra: < 0.1Ω (continuidade perfeita)

---

### ✅ Verificações do Sistema Completo

**P031 (DC Supply):**
- [ ] P031 já testado e funcionando (pré-requisito)
- [ ] Barramento DC disponível no Item 14 do P031
- [ ] Tensão DC medida: 540-800V DC (desligado capacitores descarregados)
- [ ] LED de status do P031 indica "pronto"

**Cabeamento:**
- [ ] Cabos de motor blindados e aterrados
- [ ] Bitola adequada: motor 0.37kW = AWG 14-16 (1.5-2.5mm²)
- [ ] Comprimento < 50m (recomendado para cabo padrão)
- [ ] Separação de cabos: potência ≠ sinal (mínimo 30cm)
- [ ] Identificação clara: U, V, W, PE

**Aterramento:**
- [ ] P031 ground conectado ao barramento de terra
- [ ] D012 ground (Item 2) conectado ao mesmo barramento
- [ ] Motor PE conectado
- [ ] Barramento de terra do painel conectado ao terra geral
- [ ] Resistência total de aterramento < 1Ω

---

### ✅ Verificações de Segurança

**Segurança Elétrica:**
- [ ] Sistema desenergizado e bloqueado (LOTO)
- [ ] Multímetro disponível para medições
- [ ] EPIs: luvas isolantes classe 2 (até 1000V), óculos, capacete
- [ ] Extintor de CO₂ ou pó químico disponível (Classe C)
- [ ] Sinalização: "Trabalho em Eletricidade - Não Ligar"

**Segurança Mecânica:**
- [ ] Motor livre para girar sem obstáculos
- [ ] Acoplamentos instalados corretamente (se houver)
- [ ] Proteções mecânicas instaladas (guardas, tampas)
- [ ] Área livre de pessoas durante energização

**Procedimentos:**
- [ ] Plano de emergência definido (quem desliga, onde está disjuntor)
- [ ] Pessoa qualificada presente (eletricista/técnico)
- [ ] Telefone de emergência acessível
- [ ] Procedimento de descarga de capacitores conhecido (5 min)

---

### ✅ Verificações de Parâmetros (após energizar)

**A configurar no D012 antes de girar motor:**
- [ ] Tensão nominal do motor: 400V
- [ ] Corrente nominal: 1.19A (configuração estrela)
- [ ] Frequência nominal: 60Hz
- [ ] Rotação nominal: 1710 RPM
- [ ] Tipo de encoder (se houver): incremental/absoluto
- [ ] Resolução do encoder: PPR (pulsos por revolução)
- [ ] Modo de controle: vetorial com encoder / V/F sem encoder
- [ ] Rampa de aceleração: começar com 5-10s (conservador)
- [ ] Rampa de desaceleração: começar com 5-10s
- [ ] Limite de corrente: 150% da nominal (1.79A)

---

### ⚠️ CHECKLIST DE PRIMEIRA ENERGIZAÇÃO

**Sequência OBRIGATÓRIA:**

1. [ ] **P031 ligado** e barramento DC estável
2. [ ] **Aplicar 24V DC** no Item 20 do D012
3. [ ] **Verificar LED** Item 12 (Module Status) acende
4. [ ] **Display LCD** Item 14 mostra informações (se houver)
5. [ ] **Sem alarmes** - verificar display/LEDs
6. [ ] **Configurar parâmetros** do motor via HMI/software
7. [ ] **Habilitar drive** (via IOD ou parâmetro)
8. [ ] **Comando de movimento lento** (10% velocidade nominal)
9. [ ] **Observar rotação** - motor gira suave sem vibrações
10. [ ] **Teste de parada** - desacelera conforme rampa
11. [ ] **Aumentar gradualmente** velocidade até nominal
12. [ ] **Testar reversão** (se aplicável)
13. [ ] **Verificar corrente** não excede nominal
14. [ ] **Temperatura** motor e drive (não deve aquecer excessivamente)

---

## 📥 Links para Download dos Manuais

**Sources:**
- [Allen-Bradley Kinetix 5700 Servo Drive Product Profile](https://literature.rockwellautomation.com/idc/groups/literature/documents/pp/2198-pp002_-en-p.pdf) - Product Profile
- [Kinetix 5700 User Manual - ManualsLib](https://www.manualslib.com/manual/1501926/Allen-Bradley-Kinetix-5700.html) - Complete User Manual
- [Rockwell Automation Kinetix 5700 User Manual](https://www.manualslib.com/manual/2429350/Rockwell-Automation-Allen-Bradley-Kinetix-5700.html) - Official Documentation
- [Kinetix 5700 Dual-axis Inverters](https://literature.rockwellautomation.com/idc/groups/literature/documents/pc/2198-pc002_-en-p.pdf) - D012 específico
- [Kinetix 5700 Installation Instructions](https://literature.rockwellautomation.com/idc/groups/literature/documents/in/2198-in009_-en-p.pdf) - Installation Guide
- [Kinetix 5700 Technical Data](https://literature.rockwellautomation.com/idc/groups/literature/documents/td/knx-td003_-en-p.pdf) - Specifications (KNX-TD003)

**Principais Publicações:**
- **2198-UM002**: User Manual (conexões, configuração, troubleshooting)
- **2198-IN009**: Installation Instructions
- **KNX-TD003**: Technical Data / Specifications

---

## 📸 Próximos Passos PRÁTICOS

### Verificações Físicas Necessárias:

- [ ] **Tirar foto do painel** mostrando P031 e D012 instalados
- [ ] **Verificar se motor SEW tem encoder** (cabo extra saindo do motor)
- [ ] **Verificar se motor SEW tem freio** (procurar BRG/BR na placa)
- [ ] **Confirmar configuração** do motor (estrela 400Y)
- [ ] **Medir bitola dos cabos** de motor instalados
- [ ] **Verificar estado atual** das conexões do D012
- [ ] **Identificar fonte 24V DC** disponível no painel
- [ ] **Verificar se DC bus** já está conectado entre P031 e D012

### Documentação:

- [x] **Imagem do diagrama** adicionada (00033..png) ✅
- [x] **Identificados todos** os 25 conectores ✅
- [x] **Tabela completa** de conectores ✅
- [x] **Instruções passo a passo** detalhadas ✅
- [x] **Checklist específico** criado ✅
- [x] **Parâmetros iniciais** documentados ✅

### Próximas Ações:

1. **Inspeção visual** do motor SEW (encoder? freio?)
2. **Fotos do estado atual** das conexões
3. **Medir tensões** disponíveis (24V DC, barramento DC)
4. **Planejar fiação** com base no estado atual
5. **Preparar parametrização** com dados do motor

---

## Notas de Segurança

⚠️ **ATENÇÃO - ALTA TENSÃO DC:**
- Barramento DC pode ter até **800V DC**
- **MUITO MAIS PERIGOSO** que AC pela dificuldade de soltar
- Aguardar **5 minutos** após desligar para descarga de capacitores
- Usar EPI classe 2 (até 1000V)
- **NUNCA** tocar em terminais DC sem verificar tensão

---

## Informações do Equipamento

**Servo Drive:** Rockwell Allen-Bradley Kinetix 5700
- **Modelo**: 2198-D012 (Dual-Axis Inverter)
- **Função**: Controle de servo motor
- **Entrada**: DC Bus (~540-800V DC)
- **Saída**: AC variável (U, V, W) para motor

**Motor:** SEW-EURODRIVE
- **Tipo**: DT71D4/BMG/TH/ES1S
- **Potência**: 0.37kW @ 60Hz
- **Tensão**: 230Δ / 400Y V
- **Corrente**: 2.09A / 1.19A
- **Rotação**: 1710 RPM

**DC Supply:** 2198-P031 (já documentado)
- Fornece barramento DC para o D012

---

## 📷 Referências de Imagens

- `999. Imagens\00025. InversorRockwell_Plaquinha.jpeg` - Placa de identificação inversor
- `999. Imagens\00026. InversorRockwell.jpeg` - Vista frontal Kinetix 5700
- `999. Imagens\00027. SEW.jpeg` - Placa identificação motor SEW
- `999. Imagens\00032. P031_Conections.png` - Diagrama oficial P031 (DC Supply)
- `999. Imagens\00033..png` - **Diagrama oficial D012 (Dual-axis Inverter)** ✅
