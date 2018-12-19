# Vaga para Estágio - Data Scientist - NLP
## Teste NLP
A tarefa consistia em obter trechos de reviews/comentários que respeitassem dois padrões pré-estabelecidos. O dataset é composto de 1000 frases curtas contento liguagem não muito estruturada. Os padrões são relativos às classes gramaticais das palavras em cada uma dessas frases. O uso de bibliotecas é livre assim como o tipo/modelo de POSTagger a ser usado.

## Organização do projeto
```
.
├── data
│ └── reviews_test_estag_nlp.txt
├── main.py
├── Makefile
├── Readme.md
├── requirements.txt
├── results
│ ├── opinions_with_aubt.txt
│ ├── opinions_with_brill.txt
│ └── opinions_with_spacy.txt
└── taggers
│ ├── mac_morpho_aubt.pickle
│ └── mac_morpho_brill_aubt.pickle
```

| Folder/File | Description |
| ------ | ------ |
| data | Onde o arquivo reviews_test_estag_nlp.txt deve estar |
| results | Local onde os resultados da extração dos padrões ficam armazenados |
| taggers | Pasta onde os modelos de parte dos taggers ficam armazenados |
| main.py | Arquivo com código python para executar toda a tarefa |
| Makefile | Arquivo para instalar o virtualenv para poder executar o código |

Obs: Com a instalação do projeto surgirá mais duas pastas, uma do virtuaenv e outra do nltk-trainer que é umas das "bibliotecas" utilizadas

## Bibliotecas utilizadas
* [NLTK](https://www.nltk.org/)
* [NLTK Trainer](https://nltk-trainer.readthedocs.io/en/latest/)
* [Spacy](https://spacy.io/)

## Instalação
```
$ git clone https://github.com/PauloLemgruberJeunon/ps_birdie.git
$ cd ps_birdie
$ make install
```
Após executar esses comandos, o dataset deve ser baixado e colocado na pasta **data**. Para baixar, acesse esse [link](https://drive.google.com/file/d/1952gkCf2UURsE2qiUwVH700qcmDkXL2D/view?usp=sharing ).

Obs: Dentro do arquivo **Makefile** há mais uma opção. Ela serve para treinar os dois POS taggers que são feitos na **NLTK**. Entretanto, ela não é necessária, pois como o treino deles é demorado e os objetos gerados não são pesados, eu os mantive no repositório e estão prontos para uso.

## Execução
```
$ make run
```
Obs: Esse passo não é necessário para se obter os resultados, uma vez que eles já se encontram na pasta **results**.

## Funcionamento
O programa carrega as reviews do arquivo texto e os modelos dos POS-taggers. Após isso ele roda o algorítimo para extrair os padrões das reviews três vezes, cada uma delas com um tagger diferente. São utilizados 3 POS-taggers diferentes:
* Modelo já feito no Spacy
* Um backoff tagger sequencial, cuja sequência é por affix, unigram, bigram, trigram taggers.
* Um Brill tagger que utiliza um backoff tagger sequencial, cuja a sequência é igual a de cima.

Os dois taggers treinados apresentados acima são treinados com o dataset mac_morpho contido no NLTK. O backoff tagger apresentou uma precisão de teste  de 90%, enquanto o brill apresentou uma precisão de teste de 97%.

No final o resultado aparenta não ser muito afetado pelo uso de diferentes taggers.

## Conclusão
No final os resultados ficaram bons, mas ainda ocorrem alguns erros devido a classificação errônea por parte dos taggers e erros de digitação no dataset. Entretanto o resultado foi relativamente bom para todos os taggers utilizados.

## Reflexões
Pelo que eu interpretei do projeto, o intuito de separar esses patterns seria o de minerar opiniões sobre aspectos dos produtos. Com isso, mesmo vários padrões terem sido obtidos corretamente, alguns deles não servem como opiniões sobre produtos. Em um ambiente com mais informações, poderia-se identificar a qual produto aquele comentário se refere e consultar alguma lista de características desse produto, podendo assim filtrar de maneira muito mais eficiente as opiniões. Outra sugestão seria somente identificar qual a classe do produto no qual a review se baseia e utilizar um modelo bag of words para entender os substantivos que mais aparecem com determinadas classes de produtos. Esse seria um jeito de se obter uma base de características relativas a cada produto (Celular: tela, velocidade, som, câmera etc).
