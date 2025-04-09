# Backup System

Questo repository contiene un sistema completo di creazione backup controllo e recupero dei file. È progettato per eseguire automaticamente backup completi e incrementali, verificare che siano presenti e integri, ed effettuare il ripristino dei dati quando necessario.

## Contenuto

- **Backup automatico**: Crea backup completi (ogni domenica) e incrementali (gli altri giorni), utilizzando `tar` e snapshot.
- **Verifica backup**: Controlla che tutti i backup previsti (dal più recente full a oggi) siano presenti.
- **Ripristino file**: Cerca un file nei backup degli ultimi 31 giorni e lo estrae automaticamente se presente.

## File

- `backup.py`: Script principale per la **creazione dei backup** completi/incrementali.
- `check_backups.py`: Script di **verifica** dei backup mancanti; utile per integrazione con sistemi di monitoraggio come **Nagios**.
- `restore.py`: Script per il **ripristino di un file** a partire da una data, cercando nei backup.

## Setup

### Requisiti

- Python 3.x
- Il comando `tar` deve essere disponibile (presente in tutti i sistemi Linux/Unix)
- Permessi di lettura/scrittura nella directory `/opt/backups`

### Installazione

1. **Clona il repository** nella tua macchina:

```bash
https://github.com/Alheys/Backup.git
```

2. **(Facoltativo)** Imposta `backup.py` come cron job per eseguirlo automaticamente ogni giorno:

```bash
sudo crontab -e
```

E aggiungi ad esempio:

```bash
0 3 * * * /usr/bin/python3 /percorso/assoluto/backup.py
```

3. **(Facoltativo)** Integra `check_backups.py` in sistemi come **Nagios** per monitorare lo stato dei backup.

4. Puoi eseguire `restore.py` manualmente quando serve ripristinare un file:

```bash
python3 restore.py
```

## Personalizzazione

- Puoi modificare i **percorsi delle cartelle** all'interno dei file (`/opt/backups`, ecc.) per adattarli alla tua infrastruttura.
- Puoi cambiare le **cartelle da includere nel backup** all’interno di `backup.py`.

## Esempi d’Uso

- Controllo backup:

```bash
python3 check_backups.py
```

- Creazione backup manuale:

```bash
python3 backup.py
```

- Ripristino di un file:

```bash
python3 restore.py
# Inserisci il percorso del file e la data quando richiesto
```

## Come usare `restore.py`

Lo script `restore.py` permette di ripristinare un file da un backup esistente. Funziona cercando nei backup completi e incrementali a partire da una data fornita e risalendo fino a 31 giorni indietro.

### Esecuzione da terminale

```bash
python3 restore.py
```

### Inserimento dati richiesti

Quando esegui lo script, ti verranno chieste due informazioni:

1. **Percorso del file da ripristinare**  
   Inserisci il percorso del file che vuoi ripristinare, come ad esempio:

   ```
   /etc/hosts
   /home/infobasic/documento.txt
   ```

   Non è necessario togliere la slash iniziale, lo script lo gestisce automaticamente.

2. **Data del backup da cui partire**  
   Inserisci la data nel formato **gg-mm-aaaa**, ad esempio:

   ```
   07-04-2025
   ```

   Lo script cercherà a ritroso fino a 31 giorni indietro per trovare un backup che contenga il file.

### Esempio completo

```bash
$ python3 restore.py
Inserisci il percorso del file da ripristinare: /etc/hosts
Inserisci la data del backup da cui partire (dd-mm-YYYY): 07-04-2025
File etc/hosts ripristinato in /opt/backups/ripristino
```

Il file verrà estratto nella cartella `/opt/backups/ripristino`.
