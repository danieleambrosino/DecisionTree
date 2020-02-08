# Decision Tree con rule post-pruning

L'intero codice è stato prodotto in autonomia, ad eccezione del metodo `Node.display()` utilizzato solo in fase di sviluppo, che è ispirato al metodo `DecisionFork.display()` del repository [aima-python](https://github.com/aimacode/aima-python/blob/master/learning.py).

Si è reso necessario eseguire il commit anche dei dataset, in quanto sono stati modificati rispetto al dataset originale (sono state eliminate le righe con attributi mancanti e sono stati redistribuiti gli esempi).

Per avviare il progetto, eseguire il file `run.py`. Il progetto è stato testato utilizzando la versione  3.7.6 dell'interprete Python.
L'unica dipendenza esterna alla standard library è la libreria `matplotlib` utilizzata per generare il grafico dell'accuracy.


Il file `config.py` consente di gestire alcuni parametri di configurazione del progetto:
- la variabile Booleana `reduce_split_points` (impostata di default a `False`)  permette di **ridurre il numero di split point** generati ad ogni valutazione degli attributi numerici, per velocizzare il processo di generazione dell'albero quando si utilizzano training set di dimensioni considerevoli. La variabile `split_point_threshold` consente quindi di scegliere la **soglia massima** di split point da generare;
- le variabili `training_set_file_path`, `validation_set_file_path` e `test_set_file_path` consentono di specificare i file da cui prelevare gli esempi per i dataset;
- le variabili `goal` e `attributes` sono specifiche del dataset scelto e contengono le informazioni sugli attributi dei dataset e sull'attributo scelto come goal.