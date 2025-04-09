# Backup System

Questo repository contiene un sistema completo di **gestione backup**, **verifica dell’integrità** e **ripristino dei file**, realizzato in Python. È progettato per eseguire automaticamente backup completi e incrementali, verificare che siano presenti e integri, ed effettuare il ripristino dei dati quando necessario.

## 📁 Contenuto

- **Backup automatico**: Crea backup completi (ogni domenica) e incrementali (gli altri giorni), utilizzando `tar` e snapshot.
- **Verifica backup**: Controlla che tutti i backup previsti (dal più recente full a oggi) siano presenti.
- **Ripristino file**: Cerca un file nei backup degli ultimi 31 giorni e lo estrae automaticamente se presente.

## 📄 File

- `backup.py`: Script principale per la **creazione dei backup** completi/incrementali.
- `check_backups.py`: Script di **verifica** dei backup mancanti; utile per integrazione con sistemi di monitoraggio come **Nagios**.
- `restore.py`: Script per il **ripristino di un file** a partire da una data, cercando nei backup.
- `full/` e `incr/`: Cartelle dove vengono salvati i backup (`/opt/backups/full` e `/opt/backups/incr`).
- `ripristino/`: Cartella dove vengono estratti i file ripristinati.

## ⚙️ Setup

### Requisiti

- Python 3.x
- Il comando `tar` deve essere disponibile (presente in tutti i sistemi Linux/Unix)
- Permessi di lettura/scrittura nella directory `/opt/backups`

### Installazione

1. **Clona il repository** nella tua macchina:

```bash
git clone https://github.com/tuo-utente/Backup-System.git
```

2. **(Facoltativo)** Imposta `backup.py` come cron job per eseguirlo automaticamente ogni giorno:

```bash
crontab -e
```

E aggiungi ad esempio:

```bash
0 3 * * * /usr/bin/python3 /percorso/assoluto/backup.py
```

3. **(Facoltativo)** Integra `check_backups.py` in sistemi come **Nagios** o **Zabbix** per monitorare lo stato dei backup.

4. Puoi eseguire `restore.py` manualmente quando serve ripristinare un file:

```bash
python3 restore.py
```

## 🛠️ Personalizzazione

- Puoi modificare i **percorsi delle cartelle** all'interno dei file (`/opt/backups`, ecc.) per adattarli alla tua infrastruttura.
- Puoi cambiare le **cartelle da includere nel backup** all’interno di `backup.py`.

## ✅ Esempi d’Uso

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
