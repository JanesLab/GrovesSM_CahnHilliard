using DelimitedFiles
using Dates
using BenchmarkTools
using Printf
# import Pkg; Pkg.add("FFTW")
# Pkg.add("Plots")
# Pkg.add("CSV")
# Pkg.add("LinearAlgebra")
# Pkg.add("BenchmarkTools")
# Pkg.add("StaticArrays")
# Pkg.add("Printf")

include("CahnHilliard_NMG.jl")
include("CahnHilliard_SAV.jl")
include("ch_movie_from_file.jl")

indir = "./IC/"
outdir = "/project/g_bme-janeslab/SarahG/spinodal_decomp_06_2025"

GridSize = parse.(Int, ARGS[1])
boundary = ARGS[2]
print = lowercase(ARGS[3]) == "true"
method = ARGS[4]
note= ARGS[5]
SLURM_ID=ARGS[6]
# if note == "50p"
#     note = ""
# end

nx = GridSize
ny = nx

n_relax = 4
h = 1 / GridSize
m = 8
epsilon = m * h / (2 * sqrt(2) * atanh(0.9))

printphi = true
#use neumann-smoothed IC for both periodic and neumann sims
phi0 = initialization_from_file("$(indir)initial_phi_$(GridSize)_smooth_n_relax_$(n_relax)_$(note)_neumann.csv", GridSize, GridSize, delim=',', transpose_matrix=false)
dt = 5.5e-7
max_it = 20000

if print
    dt_out = 10
else
    dt_out = 20000
end

id = @sprintf("%s_Julia_%d_dt_%.2e_Nx_%d_%s_dtout_%d%s", method, max_it, dt, GridSize, boundary, dt_out, note)
pathname = @sprintf("%s/out_julia/%s_", outdir, id)
date_time = now()

if method == "NMG"
    result, elapsed_time, mem_allocated, gc_time, memory_counters = @timed CahnHilliard_NMG(phi0; t_iter=max_it, dt=dt, dt_out=dt_out, m=m, boundary=boundary, printphi=printphi, pathname=pathname)
    open("$(outdir)/Job_specs_updated.csv", "a", lock=false) do f
        writedlm(f, [Dates.format(date_time, "mm/dd/yyyy HH:MM:SS") "Julia" method GridSize epsilon dt 1e-5 max_it 1e4 dt_out print boundary pathname elapsed_time (mem_allocated/1e6) SLURM_ID note], ",")
    end
elseif method == "SAV"
    result, elapsed_time, mem_allocated, gc_time, memory_counters = @timed CahnHilliard_SAV(phi0; t_iter=max_it, dt=dt, dt_out=dt_out, m=m, boundary=boundary, printphi=printphi, pathname=pathname)
    open("$(outdir)/Job_specs_updated.csv", "a", lock=false) do f
        writedlm(f, [Dates.format(date_time, "mm/dd/yyyy HH:MM:SS") "Julia" method GridSize epsilon dt "NaN" max_it "NaN" dt_out print boundary pathname elapsed_time (mem_allocated/1e6) SLURM_ID note], ",")
    end
end

if print
    println("Printing out results...")
    t_out = result[1]
    phi_t = result[2]
    mass_t = result[3]
    E_t = result[4]
    open("$(pathname)t_out.csv", "w", lock=false) do f
        writedlm(f, t_out, " ")
    end
    open("$(pathname)mass.csv", "w", lock=false) do f
        writedlm(f, mass_t, " ")
    end
    open("$(pathname)energy.csv", "w", lock=false) do f
        writedlm(f, E_t, " ")
    end
    # t_out = readdlm("$(pathname)t_out.csv", ',', Float64)
    ch_movie_from_file("$(pathname)phi.csv", t_out, GridSize; dtframes=1, filename="$(pathname)movie", filetype="mp4", colorbar_type="default")
end