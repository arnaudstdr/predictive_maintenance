# Predictive Maintenance

projet MLOps de maintenance prédictive simulée en temps réel à la périphérie avec Jetson Orin Nano, K3s, Triton/TensorRT et auto-réentraînement dans le cloud.
Ce projet est conçu pour être ultra-convaincant en entretien et démontrer des résultats concrets avec un ROI rapide.


## 🔥 Objectifs et résultats attendus :
- Réduction d’au moins 30 % des arrêts non planifiés.
- ROI inférieur à 6 mois.
- Démonstration percutante « hardware-in-the-loop » pour les entretiens.
- Jetson Orin Nano comme dispositif « Edge » performant en temps réel.


## 🧪 Mise en place de la simulation
- Équipement simulé : pompe centrifuge virtuelle (moteur + rotor).
- Capteurs simulés :
  - Température (°C) du roulement.
  - Vibration (g RMS) du rotor.
  - Courant électrique (A) du moteur.
  - Pression (bar) du fluide.
- Génération des données : script Python pour créer des séries temporelles normales et anomalies (pics de vibration, dérive de température).
- KPIs simulés :
  - Taux de détection des anomalies (true positive rate).
  - Taux de fausses alertes (false positive rate).
  - Latence de détection (secondes).
  - Réduction simulée des arrêts non planifiés (–30 % vs. scénario non prédictif).
⸻

## ⚙️ Stack technologique proposée :
Catégorie
Technologies clés
Hardware -> Jetson Orin Nano
Edge -> K3s, Triton Inference Server, TensorRT, Prometheus, Grafana
Cloud -> Kubernetes (GKE/EKS), MLflow, Kubeflow, Docker, Artifact Registry
CI/CD -> GitHub Actions
Data -> MQTT, Kafka, PostgreSQL, InfluxDB
Monitoring & Alerting -> Prometheus, Grafana, Alertmanager
Re-entraînement -> Kubeflow Pipelines, MLflow
IaC -> Terraform, Helm
