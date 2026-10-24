"""Optional educational ML experiment using only synthetic generated measurements.

Run: python ml/anomaly_detection.py
This is NOT a diagnostic classifier or evidence of vehicle safety.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, precision_score, recall_score

def main():
    rng = np.random.default_rng(42)
    # Training data: synthetic normal measurements only.
    train = rng.normal(loc=[12.0, 30.0], scale=[0.25, 3.0], size=(400, 2))
    # Unseen synthetic evaluation data.
    normal = rng.normal(loc=[12.0, 30.0], scale=[0.25, 3.0], size=(100, 2))
    abnormal = rng.normal(loc=[9.8, 70.0], scale=[0.25, 3.0], size=(100, 2))
    test = np.vstack([normal, abnormal])
    labels = np.array([0] * len(normal) + [1] * len(abnormal))
    model = IsolationForest(n_estimators=150, contamination=0.1, random_state=42)
    model.fit(train)
    predictions = (model.predict(test) == -1).astype(int)
    print("SIMULATED anomaly-detection evaluation only")
    print("Confusion matrix (labels: 0=synthetic normal, 1=synthetic anomaly):")
    print(confusion_matrix(labels, predictions, labels=[0, 1]))
    print(f"Precision: {precision_score(labels, predictions, zero_division=0):.3f}")
    print(f"Recall: {recall_score(labels, predictions, zero_division=0):.3f}")
    print("Result is not a real-vehicle validation or fault diagnosis.")

if __name__ == "__main__":
    main()
