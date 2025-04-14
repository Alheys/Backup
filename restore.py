import os
import datetime
import subprocess  # Serve per eseguire comandi di sistema come "tar"

# Funzione che cerca il primo backup (completo o incrementale) contenente il file richiesto
def trova_backup_con_file(data, cartella_backup, percorso_file):
    data_attuale = datetime.date.today()

    for _ in range(31):  # Controlla fino a 31 giorni indietro
        
        # Costruisce i percorsi per il backup completo e incrementale del giorno attuale
        percorso_full = os.path.join(cartella_backup, "full", f"full-{data_attuale}.tar.gz")
        percorso_incr = os.path.join(cartella_backup, "incr", f"incr-{data_attuale}.tar.gz")
        
        # Controlla prima nel backup completo, poi in quello incrementale
        for file_backup in [percorso_full, percorso_incr]:

            if os.path.exists(file_backup):  # Se il file esiste
                # Controlla se il file specificato è contenuto nell'archivio tar (senza estrarlo)

                result = subprocess.run(["tar", "-tzf", file_backup, percorso_file], capture_output=True)

                if result.returncode == 0:  # Se il file è stato trovato

                    return file_backup  # Ritorna il percorso del file di backup
        
        # Se il file non è stato trovato, si passa al giorno precedente
        data_attuale -= datetime.timedelta(days=1)
    
    return None  # Nessun backup trovato contenente il file

# Funzione che ripristina un file a partire da una data
def ripristina_file(percorso_file, data):

    percorso_file = percorso_file.lstrip("/")  # Rimuove la slash iniziale se presente

    cartella_backup = "/opt/backups"  # Directory dei backup

    cartella_ripristino = os.path.join(cartella_backup, "ripristino")  # Directory dove estrarre il file

    # Crea la cartella di ripristino se non esiste
    os.makedirs(cartella_ripristino, exist_ok=True)
    
    # Cerca un backup che contenga il file richiesto
    file_backup = trova_backup_con_file(data, cartella_backup, percorso_file)
    
    if not file_backup:
        print("Nessun backup trovato contenente il file richiesto.")
        return
    
    try:
        # Estrae il file nella cartella di ripristino
        subprocess.run(["tar", "-xzf", file_backup, "-C", cartella_ripristino, percorso_file], check=True)

        print(f"File {percorso_file} ripristinato in {cartella_ripristino}")

    except subprocess.CalledProcessError:
        print("Errore durante il ripristino.")

# Esecuzione del programma
if __name__ == "__main__":
    # Input dell'utente per il percorso del file e la data da cui partire
    file_da_ripristinare = input("Inserisci il percorso del file da ripristinare: ").lstrip("/")
    
    data_backup = input("Inserisci la data del backup da cui partire (YYYY-mm-dd): ")
    
    # Avvia il processo di ripristino
    ripristina_file(file_da_ripristinare, data_backup)
