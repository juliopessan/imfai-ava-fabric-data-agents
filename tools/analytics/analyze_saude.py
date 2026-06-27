#!/usr/bin/env python3
"""Análise de estrutura do projeto Reference Saúde para cálculo de tokens."""

import os
import json
from pathlib import Path
from collections import defaultdict

def analyze_directory(root_path):
    """Analisa diretório e retorna estatísticas."""
    stats = defaultdict(lambda: {'count': 0, 'size_bytes': 0})
    total_files = 0
    total_size_bytes = 0
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
                ext = Path(filename).suffix if Path(filename).suffix else '(no-ext)'
                stats[ext]['count'] += 1
                stats[ext]['size_bytes'] += size
                total_files += 1
                total_size_bytes += size
            except Exception as e:
                print(f"Erro ao processar {filepath}: {e}")
    
    return stats, total_files, total_size_bytes

def format_size(bytes_size):
    """Converte bytes para formato legível."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def analyze_sql_files(root_path):
    """Analisa arquivos SQL."""
    sql_files = []
    db_objects = defaultdict(list)
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.sql'):
                sql_files.append(filename.replace('.sql', ''))
                # Inferir tipo de BD pelo nome
                if 'bi_' in filename:
                    db_objects['BI_Schemas'].append(filename.replace('.sql', ''))
                elif 'dw' in filename.lower():
                    db_objects['DW_Schemas'].append(filename.replace('.sql', ''))
                elif 'crm' in filename.lower():
                    db_objects['CRM_Schemas'].append(filename.replace('.sql', ''))
                else:
                    db_objects['Other_Schemas'].append(filename.replace('.sql', ''))
    
    return sql_files, db_objects

def analyze_directory_structure(root_path):
    """Analisa estrutura de diretórios."""
    structure = defaultdict(int)
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_path = os.path.relpath(dirpath, root_path)
        if rel_path != '.':
            parts = rel_path.split(os.sep)
            if len(parts) >= 1:
                main_dir = parts[0]
                structure[main_dir] += len(filenames)
    
    return dict(sorted(structure.items(), key=lambda x: x[1], reverse=True))

def analyze_airflow_dags(root_path):
    """Analisa DAGs do Airflow."""
    dags = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.startswith('dag_') and filename.endswith('.py'):
                dag_name = filename.replace('dag_', '').replace('.py', '')
                dags.append(dag_name)
    
    return dags

def main():
    print("\n" + "="*70)
    print("ANÁLISE DE ESCOPO - PROJETO REFERENCE SAÚDE")
    print("="*70 + "\n")
    
    # Analisar pasta reference-saude
    stats, total_files, total_size_bytes = analyze_directory('projects/reference-saude/legacy')
    
    print(f"Total de arquivos: {total_files:,}")
    print(f"Tamanho total: {format_size(total_size_bytes)}")
    print(f"\nArquivos por tipo (ordenado por tamanho):\n")
    print(f"{'Extensão':<15} {'Quantidade':<12} {'Tamanho':<15} {'% Total':<10}")
    print("-" * 52)
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['size_bytes'], reverse=True)
    
    for ext, data in sorted_stats:
        pct = (data['size_bytes'] / total_size_bytes * 100) if total_size_bytes > 0 else 0
        print(f"{ext:<15} {data['count']:<12} {format_size(data['size_bytes']):<15} {pct:>6.1f}%")
    
    # Análise SQL
    sql_files, db_objects = analyze_sql_files('projects/reference-saude/legacy')
    print(f"\n📊 OBJETOS SQL:\n")
    print(f"   ✓ Total de SQL files:        {len(sql_files):>3}")
    for db_type, objects in sorted(db_objects.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"     └─ {db_type:<35} {len(objects):>3}")
        if objects and len(objects) <= 5:
            for obj in objects[:5]:
                print(f"        • {obj}")
        elif objects:
            for obj in objects[:3]:
                print(f"        • {obj}")
            print(f"        ... e {len(objects)-3} others")
    
    # Análise Airflow
    dags = analyze_airflow_dags('projects/reference-saude/legacy')
    print(f"\n🔄 AIRFLOW/ORCHESTRATION:\n")
    print(f"   ✓ DAGs encontradas:          {len(dags):>3}")
    if dags:
        print(f"     Exemplos: {', '.join(dags[:5])}")
    
    # Estrutura de diretórios
    dir_struct = analyze_directory_structure('projects/reference-saude/legacy')
    print(f"\n📁 ESTRUTURA PRINCIPAL:\n")
    for dir_name, count in dir_struct.items():
        print(f"   {dir_name:<35} {count:>4} arquivos")
    
    # Token estimate
    estimated_tokens = total_size_bytes / 4
    
    print("\n" + "-" * 52)
    print(f"\n📈 RESUMO PARA MIGRAÇÃO:\n")
    
    print(f"   Total de schemas SQL:          {len(db_objects):>3}")
    print(f"   Total de DAGs Airflow:         {len(dags):>3}")
    print(f"   Total de arquivos:             {total_files:>3}")
    print(f"   Complexidade estimada:         {'ALTA' if total_files > 500 else 'MÉDIA' if total_files > 100 else 'BAIXA'}")
    
    print(f"\n💰 CUSTO EM TOKENS:\n")
    print(f"   Total em bytes:                {total_size_bytes:,}")
    print(f"   Estimativa bruta:              ~{int(estimated_tokens):,} tokens")
    print(f"   Com overhead (30%):            ~{int(estimated_tokens * 1.3):,} tokens\n")

if __name__ == '__main__':
    main()
