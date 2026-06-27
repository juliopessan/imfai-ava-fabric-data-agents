#!/usr/bin/env python3
"""Análise de estrutura do projeto Financeiro para cálculo de tokens."""

import os
import json
from pathlib import Path
from collections import defaultdict

def analyze_directory(root_path):
    """Analisa diretório e retorna estatísticas."""
    stats = defaultdict(lambda: {'count': 0, 'size_bytes': 0})
    total_files = 0
    total_size_bytes = 0
    structure = {'directories': {}, 'files': []}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_path = os.path.relpath(dirpath, root_path)
        
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

def main():
    print("\n" + "="*70)
    print("ANÁLISE DE ESCOPO - PROJETO FINANCEIRO")
    print("="*70 + "\n")
    
    # Analisar pasta financeiro
    stats, total_files, total_size_bytes = analyze_directory('projects/financeiro')
    
    print(f"Total de arquivos: {total_files:,}")
    print(f"Tamanho total: {format_size(total_size_bytes)}")
    print(f"\nArquivos por tipo (ordenado por tamanho):\n")
    print(f"{'Extensão':<15} {'Quantidade':<12} {'Tamanho':<15} {'% Total':<10}")
    print("-" * 52)
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['size_bytes'], reverse=True)
    
    for ext, data in sorted_stats:
        pct = (data['size_bytes'] / total_size_bytes * 100) if total_size_bytes > 0 else 0
        print(f"{ext:<15} {data['count']:<12} {format_size(data['size_bytes']):<15} {pct:>6.1f}%")
    
    # Token estimation (aproximado: 4 chars = 1 token)
    estimated_tokens = total_size_bytes / 4
    
    print("\n" + "-" * 52)
    print(f"\n📊 ESTIMATIVA DE TOKENS (aproximado):")
    print(f"   Total em bytes: {total_size_bytes:,}")
    print(f"   Estimativa: ~{int(estimated_tokens):,} tokens (1 token ≈ 4 chars)")
    print(f"   Para análise completa: ~{int(estimated_tokens * 1.3):,} tokens (com overhead)")
    
    # Análise por categoria
    print(f"\n📁 ANÁLISE POR CATEGORIA:\n")
    
    categories = {
        'SQL': ['.sql', '.ddl', '.dml'],
        'Python': ['.py'],
        'Shell': ['.sh'],
        'Configuration': ['.cfg', '.yaml', '.yml', '.xml', '.json'],
        'Documentação': ['.md', '.txt', '.rst'],
        'SSIS/ETL': ['.sln', '.dtsx'],
        'Outros': []
    }
    
    category_stats = {}
    for cat, exts in categories.items():
        size = 0
        count = 0
        for ext, data in stats.items():
            if ext in exts:
                size += data['size_bytes']
                count += data['count']
        if count > 0:
            category_stats[cat] = {'count': count, 'size': size}
    
    for cat in sorted(category_stats.keys(), key=lambda x: category_stats[x]['size'], reverse=True):
        data = category_stats[cat]
        pct = (data['size'] / total_size_bytes * 100) if total_size_bytes > 0 else 0
        print(f"{cat:<20} {data['count']:>6} arquivos  {format_size(data['size']):<12}  {pct:>5.1f}%")

if __name__ == '__main__':
    main()
