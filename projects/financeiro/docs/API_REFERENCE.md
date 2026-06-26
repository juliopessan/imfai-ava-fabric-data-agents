# 📡 Referência de APIs

> Especificação completa de endpoints, payloads, autenticação e exemplos.

---

## 📑 Índice

1. [Autenticação](#autenticação)
2. [Base API & Versionamento](#base-api--versionamento)
3. [Endpoints](#endpoints)
4. [Modelos de Dados](#modelos-de-dados)
5. [Exemplos](#exemplos)
6. [Rate Limiting & Quotas](#rate-limiting--quotas)

---

## Autenticação

### OAuth 2.0 (Client Credentials)

**Endpoint:** `POST /auth/token`

```bash
curl -X POST https://api.avanade.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "scope": "api://avanade/migration.read migration.write"
  }'

# Response (200 OK):
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "api://avanade/migration.read migration.write"
}
```

### API Key (Legacy)

```bash
# All requests include API key header
curl https://api.avanade.com/v1/jobs \
  -H "X-API-Key: your-api-key-here"
```

---

## Base API & Versionamento

**Base URL:** `https://api.avanade.com`

**Versão Current:** `v1`

**Headers Obrigatórios:**
```
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
User-Agent: MigrationClient/1.0
X-Request-ID: {uuid}  # para tracing
```

---

## Endpoints

### 1. Connectors

#### Register Connector

```
POST /v1/connectors
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "name": "Financeiro-connector-001",
  "tenant_id": "Financeiro-001",
  "description": "Clouderea → Databricks migration",
  "data_sources": [
    {
      "type": "hive",
      "host": "cloudera.internal",
      "port": 10000,
      "database": "raw_data"
    },
    {
      "type": "mssql",
      "host": "db.internal",
      "port": 1433,
      "database": "erp_prod"
    }
  ],
  "pattern": "push",  # push | pull | private_link
  "tags": {
    "environment": "production",
    "team": "data-platform"
  }
}

Response (201 Created):
{
  "id": "c-Financeiro-001",
  "name": "Financeiro-connector-001",
  "status": "registered",
  "license_key": "lic-XXXXX-XXXXX",
  "license_expiry": "2027-06-12T00:00:00Z",
  "created_at": "2026-06-12T10:30:00Z",
  "download_url": "https://cdn.avanade.com/connector-agent/1.0.0/connector-agent-1.0.0.whl?token=xyz"
}
```

#### List Connectors

```
GET /v1/connectors?tenant_id=Financeiro-001&status=active

Response (200 OK):
{
  "connectors": [
    {
      "id": "c-Financeiro-001",
      "name": "Financeiro-connector-001",
      "status": "registered",
      "pattern": "push",
      "created_at": "2026-06-12T10:30:00Z",
      "last_activity": "2026-06-12T15:45:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 50
}
```

#### Get Connector Details

```
GET /v1/connectors/c-Financeiro-001

Response (200 OK):
{
  "id": "c-Financeiro-001",
  "name": "Financeiro-connector-001",
  "tenant_id": "Financeiro-001",
  "status": "registered",
  "pattern": "push",
  "data_sources": [
    {
      "id": "ds-hive-01",
      "type": "hive",
      "host": "cloudera.internal",
      "port": 10000,
      "database": "raw_data",
      "tables": 127,
      "last_sync": "2026-06-12T15:45:00Z"
    }
  ],
  "license": {
    "key": "lic-XXXXX-XXXXX",
    "status": "active",
    "expiry": "2027-06-12T00:00:00Z"
  }
}
```

### 2. SAS Tokens (Padrão A - Push)

#### Request SAS Token

```
POST /v1/connectors/{connector_id}/sas-token
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "validity_hours": 24,
  "max_uploads": 100,
  "max_size_mb": 500000,
  "data_sources": ["ds-hive-01", "ds-sql-01"]
}

Response (200 OK):
{
  "sas_url": "https://avanadeadls.blob.core.windows.net/landing/Financeiro-001/run-20260612-001?sv=2021-06-08&ss=b&srt=sco&sp=rwdlacx&se=2026-06-13T12:00:00Z&st=2026-06-12T12:00:00Z&spr=https&sig=...",
  "upload_path": "landing/Financeiro-001/run-20260612-001/",
  "expiration": "2026-06-13T12:00:00Z",
  "max_size_mb": 500000,
  "max_uploads": 100
}
```

#### Revoke SAS Token

```
DELETE /v1/connectors/{connector_id}/sas-token/{token_id}
Authorization: Bearer {token}

Response (204 No Content):
```

### 3. Jobs

#### Create Job

```
POST /v1/jobs
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "connector_id": "c-Financeiro-001",
  "data_sources": ["ds-hive-01", "ds-sql-01"],
  "job_type": "full_migration",  # full_migration | incremental | discovery
  "config": {
    "sample_size": 100000,
    "validate": true,
    "transform_rules": true
  },
  "tags": {
    "wave": "1",
    "priority": "high"
  }
}

Response (201 Created):
{
  "id": "job-20260612-001",
  "connector_id": "c-Financeiro-001",
  "status": "queued",
  "job_type": "full_migration",
  "created_at": "2026-06-12T12:00:00Z",
  "estimated_duration_minutes": 180
}
```

#### Get Job Status

```
GET /v1/jobs/job-20260612-001?include=metrics,events

Response (200 OK):
{
  "id": "job-20260612-001",
  "connector_id": "c-Financeiro-001",
  "status": "running",  # queued | running | completed | failed
  "stages": [
    {
      "name": "discovery",
      "status": "completed",
      "started_at": "2026-06-12T12:00:00Z",
      "completed_at": "2026-06-12T12:15:00Z",
      "duration_seconds": 900
    },
    {
      "name": "validation",
      "status": "running",
      "started_at": "2026-06-12T12:15:00Z",
      "progress": 65
    },
    {
      "name": "transform",
      "status": "pending"
    },
    {
      "name": "publish",
      "status": "pending"
    }
  ],
  "metrics": {
    "rows_discovered": 52487234,
    "rows_validated": 34200145,
    "rows_transformed": 0,
    "rows_published": 0,
    "data_size_gb": 2.3,
    "errors": 0,
    "warnings": 3
  },
  "events": [
    {
      "timestamp": "2026-06-12T12:15:00Z",
      "level": "INFO",
      "message": "Validation started"
    },
    {
      "timestamp": "2026-06-12T12:16:30Z",
      "level": "WARNING",
      "message": "3 null values found in column 'customer_id'"
    }
  ]
}
```

#### List Jobs

```
GET /v1/jobs?connector_id=c-Financeiro-001&status=running,failed&limit=50&offset=0

Response (200 OK):
{
  "jobs": [
    {
      "id": "job-20260612-001",
      "connector_id": "c-Financeiro-001",
      "status": "running",
      "created_at": "2026-06-12T12:00:00Z",
      "progress": 45
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### Cancel Job

```
DELETE /v1/jobs/job-20260612-001
Authorization: Bearer {token}

Response (200 OK):
{
  "id": "job-20260612-001",
  "status": "cancelled",
  "cancelled_at": "2026-06-12T12:45:00Z"
}
```

### 4. Webhooks

#### Register Webhook

```
POST /v1/webhooks
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "url": "https://your-company.com/webhooks/avanade",
  "events": [
    "job.completed",
    "job.failed",
    "job.stage_completed"
  ],
  "headers": {
    "X-Custom-Auth": "your-auth-token"
  },
  "retry_policy": {
    "max_retries": 5,
    "backoff_multiplier": 2
  }
}

Response (201 Created):
{
  "id": "webhook-123",
  "url": "https://your-company.com/webhooks/avanade",
  "events": ["job.completed", "job.failed", "job.stage_completed"],
  "status": "active",
  "created_at": "2026-06-12T12:00:00Z"
}
```

#### Webhook Payload

```json
{
  "event": "job.completed",
  "timestamp": "2026-06-12T14:30:00Z",
  "webhook_id": "webhook-123",
  "data": {
    "job_id": "job-20260612-001",
    "connector_id": "c-Financeiro-001",
    "status": "completed",
    "metrics": {
      "rows_processed": 52487234,
      "duration_minutes": 120,
      "errors": 0
    }
  }
}
```

### 5. Dashboards & Metrics

#### Get Metrics

```
GET /v1/metrics/jobs?connector_id=c-Financeiro-001&granularity=hourly&hours=24

Response (200 OK):
{
  "metrics": [
    {
      "timestamp": "2026-06-11T14:00:00Z",
      "jobs_completed": 2,
      "jobs_failed": 0,
      "rows_processed": 10234567,
      "avg_throughput_mb_sec": 45.2,
      "errors": 0
    }
  ]
}
```

### 6. Health & Status

#### API Health

```
GET /health

Response (200 OK):
{
  "status": "healthy",
  "timestamp": "2026-06-12T16:30:00Z",
  "services": {
    "auth": "healthy",
    "database": "healthy",
    "storage": "healthy",
    "queue": "healthy"
  },
  "version": "1.0.0"
}
```

---

## Modelos de Dados

### Connector

```typescript
interface Connector {
  id: string;                    // c-{tenant}-{number}
  name: string;
  tenant_id: string;
  pattern: "push" | "pull" | "private_link";
  status: "registered" | "active" | "suspended" | "revoked";
  data_sources: DataSource[];
  license: License;
  created_at: ISO8601;
  updated_at: ISO8601;
  metadata: Record<string, any>;
}

interface DataSource {
  id: string;                    // ds-{type}-{number}
  type: "hive" | "mssql" | "postgresql" | "oracle" | "databricks";
  host: string;
  port: number;
  database: string;
  tables: number;
  last_sync?: ISO8601;
}

interface License {
  key: string;
  status: "active" | "suspended" | "expired";
  expiry: ISO8601;
  max_jobs_per_day?: number;
  max_data_gb_per_month?: number;
}
```

### Job

```typescript
interface Job {
  id: string;                    // job-{timestamp}-{number}
  connector_id: string;
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  job_type: "full_migration" | "incremental" | "discovery";
  stages: JobStage[];
  metrics: JobMetrics;
  events: JobEvent[];
  created_at: ISO8601;
  started_at?: ISO8601;
  completed_at?: ISO8601;
  estimated_duration_minutes: number;
}

interface JobStage {
  name: string;
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  started_at?: ISO8601;
  completed_at?: ISO8601;
  duration_seconds?: number;
  progress: number;                 // 0-100
}

interface JobMetrics {
  rows_discovered: number;
  rows_validated: number;
  rows_transformed: number;
  rows_published: number;
  data_size_gb: number;
  errors: number;
  warnings: number;
  throughput_mb_sec: number;
}
```

---

## Exemplos

### Python Client

```python
from avanade_migration import Client, ConnectorConfig

# Initialize client
client = Client(
    client_id="your-client-id",
    client_secret="your-client-secret",
    base_url="https://api.avanade.com"
)

# Register connector
connector = client.connectors.register(
    name="Financeiro-connector",
    tenant_id="Financeiro-001",
    pattern="push",
    data_sources=[
        {"type": "hive", "host": "cloudera.internal", "database": "raw_data"},
        {"type": "mssql", "host": "db.internal", "database": "erp_prod"}
    ]
)

# Request SAS token
sas = client.connectors.request_sas_token(
    connector_id=connector.id,
    validity_hours=24
)
print(f"SAS URL: {sas.sas_url}")

# Create job
job = client.jobs.create(
    connector_id=connector.id,
    job_type="full_migration",
    data_sources=["ds-hive-01"]
)

# Poll job status
while True:
    status = client.jobs.get(job.id)
    print(f"Job {job.id}: {status.status} ({status.stages[-1].progress}%)")
    if status.status in ["completed", "failed"]:
        break
    time.sleep(10)

print(f"Final metrics: {status.metrics}")
```

### cURL Examples

#### Request SAS Token
```bash
curl -X POST https://api.avanade.com/v1/connectors/c-Financeiro-001/sas-token \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "validity_hours": 24,
    "max_uploads": 100
  }' | jq .
```

#### Poll Job Status
```bash
while true; do
  curl -s https://api.avanade.com/v1/jobs/job-20260612-001 \
    -H "Authorization: Bearer $TOKEN" | jq '{status: .status, progress: .stages[-1].progress}'
  
  sleep 30
done
```

---

## Rate Limiting & Quotas

### Rate Limits

| Endpoint | Limite | Janela |
|----------|--------|--------|
| `/auth/token` | 100 | 1 min |
| `/connectors` | 1000 | 1 min |
| `/jobs` | 500 | 1 min |
| `/webhooks` | 100 | 1 min |

**Headers de Response:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1686502864
```

### Quotas (por tenant/mês)

| Recurso | Limite |
|---------|--------|
| Jobs | 1000 |
| Data (GB) | 10000 |
| Connectors | 100 |
| SAS Tokens | 5000 |

---

**Última atualização:** 2026-06-12 | **Status:** ✅ v1.0 (Stable)
