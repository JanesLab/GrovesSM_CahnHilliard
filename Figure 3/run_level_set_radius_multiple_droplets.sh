#!/bin/bash
#SBATCH -N 1
#SBATCH -o ./Reports/%A/output.%j.out 
#SBATCH --ntasks-per-node=16
#SBATCH --account=janeslab
#SBATCH --time=10:00:00
#SBATCH --mem=300G
#SBATCH --partition=standard
#SBATCH --array=1-40

module load matlab
# seed="1111"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0075_noisy_cohesin/sd_0.25/seed_${seed}"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.008_noisy_cohesin/sd_0.11/individual_seeds"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067"
indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_noisy_cohesin/sd_0.11/"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.04"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.4"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0089_noisy_cohesin"

# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0075_alpha_-0.5_new_IC"
OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p CPC_geometric_array_noisy_cohesin_full_set.txt)

# OPTS=$(sed -n "${SLURM_ARRAY_TASK_ID}"p CPC_geometric_array_with_alpha_change_domain_options_eps_0.0067_large_widths_t_0.4_v2.txt)
contour_level=0
dtout=10
dt=0.000001525878906
nx=512
alpha="0"

CPC=$(echo "$OPTS" | awk '{print $1}')
cohesin=$(echo "$OPTS" | awk '{print $2}')
time=$(echo "$OPTS" | awk '{print $4}')
random=$(echo "$OPTS" | awk '{print $5}')

echo $CPC
echo $cohesin
echo $time
echo $random
# phi_512_19661_1.0e-5__8_CPC_0.3_cohesin_0.09_eps_0.01_alpha_0_domain_0_2

#2112871
# if [[ "$CPC" == "0.15" || "$CPC" == "0.173" ]]; then
#     echo "CPC is either 0.15 or 0.173"

matlab -nodisplay -nosplash -r "cd ..; level_set_radius_multiple_droplets($CPC, $cohesin, 0.0067, '$indir', '$alpha', $nx, $dt, $time, '_alpha_0_domain_0_2_$random', $contour_level);quit;"
# fi
# echo "Done."





