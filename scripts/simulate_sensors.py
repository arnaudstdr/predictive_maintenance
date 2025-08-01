#!/usr/bin/env python3
"""
Génère des séries temporelles simulées pour différents capteurs (température, vibration, courant, pression) avec injection d'anomalies.
Sauvegarde les données en CSV dans le dossier `data/raw/`.
"""
import numpy as np
import pandas as pd
import argparse
import os
from datetime import datetime, timedelta

def generate_time_index(start_time, periods, freq_hz):
    delta = timedelta(seconds=1.0 / freq_hz)
    return [start_time + i * delta for i in range(periods)]

def generate_normal_data(periods):
    # Valeurs normales autour de points de consigne
    temp = np.random.normal(loc=60.0, scale=0.5, size=periods)
    vib = np.random.normal(loc=0.2, scale=0.05, size=periods)
    current = np.random.normal(loc=5.0, scale=0.1, size=periods)
    pressure = np.random.normal(loc=3.0, scale=0.1, size=periods)
    return temp, vib, current, pressure

def inject_anomalies(data, anomaly_ratio, freq_hz):
    periods = len(data[0])
    n_anomalies = max(1, int(periods * anomaly_ratio))
    indices = np.random.choice(periods, size=n_anomalies, replace=False)
    for idx in indices:
        # Choisir type aléatoire d'anomalie
        t = np.random.choice(['temp', 'vib', 'current', 'pressure'])
        if t == 'temp':
            data[0][idx:idx+int(freq_hz*5)] += np.linspace(2, 5, num=min(freq_hz*5, periods-idx))
        elif t == 'vib':
            data[1][idx] += np.random.uniform(1.0, 2.0)
        elif t == 'current':
            data[2][idx:idx+int(freq_hz*3)] *= np.random.uniform(1.5, 2.0)
        else:  # pressure
            data[3][idx] -= np.random.uniform(0.5, 1.0)
    return data

def main():
    parser = argparse.ArgumentParser(description="Simule capteurs et anomalies pour maintenance prédictive.")
    parser.add_argument('--duration', type=float, default=300.0,
                        help='Durée de la simulation en secondes (défaut: 300s)')
    parser.add_argument('--freq', type=float, default=10.0,
                        help='Fréquence d\'échantillonnage en Hz (défaut: 10Hz)')
    parser.add_argument('--anomaly_ratio', type=float, default=0.01,
                        help='Ratio d\'anomalies à injecter (défaut: 1%%)')
    parser.add_argument('--output', type=str, default='data/raw/simulated_data.csv',
                        help='Chemin du fichier de sortie CSV')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    periods = int(args.duration * args.freq)
    start = datetime.utcnow()

    # Génération des données normales
    temp, vib, current, pressure = generate_normal_data(periods)

    # Injection d'anomalies
    temp, vib, current, pressure = inject_anomalies(
        [temp, vib, current, pressure], args.anomaly_ratio, int(args.freq)
    )

    # Création de l'index temporel
    timestamps = generate_time_index(start, periods, args.freq)

    # Construction du DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'temperature_C': temp,
        'vibration_g': vib,
        'current_A': current,
        'pressure_bar': pressure
    })

    # Sauvegarde en CSV
    df.to_csv(args.output, index=False)
    print(f"Simulation terminée. Données sauvegardées dans {args.output}")

if __name__ == '__main__':
    main()