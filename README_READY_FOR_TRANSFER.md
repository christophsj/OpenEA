# OpenEA: Ready for New Machine

## ✅ Setup Complete!

Your OpenEA repository is now fully prepared for transfer and execution on a new machine.

## 📦 What's Included

### 1. Environment Setup (`setup_environment.sh`)
- **Purpose**: Automated conda environment creation
- **Creates**: `openea` conda environment with all dependencies
- **Installs**: Python 3.6, TensorFlow 1.12, all required packages
- **Time**: ~10-20 minutes

### 2. Experiment Runner (`run_all_experiments.sh`)
- **Purpose**: Batch execution of experiments
- **Features**:
  - Runs all datasets automatically
  - 3 repetitions per dataset (configurable)
  - Progress tracking and colored output
  - Automatic logging
  - Summary report generation
  - Error handling
- **Configurable**:
  - Number of repetitions
  - Method to use
  - Which datasets to run
- **Time**: ~7 hours (GPU) or ~42 hours (CPU) for all experiments

### 3. Quick Setup (`quick_setup.sh`)
- **Purpose**: Guided one-command setup
- **Does**: Runs environment setup and provides next steps

### 4. Documentation

| File | Purpose |
|------|---------|
| `SETUP_NEW_MACHINE.md` | Complete setup guide with troubleshooting |
| `TRANSFER_CHECKLIST.md` | Step-by-step checklist for migration |
| `QUICK_REFERENCE.md` | Command cheat sheet |
| `CUSTOM_DATASET_GUIDE.md` | Dataset format documentation |
| `DATASET_VERIFICATION_SUMMARY.md` | Your datasets status |

### 5. Utilities

| Tool | Purpose |
|------|---------|
| `validate_dataset.py` | Verify dataset format and integrity |
| `dataset_converter.py` | Convert and split datasets |

### 6. Datasets (Ready to Use)

All 7 datasets validated and prepared:
- ✅ D_W_15K_V2 (30K entities)
- ✅ D_Y_15K_V2 (30K entities)
- ✅ EN_DE_15K_V2 (30K entities)
- ✅ EN_FR_15K_V2 (30K entities)
- ✅ fr_en (39.6K entities)
- ✅ zh_en (39K entities)
- ✅ ja_en (39.6K entities)

All with proper train/valid/test splits (721_5fold/1/)

## 🚀 Quick Start on New Machine

```bash
# 1. Transfer files (choose one method)
git clone https://github.com/YOUR_REPO/OpenEA.git
# OR
scp -r OpenEA/ user@server:~/
# OR
rsync -avz OpenEA/ user@server:~/OpenEA/

# 2. On new machine
cd OpenEA
./quick_setup.sh

# 3. Run experiments
conda activate openea
cd run
./run_all_experiments.sh
```

## 📊 Expected Results

### Experiment Statistics
- **Total datasets**: 7
- **Repetitions per dataset**: 3
- **Total experiments**: 21
- **Default method**: MTransE (configurable)

### Time Estimates
- **GPU (recommended)**: ~7 hours total
- **CPU**: ~42 hours total
- **Per experiment (GPU)**: ~20 minutes
- **Per experiment (CPU)**: ~2 hours

### Output Structure
```
OpenEA/
├── logs/
│   ├── D_W_15K_V2_rep1_[timestamp].log
│   ├── D_W_15K_V2_rep2_[timestamp].log
│   ├── ...
│   └── experiment_summary_[timestamp].txt
└── output/results/
    └── [various result files]
```

## 🔧 Configuration

### Change Number of Repetitions
Edit `run_all_experiments.sh`:
```bash
REPETITIONS=5  # Change from 3 to 5
```

### Change Method
Edit `run_all_experiments.sh`:
```bash
METHOD="BootEA"
CONFIG_FILE="./args/bootea_args_15K.json"
```

### Run Specific Datasets
Edit `run_all_experiments.sh` (add after line ~60):
```bash
DATASETS=("D_W_15K_V2" "EN_FR_15K_V2")  # Only these two
```

### Modify Parameters
Edit config files in `run/args/`:
```json
{
    "batch_size": 5000,      // Reduce if memory issues
    "max_epoch": 2000,       // Increase for better results
    "dim": 100,              // Embedding dimension
    "learning_rate": 0.01    // Learning rate
}
```

## 📝 Files to Transfer

### Essential (Always transfer)
- ✅ All code files (`src/`, `run/`, `*.py`)
- ✅ Setup scripts (`*.sh`)
- ✅ Config files (`run/args/*.json`)
- ✅ Documentation (`*.md`)
- ✅ Datasets (`datasets/`)

### Optional (Can regenerate)
- ❌ Output files (`output/`)
- ❌ Logs (`logs/`)
- ❌ Python cache (`__pycache__/`, `*.pyc`)
- ❌ Egg info (`*.egg-info/`)

### Archive Command
```bash
# Exclude unnecessary files
tar -czf openea_transfer.tar.gz \
    --exclude='output' \
    --exclude='logs' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.egg-info' \
    OpenEA/
```

## 🔍 Verification Steps

Before running batch experiments:

1. **Environment Test**
   ```bash
   conda activate openea
   python -c "import tensorflow; import openea; print('OK')"
   ```

2. **GPU Check** (if available)
   ```bash
   nvidia-smi
   python -c "import tensorflow as tf; print(tf.test.is_gpu_available())"
   ```

3. **Dataset Test**
   ```bash
   python validate_dataset.py datasets/D_W_15K_V2
   ```

4. **Single Run Test**
   ```bash
   cd run
   python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/
   ```

5. **Batch Run**
   ```bash
   ./run_all_experiments.sh
   ```

## 📈 Monitoring Experiments

### Real-time Progress
```bash
# In separate terminal
tail -f logs/experiment_summary_*.txt

# Or watch all logs
tail -f logs/*.log
```

### GPU Usage
```bash
watch -n 1 nvidia-smi
```

### Check Status
```bash
grep -E "(SUCCESS|FAILED)" logs/experiment_summary_*.txt
```

## 🎯 Available Methods

You can run experiments with any of these methods by editing `run_all_experiments.sh`:

| Method | Strong Points | Config File |
|--------|---------------|-------------|
| MTransE | Translation-based, fast | `mtranse_args_15K.json` |
| BootEA | Bootstrapping, iterative | `bootea_args_15K.json` |
| GCN-Align | Graph neural network | `gcnalign_args_15K.json` |
| JAPE | Attribute-based | `jape_args_15K.json` |
| AttrE | Pure attributes | `attre_args_15K.json` |
| AliNet | Multi-hop GNN | `alinet_args_15K.json` |
| MultiKE | Multi-view | `multike_args_15K.json` |
| RSN4EA | Recurrent networks | `rsn4ea_args_15K.json` |

## 🐛 Common Issues & Solutions

### Issue: GPU not detected
```bash
# Check CUDA
python -c "import tensorflow as tf; print(tf.test.is_gpu_available())"

# If false, install CPU version
conda install tensorflow==1.12
```

### Issue: Out of memory
Edit config file:
```json
"batch_size": 2000  // Reduce from 5000
```

### Issue: Import errors
```bash
conda activate openea
pip install -e .  # Reinstall OpenEA
```

### Issue: Permission denied
```bash
chmod +x *.sh
```

## 💡 Pro Tips

1. **Use screen/tmux** for long experiments
   ```bash
   screen -S openea
   ./run_all_experiments.sh
   # Ctrl+A, D to detach
   ```

2. **Background execution**
   ```bash
   nohup ./run_all_experiments.sh > exp.log 2>&1 &
   ```

3. **Save results regularly**
   ```bash
   tar -czf backup_$(date +%Y%m%d).tar.gz output/ logs/
   ```

4. **Multiple GPUs** - Edit script to set `CUDA_VISIBLE_DEVICES`

5. **Dry run first** - Test with 1 repetition before full batch

## 📚 Documentation Index

- **[SETUP_NEW_MACHINE.md](SETUP_NEW_MACHINE.md)** - Detailed setup guide
- **[TRANSFER_CHECKLIST.md](TRANSFER_CHECKLIST.md)** - Migration checklist
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference
- **[CUSTOM_DATASET_GUIDE.md](CUSTOM_DATASET_GUIDE.md)** - Dataset format
- **[DATASET_VERIFICATION_SUMMARY.md](DATASET_VERIFICATION_SUMMARY.md)** - Dataset status

## ✨ What's Next?

Your OpenEA setup is complete and ready! Here's what to do:

1. ✅ **Transfer** files to new machine (see TRANSFER_CHECKLIST.md)
2. ✅ **Setup** environment with `./quick_setup.sh`
3. ✅ **Test** with single experiment
4. ✅ **Run** batch experiments with `./run_all_experiments.sh`
5. ✅ **Collect** results from `output/` and `logs/`

---

**Need Help?**
- Check `SETUP_NEW_MACHINE.md` for detailed instructions
- Use `TRANSFER_CHECKLIST.md` for step-by-step guide
- See `QUICK_REFERENCE.md` for command cheat sheet

**Ready to go!** 🚀
