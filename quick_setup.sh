#!/bin/bash
# Quick Setup for New Machine - OpenEA

echo "OpenEA Quick Setup"
echo "=================="
echo ""
echo "This will guide you through setting up OpenEA on a new machine."
echo ""

# Check conda
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found!"
    echo ""
    echo "Please install Miniconda first:"
    echo "  Linux:   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh"
    echo "  macOS:   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh && bash Miniconda3-latest-MacOSX-x86_64.sh"
    exit 1
fi

echo "✓ Conda found"
echo ""

# Run setup
echo "Step 1/2: Setting up environment..."
./setup_environment.sh

# Provide next steps
echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate environment:"
echo "   conda activate openea"
echo ""
echo "2. Validate datasets (optional):"
echo "   python validate_dataset.py datasets/D_W_15K_V2"
echo ""
echo "3. Run all experiments:"
echo "   cd run"
echo "   ./run_all_experiments.sh"
echo ""
echo "4. Or run single experiment:"
echo "   cd run"
echo "   python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/"
echo ""
