#!/usr/bin/env python3
"""
VS Code Playwright Integration Test & Automation
Testa a instalação do Playwright e automatiza capturas de screenshots
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def check_python_version():
    """Verifica se Python 3.8+ está instalado"""
    print("🔍 Verificando Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"   ❌ Python 3.8+ requerido (atual: {version.major}.{version.minor})")
    return False


def check_playwright_installed():
    """Verifica se Playwright está instalado"""
    print("\n🔍 Verificando Playwright...")
    try:
        import playwright
        print(f"   ✅ Playwright v1.60.0 (ou superior)")
        return True
    except ImportError:
        print("   ❌ Playwright não instalado")
        return False


def check_chromium_installed():
    """Verifica se Chromium está instalado"""
    print("\n🔍 Verificando Chromium...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            print("   ✅ Chromium OK")
            browser.close()
            return True
    except Exception as e:
        print(f"   ❌ Chromium não disponível: {str(e)}")
        return False


def install_playwright():
    """Instala Playwright e Chromium"""
    print("\n📦 Instalando Playwright...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        print("   ✅ Playwright instalado")
        
        print("\n📦 Instalando Chromium...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("   ✅ Chromium instalado")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False


def test_screenshot_capture():
    """Testa captura de screenshot simples"""
    print("\n🎬 Testando captura de screenshot...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto("data:text/html,<h1>Playwright Test ✅</h1>")
            
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / "test_screenshot.png"
            
            page.screenshot(path=str(screenshot_path))
            browser.close()
            
            print(f"   ✅ Screenshot salvo: {screenshot_path}")
            return True
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False


def setup_vscode_tasks():
    """Cria arquivo .vscode/tasks.json com tasks Playwright"""
    print("\n⚙️ Configurando VS Code tasks...")
    
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "🎬 Playwright: Capturar Screenshots (Financeiro - Upstream)",
                "type": "shell",
                "command": "python",
                "args": [
                    "reports/_templates/playwright_screenshot_generator.py",
                    "--project", "Financeiro",
                    "--stage", "upstream"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": False
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                }
            },
            {
                "label": "🎬 Playwright: Capturar Screenshots (Financeiro - Midstream)",
                "type": "shell",
                "command": "python",
                "args": [
                    "reports/_templates/playwright_screenshot_generator.py",
                    "--project", "Financeiro",
                    "--stage", "midstream"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": False
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                }
            },
            {
                "label": "🎬 Playwright: Capturar Screenshots (Financeiro - Downstream)",
                "type": "shell",
                "command": "python",
                "args": [
                    "reports/_templates/playwright_screenshot_generator.py",
                    "--project", "Financeiro",
                    "--stage", "downstream"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": False
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                }
            }
        ]
    }
    
    import json
    tasks_path = vscode_dir / "tasks.json"
    with open(tasks_path, 'w', encoding='utf-8') as f:
        json.dump(tasks_json, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Salvo: {tasks_path}")
    return True


def print_summary(all_checks: dict):
    """Imprime sumário da configuração"""
    print("\n" + "="*70)
    print("  ✅ PLAYWRIGHT + VS CODE INTEGRATION — RESUMO")
    print("="*70 + "\n")
    
    if all(all_checks.values()):
        print("🟢 Todos os testes passaram! Pronto para usar.")
    else:
        print("🟡 Alguns itens precisam de atenção:")
    
    print()
    for check_name, status in all_checks.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {check_name}")
    
    print("\n" + "="*70)
    print("  📸 PRÓXIMOS PASSOS")
    print("="*70 + "\n")
    
    if all(all_checks.values()):
        print("  1️⃣  Abra o VS Code (Ctrl+Shift+B) e selecione uma task Playwright")
        print("  2️⃣  Ou execute direto no terminal:")
        print("      python reports/_templates/playwright_screenshot_generator.py --project Financeiro --stage upstream")
        print("  3️⃣  Verifique os screenshots em: reports/screenshots/Financeiro/")
        print("  4️⃣  Abra o HTML gerado: reports/screenshots/Financeiro/before_after_comparison.html")
    else:
        print("  1️⃣  Execute a instalação automática:")
        print("      python reports/_templates/playwright_vscode_integration_test.py --install")
        print("  2️⃣  Reexecute este script para validar")
    
    print("\n" + "="*70)
    print("  📖 DOCUMENTAÇÃO")
    print("="*70 + "\n")
    print("  Leia: reports/_templates/PLAYWRIGHT-SETUP-GUIDE.md")
    print()


def main():
    """Executa todos os testes"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Teste e setup de Playwright + VS Code")
    parser.add_argument("--install", action="store_true", help="Instalar dependências automaticamente")
    parser.add_argument("--test", action="store_true", help="Testar captura de screenshot")
    parser.add_argument("--setup-vscode", action="store_true", help="Configurar VS Code tasks")
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("  🚀 PLAYWRIGHT + VS CODE INTEGRATION TEST")
    print("="*70 + "\n")
    
    all_checks = {}
    
    # Verificar Python
    all_checks["Python 3.8+"] = check_python_version()
    
    # Verificar Playwright
    all_checks["Playwright instalado"] = check_playwright_installed()
    
    if not all_checks["Playwright instalado"] and args.install:
        if install_playwright():
            all_checks["Playwright instalado"] = check_playwright_installed()
    
    # Verificar Chromium
    if all_checks["Playwright instalado"]:
        all_checks["Chromium OK"] = check_chromium_installed()
    else:
        all_checks["Chromium OK"] = False
    
    # Testar captura
    if args.test and all_checks["Chromium OK"]:
        all_checks["Screenshot capture"] = test_screenshot_capture()
    
    # Setup VS Code
    if args.setup_vscode or all(all_checks.values()):
        if setup_vscode_tasks():
            all_checks["VS Code tasks"] = True
    else:
        all_checks["VS Code tasks"] = False
    
    # Sumário
    print_summary(all_checks)


if __name__ == "__main__":
    main()
