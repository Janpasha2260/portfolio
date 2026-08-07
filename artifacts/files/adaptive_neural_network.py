"""Workshop Three evidence: a neural network adapting to a changed data pattern.

The example uses synthetic two-class data so no private or real-world records are used.
It demonstrates concept drift: a model performs well in the original environment,
its accuracy falls when the environment changes, and performance improves after
retraining with representative data from the new environment.
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

RANDOM_STATE = 42


def build_model() -> MLPClassifier:
    """Create a small feed-forward artificial neural network."""
    return MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        solver="adam",
        max_iter=2_000,
        random_state=RANDOM_STATE,
    )


def create_changed_reality(features: np.ndarray) -> np.ndarray:
    """Rotate, rescale, and shift the feature space to simulate concept drift."""
    angle = np.deg2rad(38)
    rotation = np.array(
        [
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)],
        ]
    )
    return (features @ rotation.T) * np.array([1.25, 0.80]) + np.array([0.45, -0.15])


def main() -> None:
    features, labels = make_moons(
        n_samples=1_600,
        noise=0.22,
        random_state=RANDOM_STATE,
    )

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.30,
        stratify=labels,
        random_state=RANDOM_STATE,
    )

    original_model = build_model()
    original_model.fit(x_train, y_train)
    original_accuracy = accuracy_score(y_test, original_model.predict(x_test))

    changed_features = create_changed_reality(features)
    xd_train, xd_test, yd_train, yd_test = train_test_split(
        changed_features,
        labels,
        test_size=0.30,
        stratify=labels,
        random_state=RANDOM_STATE,
    )

    drift_accuracy = accuracy_score(yd_test, original_model.predict(xd_test))

    adapted_model = build_model()
    adapted_model.fit(xd_train, yd_train)
    adapted_accuracy = accuracy_score(yd_test, adapted_model.predict(xd_test))

    print(f"Original environment accuracy: {original_accuracy:.1%}")
    print(f"Changed environment before adaptation: {drift_accuracy:.1%}")
    print(f"Changed environment after retraining: {adapted_accuracy:.1%}")


if __name__ == "__main__":
    main()
