using Dates
function initialize_two_halves(nx, ny; R0=0.1, gam=0.01)
    phi = zeros(Float64, nx, ny)
    h = 1/nx
    x = h .* (0:nx-1)
    y = h .* (0:ny-1)
    xx, yy = meshgrid(x, y)
    x_center = 0.5
    y_center1 = 0.0
    y_center2 = 1.0

    R1 = @. sqrt((xx - x_center)^2 + (yy - y_center1)^2)
    R2 = @. sqrt((xx - x_center)^2 + (yy - y_center2)^2)

    #the +1 is necessary because we are superimposing two phase fields and the background of both is -1, so everything with be 1 less than we want. 
    phi = @.tanh((R0 .- R1) / (sqrt(2) * gam)) .+ @.tanh((R0 .- R2) / (sqrt(2) * gam)) .+ 1

    return phi
end

date_time = now()
include("../spinodal_decomp/CahnHilliard_Julia_solvers/CahnHilliard_NMG.jl")
#ARGS: [R0, M, total_time]
nx = 128
tol = 1e-6
dt = 2.5e-5
R0 =parse.(Float64, ARGS[1])
M = parse.(Float64, ARGS[2]) # M = 8 is eps0 = 0.015
gam = M * (1 / nx) / (2 * sqrt(2) * atanh(0.9))
total_time = parse.(Int, ARGS[3])
max_it = Int.(total_time/dt)
max_it_CH = 10000
ns = 10
println(R0)
println("starting initialization")
phi0 = initialize_two_halves(nx, nx, R0 = R0, gam = gam)
# outdir = "/scratch/xpz5km/Cahn_Hilliard_Model/julia_out/critical_radius_updated_IC"
outdir = "/project/g_bme-janeslab/SarahG/julia_out/critical_radius_alt_IC/phi_$(nx)_$(max_it)_$(tol)__R0_$(R0)_eps_$(round(gam, sigdigits = 5))_two_halves"
println("starting ch solver")

time_passed = @elapsed CahnHilliard_NMG(phi0; t_iter=max_it, dt=dt, tol=tol, dt_out=ns, epsilon2=gam^2, boundary="periodic", printres=false, printphi=true, pathname=outdir)

# time_passed = @elapsed multigrid_solver_with_periodic(phi, nx, tol, outdir, dt=dt, epsilon=gam, max_it=max_it, print_mass=false, print_e=false, overwrite=false, print_r=false, suffix="_R0_$(R0)_eps_$(round(gam, sigdigits = 5))_two_halves", check_dir=false)
open("/home/xpz5km/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, [date_time, "critical_radius_R0_$(R0)_eps_$(round(gam, sigdigits = 5))_two_halves" "Julia" nx gam dt tol max_it max_it_CH time_passed], ",")
end
