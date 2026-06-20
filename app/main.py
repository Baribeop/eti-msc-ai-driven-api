# from fastapi import FastAPI, UploadFile, File, Header, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Any, List, Dict
# import json
# import pandas as pd

# from app.config import Config
# from app.analysis.payload_analyzer import analyze_payload
# from app.ai.predictor import MultiModelPredictor
#  # Correct import path
# from app.ai.train_model import MultiModelTrainer

# app = FastAPI(title="AI Polyglot Middleware v2.0", version="2.0")

# predictor = MultiModelPredictor()

# class Payload(BaseModel):
#     data: Any

# class QueryRequest(BaseModel):
#     database: str
#     query: Dict = {}

# @app.get("/")
# def home():
#     return {"message": "AI Polyglot Middleware v2.0", "active_model": predictor.current_model}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# @app.post("/analyze")
# def analyze(data: dict):
#     return {"features": analyze_payload(data)}

# @app.post("/predict")
# def predict(payload: dict, x_api_key: str = Header(None)):
#     if x_api_key != Config.API_KEY:
#         raise HTTPException(401, "Invalid API Key")
#     features = analyze_payload(payload)
#     return predictor.predict(features)

# @app.post("/predict/explain")
# def explain(payload: dict):
#     features = analyze_payload(payload)
#     return predictor.explain(features)

# @app.post("/predict/batch")
# def predict_batch(payloads: List[dict]):
#     return {"results": [predictor.predict(analyze_payload(p)) for p in payloads]}

# @app.post("/analyze/file")
# async def analyze_file(file: UploadFile = File(...)):
#     content = await file.read()
#     try:
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(pd.compat.StringIO(content.decode()))
#             sample = df.iloc[0].to_dict() if not df.empty else {}
#         elif file.filename.endswith('.json'):
#             sample = json.loads(content)
#         else:
#             sample = {"content": content.decode()[:800]}
#     except:
#         sample = {"raw": content.decode()[:500]}
#     return {"filename": file.filename, "features": analyze_payload(sample)}

# @app.get("/model/current")
# def current_model():
#     return predictor.get_current_model_info()

# @app.post("/model/switch")
# def switch_model(model_name: str):
#     success = predictor.switch_model(model_name)
#     return {"success": success, "active_model": predictor.current_model}

# # @app.post("/retrain")
# # def retrain():
# #     from app.ai.train_model import MultiModelTrainer
# #     trainer = MultiModelTrainer()
# #     metrics = trainer.train_all_models()
# #     return {"status": "success", "metrics": metrics}

# @app.post("/retrain")
# def retrain():
#     try:
#         trainer = MultiModelTrainer()
#         metrics = trainer.train_all_models()
#         return {"status": "success", "message": "All models retrained", "metrics": metrics}
#     except Exception as e:
#         logger.error(f"Retraining failed: {e}")
#         raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")

# @app.post("/query")
# def query_database(request: QueryRequest):
#     # Placeholder for actual query execution
#     return {"database": request.database, "result": "Query executed successfully (placeholder)"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




# from fastapi import FastAPI, UploadFile, File, Header, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Any, List, Dict
# import json
# import pandas as pd

# from app.config import Config
# from app.logging_config import setup_logging
# from app.analysis.payload_analyzer import analyze_payload
# from app.ai.predictor import MultiModelPredictor

# # Initialize global logging
# logger = setup_logging()
# tags_metadata = [
#     {
#         "name": "System",
#         "description": "System status, health checks, and API information."
#     },
#     {
#         "name": "Analysis",
#         "description": "Payload and file analysis services."
#     },
#     {
#         "name": "Prediction",
#         "description": "AI-powered database recommendation endpoints."
#     },
#     {
#         "name": "Explainability",
#         "description": "Explainable AI services."
#     },
#     {
#         "name": "Model Management",
#         "description": "Model monitoring, switching, and retraining."
#     },
#     {
#         "name": "Database Operations",
#         "description": "Database query and routing operations."
#     }
# ]
# app = FastAPI(title="AI Polyglot Middleware v2.0", version="2.0")

# predictor = MultiModelPredictor()

# class Payload(BaseModel):
#     data: Any

# class QueryRequest(BaseModel):
#     database: str
#     query: Dict = {}

# @app.get("/")
# def home():
#     return {"message": "AI Polyglot Middleware v2.0", "active_model": predictor.current_model}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# @app.post("/analyze")
# def analyze(data: dict):
#     return {"features": analyze_payload(data)}

# # @app.post("/predict")
# # def predict(payload: dict, x_api_key: str = Header(None)):
# #     if x_api_key != Config.API_KEY:
# #         raise HTTPException(401, "Invalid API Key")
# #     features = analyze_payload(payload)
# #     return predictor.predict(features)
# @app.post("/predict")
# def predict(payload: dict, x_api_key: str = Header(None)):
#     if x_api_key != Config.API_KEY:
#         raise HTTPException(401, "Invalid API Key")
#     try:
#         features = analyze_payload(payload)
#         return predictor.predict(features)
#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/predict/explain")
# def explain(payload: dict):
#     features = analyze_payload(payload)
#     return predictor.explain(features)

# @app.post("/predict/batch")
# def predict_batch(payloads: List[dict]):
#     return {"results": [predictor.predict(analyze_payload(p)) for p in payloads]}

# @app.post("/analyze/file")
# async def analyze_file(file: UploadFile = File(...)):
#     content = await file.read()
#     try:
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(pd.compat.StringIO(content.decode()))
#             sample = df.iloc[0].to_dict() if not df.empty else {}
#         elif file.filename.endswith('.json'):
#             sample = json.loads(content)
#         else:
#             sample = {"content": content.decode()[:800]}
#     except:
#         sample = {"raw": content.decode()[:500]}
#     return {"filename": file.filename, "features": analyze_payload(sample)}

# @app.get("/model/current")
# def current_model():
#     return predictor.get_current_model_info()

# @app.post("/model/switch")
# def switch_model(model_name: str):
#     success = predictor.switch_model(model_name)
#     return {"success": success, "active_model": predictor.current_model}

# @app.post("/retrain")
# def retrain():
#     try:
#         from app.ai.train_model import MultiModelTrainer
#         trainer = MultiModelTrainer()
#         metrics = trainer.train_all_models()
#         return {
#             "status": "success", 
#             "message": "All models retrained successfully",
#             "metrics": metrics
#         }
#     except Exception as e:
#         logger.error(f"Retraining failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/query")
# def query_database(request: QueryRequest):
#     return {"database": request.database, "result": "Query executed (placeholder)"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





# from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Depends
# from fastapi.responses import JSONResponse, RedirectResponse
# from pydantic import BaseModel
# from typing import Any, List, Dict
# import json
# import pandas as pd
# import os # Render: read PORT from env

# from app.config import Config
# from app.logging_config import setup_logging
# from app.analysis.payload_analyzer import analyze_payload
# from app.ai.predictor import MultiModelPredictor

# # Initialize global logging
# logger = setup_logging()

# tags_metadata = [
#     {"name": "System", "description": "System status, health checks, API configuration."},
#     {"name": "Analysis", "description": "Payload and file analysis services."},
#     {"name": "Prediction", "description": "AI-powered database recommendation endpoints. Requires API key."},
#     {"name": "Explainability", "description": "Explainable AI services."},
#     {"name": "Model Management", "description": "Model monitoring, switching, and retraining. Admin only."},
#     {"name": "Database Operations", "description": "Database query and routing operations."}
# ]

# async def verify_api_key(x_api_key: str = Header(None)):
#     if x_api_key!= Config.API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API Key")
#     return x_api_key

# app = FastAPI(
#     title="AI Polyglot Middleware API",
#     description="""
#     ## AI Polyglot Middleware v1.0

#     An API for automatic database selection using ML.
#     Supports: PostgreSQL, MongoDB, Redis, InfluxDB, Neo4j

#     ### Base URL
#     `https://your-service.onrender.com`

#     ### Authentication
#     `POST /predict`, `POST /model/switch`, `POST /retrain` require `x_api_key` header.
#     Set `API_KEY` in Render Environment Variables, then use it in Swagger "Authorize".

#     ### Quick Start
#     1. `POST /analyze` Extract features from payload
#     2. `POST /predict` Get recommended DB. Needs API key
#     3. `POST /query` Execute DB query. Placeholder

#     **Rate Limits**: 100 requests/min on free tier
#     **Docs**: [Interactive](/docs) | [Clean](/redoc)
#     """,
#     version="1.0", 
#     contact={"name": "API Support - MSc Thesis", "email": "support@polyglot.ai"},
#     license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json",
#     openapi_tags=tags_metadata
# )

# predictor = MultiModelPredictor()

# class Payload(BaseModel):
#     data: Any

# class BatchRequest(BaseModel):
#     payloads: List[Dict] = []

# class QueryRequest(BaseModel):
#     database: str
#     query: Dict = {}

# @app.get("/configuration", tags=["System"])
# def configuration():
#     """Get API configuration, supported DBs, and version info. TMDB-style."""
#     return {
#         "version": "1.0", # Changed
#         "supported_databases": ["PostgreSQL", "MongoDB", "Redis", "InfluxDB", "Neo4j"],
#         "rate_limit": "100/min",
#         "authentication": {"required_for": ["POST /predict", "POST /model/switch", "POST /retrain"]}
#     }

# @app.get("/", tags=["System"], include_in_schema=False)
# def home():
#     # Auto-load docs when app starts / root is hit
#     return RedirectResponse(url="/docs")

# @app.get("/health", tags=["System"])
# def health():
#     return {"status": "healthy"}

# @app.post("/analyze", tags=["Analysis"])
# def analyze(data: dict):
#     return {"features": analyze_payload(data)}

# @app.post("/predict", tags=["Prediction"], dependencies=[Depends(verify_api_key)])
# def predict(payload: dict, x_api_key: str = Header(None)):
#     if x_api_key!= Config.API_KEY:
#         raise HTTPException(401, "Invalid API Key")
#     try:
#         features = analyze_payload(payload)
#         return predictor.predict(features)
#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/predict/explain", tags=["Explainability"])
# def explain(payload: dict):
#     features = analyze_payload(payload)
#     return predictor.explain(features)

# # @app.post("/predict/batch", tags=["Prediction"])
# # def predict_batch(payloads: List):
# #     return {"results": [predictor.predict(analyze_payload(p)) for p in payloads]}

# # @app.post("/predict/batch", tags=["Prediction"])
# # def predict_batch(payloads: List[dict]):
# #     return {"results": [predictor.predict(analyze_payload(p)) for p in payloads]}

# @app.post("/predict/batch")
# async def predict_batch(
#     payloads: List[Dict] = None,           # For raw array: []
#     batch: BatchRequest = None,            # For wrapped: {"payloads": [...]}
#     x_api_key: str = Header(None)
# ):
#     """Single Batch Prediction Endpoint
#     Supports BOTH formats:
#     1. Raw JSON Array: [ {payload1}, {payload2} ]
#     2. Wrapped: { "payloads": [ {payload1}, {payload2} ] }
#     """
#     if x_api_key != Config.API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API Key")

#     # Determine which format was used
#     if batch and batch.payloads:
#         payload_list = batch.payloads
#     elif payloads:
#         payload_list = payloads
#     else:
#         raise HTTPException(status_code=400, detail="No payloads provided. Send either a JSON array or {'payloads': [...]}")

#     if not payload_list:
#         raise HTTPException(status_code=400, detail="Payload list is empty")

#     results = []
#     for p in payload_list:
#         try:
#             features = analyze_payload(p)
#             result = predictor.predict(features)
#             results.append(result)
#         except Exception as e:
#             logger.error(f"Batch item failed: {e}")
#             results.append({
#                 "error": str(e),
#                 "payload": p
#             })

#     return {
#         "results": results,
#         "total": len(results),
#         "model_used": predictor.current_model,
#         "successful": sum(1 for r in results if "error" not in r)
#     }

# @app.get("/model/current", tags=["Model Management"])
# def current_model():
#     return predictor.get_current_model_info()

# @app.post("/model/switch", tags=["Model Management"], dependencies=[Depends(verify_api_key)])
# def switch_model(model_name: str):
#     success = predictor.switch_model(model_name)
#     return {"success": success, "active_model": predictor.current_model}

# @app.post("/retrain", tags=["Model Management"], dependencies=[Depends(verify_api_key)])
# def retrain():
#     try:
#         from app.ai.train_model import MultiModelTrainer
#         trainer = MultiModelTrainer()
#         metrics = trainer.train_all_models()
#         return {"status": "success", "message": "All models retrained successfully", "metrics": metrics}
#     except Exception as e:
#         logger.error(f"Retraining failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/query", tags=["Database Operations"])
# def query_database(request: QueryRequest):
#     return {"database": request.database, "result": "Query executed (placeholder)"}

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)



# # app/main.py
# from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Depends, Security, Body
# from fastapi.responses import RedirectResponse
# from fastapi.security import APIKeyHeader
# from pydantic import BaseModel
# from typing import Any, List, Dict
# import json
# import pandas as pd
# import os

# from io import StringIO

# from metrics.history import (
#     initialize_history_db,
#     log_prediction
# )
# import sqlite3
# from app.config import Config
# from app.logging_config import setup_logging
# from app.analysis.payload_analyzer import analyze_payload
# from app.ai.predictor import MultiModelPredictor

# # ====================== LOGGING & APP SETUP ======================
# logger = setup_logging()

# tags_metadata = [
#     {"name": "System", "description": "System status, health checks, API configuration."},
#     {"name": "Analysis", "description": "Payload and file analysis services."},
#     {"name": "Prediction", "description": "AI-powered database recommendation endpoints. Requires API key."},
#     {"name": "Explainability", "description": "Explainable AI services."},
#     {"name": "Model Management", "description": "Model monitoring, switching, and retraining."},
#     {"name": "Database Operations", "description": "Database query and routing operations."}
# ]

# # ====================== SECURITY SETUP (for Swagger) ======================
# api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# async def get_api_key(api_key: str = Security(api_key_header)):
#     if api_key == Config.API_KEY:
#         return api_key
#     raise HTTPException(
#         status_code=401,
#         detail="Invalid API Key"
#     )

# app = FastAPI(
#      title="AI Polyglot Middleware API",
#     description="""
#     ## AI Polyglot Middleware v1.0

#     An API for automatic database selection using ML.
#     Supports: PostgreSQL, MongoDB, Redis, InfluxDB, Neo4j

#     ### Base URL
#     `https://your-service.onrender.com`

#     ### Authentication
#     `POST /predict`, `POST /model/switch`, `POST /retrain` require `x_api_key` header.
#     Set `API_KEY` in Render Environment Variables, then use it in Swagger "Authorize".

#     ### Quick Start
#     1. `POST /analyze` Extract features from payload
#     2. `POST /predict` Get recommended DB. Needs API key
#     3. `POST /query` Execute DB query. Placeholder

#     **Rate Limits**: 100 requests/min on free tier
#     **Docs**: [Interactive](/docs) | [Clean](/redoc)
#     """,
#     version="1.0", 
#     contact={"name": "API Support - MSc Thesis", "email": "support@polyglot.ai"},
#     license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json",
#     openapi_tags=tags_metadata
# )

# # Initialize Predictor
# predictor = MultiModelPredictor()


# initialize_history_db()

# # ====================== PYDANTIC MODELS ======================
# class BatchRequest(BaseModel):
#     payloads: List[Dict] = []

# class QueryRequest(BaseModel):
#     database: str
#     query: Dict = {}

# # ====================== ENDPOINTS ======================

# @app.get("/", tags=["System"], include_in_schema=False)
# def home():
#     return RedirectResponse(url="/docs")

# # @app.get("/health", tags=["System"])
# # def health():
# #     return {"status": "healthy"}

# @app.get("/health", tags=["System"])
# def health():
#     return {
#         "status": "healthy",
#         "model": predictor.current_model,
#         "available_models": len(
#             predictor.models
#         )
#     }

# @app.get("/configuration", tags=["System"])
# def configuration():
#     return {
#         "version": "1.0",
#         "supported_databases": ["PostgreSQL", "MongoDB", "Redis", "InfluxDB", "Neo4j"],
#         "authentication": "x-api-key header required for prediction endpoints"
#     }


# @app.get("/history", tags=["System"])
# def get_prediction_history():

#     conn = sqlite3.connect("data/prediction_history.db")
#     conn.row_factory = sqlite3.Row

#     rows = conn.execute("""
#         SELECT *
#         FROM prediction_history
#         ORDER BY id DESC
#         LIMIT 100
#     """).fetchall()

#     conn.close()

#     return [dict(row) for row in rows]

# @app.post("/analyze", tags=["Analysis"])
# def analyze(data: dict):
#     return {"features": analyze_payload(data)}

# @app.get("/history/stats", tags=["System"])
# def prediction_stats():

#     conn = sqlite3.connect("data/prediction_history.db")

#     total = conn.execute("""
#         SELECT COUNT(*)
#         FROM prediction_history
#     """).fetchone()[0]

#     avg_confidence = conn.execute("""
#         SELECT AVG(confidence)
#         FROM prediction_history
#     """).fetchone()[0]

#     db_distribution = conn.execute("""
#         SELECT database_name, COUNT(*)
#         FROM prediction_history
#         GROUP BY database_name
#     """).fetchall()

#     conn.close()

#     return {
#         "total_predictions": total,
#         "average_confidence": round(avg_confidence or 0, 4),
#         "database_distribution": [
#             {
#                 "database": row[0],
#                 "count": row[1]
#             }
#             for row in db_distribution
#         ]
#     }
# # @app.post("/predict", tags=["Prediction"], dependencies=[Depends(get_api_key)])
# # def predict(payload: dict):
# #     try:
# #         features = analyze_payload(payload)
# #         return predictor.predict(features)
# #     except Exception as e:
# #         logger.error(f"Prediction error: {e}")
# #         raise HTTPException(status_code=500, detail=str(e))

# @app.post(
#     "/predict",
#     tags=["Prediction"],
#     dependencies=[Depends(get_api_key)]
# )
# def predict(payload: dict):

#     try:

#         features = analyze_payload(
#             payload
#         )

#         prediction = predictor.predict(
#             features
#         )

#         if (
#             isinstance(prediction, dict)
#             and "database" in prediction
#         ):

#             log_prediction(
#                 prediction["database"],
#                 prediction.get(
#                     "confidence",
#                     0
#                 ),
#                 prediction.get(
#                     "model_used",
#                     predictor.current_model
#                 )
#             )

#         return prediction

#     except Exception as e:

#         logger.exception(
#             "Prediction error"
#         )

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )



# @app.post(
#     "/route",
#     tags=["Database Operations"],
#     dependencies=[Depends(get_api_key)]
# )
# def route_payload(
#         payload: dict
# ):

#     features = analyze_payload(
#         payload
#     )

#     prediction = predictor.predict(
#         features
#     )

#     return {

#         "routing_decision":
#             prediction.get(
#                 "database"
#             ),

#         "confidence":
#             prediction.get(
#                 "confidence"
#             ),

#         "model_used":
#             prediction.get(
#                 "model_used"
#             ),

#         "features":
#             features
#     }
# # @app.post("/predict/batch", tags=["Prediction"], dependencies=[Depends(get_api_key)])
# # async def predict_batch(
# #     payloads: List[Dict] = None,      # Raw JSON array support
# #     batch: BatchRequest = None,       # Wrapped {"payloads": [...]} support
# # ):
# #     """Combined Batch Prediction - Supports BOTH input formats"""
# #     # Determine input format
# #     if batch and batch.payloads:
# #         payload_list = batch.payloads
# #     elif payloads:
# #         payload_list = payloads
# #     else:
# #         raise HTTPException(status_code=400, detail="No payloads provided")

# #     if not payload_list:
# #         raise HTTPException(status_code=400, detail="Payload list is empty")

# #     results = []
# #     for p in payload_list:
# #         try:
# #             features = analyze_payload(p)
# #             result = predictor.predict(features)
# #             results.append(result)
# #         except Exception as e:
# #             logger.error(f"Batch item failed: {e}")
# #             results.append({"error": str(e), "payload": p})

# #     return {
# #         "results": results,
# #         "total": len(results),
# #         "model_used": predictor.current_model,
# #         "successful": sum(1 for r in results if "error" not in r)
# #     }



# @app.post("/predict/batch", tags=["Prediction"], dependencies=[Depends(get_api_key)])
# async def predict_batch(
#     request_data: Any = Body(...)
# ):
#     """Smart Batch Endpoint - Accepts raw array OR wrapped object"""
    
#     # Handle different input formats
#     if isinstance(request_data, list):
#         payload_list = request_data
#     elif isinstance(request_data, dict):
#         # Support both "payloads" and direct dict
#         payload_list = request_data.get("payloads") or request_data.get("data") or [request_data]
#     else:
#         raise HTTPException(status_code=400, detail="Invalid format. Send JSON array or {'payloads': [...]}")

#     if not isinstance(payload_list, list) or len(payload_list) == 0:
#         raise HTTPException(status_code=400, detail="No valid payloads provided")

#     results = []
#     for p in payload_list:
#         try:
#             if not isinstance(p, dict):
#                 p = {"data": p}
#             features = analyze_payload(p)
#             result = predictor.predict(features)
#             results.append(result)
#         except Exception as e:
#             logger.error(f"Batch item failed: {e}")
#             results.append({"error": str(e), "payload": p})

#     return {
#         "results": results,
#         "total": len(results),
#         "model_used": predictor.current_model,
#         "successful": sum(1 for r in results if "error" not in r)
#     }

# # @app.post("/predict/explain", tags=["Explainability"])
# @app.post(
#     "/predict/explain",
#     tags=["Explainability"],
#     dependencies=[Depends(get_api_key)]
# )
# def explain(payload: dict):
#     features = analyze_payload(payload)
#     return predictor.explain(features)

# # @app.post("/analyze/file", tags=["Analysis"])
# @app.post(
#     "/analyze/file",
#     tags=["Analysis"],
#     dependencies=[Depends(get_api_key)]
# )
# async def analyze_file(file: UploadFile = File(...)):
#     content = await file.read()
#     if len(content) > Config.MAX_FILE_SIZE:

#         raise HTTPException(
#             status_code=413,
#             detail="File too large"
#         )
#     try:
#         if file.filename.endswith('.json'):
#             sample = json.loads(content)
#         # elif file.filename.endswith('.csv'):
#         #     df = pd.read_csv(pd.compat.StringIO(content.decode()))
#         #     sample = df.iloc[0].to_dict() if not df.empty else {}
#         elif file.filename.endswith('.csv'):

#             df = pd.read_csv(
#                 StringIO(
#                     content.decode(
#                         errors="ignore"
#                     )
#                 )
#             )

#             sample = (
#                 df.head(5)
#                 .to_dict(
#                     orient="records"
#                 )
#             )

#             file_analysis = {

#                 "rows": len(df),

#                 "columns": len(df.columns),

#                 "column_names":
#                     list(df.columns),

#                 "numeric_columns":
#                     len(
#                         df.select_dtypes(
#                             include=["number"]
#                         ).columns
#                     ),

#                 "text_columns":
#                     len(
#                         df.select_dtypes(
#                             include=["object"]
#                         ).columns
#                     )
#             }
#         else:
#             sample = {"content": content.decode()[:800]}
#     except:
#         sample = {"raw": content.decode()[:500]}
    
#     # return {"filename": file.filename, "features": analyze_payload(sample)}

#     payload_features = (
#     analyze_payload(sample)
# )

#     return {
#         "filename": file.filename,
#         "file_analysis":
#             locals().get(
#                 "file_analysis",
#                 {}
#             ),
#         "features":
#             payload_features
#     }
# @app.get("/model/current", tags=["Model Management"])
# def current_model():
#     return predictor.get_current_model_info()

# @app.post("/model/switch", tags=["Model Management"], dependencies=[Depends(get_api_key)])
# def switch_model(model_name: str):
#     success = predictor.switch_model(model_name)
#     return {"success": success, "active_model": predictor.current_model}

# @app.post("/retrain", tags=["Model Management"], dependencies=[Depends(get_api_key)])
# def retrain():
#     try:
#         from app.ai.train_model import MultiModelTrainer
#         trainer = MultiModelTrainer()
#         metrics = trainer.train_all_models()
#         return {
#             "status": "success",
#             "message": "All models retrained successfully",
#             "metrics": metrics
#         }
#     except Exception as e:
#         logger.error(f"Retraining failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/query", tags=["Database Operations"])
# def query_database(request: QueryRequest):
#     return {"database": request.database, "result": "Query executed (placeholder)"}

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)




# app/main.py
from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Depends, Security, Body
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Any, List, Dict
import json
import pandas as pd
import os
import traceback

from io import StringIO

from metrics.history import (
    initialize_history_db,
    log_prediction
)
import sqlite3
from app.config import Config
from app.logging_config import setup_logging
from app.analysis.payload_analyzer import analyze_payload
from app.ai.predictor import MultiModelPredictor

# ====================== LOGGING & APP SETUP ======================
logger = setup_logging()

tags_metadata = [
    {"name": "System", "description": "System status, health checks, API configuration."},
    {"name": "Analysis", "description": "Payload and file analysis services."},
    {"name": "Prediction", "description": "AI-powered database recommendation endpoints."},
    {"name": "Persistence", "description": "Persist data to recommended or specified database."},
    {"name": "Explainability", "description": "Explainable AI services."},
    {"name": "Model Management", "description": "Model monitoring, switching, and retraining."},
    {"name": "Database Operations", "description": "Database query and routing operations."}
]

# ====================== SECURITY SETUP ======================
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == Config.API_KEY:
        return api_key
    raise HTTPException(status_code=401, detail="Invalid API Key")

app = FastAPI(
    title="AI Polyglot Middleware API",
    description="""
    ## AI Polyglot Middleware v1.0

    An API for automatic database selection using ML.
    Supports: PostgreSQL, MongoDB, Redis, InfluxDB, Neo4j

    ### Base URL
    `https://eti-msc-ai-driven-api.onrender.com/docs`

    ### Authentication
    `POST /predict`, `POST /model/switch`, `POST /retrain` require `x_api_key` header.
   

    ### Quick Start
    1. `POST /analyze` Extract features from payload
    2. `POST /predict` Get recommended DB. Needs API key
    3. `POST /query` Execute DB query. Placeholder

    **Rate Limits**: 100 requests/min on free tier
    **Docs**: [Interactive](/docs) | [Clean](/redoc)
    """,
    version="1.0", 
    contact={"name": "API Support - MSc Thesis", "email": "support@polyglot.ai"},
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata
)

# Initialize Predictor
predictor = MultiModelPredictor()

initialize_history_db()

# ====================== PYDANTIC MODELS ======================
class PersistRequest(BaseModel):
    data: Any
    database: str = None                    # Optional - uses AI recommendation if omitted
    connection: Dict = None                 # Required for persistence

class BatchRequest(BaseModel):
    payloads: List[Dict] = []

class QueryRequest(BaseModel):
    database: str
    query: Dict = {}

# ====================== ENDPOINTS ======================

@app.get("/", tags=["System"], include_in_schema=False)
def home():
    return RedirectResponse(url="https://eti-msc-ai-driven-api.onrender.com/docs")

@app.get("/health", tags=["System"])
def health():
    try:
        return {
            "status": "healthy",
            "model": predictor.current_model,
            "available_models": len(predictor.models)
        }
    except Exception as e:
        logger.error(f"Health check failed: {traceback.format_exc()}")
        return {"status": "degraded"}

@app.get("/configuration", tags=["System"])
def configuration():
    return {
        "version": "1.0",
        "supported_databases": ["PostgreSQL", "MongoDB", "Redis", "InfluxDB", "Neo4j"],
        "authentication": "x-api-key header required for protected endpoints"
    }

@app.get("/history", tags=["System"])
def get_prediction_history():
    try:
        conn = sqlite3.connect("data/prediction_history.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM prediction_history ORDER BY id DESC LIMIT 100").fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"History fetch failed: {traceback.format_exc()}")
        raise HTTPException(500, "Failed to fetch history")

@app.post("/analyze", tags=["Analysis"])
def analyze(data: dict):
    try:
        return {"features": analyze_payload(data)}
    except Exception as e:
        logger.error(f"Analyze error: {traceback.format_exc()}")
        raise HTTPException(500, "Failed to analyze payload")

@app.post("/predict", tags=["Prediction"], dependencies=[Depends(get_api_key)])
def predict(payload: dict):
    try:
        features = analyze_payload(payload)
        prediction = predictor.predict(features)

        if isinstance(prediction, dict) and "database" in prediction:
            log_prediction(
                prediction["database"],
                prediction.get("confidence", 0),
                prediction.get("model_used", predictor.current_model)
            )
        return prediction
    except Exception as e:
        logger.error(f"Prediction error: {traceback.format_exc()}")
        raise HTTPException(500, "Prediction failed")

@app.post("/persist", tags=["Persistence"], dependencies=[Depends(get_api_key)])
def persist_data(request: PersistRequest):
    """Persist data to recommended or specified database"""
    try:
        if not request.data:
            raise HTTPException(400, "Missing 'data' field")

        # Determine target database
        target_db = request.database
        if not target_db:
            features = analyze_payload(request.data)
            decision = predictor.predict(features)
            target_db = decision["database"]

        # Validate connection
        if not request.connection or not request.connection.get("type"):
            raise HTTPException(400, "Connection details are required for persistence")

        conn_type = request.connection["type"].lower()

        # Select adapter
        if conn_type == "postgres":
            from app.adapters.postgres_adapter import PostgresAdapter
            adapter = PostgresAdapter()
        elif conn_type == "mongo":
            from app.adapters.mongo_adapter import MongoAdapter
            adapter = MongoAdapter()
        elif conn_type == "redis":
            from app.adapters.redis_adapter import RedisAdapter
            adapter = RedisAdapter()
        elif conn_type == "influxdb":
            from app.adapters.influx_adapter import InfluxAdapter
            adapter = InfluxAdapter()
        elif conn_type == "neo4j":
            from app.adapters.neo4j_adapter import Neo4jAdapter
            adapter = Neo4jAdapter()
        else:
            raise HTTPException(400, f"Unsupported database type: {conn_type}")

        # Persist data
        result = adapter.insert(request.data)

        return {
            "success": True,
            "database": target_db,
            "record_id": result.get("id"),
            "strategy_used": result.get("strategy", "insert"),
            "message": f"Data successfully persisted in {target_db}"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Persistence failed for {target_db if 'target_db' in locals() else 'unknown'}: {traceback.format_exc()}")
        raise HTTPException(500, f"Failed to persist data: {str(e)}")

@app.post("/route", tags=["Database Operations"], dependencies=[Depends(get_api_key)])
def route_payload(payload: dict):
    try:
        features = analyze_payload(payload)
        prediction = predictor.predict(features)
        return {
            "routing_decision": prediction.get("database"),
            "confidence": prediction.get("confidence"),
            "model_used": prediction.get("model_used"),
            "features": features
        }
    except Exception as e:
        logger.error(f"Route error: {traceback.format_exc()}")
        raise HTTPException(500, "Routing failed")

@app.post("/predict/batch", tags=["Prediction"], dependencies=[Depends(get_api_key)])
async def predict_batch(request_data: Any = Body(...)):
    try:
        if isinstance(request_data, list):
            payload_list = request_data
        elif isinstance(request_data, dict):
            payload_list = request_data.get("payloads") or request_data.get("data") or [request_data]
        else:
            raise HTTPException(400, "Invalid format")

        if not isinstance(payload_list, list) or len(payload_list) == 0:
            raise HTTPException(400, "No valid payloads provided")

        results = []
        for p in payload_list:
            try:
                if not isinstance(p, dict):
                    p = {"data": p}
                features = analyze_payload(p)
                result = predictor.predict(features)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch item failed: {e}")
                results.append({"error": str(e), "payload": p})

        return {
            "results": results,
            "total": len(results),
            "model_used": predictor.current_model,
            "successful": sum(1 for r in results if "error" not in r)
        }
    except Exception as e:
        logger.error(f"Batch prediction failed: {traceback.format_exc()}")
        raise HTTPException(500, "Batch processing failed")

@app.post("/predict/explain", tags=["Explainability"], dependencies=[Depends(get_api_key)])
def explain(payload: dict):
    try:
        features = analyze_payload(payload)
        return predictor.explain(features)
    except Exception as e:
        logger.error(f"Explain error: {traceback.format_exc()}")
        raise HTTPException(500, "Failed to generate explanation")

@app.post("/analyze/file", tags=["Analysis"], dependencies=[Depends(get_api_key)])
async def analyze_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if len(content) > getattr(Config, 'MAX_FILE_SIZE', 10 * 1024 * 1024):
            raise HTTPException(413, "File too large")

        if file.filename.endswith('.json'):
            sample = json.loads(content)
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(StringIO(content.decode(errors="ignore")))
            sample = df.head(5).to_dict(orient="records")
            file_analysis = {"rows": len(df), "columns": len(df.columns)}
        else:
            sample = {"content": content.decode()[:800]}

        return {
            "filename": file.filename,
            "file_analysis": locals().get("file_analysis", {}),
            "features": analyze_payload(sample)
        }
    except Exception as e:
        logger.error(f"File analysis error: {traceback.format_exc()}")
        raise HTTPException(500, f"File analysis failed: {str(e)}")

@app.get("/model/current", tags=["Model Management"])
def current_model():
    try:
        return predictor.get_current_model_info()
    except Exception as e:
        logger.error(f"Model info error: {e}")
        raise HTTPException(500, "Failed to retrieve model information")

@app.post("/model/switch", tags=["Model Management"], dependencies=[Depends(get_api_key)])
def switch_model(model_name: str):
    try:
        success = predictor.switch_model(model_name)
        return {"success": success, "active_model": predictor.current_model}
    
    except Exception as e:
        logger.error(f"Model switch error: {traceback.format_exc()}")
        raise HTTPException(500, "Failed to switch model")

@app.post("/retrain", tags=["Model Management"], dependencies=[Depends(get_api_key)])
def retrain():
    try:
        from app.ai.train_model import MultiModelTrainer
        trainer = MultiModelTrainer()
        metrics = trainer.train_all_models()
        return {
            "status": "success",
            "message": "All models retrained successfully",
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Retraining failed: {traceback.format_exc()}")
        raise HTTPException(500, "Retraining failed")

@app.post("/query", tags=["Database Operations"])
def query_database(request: QueryRequest):
    try:
        return {"database": request.database, "result": "Query executed (placeholder)"}
    except Exception as e:
        logger.error(f"Query error: {traceback.format_exc()}")
        raise HTTPException(500, "Query execution failed")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)