#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=250G
#SBATCH --partition=standard


indir="/project/g_bme-janeslab/SarahG/julia_out/critical_radius_updated_IC"
dtout=10
dt=2.5e-5
nx=128
frame_rate=40

name="phi_128_400000_1.0e-6__R0_0.3_eps_0.10131"

echo $(date)
module load matlab
echo "LOADED MATLAB"

# Run Matlab single core program
matlab -nodisplay -r "CHplotting_function('$indir', '$name', $dt, $dtout, '_fast', $frame_rate);quit;"

# suffix=""
# matlab -nodisplay -r "plot_single_timepoint_heatmap(1, '$indir','$name', '$suffix');quit;"
# matlab -nodisplay -r "plot_IC_heatmap('$indir','$name', '$suffix', 512, 50);quit;"

echo "Done."
