# Análise de Viabilidade: Monitoramento de Sinais pelo Pulso (Hobista)

## 1. Introdução
Esta análise explora a viabilidade de um hobista, com orçamento limitado, captar e analisar sinais provenientes do pulso humano. Existem duas abordagens principais: a óptica (PPG) e a elétrica (ECG).

## 2. Tecnologias Disponíveis (Baixo Custo)

### A. Fotopletismografia (PPG) - Óptico
Utiliza LEDs e fotodetectores para medir a variação do volume sanguíneo. É o método usado em smartwatches.
*   **Sensor Principal:** MAX30102 ou MAX30105.
*   **Custo Estimado:** R$ 20,00 - R$ 40,00.
*   **Dificuldade:** Baixa. A biblioteca para Arduino/ESP32 é madura.
*   **O que mede:** Frequência cardíaca e saturação de oxigênio (SpO2). Não mede a atividade elétrica real do coração.

### B. Eletrocardiografia (ECG) - Elétrico
Mede os potenciais elétricos gerados pela despolarização do músculo cardíaco.
*   **Sensor Principal:** Módulo AD8232.
*   **Custo Estimado:** R$ 35,00 - R$ 60,00 (incluindo eletrodos).
*   **Dificuldade:** Média. Exige posicionamento correto dos eletrodos e filtragem de ruído (60Hz da rede elétrica).
*   **O que mede:** O complexo QRS, permitindo ver a "forma" do batimento cardíaco.

## 3. Hardware Necessário
Para ambos os casos, o hobista precisará de:
1.  **Microcontrolador:** 
    *   Arduino Nano (Barato, mas limitado) ou 
    *   ESP32 (Recomendado: Wi-Fi/Bluetooth integrados, maior processamento por ~R$ 35,00).
2.  **Cabos e Protoboard:** R$ 20,00.
3.  **Fonte de Alimentação:** Bateria LiPo ou PowerBank (O uso de USB conectado diretamente ao PC pode introduzir muito ruído).

## 4. Detecção de Toque e Interação
Existem três formas de validar um "toque" ou presença no pulso:
1.  **Proximidade PPG (MAX30102):** Este sensor possui um modo de interrupção que detecta quando um objeto (o pulso) se aproxima ou encosta no sensor, permitindo "acordar" o sistema.
2.  **Capacitive Touch (ESP32):** O ESP32 possui 10 pinos internos de toque capacitivo. É possível usar uma pequena superfície metálica ou o próprio fio para detectar o toque do dedo ou do pulso sem sensores extras.
3. Ruído de ECG:** Embora o AD8232 detecte quando os eletrodos são desconectados ("Leads Off"), ele não é ideal para interação, pois o toque gera apenas ruído errático no sinal.

## 5. Detecção de Gestos (Dedo tocando Dedo)
Para detectar especificamente se o usuário encostou um dedo no outro (gestos de pinça), os sensores cardíacos (PPG/ECG) **não funcionam**. Você precisará monitorar a atividade muscular ou vibração mecânica.

### Soluções Possíveis (Do mais fácil ao mais difícil):
1.  **IMU (Acelerômetro/Giroscópio - MPU6050):**
    *   **Como funciona:** Detecta a vibração sutil do tendão ("tendon snap") quando os dedos se tocam firmemente.
    *   **Custo:** ~R$ 15,00.
    *   **Desafio:** Requer lógica inteligente ou Machine Learning (TinyML no ESP32) para diferenciar um "toque de dedo" de um balançar de braço.

2.  **EMG (Eletromiografia - Sensor Muscular):**
    *   **Como funciona:** Mede os disparos elétricos dos músculos do antebraço que controlam os dedos. Ao fechar a mão ou tocar o polegar, o sinal elétrico no pulso muda drasticamente.
    *   **Sensor:** Módulo EMG genérico (clone do MyoWare).
    *   **Custo:** ~R$ 80,00 - R$ 120,00.
    *   **Veredito:** É a tecnologia usada em pulseiras de controle por gestos.

## 6. Análise de Viabilidade Econômica
*   **Kit Mínimo (PPG):** ~R$ 70,00.
*   **Kit Mínimo (ECG):** ~R$ 90,00.
*   **Conclusão:** É extremamente viável para um hobista. O investimento total fica abaixo de R$ 150,00 para um protótipo funcional.

## 5. Desafios e Riscos
1.  **Ruído Elétrico:** O corpo humano atua como uma antena. Captar sinais de microvolts no pulso exige bons algoritmos de filtragem (filtros passa-baixa e notch).
2.  **Segurança:** **NUNCA** conectar eletrodos ao corpo enquanto o circuito estiver ligado à tomada (rede elétrica) sem isolamento galvânico. Recomenda-se o uso exclusivo de baterias durante os testes.
3.  **Precisão:** Sensores de baixo custo não substituem equipamentos médicos. São para fins educacionais e de biofeedback.

## 6. Próximos Passos Sugeridos
1.  Aquisição de um módulo ESP32 e um AD8232.
2.  Estudo de processamento digital de sinais (DSP) básico para limpeza do sinal.
3.  Uso do Serial Plotter do Arduino para visualização em tempo real.
