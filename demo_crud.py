import rocksdb_simulator as rocksdb
import os
import shutil
from utils import MetricsCollector, DataGenerator

class CRUDDemo:
    def __init__(self, db_path="data/crud_demo"):
        self.db_path = db_path
        self.db = None
        self.metrics = MetricsCollector()
    
    def setup(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        
        opts = rocksdb.Options()
        opts.create_if_missing = True
        self.db = rocksdb.DB(self.db_path, opts)
        print("✓ Banco RocksDB inicializado")
    
    def demo_create(self, count=10000):
        print(f"\n--- DEMO CREATE: Inserindo {count} registros ---")
        
        test_data = DataGenerator.generate_test_data(count, 'small')
        
        self.metrics.start_timer("insert")
        for key, value in test_data.items():
            self.db.put(key.encode(), value.encode())
        
        duration = self.metrics.end_timer("insert")
        ops_per_sec = count / (duration / 1000)
        
        self.metrics.record_metric("insert_count", count)
        self.metrics.record_metric("insert_ops_per_sec", ops_per_sec)
        
        print(f"✓ {count} registros inseridos em {duration:.2f}ms")
        print(f"✓ Throughput: {ops_per_sec:.0f} ops/segundo")
    
    def demo_read(self, count=1000):
        print(f"\n--- DEMO READ: Lendo {count} registros aleatórios ---")
        
        keys_to_read = [f"key_{i:06d}" for i in range(0, count)]
        
        self.metrics.start_timer("read")
        found_count = 0
        for key in keys_to_read:
            value = self.db.get(key.encode())
            if value:
                found_count += 1
        
        duration = self.metrics.end_timer("read")
        ops_per_sec = count / (duration / 1000)
        
        self.metrics.record_metric("read_count", count)
        self.metrics.record_metric("read_found", found_count)
        self.metrics.record_metric("read_ops_per_sec", ops_per_sec)
        
        print(f"✓ {found_count}/{count} registros encontrados em {duration:.2f}ms")
        print(f"✓ Throughput: {ops_per_sec:.0f} ops/segundo")
    
    def demo_update(self, count=1000):
        print(f"\n--- DEMO UPDATE: Atualizando {count} registros ---")
        
        self.metrics.start_timer("update")
        for i in range(count):
            key = f"key_{i:06d}"
            new_value = f"updated_value_{i}"
            self.db.put(key.encode(), new_value.encode())
        
        duration = self.metrics.end_timer("update")
        ops_per_sec = count / (duration / 1000)
        
        self.metrics.record_metric("update_count", count)
        self.metrics.record_metric("update_ops_per_sec", ops_per_sec)
        
        print(f"✓ {count} registros atualizados em {duration:.2f}ms")
        print(f"✓ Throughput: {ops_per_sec:.0f} ops/segundo")
    
    def demo_delete(self, count=500):
        print(f"\n--- DEMO DELETE: Removendo {count} registros ---")
        
        self.metrics.start_timer("delete")
        for i in range(count):
            key = f"key_{i:06d}"
            self.db.delete(key.encode())
        
        duration = self.metrics.end_timer("delete")
        ops_per_sec = count / (duration / 1000)
        
        self.metrics.record_metric("delete_count", count)
        self.metrics.record_metric("delete_ops_per_sec", ops_per_sec)
        
        print(f"✓ {count} registros removidos em {duration:.2f}ms")
        print(f"✓ Throughput: {ops_per_sec:.0f} ops/segundo")
    
    def run_all_demos(self):
        self.setup()
        self.demo_create()
        self.demo_read()
        self.demo_update()
        self.demo_delete()
        self.metrics.print_report()
    
    def cleanup(self):
        if self.db:
            del self.db
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

if __name__ == "__main__":
    demo = CRUDDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()
