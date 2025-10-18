"""
Basic model loading tests for Titanic Survival Prediction.
Ensures that serialized models (Keras, PyTorch, Scikit-Learn) can be loaded
without errors, confirming that training scripts saved them correctly.
"""

import os
from typing import Callable, Optional

import pytest

# Import frameworks with safe fallbacks
try:
    import joblib
except ImportError:
    joblib = None

try:
    import torch
except ImportError:
    torch = None


keras_load_model: Optional[Callable] = None
try:
    from tensorflow.keras.models import load_model as keras_load_model
except Exception:
    pass


@pytest.mark.parametrize(
    "path",
    ["models/sklearn_model.pkl", "models/keras_model.h5", "models/pytorch_model.pt"],
)
def test_model_file_exists(path):
    """Check that model files exist in /models."""
    assert os.path.exists(path), f"Missing model file: {path}"


@pytest.mark.skipif(joblib is None, reason="Joblib not available")
def test_load_sklearn_model():
    """Ensure scikit-learn model loads successfully."""
    model_path = "models/sklearn_model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        assert model is not None, "Failed to load scikit-learn model"


@pytest.mark.skipif(keras_load_model is None, reason="TensorFlow not available")
def test_load_keras_model():
    """Ensure Keras model loads successfully."""
    model_path = "models/keras_model.h5"
    if os.path.exists(model_path):
        if keras_load_model is not None:
            model = keras_load_model(model_path)
            assert hasattr(model, "predict"), "Keras model missing predict()"


@pytest.mark.skipif(torch is None, reason="PyTorch not available")
def test_load_pytorch_model():
    """Ensure PyTorch model loads successfully."""
    model_path = "models/pytorch_model.pt"
    if os.path.exists(model_path):
        model = torch.load(model_path, map_location="cpu")
        assert model is not None, "Failed to load PyTorch model"
