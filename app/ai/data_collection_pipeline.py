# import pandas as pd
# import numpy as np
# import kagglehub
# import json
# import logging
# from pathlib import Path
# from datetime import datetime
# from app.analysis.payload_analyzer import analyze_payload


# # Ensure log directory exists
# log_dir = Path("app/ai")
# log_dir.mkdir(parents=True, exist_ok=True)
# # Configure Logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s | %(levelname)s | %(message)s',
#     handlers=[
#         logging.FileHandler("app/ai/data_collection.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# class PolyglotDataCollector:
    
#     def __init__(self):
#         self.data = []
#         self.data_dir = Path("data")
#         self.data_dir.mkdir(exist_ok=True)
#         self.version = datetime.now().strftime("%Y%m%d_%H%M%S")
#         self.output_file = f"app/ai/real_training_data_{self.version}.csv"
    
#     def download_kaggle_dataset(self, dataset_slug: str):
#         """Download dataset with error handling"""
#         try:
#             logger.info(f"Downloading dataset: {dataset_slug}")
#             path = kagglehub.dataset_download(dataset_slug)
#             logger.info(f"Successfully downloaded: {path}")
#             return Path(path)
#         except Exception as e:
#             logger.error(f"Failed to download {dataset_slug}: {str(e)}")
#             return None
    
#     def process_transactional(self, sample_size=800):
#         path = self.download_kaggle_dataset("olistbr/brazilian-ecommerce")
#         if not path:
#             return self._add_synthetic_transactional(sample_size)
        
#         csv_path = path / "olist_orders_dataset.csv"
#         if csv_path.exists():
#             try:
#                 df = pd.read_csv(csv_path)
#                 for _, row in df.sample(min(sample_size, len(df))).iterrows():
#                     features = analyze_payload(row.to_dict())
#                     features['target'] = 'postgres'
#                     self.data.append(features)
#                 logger.info(f"✅ Transactional data processed ({len(df)} rows)")
#             except Exception as e:
#                 logger.error(f"Error processing transactional data: {e}")
#                 self._add_synthetic_transactional(sample_size)
    
#     def process_time_series(self, sample_size=700):
#         path = self.download_kaggle_dataset("ziya07/iot-integrated-predictive-maintenance-dataset")
#         if not path:
#             return self._add_synthetic_time_series(sample_size)
        
#         csv_files = list(path.glob("*.csv"))
#         if csv_files:
#             try:
#                 df = pd.read_csv(csv_files[0])
#                 for _, row in df.sample(min(sample_size, len(df))).iterrows():
#                     payload = {
#                         "sensor_id": str(row.get("sensor_id", "S001")),
#                         "timestamp": str(pd.Timestamp.now()),
#                         **{k: v for k, v in row.to_dict().items() if isinstance(v, (int, float))}
#                     }
#                     features = analyze_payload(payload)
#                     features['target'] = 'influxdb'
#                     self.data.append(features)
#                 logger.info("✅ Time-Series (InfluxDB) processed")
#             except Exception as e:
#                 logger.error(f"Error processing time-series data: {e}")
    
#     def process_graph(self, sample_size=600):
#         path = self.download_kaggle_dataset("wolfram77/graphs-social")
#         if path and (path / "facebook_combined.txt").exists():
#             try:
#                 df = pd.read_csv(path / "facebook_combined.txt", sep=' ', header=None, names=['source', 'target'])
#                 for _, row in df.sample(min(sample_size, len(df))).iterrows():
#                     payload = {
#                         "nodes": [int(row['source']), int(row['target'])],
#                         "relationship": "FRIENDS",
#                         "type": "social_connection"
#                     }
#                     features = analyze_payload(payload)
#                     features['target'] = 'neo4j'
#                     self.data.append(features)
#                 logger.info("✅ Graph (Neo4j) processed")
#                 return
#             except Exception as e:
#                 logger.warning(f"Graph processing failed: {e}")
#         self._add_synthetic_graph(sample_size)
    
#     def process_document(self, sample_size=500):
#         path = self.download_kaggle_dataset("shrashtisinghal/mongo-db-datsets")
#         if path:
#             json_files = list(path.glob("**/*.json"))
#             if json_files:
#                 try:
#                     with open(json_files[0], 'r', encoding='utf-8') as f:
#                         data_list = json.load(f) if json_files[0].stat().st_size < 10_000_000 else []
#                     for item in data_list[:sample_size]:
#                         payload = item if isinstance(item, dict) else {"document": item}
#                         features = analyze_payload(payload)
#                         features['target'] = 'mongo'
#                         self.data.append(features)
#                     logger.info("✅ Document (MongoDB) processed")
#                     return
#                 except Exception as e:
#                     logger.warning(f"JSON processing failed: {e}")
#         self._add_synthetic_document(sample_size)
    
#     def process_cache_like(self, sample_size=700):
#         path = self.download_kaggle_dataset("faheem113141/session-data")
#         if path:
#             csv_files = list(path.glob("**/*.csv"))
#             if csv_files:
#                 try:
#                     df = pd.read_csv(csv_files[0])
#                     for _, row in df.sample(min(sample_size, len(df))).iterrows():
#                         payload = {
#                             "session_id": str(row.get("session_id", f"sess_{np.random.randint(10000,99999)}")),
#                             "user_id": str(row.get("user_id", "U123")),
#                             "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#                             "expires": str(pd.Timestamp.now() + pd.Timedelta(hours=2)),
#                             "activity": row.to_dict()
#                         }
#                         features = analyze_payload(payload)
#                         features['target'] = 'redis'
#                         self.data.append(features)
#                     logger.info(f"✅ Real Cache/Session data processed")
#                     return
#                 except Exception as e:
#                     logger.warning(f"Cache data processing failed: {e}")
#         self._add_synthetic_cache(sample_size)
    
#     # Synthetic fallbacks
#     def _add_synthetic_transactional(self, n): 
#         logger.info("Using synthetic transactional data")
#         for _ in range(n):
#             self.data.append(analyze_payload({"order_id": 1001, "amount": 2500, "status": "completed"}))
#             self.data[-1]['target'] = 'postgres'
    
#     def _add_synthetic_time_series(self, n):
#         logger.info("Using synthetic time-series data")
#         for _ in range(n):
#             self.data.append(analyze_payload({"sensor_id": "S001", "temperature": 28.5, "timestamp": str(pd.Timestamp.now())}))
#             self.data[-1]['target'] = 'influxdb'
    
#     def _add_synthetic_graph(self, n): 
#         logger.info("Using synthetic graph data")
#         for _ in range(n):
#             self.data.append(analyze_payload({"nodes": [123, 456], "relationship": "FRIENDS"}))
#             self.data[-1]['target'] = 'neo4j'
    
#     def _add_synthetic_document(self, n):
#         logger.info("Using synthetic document data")
#         for _ in range(n):
#             self.data.append(analyze_payload({"user": {"id": 999, "address": {"city": "Lagos"}}}))
#             self.data[-1]['target'] = 'mongo'
    
#     def _add_synthetic_cache(self, n):
#         logger.info("Using synthetic cache data")
#         for _ in range(n):
#             self.data.append(analyze_payload({"session_id": "sess_12345", "expires": "2026-06-10"}))
#             self.data[-1]['target'] = 'redis'
    
#     def build_dataset(self):
#         df = pd.DataFrame(self.data)
#         df = df.fillna(0)
#         numeric_cols = ['scs', 'max_depth', 'transactional_score', 'cache_score',
#                        'relationship_score', 'time_series_score', 'schema_flexibility']
#         for col in numeric_cols:
#             if col in df.columns:
#                 df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
#         return df


# if __name__ == "__main__":
#     logger.info("🚀 Starting Automated Polyglot Data Collection Pipeline v2.0")
#     start_time = datetime.now()
    
#     collector = PolyglotDataCollector()
    
#     collector.process_transactional(800)
#     collector.process_time_series(700)
#     collector.process_graph(600)
#     collector.process_document(500)
#     collector.process_cache_like(700)
    
#     final_df = collector.build_dataset()
#     final_df.to_csv(collector.output_file, index=False)
    
#     elapsed = datetime.now() - start_time
#     logger.info(f"🎉 Pipeline Completed in {elapsed.seconds} seconds")
#     logger.info(f"Total samples: {len(final_df)}")
#     logger.info(f"Class distribution:\n{final_df['target'].value_counts()}")
#     logger.info(f"Versioned dataset saved: {collector.output_file}")



import pandas as pd
import numpy as np
import kagglehub
import requests
import json
import logging
from pathlib import Path
from datetime import datetime
from app.analysis.payload_analyzer import analyze_payload

# Optional: Hugging Face
try:
    from datasets import load_dataset
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    logging.warning("Hugging Face datasets library not installed. Install with: pip install datasets")

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s | %(levelname)s | %(message)s',
#     handlers=[logging.FileHandler("app/ai/data_collection.log"), logging.StreamHandler()]
# )

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("app/ai/data_collection.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PolyglotDataCollector:
    def __init__(self):
        self.data = []
        self.data_dir = Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.version = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"app/ai/real_training_data_{self.version}.csv"
        self.report_file = f"app/ai/data_collection_report_{self.version}.txt"
        self.failed = 0

    def get_local(self, keyword):
        files = list(self.raw_dir.glob(f"*{keyword}*")) + list(self.raw_dir.glob("*.csv")) + list(self.raw_dir.glob("*.json"))
        return files[0] if files else None

    def try_kaggle(self, slug, keyword):
        local = self.get_local(keyword)
        if local:
            logger.info(f"✅ Local: {local.name}")
            return local.parent
        try:
            logger.info(f"📥 Kaggle: {slug}")
            path = kagglehub.dataset_download(slug)
            return Path(path)
        except:
            return None

    def try_direct_url(self, url, filename, keyword):
        local = self.get_local(keyword)
        if local: return local.parent
        try:
            logger.info(f"📥 Direct: {filename}")
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                (self.raw_dir / filename).write_bytes(r.content)
                return self.raw_dir
        except:
            return None

    def try_huggingface(self, dataset_name, split="train", keyword="hf"):
        local = self.get_local(keyword)
        if local: return local.parent
        if not HF_AVAILABLE:
            return None
        try:
            logger.info(f"📥 Hugging Face: {dataset_name}")
            dataset = load_dataset(dataset_name, split=split)
            df = dataset.to_pandas()
            df.to_csv(self.raw_dir / f"{dataset_name.replace('/', '_')}.csv", index=False)
            logger.info(f"✅ HF dataset saved as CSV")
            return self.raw_dir
        except Exception as e:
            logger.warning(f"HF failed: {e}")
            return None

    # ==================== MULTI-PLATFORM PROCESSORS ====================

    def process_transactional(self, n=700):
        sources = [
            ("olistbr/brazilian-ecommerce", "brazilian"),                    # Kaggle
            ("https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx", "Online Retail.xlsx", "retail"),  # UCI
        ]
        for src in sources:
            if len(src) == 2:
                path = self.try_kaggle(src[0], src[1])
            else:
                path = self.try_direct_url(src[0], src[1], src[2])
            if path and list(path.glob("**/*.csv")):
                df = pd.read_csv(list(path.glob("**/*.csv"))[0])
                for _, row in df.sample(min(n, len(df))).iterrows():
                    features = analyze_payload(row.to_dict())
                    features['target'] = 'postgres'
                    self.data.append(features)
                logger.info("✅ Transactional data loaded")
                return
        self._synthetic_transactional(n)

    def process_time_series(self, n=600):
        sources = [
            ("ziya07/iot-integrated-predictive-maintenance-dataset", "iot"),   # Kaggle
            ("https://raw.githubusercontent.com/selva86/datasets/master/Raotbl6.csv", "Raotbl6.csv", "time"),  # GitHub
        ]
        for src in sources:
            if len(src) == 2:
                path = self.try_kaggle(src[0], src[1])
            else:
                path = self.try_direct_url(src[0], src[1], src[2])
            if path:
                csv_files = list(path.glob("**/*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                    for _, row in df.sample(min(n, len(df))).iterrows():
                        payload = {"sensor_id": "S001", "timestamp": str(pd.Timestamp.now()), **{k:v for k,v in row.to_dict().items() if isinstance(v,(int,float))}}
                        features = analyze_payload(payload)
                        features['target'] = 'influxdb'
                        self.data.append(features)
                    logger.info("✅ Time-Series data loaded")
                    return
        self._synthetic_time_series(n)

    # def process_graph(self, n=500):
    #     path = self.try_kaggle("wolfram77/graphs-social", "facebook")
    #     if path:
    #         edge_file = path / "facebook_combined.txt"
    #         if edge_file.exists():
    #             df = pd.read_csv(edge_file, sep=' ', header=None, names=['source', 'target'])
    #             for _, row in df.sample(min(n, len(df))).iterrows():
    #                 payload = {
    #                     "nodes": [int(row['source']), int(row['target'])],
    #                     "relationship": "FRIENDS",
    #                     "type": "social_connection",
    #                     "mutual_friends": np.random.randint(0, 20)
    #                 }
    #                 features = analyze_payload(payload)
    #                 features['target'] = 'neo4j'
    #                 self.data.append(features)
    #             logger.info("✅ Graph data loaded")
    #             return
    #     self._synthetic_graph(n)


    def process_graph(self, n=600):
        """Graph - Two sources"""
        path = self.try_kaggle("wolfram77/graphs-social", "facebook")
        if path:
            for file_name in ["facebook_combined.txt", "wiki-Vote.txt"]:
                edge_file = path / file_name
                if edge_file.exists():
                    df = pd.read_csv(edge_file, sep=' ', header=None, names=['source', 'target'])
                    for _, row in df.sample(min(n//2, len(df))).iterrows():
                        payload = {
                            "nodes": [int(row['source']), int(row['target'])],
                            "relationship": "FRIENDS",
                            "type": "social_connection",
                            "mutual_friends": np.random.randint(0, 20)
                        }
                        features = analyze_payload(payload)
                        features['target'] = 'neo4j'
                        self.data.append(features)
                    logger.info(f"✅ Graph data from {file_name}")
                    return
        self._synthetic_graph(n)

    def process_document(self, n=500):
        # Try Hugging Face first for rich JSON
        if HF_AVAILABLE:
            path = self.try_huggingface("mongo-db", "train", "mongo")
        if path:
            json_files = list(path.glob("**/*.json"))

            if json_files:
                with open(json_files[0], 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                try:
                    data = json.loads(content)
                    data_list = data if isinstance(data, list) else [data]

                except json.JSONDecodeError:
                    data_list = []
                    for line in content.splitlines():
                        line = line.strip()
                        if line:
                            try:
                                data_list.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue

                # ✅ FIX IS HERE (YOU WERE MISSING THIS LOOP)
                for item in data_list[:n]:
                    payload = item if isinstance(item, dict) else {"document": item}
                    features = analyze_payload(payload)
                    features['target'] = 'mongo'
                    self.data.append(features)

                logger.info("✅ Document data from Hugging Face")
                return
        # if HF_AVAILABLE:
        #     path = self.try_huggingface("mongo-db", "train", "mongo")
        #     if path:
        #         json_files = list(path.glob("**/*.json"))
        #         if json_files:
        #             with open(json_files[0], 'r', encoding='utf-8') as f:
        #             #     data_list = json.load(f) if isinstance(json.load(f), list) else [json.load(f)]
        #             # for item in data_list[:n]:
        #                 # with open(json_files[0], 'r', encoding='utf-8') as f:
        #                 #     data = json.load(f)
        #                 #     data_list = data if isinstance(data, list) else [data]
        #                 with open(json_files[0], 'r', encoding='utf-8') as f:
        #                     content = f.read().strip()

        #                 try:
        #                     # Case 1: normal JSON (dict or list)
        #                     data = json.loads(content)
        #                     data_list = data if isinstance(data, list) else [data]

        #                 except json.JSONDecodeError:
        #                     # Case 2: JSONL (line-by-line JSON)
        #                     data_list = []
        #                     for line in content.splitlines():
        #                         line = line.strip()
        #                         if line:
        #                             try:
        #                                 data_list.append(json.loads(line))
        #                             except json.JSONDecodeError:
        #                                 continue
        #                 payload = item if isinstance(item, dict) else {"document": item}
        #                 features = analyze_payload(payload)
        #                 features['target'] = 'mongo'
        #                 self.data.append(features)
        #             logger.info("✅ Document data from Hugging Face")
        #             return
        # # Fallback to Kaggle
        # path = self.try_kaggle("shrashtisinghal/mongo-db-datsets", "mongo")
        # if path:
        #     json_files = list(path.glob("**/*.json"))
        #     if json_files:
        #         with open(json_files[0], 'r', encoding='utf-8') as f:
        #             # data_list = json.load(f) if isinstance(json.load(f), list) else [json.load(f)]
        #             # data_list = [json.loads(line) for line in f]
        #             with open(json_files[0], 'r', encoding='utf-8') as f:
        #                 content = f.read().strip()
        #             try:
        #                 data_list = json.loads(content)
        #                 if isinstance(data_list, dict):
        #                     data_list = [data_list]
        #             except json.JSONDecodeError:
        #                 data_list = [json.loads(line) for line in content.splitlines() if line.strip()]
        #         for item in data_list[:n]:
        #             payload = item if isinstance(item, dict) else {"document": item}
        #             features = analyze_payload(payload)
        #             features['target'] = 'mongo'
        #             self.data.append(features)
        #         logger.info("✅ Document data from Kaggle")
        #         return
        # self._synthetic_document(n)

    # def process_cache_like(self, n=500):
    #     path = self.try_kaggle("faheem113141/session-data", "session")
    #     if path:
    #         csv_files = list(path.glob("**/*.csv"))
    #         if csv_files:
    #             df = pd.read_csv(csv_files[0])
    #             for _, row in df.sample(min(n, len(df))).iterrows():
    #                 payload = {"session_id": f"sess_{np.random.randint(10000,99999)}", "user_id": "U123", "expires": str(pd.Timestamp.now() + pd.Timedelta(hours=2))}
    #                 features = analyze_payload(payload)
    #                 features['target'] = 'redis'
    #                 self.data.append(features)
    #             logger.info("✅ Cache data loaded")
    #             return
    #     self._synthetic_cache(n)

    def process_cache_like(self, n=600):
        """Cache - Two sources"""
        path = self.try_kaggle("faheem113141/session-data", "session")
        if path:
            csv_files = list(path.glob("**/*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                for _, row in df.sample(min(n//2, len(df))).iterrows():
                    payload = {
                        "session_id": f"sess_{np.random.randint(10000,99999)}",
                        "user_id": "U123",
                        "expires": str(pd.Timestamp.now() + pd.Timedelta(hours=2)),
                        "activity_type": "login"
                    }
                    features = analyze_payload(payload)
                    features['target'] = 'redis'
                    self.data.append(features)
                logger.info("✅ Cache/Session data loaded")
                return
        self._synthetic_cache(n)


    # Synthetic fallbacks (unchanged)
    def _synthetic_transactional(self, n=300):
        for _ in range(n): self.data.append({**analyze_payload({"order_id": 1001, "amount": 2500}), 'target': 'postgres'})
    def _synthetic_time_series(self, n=300):
        for _ in range(n): self.data.append({**analyze_payload({"sensor_id": "S001", "temperature": 28.5}), 'target': 'influxdb'})
    def _synthetic_graph(self, n=300):
        for _ in range(n): self.data.append({**analyze_payload({"nodes": [123, 456], "relationship": "FRIENDS"}), 'target': 'neo4j'})
    def _synthetic_document(self, n=300):
        for _ in range(n): self.data.append({**analyze_payload({"user": {"id": 999, "address": {"city": "Lagos"}}}), 'target': 'mongo'})
    def _synthetic_cache(self, n=300):
        for _ in range(n): self.data.append({**analyze_payload({"session_id": "sess_12345"}), 'target': 'redis'})

    def build_dataset(self):
        df = pd.DataFrame(self.data).fillna(0)
        numeric_cols = ['scs', 'max_depth', 'transactional_score', 'cache_score', 'relationship_score', 'time_series_score', 'schema_flexibility']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df


if __name__ == "__main__":
    logger.info("Starting Multi-Platform Data Collection (Kaggle + UCI + GitHub + Hugging Face)")
    collector = PolyglotDataCollector()
    
    collector.process_transactional()
    collector.process_time_series()
    collector.process_graph()
    collector.process_document()
    collector.process_cache_like()
    
    final_df = collector.build_dataset()
    final_df.to_csv(collector.output_file, index=False)
    logger.info(f"Dataset ready: {len(final_df)} samples from diverse platforms")