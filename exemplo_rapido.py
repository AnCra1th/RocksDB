#!/usr/bin/env python3
"""
Exemplo rápido de uso do RocksDB Simulator
Para demonstração em apresentações
"""

import rocksdb_simulator as rocksdb
import time

def exemplo_basico():
    print("=== EXEMPLO BÁSICO DO ROCKSDB ===\n")
    
    # 1. Abrir banco de dados
    print("1. Abrindo banco de dados...")
    opts = rocksdb.Options()
    opts.create_if_missing = True
    db = rocksdb.DB("exemplo_db", opts)
    print("✓ Banco aberto com sucesso\n")
    
    # 2. Inserir dados
    print("2. Inserindo dados...")
    dados = {
        b"usuario:001": "Joao Silva, 30 anos".encode(),
        b"usuario:002": "Maria Santos, 25 anos".encode(), 
        b"produto:001": "Notebook Dell, R$ 2500".encode(),
        b"produto:002": "Mouse Logitech, R$ 50".encode()
    }
    
    start_time = time.time()
    for chave, valor in dados.items():
        db.put(chave, valor)
    insert_time = (time.time() - start_time) * 1000
    
    print(f"✓ {len(dados)} registros inseridos em {insert_time:.2f}ms\n")
    
    # 3. Ler dados
    print("3. Lendo dados...")
    for chave in dados.keys():
        valor = db.get(chave)
        print(f"  {chave.decode()}: {valor.decode()}")
    print()
    
    # 4. Buscar por prefixo
    print("4. Buscando usuários (prefixo 'usuario:')...")
    it = db.iteritems()
    it.seek(b"usuario:")
    
    count = 0
    for chave, valor in it:
        chave_str = chave.decode()
        if not chave_str.startswith("usuario:"):
            break
        print(f"  {chave_str}: {valor.decode()}")
        count += 1
    
    print(f"✓ {count} usuários encontrados\n")
    
    # 5. Operação em lote
    print("5. Operacao em lote...")
    batch = rocksdb.WriteBatch()
    batch.put(b"usuario:003", "Pedro Costa, 35 anos".encode())
    batch.put(b"produto:003", "Teclado Mecanico, R$ 200".encode())
    batch.delete(b"produto:002")  # Remove mouse
    
    db.write(batch)
    print("✓ Batch executado: +2 inserções, -1 deleção\n")
    
    # 6. Contar registros finais
    print("6. Contagem final...")
    total = 0
    it = db.iterkeys()
    it.seek_to_first()
    for chave in it:
        total += 1
    
    print(f"✓ Total de registros: {total}")
    
    # Limpeza
    db.close()
    import shutil
    shutil.rmtree("exemplo_db")
    print("\n✓ Exemplo concluído e dados limpos!")

if __name__ == "__main__":
    exemplo_basico()
