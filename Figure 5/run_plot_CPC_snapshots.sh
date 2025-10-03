#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/%A/output.%J.out
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=250G
#SBATCH --partition=standard

#3035034
#4156068
echo $(date)
# Load  Julia environment
module load miniforge/24.3.0-py3.11
echo "MODULES LOADED"
python plot_CPC_snapshots.py

echo "DONE"