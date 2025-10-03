include("../CH_multigrid_solver_with_alpha_change_domain.jl")
using Dates
date_time = now()

tol = 1e-5
dt = 0.1 * (1 / 256)^2
epsilon = 0.0067

CPC_width = parse.(Float64, ARGS[1])
cohesin_width = parse.(Float64, ARGS[2])
nx = parse.(Int, ARGS[3])
ny = nx
total_time = parse.(Float64, ARGS[4])
# name = ARGS[5] #remove when running with slurm array
# alpha = parse.(Float64, ARGS[5])
alpha = 0 #the below code is obsolete
if alpha == -0.5
    beta = 0.679355124356581
    phi_1 = -1.2074996663997333
    phi_2 = 0.8741663330663997
elseif alpha == -0.1
    beta = 0.7024393586862704
    phi_1 = -1.0349986134211147
    phi_2 = 0.968331946754448
elseif alpha == 0.1
    beta = 0.7059312080025176
    phi_1 = -0.9683319467544478
    phi_2 =1.0349986134211147
elseif alpha == 0.5
    beta = 0.679366220486757
    phi_1 = -0.8741663330663997
    phi_2 = 1.2074996663997333
elseif alpha == 0
    beta = 0
    phi_1 = -1.0
    phi_2 = 1.0
end

max_it = Int.(round(total_time / dt))
ns = 10

println(CPC_width)
println(cohesin_width)
println("starting initialization")
# phi = initialize_geometric_CPC(nx, ny; CPC_width=20, cohesin_width=4)
# outdir = "/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0075_alpha_-0.5_new_IC"
outdir = "/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.4"
# outdir = "/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.04"

# outdir = "/scratch/xpz5km/Cahn_Hilliard_Model/CPC_geometry/CPC_domain_0_2"

println("starting ch solver")
println("cohesin=$(cohesin_width), CPC=$(CPC_width), epsilon=$(epsilon)")
phi = initialize_round_CPC_um(nx, nx, CPC_width=CPC_width, cohesin_width=cohesin_width, domain_width=6.4, c1 = phi_1, c2 = phi_2)
time_passed = @elapsed main_w_alpha(phi, nx, tol, outdir, dt=dt, gam=epsilon, max_it=max_it, print_mass=false, print_e=false, overwrite=false, suffix="_CPC_$(CPC_width)_cohesin_$(cohesin_width)_eps_$(epsilon)_domain_0_2", check_dir=false, alpha=0)
open("/home/xpz5km/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, ["CPC_geometry_domain_0_2_e_0.0067" "Julia" nx epsilon dt tol max_it 10000 time_passed], ",")
end



