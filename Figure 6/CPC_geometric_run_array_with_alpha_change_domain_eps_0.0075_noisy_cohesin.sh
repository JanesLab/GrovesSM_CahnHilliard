#!/bin/bash
#SBATCH -N 1
#SBATCH -o ../Reports/%A/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=200G
#SBATCH --partition=standard
#SBATCH --array=1-40

echo $(date)
OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p CPC_geometric_array_noisy_cohesin_full_set.txt)
# outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.008_noisy_cohesin/sd_0.11/individual_seeds"
# outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_noisy_cohesin/sd_0.11/"
outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_noisy_cohesin"

mkdir -p $outdir
echo $OPTS
# Load  Julia environment
module load julia/1.9.2
echo "MODULES LOADED"
julia CPC_geometric_run_array_with_alpha_change_domain_eps_0.0075_noisy_cohesin.jl $OPTS

echo "DONE"