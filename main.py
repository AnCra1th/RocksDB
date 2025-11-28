#!/usr/bin/env python3
"""
Demonstração Prática do RocksDB
Projeto acadêmico para mostrar funcionalidades e performance do RocksDB
"""

import sys
import os
from demo_crud import CRUDDemo
from demo_benchmark import BenchmarkDemo
from demo_batch import BatchDemo
from demo_iterator import IteratorDemo

def print_header():
    print("="*60)
    print("DEMONSTRAÇÃO PRÁTICA DO ROCKSDB")
    print("="*60)
    print("Este projeto demonstra as principais funcionalidades")
    print("e características de performance do RocksDB em Python")
    print("="*60)

def print_menu():
    print("\nEscolha uma demonstração:")
    print("1. CRUD - Operações básicas (Create, Read, Update, Delete)")
    print("2. Benchmark - Testes de performance")
    print("3. Batch - Operações em lote")
    print("4. Iterator - Navegação e busca de dados")
    print("5. Executar TODAS as demonstrações")
    print("0. Sair")
    print("-" * 50)

def run_crud_demo():
    print("\n🚀 Executando demonstração CRUD...")
    demo = CRUDDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()

def run_benchmark_demo():
    print("\n🚀 Executando demonstração de Benchmark...")
    demo = BenchmarkDemo()
    try:
        demo.run_all_benchmarks()
    finally:
        demo.cleanup()

def run_batch_demo():
    print("\n🚀 Executando demonstração de Batch...")
    demo = BatchDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()

def run_iterator_demo():
    print("\n🚀 Executando demonstração de Iterator...")
    demo = IteratorDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()

def run_all_demos():
    print("\n🚀 Executando TODAS as demonstrações...")
    print("\nEsta execução pode levar alguns minutos...")
    
    demos = [
        ("CRUD Operations", run_crud_demo),
        ("Performance Benchmarks", run_benchmark_demo),
        ("Batch Operations", run_batch_demo),
        ("Iterator & Search", run_iterator_demo)
    ]
    
    for name, demo_func in demos:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            demo_func()
        except Exception as e:
            print(f"❌ Erro na demonstração {name}: {e}")
        print(f"✅ {name} concluída")
    
    print("\n🎉 Todas as demonstrações foram executadas!")

def check_dependencies():
    try:
        import rocksdb_simulator
        import psutil
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install psutil")
        return False

def main():
    print_header()
    
    # Verificar dependências
    if not check_dependencies():
        return 1
    
    # Criar diretório de dados se não existir
    os.makedirs("data", exist_ok=True)
    
    while True:
        print_menu()
        
        try:
            choice = input("Digite sua escolha (0-5): ").strip()
            
            if choice == "0":
                print("👋 Encerrando demonstração. Obrigado!")
                break
            elif choice == "1":
                run_crud_demo()
            elif choice == "2":
                run_benchmark_demo()
            elif choice == "3":
                run_batch_demo()
            elif choice == "4":
                run_iterator_demo()
            elif choice == "5":
                run_all_demos()
            else:
                print("❌ Opção inválida. Tente novamente.")
                continue
                
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demonstração interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            input("Pressione Enter para continuar...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
