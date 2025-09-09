#!/bin/bash
export MDP="Tu l'auras toujours pas :)"
# Chemin vers le fichier de log
LOG_FILE="/home/noe_leyhuelic/log_presence.txt"
ERROR_LOG_FILE="/home/noe_leyhuelic/log_presence_errors.txt"

# Ajouter un message de début dans le fichier de log
echo "[$(date)] Starting script" >> "$LOG_FILE"

# Exécuter le script Python et rediriger les sorties
/usr/bin/python3 /home/noe_leyhuelic/Calendrier.py >> "$LOG_FILE" 2>> "$ERROR_LOG_FILE"

# Ajouter un message de fin dans le fichier de log
echo "[$(date)] Script finished" >> "$LOG_FILE"
