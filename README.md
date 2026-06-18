# AI Polyglot Middleware API

> TMDB-style REST API for automatic database selection using ML
> Supports: PostgreSQL, MongoDB, Redis, InfluxDB, Neo4j

**Live Docs**: https://your-service.onrender.com
**Base URL**: `https://your-service.onrender.com`
**Version**: 1.0
**License**: MIT

---

## 1. Overview

The AI Polyglot Middleware analyzes your dataset and automatically recommends the optimal database: PostgreSQL, MongoDB, Redis, InfluxDB, or Neo4j. It also provides endpoints to provision, write, and query data.

**Key Features**
1. Rule-based + ML ensemble prediction
2. Explainable AI: feature importance
3. Batch prediction
4. File upload: CSV, JSON, JSONL, XLSX, Parquet
5. Model switching + retraining

---


## 2. Authentication

Most prediction endpoints require an API key.

**Header**: `x_api_key: YOUR_API_KEY`

Set `API_KEY` in Render Environment Variables.
In Swagger UI: Click `Authorize` -> Enter your key -> `Authorize`

Protected endpoints:
`POST /predict`, `POST /model/switch`, `POST /retrain`

---

## 3. Rate Limits

Free tier: `100 requests/min`
Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

## 4. Endpoints

### System
| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/` | Redirects to `/docs` | No |
| `GET` | `/health` | Health check | No |
| `GET` | `/configuration` | API config, supported DBs | No |

### Analysis
| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/analyze` | Extract features from JSON payload | No |
| `POST` | `/analyze/file` | Upload CSV/JSON file, extract features from row 1 | No |

### Prediction
| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/predict` | Get recommended DB for payload | Yes |
| `POST` | `/predict/batch` | Batch prediction for list of payloads | No |
| `POST` | `/predict/explain` | Explain model decision with feature importance | No |

### Model Management
| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/model/current` | Get active model info | No |
| `POST` | `/model/switch` | Switch active model. `model_name: str` | Yes |
| `POST` | `/retrain` | Retrain all models from local/synthetic data | Yes |

### Database Operations
| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/query` | Execute query. Placeholder | No |

---

## 5. Request/Response Examples

### `POST /analyze`
**Request**
```json
{
  "rows": 50000,
  "cols": 12,
  "has_timestamp": true,
  "has_geo": false,
  "sparsity": 0.1
}


