# OpenEA Portable Installation Guide

This guide helps you set up and run OpenEA experiments on a new machine.

## Quick Start (3 Steps)

```bash
# 1. Setup environment (one-time)
chmod +x setup_environment.sh
./setup_environment.sh

# 2. Activate environment
conda activate openea

# 3. Run all experiments
cd run
chmod +x run_all_experiments.sh
./run_all_experiments.sh
```

## Detailed Instructions

### 1. Prerequisites

**Required:**
- Anaconda or Miniconda installed
- Git (to clone the repository)
- 10+ GB disk space
- CUDA-capable GPU (recommended) or CPU

**Download Miniconda:**
```bash
# Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# macOS
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

### 2. Transfer Files to New Machine

**Option A: Using Git (recommended)**
```bash
git clone https://github.com/YOUR_USERNAME/OpenEA.git
cd OpenEA
```

**Option B: Using rsync/scp**
```bash
# From your local machine:
rsync -avz --progress /path/to/OpenEA/ user@remote:/path/to/OpenEA/

# Or using scp:
scp -r /path/to/OpenEA/ user@remote:/path/to/
```

**Option C: Using tar archive**
```bash
# On source machine:
cd /path/to
tar -czf openea_project.tar.gz OpenEA/

# Transfer the tar file, then on target machine:
tar -xzf openea_project.tar.gz
cd OpenEA/
```

### 3. Environment Setup

Run the automated setup script:

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

This script will:
- ✓ Create conda environment named `openea`
- ✓ Install Python 3.6
- ✓ Install TensorFlow 1.12
- ✓ Install all required packages
- ✓ Install OpenEA in development mode

**Manual Setup (if script fails):**
```bash
conda create --name openea python=3.6 -y
conda activate openea
conda install -y -c conda-forge python-igraph
conda install -y tensorflow==1.12
pip install -r requirements.txt
pip install -e .
```

### 4. Verify Installation

```bash
conda activate openea
python -c "import tensorflow; print('TensorFlow:', tensorflow.__version__)"
python -c "import openea; print('OpenEA installed successfully')"
```

### 5. Prepare Datasets

Ensure your datasets are in the correct location:

```bash
ls datasets/
# Should show: D_W_15K_V2, EN_FR_15K_V2, zh_en, ja_en, etc.

# Verify dataset structure
python validate_dataset.py datasets/D_W_15K_V2
```

If you need to transfer datasets separately:
```bash
# On source machine:
tar -czf openea_datasets.tar.gz datasets/

# Transfer and extract on target machine:
tar -xzf openea_datasets.tar.gz
```

### 6. Run Experiments

**Run all datasets with 3 repetitions:**
```bash
cd run
chmod +x run_all_experiments.sh
./run_all_experiments.sh
```

**Run single dataset:**
```bash
cd run
python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/
```

## Experiment Runner Features

The `run_all_experiments.sh` script provides:

### Configuration (edit the script to customize)
```bash
REPETITIONS=3                              # Number of times to run each dataset
METHOD="MTransE"                           # Method name
CONFIG_FILE="./args/mtranse_args_15K.json" # Configuration file
SPLIT_PATH="721_5fold/1/"                  # Dataset split path
```

### Features
- ✅ Automatic dataset discovery
- ✅ Progress tracking
- ✅ Detailed logging for each experiment
- ✅ Summary report generation
- ✅ Error handling and recovery
- ✅ Time tracking
- ✅ Colored console output

### Logs and Results

**Log files:**
```
logs/
├── D_W_15K_V2_rep1_20251218_143022.log
├── D_W_15K_V2_rep2_20251218_144531.log
├── experiment_summary_20251218_143020.txt
└── ...
```

**Results:**
```
output/results/
└── [timestamp]/
    ├── model_results.txt
    ├── embeddings/
    └── ...
```

## Running Different Methods

Edit `run_all_experiments.sh` to change the method:

```bash
# For BootEA
METHOD="BootEA"
CONFIG_FILE="./args/bootea_args_15K.json"

# For GCN-Align
METHOD="GCN_Align"
CONFIG_FILE="./args/gcnalign_args_15K.json"

# For JAPE
METHOD="JAPE"
CONFIG_FILE="./args/jape_args_15K.json"
```

## Advanced Configuration

### Run Specific Datasets Only

Edit the script and modify the datasets array:
```bash
# In run_all_experiments.sh, add after line ~60:
DATASETS=("D_W_15K_V2" "EN_FR_15K_V2")  # Override auto-discovery
```

### Parallel Execution

To run experiments in parallel (if you have multiple GPUs):

```bash
# Terminal 1
CUDA_VISIBLE_DEVICES=0 python main_from_args.py config.json dataset1 split/

# Terminal 2  
CUDA_VISIBLE_DEVICES=1 python main_from_args.py config.json dataset2 split/
```

### Background Execution

Run experiments in background (useful for remote servers):

```bash
nohup ./run_all_experiments.sh > experiments.log 2>&1 &

# Check progress
tail -f experiments.log

# Or use screen/tmux
screen -S openea
./run_all_experiments.sh
# Ctrl+A, D to detach
```

## Troubleshooting

### TensorFlow GPU not detected
```bash
# Check CUDA availability
python -c "import tensorflow as tf; print(tf.test.is_gpu_available())"

# Install CPU version if no GPU
conda install tensorflow==1.12
```

### graph-tool installation fails
```bash
# It's optional - OpenEA can use igraph or networkx
# Already handled by setup script
```

### Memory errors
```bash
# Reduce batch size in config file
# Edit: run/args/mtranse_args_15K.json
"batch_size": 2000  # Instead of 5000
```

### Permission denied
```bash
chmod +x setup_environment.sh
chmod +x run_all_experiments.sh
```

## Resource Requirements

### Minimum
- CPU: 4 cores
- RAM: 8 GB
- Disk: 10 GB
- Time: ~2 hours per dataset (CPU)

### Recommended
- CPU: 8+ cores
- RAM: 16 GB
- GPU: NVIDIA with 6+ GB VRAM
- Disk: 20 GB
- Time: ~20 minutes per dataset (GPU)

## Example Workflow

```bash
# 1. Setup on new machine
ssh user@remote-machine
git clone https://github.com/YOUR_REPO/OpenEA.git
cd OpenEA
./setup_environment.sh

# 2. Activate environment
conda activate openea

# 3. Validate datasets
python validate_dataset.py datasets/D_W_15K_V2

# 4. Test single experiment
cd run
python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/

# 5. Run all experiments
./run_all_experiments.sh

# 6. Monitor progress
tail -f ../logs/experiment_summary_*.txt

# 7. Collect results
tar -czf results_$(date +%Y%m%d).tar.gz ../output/results/ ../logs/
```

## Cleaning Up

```bash
# Remove environment
conda deactivate
conda env remove -n openea

# Clean temporary files
rm -rf output/
rm -rf logs/
rm -rf __pycache__/
rm -rf src/openea.egg-info/
```

## Summary Checklist

- [ ] Anaconda/Miniconda installed
- [ ] OpenEA repository transferred/cloned
- [ ] Datasets in `datasets/` folder
- [ ] Environment setup: `./setup_environment.sh`
- [ ] Environment activated: `conda activate openea`
- [ ] Datasets validated
- [ ] Scripts executable: `chmod +x *.sh`
- [ ] Test run completed
- [ ] Batch experiments running

---

**Need Help?**
- Check logs in `logs/` directory
- Review `CUSTOM_DATASET_GUIDE.md` for dataset issues
- See `DATASET_VERIFICATION_SUMMARY.md` for dataset status
