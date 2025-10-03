#!/bin/bash
#SBATCH -N 1
#SBATCH -o ../Reports/%A/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=28:00:00
#SBATCH --mem=500G
#SBATCH --partition=standard
#SBATCH --array=1

echo $(date)
OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p CPC_geometric_array_with_alpha_change_domain_options_eps_0.0067_large_widths_t_0.4_v3.txt)
echo $OPTS
outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.4"

# outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0089"
mkdir -p $outdir
# Load  Julia environment
module load julia/1.9.2
echo "MODULES LOADED"
julia CPC_geometric_run_array_with_alpha_change_domain_eps_0.0075.jl $OPTS

echo "DONE"