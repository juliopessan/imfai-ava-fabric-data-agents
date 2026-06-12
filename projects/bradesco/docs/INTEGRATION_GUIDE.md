# 🔌 Guia de Integração

> Passo a passo para implementar cada padrão de conexão (Push/Pull/Private Link).

---

## 📑 Índice

1. [Overview](#overview)
2. [Padrão A — Push (Quick Start)](#padrão-a--push-quick-start)
3. [Padrão B — Pull (Compliance-First)](#padrão-b--pull-compliance-first)
4. [Padrão C — Private Link (Enterprise)](#padrão-c--private-link-enterprise)
5. [Validação & Testes](#validação--testes)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### Diagrama de Fluxo Geral

```
1. Cliente escolhe padrão
   ├─ Performance? Escalabilidade?    → A (Push)
   ├─ Compliance? Dados sensíveis?    → B (Pull)
   └─ Zero-trust? Enterprise?         → C (Private Link)

2. Setup credenciais/rede

3. Deploy connector/agent

4. Teste funcional

5. Go-live
```

---

## Padrão A — Push (Quick Start)

### 1. Pré-requisitos

**Cliente:**
- [x] Windows Server 2019+ ou Linux (Ubuntu 20.04+)
- [x] Python 3.10+
- [x] Network acesso ao Connector Agent (download)
- [x] Credenciais read-only para DB (suportado: SQL, Hive, PostgreSQL, Oracle)

**Avanade:**
- [x] Tenant Bradesco provisionado
- [x] ADLS Gen2 landing zone criada
- [x] Service Bus queue configurado

### 2. Download e Instalação

```bash
# Step 1: Download do agent
curl -O https://cdn.avanade.com/connector-agent/1.0.0/connector-agent-1.0.0.whl \
  --header "Authorization: Bearer {LICENSE_TOKEN}"

# Step 2: Install
pip install connector-agent-1.0.0.whl

# Step 3: Verify
connector-agent --version
# Output: Connector Agent v1.0.0
```

### 3. Configuração

**Arquivo: `/opt/avanade/connector/config.yaml`**

```yaml
agent:
  id: c-bradesco-001
  license_key: "lic-XXXXX-XXXXX"
  connector_id: c-12345
  region: eastus
  environment: production

sources:
  - name: cloudera_main
    type: hive
    host: 10.0.1.100
    port: 10000
    database: raw_data
    connection_pool_size: 20
    readonly: true
    
  - name: sql_erp
    type: mssql
    server: 10.0.2.50
    port: 1433
    database: erp_prod
    connection_pool_size: 10
    readonly: true

security:
  tls_version: "1.2"
  verify_ssl: true
  cipher_suites:
    - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    - TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305

upload:
  batch_size: 100000
  compression: gzip
  compression_level: 6
  max_parallel_uploads: 5
  max_retries: 3
  retry_backoff: exponential
  
logging:
  level: INFO
  file: /var/log/avanade/connector.log
  max_size_mb: 500
  backup_count: 10
```

### 4. Teste de Conexão

```bash
# Test Hive
connector-agent test-connection \
  --source cloudera_main \
  --timeout 30

# Output:
# ✅ Hive connection OK
# ✅ Database: raw_data accessible
# ✅ Sample query: 1,234,567 rows
# 🔐 Mode: read-only enforced

# Test SQL
connector-agent test-connection \
  --source sql_erp \
  --query "SELECT COUNT(*) FROM dbo.customers"

# Output:
# ✅ MSSQL connection OK
# ✅ Query executed
# Result: 5,432,101 rows
```

### 5. Requestar SAS Token

```bash
# Backend API call (realizado via portal)
curl -X POST https://api.avanade.com/v1/connectors/c-12345/sas-token \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ADMIN_TOKEN}" \
  -d '{
    "validity_hours": 24,
    "max_uploads": 100,
    "max_size_mb": 500000
  }'

# Response:
{
  "sas_url": "https://avanadeadls.blob.core.windows.net/landing/bradesco-001/run-20260612-001?sv=2021-06-08&...",
  "sas_token": "sv=2021-06-08&...",
  "expiration": "2026-06-13T12:00:00Z",
  "upload_path": "landing/bradesco-001/run-20260612-001/",
  "max_size_mb": 500000
}

# Copiar SAS URL e passar ao agent
```

### 6. Configurar Upload

```bash
# Store SAS URL in agent (encrypted on disk)
connector-agent configure-upload \
  --sas-url "https://avanadeadls.blob.core.windows.net/landing/bradesco-001/run-20260612-001?sv=2021-06-08&..." \
  --batch-size 100000 \
  --compression gzip \
  --parallel-uploads 5

# Verify
connector-agent show-upload-config
# Output:
# Upload Configuration
# ├─ SAS URL: configured ✅
# ├─ Batch size: 100,000 rows
# ├─ Compression: gzip (level 6)
# ├─ Parallel uploads: 5
# └─ TTL: 24 hours remaining
```

### 7. Validação Pré-Extração

```bash
# Dry-run: Teste sem fazer upload
connector-agent extract \
  --source cloudera_main \
  --sample-rows 10000 \
  --dry-run

# Output:
# Dry-run: cloudera_main
# ├─ Tables found: 127
# ├─ Sample rows: 10,000
# ├─ Estimated size: 2.3 GB
# ├─ Extraction time: ~5 minutes
# └─ Status: ✅ Ready
```

### 8. Extração Completa

```bash
# Extract all data
connector-agent extract \
  --source cloudera_main \
  --parallel-queries 10 \
  --progress

# Output (streaming):
# Extracting: cloudera_main
# ├─ [████████████░░░░░░░░░░░░░░░░] 45% (1.2GB/2.7GB, ~3min remaining)
# ├─ Uploaded batches: 12/27
# ├─ Throughput: 45 MB/s
# └─ Errors: 0

# Após conclusão:
# ✅ Extraction complete!
# ├─ Total rows: 52,487,234
# ├─ Total size: 2.7 GB
# ├─ Duration: 8 minutes
# ├─ Batches: 27
# ├─ Errors: 0
# └─ Hash: abc123def456 (for validation)
```

### 9. Monitorar Processamento

```bash
# Via Portal ou API
curl https://api.avanade.com/v1/jobs/job-12345 \
  -H "Authorization: Bearer {TOKEN}"

# Response:
{
  "job_id": "job-12345",
  "status": "processing",
  "stage": "transform",
  "progress": {
    "overall": 67,
    "discovery": 100,
    "validation": 100,
    "transform": 45,
    "publish": 0
  },
  "metrics": {
    "rows_ingested": 52487234,
    "rows_validated": 52487234,
    "rows_transformed": 35124567,
    "duration_minutes": 8,
    "throughput_mb_sec": 45.2
  },
  "eta": "2026-06-12T16:30:00Z"
}
```

---

## Padrão B — Pull (Compliance-First)

### 1. Pré-requisitos

**Cliente:**
- [x] Entra ID app registration
- [x] Service Principal + certificate (60 meses)
- [x] Database read-only role criado
- [x] Network firewall: Allow Avanade IP range

**Avanade:**
- [x] Credential Broker deployed
- [x] Key Vault secrets configured
- [x] Staging zone (ADLS Gen2) ready

### 2. Cliente: Setup Service Principal

#### 2.1 Entra ID App Registration

```powershell
# Script: New-MigrationServicePrincipal.ps1

# Connect to Entra ID
Connect-AzureAD

# Create app registration
$app = New-AzureADApplication `
  -DisplayName "Avanade-Migration-Agent" `
  -SignInAudience "AzureADMultiOrg" `
  -PublicClient $false

Write-Host "App created: $($app.AppId)"

# Create service principal
$sp = New-AzureADServicePrincipal `
  -AppId $app.AppId `
  -DisplayName "Avanade-Migration-Agent"

Write-Host "Service Principal created: $($sp.ObjectId)"
```

#### 2.2 Create Certificate

```powershell
# Create self-signed certificate (60 months)
$certName = "Avanade-Migration-Cert"
$cert = New-SelfSignedCertificate `
  -Subject "CN=$certName" `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -KeyExportPolicy Exportable `
  -KeySpec Signature `
  -KeyLength 4096 `
  -KeyUsage DigitalSignature `
  -NotAfter (Get-Date).AddDays(21900)

Write-Host "Certificate created: $($cert.Thumbprint)"

# Export certificate
$certPath = "C:\certs\avanade-migration.cer"
Export-Certificate -Cert $cert -FilePath $certPath
Write-Host "Certificate exported to: $certPath"

# Export private key (for Avanade Vault)
$pfxPath = "C:\certs\avanade-migration.pfx"
$password = ConvertTo-SecureString "YourStrongPassword" -AsPlainText -Force
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password -Force
Write-Host "PFX exported to: $pfxPath"
```

#### 2.3 Upload Certificate to Entra

```powershell
# Upload certificate to app
$cert = Get-Item Cert:\CurrentUser\My\{THUMBPRINT}
$keyCredential = New-Object Microsoft.Open.AzureAD.Model.KeyCredential
$keyCredential.CustomKeyIdentifier = [System.Convert]::FromBase64String($cert.Thumbprint)
$keyCredential.Type = "AsymmetricX509Cert"
$keyCredential.Usage = "Sign"
$keyCredential.Value = [System.Convert]::ToBase64String($cert.RawData)

New-AzureADApplicationKeyCredential `
  -ObjectId $app.ObjectId `
  -KeyCredential $keyCredential

Write-Host "Certificate uploaded to app"
```

#### 2.4 Database: Create Read-Only User

```sql
-- SQL Server
CREATE LOGIN [avanade-agent] FROM EXTERNAL PROVIDER;
CREATE USER [avanade-agent] FOR LOGIN [avanade-agent];
ALTER ROLE db_datareader ADD MEMBER [avanade-agent];

-- Grant SELECT on specific schemas (least privilege)
GRANT SELECT ON SCHEMA::dbo TO [avanade-agent];
GRANT SELECT ON SCHEMA::staging TO [avanade-agent];

-- Verify
SELECT * FROM sys.sysusers WHERE name = 'avanade-agent';

-- Hive / Spark
-- Create Kerberos principal
kadmin -p admin/admin@REALM
  addprinc -randkey hive/avanade-agent@REALM
  ktadd -k /etc/security/keytabs/avanade-agent.keytab hive/avanade-agent@REALM

-- Grant role
GRANT SELECT ON DATABASE raw_data TO ROLE `avanade-agent`;
```

### 3. Avanade: Credential Broker Setup

```bash
# Deploy credential broker (Helm chart or ARM)
helm install credential-broker avanade/credential-broker \
  --namespace avanade-system \
  --values - <<EOF
config:
  credentials:
    bradesco-001:
      type: service_principal
      tenant_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      certificate_name: "avanade-migration"  # in Key Vault
      token_ttl: 15m
      token_refresh_offset: 2m
      endpoint: "https://database.windows.net"
  
  azure:
    key_vault_name: avanade-vaultavanade-vault
    managed_identity_client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

monitoring:
  prometheus_enabled: true
  port: 9090
EOF
```

### 4. Test: Token Request

```bash
# Test credential broker
curl -X POST https://credential-broker.internal:8443/token/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {AGENT_TOKEN}" \
  -d '{
    "credential_name": "bradesco-001",
    "agent_id": "a-bradesco-001",
    "purpose": "data_extraction"
  }'

# Response:
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "resource": "https://database.windows.net"
}
```

### 5. Deploy Pull Agent

```yaml
# deployment-pull-agent.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pull-agent-bradesco
  namespace: migration
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pull-agent
      tenant: bradesco
  template:
    metadata:
      labels:
        app: pull-agent
        tenant: bradesco
    spec:
      serviceAccountName: avanade-agent
      containers:
      - name: pull-agent
        image: mcr.microsoft.com/avanade/pull-agent:1.0.0
        imagePullPolicy: Always
        env:
        - name: CREDENTIAL_BROKER_URL
          value: "https://credential-broker.internal:8443"
        - name: CREDENTIAL_NAME
          value: "bradesco-001"
        - name: STAGING_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: staging-creds
              key: connection_string
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 6. Monitor Extraction

```bash
# View pod logs
kubectl logs -f deployment/pull-agent-bradesco -n migration

# Output:
# [INFO] Pull agent started
# [INFO] Credential broker: connected
# [INFO] Polling for jobs...
# [INFO] Job received: job-12345
# [INFO] Getting credentials for: bradesco-001
# [INFO] Token valid: 900s TTL
# [INFO] Connecting to database: server.database.windows.net
# [INFO] Reading table: [dbo].[customers] (5.4M rows)
# [INFO] Batch 1: 100K rows → staging (3.2MB, 1.2s)
# [INFO] Batch 2: 100K rows → staging (3.2MB, 1.1s)
# ...
# [INFO] Extraction complete: 5,432,101 rows, 180s
```

---

## Padrão C — Private Link (Enterprise)

### 1. Network Preparation (Arquitetura)

```bash
# Deploy VNet peering & private endpoints
az deployment group create \
  --resource-group avanade-prod \
  --template-file network-setup.bicep \
  --parameters \
    clientVnetId=/subscriptions/.../resourceGroups/cliente/providers/Microsoft.Network/virtualNetworks/cliente-vnet \
    peeringName=cliente-to-avanade \
    allowForwardedTraffic=true \
    allowGatewayTransit=false
```

### 2. Configure Private Endpoints

```bash
# ADLS Gen2 private endpoint
az network private-endpoint create \
  --resource-group avanade-prod \
  --vnet-name avanade-prod-vnet \
  --subnet avanade-storage \
  --name adls-private-endpoint \
  --connection-name adls-privatelink-connection \
  --private-connection-resource-id /subscriptions/.../Microsoft.Storage/storageAccounts/avanadeadls \
  --group-ids blob
```

### 3. Deploy Agent (VNet-injected)

```yaml
# container-app-vnet-injected.yaml
apiVersion: containerapps.io/v1
kind: ContainerApp
metadata:
  name: private-link-agent
  properties:
    environmentId: /subscriptions/.../containerAppEnvironments/avanade-prod
    configuration:
      registries:
        - server: mcr.microsoft.com
      ingress:
        external: false  # No public access
        targetPort: 8080
      secrets:
        - name: client-connection
          value: "server=10.0.1.100;database=prod;..." # Private IP
    template:
      containers:
      - name: agent
        image: mcr.microsoft.com/avanade/private-link-agent:1.0.0
        env:
        - name: CLIENT_DB_HOST
          value: "10.0.1.100"  # Private IP
        - name: CLIENT_DB_PORT
          value: "1433"
        - name: MANAGED_IDENTITY_CLIENT_ID
          value: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        resources:
          cpu: "2"
          memory: "4Gi"
      scale:
        minReplicas: 3
        maxReplicas: 10
        rules:
        - name: cpu-scale-rule
          custom:
            query: "cpu"
            threshold: "70"
```

### 4. Verify Private Connectivity

```bash
# SSH into agent pod
kubectl exec -it deployment/private-link-agent -- /bin/bash

# Test DNS resolution (deve resolver para IP privado)
nslookup client-db.database.windows.net
# Output:
# Server: 10.100.2.1 (private DNS)
# Name: client-db.database.windows.net
# Address: 10.0.1.100  ← private IP, not public

# Test connectivity
sqlcmd -S 10.0.1.100 -d client_db \
  -U "avanade-agent" -C \
  -Q "SELECT COUNT(*) FROM dbo.customers"
# Output: 5432101

# Verify no public routing
tracert client-db.database.windows.net
# Output: all hops are internal (10.x.x.x)
```

---

## Validação & Testes

### Checklist Pré-Produção

```
[ ] Padrão escolhido e validado
[ ] Credenciais testadas (read-only enforced)
[ ] Network connectivity verified (latência < 100ms)
[ ] SAS token / service principal / private link working
[ ] Sample extraction successful (100K rows)
[ ] Data validation passed (row count, MD5 hash)
[ ] Monitoring alerts configured
[ ] Disaster recovery tested
[ ] Security audit passed
[ ] Runbook reviewed
```

### Test Cases

| Teste | Esperado | Pass |
|-------|----------|------|
| Connection timeout | Retry com backoff | ✓ |
| Token expiration | Refresh automático | ✓ |
| Large batch (>1M rows) | Streaming, sem OOM | ✓ |
| Network interruption | Checkpoint + resume | ✓ |
| Concurrent extractions | Isolamento por tenant | ✓ |

---

## Troubleshooting

### Push Pattern

| Erro | Causa | Solução |
|-----|-------|---------|
| License invalid | Key expirada/revogada | Portal: regenerar license |
| SAS token expired | TTL expirado | Request novo token |
| Connection refused | Firewall cliente | Whitelist IP Connector Agent |
| Upload timeout | Network lento | Aumentar timeout/batch-size |

### Pull Pattern

| Erro | Causa | Solução |
|-----|-------|---------|
| Token request fails | SP cert expirada | Renovar cert no Entra |
| Database auth fails | User sem permissão | Verificar GRANT SELECT |
| Connection timeout | Network blocking | Firewall: allow Foundry IPs |

### Private Link

| Erro | Causa | Solução |
|-----|-------|---------|
| Private endpoint creation fails | Quota excedida | Request limit increase |
| DNS resolution fails | Private DNS zone não confugurada | Criar zona privada |
| Latência alta | VNet peering congestionada | Add transit gateway |

---

**Última atualização:** 2026-06-12 | **Status:** ✅ Pronto para Produção
