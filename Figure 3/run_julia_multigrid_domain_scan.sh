#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/%A/output.%J.out
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=50:00:00
#SBATCH --mem=300G
#SBATCH --partition=standard
#SBATCH --array=1-5
 
# Domain size study: fixed epsilon, R0, nx — varying domain [0,L]
# Each array task runs one domain size.
# Arguments passed to julia: L  R0  total_time
 
R0_originals=(0.09 0.10 0.105 0.11 0.12)  # R0 values for L=1.0; will be scaled by L in julia script
total_time=10
 
# Map array task ID to domain size
# domain_sizes=(2.0 4.0)
# Nx=(256 512)  # grid resolution (number of points along one dimension)
# L=${domain_sizes[$((SLURM_ARRAY_TASK_ID - 1))]}
# nx=${Nx[$((SLURM_ARRAY_TASK_ID - 1))]}
L=2.0
nx=256
R0_original=${R0_originals[$((SLURM_ARRAY_TASK_ID - 1))]} 

echo $(date)
echo "Task ${SLURM_ARRAY_TASK_ID}: L=${L}, R0 original=${R0_original}, total_time=${total_time}, nx=${nx}"
 
module load julia/1.11.6
echo "MODULES LOADED"

# R0 = RO_original * L
# R0=$(echo "$R0_original * $L" | bc -l) 
julia julia_run_critical_radius_domain_scan.jl ${L} ${R0_original} ${total_time} ${nx}
 
echo "DONE"