
using Dates
date_time = now()
include("../CH_multigrid_solver.jl")
#ARGS: [R0, M, total_time]
nx = 128
tol = 1e-6
dt = 2.5e-5
R0 =parse.(Float64, ARGS[1])
M = parse.(Float64, ARGS[2]) # M = 8 is eps0 = 0.015
gam = M * (1 / 128) / (2 * sqrt(2) * atanh(0.9))
total_time = parse.(Int, ARGS[3])
max_it = Int.(total_time/dt)
max_it_CH = 10000
ns = 10
println(R0)
println("starting initialization")
phi = initialization(nx, nx, method="droplet", h=1 / 128, R0 = R0, gam = gam)
# outdir = "/scratch/xpz5km/Cahn_Hilliard_Model/julia_out/critical_radius_updated_IC"
outdir = "/project/g_bme-janeslab/SarahG/julia_out/critical_radius_updated_IC"
println("starting ch solver")

time_passed = @elapsed main(phi, nx, tol, outdir, dt=dt, gam=gam, max_it=max_it, print_mass=false, print_e=false, overwrite=false, print_r=false, suffix="_R0_$(R0)_eps_$(round(gam, sigdigits = 5))", check_dir=false)
open("/home/xpz5km/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, [date_time, "critical_radius_R0_$(R0)_eps_$(round(gam, sigdigits = 5))" "Julia" nx gam dt tol max_it max_it_CH time_passed], ",")
end
