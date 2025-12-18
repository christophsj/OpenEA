#!/bin/bash
# OpenEA Batch Experiment Runner
# Runs experiments on all datasets with multiple repetitions

set -e  # Exit on error

# Configuration
REPETITIONS=3
METHOD="RDGCN"
CONFIG_FILE="./args/rdgcn_args_15K.json"
SPLIT_PATH="721_5fold/1/"
DATASET_DIR="../datasets"
OUTPUT_BASE="../output/results"
LOG_DIR="../logs"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "=================================================="
    echo "$1"
    echo "=================================================="
    echo ""
}

# Check if we're in the run directory
if [ ! -d "args" ]; then
    print_error "Please run this script from the 'run' directory"
    exit 1
fi

# Check if conda environment is activated
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    print_warning "No conda environment activated"
    print_info "Attempting to activate 'openea' environment..."
    source "$(conda info --base)/etc/profile.d/conda.sh" 2>/dev/null || true
    conda activate openea 2>/dev/null || print_warning "Could not activate environment. Proceeding anyway..."
fi

# Create log directory
mkdir -p "$LOG_DIR"

# Get list of datasets
print_info "Scanning for datasets in: $DATASET_DIR"
DATASETS=()
if [ -d "$DATASET_DIR" ]; then
    for dataset_path in "$DATASET_DIR"/*/ ; do
        dataset_name=$(basename "$dataset_path")
        # Check if it has the required split folder
        if [ -d "$dataset_path/$SPLIT_PATH" ]; then
            DATASETS+=("$dataset_name")
        else
            print_warning "Skipping $dataset_name (no $SPLIT_PATH folder found)"
        fi
    done
else
    print_error "Dataset directory not found: $DATASET_DIR"
    exit 1
fi

if [ ${#DATASETS[@]} -eq 0 ]; then
    print_error "No valid datasets found in $DATASET_DIR"
    exit 1
fi

print_success "Found ${#DATASETS[@]} datasets: ${DATASETS[*]}"

# Summary
print_header "Experiment Configuration"
echo "Method: $METHOD"
echo "Config: $CONFIG_FILE"
echo "Datasets: ${DATASETS[*]}"
echo "Repetitions: $REPETITIONS"
echo "Split: $SPLIT_PATH"
echo "Output: $OUTPUT_BASE"
echo ""

# Ask for confirmation
read -p "Start experiments? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Experiments cancelled"
    exit 0
fi

# Calculate total experiments
TOTAL_EXPERIMENTS=$((${#DATASETS[@]} * REPETITIONS))
CURRENT_EXPERIMENT=0
START_TIME=$(date +%s)

print_header "Starting Experiments"
echo "Total experiments: $TOTAL_EXPERIMENTS"
echo "Start time: $(date)"
echo ""

# Create summary file
SUMMARY_FILE="$LOG_DIR/experiment_summary_$(date +%Y%m%d_%H%M%S).txt"
echo "OpenEA Batch Experiment Summary" > "$SUMMARY_FILE"
echo "================================" >> "$SUMMARY_FILE"
echo "Start time: $(date)" >> "$SUMMARY_FILE"
echo "Method: $METHOD" >> "$SUMMARY_FILE"
echo "Datasets: ${DATASETS[*]}" >> "$SUMMARY_FILE"
echo "Repetitions: $REPETITIONS" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Run experiments
for dataset in "${DATASETS[@]}"; do
    for rep in $(seq 1 $REPETITIONS); do
        CURRENT_EXPERIMENT=$((CURRENT_EXPERIMENT + 1))
        
        print_header "Experiment $CURRENT_EXPERIMENT/$TOTAL_EXPERIMENTS"
        print_info "Dataset: $dataset"
        print_info "Repetition: $rep/$REPETITIONS"
        
        # Create log file
        LOG_FILE="$LOG_DIR/${dataset}_rep${rep}_$(date +%Y%m%d_%H%M%S).log"
        
        # Run experiment
        echo "Running: python main_from_args.py $CONFIG_FILE $dataset $SPLIT_PATH"
        echo ""
        
        EXP_START=$(date +%s)
        
        if python main_from_args.py "$CONFIG_FILE" "$dataset" "$SPLIT_PATH" 2>&1 | tee "$LOG_FILE"; then
            EXP_END=$(date +%s)
            EXP_DURATION=$((EXP_END - EXP_START))
            
            print_success "Completed in ${EXP_DURATION}s"
            echo "[$dataset Rep $rep] SUCCESS - Duration: ${EXP_DURATION}s" >> "$SUMMARY_FILE"
        else
            EXP_END=$(date +%s)
            EXP_DURATION=$((EXP_END - EXP_START))
            
            print_error "Failed after ${EXP_DURATION}s"
            echo "[$dataset Rep $rep] FAILED - Duration: ${EXP_DURATION}s" >> "$SUMMARY_FILE"
        fi
        
        echo "Log saved to: $LOG_FILE"
        echo ""
    done
done

# Calculate total time
END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))
HOURS=$((TOTAL_DURATION / 3600))
MINUTES=$(((TOTAL_DURATION % 3600) / 60))
SECONDS=$((TOTAL_DURATION % 60))

# Final summary
print_header "All Experiments Complete!"
echo "End time: $(date)" >> "$SUMMARY_FILE"
echo "Total duration: ${HOURS}h ${MINUTES}m ${SECONDS}s" >> "$SUMMARY_FILE"

print_info "Total experiments: $TOTAL_EXPERIMENTS"
print_info "Total duration: ${HOURS}h ${MINUTES}m ${SECONDS}s"
print_info "Average per experiment: $((TOTAL_DURATION / TOTAL_EXPERIMENTS))s"
echo ""
print_info "Summary saved to: $SUMMARY_FILE"
print_info "Logs saved to: $LOG_DIR"
print_info "Results saved to: $OUTPUT_BASE"
echo ""

print_success "All done! 🎉"
