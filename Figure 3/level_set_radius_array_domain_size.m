function [] = level_set_radius_array_domain_size(R0_name, L, Nx,epsilon_name, indir)

    name=sprintf('nx%s_L%s_R0%s_eps%s_phi',string(Nx),string(L),string(R0_name), string(epsilon_name))

    folder = "plots";
    total_time=10; 
    everyR=10;
    [rr,tt] = level_set_plot_domain_size(2.5e-5, indir, total_time, everyR, epsilon_name, R0_name, L, folder, Nx);
    R0_vector = repmat(R0_name, 1,length(tt));
    length(rr)
    length(R0_vector)
    length(tt)
    tt=tt(1:length(rr));
    length(tt)
    R0_vector=R0_vector(1:length(rr));
    length(R0_vector)

    T = table(transpose(rr), transpose(tt), transpose(R0_vector),'VariableNames',{'radius', 'time', 'R0'});
    writetable(T,sprintf('%s/radius_0.5_%s.txt',indir, name),'WriteMode','append', 'FileType','text')

    % M = [[rr; nan], [tt; nan], R0_vector]
end
