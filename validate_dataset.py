#!/usr/bin/env python3
"""
Dataset Validator for OpenEA
This script checks if your custom dataset follows the correct format.
"""

import os
import sys

def validate_file_exists(filepath, description):
    """Check if a file exists."""
    if not os.path.exists(filepath):
        print(f"❌ Missing: {description} at {filepath}")
        return False
    print(f"✓ Found: {description}")
    return True

def validate_triple_file(filepath, name):
    """Validate relation or attribute triple file format."""
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            lines = f.readlines()
            if len(lines) == 0:
                print(f"⚠️  Warning: {name} is empty")
                return True
            
            entities = set()
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                parts = line.strip().split('\t')
                if len(parts) < 3:
                    print(f"❌ {name} line {i+1}: Expected at least 3 tab-separated values, got {len(parts)}")
                    print(f"   Line content: {line.strip()}")
                    return False
                entities.add(parts[0])
                entities.add(parts[2])
            
            print(f"✓ {name}: {len(lines)} lines, valid format (sample checked)")
            return True
    except Exception as e:
        print(f"❌ Error reading {name}: {e}")
        return False

def validate_links_file(filepath, name):
    """Validate entity links file format."""
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            lines = f.readlines()
            if len(lines) == 0:
                print(f"❌ {name} is empty")
                return False
            
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                parts = line.strip().split('\t')
                if len(parts) != 2:
                    print(f"❌ {name} line {i+1}: Expected 2 tab-separated values, got {len(parts)}")
                    print(f"   Line content: {line.strip()}")
                    return False
            
            print(f"✓ {name}: {len(lines)} entity pairs, valid format")
            return True
    except Exception as e:
        print(f"❌ Error reading {name}: {e}")
        return False

def collect_entities_from_triples(filepath):
    """Collect all entities from a triple file."""
    entities = set()
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    entities.add(parts[0])
                    entities.add(parts[2])
    except:
        pass
    return entities

def collect_entities_from_links(filepath):
    """Collect entities from a links file."""
    entities_kg1 = set()
    entities_kg2 = set()
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    entities_kg1.add(parts[0])
                    entities_kg2.add(parts[1])
    except:
        pass
    return entities_kg1, entities_kg2

def validate_dataset(dataset_path, split_name='721_5fold/1'):
    """Main validation function."""
    print("="*60)
    print(f"Validating OpenEA Dataset: {dataset_path}")
    print("="*60)
    print()
    
    all_valid = True
    
    # Check main files
    print("1. Checking main data files...")
    print("-" * 40)
    rel_triples_1 = os.path.join(dataset_path, 'rel_triples_1')
    rel_triples_2 = os.path.join(dataset_path, 'rel_triples_2')
    attr_triples_1 = os.path.join(dataset_path, 'attr_triples_1')
    attr_triples_2 = os.path.join(dataset_path, 'attr_triples_2')
    
    all_valid &= validate_file_exists(rel_triples_1, "Relation triples KG1")
    all_valid &= validate_file_exists(rel_triples_2, "Relation triples KG2")
    
    # Attribute triples are optional
    has_attr_1 = os.path.exists(attr_triples_1)
    has_attr_2 = os.path.exists(attr_triples_2)
    if has_attr_1:
        validate_file_exists(attr_triples_1, "Attribute triples KG1")
    else:
        print("ℹ️  Attribute triples KG1: Not provided (optional)")
    if has_attr_2:
        validate_file_exists(attr_triples_2, "Attribute triples KG2")
    else:
        print("ℹ️  Attribute triples KG2: Not provided (optional)")
    print()
    
    # Check split files
    print("2. Checking split files...")
    print("-" * 40)
    split_path = os.path.join(dataset_path, split_name)
    train_links = os.path.join(split_path, 'train_links')
    valid_links = os.path.join(split_path, 'valid_links')
    test_links = os.path.join(split_path, 'test_links')
    
    all_valid &= validate_file_exists(train_links, "Training links")
    all_valid &= validate_file_exists(valid_links, "Validation links")
    all_valid &= validate_file_exists(test_links, "Test links")
    print()
    
    # Validate file formats
    print("3. Validating file formats...")
    print("-" * 40)
    all_valid &= validate_triple_file(rel_triples_1, "rel_triples_1")
    all_valid &= validate_triple_file(rel_triples_2, "rel_triples_2")
    if has_attr_1:
        all_valid &= validate_triple_file(attr_triples_1, "attr_triples_1")
    if has_attr_2:
        all_valid &= validate_triple_file(attr_triples_2, "attr_triples_2")
    print()
    
    all_valid &= validate_links_file(train_links, "train_links")
    all_valid &= validate_links_file(valid_links, "valid_links")
    all_valid &= validate_links_file(test_links, "test_links")
    print()
    
    # Check entity coverage
    print("4. Checking entity coverage...")
    print("-" * 40)
    kg1_entities = collect_entities_from_triples(rel_triples_1)
    kg2_entities = collect_entities_from_triples(rel_triples_2)
    
    print(f"✓ KG1 has {len(kg1_entities)} unique entities")
    print(f"✓ KG2 has {len(kg2_entities)} unique entities")
    
    train_kg1, train_kg2 = collect_entities_from_links(train_links)
    valid_kg1, valid_kg2 = collect_entities_from_links(valid_links)
    test_kg1, test_kg2 = collect_entities_from_links(test_links)
    
    all_link_kg1 = train_kg1 | valid_kg1 | test_kg1
    all_link_kg2 = train_kg2 | valid_kg2 | test_kg2
    
    # Check if linked entities exist in triples
    missing_kg1 = all_link_kg1 - kg1_entities
    missing_kg2 = all_link_kg2 - kg2_entities
    
    if missing_kg1:
        print(f"⚠️  Warning: {len(missing_kg1)} entities in links not found in KG1 triples")
        if len(missing_kg1) <= 5:
            print(f"   Examples: {list(missing_kg1)[:5]}")
    else:
        print("✓ All linked entities exist in KG1 triples")
    
    if missing_kg2:
        print(f"⚠️  Warning: {len(missing_kg2)} entities in links not found in KG2 triples")
        if len(missing_kg2) <= 5:
            print(f"   Examples: {list(missing_kg2)[:5]}")
    else:
        print("✓ All linked entities exist in KG2 triples")
    print()
    
    # Dataset statistics
    print("5. Dataset Statistics")
    print("-" * 40)
    print(f"Total entities: {len(kg1_entities) + len(kg2_entities)}")
    print(f"Training pairs: {len(train_kg1)}")
    print(f"Validation pairs: {len(valid_kg1)}")
    print(f"Test pairs: {len(test_kg1)}")
    print(f"Total alignment: {len(all_link_kg1)}")
    
    train_ratio = len(train_kg1) / len(all_link_kg1) * 100
    valid_ratio = len(valid_kg1) / len(all_link_kg1) * 100
    test_ratio = len(test_kg1) / len(all_link_kg1) * 100
    print(f"Split ratio: {train_ratio:.1f}% / {valid_ratio:.1f}% / {test_ratio:.1f}%")
    print()
    
    # Final verdict
    print("="*60)
    if all_valid:
        print("✅ Dataset validation PASSED!")
        print("Your dataset is ready to use with OpenEA.")
    else:
        print("❌ Dataset validation FAILED!")
        print("Please fix the issues above before using the dataset.")
    print("="*60)
    
    return all_valid

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset.py <dataset_path> [split_name]")
        print("Example: python validate_dataset.py datasets/MY_DATASET 721_5fold/1")
        sys.exit(1)
    
    dataset_path = sys.argv[1]
    split_name = sys.argv[2] if len(sys.argv) > 2 else '721_5fold/1'
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' does not exist!")
        sys.exit(1)
    
    validate_dataset(dataset_path, split_name)
