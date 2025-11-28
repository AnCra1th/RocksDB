"""
Simulador do RocksDB para demonstração acadêmica
Implementa as principais funcionalidades sem dependências externas
"""

import os
import json
import time
import pickle
from typing import Dict, Any, Optional, Iterator, Tuple

class RocksDBSimulator:
    """Simulador do RocksDB que mantém dados em memória e persiste em arquivo"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.data: Dict[bytes, bytes] = {}
        self.is_open = False
        
        # Criar diretório se não existir
        os.makedirs(db_path, exist_ok=True)
        self.data_file = os.path.join(db_path, "data.pkl")
        
        # Carregar dados existentes
        self._load_data()
        self.is_open = True
    
    def _load_data(self):
        """Carrega dados do arquivo de persistência"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'rb') as f:
                    self.data = pickle.load(f)
            except:
                self.data = {}
    
    def _save_data(self):
        """Salva dados no arquivo de persistência"""
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.data, f)
    
    def put(self, key: bytes, value: bytes):
        """Insere ou atualiza um valor"""
        if not self.is_open:
            raise RuntimeError("Database is closed")
        self.data[key] = value
        self._save_data()
    
    def get(self, key: bytes) -> Optional[bytes]:
        """Recupera um valor pela chave"""
        if not self.is_open:
            raise RuntimeError("Database is closed")
        return self.data.get(key)
    
    def delete(self, key: bytes):
        """Remove uma chave"""
        if not self.is_open:
            raise RuntimeError("Database is closed")
        if key in self.data:
            del self.data[key]
            self._save_data()
    
    def iterkeys(self):
        """Retorna iterador de chaves"""
        return RocksDBIterator(self.data, 'keys')
    
    def itervalues(self):
        """Retorna iterador de valores"""
        return RocksDBIterator(self.data, 'values')
    
    def iteritems(self):
        """Retorna iterador de pares chave-valor"""
        return RocksDBIterator(self.data, 'items')
    
    def write(self, batch):
        """Executa operações em lote"""
        if not self.is_open:
            raise RuntimeError("Database is closed")
        batch.apply(self)
        self._save_data()
    
    def close(self):
        """Fecha o banco de dados"""
        self.is_open = False
    
    def __del__(self):
        """Destrutor"""
        if hasattr(self, 'is_open') and self.is_open:
            self.close()

class RocksDBIterator:
    """Simulador de iterador do RocksDB"""
    
    def __init__(self, data: Dict[bytes, bytes], mode: str):
        self.data = data
        self.mode = mode
        self.keys = sorted(data.keys())
        self.position = 0
    
    def seek_to_first(self):
        """Move para o primeiro elemento"""
        self.position = 0
    
    def seek_to_last(self):
        """Move para o último elemento"""
        self.position = len(self.keys) - 1 if self.keys else 0
    
    def seek(self, key: bytes):
        """Move para a chave especificada ou a próxima"""
        for i, k in enumerate(self.keys):
            if k >= key:
                self.position = i
                return
        self.position = len(self.keys)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.position >= len(self.keys):
            raise StopIteration
        
        key = self.keys[self.position]
        self.position += 1
        
        if self.mode == 'keys':
            return key
        elif self.mode == 'values':
            return self.data[key]
        else:  # items
            return key, self.data[key]
    
    def __reversed__(self):
        """Iteração reversa"""
        return RocksDBReverseIterator(self.data, self.mode)

class RocksDBReverseIterator:
    """Iterador reverso"""
    
    def __init__(self, data: Dict[bytes, bytes], mode: str):
        self.data = data
        self.mode = mode
        self.keys = sorted(data.keys(), reverse=True)
        self.position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.position >= len(self.keys):
            raise StopIteration
        
        key = self.keys[self.position]
        self.position += 1
        
        if self.mode == 'keys':
            return key
        elif self.mode == 'values':
            return self.data[key]
        else:  # items
            return key, self.data[key]

class WriteBatch:
    """Simulador de batch de operações"""
    
    def __init__(self):
        self.operations = []
    
    def put(self, key: bytes, value: bytes):
        """Adiciona operação de inserção ao batch"""
        self.operations.append(('put', key, value))
    
    def delete(self, key: bytes):
        """Adiciona operação de deleção ao batch"""
        self.operations.append(('delete', key, None))
    
    def apply(self, db: RocksDBSimulator):
        """Aplica todas as operações no banco"""
        for op, key, value in self.operations:
            if op == 'put':
                db.data[key] = value
            elif op == 'delete':
                if key in db.data:
                    del db.data[key]

class Options:
    """Simulador de opções do RocksDB"""
    
    def __init__(self):
        self.create_if_missing = False

def DB(path: str, options: Options) -> RocksDBSimulator:
    """Factory function para criar instância do simulador"""
    return RocksDBSimulator(path)
