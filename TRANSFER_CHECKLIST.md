# Transfer Checklist for New Machine

Use this checklist when setting up OpenEA on a new machine.

## Before Transfer

### On Source Machine

- [ ] Verify all datasets are present and validated
  ```bash
  ls datasets/
  python validate_dataset.py datasets/D_W_15K_V2
  ```

- [ ] Check dataset splits exist
  ```bash
  for d in datasets/*/; do ls "$d/721_5fold/1/" 2>/dev/null && echo "✓ $(basename $d)" || echo "✗ $(basename $d)"; done
  ```

- [ ] Create archive (choose one method)
  ```bash
  # Full archive (includes everything)
  tar -czf openea_full.tar.gz OpenEA/
  
  # Or separate datasets (if large)
  tar -czf openea_code.tar.gz --exclude=OpenEA/datasets OpenEA/
  tar -czf openea_datasets.tar.gz OpenEA/datasets/
  ```

- [ ] Note the archive size
  ```bash
  ls -lh openea_*.tar.gz
  ```

## Transfer to New Machine

### Choose Transfer Method

#### Method 1: Git (Recommended if repository is on GitHub)
- [ ] Push to git repository
  ```bash
  git add .
  git commit -m "Prepared for transfer"
  git push
  ```
- [ ] Clone on new machine
  ```bash
  git clone https://github.com/YOUR_USERNAME/OpenEA.git
  ```

#### Method 2: SCP (Secure Copy)
- [ ] Transfer files
  ```bash
  scp openea_full.tar.gz user@remote-server:/path/to/destination/
  ```
- [ ] Extract on remote
  ```bash
  ssh user@remote-server
  cd /path/to/destination
  tar -xzf openea_full.tar.gz
  ```

#### Method 3: rsync (Efficient sync)
- [ ] Sync files
  ```bash
  rsync -avz --progress OpenEA/ user@remote-server:/path/to/OpenEA/
  ```

#### Method 4: Cloud Storage (for very large files)
- [ ] Upload to cloud (Dropbox, Google Drive, AWS S3, etc.)
- [ ] Download on new machine
- [ ] Extract archive

## On New Machine

### Initial Setup

- [ ] Verify conda is installed
  ```bash
  conda --version
  ```
  If not: See SETUP_NEW_MACHINE.md for installation

- [ ] Navigate to OpenEA directory
  ```bash
  cd OpenEA
  ```

- [ ] Make scripts executable
  ```bash
  chmod +x setup_environment.sh run_all_experiments.sh quick_setup.sh
  ```

### Environment Setup

- [ ] Run environment setup
  ```bash
  ./setup_environment.sh
  ```

- [ ] Activate environment
  ```bash
  conda activate openea
  ```

- [ ] Verify TensorFlow installation
  ```bash
  python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
  ```

- [ ] Check GPU availability (if applicable)
  ```bash
  python -c "import tensorflow as tf; print('GPU available:', tf.test.is_gpu_available())"
  nvidia-smi  # Should show GPU info
  ```

### Dataset Verification

- [ ] Check datasets are present
  ```bash
  ls datasets/
  ```

- [ ] Validate one dataset
  ```bash
  python validate_dataset.py datasets/D_W_15K_V2
  ```

- [ ] Check all datasets have splits
  ```bash
  for d in datasets/*/; do 
    if [ -d "$d/721_5fold/1" ]; then 
      echo "✓ $(basename $d)"; 
    else 
      echo "✗ $(basename $d) - MISSING SPLITS"; 
    fi
  done
  ```

### Test Run

- [ ] Run a single test experiment
  ```bash
  cd run
  python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/
  ```

- [ ] Verify test completed successfully
  ```bash
  ls ../output/results/
  ```

- [ ] Check logs
  ```bash
  tail ../logs/*.log
  ```

### Production Run

- [ ] Configure experiment settings (optional)
  ```bash
  nano run_all_experiments.sh  # Edit REPETITIONS, METHOD, etc.
  ```

- [ ] Start batch experiments
  ```bash
  ./run_all_experiments.sh
  ```

- [ ] Monitor progress (in another terminal)
  ```bash
  tail -f logs/experiment_summary_*.txt
  ```

## Post-Run

### Collect Results

- [ ] Check experiment summary
  ```bash
  cat logs/experiment_summary_*.txt
  ```

- [ ] Verify all experiments completed
  ```bash
  grep -c "SUCCESS" logs/experiment_summary_*.txt
  grep -c "FAILED" logs/experiment_summary_*.txt
  ```

- [ ] Archive results
  ```bash
  tar -czf results_$(date +%Y%m%d).tar.gz output/results/ logs/
  ```

- [ ] Transfer results back (if needed)
  ```bash
  scp results_*.tar.gz user@local-machine:/path/to/results/
  ```

## Troubleshooting Checklist

If something goes wrong:

- [ ] Check conda is in PATH
  ```bash
  which conda
  source ~/.bashrc  # or ~/.zshrc
  ```

- [ ] Verify environment exists
  ```bash
  conda env list | grep openea
  ```

- [ ] Check Python version
  ```bash
  python --version  # Should be 3.6.x
  ```

- [ ] Verify TensorFlow
  ```bash
  python -c "import tensorflow; print(tensorflow.__version__)"
  ```

- [ ] Check disk space
  ```bash
  df -h
  ```

- [ ] Monitor memory usage
  ```bash
  free -h
  htop  # or top
  ```

- [ ] Check GPU memory (if using GPU)
  ```bash
  nvidia-smi
  ```

## File Size Reference

Typical file sizes to expect:

| Item | Size (approx) |
|------|---------------|
| OpenEA code | 50 MB |
| Single dataset (15K) | 20-50 MB |
| All datasets (7×15K) | 200-350 MB |
| Results per experiment | 10-100 MB |
| Full archive | 300-500 MB |

## Time Estimates

| Task | Time |
|------|------|
| File transfer (100 MB/s) | 5-30 seconds |
| File transfer (10 MB/s) | 30-300 seconds |
| Environment setup | 10-20 minutes |
| Single test run (GPU) | 15-20 minutes |
| Single test run (CPU) | 1-2 hours |
| Full batch (7 datasets × 3 reps, GPU) | 6-8 hours |
| Full batch (7 datasets × 3 reps, CPU) | 40-50 hours |

## Quick Commands Reference

```bash
# Setup
./setup_environment.sh
conda activate openea

# Validate
python validate_dataset.py datasets/DATASET_NAME

# Test run
cd run && python main_from_args.py ./args/mtranse_args_15K.json D_W_15K_V2 721_5fold/1/

# Full run
cd run && ./run_all_experiments.sh

# Monitor
tail -f logs/*.log

# Results
tar -czf results.tar.gz output/ logs/
```

## Notes

- Make sure to have at least 10 GB free disk space
- GPU is highly recommended (10-20x faster)
- Use `screen` or `tmux` for long-running experiments
- Keep backup of original datasets
- Save experiment logs for troubleshooting

---

**Status:** [ ] Ready to transfer | [ ] Transferred | [ ] Setup complete | [ ] Experiments running | [ ] Complete
