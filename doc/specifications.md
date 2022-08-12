# Controles (Widgets) da Página SCADA

&emsp;A página **SCADA** é destinada a criação e utilização de elementos de uma interface de usuário SCADA¹.<br>

&emsp;Para ilustrar considere o caso de uso em que tem-se um sistema de controle de velocidade de um motor CC². As 3 principais variáveis seriam:
- Tensão: A tensão aplicada nos terminais do motor ao longo do tempo. Ao longo do tempo isso geraria um conjunto de dados conhecido como série temporal - que consistiria em um valor de ponto flutuante a cada certo intervalo de tempo, suponha 10sps (10 amostras por segundo);
- Corrente: A corrente elétrica circulando no circuito de armadura do motor - assim como a Tensão, geraria uma série temporal com uma taxa de amostragem;
- Velocidade: A velocidade de rotação do eixo do motor, por exemplo 500rpm (500 revoluções por minuto) - que também geraria uma série temporal com uma taxa de amostragem;<br>

&emsp;Um sistema de controle implementado na prática possuiria também muitas outras variáveis que gerariam séries temporais muito relevantes.<br>

&emsp;Estes foram exemplos de series temporais que podem vir do Arduino para o ASCADA, mas também podemos ter séries temporais indo do ASCADA para o Arduino, por exemplo a velocidade do motor desejada ao longo do tempo.<br>

&emsp;Além de variáveis que geram séries temporais também pode-se ter variáveis que representam o estado de algo, chamaremos esse tipo de variável de Flag. Por exemplo suponha a situação em a velocidade do motor é 0, isso poderia acontecer no caso em que o sistema de controle não está atuando ou quanto ele esteja atuando para manter a velocidade igual a zero, no primeiro caso o eixo do motor estaria livre, no segundo, se um torque externo fosse aplicado ao eixo o sistema de controle tentaria se opor, tentando manter a velocidade em zero. Neste caso seria muito útil que houvesse uma variável indicando se o sistema de controle está atuando ou não.<br>

&emsp;Outro exemplo de Flag seria a posição do motor, por exemplo, "desde que o sistema iniciou o eixo do motor deu 73,5 revoluções", perceba que a posição Também pode gerar uma série temporal, mas muitas vezes a posição ao longo do tempo não é importante somente a posição atual. Este é o exemplo de uma Flag que seria atualizada frequentemente.<br>

&emsp;Flag são muito comuns em sistemas SCADA, podem representar também alertas, como sobrecarga do motor, velocidade atual próximo ao limite máximo, indicação de algum erro, ou estado de alguma variável interna do sistema de controle. E além de Flags que fornecem informações sobre o estado do sistema pode-se ter também Flags que são enviada do ASCADA para o Arduino, indicando um estado desejado.<br>

&emsp;Esses são exemplos para um simples sistema de controle de velocidade de um motor, se imaginarmos um sistema com vários atuadores e sensores, podemos ter muito mais possibilidades de Flags.<br>

&emsp;Dada a necessidade de recepção de envio de valores para variáveis como essas é necessária a implementação de elementos de visualização e manipulação dessas variáveis na página **SCADA**, conforme especificação a seguir.<br>

## Especificação

### Organização, Referência (código hex) e Tipos de Dados

- Variável: Aqui, entende-se por variável a entidade que representa um dado ou conjunto de dados específicos. As variáveis podem ser do tipo (tipo de variável) **Flag**, **Serie** ou **TimeSerie** e os dados representados pelas variáveis também tem seus tipos (tipo de dado da variável), estes são alguns dos tipos primitivos de linguagens baixo ou médio nível como C/C++ (bool, int, float, etc.);
- Flag: Variáveis que representam o estado de alguma grandeza física, ou abstrata do sistema, ex.: Led 1 ligado ou desligado (dado bool), Valor de temperatura (dado float), quantidade de vezes que o motor chegou a velocidade igual a zero (dado int), corrente máxima permitida (dado float), etc. Nesse tipo de variável o histórico de valores não importa, somente o último valor;
- Serie: O histórico importa, por exemplo suponha que deseja-se saber quais os valores que uma grandeza assumiu, ou a sequência de estados que um dado do sistema assumiu. Neste tipo de variável o tempo não importa mas a sequência sim. Pode-se pensar nesse tipo de variável como um vetor ou lista unidimensional, onde os dados vão chegando ou saindo do ASCADA, aumentando o número de elementos na lista ou vetor a medida que o tempo passa;
- TimeSerie: Por exemplo o valor da corrente ao longo do tempo.  Pode-se pensar nesse tipo de variável como um vetor ou lista bidimensional, representando pares ordenados, designados aqui como **Abscissa** e **Ordenada**. Embora seja mais intuitivo pensar nesse tipo de variável como sempre representando valores de tempo e amplitude nem sempre este será o caso, mas qualquer sinal bidimensional, onde os dados vão chegando ou saindo do ASCADA, aumentando o número de elementos na lista ou vetor a medida que o tempo passa;

&emsp;Cada variável é identificada por um código hexadecimal de 8 bits. As variáveis são cadastradas no ASCADA atribuindo para cada variável os seguintes descritores:
- Código de identificação único (obrigatório): hexadecimal de 1 byte
- Nome (opcional): string de até 20 caracteres (futuramente deverá suportar caracteres matemáticos especiais e índices com sintaxe Latex);
- Tipo de variável (obrigatório): Flag, Serie ou TimeSerie;
- Tipo de dado (obrigatório): bool, char, int8, int16, int32, int64, float32 ou float64. No caso de variáveis TimeSerie precisa ser especificado o tipo do dado da Abscissa e o tipo da Ordenada;
- Descrição (opcional): string de até 255 caracteres.

### Widgets

&emsp;A página SCADA deve:
- Ter a funcionalidade de adicionar, remover e organizar Widgets de forma dinâmica;
- Adicionar, remover e organizar widgets do tipo: TsChart, envio de valores de Flags dos tipos de dado suportados (criar widgets)
- Visualização de valores de Flags recebidos dos tipos de dado suportados (criar widgets).
- Os Widgets para envio e recepção de Flag devem exibir seu tipo de dado e identificação (hexadecimal) e possuir validadores de valores (evitando que o usuário possa envia um caractere não numérico, por exemplo, em uma Flag com tipo de dado diferente de char).

### Implementação

&emsp;A classe estática `DataGateway` implementa uma interface de comunicação de alto nível (como uma API) entre o Arduino e o ASCADA. Em qualquer parte do código pode-se importar a classe DataGateway (`from app import DataGateway`) e:<br>
- Para widgets de envio de Flag: o widget deve emitir um sinal com o valor inserido pelo usuário ao slot (método estático) correspondente da classe `DataGateway` de acordo com o tipo de dado. (ver docstrings na implementação dos slots).<br>
- Para widgets de recepção de Flag: quando um novo widget é adicionado chamar o método `addFlagWidget` da classe `DataGateway`, e quando o widget for removido, chamar o método `rmFlagWidget` (ves docstrings na implementação dos métodos para saber quais os parâmetros passados na chamada)
- Para TsChart: Adicione widgets TsCharts chamando o método `DataGateway.get_new_chart()`. Esse método cria o widget e conecta todas as variáveis do tipo Serie e TimeSerie cadastrados para que possam ser visualizados em tempo real. Se for utilizar um TsChart fora de uma `ChartWindow` implemente algo semelhante ao método `ChartWindow.add_widget` para desconecta o TsChart das variáveis quando o TsChart for removido. Tome como exemplo a utilização de `TsChart` em `UI_application_page_3`.


---
_[¹SCADA](https://www.hitecnologia.com.br/o-que-e-um-sistema-scada/#:~:text=SCADA%20%C3%A9%20a%20sigla%20em,os%20dispositivos%20de%20um%20processo.): SCADA é a sigla em inglês para Supervisory Control And Data Acquisition que na tradução para o português significa Sistema de Supervisão e Aquisição de Dados. O SCADA é um sistema que usa um software para monitorar, supervisionar e controlar as variáveis e os dispositivos de um processo._<br>
_²CC: Motor de corrente contínua._<br>