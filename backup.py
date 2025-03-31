import os
import datetime
import subprocess  # Permette di eseguire comandi di sistema come "tar"

def elimina_backup_vecchi(backup_dir, giorni=31):  #Elimina i file di backup più vecchi di 31 di giorni


    limite = datetime.datetime.now() - datetime.timedelta(days=giorni)  # Data limite oltre cui i file verranno eliminati
    
    # Scansiona tutti i file presenti nella cartella di backup
    for cartella, _, files in os.walk(backup_dir):
        for file in files:
            file_path = os.path.join(cartella, file)  # Percorso completo del file
            try:
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))  # Data ultima modifica del file
                if file_mtime < limite:  # Se il file è più vecchio del limite viene eliminato
                    os.remove(file_path)  
            except FileNotFoundError:  
                pass  # Se il file è già stato eliminato, l'errore viene ignorato

def crea_backup():

    # Cartelle da includere nel backup
    cartelle = [
        "/etc",
        "/home/infobasic",
        "/usr/local/nagios",
        "/usr/share/munin",
        "/var/www"
    ]
    
    # Percorsi delle cartelle di backup
    backup_dir = "/opt/backups"
    full_dir = os.path.join(backup_dir, "full")
    incr_dir = os.path.join(backup_dir, "incr")

    # File snapshot per i backup incrementali e full
    full_snapshot = os.path.join(full_dir, "snapshot.snar")
    incr_snapshot = os.path.join(incr_dir, "snapshot.snar")
    
    # Eliminazione backup più vecchi di 31 giorni
    elimina_backup_vecchi(full_dir)
    elimina_backup_vecchi(incr_dir)
    
    # Creazione delle cartelle di backup se non esistono
    os.makedirs(full_dir, exist_ok=True)
    os.makedirs(incr_dir, exist_ok=True)
    
    # Data attuale formattata come "gg-mm-aaaa"
    giorno_attuale = datetime.date.today()
    formato_giorno = giorno_attuale.strftime("%d-%m-%Y")
    
    # Se oggi è domenica viene creato un backup full
    if giorno_attuale.weekday() == 6:
        backup_file = os.path.join(full_dir, f"full-{formato_giorno}.tar.gz")
        tar_command = ["tar", "-czpf", backup_file, "--listed-incremental=" + full_snapshot] + cartelle
        
        # Se esiste già un file snapshot full, viene rimosso per forzare un nuovo backup completo
        if os.path.exists(full_snapshot):
            os.remove(full_snapshot)
    else:
        #creazione backup incrementale
        backup_file = os.path.join(incr_dir, f"incr-{formato_giorno}.tar.gz")
        tar_command = ["tar", "-czpf", backup_file, "--listed-incremental=" + incr_snapshot] + cartelle

        # Se il file snapshot incrementale non esiste, crealo
        open(incr_snapshot, "a").close()
    
    # creazione backup usando tar
    try:
        subprocess.run(tar_command, check=True)
    except subprocess.CalledProcessError:
        pass

if __name__ == "__main__":
    crea_backup()
