#!/usr/bin/env python3
"""
Dataset Converter for OpenEA
Helps convert common RDF/KG formats to OpenEA format
"""

import os
import argparse
from collections import defaultdict

def convert_from_rdf_ntriples(input_file, output_file):
    """Convert N-Triples RDF format to OpenEA TSV format."""
    print(f"Converting {input_file} to {output_file}...")
    
    with open(input_file, 'r', encoding='utf8') as infile, \
         open(output_file, 'w', encoding='utf8') as outfile:
        
        for line in infile:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse N-Triple: <subject> <predicate> <object> .
            if line.endswith(' .'):
                line = line[:-2]
            
            parts = line.split(' ', 2)
            if len(parts) < 3:
                continue
            
            subject = parts[0].strip('<>').strip('"')
            predicate = parts[1].strip('<>').strip('"')
            obj = parts[2].strip('<>').strip('"')
            
            outfile.write(f"{subject}\t{predicate}\t{obj}\n")
    
    print(f"✓ Conversion complete: {output_file}")

def split_alignments(input_file, train_ratio=0.2, valid_ratio=0.1, output_dir='721_5fold/1'):
    """Split entity alignments into train/valid/test sets."""
    print(f"Splitting alignments from {input_file}...")
    
    # Read all alignments
    alignments = []
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                alignments.append((parts[0], parts[1]))
    
    total = len(alignments)
    train_size = int(total * train_ratio)
    valid_size = int(total * valid_ratio)
    
    # Split
    train_links = alignments[:train_size]
    valid_links = alignments[train_size:train_size + valid_size]
    test_links = alignments[train_size + valid_size:]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Write splits
    with open(os.path.join(output_dir, 'train_links'), 'w', encoding='utf8') as f:
        for e1, e2 in train_links:
            f.write(f"{e1}\t{e2}\n")
    
    with open(os.path.join(output_dir, 'valid_links'), 'w', encoding='utf8') as f:
        for e1, e2 in valid_links:
            f.write(f"{e1}\t{e2}\n")
    
    with open(os.path.join(output_dir, 'test_links'), 'w', encoding='utf8') as f:
        for e1, e2 in test_links:
            f.write(f"{e1}\t{e2}\n")
    
    print(f"✓ Split complete:")
    print(f"  Train: {len(train_links)} ({train_ratio*100:.0f}%)")
    print(f"  Valid: {len(valid_links)} ({valid_ratio*100:.0f}%)")
    print(f"  Test: {len(test_links)} ({(1-train_ratio-valid_ratio)*100:.0f}%)")

def separate_relations_and_attributes(input_file, rel_output, attr_output, 
                                     attr_predicates=None):
    """
    Separate triples into relations and attributes based on predicate URIs.
    
    Args:
        input_file: Input triple file
        rel_output: Output file for relation triples
        attr_output: Output file for attribute triples
        attr_predicates: Set of predicates to treat as attributes
    """
    print(f"Separating relations and attributes from {input_file}...")
    
    if attr_predicates is None:
        # Default attribute predicates (customize for your KG)
        attr_predicates = {
            'name', 'label', 'comment', 'abstract', 
            'birthDate', 'deathDate', 'population', 'area',
            'rdfs:label', 'rdfs:comment', 'foaf:name'
        }
    
    relations = []
    attributes = []
    
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            
            subject, predicate, obj = parts[0], parts[1], parts[2]
            
            # Check if predicate indicates attribute
            is_attribute = False
            for attr_pred in attr_predicates:
                if attr_pred in predicate:
                    is_attribute = True
                    break
            
            # Also check if object looks like a literal (not a URI)
            if not is_attribute and not obj.startswith('http://') and not obj.startswith('ent:'):
                is_attribute = True
            
            if is_attribute:
                attributes.append((subject, predicate, obj))
            else:
                relations.append((subject, predicate, obj))
    
    # Write outputs
    with open(rel_output, 'w', encoding='utf8') as f:
        for s, p, o in relations:
            f.write(f"{s}\t{p}\t{o}\n")
    
    with open(attr_output, 'w', encoding='utf8') as f:
        for s, p, o in attributes:
            f.write(f"{s}\t{p}\t{o}\n")
    
    print(f"✓ Separation complete:")
    print(f"  Relations: {len(relations)}")
    print(f"  Attributes: {len(attributes)}")

def create_sample_config(dataset_name, method='MTransE', size='15K'):
    """Create a sample configuration file for the dataset."""
    config = {
        "training_data": "../../datasets/",
        "output": "../../output/results/",
        "dataset_division": "721_5fold/1/",
        
        "embedding_module": method,
        "alignment_module": "mapping",
        "search_module": "greedy",
        
        "dim": 100,
        "init": "unit",
        "ent_l2_norm": True,
        "rel_l2_norm": True,
        "loss_norm": "L2",
        
        "learning_rate": 0.01,
        "optimizer": "Adagrad",
        "max_epoch": 2000,
        "batch_size": 5000 if size == '15K' else 20000,
        
        "eval_metric": "inner",
        "eval_norm": True,
        "eval_threads_num": 4,
        "test_threads_num": 4,
        "ordered": True,
        
        "neg_triple_num": 1,
        "truncated_epsilon": 0.98
    }
    
    import json
    config_file = f'{method.lower()}_args_{dataset_name}.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"✓ Created config file: {config_file}")
    return config_file

def main():
    parser = argparse.ArgumentParser(
        description='Convert datasets to OpenEA format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert N-Triples to TSV
  python dataset_converter.py --convert-ntriples kg1.nt --output rel_triples_1
  
  # Split alignments
  python dataset_converter.py --split-alignments all_links.txt --output-dir 721_5fold/1
  
  # Separate relations and attributes
  python dataset_converter.py --separate-triples all_triples.txt \\
      --rel-output rel_triples_1 --attr-output attr_triples_1
  
  # Create sample config
  python dataset_converter.py --create-config MY_DATASET --method BootEA --size 15K
        """
    )
    
    parser.add_argument('--convert-ntriples', metavar='INPUT',
                       help='Convert N-Triples file to OpenEA TSV format')
    parser.add_argument('--split-alignments', metavar='INPUT',
                       help='Split entity alignments into train/valid/test')
    parser.add_argument('--separate-triples', metavar='INPUT',
                       help='Separate triples into relations and attributes')
    parser.add_argument('--create-config', metavar='DATASET',
                       help='Create sample config file for dataset')
    
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--output-dir', metavar='DIR', default='721_5fold/1',
                       help='Output directory for splits (default: 721_5fold/1)')
    parser.add_argument('--rel-output', metavar='FILE',
                       help='Output file for relation triples')
    parser.add_argument('--attr-output', metavar='FILE',
                       help='Output file for attribute triples')
    
    parser.add_argument('--train-ratio', type=float, default=0.2,
                       help='Training set ratio (default: 0.2)')
    parser.add_argument('--valid-ratio', type=float, default=0.1,
                       help='Validation set ratio (default: 0.1)')
    
    parser.add_argument('--method', default='MTransE',
                       help='Method for config file (default: MTransE)')
    parser.add_argument('--size', default='15K', choices=['15K', '100K'],
                       help='Dataset size for config (default: 15K)')
    
    args = parser.parse_args()
    
    if args.convert_ntriples:
        if not args.output:
            print("Error: --output required for conversion")
            return
        convert_from_rdf_ntriples(args.convert_ntriples, args.output)
    
    elif args.split_alignments:
        split_alignments(args.split_alignments, 
                        args.train_ratio, args.valid_ratio,
                        args.output_dir)
    
    elif args.separate_triples:
        if not args.rel_output or not args.attr_output:
            print("Error: --rel-output and --attr-output required")
            return
        separate_relations_and_attributes(args.separate_triples,
                                         args.rel_output, args.attr_output)
    
    elif args.create_config:
        create_sample_config(args.create_config, args.method, args.size)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
