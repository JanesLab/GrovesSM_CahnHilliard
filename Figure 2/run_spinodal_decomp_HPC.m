function run_spinodal_decomp_HPC(GridSize, boundary, print_results, solver, SLURM_ID, note)
    indir = "../IC";
    outdir = "/project/g_bme-janeslab/SarahG/spinodal_decomp_06_2025"

    n_relax = 4;
    m = 8;
    h = 1/GridSize;
    epsilon = m * h/ (2 * sqrt(2) * atanh(0.9)); 

    dt = 5.5e-7;
    max_it = 20000;

    %run both periodic and neumann with the IC that were smoothed using neumann-BC-smoothing
    init_file = sprintf("%s/initial_phi_%d_smooth_n_relax_%d_%s_neumann.csv",indir,GridSize, n_relax,note);
    phi0 = readmatrix(init_file);
    print_phi = true;
    dt_out = 10;
    ny = GridSize;
    if print_results == "true"
        dt_out = 10
    else
        dt_out = 20000
    end
    pathname = sprintf("%s/out_MATLAB/%s_MATLAB_%d_dt_%.2e_Nx_%d_%s_dt_out_%d%s_",outdir,solver, max_it,dt, GridSize, boundary, dt_out,note);

    % #################################################
    % RUN SAV SOLVER 
    % #################################################
    if solver == "SAV"
        fprintf("Running SAV solver with parameters: %s\n", pathname);
        tol = "NaN";
        solver_iter = "NaN";

        tStart_SAV = tic;
   
        [t_out, phi_t, delta_mass_t, E_t] = CahnHilliard_SAV(phi0,...
                                            t_iter = max_it,...
                                            dt = dt,...
                                            m = m,...
                                            boundary = boundary,...
                                            printphi=print_phi,...
                                            pathname=pathname,...
                                            dt_out = dt_out);
        elapsedTime = toc(tStart_SAV);


    end
    % % #################################################
    % % RUN NMG SOLVER 
    % % #################################################

    if solver == "NMG"
        fprintf("Running NMG solver with parameters: %s\n", pathname);
        tStart_NMG = tic;
        tol = "1e-5"
        solver_iter = "1e4"
        [t_out, phi_t, delta_mass_t, E_t] = CahnHilliard_NMG(phi0,...
                                            t_iter = max_it,...
                                            dt = dt,...
                                            m = m,...
                                            boundary = boundary,...
                                            printphi=print_phi,...
                                            pathname=pathname,...
                                            dt_out = dt_out);
        elapsedTime = toc(tStart_NMG);


    end
    filename = strcat(pathname, "movie");
    fprintf("Creating movie\n");
    if print_results
        ch_movie_from_file(strcat(pathname,"phi.csv"), t_out, ny,filename = filename, filetype = "Motion JPEG AVI")

    writematrix(t_out,sprintf('%st_out.csv', pathname));
    writematrix(delta_mass_t,sprintf('%smass.csv', pathname));
    writematrix(E_t,sprintf('%senergy.csv', pathname));

    fid = fopen(sprintf('%s/Job_specs.csv', outdir), 'a+');
    v = [string(datetime) "MATLAB" solver GridSize epsilon dt tol max_it solver_iter dt_out print_results boundary pathname elapsedTime "NaN" SLURM_ID note];
    fprintf(fid, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n', v);
    fclose(fid);

end
