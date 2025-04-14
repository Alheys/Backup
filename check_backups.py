#!/usr/bin/python3

import os
import datetime
import sys

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

def controlla_backup():
    backup_dir = "/opt/backups"
    oggi = datetime.date.today()

    full_backups = []
    for f in os.listdir(f"{backup_dir}/full"):
        if f.startswith("full-") and f.endswith(".tar.gz"):
            try:
                data = datetime.datetime.strptime(f[5:-7], "%Y-%m-%d").date()
                full_backups.append(data)
            except:
                continue

    if not full_backups:
        return CRITICAL, "Nessun backup completo trovato"

    ultimo_full = max(full_backups)

    mancanti_completi = []
    mancanti_incrementali = []

    data_corrente = ultimo_full + datetime.timedelta(days=1)

    while data_corrente <= oggi:

        if data_corrente.weekday() == 6:

            path = f"{backup_dir}/full/full-{data_corrente.strftime('%Y-%m-%d')}.tar.gz"

            if not os.path.exists(path):
                mancanti_completi.append(data_corrente)
        else:
            path = f"{backup_dir}/incr/incr-{data_corrente.strftime('%Y-%m-%d')}.tar.gz"

            if not os.path.exists(path):
                mancanti_incrementali.append(data_corrente.strftime('%Y-%m-%d'))

        data_corrente += datetime.timedelta(days=1)

    if not mancanti_completi and not mancanti_incrementali:
        return OK, f"Tutti i backup OK dal {ultimo_full.strftime('%Y-%m-%d')}"

    msg = "Backup mancanti:\n"

    if mancanti_completi:
        msg += "\nBackup completi mancanti:\n" + "\n".join(mancanti_completi)

    if mancanti_incrementali:
        msg += "\n\nBackup incrementali mancanti:\n" + "\n".join(mancanti_incrementali)

    totale_mancanti = len(mancanti_completi) + len(mancanti_incrementali)

    stato = WARNING if totale_mancanti == 1 else CRITICAL

    return stato, msg


try:
    stato, msg = controlla_backup()
    print(msg)
    sys.exit(stato)

except Exception as e:
    print(f"Errore: {e}")
    sys.exit(UNKNOWN)
