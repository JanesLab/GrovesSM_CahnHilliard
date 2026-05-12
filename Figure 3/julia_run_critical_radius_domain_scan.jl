# Run droplet critical radius simulations across different domain sizes,
# keeping epsilon, R0, nx, and dt fixed so that the droplet is the same
# absolute physical size but a smaller fraction of the larger domains.
#
# Domain sizes tested: [0,1], [0,2], [0,4]
# epsilon is anchored to M=8 mesh points at nx=128 on a [0,1] domain.
#
# ARGS: L  R0  total_time
#   L           = right edge of domain (left is always 0); e.g. 1, 2, or 4
#   R0          = initial droplet radius in physical units; e.g. 0.1
#   total_time  = simulation duration in characteristic time units; e.g. 10

using Dates
using DelimitedFiles

include("../spinodal_decomp/CahnHilliard_Julia_solvers/CahnHilliard_SAV.jl")

date_time = now()

# --- Parse arguments ---
L          = parse(Float64, ARGS[1])   # domain size: [0, L] x [0, L]
R0_original         = parse(Float64, ARGS[2])   # droplet radius (physical units)
total_time = parse(Float64, ARGS[3])   # simulation duration
nx         = parse(Float64, ARGS[4])   # grid resolution (number of points along one dimension)
# --- Fixed numerical parameters ---
# nx  = 128
dt  = 2.5e-5
# tol = 1e-6
# solver_iter = 10000
dt_out      = 10   

max_it = Int(round(total_time / dt))
# ref epsilon = 0.011257 for figure 3
epsilon = 0.011257 * L
epsilon2 = epsilon^2
println("R0 original = $R0_original (physical units)")
R0 = R0_original * L   # scale R0 with domain size so droplet is same physical size across all domains
println("Domain: [0, $L] x [0, $L]")
println("nx = $nx,  h = $(L/nx)")
println("R0 = $R0 (physical units)")
println("epsilon = $(round(epsilon, sigdigits=5))  (fixed, anchored to M=8 at nx=128, L=1)")
println("epsilon2 = $(round(epsilon2, sigdigits=5))")
println("dt = $dt,  max_it = $max_it,  total_time = $total_time")

# --- Domain-aware droplet initialization ---
# The droplet is centered at (L/2, L/2) with radius R0 in physical units.
# Coordinates span [0, L]; interface width set by epsilon (physical).
function init_droplet_domain(nx, ny, L; R0=0.1, epsilon=0.01)
    h = L / nx
    x = h .* (0:nx-1)
    y = h .* (0:ny-1)
    xx = [xi for xi in x, _ in 1:ny]
    yy = [yi for _ in 1:nx, yi in y]
    center = L / 2
    R = @. sqrt((xx - center)^2 + (yy - center)^2)
    return @. tanh((R0 - R) / (sqrt(2) * epsilon))
end

# --- Initialize phi ---
println("Initializing phi...")
phi0 = init_droplet_domain(nx, nx, L; R0=R0, epsilon=epsilon)

# --- Output directory and file prefix ---
outdir = "/project/g_bme-janeslab/SarahG/julia_out/domain_size_SAV_longertimelimit"
mkpath(outdir)

label    = "nx$(nx)_L$(L)_R0$(R0)_eps$(round(epsilon, sigdigits=4))"
pathname = "$(outdir)/$(label)_"   # CahnHilliard_SAV appends "phi.csv"

# --- Run solver ---
println("Starting CahnHilliard_SAV solver...")
time_passed = @elapsed begin
    t_out, phi_t, mass_t, E_t = CahnHilliard_SAV(
        phi0;
        t_iter      = max_it,
        dt          = dt,
        # solver_iter = solver_iter,
        # tol         = tol,
        dt_out      = dt_out,
        epsilon2    = epsilon2,
        boundary    = "neumann",
        domain      = [L, 0.0, L, 0.0],   # [xright, xleft, yright, yleft]
        printphi    = true,
        pathname    = pathname,
        Mob = L^2
    )
end

# --- Save mass and energy time series ---
writedlm("$(outdir)/mass_$(label).csv",   mass_t, ",")
writedlm("$(outdir)/energy_$(label).csv", E_t,    ",")
writedlm("$(outdir)/time_$(label).csv",   t_out,  ",")

println("Finished in $(round(time_passed, digits=1)) seconds.")

# --- Append to job specs log ---
open("/home/xpz5km/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, [date_time "domain_size_study" "Julia_SAV" nx L R0 epsilon dt tol max_it time_passed], ",")
end
