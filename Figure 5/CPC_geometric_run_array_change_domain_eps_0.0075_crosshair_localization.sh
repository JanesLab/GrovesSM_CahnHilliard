#!/bin/bash
#SBATCH -N 1
#SBATCH -o ../Reports/%A/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=200G
#SBATCH --partition=standard
#SBATCH --array=1-87

echo $(date)
OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p CPC_geometric_array_change_domain_options_eps_0.0075_crosshair_localization.txt)
echo $OPTS
# Load  Julia environment
module load julia/1.9.2
echo "MODULES LOADED"
julia CPC_geometric_run_array_change_domain_eps_0.0075_crosshair_localization.jl $OPTS

echo "DONE"