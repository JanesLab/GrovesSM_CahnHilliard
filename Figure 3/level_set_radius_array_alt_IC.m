function [] = level_set_radius_array_alt_IC(R0, m, Nx,indir, suffix)
    folder = "plots";
    total_time=10;
    everyR=10;
    epsilon = m * (1 / Nx) / (2 * sqrt(2) * atanh(0.9));
    epsilon_name = sprintf("%.5g", epsilon);
    R0_name = sprintf('%.5g', R0);
    dt = 2.5e-5;
    dt
    indir
    total_time
    everyR
    epsilon_name
    R0_name
    folder
    Nx
    suffix
    [rr,tt] = level_set_plot_alt_IC(dt, indir, total_time, everyR, epsilon_name, R0_name, folder, Nx, suffix);
    R0_vector = repmat(R0, 1,length(tt));
    length(rr)
    length(R0_vector)
    length(tt)
    tt=tt(1:length(rr));
    length(tt)
    R0_vector=R0_vector(1:length(rr));
    length(R0_vector)

    T = table(transpose(rr), transpose(tt), transpose(R0_vector),'VariableNames',{'radius', 'time', 'R0'});
    writetable(T,sprintf('%s/radius_0.5_level_set_epsilon_%s_%s.txt',indir, epsilon_name, Nx),'WriteMode','append')

    % M = [[rr; nan], [tt; nan], R0_vector]
end
