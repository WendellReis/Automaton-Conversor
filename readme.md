## Overview
**Criado por: Wendell Reis Milani Matias**

Este projeto conciste na implementação de um algortimo que reconhece, avalia, testa e minizava um automato finito. É motivado pela disciplina de Linguagens Formais e Autômatos (LFA) ofertada pelo CEFET-MG Campus Leopoldina.

## Guia de Uso
A execução do programa depende da passagem do nome de um arquivo em formato .json que deverá conter todas as informações de um autômato finito: 

- **alfabeto**: vetor contendo os caracteres aceitos pela linguagem considerando **'&'** como caracter vazio.
- **estados: vetor** contendo o nome dos estados
- **estado_inicial**: nome do estado inicial
- **estados_finais**: vetor contendo os estados finais
- **transicoes**: vetor de tuplas onde cada elemento representa uma transição do tipo **(QI,c,QF)**, quer dizer uma transição de **QI** para **QF** processando um caracter **c** do alfabeto do autômato.
- **palavras**: vetor contendo um conjunto de palavras que serão testadas pelo autômato. Esse conjunto pode ser vazio e a palavra vazia pode ser representada pelo caracter vazio.

O presente repositório possui arquivos .json que exemplificam a forma correta que um autômato deve ser descrito. É possível executar um teste com:

```
python3 main.py afd.json
```

*O correto funcionamento do programa está condicionada a correta descrição do autômato através do arquivo de entrada .json. Além disso, o autômato descrito não deve conter ciclos que podem ser percorridos com caracter vazio ('&').*