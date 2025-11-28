import time
import random
import string
import json
import os
import psutil

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation):
        self.metrics[f"{operation}_start"] = time.time()
    
    def end_timer(self, operation):
        start_time = self.metrics.get(f"{operation}_start", time.time())
        duration = (time.time() - start_time) * 1000  # em ms
        self.metrics[f"{operation}_duration_ms"] = duration
        return duration
    
    def record_metric(self, name, value):
        self.metrics[name] = value
    
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB
    
    def print_report(self):
        print("\n" + "="*50)
        print("RELATÓRIO DE MÉTRICAS")
        print("="*50)
        for key, value in self.metrics.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        print("="*50)

class DataGenerator:
    @staticmethod
    def generate_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_json_data():
        return json.dumps({
            'id': random.randint(1, 10000),
            'name': DataGenerator.generate_string(20),
            'email': f"{DataGenerator.generate_string(10)}@example.com",
            'age': random.randint(18, 80),
            'active': random.choice([True, False])
        })
    
    @staticmethod
    def generate_test_data(count, data_type='small'):
        data = {}
        for i in range(count):
            key = f"key_{i:06d}"
            if data_type == 'small':
                value = DataGenerator.generate_string(random.randint(10, 50))
            elif data_type == 'medium':
                value = DataGenerator.generate_string(random.randint(100, 500))
            elif data_type == 'json':
                value = DataGenerator.generate_json_data()
            data[key] = value
        return data

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / 1024 / 1024  # MB
