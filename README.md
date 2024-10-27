
# CSV Splitter

Uma ferramenta para dividir arquivos CSV em múltiplos arquivos com base na quantidade de registros especificada, mantendo a integridade dos dados e permitindo configurações de charset, separador e formatação. Ideal para lidar com grandes arquivos CSV que precisam ser fragmentados para melhor manuseio e processamento.

## Funcionalidades

- **Divisão de CSV**: Divide o arquivo original em múltiplos arquivos CSV, com o número de registros por arquivo definido pelo usuário.
- **Detecção Automática de Charset e Separador**: O charset e o separador do arquivo de origem podem ser detectados automaticamente ou especificados manualmente.
- **Configuração de Destino Personalizável**: Permite definir charset e separador de destino.
- **Formatação de Dados**: Formatação opcional para os padrões BR, EUA, EU e UK, com exemplos para ajudar na escolha do formato desejado.
- **Interface Gráfica Intuitiva**: Interface com `Tkinter`, incluindo barra de progresso e log do processo em tempo real.

## Tecnologias

- Python 3
- Tkinter
- Pandas
- Chardet (para detecção de charset)

## Pré-requisitos

- Python 3.x instalado
- Bibliotecas adicionais (instaláveis via `pip`):
  ```bash
  pip install pandas chardet
  ```

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/GuilhermeP96/csv-splitter.git
   cd csv-splitter
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o script:
   ```bash
   python csv_splitter.py
   ```

2. Na interface gráfica:
   - **Selecione o arquivo CSV**: Escolha o arquivo que deseja dividir.
   - **Configurações de Origem**:
     - `Charset de Origem`: Detectado automaticamente por padrão, ou selecione manualmente.
     - `Separador de Origem`: Detectado automaticamente por padrão, ou escolha entre `;`, `,`, `\t`, `|` ou insira um personalizado.
   - **Número de Registros por CSV**: Defina a quantidade de registros para cada arquivo dividido.
   - **Formato de Dados**:
     - Escolha entre `Manter Original` (para preservar os dados como strings) ou formate-os para padrões BR, EUA, EU, ou UK.
     - Configure o `Formato de Origem` (detectado automaticamente ou manual).
   - **Configurações de Destino**:
     - `Charset de Destino`: Escolha o charset do arquivo de saída.
     - `Separador de Destino`: Escolha o separador do arquivo de saída ou insira um personalizado.
   - **Dividir CSV**: Clique para iniciar o processo de divisão. Uma barra de progresso e log do processo são exibidos em tempo real.

## Exemplo

- Arquivo de origem: `dados_grandes.csv`
- Configuração de destino:
  - Charset: `utf-8`
  - Separador: `,`
  - Número de registros por arquivo: `1000`
- Arquivos resultantes:
  - `dados_grandes_1.csv`, `dados_grandes_2.csv`, ..., contendo até 1000 registros cada.

## Notas

- O charset e separador de origem são detectados automaticamente, mas podem ser ajustados manualmente para casos específicos.
- Ao selecionar `Personalizar` no separador, um campo de entrada será exibido para inserir o separador desejado.
- A formatação dos dados é opcional e pode ser útil para garantir a consistência regional dos formatos de data e número.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para bugs e sugestões.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
