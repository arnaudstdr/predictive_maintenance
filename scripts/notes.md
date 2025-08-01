# simulate_sensors.py

## Objectif du script

Ce script simule des séries temporelles de mesures provenant de capteurs industriels (température, vibration, courant, pression) et injecte des anomalies pour générer des données réalistes destinées à la maintenance prédictive. Les données sont sauvegardées dans un fichier CSV.

---

## Fonctionnement détaillé

### 1. **Imports et configuration**
- Utilise `numpy` pour la génération de données aléatoires.
- Utilise `pandas` pour la manipulation et l’export des données.
- Utilise `argparse` pour gérer les arguments en ligne de commande.
- Utilise `os` pour la gestion des dossiers.
- Utilise `datetime` pour la gestion des timestamps.

---

### 2. **Fonctions principales**

#### a. `generate_time_index(start_time, periods, freq_hz)`
- Crée une liste de timestamps espacés régulièrement selon la fréquence d’échantillonnage (`freq_hz`).
- Exemple : pour 10 Hz et 300 secondes, il génère 3000 timestamps espacés de 0,1s.

#### b. `generate_normal_data(periods)`
- Génère des séries de valeurs normales pour chaque capteur :
  - Température autour de 60°C (bruit ±0,5)
  - Vibration autour de 0,2g (bruit ±0,05)
  - Courant autour de 5A (bruit ±0,1)
  - Pression autour de 3 bars (bruit ±0,1)

#### c. `inject_anomalies(data, anomaly_ratio, freq_hz)`
- Injecte des anomalies dans les données simulées.
- Le nombre d’anomalies dépend du ratio fourni (`anomaly_ratio`).
- Pour chaque anomalie, choisit aléatoirement le capteur affecté et modifie les valeurs sur une courte période :
  - Température : élévation progressive sur 5 secondes.
  - Vibration : pic soudain.
  - Courant : augmentation soudaine sur 3 secondes.
  - Pression : chute soudaine.

---

### 3. **Fonction principale `main()`**

- **Arguments en ligne de commande** :
  - `--duration` : durée de la simulation (en secondes)
  - `--freq` : fréquence d’échantillonnage (en Hz)
  - `--anomaly_ratio` : proportion d’anomalies à injecter
  - `--output` : chemin du fichier CSV de sortie

- **Étapes** :
  1. Crée le dossier de sortie si besoin.
  2. Calcule le nombre total de points (`periods`).
  3. Génère les données normales.
  4. Injecte les anomalies.
  5. Génère l’index temporel.
  6. Construit un DataFrame pandas avec toutes les données.
  7. Sauvegarde le DataFrame en CSV.
  8. Affiche un message de confirmation.

---

## Résumé

Ce script permet de générer rapidement des données de capteurs réalistes, avec des anomalies, pour tester des algorithmes de détection ou entraîner des modèles de maintenance prédictive.  
Il est paramétrable via la ligne de commande pour s’adapter à différents scénarios.

# preprocess.py

Bien sûr ! Voici une explication détaillée du script preprocess.py :

---

## Objectif du script

Ce script prépare les données simulées pour l’entraînement de modèles de maintenance prédictive.  
Il effectue trois étapes principales :
1. **Chargement et nettoyage** des données.
2. **Normalisation** des variables (mise à l’échelle entre 0 et 1).
3. **Découpage en fenêtres temporelles** (pour les modèles séquentiels type RNN/CNN).

---

## Fonctionnement détaillé

### 1. **Imports et configuration**
- `pandas` et `numpy` : manipulation des données.
- `MinMaxScaler` de scikit-learn : normalisation.
- `joblib` : sauvegarde du scaler pour réutilisation.
- `argparse` et `os` : gestion des arguments et des dossiers.

---

### 2. **Fonctions principales**

#### a. `load_data(input_path)`
- Charge le CSV des données simulées.
- Trie les données par timestamp et réinitialise les index.
- Retourne un DataFrame propre.

#### b. `normalize(df, feature_cols, scaler_path)`
- Applique une normalisation MinMax (chaque variable entre 0 et 1) sur les colonnes d’intérêt.
- Enregistre le scaler sur disque pour garantir la cohérence lors de l’inférence ou d’autres traitements.
- Retourne les données normalisées et le scaler.

#### c. `create_windows(data, window_size, step_size)`
- Découpe les données normalisées en fenêtres temporelles glissantes :
  - `window_size` : nombre de points par fenêtre.
  - `step_size` : décalage entre deux fenêtres.
- Retourne un tableau numpy de forme `(nb_fenêtres, window_size, nb_features)`.

---

### 3. **Fonction principale `main()`**

- **Arguments en ligne de commande** :
  - `--input` : chemin du CSV d’entrée.
  - `--output-dir` : dossier où sauvegarder les fenêtres.
  - `--window-size` : taille de chaque fenêtre.
  - `--step-size` : pas de déplacement de la fenêtre.
  - `--scaler-path` : chemin pour sauvegarder le scaler.

- **Étapes** :
  1. Crée les dossiers de sortie si besoin.
  2. Charge et nettoie les données.
  3. Sélectionne les colonnes de features.
  4. Normalise les données et sauvegarde le scaler.
  5. Découpe les données en fenêtres temporelles.
  6. Sauvegarde les fenêtres dans un fichier `.npy` (format numpy).
  7. Affiche des informations sur la forme des données sauvegardées.

---

## Résumé

Ce script transforme les données brutes simulées en un format directement exploitable pour l’entraînement de modèles de deep learning, tout en garantissant la reproductibilité de la normalisation.  
Il est entièrement paramétrable via la ligne de commande.

N’hésite pas si tu veux des précisions sur une étape !