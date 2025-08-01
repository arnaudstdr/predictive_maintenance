#!/usr/bin/env python3
"""
Nettoyage, normalisation et découpage en fenêtres temporelles des données simulées.
"""
import argparse
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

def load_data(input_path):
    df = pd.read_csv(input_path, parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def normalize(df, feature_cols, scaler_path):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[feature_cols])
    joblib.dump(scaler, scaler_path)
    return scaled, scaler

def create_windows(data, window_size, step_size):
    n_samples, n_features = data.shape
    windows = []
    for start in range(0, n_samples - window_size + 1, step_size):
        windows.append(data[start:start+window_size])
    return np.stack(windows)

def main():
    parser = argparse.ArgumentParser(description='Preprocess sensor data: normalization and windowing')
    parser.add_argument('--input', type=str, default='data/raw/simulated_data.csv',
                        help='Chemin du CSV d\'entrées')
    parser.add_argument('--output-dir', type=str, default='data/processed',
                        help='Répertoire de sortie')
    parser.add_argument('--window-size', type=int, default=100,
                        help='Taille de la fenêtre (nbre de pas)')
    parser.add_argument('--step-size', type=int, default=10,
                        help='Pas de déplacement de la fenêtre')
    parser.add_argument('--scaler-path', type=str, default='models/scaler.pkl',
                        help='Chemin pour sauvegarde du scaler')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.scaler_path), exist_ok=True)

    df = load_data(args.input)
    feature_cols = ['temperature_C', 'vibration_g', 'current_A', 'pressure_bar']
    data_scaled, scaler = normalize(df, feature_cols, args.scaler_path)
    windows = create_windows(data_scaled, args.window_size, args.step_size)

    # Sauvegarde des fenêtres
    output_path = os.path.join(args.output_dir, 'windows.npy')
    np.save(output_path, windows)
    print(f'Fenêtres générées : {windows.shape}, sauvegardées dans {output_path}')
    print(f'Scaler sauvegardé dans {args.scaler_path}')

if __name__ == '__main__':
    main()