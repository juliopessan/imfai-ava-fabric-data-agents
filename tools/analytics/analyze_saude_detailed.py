#!/usr/bin/env python3
"""Análise detalhada do Reference Saúde - Schemas, DAGs, Estrutura."""

import os
from pathlib import Path
from collections import defaultdict
import re

def analyze_sql_detailed(root_path):
    """Analisa arquivos SQL em detalhe."""
    schemas = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.sql'):
                filepath = os.path.join(dirpath, filename)
                schema_name = filename.replace('.sql', '')
                
                # Tentar contar linhas
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        schemas.append({'name': schema_name, 'lines': lines, 'path': filepath})
                except:
                    schemas.append({'name': schema_name, 'lines': 0, 'path': filepath})
    
    return schemas

def analyze_dag_structure(root_path):
    """Analisa estrutura de DAGs."""
    dags = defaultdict(lambda: {'tasks': [], 'config_files': 0})
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # DAG files
            if filename.startswith('dag_') and filename.endswith('.py'):
                dag_name = filename.replace('dag_', '').replace('.py', '')
                dags[dag_name]['tasks'].append('main_dag')
            
            # Task files
            elif filename.startswith('task_') and filename.endswith('.sh'):
                # Extrair DAG de task_ name
                parts = filename.replace('task_', '').replace('.sh', '').split('_')
                dag_prefix = '_'.join(parts[:-1]) if len(parts) > 1 else filename
                dags[dag_prefix]['tasks'].append(filename)
            
            # Config files
            elif filename in ['docker-compose.yml', 'constraints.txt', 'webserver_config.py']:
                dags['airflow_config']['config_files'] += 1
    
    return dags

def analyze_stack(root_path):
    """Detecta stack de tecnologia."""
    stack = {
        'databases': set(),
        'orchestration': set(),
        'compute': set(),
        'files': defaultdict(int)
    }
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_path = os.path.relpath(dirpath, root_path).lower()
        
        # Detectar tecnologias por caminho
        if 'airflow' in rel_path:
            stack['orchestration'].add('Airflow')
        if 'emr' in rel_path:
            stack['compute'].add('EMR (Spark/Hadoop)')
        if 'dw' in rel_path or 'bi_' in rel_path or 'dwpacs' in rel_path:
            stack['databases'].add('SQL Server DW')
        
        # Contar por tipo de arquivo
        for filename in filenames:
            ext = Path(filename).suffix
            if ext:
                stack['files'][ext] += 1
    
    return stack

def main():
    print("\n" + "="*80)
    print("ANÁLISE DETALHADA - PROJETO REFERENCE SAÚDE")
    print("Schemas SQL, DAGs Airflow, Stack & Arquitetura")
    print("="*80 + "\n")
    
    # Análise SQL detalhada
    schemas = analyze_sql_detailed('projects/reference-saude/legacy')
    print(f"📊 SQL SCHEMAS DETALHADOS:\n")
    print(f"   Total de schemas:             {len(schemas):>3}")
    if schemas:
        # Agrupar por tipo
        bi_schemas = [s for s in schemas if 'bi_' in s['name']]
        dw_schemas = [s for s in schemas if 'dw' in s['name'].lower()]
        crm_schemas = [s for s in schemas if 'crm' in s['name'].lower()]
        other_schemas = [s for s in schemas if s not in bi_schemas + dw_schemas + crm_schemas]
        
        print(f"\n   BI Schemas ({len(bi_schemas)}):")
        for schema in bi_schemas[:5]:
            print(f"     - {schema['name']:<30} {schema['lines']:>6} linhas")
        
        print(f"\n   DW Schemas ({len(dw_schemas)}):")
        for schema in dw_schemas[:5]:
            print(f"     - {schema['name']:<30} {schema['lines']:>6} linhas")
        
        print(f"\n   CRM Schemas ({len(crm_schemas)}):")
        for schema in crm_schemas[:3]:
            print(f"     - {schema['name']:<30} {schema['lines']:>6} linhas")
        
        if other_schemas:
            print(f"\n   Outros Schemas ({len(other_schemas)}):")
            for schema in other_schemas[:5]:
                print(f"     - {schema['name']:<30} {schema['lines']:>6} linhas")
    
    # Análise DAGs
    dags = analyze_dag_structure('projects/reference-saude/legacy')
    print(f"\n🔄 AIRFLOW DAGs & TASKS:\n")
    print(f"   Total de DAGs:                {len([d for d in dags if d != 'airflow_config']):>3}")
    
    for dag_name in sorted([d for d in dags if d != 'airflow_config']):
        tasks = dags[dag_name]['tasks']
        print(f"\n   DAG: {dag_name}")
        print(f"     └─ Tasks/Files: {len(tasks)}")
        for task in tasks[:3]:
            print(f"        • {task}")
        if len(tasks) > 3:
            print(f"        ... + {len(tasks)-3} more")
    
    # Stack detectado
    stack = analyze_stack('projects/reference-saude/legacy')
    print(f"\n🏗️ STACK TECNOLÓGICO:\n")
    print(f"   Databases:      {', '.join(sorted(stack['databases'])) if stack['databases'] else 'N/A'}")
    print(f"   Orchestration:  {', '.join(sorted(stack['orchestration'])) if stack['orchestration'] else 'N/A'}")
    print(f"   Compute:        {', '.join(sorted(stack['compute'])) if stack['compute'] else 'N/A'}")
    
    # Arquivos
    print(f"\n📦 COMPOSIÇÃO DE ARQUIVOS:\n")
    for ext, count in sorted(stack['files'].items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"   {ext or '(no-ext)':<15} {count:>4} arquivos")
    
    print(f"\n" + "="*80)
    print("💰 RESUMO PARA CÁLCULO DE TOKENS\n")
    
    print(f"   Schemas SQL:                  {len(schemas)}")
    print(f"   DAGs Airflow:                 {len([d for d in dags if d != 'airflow_config'])}")
    print(f"   Complexidade:                 {'MÉDIA-ALTA' if len(dags) > 5 else 'MÉDIA' if len(schemas) > 15 else 'MÉDIA-BAIXA'}")
    
    print(f"\n   Token estimate:")
    print(f"   - Inventário (scan):          ~30k tokens")
    print(f"   - SQL Analysis (27 schemas):  ~100k tokens")
    print(f"   - Airflow DAGs (5 DAGs):      ~80k tokens")
    print(f"   - Design + validação:         ~150k tokens")
    print(f"   ────────────────────────────────────────")
    print(f"   - TOTAL ESTIMADO:             ~360k tokens\n")

if __name__ == '__main__':
    main()
