#%% FIGURE 2 GENERATING DIFFERENT IC FOR SPINODAL DECOMPOSITION

#%%
using DelimitedFiles
using Dates

#use the official final code for smoothing
include("CahnHilliard_Julia_solvers/nmg_solver.jl")
include("CahnHilliard_Julia_solvers/relax.jl")

outdir = ""

#%%
# tol = 1e-6
nx = 128
ny = nx
perc = "50p"

date_time = now()

using Random
Random.seed!(1234)

function biased_spin_matrix(nx, p_plus=0.75)
    total = nx * nx
    n_plus = round(Int, p_plus * total)
    n_minus = total - n_plus

    # Create the array
    values = vcat(fill(1.0, n_plus), fill(-1.0, n_minus))
    shuffle!(values)

    # Reshape into matrix
    return reshape(values, nx, nx)
end

if perc == "25p"
    p_plus = 0.25
elseif perc == "50p"
    p_plus = 0.5
elseif perc == "75p"
    p_plus = 0.75
end
# phi = biased_spin_matrix(nx, p_plus)
# writedlm("$(outdir)$(perc)/initial_phi_$(nx)_$(perc).csv", phi, ',')
#%%
n_relax = 4
boundary = "periodic"

domain_left = 0
domain_right = 1
tol = 1e-6
dt = 6.25e-6
m = 8
epsilon = m * (1 / 128) / (2 * sqrt(2) * atanh(0.9))
Cahn = epsilon^2  # ϵ^2 defined as a global variable

phi = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_$(perc).csv", nx, nx)
sc, smu = source(phi, nx, ny, dt, domain_right, domain_left, domain_right, domain_left, boundary)
mu = zeros(Float64, nx, ny)
relax!(phi, mu, sc, smu, nx, nx, n_relax, domain_right, domain_left, domain_right, domain_left, dt, Cahn, boundary)

# phi_smooth, mu_smooth = relax(phi, mu, sc, smu, nx, nx, n_relax, domain_right, domain_left, domain_right, domain_left, dt, Cahn, boundary)
writedlm("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary)_v2.csv", phi, ',')


#%% visualize the initial condition from file
# import Pkg;
# Pkg.add("Plots");
using Plots
using DelimitedFiles
perc = "50p"
nx = 128
boundary = "periodic"
n_relax = 16
phi_smooth = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary)_v2.csv", nx, nx)
gr()
heatmap(1:size(phi_smooth, 1),
    1:size(phi_smooth, 2), phi_smooth,
    c=cgrad([:blue, :white, :red]),
    title="Initial condition for phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary)",
    aspect_ratio=1,
    clim=(-1, 1),
    xlims=(1, nx),
    ylims=(1, nx))

#%% comparing v1 and v2 for different levels of smoothing
using Plots
using DelimitedFiles
perc = "50p"
nx = 128
boundary = "periodic"
n_relax = 4
phi_smooth_v1 = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary).csv", nx, nx)
phi_smooth_v2 = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary)_v2.csv", nx, nx)

gr()
heatmap(phi_smooth_v1 - phi_smooth_v2,
    c=cgrad([:blue, :white, :red]),
    title="Initial condition for phi_$(nx)_smooth_n_relax_$(n_relax)_$(perc)_$(boundary)",
    aspect_ratio=1,
    clim=(-1, 1),
    xlims=(1, nx),
    ylims=(1, nx))


#%% compare different levels of smoothing
perc = "50p"
nx = 128
boundary = "neumann"
smooth1 = 1
smooth2 = 16
phi_smooth_1 = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(smooth1)_$(perc)_$(boundary)_v2.csv", nx, nx)
phi_smooth_2 = initialization_from_file("$(outdir)$(perc)/initial_phi_$(nx)_smooth_n_relax_$(smooth2)_$(perc)_$(boundary)_v2.csv", nx, nx)

gr()
heatmap(phi_smooth_1 - phi_smooth_2,
    c=cgrad([:blue, :white, :red]),
    title="n = $(smooth1) - n = $(smooth2)",
    aspect_ratio=1,
    clim=(-1, 1),
    xlims=(1, nx),
    ylims=(1, nx))


#%%

nx = 128
dt = 5.5e-6
n_relax = 4
ny = nx
tol = 1e-5
m = 8
epsilon = m * (1 / 128) / (2 * sqrt(2) * atanh(0.9))

max_it = 2000
total_time = max_it * dt
date_time = now()
name = "MG_$(max_it)_dt_$(dt)_Nx_$(nx)_n_relax_$(n_relax)_eps_$(epsilon)"
phi = initialization_from_file("$(indir)initial_phi_$(nx)_smooth_n_relax_$(n_relax).csv", nx, nx)
date_time = now()
time_passed = @elapsed multigrid_solver(phi, nx, tol, outdir, ns=10, dt=dt, epsilon=epsilon, max_it=max_it, print_mass=false, print_e=false, overwrite=false, print_r=false, print_phi=false, suffix=name, check_dir=false)
open("/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/Job_specs.csv", "a", lock=false) do f
    writedlm(f, [date_time "spinodal_smoothed_no_print" "Julia" nx epsilon dt tol max_it 10000 time_passed], ",")
end