#Backup e Ripristino

Questo progetto include due script Python per la gestione dei backup e del ripristino di file.

- **`backup.py`**: Esegue il backup automatico di specifiche cartelle, con backup completi settimanali e incrementali giornalieri.
- **`restore.py`**: Permette di ripristinare un singolo file o un'intera cartella a partire da un backup esistente.

##Installazione e Configurazione

###Installare Python
Assicurati di avere Python installato sul sistema per eseguire gli script.

###Rendere eseguibili gli script

sudo chmod +x backup.py
sudo chmod +x restore.py


###Automazione con `cron`
Per eseguire automaticamente il backup, modifica il crontab:

sudo crontab -e

Scegli l'orario e i giorni in cui eseguire lo script.
Esempio: per eseguirlo ogni giorno alle 02:30 di notte, aggiungi questa riga:

30 2 * * * /usr/bin/python /percorso/del/file/backup.py

(Sostituisci `/percorso/del/file/` con il percorso effettivo del file `backup.py`.)

##Uso Manuale

###Eseguire manualmente il backup

sudo python /percorso/del/file/backup.py

Se vuoi modificare le cartelle da includere nei backup, modifica la variabile `cartelle` nel file `backup.py`:

cartelle = ["/percorso/cartella/", "/percorso/cartella/" etc...]


###Ripristinare un file o una cartella

sudo python /percorso/del/file/restore.py

Il programma:
1. Chiederà il **percorso del file o della cartella** da ripristinare.
2. Chiederà la **data del backup** da cui partire per la ricerca.
   - Se il file non è presente nella data selezionata, il programma cercherà nei backup precedenti.
3. Il file o la cartella verranno ripristinati in `/backup/ripristino/`.





