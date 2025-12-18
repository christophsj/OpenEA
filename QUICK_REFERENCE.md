# OpenEA Quick Reference Card

## 🚀 Quick Start (New Machine)

```bash
# 1. One-time setup
./setup_environment.sh

# 2. Activate
conda activate openea

# 3. Run all experiments (3 repetitions per dataset)
cd run && ./run_all_experiments.sh
```

## 📦 File Transfer

```bash
# Method 1: Git
git clone https://github.com/YOUR_REPO/OpenEA.git

# Method 2: Archive
tar -czf openea.tar.gz OpenEA/
scp openea.tar.gz user@server:~
ssh user@server "tar -xzf openea.tar.gz"

# Method 3: rsync
rsync -avz OpenEA/ user@server:~/OpenEA/
```

## 🔧 Commands

### Environment
```bash
# Create environment
./setup_environment.sh

# Activate
conda activate openea

# Deactivate
conda deactivate

# Remove
conda env remove -n openea
```

### Validation
```bash
# Validate single dataset
python validate_dataset.py datasets/DATASET_NAME

# Validate all
for d in datasets/*/; do python validate_dataset.py "$d"; done
```

### Single Experiment
```bash
cd run
python main_from_args.py \
    ./args/mtranse_args_15K.json \
    D_W_15K_V2 \
    721_5fold/1/
```

### Batch Experiments
```bash
cd run
./run_all_experiments.sh
```

### Background Execution
```bash
# Using nohup
nohup ./run_all_experiments.sh > exp.log 2>&1 &
tail -f exp.log

# Using screen
screen -S openea
./run_all_experiments.sh
# Ctrl+A, D to detach
screen -r openea  # reattach

# Using tmux
tmux new -s openea
./run_all_experiments.sh
# Ctrl+B, D to detach
tmux attach -t openea  # reattach
```

## 📊 Results & Logs

```bash
# View logs
ls logs/
tail -f logs/experiment_summary_*.txt

# View results
ls output/results/

# Compress results
tar -czf results_$(date +%Y%m%d).tar.gz output/results/ logs/
```

## ⚙️ Configuration

### Edit Experiment Settings
Edit `run_all_experiments.sh`:
```bash
REPETITIONS=3                              # Number of repetitions
METHOD="MTransE"                           # Method name
CONFIG_FILE="./args/mtranse_args_15K.json" # Config path
```

### Edit Method Parameters
Edit config file (e.g., `run/args/mtranse_args_15K.json`):
```json
{
    "batch_size": 5000,      // Reduce if memory issues
    "max_epoch": 2000,       // Training epochs
    "dim": 100,              // Embedding dimension
    "learning_rate": 0.01
}
```

## 🎯 Available Methods

| Method | Config File |
|--------|-------------|
| MTransE | `mtranse_args_15K.json` |
| BootEA | `bootea_args_15K.json` |
| GCN-Align | `gcnalign_args_15K.json` |
| JAPE | `jape_args_15K.json` |
| AttrE | `attre_args_15K.json` |
| AliNet | `alinet_args_15K.json` |
| MultiKE | `multike_args_15K.json` |
| RSN4EA | `rsn4ea_args_15K.json` |

## 🔍 Monitoring

```bash
# Check GPU usage
nvidia-smi

# Watch GPU in real-time
watch -n 1 nvidia-smi

# Monitor logs
tail -f logs/*.log

# Check experiment status
grep -E "(SUCCESS|FAILED)" logs/experiment_summary_*.txt
```

## 🐛 Troubleshooting

### GPU not detected
```bash
python -c "import tensorflow as tf; print(tf.test.is_gpu_available())"
```

### Out of memory
Reduce batch_size in config file:
```json
"batch_size": 2000  // instead of 5000
```

### Permission denied
```bash
chmod +x setup_environment.sh run_all_experiments.sh quick_setup.sh
```

### Environment activation fails
```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate openea
```

## 📁 File Structure

```
OpenEA/
├── setup_environment.sh          # Setup script
├── run_all_experiments.sh        # Batch runner
├── quick_setup.sh               # Quick start
├── validate_dataset.py          # Dataset validator
├── SETUP_NEW_MACHINE.md         # Detailed guide
├── datasets/                    # Your datasets
│   ├── D_W_15K_V2/
│   ├── EN_FR_15K_V2/
│   └── .../
├── run/                         # Experiment scripts
│   ├── args/                    # Config files
│   └── main_from_args.py        # Main script
├── logs/                        # Generated logs
└── output/results/              # Results
```

## 💡 Tips

1. **Test first**: Run a single experiment before batch
2. **Use screen/tmux**: For long-running experiments
3. **Monitor logs**: Check for errors early
4. **Save results**: Compress and backup regularly
5. **GPU selection**: Use `CUDA_VISIBLE_DEVICES=0` to select GPU

## 📚 Documentation

- `SETUP_NEW_MACHINE.md` - Detailed setup guide
- `CUSTOM_DATASET_GUIDE.md` - Dataset format guide
- `DATASET_VERIFICATION_SUMMARY.md` - Dataset status
- `README.md` - Original OpenEA documentation

## ⏱️ Expected Runtime

| Configuration | Time per Dataset |
|---------------|------------------|
| CPU only | ~2 hours |
| GPU (6GB) | ~20 minutes |
| GPU (12GB) | ~15 minutes |

**Total for 7 datasets × 3 reps:**
- CPU: ~42 hours
- GPU: ~7 hours

---

**Quick Help:**
```bash
./quick_setup.sh              # Guided setup
./run_all_experiments.sh      # Run all
tail -f logs/*.log           # Monitor
```
