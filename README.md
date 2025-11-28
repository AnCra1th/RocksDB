# Demonstração Prática do RocksDB

Este projeto demonstra as principais funcionalidades e características de performance do RocksDB usando Python, desenvolvido para fins acadêmicos.

**Nota**: Este projeto usa um simulador do RocksDB implementado em Python puro para evitar problemas de compilação e dependências complexas, mantendo todas as funcionalidades essenciais para demonstração.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o projeto:
```bash
python main.py
```

## Estrutura do Projeto

```
praticaRocksDB/
├── main.py              # Interface principal com menu interativo
├── demo_crud.py         # Demonstração de operações CRUD
├── demo_benchmark.py    # Testes de performance e benchmarks
├── demo_batch.py        # Operações em lote (batch)
├── demo_iterator.py     # Navegação e busca de dados
├── utils.py            # Utilitários para métricas e geração de dados
├── rocksdb_simulator.py # Simulador do RocksDB em Python puro
├── requirements.txt    # Dependências do projeto
└── data/              # Diretório para dados do RocksDB (criado automaticamente)
```

## Demonstrações Disponíveis

### 1. CRUD Operations (`demo_crud.py`)
- Inserção de 10.000 registros
- Leitura de registros aleatórios
- Atualização de registros existentes
- Deleção de registros
- Métricas de throughput (ops/segundo)

### 2. Performance Benchmarks (`demo_benchmark.py`)
- Comparação inserção sequencial vs aleatória
- Teste com diferentes tamanhos de valor
- Monitoramento de uso de memória
- Análise de crescimento do banco de dados

### 3. Batch Operations (`demo_batch.py`)
- Comparação inserção individual vs batch
- Operações mistas em lote (insert/update/delete)
- Demonstração de atomicidade

### 4. Iterator & Search (`demo_iterator.py`)
- Iteração completa do banco
- Busca por prefixo
- Iteração por intervalo de chaves
- Iteração reversa
- Comparação de performance: busca direta vs iteração

## Execução Individual

Você pode executar cada demonstração individualmente:

```bash
# Apenas operações CRUD
python demo_crud.py

# Apenas benchmarks
python demo_benchmark.py

# Apenas operações batch
python demo_batch.py

# Apenas iteradores
python demo_iterator.py
```

## Métricas Coletadas

O projeto coleta e exibe as seguintes métricas:

- **Tempo de execução** (milissegundos)
- **Throughput** (operações por segundo)
- **Uso de memória** (MB)
- **Tamanho do banco** (MB)
- **Contadores de operações**

## Requisitos do Sistema

- Python 3.6+
- psutil (para monitoramento de memória)

## Simulador RocksDB

O projeto inclui um simulador completo do RocksDB (`rocksdb_simulator.py`) que implementa:

- **Operações básicas**: put, get, delete
- **Iteradores**: keys, values, items
- **Batch operations**: WriteBatch para operações atômicas
- **Persistência**: Dados salvos em arquivo pickle
- **Interface compatível**: Mesma API do python-rocksdb

### Vantagens do Simulador:
- ✅ Sem dependências de compilação
- ✅ Funciona em qualquer sistema
- ✅ Demonstra todos os conceitos principais
- ✅ Métricas reais de performance
- ✅ Ideal para fins acadêmicos

## Limpeza

Os dados são automaticamente limpos após cada demonstração. O diretório `data/` pode ser removido manualmente se necessário:

```bash
rm -rf data/
```

## Uso Acadêmico

Este projeto foi desenvolvido para demonstrar:

1. **Funcionalidades básicas** do RocksDB
2. **Características de performance** 
3. **Comparações** entre diferentes abordagens
4. **Casos de uso práticos** com métricas reais

Ideal para apresentações que precisam mostrar o RocksDB funcionando na prática com dados quantitativos.

## Exemplo de Saída

```
============================================================
DEMONSTRAÇÃO PRÁTICA DO ROCKSDB
============================================================

--- DEMO CREATE: Inserindo 10000 registros ---
✓ 10000 registros inseridos em 6405.22ms
✓ Throughput: 1561 ops/segundo

--- DEMO READ: Lendo 1000 registros aleatórios ---
✓ 1000/1000 registros encontrados em 0.09ms
✓ Throughput: 11125475 ops/segundo

==================================================
RELATÓRIO DE MÉTRICAS
==================================================
insert_duration_ms: 6405.22
insert_ops_per_sec: 1561.23
read_duration_ms: 0.09
read_ops_per_sec: 11125474.80
==================================================
```
