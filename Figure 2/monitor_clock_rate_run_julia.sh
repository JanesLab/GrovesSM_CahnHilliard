#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/julia/%A/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=30:00:00
#SBATCH --mem=500G
#SBATCH --partition=standard
#SBATCH --array=1-3

echo $(date)

# Capture initial CPU info
echo "=== CPU SPECIFICATIONS ==="
lscpu | grep -E "Model name|CPU max MHz|CPU min MHz|Socket"
echo ""

OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p opts_Julia_redo_v4.txt)
echo $OPTS

outdir="/project/g_bme-janeslab/SarahG/spinodal_decomp_06_2025/out_julia"
mkdir -p $outdir

# Load Julia environment
module load julia/1.11.6
echo "MODULES LOADED"

boundary=$(echo "$OPTS" | awk '{print $2}')
print=$(echo "$OPTS" | awk '{print $3}')
SLURM_ID=${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}

if [[ "$print" == "true"  ]]; then
    # Start monitoring clock rate in background
    (
        while true; do
            grep MHz /proc/cpuinfo | head -1
            sleep 2
        done > "${outdir}/cpu_freq_${SLURM_ID}.log" &
    )
    MONITOR_PID=$!
    
    julia ./CahnHilliard_Julia_solvers/run_spinodal_decomp_HPC.jl $OPTS $SLURM_ID
    
    # Stop monitoring
    kill $MONITOR_PID 2>/dev/null
    
    # Report average clock rate
    echo ""
    echo "=== CLOCK RATE DURING SIMULATION ==="
    if [ -f "${outdir}/cpu_freq_${SLURM_ID}.log" ]; then
        awk '{sum+=$3; count++} END {print "Average CPU MHz: " sum/count}' "${outdir}/cpu_freq_${SLURM_ID}.log"
    fi
fi

echo "DONE"