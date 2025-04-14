import os
import datetime
import subprocess  # Serve per eseguire comandi come "tar"

def elimina_backup_vecchi(cartella_backup, giorni=31):
    
    oggi = datetime.date.today()    
    limite_data = oggi - datetime.timedelta(days=giorni)

    # Scansiona ricorsivamente la cartella
    for cartella_corrente, _, files in os.walk(cartella_backup):
        for f in files:
            percorso_file = os.path.join(cartella_corrente, f)
            try:
                # Ottiene la data dell'ultima modifica 
                timestamp_modifica = os.path.getmtime(percorso_file)

                data_modifica = datetime.date.fromtimestamp(timestamp_modifica) #conversione del formato in data y-m-d

                # Elimina il file se è più vecchio della data limite
                if data_modifica < limite_data:
                    os.remove(percorso_file)
            except FileNotFoundError:
                pass  # Il file potrebbe essere stato già eliminato


# Funzione principale che crea il backup
def crea_backup():
    # Cartelle da includere nel backup
    cartelle = [
        "/etc",
        "/home/infobasic",
        "/usr/local/nagios",
        "/usr/share/munin",
        "/var/www"
    ]
    
    # Definizione delle cartelle per i backup completi e incrementali
    backup_dir = "/opt/backups"
    full_dir = os.path.join(backup_dir, "full")
    incr_dir = os.path.join(backup_dir, "incr")
    snapshot = os.path.join(incr_dir, "snapshot.snar")


    
    # Elimina i backup più vecchi di 31 giorni
    elimina_backup_vecchi(full_dir)
    elimina_backup_vecchi(incr_dir)
    
    # Crea le directory di backup se non esistono
    os.makedirs(full_dir, exist_ok=True)
    os.makedirs(incr_dir, exist_ok=True)
    
    # Ottiene la data odierna nel formato aaaa-mm-gg
    giorno_attuale = datetime.date.today()

    # Se oggi è domenica, si fa un backup completo
    if giorno_attuale.weekday() == 6:

        backup_file = os.path.join(full_dir, f"full-{giorno_attuale}.tar.gz")
        comando_tar = ["tar", "-czpf", backup_file] + cartelle
    else:
        # Altrimenti si fa un backup incrementale

        backup_file = os.path.join(incr_dir, f"incr-{giorno_attuale}.tar.gz")

        #creazione file snapshot
        open(snapshot, "a").close()

        comando_tar = ["tar", "-czpf", backup_file, "--listed-incremental=" + snapshot] + cartelle

    
    # Esegue il comando di backup
    try:
        subprocess.run(comando_tar, check=True)
    except subprocess.CalledProcessError:
        pass  # Se c'è errore durante il backup, non viene sollevata eccezione


# Esecuzione del backup se lo script è lanciato direttamente
if __name__ == "__main__":
    crea_backup()
