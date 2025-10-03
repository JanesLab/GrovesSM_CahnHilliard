include("../CH_multigrid_solver_with_alpha_change_domain.jl")
using Dates
date_time = now()

tol = 1e-5
dt = 0.1 * (1 / 256)^2
# epsilon = 0.0089
epsilon = 0.0067
CPC_width = parse.(Float64, ARGS[1])
cohesin_width = parse.(Float64, ARGS[2])
nx = parse.(Int, ARGS[3])
ny = nx
total_time = parse.(Float64, ARGS[4])
max_it = Int.(round(total_time / dt))
ns = 10
seed = parse.(Int, ARGS[5])
name = ARGS[6]
println(CPC_width)
println(cohesin_width)
println("starting initialization")
# seed = 4444
# outdir = "/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.008_noisy_cohesin/sd_0.11/individual_seeds"
# outdir = "/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_noisy_cohesin/sd_0.11"
outdir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.04"

println("starting ch solver")
println("cohesin=$(cohesin_width), CPC=$(CPC_width), epsilon=$(epsilon)")
# phi = initialize_round_CPC_um(nx, nx, CPC_width=CPC_width, cohesin_width=cohesin_width, domain_width=6.4)
phi = initialize_round_CPC_noisy_cohesin_um(nx, nx, CPC_width=CPC_width, cohesin_width=cohesin_width, domain_width=6.4, sd = 0.11, seed = seed)

# alpha = 0_CPC_$(CPC_width)_cohesin_$(cohesin_width)_eps_$(epsilon)_alpha_$(alpha)_domain_0_2_$(seed)
time_passed = @elapsed main_w_alpha(phi, nx, tol, outdir, dt=dt, gam=epsilon, max_it=max_it, print_mass=false, print_e=false, overwrite=false, suffix=name, check_dir=false, alpha=0)
open("/home/xpz5km/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, ["CPC_geometry_domain_0_2_e_0.0067" "Julia" nx epsilon dt tol max_it 10000 time_passed], ",")
end



