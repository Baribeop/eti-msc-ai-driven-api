

# import pandas as pd
# import joblib
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import logging
# from pathlib import Path
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# from sklearn.preprocessing import LabelEncoder
# import warnings

# # At the top of train_model.py
# from pathlib import Path

# # Load latest versioned dataset
# data_files = sorted(Path("app/ai").glob("real_training_data_*.csv"))
# data_path = data_files[-1] if data_files else Path("app/ai/real_training_data.csv")

# data = pd.read_csv(data_path)
# print(f"Training on: {data_path.name} | Samples: {len(data)}")

# warnings.filterwarnings('ignore')

# print("🚀 Training AI Model on Real Kaggle Data...\n")

# # ==========================
# # LOAD DATA
# # ==========================

# # data_path = "app/ai/real_training_data.csv"

# # try:
# #     data = pd.read_csv(data_path)
# #     print(f"✅ Dataset loaded successfully! Shape: {data.shape}")
# # except FileNotFoundError:
# #     print("❌ real_training_data.csv not found. Please run data_collection_pipeline.py first.")
# #     exit()

# logger = logging.getLogger(__name__)

# # Load latest dataset
# data_files = sorted(Path("app/ai").glob("real_training_data_*.csv"))
# if data_files:
#     data_path = data_files[-1]   # Use most recent
#     data = pd.read_csv(data_path)
#     logger.info(f"Loaded dataset: {data_path.name}")
# else:
#     data = pd.read_csv("app/ai/real_training_data.csv")
# # ==========================
# # PREPROCESSING
# # ==========================

# # Define feature columns
# feature_cols = [
#     'scs', 'max_depth', 'transactional_score', 'cache_score',
#     'relationship_score', 'time_series_score', 'schema_flexibility'
# ]

# X = data[feature_cols]
# y = data['target']

# # Handle any remaining NaN values
# X = X.fillna(0)

# # Class distribution
# print("\n📊 Class Distribution:")
# print(y.value_counts())

# # ==========================
# # TRAIN-TEST SPLIT
# # ==========================

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, 
#     test_size=0.25, 
#     random_state=42, 
#     stratify=y
# )

# print(f"\nTraining samples: {len(X_train)} | Test samples: {len(X_test)}")

# # ==========================
# # MODEL TRAINING (Improved)
# # ==========================

# model = RandomForestClassifier(
#     n_estimators=400,
#     max_depth=20,
#     min_samples_split=4,
#     min_samples_leaf=2,
#     class_weight='balanced',      # Handles class imbalance from real data
#     random_state=42,
#     n_jobs=-1
# )

# model.fit(X_train, y_train)

# # ==========================
# # EVALUATION
# # ==========================

# y_pred = model.predict(X_test)

# print("\n" + "="*60)
# print("MODEL PERFORMANCE ON REAL DATA")
# print("="*60)
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))

# # Cross-validation score
# cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
# print(f"\n5-Fold Cross Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# # ==========================
# # FEATURE IMPORTANCE
# # ==========================

# feature_importance = pd.DataFrame({
#     'Feature': feature_cols,
#     'Importance': model.feature_importances_
# }).sort_values('Importance', ascending=False)

# print("\n🔝 Top Feature Importance:")
# print(feature_importance)

# # Plot and save
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Importance', y='Feature', data=feature_importance)
# plt.title('Feature Importance - AI Polyglot Router')
# plt.tight_layout()
# plt.savefig('app/ai/feature_importance.png')
# print("📈 Feature importance plot saved as feature_importance.png")

# # ==========================
# # SAVE MODEL
# # ==========================

# joblib.dump(model, 'app/ai/model.pkl')
# print("\n💾 Model saved successfully as app/ai/model.pkl")

# # ==========================
# # SAVE METADATA
# # ==========================

# model_metadata = {
#     "model_type": "RandomForestClassifier",
#     "n_estimators": 400,
#     "accuracy": float(accuracy_score(y_test, y_pred)),
#     "cv_score": float(cv_scores.mean()),
#     "num_samples": len(data),
#     "features_used": feature_cols,
#     "classes": list(model.classes_),
#     "trained_on": "real_kaggle_data + synthetic"
# }

# import json
# with open('app/ai/model_metadata.json', 'w') as f:
#     json.dump(model_metadata, f, indent=2)

# print("📋 Model metadata saved as model_metadata.json")
# print("\n🎉 Training completed successfully!")



# import pandas as pd
# import joblib
# from pathlib import Path
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import LabelEncoder
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from xgboost import XGBClassifier
# from lightgbm import LGBMClassifier
# import logging
# from datetime import datetime

# logger = logging.getLogger(__name__)

# class MultiModelTrainer:
#     def __init__(self):
#         self.models_dir = Path("app/ai/models")
#         self.models_dir.mkdir(parents=True, exist_ok=True)
#         self.label_encoder = LabelEncoder()

#     def load_latest_data(self):
#         data_files = sorted(Path("app/ai").glob("real_training_data_*.csv"))
#         if data_files:
#             data_path = data_files[-1]
#             logger.info(f"Loading latest dataset: {data_path.name}")
#             return pd.read_csv(data_path)
#         else:
#             logger.warning("No versioned dataset found.")
#             return pd.read_csv("app/ai/real_training_data.csv")

#     def train_all_models(self):
#         data = self.load_latest_data()
#         X = data.drop("target", axis=1)
#         y = data["target"]

#         # Encode string labels to integers
#         y_encoded = self.label_encoder.fit_transform(y)
#         joblib.dump(self.label_encoder, self.models_dir / "label_encoder.pkl")

#         X_train, X_test, y_train, y_test = train_test_split(
#             X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
#         )

#         model_configs = {
#             "decision_tree": DecisionTreeClassifier(max_depth=15, random_state=42),
#             "random_forest": RandomForestClassifier(n_estimators=300, random_state=42),
#             "gradient_boosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
#             "xgboost": XGBClassifier(n_estimators=300, eval_metric='mlogloss', random_state=42),
#             "lightgbm": LGBMClassifier(n_estimators=300, verbose=-1, random_state=42)
#         }

#         metrics = {}

#         for name, model in model_configs.items():
#             logger.info(f"Training {name}...")
#             model.fit(X_train, y_train)
#             pred = model.predict(X_test)
#             acc = accuracy_score(y_test, pred)
            
#             metrics[name] = {"accuracy": round(acc, 4), "timestamp": datetime.now().isoformat()}
            
#             joblib.dump(model, self.models_dir / f"{name}.pkl")
#             logger.info(f"✅ {name} trained | Accuracy: {acc:.4f}")

            

#         joblib.dump(metrics, self.models_dir / "metrics.pkl")
#         logger.info("🎉 All models trained successfully!")
#         return metrics


# if __name__ == "__main__":
#     trainer = MultiModelTrainer()
#     trainer.train_all_models()



import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class MultiModelTrainer:
    def __init__(self):
        self.data_dir = Path("data")
        self.model_dir = Path("app/ai/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.feature_names = [
            'scs', 'max_depth', 'transactional_score', 'cache_score',
            'relationship_score', 'time_series_score', 'schema_flexibility',
            'is_bulk', 'has_identifier', 'num_keys', 'has_nested'
        ]

    def load_data(self):
        """Load latest training data"""
        csv_files = list(self.data_dir.glob("*.csv")) + list(Path("app/ai").glob("real_training_data_*.csv"))
        if not csv_files:
            raise FileNotFoundError("No training data found. Run data collector first.")
        
        latest = max(csv_files, key=lambda x: x.stat().st_mtime)
        logger.info(f"Loading training data: {latest.name}")
        df = pd.read_csv(latest)
        return df

    def prepare_data(self, df: pd.DataFrame):
        """Ensure all 11 features are present"""
        # Fill missing structural features with sensible defaults
        for col in ['is_bulk', 'has_identifier', 'has_nested']:
            if col not in df.columns:
                df[col] = 0
            else:
                df[col] = df[col].astype(int)
        
        if 'num_keys' not in df.columns:
            df['num_keys'] = 0

        # Keep only required features + target
        X = df[self.feature_names]
        y = df['target']
        
        # Encode labels
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Save label encoder
        joblib.dump(le, self.model_dir / "label_encoder.pkl")
        logger.info(f"Classes: {le.classes_}")
        
        return X, y_encoded, le

    def train_all_models(self):
        df = self.load_data()
        X, y, le = self.prepare_data(df)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        models = {}
        metrics = {}

        # Decision Tree
        dt = DecisionTreeClassifier(random_state=42)
        dt.fit(X_train, y_train)
        models["decision_tree"] = dt
        metrics["decision_tree"] = dt.score(X_test, y_test)

        # Random Forest (main model)
        rf = RandomForestClassifier(n_estimators=200, random_state=42)
        rf.fit(X_train, y_train)
        models["random_forest"] = rf
        metrics["random_forest"] = rf.score(X_test, y_test)

        # Gradient Boosting
        gb = GradientBoostingClassifier(random_state=42)
        gb.fit(X_train, y_train)
        models["gradient_boosting"] = gb
        metrics["gradient_boosting"] = gb.score(X_test, y_test)

        # XGBoost
        xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')
        xgb_model.fit(X_train, y_train)
        models["xgboost"] = xgb_model
        metrics["xgboost"] = xgb_model.score(X_test, y_test)

        # LightGBM
        lgb_model = lgb.LGBMClassifier(random_state=42, verbose=-1)
        lgb_model.fit(X_train, y_train)
        models["lightgbm"] = lgb_model
        metrics["lightgbm"] = lgb_model.score(X_test, y_test)

        # Save all models
        for name, model in models.items():
            joblib.dump(model, self.model_dir / f"{name}.pkl")
            logger.info(f"✅ Saved {name} model")

        logger.info("Training completed with metrics:")
        for model_name, score in metrics.items():
            logger.info(f"  {model_name}: {score:.4f}")

        return metrics

if __name__ == "__main__":
    trainer = MultiModelTrainer()
    trainer.train_all_models()