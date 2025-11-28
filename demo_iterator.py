import rocksdb_simulator as rocksdb
import os
import shutil
from utils import MetricsCollector, DataGenerator

class IteratorDemo:
    def __init__(self, db_path="data/iterator_demo"):
        self.db_path = db_path
        self.db = None
        self.metrics = MetricsCollector()
    
    def setup(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        
        opts = rocksdb.Options()
        opts.create_if_missing = True
        self.db = rocksdb.DB(self.db_path, opts)
        
        # Inserir dados de teste organizados
        self.populate_test_data()
        print("✓ Banco RocksDB inicializado com dados de teste")
    
    def populate_test_data(self):
        # Dados de usuários
        for i in range(100):
            key = f"user:{i:03d}"
            value = f"name=User{i},email=user{i}@example.com,age={20+i%50}"
            self.db.put(key.encode(), value.encode())
        
        # Dados de produtos
        for i in range(50):
            key = f"product:{i:03d}"
            value = f"name=Product{i},price={10+i*5},category=cat{i%5}"
            self.db.put(key.encode(), value.encode())
        
        # Dados de logs com timestamp
        for i in range(200):
            key = f"log:2024-01-{(i%30)+1:02d}:{i:04d}"
            value = f"event=action{i%10},user=user{i%100},status=ok"
            self.db.put(key.encode(), value.encode())
    
    def demo_full_iteration(self):
        print(f"\n--- DEMO: Iteração Completa ---")
        
        self.metrics.start_timer("full_iteration")
        
        count = 0
        it = self.db.iteritems()
        it.seek_to_first()
        
        for key, value in it:
            count += 1
            # Processar apenas alguns para não poluir a saída
            if count <= 5:
                print(f"  {key.decode()}: {value.decode()}")
        
        duration = self.metrics.end_timer("full_iteration")
        
        print(f"✓ Total de registros: {count}")
        print(f"✓ Tempo de iteração: {duration:.2f}ms")
        print(f"✓ Velocidade: {count/(duration/1000):.0f} registros/segundo")
        
        self.metrics.record_metric("total_records", count)
        self.metrics.record_metric("iteration_speed", count/(duration/1000))
    
    def demo_prefix_search(self):
        print(f"\n--- DEMO: Busca por Prefixo ---")
        
        prefixes = ["user:", "product:", "log:2024-01-15"]
        
        for prefix in prefixes:
            print(f"\nBuscando prefixo '{prefix}':")
            
            self.metrics.start_timer(f"prefix_search_{prefix.replace(':', '_')}")
            
            count = 0
            it = self.db.iteritems()
            it.seek(prefix.encode())
            
            for key, value in it:
                key_str = key.decode()
                if not key_str.startswith(prefix):
                    break
                count += 1
                if count <= 3:  # Mostrar apenas os primeiros
                    print(f"  {key_str}: {value.decode()}")
            
            duration = self.metrics.end_timer(f"prefix_search_{prefix.replace(':', '_')}")
            
            print(f"✓ Encontrados: {count} registros em {duration:.2f}ms")
    
    def demo_range_iteration(self):
        print(f"\n--- DEMO: Iteração por Intervalo ---")
        
        # Buscar logs de um período específico
        start_key = "log:2024-01-10"
        end_key = "log:2024-01-20"
        
        print(f"Buscando logs entre {start_key} e {end_key}:")
        
        self.metrics.start_timer("range_iteration")
        
        count = 0
        it = self.db.iteritems()
        it.seek(start_key.encode())
        
        for key, value in it:
            key_str = key.decode()
            if key_str > end_key:
                break
            count += 1
            if count <= 5:  # Mostrar apenas os primeiros
                print(f"  {key_str}: {value.decode()}")
        
        duration = self.metrics.end_timer("range_iteration")
        
        print(f"✓ Registros no intervalo: {count}")
        print(f"✓ Tempo de busca: {duration:.2f}ms")
    
    def demo_reverse_iteration(self):
        print(f"\n--- DEMO: Iteração Reversa ---")
        
        self.metrics.start_timer("reverse_iteration")
        
        count = 0
        it = self.db.iteritems()
        it.seek_to_last()
        
        print("Últimos 5 registros (ordem reversa):")
        for key, value in reversed(it):
            count += 1
            if count <= 5:
                print(f"  {key.decode()}: {value.decode()}")
            if count >= 10:  # Limitar para não iterar tudo
                break
        
        duration = self.metrics.end_timer("reverse_iteration")
        
        print(f"✓ Iteração reversa completada em {duration:.2f}ms")
    
    def demo_key_only_iteration(self):
        print(f"\n--- DEMO: Iteração Apenas de Chaves ---")
        
        self.metrics.start_timer("keys_only_iteration")
        
        count = 0
        it = self.db.iterkeys()
        it.seek_to_first()
        
        user_keys = []
        for key in it:
            key_str = key.decode()
            if key_str.startswith("user:"):
                user_keys.append(key_str)
            count += 1
        
        duration = self.metrics.end_timer("keys_only_iteration")
        
        print(f"✓ Total de chaves processadas: {count}")
        print(f"✓ Chaves de usuário encontradas: {len(user_keys)}")
        print(f"✓ Tempo: {duration:.2f}ms")
        print(f"✓ Primeiras chaves de usuário: {user_keys[:5]}")
    
    def demo_search_performance(self):
        print(f"\n--- DEMO: Performance de Busca ---")
        
        # Busca direta vs iteração
        target_key = "user:050"
        
        # Busca direta
        self.metrics.start_timer("direct_search")
        value = self.db.get(target_key.encode())
        direct_duration = self.metrics.end_timer("direct_search")
        
        # Busca por iteração
        self.metrics.start_timer("iteration_search")
        found_by_iteration = None
        it = self.db.iteritems()
        it.seek_to_first()
        for key, val in it:
            if key.decode() == target_key:
                found_by_iteration = val
                break
        iteration_duration = self.metrics.end_timer("iteration_search")
        
        print(f"Buscando chave '{target_key}':")
        print(f"✓ Busca direta: {direct_duration:.4f}ms")
        print(f"✓ Busca por iteração: {iteration_duration:.4f}ms")
        print(f"✓ Diferença: {iteration_duration/direct_duration:.1f}x mais lenta")
        print(f"✓ Valor encontrado: {value.decode() if value else 'Não encontrado'}")
    
    def run_all_demos(self):
        self.setup()
        self.demo_full_iteration()
        self.demo_prefix_search()
        self.demo_range_iteration()
        self.demo_reverse_iteration()
        self.demo_key_only_iteration()
        self.demo_search_performance()
        self.metrics.print_report()
    
    def cleanup(self):
        if self.db:
            del self.db
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

if __name__ == "__main__":
    demo = IteratorDemo()
    try:
        demo.run_all_demos()
    finally:
        demo.cleanup()
