#!/usr/bin/python3

import os
import datetime
import sys
import calendar

# Stati Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

def controlla_backup():
    backup_dir = "/opt/backups"
    oggi = datetime.date.today()

    # Trova data ultimo backup completo
    full_backups = []
    for f in os.listdir(f"{backup_dir}/full"):
        if f.startswith("full-") and f.endswith(".tar.gz"):
            try:
                data = datetime.datetime.strptime(f[5:-7], "%d-%m-%Y").date()
                full_backups.append(data)
            except:
                continue

    if not full_backups:
        return CRITICAL, "Nessun backup completo trovato"

    ultimo_full = max(full_backups)
    
    # Verifica backup mancanti solo per date esistenti
    mancanti = []
    data_corrente = ultimo_full + datetime.timedelta(days=1)
    
    while data_corrente <= oggi:
        # Verifica se la data corrente esiste nel mese/anno
        _, giorni_nel_mese = calendar.monthrange(data_corrente.year, data_corrente.month)
        if data_corrente.day <= giorni_nel_mese:
            if data_corrente.weekday() == 6:  # Domenica
                path = f"{backup_dir}/full/full-{data_corrente.strftime('%d-%m-%Y')}.tar.gz"
                tipo = "completo"
            else:
                path = f"{backup_dir}/incr/incr-{data_corrente.strftime('%d-%m-%Y')}.tar.gz"
                tipo = "incrementale"

            if not os.path.exists(path):
                mancanti.append(f"{tipo} del {data_corrente.strftime('%d-%m-%Y')}")
        
        data_corrente += datetime.timedelta(days=1)

    if not mancanti:
        return OK, f"Tutti i backup OK dal {ultimo_full.strftime('%d-%m-%Y')}"

    msg = "Backup mancanti:\n" + "\n".join(mancanti)

    if len(mancanti) == 1:
        return WARNING, msg
    else:
        return CRITICAL, msg

try:
    stato, msg = controlla_backup()
    print(msg)
    sys.exit(stato)
except Exception as e:
    print(f"Errore: {e}")
    sys.exit(UNKNOWN)
