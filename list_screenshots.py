from pathlib import Path

print("\n" + "="*70)
print("  📁 ARQUIVOS DE SCREENSHOTS CRIADOS")
print("="*70 + "\n")

screenshots_dir = Path("reports/screenshots")
if screenshots_dir.exists():
    for item in sorted(screenshots_dir.rglob("*")):
        rel_path = item.relative_to(screenshots_dir)
        if item.is_file():
            size_kb = item.stat().st_size / 1024
            print(f"  ✅ {rel_path} ({size_kb:.1f} KB)")
        else:
            print(f"  📁 {rel_path}/")
    
    print("\n" + "="*70)
    print("✅ Arquivos de screenshot gerados com sucesso!")
    print("="*70 + "\n")
else:
    print("  ❌ Diretório não encontrado")
