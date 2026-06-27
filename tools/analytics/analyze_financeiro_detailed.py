#!/usr/bin/env python3
"""Análise detalhada do projeto Financeiro - Tabelas, Scripts, Estrutura."""

import os
from pathlib import Path
from collections import defaultdict
import re

def analyze_sql_files(root_path):
    """Analisa arquivos SQL para encontrar CREATE TABLE, procedures, etc."""
    tables = []
    procedures = []
    views = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.sql'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Procurar CREATE TABLE
                        for match in re.finditer(r'CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)', content, re.IGNORECASE):
                            table_name = match.group(1)
                            if table_name not in tables:
                                tables.append(table_name)
                        
                        # Procurar CREATE PROCEDURE
                        for match in re.finditer(r'CREATE\s+(?:OR\s+ALTER\s+)?PROCEDURE\s+[`"\[]?(\w+)', content, re.IGNORECASE):
                            proc_name = match.group(1)
                            if proc_name not in procedures:
                                procedures.append(proc_name)
                        
                        # Procurar CREATE VIEW
                        for match in re.finditer(r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+[`"\[]?(\w+)', content, re.IGNORECASE):
                            view_name = match.group(1)
                            if view_name not in views:
                                views.append(view_name)
                except Exception as e:
                    pass
    
    return tables, procedures, views

def analyze_hql_files(root_path):
    """Analisa arquivos Hive SQL."""
    hql_files = []
    hql_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.hql'):
                hql_count += 1
                hql_files.append(os.path.relpath(os.path.join(dirpath, filename), root_path))
    
    return hql_files, hql_count

def analyze_python_scripts(root_path):
    """Analisa scripts Python - reconhece reprocedimentos."""
    reproc_scripts = []
    other_scripts = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.py'):
                if filename.startswith('reproc_'):
                    reproc_scripts.append(filename)
                elif filename not in ['__init__.py', 'setup.py', 'config.py']:
                    other_scripts.append(filename)
    
    return reproc_scripts, other_scripts

def get_directory_structure(root_path):
    """Mapeia estrutura de diretórios principais."""
    structure = defaultdict(int)
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Pegar apenas primeiro nível relevante
        rel_path = os.path.relpath(dirpath, root_path)
        if rel_path != '.':
            parts = rel_path.split(os.sep)
            if len(parts) <= 2:
                main_dir = parts[0]
                structure[main_dir] += len(filenames)
    
    return dict(sorted(structure.items(), key=lambda x: x[1], reverse=True))

def main():
    print("\n" + "="*80)
    print("ANÁLISE DETALHADA - PROJETO FINANCEIRO")
    print("Tabelas, Stored Procedures, Scripts e Estrutura")
    print("="*80 + "\n")
    
    # Análise SQL
    tables, procedures, views = analyze_sql_files('projects/financeiro')
    print(f"📊 OBJETOS DE BANCO DE DADOS (SQL):\n")
    print(f"   ✓ Tabelas criadas:        {len(tables):>3}")
    if tables:
        print(f"     Exemplos: {', '.join(tables[:5])}")
    print(f"   ✓ Procedures/Functions:   {len(procedures):>3}")
    if procedures:
        print(f"     Exemplos: {', '.join(procedures[:5])}")
    print(f"   ✓ Views:                  {len(views):>3}")
    if views:
        print(f"     Exemplos: {', '.join(views[:5])}")
    
    # Análise Hive
    hql_files, hql_count = analyze_hql_files('projects/financeiro')
    print(f"\n🐘 HIVE/HDFS (Big Data Legacy):\n")
    print(f"   ✓ Arquivos HQL:           {hql_count:>3}")
    if hql_files:
        print(f"     Exemplos:")
        for hql in hql_files[:5]:
            print(f"       - {hql}")
    
    # Análise Python
    reproc_scripts, other_scripts = analyze_python_scripts('projects/financeiro')
    print(f"\n🐍 SCRIPTS PYTHON:\n")
    print(f"   ✓ Scripts reproc:         {len(reproc_scripts):>3}")
    if reproc_scripts:
        print(f"     Exemplos: {', '.join(reproc_scripts[:5])}")
    print(f"   ✓ Outros scripts:         {len(other_scripts):>3}")
    if other_scripts:
        print(f"     Exemplos: {', '.join(other_scripts[:5])}")
    
    # Estrutura de diretórios
    dir_struct = get_directory_structure('projects/financeiro')
    print(f"\n📁 ESTRUTURA PRINCIPAL (diretórios):\n")
    for dir_name, count in dir_struct.items():
        print(f"   {dir_name:<35} {count:>4} arquivos")
    
    # Estimativa de complexidade
    print(f"\n" + "="*80)
    print("📈 RESUMO PARA MIGRAÇÃO:\n")
    
    total_entities = len(tables) + len(procedures) + len(views) + hql_count
    total_scripts = len(reproc_scripts) + len(other_scripts)
    
    print(f"   Total de entidades de BD:      {total_entities:>3}")
    print(f"   Total de scripts de lógica:    {total_scripts:>3}")
    print(f"   Complexidade estimada:         {'ALTA' if total_entities > 50 else 'MÉDIA' if total_entities > 20 else 'BAIXA'}")
    
    # Token estimate mais detalhado
    print(f"\n💰 CUSTO EM TOKENS (para migração):\n")
    print(f"   Inventário (scan):             ~50k tokens")
    print(f"   Análise SQL/Python:            ~200k tokens")
    print(f"   Design + validação:            ~300k tokens")
    print(f"   ────────────────────────────────────────")
    print(f"   TOTAL ESTIMADO:                ~550k tokens")
    print(f"   (Com overhead de context):     ~750k tokens\n")

if __name__ == '__main__':
    main()
