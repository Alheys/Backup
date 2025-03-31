import os
import datetime
import subprocess  # Per eseguire il comando "tar"

def trova_backup_con_file(data, cartella_backup, percorso_file):   #Trova il primo backup disponibile che contiene il file richiesto, partendo dalla data fornita e andando a ritroso fino a 31 giorni
    data_attuale = datetime.datetime.strptime(data, "%d-%m-%Y")  # Converte la stringa in oggetto data
    for _ in range(31):  # Controlla fino a 31 giorni indietro
        formato_data = data_attuale.strftime("%d-%m-%Y")  # Formatta la data in gg-mm-aaaa
        
        # Percorsi dei file di backup per il giorno attuale
        percorso_full = os.path.join(cartella_backup, "full", f"full-{formato_data}.tar.gz")
        percorso_incr = os.path.join(cartella_backup, "incr", f"incr-{formato_data}.tar.gz")
        
        # Controlla prima nel full, poi nell'incrementale
        for file_backup in [percorso_full, percorso_incr]:
            if os.path.exists(file_backup):  # Se il file di backup esiste
                # Controlla se il file è presente nell'archivio senza estrarlo
                result = subprocess.run(["tar", "-tzf", file_backup, percorso_file], capture_output=True)
                if result.returncode == 0:  # Se il file è stato trovato
                    return file_backup  # Restituisce il percorso del file di backup
        
        # Se il file non è stato trovato, passa al giorno precedente
        data_attuale -= datetime.timedelta(days=1)
    
    return None  #il file non è stato trovato in nessun backup

def ripristina_file(percorso_file, data): #Ripristina un file da un backup tar cercando nei backup
    
    percorso_file = percorso_file.lstrip("/")  # Rimuove la / iniziale se presente
    cartella_backup = "/opt/backups"
    cartella_ripristino = os.path.join(cartella_backup, "ripristino")
    
    # Crea la cartella di ripristino se non esiste
    os.makedirs(cartella_ripristino, exist_ok=True)
    
    # Cerca un backup che contenga il file richiesto
    file_backup = trova_backup_con_file(data, cartella_backup, percorso_file)
    
    if not file_backup:
        print("Nessun backup trovato contenente il file richiesto.")
        return
    
    try:
        # Estrai il file nella cartella di ripristino
        subprocess.run(["tar", "-xzf", file_backup, "-C", cartella_ripristino, percorso_file], check=True)
        print(f"File {percorso_file} ripristinato in {cartella_ripristino}")
    except subprocess.CalledProcessError:
        print("Errore durante il ripristino.")

if __name__ == "__main__":
    # Input dell'utente per il file da ripristinare e la data del backup
    file_da_ripristinare = input("Inserisci il percorso del file da ripristinare: ").lstrip("/")
    data_backup = input("Inserisci la data del backup da cui partire (dd-mm-YYYY): ")
    
    # Avvia il processo di ripristino
    ripristina_file(file_da_ripristinare, data_backup)
