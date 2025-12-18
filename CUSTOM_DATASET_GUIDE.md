# Guide: Using Custom Datasets with OpenEA

This guide explains how to prepare and plug in your own datasets for running OpenEA entity alignment experiments.

## Dataset Structure

OpenEA expects datasets in a specific folder structure. Here's what you need:

```
YOUR_DATASET_NAME/
├── rel_triples_1          # Relation triples for KG1
├── rel_triples_2          # Relation triples for KG2
├── attr_triples_1         # Attribute triples for KG1 (optional)
├── attr_triples_2         # Attribute triples for KG2 (optional)
└── 721_5fold/            # Or your custom split name
    ├── 1/                 # Fold 1 (or single split)
    │   ├── train_links
    │   ├── valid_links
    │   └── test_links
    ├── 2/                 # Additional folds (optional)
    ├── 3/
    ├── 4/
    └── 5/
```

## File Formats

### 1. Relation Triples (`rel_triples_1` and `rel_triples_2`)

**Format:** Tab-separated values (TSV) with 3 columns  
**Content:** `head_entity \t relation \t tail_entity`

**Example:**
```
http://dbpedia.org/resource/Paris	http://dbpedia.org/ontology/country	http://dbpedia.org/resource/France
http://dbpedia.org/resource/Berlin	http://dbpedia.org/ontology/country	http://dbpedia.org/resource/Germany
http://dbpedia.org/resource/London	http://dbpedia.org/ontology/capital	http://dbpedia.org/resource/United_Kingdom
```

**Notes:**
- Each line represents one triple (head, relation, tail)
- Entities and relations should be URIs or unique identifiers
- No header line
- Use consistent identifier format across both KGs

### 2. Attribute Triples (`attr_triples_1` and `attr_triples_2`) - Optional

**Format:** Tab-separated values (TSV) with 3+ columns  
**Content:** `entity \t attribute \t value [additional_value_parts]`

**Example:**
```
http://dbpedia.org/resource/Paris	http://dbpedia.org/property/name	Paris
http://dbpedia.org/resource/Paris	http://dbpedia.org/property/population	2165423
http://dbpedia.org/resource/Berlin	http://dbpedia.org/property/name	Berlin
http://dbpedia.org/resource/Berlin	http://dbpedia.org/property/founded	1237
```

**Notes:**
- Attribute values can span multiple columns (spaces will be concatenated)
- Trailing periods are automatically removed
- If you don't have attributes, you can create empty files or omit them

### 3. Entity Links (`train_links`, `valid_links`, `test_links`)

**Format:** Tab-separated values (TSV) with 2 columns  
**Content:** `entity_in_kg1 \t entity_in_kg2`

**Example:**
```
http://dbpedia.org/resource/Paris	http://fr.dbpedia.org/resource/Paris
http://dbpedia.org/resource/Berlin	http://fr.dbpedia.org/resource/Berlin
http://dbpedia.org/resource/London	http://fr.dbpedia.org/resource/Londres
```

**Notes:**
- Each line represents an alignment between entities in KG1 and KG2
- Entities must exist in the respective relation/attribute triples
- Standard split: 20% training, 10% validation, 70% testing (for 15K datasets: 3000/1500/10500)

## Step-by-Step Setup

### Step 1: Prepare Your Data

1. **Export your KGs** into the triple format described above
2. **Create the folder structure** as shown
3. **Split your entity alignments** into train/valid/test sets

### Step 2: Place Dataset in Datasets Folder

```bash
# Create datasets directory if it doesn't exist
mkdir -p datasets/

# Move your dataset folder there
mv YOUR_DATASET_NAME/ datasets/
```

Your structure should look like:
```
OpenEA/
├── datasets/
│   └── YOUR_DATASET_NAME/
│       ├── rel_triples_1
│       ├── rel_triples_2
│       ├── attr_triples_1
│       ├── attr_triples_2
│       └── 721_5fold/1/
│           ├── train_links
│           ├── valid_links
│           └── test_links
└── run/
    └── args/
```

### Step 3: Create Configuration File

Create a new JSON configuration file in `run/args/` (e.g., `mtranse_args_custom.json`):

```json
{
    "training_data": "../../datasets/",
    "output": "../../output/results/",
    "dataset_division": "721_5fold/1/",
    
    "embedding_module": "MTransE",
    "alignment_module": "mapping",
    "search_module": "greedy",
    
    "dim": 100,
    "init": "unit",
    "ent_l2_norm": true,
    "rel_l2_norm": true,
    "loss_norm": "L2",
    
    "learning_rate": 0.01,
    "optimizer": "Adagrad",
    "max_epoch": 2000,
    "batch_size": 5000,
    
    "eval_metric": "inner",
    "eval_norm": true,
    "eval_threads_num": 4,
    "test_threads_num": 4,
    "ordered": true,
    
    "neg_triple_num": 1,
    "truncated_epsilon": 0.98,
    "ent_l2_norm": true,
    "rel_l2_norm": true
}
```

**Key parameters to adjust:**
- `dataset_division`: Path to your split (e.g., "721_5fold/1/" or "custom_split/")
- `embedding_module`: Choose your method (MTransE, BootEA, JAPE, GCN_Align, etc.)
- `batch_size`: 5000 for 15K datasets, 20000 for 100K datasets
- `max_epoch`: 2000 is standard, may need adjustment
- `alignment_module`: "mapping", "sharing", or "swapping"

### Step 4: Run the Experiment

```bash
cd run/
python main_from_args.py ./args/mtranse_args_custom.json YOUR_DATASET_NAME 721_5fold/1/
```

**Command breakdown:**
- First argument: Path to your config JSON
- Second argument: Your dataset folder name
- Third argument: Split folder path

## Alternative: Using Python API

You can also load datasets directly in Python:

```python
from openea.modules.load.kgs import read_kgs_from_folder
from openea.approaches import MTransE

# Load your dataset
kgs = read_kgs_from_folder(
    training_data_folder='../../datasets/YOUR_DATASET_NAME/',
    division='721_5fold/1/',
    mode='mapping',
    ordered=True
)

# Initialize and run model
model = MTransE()
model.set_args(args)  # Your args object
model.set_kgs(kgs)
model.init()
model.run()
model.test()
```

## Tips and Best Practices

### Data Quality
- **Consistent URIs**: Use the same URI format across files
- **No duplicates**: Ensure no duplicate triples in your data
- **Entity coverage**: Entities in links must appear in triples
- **Balanced splits**: Maintain reasonable train/valid/test ratios

### File Encoding
- Always use **UTF-8 encoding**
- Avoid special characters that might cause parsing issues
- Test with a small sample first

### Performance Optimization
- For large datasets (100K+), increase `batch_size` to 20000
- Adjust `eval_freq` to control validation frequency
- Use `truncated_epsilon` to filter low-confidence alignments

### Common Issues

**Issue:** "Entity not found" errors  
**Solution:** Ensure all entities in link files exist in triple files

**Issue:** Very low performance  
**Solution:** Check data quality, try different hyperparameters, ensure sufficient training data

**Issue:** Out of memory  
**Solution:** Reduce batch_size, use smaller embedding dimensions

## Dataset Statistics Checker

You can verify your dataset with this simple script:

```python
from openea.modules.load.read import read_relation_triples, read_links, read_attribute_triples

# Check relation triples
triples1, ents1, rels1 = read_relation_triples('datasets/YOUR_DATASET_NAME/rel_triples_1')
triples2, ents2, rels2 = read_relation_triples('datasets/YOUR_DATASET_NAME/rel_triples_2')

print(f"KG1: {len(triples1)} triples, {len(ents1)} entities, {len(rels1)} relations")
print(f"KG2: {len(triples2)} triples, {len(ents2)} entities, {len(rels2)} relations")

# Check links
train_links = read_links('datasets/YOUR_DATASET_NAME/721_5fold/1/train_links')
valid_links = read_links('datasets/YOUR_DATASET_NAME/721_5fold/1/valid_links')
test_links = read_links('datasets/YOUR_DATASET_NAME/721_5fold/1/test_links')

print(f"Train: {len(train_links)}, Valid: {len(valid_links)}, Test: {len(test_links)}")
```

## Available Methods

You can use any of these embedding modules with your dataset:

### Translation-based
- **MTransE**: Basic translation-based approach
- **IPTransE**: Iterative approach with joint embeddings
- **BootEA**: Bootstrapping-based alignment
- **TransH**, **TransR**, **TransD**: Advanced translation models

### GNN-based
- **GCN_Align**: Graph Convolutional Network approach
- **RDGCN**: Relation-aware dual-graph convolutional network
- **AliNet**: Alignment network with multi-hop aggregation

### Attribute-based
- **JAPE**: Joint attribute-preserving embedding
- **AttrE**: Attribute embedding method
- **IMUSE**: Unsupervised with attributes

### Others
- **MultiKE**: Multi-view knowledge embedding
- **RSN4EA**: Recurrent skipping networks
- **SEA**: Semi-supervised entity alignment
- **RotatE**, **HolE**, **SimplE**, **ConvE**: Various KG embedding models

## Configuration Examples

You can find pre-configured hyperparameters in `run/args/`:
- `*_args_15K.json`: For 15K-sized datasets
- `*_args_100K.json`: For 100K-sized datasets

Copy and modify these for your custom dataset.

## Need Help?

1. Check the original paper's supplementary materials for dataset format details
2. Look at the example datasets (DBP15K, EN-FR-15K) for reference
3. Examine the code in `src/openea/modules/load/` for data loading logic
4. Check the results in `output/results/` after running

## Summary

To use your own dataset:
1. Format your data as tab-separated triple files
2. Create the folder structure with train/valid/test splits
3. Place in `datasets/` folder
4. Create/modify a config JSON file
5. Run: `python main_from_args.py config.json DATASET_NAME split_folder/`

Your custom dataset is now ready to be used with any OpenEA method!
