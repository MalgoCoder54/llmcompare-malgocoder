# Confronto tra GPT-o3-mini-high e GPT-o1

Questa repository contiene quattro script Python generati utilizzando i modelli GPT-o3-mini-high e GPT-o1, ciascuno applicato a due prompt distinti. L'obiettivo è analizzare e confrontare le differenze nei codici prodotti dai due modelli in risposta agli stessi input.

## Struttura della Repository

La repository è organizzata come segue:

```
├── prompt1_gpt_o3_mini_high.py
├── prompt1_gpto1.py
├── prompt2_gpt_o3_mini_high.py
└── prompt2_gpto1.py
```

- **prompt1_gpt_o3_mini_high.py**: Script generato dal modello GPT3o-mini-high in risposta al primo prompt.
- **prompt1_gpto1.py**: Script generato dal modello GPTo1 in risposta al primo prompt.
- **prompt2_gpt_o3_mini_high.py**: Script generato dal modello GPT3o-mini-high in risposta al secondo prompt.
- **prompt2_gpto1.py**: Script generato dal modello GPTo1 in risposta al secondo prompt.

## Prompt Utilizzati

Di seguito sono riportati i prompt utilizzati per generare gli script:

**Prompt 1:**

```
Ciao! Voglio creare una simulazione realistica del tiro di una freccia con Python. Voglio una interfaccia grafica che con i pulsanti (frecce) mi permette di regolare sia l'inclinazione sia l'angolo di lancio. Considera gravità e attrito dell'aria, più le perdite sull'arco e sulla elasticità della freccia. Voglio che mi disegni sia l'arco "teorico" senza attrito e considerandola un punto materiale, sia l'animazione della freccia reale
```

**Prompt 2:**

```
Ottimo punto di partenza, ora vorrei che ogni volta che cambio un parametro, una linea tratteggiata mostri la posizione iniziale e la traiettoria teorica. Vorrei anche che la velocità iniziale potesse essere parametrizzata, e che i parametri siano sulla sinistra dell'interfaccia.
```

## Esecuzione degli Script

Per eseguire gli script, assicurati di avere Python installato sul tuo sistema. Puoi eseguire ciascuno script utilizzando il seguente comando:

```bash
pip install requirements.txt
python nome_script.py
```

Sostituisci `nome_script.py` con il nome del file che desideri eseguire.

## Contributi

I contributi a questa repository sono benvenuti. Se desideri aggiungere miglioramenti o ulteriori analisi, sentiti libero di aprire una pull request o di contattarmi direttamente.

## Licenza

Questa repository è distribuita sotto la licenza GNU v3.0. Per maggiori dettagli, consulta il file [LICENSE](LICENSE).

