import CHsolvers as ch
import pandas as pd
import os
from datetime import datetime
import numpy as np
import sys

indir = "./IC/"
outdir = "/project/g_bme-janeslab/SarahG/spinodal_decomp_06_2025/"


if True:
    GridSize = int(sys.argv[1])
    boundary = sys.argv[2]
    print_results = sys.argv[3] == "true"
    method = sys.argv[4]
    if len(sys.argv )>4:
        SLURM_ID = sys.argv[5]
    if len(sys.argv)>5:
        note = sys.argv[6]
    else:
        note = ""
else:
    GridSize = 128
    boundary = "periodic"
    print = True
    method = "SAV"

n_relax = 4
h = 1/GridSize
m = 8
epsilon = m * h / (2 * np.sqrt(2) * np.arctanh(0.9))

printphi = True
#use neumann-smoothed IC for both periodic and neumann sims

phi0 = np.loadtxt(
    f"{indir}initial_phi_{GridSize}_smooth_n_relax_{n_relax}_{note}_neumann.csv", delimiter=",")

dt = 5.5E-06



date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

if method == "NMG":
    print("Running NMG...")
    max_it = 20
    if print_results:
        dt_out = 1
    else:
        dt_out = 20
    pathname = f"{outdir}/{method}_Python_{max_it}_dt_{dt:.2e}_Nx_{GridSize}_{boundary}_dtout_{dt_out}{note}"

    # note that if using the time_and_mem decorator (in CahnHilliard_NMG), it will return a results dictionary.
    # TODO remove decorator for final package
    results_dict = ch.NMG.CahnHilliard_NMG(phi0, t_iter=max_it, dt=dt, dt_out=dt_out, m=m,
                                        boundary=boundary, printphi=printphi, printres=True, pathname=pathname)
elif method == "SAV":
    print("Running SAV...")

    max_it = 2000
    if print_results:
        dt_out = 10
    else:
        dt_out = 2000
    pathname = f"{outdir}/{method}_Python_{max_it}_dt_{dt:.2e}_Nx_{GridSize}_{boundary}_dtout_{dt_out}{note}"

    results_dict = ch.SAV.CahnHilliard_SAV(phi0, t_iter=max_it, dt=dt, dt_out=dt_out, m=m,
                                        boundary=boundary, printphi=printphi, printres=True, pathname=pathname)

# t_out, phi_t, delta_mass_t, E_t
# rename results_dict keys from results1, results2, etc. to t_out, phi_t, delta_mass_t, E_t
if print_results:
    results_dict["t_out"] = results_dict.pop("results1")
    results_dict["phi_t"] = results_dict.pop("results2")
    results_dict["mass_t"] = results_dict.pop("results3")
    results_dict["E_t"] = results_dict.pop("results4")

    # Save results
    np.savetxt(f"{pathname}t_out.csv", results_dict["t_out"], delimiter=",")
    np.savetxt(f"{pathname}mass.csv",
            results_dict["mass_t"], delimiter=",")
    np.savetxt(f"{pathname}energy.csv", results_dict["E_t"], delimiter=",")

#date,language,method,GridSize,epsilon,dt,tol,t_iter,solver_iter,dt_out,
# print,boundary,pathname,elapsed_time(s),mem_allocated(Gb)

T = {}
T['date'] = date_time
T['language'] = "Python"
T['method'] = method
T['GridSize'] = GridSize
T['epsilon'] = epsilon
T['dt'] = dt
if method == "NMG":
    T['tol'] = 1e-5
else:
    T['tol'] = np.nan
T['t_iter'] = max_it
if method == "NMG":
    T['solver_iter'] = 1e4
else:
    T['solver_iter'] = np.nan
T["dt_out"] = dt_out
T["print"] = print_results
T['boundary'] = boundary
T['pathname'] = pathname
T['elapsed_time(s)'] = results_dict["computation_time_Sec"]
T['mem_allocated(Gb)'] = results_dict["memory_usage_MB"]
T["SLURM_ID"] = SLURM_ID
T['note'] = note

T = pd.DataFrame([T])
file = f"{outdir}/Job_specs_Python.csv"
if not os.path.isfile(file):
    T.to_csv(file)
else:
    with open(file, "a") as f:
        T.to_csv(f, header=False, index=False)