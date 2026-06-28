

# import joblib
# import pandas as pd
# from pathlib import Path
# import logging
# from typing import Dict

# logger = logging.getLogger(__name__)

# class MultiModelPredictor:
#     def __init__(self):
#         self.models = {}
#         self.current_model = "random_forest"
#         self.load_models()

#     def load_models(self):
#         model_dir = Path("app/ai/models")
#         model_dir.mkdir(exist_ok=True)
#         for name in ["decision_tree", "random_forest", "gradient_boosting", "xgboost", "lightgbm"]:
#             path = model_dir / f"{name}.pkl"
#             if path.exists():
#                 self.models[name] = joblib.load(path)
#                 logger.info(f"Loaded model: {name}")

#     def predict(self, features: Dict) -> Dict:
#         if not self.models:
#             return {"error": "No models loaded"}
        
#         model = self.models.get(self.current_model, list(self.models.values())[0])
        
#         feature_list = [
#             features.get("scs", 0), features.get("max_depth", 0),
#             features.get("transactional_score", 0), features.get("cache_score", 0),
#             features.get("relationship_score", 0), features.get("time_series_score", 0),
#             features.get("schema_flexibility", 0)
#         ]
        
#         X = pd.DataFrame([feature_list], columns=[
#             'scs','max_depth','transactional_score','cache_score',
#             'relationship_score','time_series_score','schema_flexibility'
#         ])
        
#         pred = model.predict(X)[0]
#         confidence = model.predict_proba(X).max() if hasattr(model, "predict_proba") else 0.85

#         return {
#             "database": str(pred),
#             "model_used": self.current_model,
#             "confidence": round(float(confidence), 4),
#             "features": features
#         }

#     def explain(self, features: Dict):
#         return {
#             "recommended_database": self.predict(features)["database"],
#             "explanation": "Based on payload workload features and multi-model ensemble.",
#             "confidence": self.predict(features)["confidence"]
#         }

#     def switch_model(self, model_name: str):
#         if model_name in self.models:
#             self.current_model = model_name
#             return True
#         return False

#     def get_current_model_info(self):
#         return {
#             "current_model": self.current_model,
#             "available_models": list(self.models.keys())
#         }



# import joblib
# import pandas as pd
# from pathlib import Path
# import logging
# from typing import Dict

# logger = logging.getLogger(__name__)

# class MultiModelPredictor:
#     def __init__(self):
#         self.models = {}
#         self.label_encoder = None
#         self.current_model = "random_forest"
#         self.load_models()

#     def load_models(self):
#         model_dir = Path("app/ai/models")
#         model_dir.mkdir(exist_ok=True)
        
#         # Load label encoder
#         le_path = model_dir / "label_encoder.pkl"
#         if le_path.exists():
#             self.label_encoder = joblib.load(le_path)

#         for name in ["decision_tree", "random_forest", "gradient_boosting", "xgboost", "lightgbm"]:
#             path = model_dir / f"{name}.pkl"
#             if path.exists():
#                 self.models[name] = joblib.load(path)
#                 logger.info(f"Loaded model: {name}")

#     def predict(self, features: Dict) -> Dict:
#         if not self.models or not self.label_encoder:
#             return {"error": "Models not loaded properly"}

#         model = self.models.get(self.current_model, list(self.models.values())[0])
        
#         feature_list = [
#             features.get("scs", 0), features.get("max_depth", 0),
#             features.get("transactional_score", 0), features.get("cache_score", 0),
#             features.get("relationship_score", 0), features.get("time_series_score", 0),
#             features.get("schema_flexibility", 0)
#         ]
        
#         X = pd.DataFrame([feature_list], columns=[
#             'scs','max_depth','transactional_score','cache_score',
#             'relationship_score','time_series_score','schema_flexibility'
#         ])


#         print("Model expects:")
#         print(model.feature_names_in_)

#         print("Predictor provides:")
#         print(X.columns.tolist())
        
#         pred_encoded = model.predict(X)[0]
#         prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

#         confidence = model.predict_proba(X).max() if hasattr(model, "predict_proba") else 0.85

#         return {
#             "database": prediction,
#             "model_used": self.current_model,
#             "confidence": round(float(confidence), 4),
#             "features": features
#         }




# import joblib
# import pandas as pd
# from pathlib import Path
# import logging
# from typing import Dict, Any

# logger = logging.getLogger(__name__)

# class MultiModelPredictor:
#     def __init__(self):
#         self.models = {}
#         self.label_encoder = None
#         self.current_model = "random_forest"
#         # Full feature list matching the trained models
#         self.feature_names = [
#             'scs', 'max_depth', 'transactional_score', 'cache_score',
#             'relationship_score', 'time_series_score', 'schema_flexibility',
#             'is_bulk', 'has_identifier', 'num_keys', 'has_nested'
#         ]
#         self.load_models()

#     def load_models(self):
#         model_dir = Path("app/ai/models")
#         model_dir.mkdir(exist_ok=True)
        
#         # Load label encoder
#         le_path = model_dir / "label_encoder.pkl"
#         if le_path.exists():
#             self.label_encoder = joblib.load(le_path)

#         for name in ["decision_tree", "random_forest", "gradient_boosting", "xgboost", "lightgbm"]:
#             path = model_dir / f"{name}.pkl"
#             if path.exists():
#                 self.models[name] = joblib.load(path)
#                 logger.info(f"Loaded model: {name}")

#     def predict(self, features: Dict) -> Dict:
#         if not self.models or not self.label_encoder:
#             return {"error": "Models not loaded properly"}

#         model = self.models.get(self.current_model, list(self.models.values())[0])
        
#         # Build complete feature vector (preserves original logic + adds missing features with defaults)
#         full_features = {
#             "scs": features.get("scs", 0.0),
#             "max_depth": features.get("max_depth", 0),
#             "transactional_score": features.get("transactional_score", 0.0),
#             "cache_score": features.get("cache_score", 0.0),
#             "relationship_score": features.get("relationship_score", 0.0),
#             "time_series_score": features.get("time_series_score", 0.0),
#             "schema_flexibility": features.get("schema_flexibility", 0.0),
#             "is_bulk": int(features.get("is_bulk", False)),
#             "has_identifier": int(features.get("has_identifier", False)),
#             "num_keys": int(features.get("num_keys", 0)),
#             "has_nested": int(features.get("has_nested", False)),
#         }

#         # Create DataFrame with exact column order
#         X = pd.DataFrame([full_features])[self.feature_names]

#         pred_encoded = model.predict(X)[0]
#         prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

#         confidence = float(model.predict_proba(X).max()) if hasattr(model, "predict_proba") else 0.85

#         return {
#             "database": prediction,
#             "model_used": self.current_model,
#             "confidence": round(confidence, 4),
#             "features": full_features
#         }

#     def explain(self, features: Dict) -> Dict:
#         # Placeholder - you can expand later
#         return {"message": "Explainability coming soon", "features": features}

#     def get_current_model_info(self):
#         return {
#             "current_model": self.current_model,
#             "available_models": list(self.models.keys()),
#             "feature_count": len(self.feature_names)
#         }
    
#     def switch_model(self, model_name: str):
#         if model_name in self.models:
#             self.current_model = model_name
#             return True
#         return False



# import joblib
# import pandas as pd
# from pathlib import Path
# import logging
# from typing import Dict, Any

# logger = logging.getLogger(__name__)

# class MultiModelPredictor:
#     def __init__(self):
#         self.models = {}
#         self.label_encoder = None
#         self.current_model = "random_forest"
#         # Full feature list matching the trained models
#         self.feature_names = [
#             'scs', 'max_depth', 'transactional_score', 'cache_score',
#             'relationship_score', 'time_series_score', 'schema_flexibility',
#             'is_bulk', 'has_identifier', 'num_keys', 'has_nested'
#         ]
#         self.load_models()

#     def load_models(self):
#         model_dir = Path("app/ai/models")
#         model_dir.mkdir(exist_ok=True)
        
#         # Load label encoder
#         le_path = model_dir / "label_encoder.pkl"
#         if le_path.exists():
#             self.label_encoder = joblib.load(le_path)

#         for name in ["decision_tree", "random_forest", "gradient_boosting", "xgboost", "lightgbm"]:
#             path = model_dir / f"{name}.pkl"
#             if path.exists():
#                 self.models[name] = joblib.load(path)
#                 logger.info(f"Loaded model: {name}")

#     def predict(self, features: Dict) -> Dict:
#         if not self.models or not self.label_encoder:
#             return {"error": "Models not loaded properly"}

#         model = self.models.get(self.current_model, list(self.models.values())[0])
        
#         # Build complete feature vector (preserves original logic + adds missing features with defaults)
#         full_features = {
#             "scs": features.get("scs", 0.0),
#             "max_depth": features.get("max_depth", 0),
#             "transactional_score": features.get("transactional_score", 0.0),
#             "cache_score": features.get("cache_score", 0.0),
#             "relationship_score": features.get("relationship_score", 0.0),
#             "time_series_score": features.get("time_series_score", 0.0),
#             "schema_flexibility": features.get("schema_flexibility", 0.0),
#             "is_bulk": int(features.get("is_bulk", False)),
#             "has_identifier": int(features.get("has_identifier", False)),
#             "num_keys": int(features.get("num_keys", 0)),
#             "has_nested": int(features.get("has_nested", False)),
#         }

#         # Create DataFrame with exact column order
#         X = pd.DataFrame([full_features])[self.feature_names]

#         pred_encoded = model.predict(X)[0]
#         prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

#         confidence = float(model.predict_proba(X).max()) if hasattr(model, "predict_proba") else 0.85

#         return {
#             "database": prediction,
#             "model_used": self.current_model,
#             "confidence": round(confidence, 4),
#             "features": full_features
#         }

#     # def explain(self, features: Dict) -> Dict:
#     #     # Placeholder - you can expand later
#     #     return {"message": "Explainability coming soon", "features": features}

#     def explain(self, features: Dict) -> Dict:

#         """Real feature importance + reasoning explanation"""

#         if not self.models or not self.label_encoder:

#             return {"error": "Models not loaded"}

#         model = self.models.get(self.current_model, list(self.models.values())[0])

#         # Build full features (same as predict)

#         full_features = {

#             "scs": features.get("scs", 0.0),

#             "max_depth": features.get("max_depth", 0),

#             "transactional_score": features.get("transactional_score", 0.0),

#             "cache_score": features.get("cache_score", 0.0),

#             "relationship_score": features.get("relationship_score", 0.0),

#             "time_series_score": features.get("time_series_score", 0.0),

#             "schema_flexibility": features.get("schema_flexibility", 0.0),

#             "is_bulk": int(features.get("is_bulk", False)),

#             "has_identifier": int(features.get("has_identifier", False)),

#             "num_keys": int(features.get("num_keys", 0)),

#             "has_nested": int(features.get("has_nested", False)),

#         }

#         X = pd.DataFrame([full_features])[self.feature_names]

#         # Get prediction first

#         pred_encoded = model.predict(X)[0]

#         prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

#         proba = model.predict_proba(X)[0]

#         confidence = float(max(proba))

#         # Simple Feature Importance (using model if available)

#         importance = {}

#         if hasattr(model, "feature_importances_"):

#             importances = model.feature_importances_

#             importance = dict(zip(self.feature_names, importances.round(4)))

#             # Sort top 5

#             top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]

#         else:

#             top_features = []

#         # Human-readable reasoning

#         reasoning = self._generate_reasoning(full_features, prediction)

#         return {

#             "database": prediction,

#             "confidence": round(confidence, 4),

#             "top_features": dict(top_features),

#             "reasoning": reasoning,

#             "feature_values": full_features

#         }

#     def _generate_reasoning(self, features: dict, predicted_db: str) -> list:

#         """Generate human-friendly explanation"""

#         reasons = []

#         if predicted_db == "postgres":

#             if features["transactional_score"] > 0.6:

#                 reasons.append("High transactional requirements → Relational DB recommended")

#             if features["is_bulk"] and features["num_keys"] > 10:

#                 reasons.append("Structured bulk data with many keys")

#         elif predicted_db == "mongo":

#             if features["schema_flexibility"] > 0.7 or features["has_nested"]:

#                 reasons.append("High schema flexibility & nested data → Document DB")

#         elif predicted_db == "redis":

#             if features["cache_score"] > 0.7:

#                 reasons.append("Strong cache-friendly patterns detected")

#         elif predicted_db == "influxdb":

#             if features["time_series_score"] > 0.6:

#                 reasons.append("Time-series / sensor data detected")

#         elif predicted_db == "neo4j":

#             if features["relationship_score"] > 0.6:

#                 reasons.append("Strong relationship / graph patterns")

#         if not reasons:

#             reasons.append(f"Model confidence based on overall feature pattern")

#         return reasons
#     def get_current_model_info(self):
#         return {
#             "current_model": self.current_model,
#             "available_models": list(self.models.keys()),
#             "feature_count": len(self.feature_names)
#         }
    
#     def switch_model(self, model_name: str):
#         if model_name in self.models:
#             self.current_model = model_name
#             return True
#         return False





import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MultiModelPredictor:
    def __init__(self):
        self.models = {}
        self.label_encoder = None
        self.current_model = "random_forest"
        # Full feature list matching the trained models
        self.feature_names = [
            'scs', 'max_depth', 'transactional_score', 'cache_score',
            'relationship_score', 'time_series_score', 'schema_flexibility',
            'is_bulk', 'has_identifier', 'num_keys', 'has_nested'
        ]
        self.load_models()

    def load_models(self):
        model_dir = Path("app/ai/models")
        model_dir.mkdir(exist_ok=True)

        # Load label encoder
        le_path = model_dir / "label_encoder.pkl"
        if le_path.exists():
            self.label_encoder = joblib.load(le_path)

        for name in ["decision_tree", "random_forest", "gradient_boosting", "xgboost", "lightgbm"]:
            path = model_dir / f"{name}.pkl"
            if path.exists():
                self.models[name] = joblib.load(path)
                logger.info(f"Loaded model: {name}")

    def predict(self, features: Dict) -> Dict:
        if not self.models or not self.label_encoder:
            return {"error": "Models not loaded properly"}

        model = self.models.get(self.current_model, list(self.models.values())[0])

        # Build complete feature vector (preserves original logic + adds missing features with defaults)
        full_features = {
            "scs": features.get("scs", 0.0),
            "max_depth": features.get("max_depth", 0),
            "transactional_score": features.get("transactional_score", 0.0),
            "cache_score": features.get("cache_score", 0.0),
            "relationship_score": features.get("relationship_score", 0.0),
            "time_series_score": features.get("time_series_score", 0.0),
            "schema_flexibility": features.get("schema_flexibility", 0.0),
            "is_bulk": int(features.get("is_bulk", False)),
            "has_identifier": int(features.get("has_identifier", False)),
            "num_keys": int(features.get("num_keys", 0)),
            "has_nested": int(features.get("has_nested", False)),
        }

        # Create DataFrame with exact column order
        X = pd.DataFrame([full_features])[self.feature_names]

        pred_encoded = model.predict(X)[0]
        prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

        confidence = float(model.predict_proba(X).max()) if hasattr(model, "predict_proba") else 0.85

        return {
            "database": prediction,
            "model_used": self.current_model,
            "confidence": round(confidence, 4),
            "features": full_features
        }

    def explain(self, features: Dict) -> Dict:
        """Real feature importance + reasoning explanation.

        NOTE ON THE FIX BELOW: model.feature_importances_ is NOT
        guaranteed to be a plain NumPy array with a .round() method
        across all five model libraries. scikit-learn's native models
        (Decision Tree, Random Forest, Gradient Boosting) return a
        standard ndarray, but XGBoost and LightGBM can return values of
        a different underlying type/dtype after joblib
        serialisation/deserialisation, which do not support .round()
        being called as a method the same way. Calling .round() directly
        on importances therefore raised an unhandled exception (visible
        as a generic 500 Internal Server Error) specifically for the
        xgboost and lightgbm models, while working correctly for the
        three scikit-learn-native models.

        THE FIX: wrap importances in np.array(..., dtype=float) first to
        force a consistent, predictable type regardless of source
        library, use the free function np.round() rather than the
        .round() method, and convert the result to a plain Python list
        with .tolist() so FastAPI's JSON serialiser never has to handle
        a raw numpy scalar type either (a related, separate failure mode
        this also pre-empts).
        """
        if not self.models or not self.label_encoder:
            return {"error": "Models not loaded"}

        model = self.models.get(self.current_model, list(self.models.values())[0])

        # Build full features (same as predict)
        full_features = {
            "scs": features.get("scs", 0.0),
            "max_depth": features.get("max_depth", 0),
            "transactional_score": features.get("transactional_score", 0.0),
            "cache_score": features.get("cache_score", 0.0),
            "relationship_score": features.get("relationship_score", 0.0),
            "time_series_score": features.get("time_series_score", 0.0),
            "schema_flexibility": features.get("schema_flexibility", 0.0),
            "is_bulk": int(features.get("is_bulk", False)),
            "has_identifier": int(features.get("has_identifier", False)),
            "num_keys": int(features.get("num_keys", 0)),
            "has_nested": int(features.get("has_nested", False)),
        }

        X = pd.DataFrame([full_features])[self.feature_names]

        # Get prediction first
        pred_encoded = model.predict(X)[0]
        prediction = self.label_encoder.inverse_transform([pred_encoded])[0]

        proba = model.predict_proba(X)[0]
        confidence = float(max(proba))

        # Feature importance (using model if available) -- FIXED to work
        # consistently across scikit-learn, XGBoost, and LightGBM models
        top_features = []
        if hasattr(model, "feature_importances_"):
            try:
                importances = np.round(
                    np.array(model.feature_importances_, dtype=float), 4
                ).tolist()
                importance = dict(zip(self.feature_names, importances))
                # Sort top 5
                top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]
            except Exception as e:
                logger.error(f"Feature importance extraction failed for model "
                             f"'{self.current_model}': {e}")
                top_features = []

        # Human-readable reasoning
        reasoning = self._generate_reasoning(full_features, prediction)

        return {
            "database": prediction,
            "confidence": round(confidence, 4),
            "top_features": dict(top_features),
            "reasoning": reasoning,
            "feature_values": full_features
        }

    def _generate_reasoning(self, features: dict, predicted_db: str) -> list:
        """Generate human-friendly explanation"""
        reasons = []

        if predicted_db == "postgres":
            if features["transactional_score"] > 0.6:
                reasons.append("High transactional requirements → Relational DB recommended")
            if features["is_bulk"] and features["num_keys"] > 10:
                reasons.append("Structured bulk data with many keys")

        elif predicted_db == "mongo":
            if features["schema_flexibility"] > 0.7 or features["has_nested"]:
                reasons.append("High schema flexibility & nested data → Document DB")

        elif predicted_db == "redis":
            if features["cache_score"] > 0.7:
                reasons.append("Strong cache-friendly patterns detected")

        elif predicted_db == "influxdb":
            if features["time_series_score"] > 0.6:
                reasons.append("Time-series / sensor data detected")

        elif predicted_db == "neo4j":
            if features["relationship_score"] > 0.6:
                reasons.append("Strong relationship / graph patterns")

        if not reasons:
            reasons.append("Model confidence based on overall feature pattern")

        return reasons

    def get_current_model_info(self):
        return {
            "current_model": self.current_model,
            "available_models": list(self.models.keys()),
            "feature_count": len(self.feature_names)
        }

    def switch_model(self, model_name: str):
        if model_name in self.models:
            self.current_model = model_name
            return True
        return False