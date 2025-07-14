using DelimitedFiles
using Dates
using BenchmarkTools
using Printf
include("CahnHilliard_NMG.jl")
include("CahnHilliard_SAV.jl")
include("ch_movie_from_file.jl")

boundary = "periodic"
indir = "./IC/"
outdir = "./output/output_julia/n_relax_test/$(boundary)"
GridSize = 128
total_time = 0.02
h = 1 / GridSize
m = 8
epsilon = m * h / (2 * sqrt(2) * atanh(0.9))

printphi = true
dt_out = 10
dt = 5.5e-6
max_it = 2000

# smoothed IC were incorrect for 2 and 16 so I am redoing those with v2
for n_relax = [0, 1, 2, 4, 8, 16]
    println(n_relax)
    if n_relax == 0
        phi0 = initialization_from_file("$(indir)initial_phi_$(GridSize)_50p.csv", GridSize, GridSize, delim=',', transpose_matrix=false)
    else
        phi0 = initialization_from_file("$(indir)initial_phi_$(GridSize)_smooth_n_relax_$(n_relax)_50p_$(boundary)_v2.csv", GridSize, GridSize, delim=',', transpose_matrix=false)
    end

    ########
    # SAV
    ########
    method = "SAV"
    println(method)
    pathname = @sprintf("%s%s_%s_Julia_%d_dt_%.2e_Nx_%d_n_relax_%d_", outdir, method, boundary, max_it, dt, GridSize, n_relax)

    date_time = now()
    result, elapsed_time, mem_allocated, gc_time, memory_counters = @timed CahnHilliard_SAV(phi0; t_iter=max_it, dt=dt, dt_out=dt_out, m=m, boundary=boundary, printphi=printphi, pathname=pathname)
    open("./Job_specs.csv", "a", lock=false) do f
        writedlm(f, [Dates.format(date_time, "mm/dd/yyyy HH:MM:SS") "spinodal_decomp_smoothed_nrelax_scan" "Julia" method GridSize epsilon dt 1e-5 max_it 1e4 pathname elapsed_time mem_allocated / 1e6], ",")
    end

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
    # ch_movie_from_file("$(pathname)phi.csv", t_out, 128; dtframes=1, filename="$(pathname)movie", filetype="mp4", colorbar_type="default")
    ################
    # NMG
    ################
    method = "NMG"
    println(method)

    pathname = @sprintf("%s%s_%s_Julia_%d_dt_%.2e_Nx_%d_n_relax_%d_", outdir, method, boundary, max_it, dt, GridSize, n_relax)
    date_time = now()
    result, elapsed_time, mem_allocated, gc_time, memory_counters = @timed CahnHilliard_NMG(phi0; t_iter=max_it, dt=dt, dt_out=dt_out, m=m, boundary=boundary, printphi=printphi, pathname=pathname)
    open("./Job_specs.csv", "a", lock=false) do f
        writedlm(f, [Dates.format(date_time, "mm/dd/yyyy HH:MM:SS") "spinodal_decomp_smoothed_nrelax_scan" "Julia" method GridSize epsilon dt 1e-5 max_it 1e4 pathname elapsed_time mem_allocated / 1e6], ",")
    end
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
    # ch_movie_from_file("$(pathname)phi.csv", t_out, 128; dtframes=1, filename="$(pathname)movie", filetype="mp4", colorbar_type="default")

end