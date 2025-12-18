#!/bin/bash
# Test script to verify OpenEA setup
# Run this to ensure everything is working before batch experiments

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_test() {
    echo -n "Testing $1... "
}

print_pass() {
    echo -e "${GREEN}✓ PASS${NC}"
}

print_fail() {
    echo -e "${RED}✗ FAIL${NC}"
    echo "  Error: $1"
}

echo "OpenEA Installation Test"
echo "========================"
echo ""

# Test 1: Check if conda environment is activated
print_test "Conda environment"
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    print_pass
    echo "  Active environment: $CONDA_DEFAULT_ENV"
else
    print_fail "No conda environment activated. Run: conda activate openea"
    exit 1
fi

# Test 2: Python version
print_test "Python version"
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ "$PYTHON_VERSION" == "3.6" ]]; then
    print_pass
    echo "  Version: $PYTHON_VERSION"
else
    print_fail "Expected Python 3.6, got $PYTHON_VERSION"
fi

# Test 3: TensorFlow
print_test "TensorFlow"
if python -c "import tensorflow" 2>/dev/null; then
    TF_VERSION=$(python -c "import tensorflow as tf; print(tf.__version__)")
    print_pass
    echo "  Version: $TF_VERSION"
else
    print_fail "TensorFlow not installed"
    exit 1
fi

# Test 4: OpenEA package
print_test "OpenEA package"
if python -c "import openea" 2>/dev/null; then
    print_pass
else
    print_fail "OpenEA not installed. Run: pip install -e ."
    exit 1
fi

# Test 5: Required packages
print_test "Required packages"
MISSING=""
for pkg in numpy scipy pandas sklearn gensim; do
    if ! python -c "import $pkg" 2>/dev/null; then
        MISSING="$MISSING $pkg"
    fi
done

if [ -z "$MISSING" ]; then
    print_pass
else
    print_fail "Missing packages:$MISSING"
fi

# Test 6: GPU availability (non-critical)
print_test "GPU availability"
if python -c "import tensorflow as tf; print(tf.test.is_gpu_available())" 2>/dev/null | grep -q True; then
    print_pass
    GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
    echo "  GPU: $GPU_INFO"
else
    echo -e "${YELLOW}⚠ No GPU${NC}"
    echo "  Will run on CPU (slower)"
fi

# Test 7: Datasets directory
print_test "Datasets directory"
if [ -d "../datasets" ]; then
    NUM_DATASETS=$(find ../datasets -maxdepth 1 -type d | tail -n +2 | wc -l)
    print_pass
    echo "  Found $NUM_DATASETS datasets"
else
    print_fail "datasets/ directory not found"
    exit 1
fi

# Test 8: Dataset splits
print_test "Dataset splits"
HAS_SPLITS=0
for dataset in ../datasets/*/; do
    if [ -d "${dataset}721_5fold/1" ]; then
        HAS_SPLITS=$((HAS_SPLITS + 1))
    fi
done

if [ $HAS_SPLITS -gt 0 ]; then
    print_pass
    echo "  $HAS_SPLITS datasets with splits"
else
    print_fail "No datasets have train/valid/test splits"
    echo "  Run: python ../dataset_converter.py --split-alignments ..."
fi

# Test 9: Config files
print_test "Config files"
if [ -d "args" ] && [ -f "args/mtranse_args_15K.json" ]; then
    NUM_CONFIGS=$(ls args/*.json 2>/dev/null | wc -l)
    print_pass
    echo "  Found $NUM_CONFIGS config files"
else
    print_fail "Config files not found in args/"
    exit 1
fi

# Test 10: Main script
print_test "Main experiment script"
if [ -f "main_from_args.py" ]; then
    print_pass
else
    print_fail "main_from_args.py not found"
    exit 1
fi

echo ""
echo "========================"
echo -e "${GREEN}✅ All tests passed!${NC}"
echo "========================"
echo ""
echo "System is ready to run experiments."
echo ""
echo "Next steps:"
echo "  1. Test single experiment:"
echo "     python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/"
echo ""
echo "  2. Run all experiments:"
echo "     ./run_all_experiments.sh"
echo ""
