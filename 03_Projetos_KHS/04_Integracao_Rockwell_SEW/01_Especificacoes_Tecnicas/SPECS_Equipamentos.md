# Integração Rockwell Kinetix 5700 + Motor SEW

> Índice rápido das especificações técnicas

---

## 📁 Arquivos

### Equipamentos

1. **[DC_BUS_2198-P031.md](./DC_BUS_2198-P031.md)** - DC Bus Supply
2. **[SERVO_DRIVE_2198-D012.md](./SERVO_DRIVE_2198-D012.md)** - Servo Drive
3. **[MOTOR_SEW_DT71D4.md](./MOTOR_SEW_DT71D4.md)** - Motor SEW

### Referências

4. **[TABELAS_Especificacoes_Oficiais.md](./TABELAS_Especificacoes_Oficiais.md)** - Specs detalhadas
5. **[MANUAIS_LINKS.md](./MANUAIS_LINKS.md)** - Links e manuais

---

## 🔧 Sistema Completo

```
[Rede AC]        [DC Bus]          [Servo Drive]      [Motor]
195-528V     →   276-747V DC   →   0-480V AC      →   230V (Δ)
3-Phase          2198-P031         2198-D012-ERS3     SEW DT71D4
11.2A            10.5A / 31.6A     5.0A / 12.5A       2.09A
                 7.0kW             1.7kW              0.37kW
```

---

## ✅ Status Atual

| Equipamento | Modelo | Status |
|-------------|--------|--------|
| DC Bus | 2198-P031 | ✅ Validado |
| Servo Drive | 2198-D012-ERS3 | ✅ Identificado |
| Motor | SEW DT71D4 | ✅ Documentado |

---

## ⚠️ Próximo Passo

**CRÍTICO**: Verificar se servo drive **2198-D012** suporta motores de indução

**Como**: Analisar manuais Rockwell (2198-UM002, 2198-AT002)

---

## 📊 Margem de Segurança

| Componente | vs Motor 0.37kW | Margem |
|------------|-----------------|---------|
| DC Bus | 7.0 kW | 18.9x ✅ |
| Servo Drive | 1.7 kW | **4.6x** ✅ |

**Limitante**: Servo Drive (ainda assim excelente)

---

**Última Atualização**: 2026-02-10
