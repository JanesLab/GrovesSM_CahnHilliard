% Script to calculate the distance between droplets at each timestep for
% Ostwald ripening simulations. This uses the trackedDroplets.mat file that
% is generated for a simulation when level_set_radius_multiple_droplets.m
% is run. This is updated from distance_between_droplets_sim.m, because chromosome length 
% is taken into account for counting droplet distances.
%%%%%%%%%%%%%% This is the most up to date version for calculating droplet distances. %%%%%%%%%%%%%
% Sarah Groves August 28, 2024
epsilon = "0.0089";
cell_line = "MCF10A";

indir = sprintf("/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/radii_lineplots_kymographs/domain_0_2_noisy_cohesin_sd_0.11_eps_%s/",epsilon);
sim_list= dir(fullfile(indir, 'phi*'));

% indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/plotting/radii_over_time_level_set_plots/domain_0_2_from_rivanna_kymographs_e_0.0075/";
total_time = 0.03;
spacing = 0.000001525878906;
x = 0:spacing:0.03;
cohesin = "0.09";
chr_lengths = load(sprintf("/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/image_analysis/chromosome_lengths_%s_v2.csv", cell_line));
num_chr = floor(length(chr_lengths)/2); %chr_lengths is 2x the number of chromosomes because it is counting each arm
% num_sims = length(sim_list);
num_sims = 50; %number of simulations to match
num_samples = ceil(num_chr/num_sims); %divide by the number of simulations 

% seed = "1111";
% for CPC = "0.12"
% for CPC = ["0.1","0.12","0.125","0.15","0.173","0.2", "0.22","0.25","0.3", "0.35"]
for i = 1:length(sim_list)
    folderName = sim_list(i).name
    pattern = 'phi_\d+_\d+_[\deE\.-]+__CPC_([^\_]+)_cohesin_([^\_]+)_eps_([^\_]+)_alpha_0_domain_0_2_([^\_]+)';
    tokens = regexp(folderName, pattern, 'tokens');

    if ~isempty(tokens)
        % 'tokens' is a nested cell array
        CPC     = tokens{1}{1};
        cohesin = tokens{1}{2};
        epsilon = tokens{1}{3};
        random_num  = tokens{1}{4};

    %     fprintf('File: %s\nCPC = %s, cohesin = %s, epsilon = %s, random = %s\n', ...
    %         folderName, CPC, cohesin, epsilon, random_num);
    % else
    %     fprintf('No match for file: %s\n', folderName);
    end

    % if str2num(random_num) > 20
    %     fprintf('Skipping file: %s\n', folderName);
    %     continue
    % end
    sampled_times = datasample(x, num_samples, 'Replace', false);

    Nx = 512;
    domain = 6.4;
    grid_spacing = domain/Nx;
    midpoint = Nx/2;
    % name = sprintf("phi_512_19661_1.0e-5__CPC_%s_cohesin_%s_eps_%s_alpha_0_domain_0_2",CPC, cohesin, epsilon)
    load(sprintf("%s/%s/trackedDroplets.mat", indir, folderName));
    dt = .1*(1/256)^2;
    for i = 1:num_samples
        t = sampled_times(i);
        arm_length = chr_lengths(i);

        droplet_centers = [];
        %check if each droplet exists at time t and if so, add to
        %droplet_centers
        for d = 1:max([trackedDroplets.id])
            if ismember(d, [2]) %ignore second IC droplet because it is in the same y location as droplet 1
            elseif ismembertol(t,trackedDroplets(d).time, 1e-3)
                if trackedDroplets(d).center(2) <= midpoint+(arm_length/grid_spacing) && trackedDroplets(d).center(2) >= midpoint-(arm_length/grid_spacing)
                    droplet_centers(end+1) = trackedDroplets(d).center(2);
                end
            end
        end
        droplet_centers = sort(droplet_centers);
        distances = domain*diff(droplet_centers)/Nx;
        num_sims = 20;
        fid = fopen(sprintf('simulated_droplet_distributions/simulated_droplet_distances_e_%s_noisy_cohesin_chr_lengths_%s_n_matched_%ssims.csv',epsilon,cell_line,string(num_sims)), 'a+');
        fprintf(fid, '%s,%s,%s,%s,%f,%f,%s \r\n', string(random_num),string(CPC), string(cohesin), string(epsilon), t,arm_length, mat2str(distances));
        fclose(fid);
         

    end


end

