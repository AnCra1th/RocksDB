import rocksdb_simulator as rocksdb
import os
import shutil
import random
from utils import MetricsCollector, DataGenerator, get_directory_size

class BenchmarkDemo:
    def __init__(self, db_path="data/benchmark_demo"):
        self.db_path = db_path
        self.db = None
        self.metrics = MetricsCollector()
    
    def setup(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        
        opts = rocksdb.Options()
        opts.create_if_missing = True
        self.db = rocksdb.DB(self.db_path, opts)
        print("✓ Banco RocksDB inicializado para benchmark")
    
    def benchmark_sequential_vs_random(self, count=5000):
        print(f"\n--- BENCHMARK: Inserção Sequencial vs Aleatória ({count} registros) ---")
        
        # Teste Sequencial
        test_data = DataGenerator.generate_test_data(count, 'medium')
        keys = list(test_data.keys())
        
        self.metrics.start_timer("sequential_insert")
        for key in keys:
            self.db.put(key.encode(), test_data[key].encode())
        seq_duration = self.metrics.end_timer("sequential_insert")
        
        # Limpar para teste aleatório
        for key in keys:
            self.db.delete(key.encode())
        
        # Teste Aleatório
        random.shuffle(keys)
        self.metrics.start_timer("random_insert")
        for key in keys:
            self.db.put(key.encode(), test_data[key].encode())
        rand_duration = self.metrics.end_timer("random_insert")
        
        seq_ops = count / (seq_duration / 1000)
        rand_ops = count / (rand_duration / 1000)
        
        print(f"✓ Sequencial: {seq_duration:.2f}ms ({seq_ops:.0f} ops/s)")
        print(f"✓ Aleatório: {rand_duration:.2f}ms ({rand_ops:.0f} ops/s)")
        print(f"✓ Diferença: {((rand_duration - seq_duration) / seq_duration * 100):.1f}%")
    
    def benchmark_value_sizes(self):
        print(f"\n--- BENCHMARK: Diferentes Tamanhos de Valor ---")
        
        sizes = [
            ('pequeno', 50, 1000),
            ('médio', 500, 1000),
            ('grande', 2000, 500)
        ]
        
        for size_name, size_bytes, count in sizes:
            # Limpar dados anteriores
            self.cleanup_data()
            
            # Gerar dados do tamanho específico
            test_data = {}
            for i in range(count):
                key = f"key_{i:06d}"
                value = DataGenerator.generate_string(size_bytes)
                test_data[key] = value
            
            # Benchmark de inserção
            self.metrics.start_timer(f"insert_{size_name}")
            for key, value in test_data.items():
                self.db.put(key.encode(), value.encode())
            duration = self.metrics.end_timer(f"insert_{size_name}")
            
            # Benchmark de leitura
            keys = list(test_data.keys())
            self.metrics.start_timer(f"read_{size_name}")
            for key in keys:
                self.db.get(key.encode())
            read_duration = self.metrics.end_timer(f"read_{size_name}")
            
            # Calcular métricas
            insert_ops = count / (duration / 1000)
            read_ops = count / (read_duration / 1000)
            db_size = get_directory_size(self.db_path)
            
            print(f"✓ Tamanho {size_name} ({size_bytes} bytes):")
            print(f"  - Inserção: {duration:.2f}ms ({insert_ops:.0f} ops/s)")
            print(f"  - Leitura: {read_duration:.2f}ms ({read_ops:.0f} ops/s)")
            print(f"  - Tamanho DB: {db_size:.2f} MB")
    
    def benchmark_memory_usage(self, count=10000):
        print(f"\n--- BENCHMARK: Uso de Memória ({count} registros) ---")
        
        initial_memory = self.metrics.get_memory_usage()
        self.metrics.record_metric("initial_memory_mb", initial_memory)
        
        # Inserir dados e medir memória
        test_data = DataGenerator.generate_test_data(count, 'medium')
        
        for i, (key, value) in enumerate(test_data.items()):
            self.db.put(key.encode(), value.encode())
            
            # Medir memória a cada 2000 inserções
            if (i + 1) % 2000 == 0:
                current_memory = self.metrics.get_memory_usage()
                print(f"  - {i+1} registros: {current_memory:.2f} MB")
        
        final_memory = self.metrics.get_memory_usage()
        memory_increase = final_memory - initial_memory
        db_size = get_directory_size(self.db_path)
        
        self.metrics.record_metric("final_memory_mb", final_memory)
        self.metrics.record_metric("memory_increase_mb", memory_increase)
        self.metrics.record_metric("db_size_mb", db_size)
        
        print(f"✓ Memória inicial: {initial_memory:.2f} MB")
        print(f"✓ Memória final: {final_memory:.2f} MB")
        print(f"✓ Aumento: {memory_increase:.2f} MB")
        print(f"✓ Tamanho em disco: {db_size:.2f} MB")
    
    def cleanup_data(self):
        # Remove todos os dados do banco
        it = self.db.iterkeys()
        it.seek_to_first()
        keys_to_delete = []
        for key in it:
            keys_to_delete.append(key)
        
        for key in keys_to_delete:
            self.db.delete(key)
    
    def run_all_benchmarks(self):
        self.setup()
        self.benchmark_sequential_vs_random()
        self.benchmark_value_sizes()
        self.benchmark_memory_usage()
        self.metrics.print_report()
    
    def cleanup(self):
        if self.db:
            del self.db
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

if __name__ == "__main__":
    demo = BenchmarkDemo()
    try:
        demo.run_all_benchmarks()
    finally:
        demo.cleanup()
