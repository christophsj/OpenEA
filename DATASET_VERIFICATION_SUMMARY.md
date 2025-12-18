# Dataset Verification Summary

**Date:** December 18, 2025  
**Status:** ✅ All datasets validated and ready to use!

## Overview

All 7 datasets in your `datasets/` directory have been validated and prepared with proper train/valid/test splits.

## Datasets Status

| Dataset | Status | Entities | Train | Valid | Test | Split Ratio |
|---------|--------|----------|-------|-------|------|-------------|
| **D_W_15K_V2** | ✅ PASSED | 30,000 | 3,000 | 1,500 | 10,500 | 20/10/70 |
| **D_Y_15K_V2** | ✅ PASSED | 30,000 | 3,000 | 1,500 | 10,500 | 20/10/70 |
| **EN_DE_15K_V2** | ✅ PASSED | 30,000 | 3,000 | 1,500 | 10,500 | 20/10/70 |
| **EN_FR_15K_V2** | ✅ PASSED | 30,000 | 3,000 | 1,500 | 10,500 | 20/10/70 |
| **fr_en** | ✅ PASSED | 39,654 | 4,500 | 1,500 | 9,000 | 30/10/60 |
| **zh_en** | ✅ PASSED | 38,960 | 3,000 | 1,500 | 10,500 | 20/10/70 |
| **ja_en** | ✅ PASSED | 39,594 | 3,000 | 1,500 | 10,500 | 20/10/70 |

## What Was Done

### 1. Created Train/Valid/Test Splits
All datasets now have the required `721_5fold/1/` directory structure with:
- `train_links` - Training entity alignments
- `valid_links` - Validation entity alignments  
- `test_links` - Test entity alignments

### 2. Validated All Files
Each dataset was checked for:
- ✅ Correct file format (tab-separated values)
- ✅ Required files present (rel_triples_1, rel_triples_2, attr_triples_1, attr_triples_2)
- ✅ Entity coverage (all linked entities exist in triples)
- ✅ Proper splits created

## Dataset Details

### Standard OpenEA Datasets (15K V2)
These are the official OpenEA v2 datasets with encoded URIs:
- **D_W_15K_V2**: DBpedia-Wikidata alignment
- **D_Y_15K_V2**: DBpedia-YAGO alignment
- **EN_DE_15K_V2**: English-German DBpedia cross-lingual
- **EN_FR_15K_V2**: English-French DBpedia cross-lingual

### Custom Cross-lingual Datasets
- **fr_en**: French-English alignment (larger dataset, 30% train split)
- **zh_en**: Chinese-English alignment
- **ja_en**: Japanese-English alignment

## Ready to Run!

All datasets are now ready to use with OpenEA. Example commands:

```bash
cd run/

# Run MTransE on D_W_15K_V2
python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/

# Run BootEA on EN_FR_15K_V2
python main_from_args.py ./args/bootea_args_15K.json EN_FR_15K_V2 721_5fold/1/

# Run GCN-Align on zh_en
python main_from_args.py ./args/gcnalign_args_15K.json zh_en 721_5fold/1/
```

## Dataset Structure

Each dataset now has this structure:
```
DATASET_NAME/
├── rel_triples_1          ✓ Relation triples for KG1
├── rel_triples_2          ✓ Relation triples for KG2
├── attr_triples_1         ✓ Attribute triples for KG1
├── attr_triples_2         ✓ Attribute triples for KG2
├── ent_links             ✓ All entity alignments
└── 721_5fold/1/          ✓ Split folder (NEW)
    ├── train_links       ✓ Training alignments
    ├── valid_links       ✓ Validation alignments
    └── test_links        ✓ Test alignments
```

## File Format

All files follow the correct OpenEA format:
- **Relation triples:** `entity1 \t relation \t entity2`
- **Attribute triples:** `entity \t attribute \t value`
- **Links:** `entity_kg1 \t entity_kg2`
- **Encoding:** UTF-8
- **Separator:** Tab character (`\t`)

## Next Steps

1. Choose a method from the available options:
   - MTransE, BootEA, JAPE, GCN_Align, AttrE, AliNet, MultiKE, RSN4EA, etc.

2. Select a dataset from the table above

3. Run experiments:
   ```bash
   cd run/
   python main_from_args.py ./args/METHOD_args_15K.json DATASET_NAME 721_5fold/1/
   ```

4. Check results in `output/results/`

## Notes

- The **fr_en** dataset has a different split ratio (30/10/60) because it came with pre-split files
- All other datasets use the standard 20/10/70 split (matching OpenEA paper recommendations)
- All datasets have both relation and attribute triples
- Entity coverage is 100% - all linked entities exist in the knowledge graphs

---

**Validation Tool:** `validate_dataset.py`  
**Converter Tool:** `dataset_converter.py`  
**Full Documentation:** See `CUSTOM_DATASET_GUIDE.md` and `QUICKSTART.md`
