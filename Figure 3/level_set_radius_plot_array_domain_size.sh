#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/%A/output.%J.out
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=200G
#SBATCH --partition=standard
#SBATCH --array=1-5

echo $(date)

 
R0s=("0.18" "0.2" "0.21" "0.22" "0.24")
total_time=10
R0=${R0s[$((SLURM_ARRAY_TASK_ID - 1))]}
# Map array task ID to domain size
# domain_sizes=(1.0 2.0 4.0)
# L=${domain_sizes[$((SLURM_ARRAY_TASK_ID - 1))]}
L=2.0
Nx="256.0"

epsilon_name="0.02251"
module load matlab
echo "LOADED MATLAB"

indir="/project/g_bme-janeslab/SarahG/julia_out/domain_size_SAV"

# suffix="_periodic_offcenterphi"
echo "Running MATLAB script for R0=$R0, L=$L, epsilon_name=$epsilon_name"
matlab -nodisplay -r "level_set_radius_array_domain_size($R0, '$L', '$Nx', $epsilon_name, '$indir'); exit;"
echo "DONE"
