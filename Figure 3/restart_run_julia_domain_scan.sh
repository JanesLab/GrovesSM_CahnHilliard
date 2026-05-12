#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/%A/output.%J.out
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=500G
#SBATCH --partition=standard
#SBATCH --array=1-5

R0_originals=(0.18 0.20 0.21 0.22 0.24)
total_time=10
L=2.0
nx=256
t_extra=5.0

R0_original=${R0_originals[$((SLURM_ARRAY_TASK_ID - 1))]}

echo $(date)
echo "Restarting L=${L}, R0=${R0_original}, t_extra=${t_extra}, nx=${nx}"

module load julia/1.11.6
julia julia_restart_domain_size_study.jl ${L} ${R0_original} ${t_extra} ${nx}

echo "DONE"