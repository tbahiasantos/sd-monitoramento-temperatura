### ✅ Instruções para executar:

1. **Instale as dependências**:

   ```bash
   pip install flask pandas
   ```

2. **Inicie o servidor principal**:

   ```bash
   cd servidor
   python servidor_main.py
   ```

3. **Inicie a interface web (em outro terminal)**:

   ```bash
   python servidor_web.py
   ```

4. **Execute o cliente sensor**:

   ```bash
   cd cliente
   python cliente_sensor.py
   ```

5. **Acesse a interface no navegador**:

   ```
   http://localhost:8000
   ```

6. **Aumentar o número de sensores**:

```bash
python cliente_sensor.py sensor_002
python cliente_sensor.py sensor_003
python cliente_sensor.py sensor_004
```

7. **Verificação**:

- As leituras de todos os sensores aparecerão no arquivo `registro_temperaturas.csv`
- A interface web listará os dados de todos eles
- Temperaturas acima de 38.0°C aparecerão na tabela de alertas
