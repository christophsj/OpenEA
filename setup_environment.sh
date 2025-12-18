#!/bin/bash
# OpenEA Environment Setup Script
# This script creates a conda environment with all necessary dependencies

set -e  # Exit on error

echo "=================================================="
echo "OpenEA Environment Setup"
echo "=================================================="
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda not found. Please install Anaconda or Miniconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✓ Found conda: $(conda --version)"
echo ""

# Environment name
ENV_NAME="openea"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠️  Environment '${ENV_NAME}' already exists."
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove -n ${ENV_NAME} -y
    else
        echo "Skipping environment creation. Using existing environment."
        echo ""
        echo "To activate the environment, run:"
        echo "  conda activate ${ENV_NAME}"
        exit 0
    fi
fi

echo "Creating conda environment: ${ENV_NAME}"
echo "This may take several minutes..."
echo ""

# Create environment with Python 3.6
conda create --name ${ENV_NAME} python=3.6 -y

# Activate environment
echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ${ENV_NAME}

# Install conda packages
echo ""
echo "Installing conda packages..."
conda install -y -c conda-forge python-igraph networkx

# Try to install graph-tool (optional, may not work on all systems)
echo ""
echo "Attempting to install graph-tool (this may fail on some systems)..."
conda install -y -c conda-forge graph-tool==2.40 || echo "⚠️  graph-tool installation failed. You can use igraph or networkx instead."

# Install pip packages
echo ""
echo "Installing pip packages..."
pip install --upgrade pip

# Install TensorFlow via pip (conda version has conflicts with Python 3.6)
echo ""
echo "Installing TensorFlow 1.12 via pip..."
pip install tensorflow-gpu==1.12.0 || pip install tensorflow==1.12.0

# Install required packages from requirements.txt with compatible versions
echo "Installing packages from requirements.txt..."
pip install numpy==1.16.0  # Compatible with TF 1.12 and Python 3.6
pip install scipy==1.2.1   # Compatible with TF 1.12 and Python 3.6
pip install -r requirements.txt

# Install additional dependencies for TensorFlow 1.12
pip install keras-applications==1.0.8
pip install keras-preprocessing==1.0.5

# Install OpenEA in development mode
echo ""
echo "Installing OpenEA..."
pip install -e .

echo ""
echo "=================================================="
echo "✅ Environment setup complete!"
echo "=================================================="
echo ""
echo "To activate the environment, run:"
echo "  conda activate ${ENV_NAME}"
echo ""
echo "To deactivate, run:"
echo "  conda deactivate"
echo ""
echo "Next steps:"
echo "  1. Activate the environment: conda activate ${ENV_NAME}"
echo "  2. Test the setup: cd run && ./test_setup.sh"
echo "  3. Run experiments: ./run_all_experiments.sh"
echo ""
