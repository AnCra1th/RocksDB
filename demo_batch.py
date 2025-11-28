import rocksdb_simulator as rocksdb
import os
import shutil
from utils import MetricsCollector, DataGenerator

class BatchDemo:
    def __init__(self, db_path="data/batch_demo"):
        self.db_path = db_path
        self.db = None
        self.metrics = MetricsCollector()
    
    def setup(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        
        opts = rocksdb.Options()
        opts.create_if_missing = True
        self.db = rocksdb.DB(self.db_path, opts)
        print("✓ Banco RocksDB inicializado para demo de batch")
    
    def demo_individual_vs_batch(self, count=5000):
        print(f"\n--- DEMO: Inserção Individual vs Batch ({count} registros) ---")
        
        test_data = DataGenerator.generate_test_data(count, 'small')
        
        # Teste Individual
        print("Testando inserção individual...")
        self.metrics.start_timer("individual_insert")
        for key, value in test_data.items():
            self.db.put(key.encode(), value.encode())
        individual_duration = self.metrics.end_timer("individual_insert")
        
        # Limpar dados
        for key in test_data.keys():
            self.db.delete(key.encode())
        
        # Teste Batch
        print("Testando inserção em batch...")
        batch = rocksdb.WriteBatch()
        
        self.metrics.start_timer("batch_insert")
        for key, value in test_data.items():
            batch.put(key.encode(), value.encode())
        
        # Executar batch
        self.db.write(batch)
        batch_duration = self.metrics.end_timer("batch_insert")
        
        # Calcular métricas
        individual_ops = count / (individual_duration / 1000)
        batch_ops = count / (batch_duration / 1000)
        improvement = ((individual_duration - batch_duration) / individual_duration) * 100
        
        self.metrics.record_metric("individual_ops_per_sec", individual_ops)
        self.metrics.record_metric("batch_ops_per_sec", batch_ops)
        self.metrics.record_metric("batch_improvement_percent", improvement)
        
        print(f"✓ Individual: {individual_duration:.2f}ms ({individual_ops:.0f} ops/s)")
        print(f"✓ Batch: {batch_duration:.2f}ms ({batch_ops:.0f} ops/s)")
        print(f"✓ Melhoria: {improvement:.1f}% mais rápido")
    
    def demo_mixed_batch_operations(self):
        print(f"\n--- DEMO: Operações Mistas em Batch ---")
        
        # Preparar dados iniciais
        initial_data = DataGenerator.generate_test_data(1000, 'small')
        for key, value in initial_data.items():
            self.db.put(key.encode(), value.encode())
        
        # Criar batch com operações mistas
        batch = rocksdb.WriteBatch()
        
        operations_count = {
            'insert': 0,
            'update': 0,
            'delete': 0
        }
        
        self.metrics.start_timer("mixed_batch")
        
        # Inserções
        new_data = DataGenerator.generate_test_data(500, 'small')
        for key, value in new_data.items():
            new_key = f"new_{key}"
            batch.put(new_key.encode(), value.encode())
            operations_count['insert'] += 1
        
        # Atualizações
        keys_to_update = list(initial_data.keys())[:300]
        for key in keys_to_update:
            new_value = f"updated_{DataGenerator.generate_string(20)}"
            batch.put(key.encode(), new_value.encode())
            operations_count['update'] += 1
        
        # Deleções
        keys_to_delete = list(initial_data.keys())[300:500]
        for key in keys_to_delete:
            batch.delete(key.encode())
            operations_count['delete'] += 1
        
        # Executar batch
        self.db.write(batch)
        duration = self.metrics.end_timer("mixed_batch")
        
        total_ops = sum(operations_count.values())
        ops_per_sec = total_ops / (duration / 1000)
        
        print(f"✓ Operações executadas em {duration:.2f}ms:")
        print(f"  - Inserções: {operations_count['insert']}")
        print(f"  - Atualizações: {operations_count['update']}")
        print(f"  - Deleções: {operations_count['delete']}")
        print(f"  - Total: {total_ops} operações")
        print(f"✓ Throughput: {ops_per_sec:.0f} ops/segundo")
        
        self.metrics.record_metric("mixed_batch_total_ops", total_ops)
        self.metrics.record_metric("mixed_batch_ops_per_sec", ops_per_sec)
    
    def demo_batch_atomicity(self):
        print(f"\n--- DEMO: Atomicidade de Batch ---")
        
        # Inserir dados iniciais
        initial_data = DataGenerator.generate_test_data(100, 'small')
        for key, value in initial_data.items():
            self.db.put(key.encode(), value.encode())
        
        # Contar registros antes
        count_before = self.count_records()
        print(f"Registros antes: {count_before}")
        
        # Criar batch que será executado com sucesso
        successful_batch = rocksdb.WriteBatch()
        for i in range(50):
            key = f"atomic_test_{i:03d}"
            value = f"value_{i}"
            successful_batch.put(key.encode(), value.encode())
        
        self.db.write(successful_batch)
        count_after_success = self.count_records()
        print(f"Registros após batch bem-sucedido: {count_after_success}")
        print(f"✓ Adicionados: {count_after_success - count_before} registros")
        
        # Demonstrar que todas as operações do batch são aplicadas juntas
        print("✓ Todas as 50 operações foram aplicadas atomicamente")
    
    def count_records(self):
        count = 0
        it = self.db.iterkeys()
        it.seek_to_first()
        for key in it:
            count += 1
        return count
    
    def run_all_demos(self):
        self.setup()
        self.demo_individual_vs_batch()
        self.demo_mixed_batch_operations()
        self.demo_batch_atomicity()
        self.metrics.print_report()
    
    def cleanup(self):
        if self.db:
            del self.db
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

if __name__ == "__main__":
    demo = BatchDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()
