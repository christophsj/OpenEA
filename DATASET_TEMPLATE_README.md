# Example Dataset Template for OpenEA

This directory contains a minimal example dataset that demonstrates the correct format for OpenEA.

## Directory Structure

```
example_dataset/
├── rel_triples_1          # Relation triples for KG1
├── rel_triples_2          # Relation triples for KG2
├── attr_triples_1         # Attribute triples for KG1 (optional)
├── attr_triples_2         # Attribute triples for KG2 (optional)
└── 721_5fold/
    └── 1/
        ├── train_links    # Training entity alignments
        ├── valid_links    # Validation entity alignments
        └── test_links     # Test entity alignments
```

## File Contents

### rel_triples_1
```
ent:e1	rel:born_in	ent:paris
ent:e2	rel:born_in	ent:london
ent:e3	rel:capital_of	ent:france
ent:paris	rel:located_in	ent:france
ent:london	rel:located_in	ent:uk
```

### rel_triples_2
```
ent:a1	rel:birthplace	ent:paris_fr
ent:a2	rel:birthplace	ent:london_uk
ent:a3	rel:is_capital	ent:france_fr
ent:paris_fr	rel:in_country	ent:france_fr
ent:london_uk	rel:in_country	ent:uk_fr
```

### attr_triples_1 (optional)
```
ent:paris	attr:name	Paris
ent:paris	attr:population	2165000
ent:london	attr:name	London
ent:london	attr:population	8900000
```

### attr_triples_2 (optional)
```
ent:paris_fr	attr:nom	Paris
ent:paris_fr	attr:habitants	2165000
ent:london_uk	attr:nom	Londres
ent:london_uk	attr:habitants	8900000
```

### 721_5fold/1/train_links
```
ent:paris	ent:paris_fr
ent:london	ent:london_uk
```

### 721_5fold/1/valid_links
```
ent:france	ent:france_fr
```

### 721_5fold/1/test_links
```
ent:uk	ent:uk_fr
ent:e1	ent:a1
ent:e2	ent:a2
ent:e3	ent:a3
```

## Notes

- All files use **tab** (`\t`) as separator, not spaces
- Entity and relation URIs can be any unique string
- No header lines in any file
- Files should be UTF-8 encoded
- Attribute values can contain spaces (everything after 2nd tab is the value)
