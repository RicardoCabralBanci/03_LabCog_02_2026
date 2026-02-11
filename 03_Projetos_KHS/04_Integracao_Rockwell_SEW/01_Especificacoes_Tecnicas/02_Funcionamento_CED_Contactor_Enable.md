# Entendendo o CED (Contactor Enable) - Item 11

> **Contexto**: Explicação da função do conector CED no módulo Kinetix 5700 2198-P031
> **Data**: 2026-02-11

---

## O que é o CED (Item 11)?

**CED = Contactor Enable Device** (Dispositivo de Habilitação do Contator)

É um **relé de segurança interno** do módulo 2198-P031 que funciona como um "sinal de OK" do inversor.

---

## Como Funciona?

O CED é um **contato seco** (dry contact) que:

### Estado Normal (inversor desligado ou com falha)
- **Contato ABERTO** (sem continuidade)
- Impede que o contator AC energize
- Circuito de controle do contator fica interrompido

### Estado Pronto (inversor OK para operar)
- **Contato FECHA** (tem continuidade)
- Permite que o contator AC energize
- Sistema pode ligar com segurança

---

## Por que em Série com a Bobina do Contator?

### Esquema de Segurança:

```
                    ┌─────────────────┐
                    │  Kinetix 5700   │
24V DC ─┬───────────┤  (Item 15-CP)   │
        │           │  Lógica Interna │
        │           └─────────────────┘
        │                    │
        │              ┌─────▼─────┐
        │              │  CED (11) │ ◄── Relé interno do inversor
        │              │  Contato  │
        │              └─────┬─────┘
        │                    │
        ├──[Botão START]────┤
        │                    │
        └────────[CED]───────┴───[Bobina Contator AC]───┐
                                                          │
                                                         0V
```

---

## Sequência de Funcionamento

### Passo 1: Sistema desenergizado
```
24V DC → [Botão START] → [CED ABERTO] ✗ [Bobina Contator] → 0V
                          └─ SEM CONTINUIDADE
```
- CED está aberto
- Bobina do contator NÃO recebe tensão
- Contator AC não fecha
- Inversor não recebe energia AC

### Passo 2: Energizar 24V DC no CP (Item 15)
```
Kinetix 5700 recebe 24V DC (Item 15)
  ↓
Lógica interna inicializa
  ↓
Faz auto-diagnóstico (verifica capacitores, circuitos, etc)
  ↓
Se tudo OK → CED FECHA
```

### Passo 3: Pressionar botão START
```
24V DC → [Botão START PRESSIONADO] → [CED FECHADO] ✓ → [Bobina Contator] → 0V
                                       └─ TEM CONTINUIDADE!
```
- CED já está fechado (inversor pronto)
- Botão START completa o circuito
- Bobina do contator recebe 24V DC
- Contator AC fecha seus contatos principais
- Energia AC chega ao IPD (Item 16)
- Sistema energizado!

---

## Por que isso é Importante? (Segurança)

### ⚠️ Proteção contra Energização Perigosa

**SEM o CED no circuito:**
```
24V → [Botão START] → [Bobina Contator] → 0V
```
- Qualquer um pode ligar o inversor apertando START
- Mesmo se inversor tiver FALHA GRAVE
- Mesmo se capacitores estiverem danificados
- **PERIGO DE EXPLOSÃO/INCÊNDIO**

**COM o CED no circuito:**
```
24V → [Botão START] → [CED] → [Bobina Contator] → 0V
```
- Inversor faz auto-diagnóstico ANTES de permitir energização
- Se detectar problema → CED NÃO fecha
- Contator não energiza mesmo apertando START
- Sistema fica SEGURO

---

## Exemplo Prático de Proteção

### Cenário 1: Capacitor danificado
1. Você liga o 24V DC (Item 15)
2. Inversor detecta capacitor com problema
3. **CED permanece ABERTO**
4. Você aperta START → nada acontece
5. Display mostra código de erro
6. ✅ Sistema protegido!

### Cenário 2: Tudo funcionando
1. Você liga o 24V DC (Item 15)
2. Inversor faz diagnóstico → tudo OK
3. **CED FECHA automaticamente**
4. LED de status fica verde
5. Você aperta START → contator energiza
6. ✅ Sistema liga com segurança!

---

## Como Conectar o CED (Item 11)

### Tipo de Conector
- **Contato seco** (sem tensão, apenas chaveamento)
- Geralmente **NA (Normalmente Aberto)**
- Capacidade típica: 24V DC @ 2A

### Diagrama de Ligação Completo

```
┌─────────────────────────────────────────────────────────┐
│                    PAINEL DE CONTROLE                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Fonte 24V DC                                           │
│    (+) ────┬─────────────────────────────┐              │
│            │                              │              │
│            │  ┌──────────────┐            │              │
│            ├──┤ Kinetix 5700 │            │              │
│            │  │  CP (Item 15)│            │              │
│            │  └──────────────┘            │              │
│            │         │                    │              │
│            │    ┌────▼────┐               │              │
│            │    │   CED   │◄──────────────┘              │
│            │    │ (Item 11)               Sinal interno  │
│            │    └────┬────┘               "inversor OK"  │
│            │         │                                    │
│            │    ┌────▼────┐                               │
│            ├────┤ Botão   │                               │
│            │    │  START  │                               │
│            │    └────┬────┘                               │
│            │         │                                    │
│            │    ┌────▼────┐                               │
│            └────┤ Bobina  │                               │
│                 │Contator │                               │
│                 │   AC    │                               │
│                 └────┬────┘                               │
│    (0V) ────────────┘                                     │
│                                                           │
│  Contator AC (Contatos Principais)                       │
│                                                           │
│    L1 ───┬───[Contato]───┬─── IPD L1 (Item 16)          │
│    L2 ───┼───[Contato]───┼─── IPD L2                     │
│    L3 ───┴───[Contato]───┴─── IPD L3                     │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## Resumo da Função

| Aspecto | Descrição |
|---------|-----------|
| **Tipo** | Relé de segurança (contato seco NA) |
| **Função** | Habilitar energização AC somente se inversor está OK |
| **Quando fecha** | Após diagnóstico bem-sucedido na inicialização |
| **Quando abre** | Falha detectada, emergência, ou desligamento |
| **Por que em série** | Interromper circuito se inversor não estiver pronto |
| **Segurança** | Previne energização com falhas no sistema |

---

## ⚠️ IMPORTANTE

**O CED NÃO é opcional!**

Conectar o AC (Item 16) **direto** sem passar pelo controle do CED é:
- ❌ Violação de segurança
- ❌ Pode danificar o equipamento
- ❌ Risco de acidente grave
- ❌ Não permite diagnóstico antes de energizar

**SEMPRE use o CED no circuito de controle do contator!**

---

## Próximos Passos

Para implementar corretamente:
1. [ ] Identificar os terminais do CED no módulo (consultar pinout)
2. [ ] Verificar se há um contator AC instalado
3. [ ] Traçar o circuito de controle existente
4. [ ] Inserir o CED em série com a bobina do contator
5. [ ] Testar funcionamento: CED deve fechar quando 24V é aplicado

---

## Referências
- Diagrama: `999. Imagens\00032. P031_Conections.png` (Item 11)
- Manual: Rockwell Automation Publication 2198-IN009
- Contexto: `01_Conexoes_Kinetix_5700_2198-P031.md`
