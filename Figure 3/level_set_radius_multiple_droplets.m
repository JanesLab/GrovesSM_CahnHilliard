% Code transparency: part of this code was generated with ChatGPT4o.
% June 25, 2025
% Sarah Maddox Groves
function [] = level_set_radius_multiple_droplets(CPC, cohesin, epsilon, indir, alpha, Nx,dt, total_time, suffix,contour_level)
    Ny = Nx;
    % total_time=.05;
    % dt_name="2.5e-5";
    % CPC=28;
    % dt = str2double(dt_name);
    ns = 10;
    dt_in_movie = dt*ns;
    timesteps=round(total_time/dt);
    % cohesin=16;
    % epsilon=0.14;
    % name=sprintf('phi_%d_%s_1.0e-5__CPC_%s_cohesin_%s_eps_%s',Nx,string(timesteps),string(CPC), string(cohesin), epsilon)

    name=sprintf('phi_%d_%s_1.0e-5__CPC_%s_cohesin_%s_eps_%s%s',Nx,string(timesteps),string(CPC), string(cohesin), string(epsilon), suffix)
    phi = readmatrix(sprintf('%s/%s.txt', indir, name),'FileType','text');
    phidims = size(phi);
    phidims(3) = phidims(1)/phidims(2); %Determine number of frames captured
    phidims(1) = phidims(2); %Determine size of square grid
    phi = reshape(phi,phidims(1),phidims(3),phidims(2)); %Reshape multidimensional array
    phi = shiftdim(phi,2); %Shift dimensions to move frames to the third dimension
    data = phi;

    outdir = sprintf("%s/%s",indir, name);
    mkdir(outdir)


    colors = {
        "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",...
        "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",...
        "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",...
        "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",...
        "#a84007","#d9e9af","#42969e","#092acc","#c4ea70",...
        "#11b17f","#5361f9","#8d00f3","#cf2abd","#589bab",...
        "#ea84d5","#db8e50","#a2ebb1","#2c1653","#4fea3b",...
        "#b5d784","#ae200d","#102e39","#8398fc","#f746dd",...
        "#6B2D8E", "#13F9A4", "#D485C9", "#E4B331", "#4F96A8",... 
        "#F13C72", "#B86D1F", "#9FC4F1", "#342E56", "#DAA4D9", ...
        "#37F298", "#84121E", "#28B0DF", "#F15B8C", "#5B6D6B", ...
        "#02EF59", "#A567B8", "#14CBE9", "#906C41", "#DEBCFA", ...
        "#4D8627", "#F9F265", "#2182C7", "#7E9F6D", "#81E3AB", ...
        "#DA2A77", "#9ACCC2", "#5944E1", "#49D483", "#D389B9", ...
        "#23B896", "#7BDFC8", "#4C7DBE", "#BF6233", "#E1A679", ...
        "#B1D84A", "#F5E7A2", "#5C3FA4", "#7AC497", "#2D7099"
    };
    % Initialize parameters
    numTimePoints = size(data, 3);
    dropletData = struct();

    first = 1;
    threshold = 10;
    total_length = numTimePoints-1;

    % Loop over each time point
    for t = first:first+total_length
        % Extract the data for the current time point
        currentData = data(:,:,t);
        
        % Find the 0-level contour
        contourMatrix = contourc(currentData, [contour_level, contour_level]);
        
        % Initialize a list to store droplets for the current time point
        droplets = [];
        startIdx = 1;

        % Parse the contour matrix
        while startIdx < size(contourMatrix, 2)
            % Read the number of points in the current contour line
            numPoints = contourMatrix(2, startIdx);
            dropletContour = contourMatrix(:, startIdx+1:startIdx+numPoints);
            
            % Calculate the center and radius
            centerX = mean(dropletContour(1, :));
            centerY = mean(dropletContour(2, :));
            distances = sqrt((dropletContour(1, :) - centerX).^2 + (dropletContour(2, :) - centerY).^2);
            radius = mean(distances)/Nx;
            
            % Store droplet information
            droplet = struct('center', [centerX, centerY], 'radius', radius, 'id', 0);
            droplets = [droplets, droplet]; %#ok<AGROW>
            
            % Move to the next contour
            startIdx = startIdx + numPoints + 1;
        end
        
        % Store the droplet data for the current time point
        dropletData(t).droplets = droplets;

        
    end

    % Track droplets across time points
    trackedDroplets = struct();

    for t = first:first+total_length
        t
        timepoint = (t-1)*(dt_in_movie);
        currentDroplets = dropletData(t).droplets;
        
        if t == first
            % Initialize tracked droplets with the first time point's data
            for i = 1:length(currentDroplets)
                trackedDroplets(i).radius = currentDroplets(i).radius;
                trackedDroplets(i).time = (t-1) * dt; % Store the actual time
                trackedDroplets(i).center = currentDroplets(i).center;
                trackedDroplets(i).id = i; % Assign a unique ID
                dropletData(t).droplets(i).id = i;
            end
        else
            try
                % Match droplets to the previous time point
                previousDroplets = [dropletData(t-1).droplets];

                for i = 1:length(currentDroplets)
                
                    currentCenter = currentDroplets(i).center;
                    distances = arrayfun(@(d) norm(d.center - currentCenter), previousDroplets);
                    [minDist, minIdx] = min(distances); %minIdx is the index of the previous Droplet that matches this one. 
                    % We want to grab the id from this previous Droplet and assign the id to the
                    % new cell. 
                    % match_id = trackedDroplets(minIdx).id;
                    match_id = previousDroplets(minIdx).id;
                    
                    % Threshold to determine if it is the same droplet
                    % Determine if it is the same droplet based on the threshold
                    if minDist < threshold
                        % Match found, update the tracked droplet
                        trackedDroplets(match_id).radius = [trackedDroplets(match_id).radius, currentDroplets(i).radius];
                        trackedDroplets(match_id).time = [trackedDroplets(match_id).time, (t-1) * dt_in_movie]; % Store the actual time
                        dropletData(t).droplets(i).id = match_id;


                    else
                        % New droplet, add to tracked droplets
                        newIdx = length(trackedDroplets) + 1;
                        trackedDroplets(newIdx).radius = currentDroplets(i).radius;
                        trackedDroplets(newIdx).time = (t-1) * dt_in_movie; % Store the actual time
                        trackedDroplets(newIdx).center = currentDroplets(i).center;
                        trackedDroplets(newIdx).id = newIdx; % Assign a unique ID
                        dropletData(t).droplets(i).id = newIdx;



                    end
                end
            catch
                sprintf("No droplets left at time %s",timepoint)
                break %if the droplet dissolves, this will throw an error, so stop iterating over timepoints
            end
        end
        if false
            if ismember(timepoint, [0, 0.004, 0.0075, 0.008, 0.01, 0.025, 0.04, 0.05])
                data_at_t = data(:, :,t);
            
                % Create contour plot
                hx = 1;
                hy = 1;
                x  = hx*(0:Nx-1);           
                y  = hy*(0:Ny-1);
                [xx,yy] = meshgrid(x,y); 
                figure('visible', 'off');
                contour(data_at_t, [0, 0], 'LineWidth', 2, "Color", '#808080'); axis square;
                xlim([0, Nx]);
                ylim([0, Nx]);
                hold on;
            
                % Extract contours at the 0 level
                contourMatrix = contourc(data_at_t, [0, 0]);
            
                % Parse the contour matrix
                startIdx = 1;
                droplets = struct();
            
                while startIdx < size(contourMatrix, 2)
                    numPoints = contourMatrix(2, startIdx);
                    dropletContour = contourMatrix(:, startIdx+1:startIdx+numPoints);
            
                    % Store droplet contour
                    droplets(end+1).contour = dropletContour;
            
                    % Calculate the radius as the average distance from the center
                    centerX = mean(dropletContour(1, :));
                    centerY = mean(dropletContour(2, :));
                    distances = sqrt((dropletContour(1, :) - centerX).^2 + (dropletContour(2, :) - centerY).^2);
                    droplets(end).radius = mean(distances);
                    color = 'k';
                    label = 'Unknown';
                    % match colors
                    for i = 1:length(trackedDroplets)
                        if abs(centerX-dropletData(t).droplets(i).center(1)) < 0.5 && abs(centerY-dropletData(t).droplets(i).center(2)) < 0.5
                            color = colors{dropletData(t).droplets(i).id};
                            label = sprintf('Data %d', dropletData(t).droplets(i).id);
                            break
                        end
                    end
                    % Plot the center and radius
                    plot(centerX, centerY, 'r+', 'MarkerSize', 10, 'LineWidth', 2,'Color', color, "DisplayName", label); axis square;
                    viscircles([centerX, centerY], droplets(end).radius, 'EdgeColor', color); axis square;
            
                    % Move to the next contour
                    startIdx = startIdx + numPoints + 1;
                end
                
                % for i = 1:length(currentDroplets)
                %     plot(dropletData(t).droplets(i).center(1), dropletData(t).droplets(i).center(2), 'x', 'MarkerSize', 10, 'LineWidth', 2,"Color", colors{dropletData(t).droplets(i).id},"DisplayName", sprintf("Current Droplet %d", dropletData(t).droplets(i).id)); axis square;
                % 
                % end


                title(sprintf('Timepoint %f \n %s', timepoint, name));
            
                % Display results
                % for i = 1:length(droplets)
                %     try
                %         fprintf('Droplet %d: Center = (%.2f, %.2f), Radius = %.6f\n', ...
                %         i, mean(droplets(i).contour(1, :)), mean(droplets(i).contour(2, :)), droplets(i).radius);
                %     end
                % end
                legend show;

                sprintf('%s/radii_at_t_%s.pdf', outdir, timepoint)
                print(gcf,sprintf('%s/radii_at_t_%f.png', outdir, timepoint),"-dpng")
                
                hold off;
            end
        end
    end

    % Plot the radius of each droplet over time
    figure('visible', 'off');
    hold on;
    for i = 1:length(trackedDroplets)
        plot(trackedDroplets(i).time, trackedDroplets(i).radius, '-o','Color', colors{i},"DisplayName",sprintf('Data %d', i));
    end
    xlabel('Time');
    ylabel('Radius');
    xlim([0, total_time]);
    ylim([0,inf]);
    title(sprintf('Radius of Each Droplet Over Time \n %s', name));
    legend show;
    % sprintf('%s/radii_over_time.pdf', outdir)
    set(gcf, 'PaperSize', [11, 20])
    orient(gcf,'landscape')
    print(gcf,sprintf('%s/radii_over_time.png', outdir),"-dpng")
    hold off;

    save(sprintf('%s/trackedDroplets.mat', outdir), "trackedDroplets")

    figure('visible', 'off');
    hold on;
    for i=1:length(trackedDroplets)
        plot(trackedDroplets(i).center(1), trackedDroplets(i).center(2), 'r+', 'MarkerSize', 10, 'LineWidth', 2, ...
            'Color', colors{i},"DisplayName",sprintf('Data %d', i));
    end
    legend show;
    xlim([0, Nx]);
    ylim([0, Nx]);
    title(sprintf('Centers of Each Droplet \n %s', name));

    % sprintf('%s/droplet_centers.pdf', outdir)
    print(gcf,sprintf('%s/droplet_centers.png', outdir),"-dpng")
    hold off;


    % %%%%%%%%%%%%%%%%%%%%%%%%%%
    % %Plot single time points
    % outdir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/Cahn_Hilliard_solvers/plotting/CPC_radii/";
    % for timepoint = [0, 0.0025, 0.00275, 0.003, 0.005, 0.00525, 0.00675, 0.007, 0.00775, 0.008]
    %     timestep = timepoint/(dt_in_movie);
    %     data_at_t = data(:, :,timestep+1);
    % 
    %     % Create contour plot
    %     Nx = 2^8;Ny=2^8;
    %     hx = 1/Nx;
    %     hy = 1/Ny;
    %     x  = hx*(0:Nx-1);           
    %     y  = hy*(0:Ny-1);
    %     [xx,yy] = meshgrid(x,y); 
    %     figure;
    %     contour(x, y, data_at_t, [0, 0], 'LineWidth', 2); axis square;
    %     xlim([0, 256]);
    %     ylim([0, 256]);
    %     hold on;
    % 
    %     % Extract contours at the 0 level
    %     contourMatrix = contourc(data_at_t, [0, 0]);
    % 
    %     % Parse the contour matrix
    %     startIdx = 1;
    %     droplets = struct();
    % 
    %     while startIdx < size(contourMatrix, 2)
    %         numPoints = contourMatrix(2, startIdx);
    %         dropletContour = contourMatrix(:, startIdx+1:startIdx+numPoints);
    % 
    %         % Store droplet contour
    %         droplets(end+1).contour = dropletContour;
    % 
    %         % Calculate the radius as the average distance from the center
    %         centerX = mean(dropletContour(1, :));
    %         centerY = mean(dropletContour(2, :));
    %         distances = sqrt((dropletContour(1, :) - centerX).^2 + (dropletContour(2, :) - centerY).^2);
    %         droplets(end).radius = mean(distances);
    %         color = 'k';
    %         label = 'Unknown';
    %         % match colors
    %         for i = 1:length(trackedDroplets)
    %             if abs(centerX-trackedDroplets(i).center(1)) < 0.5 && abs(centerY-trackedDroplets(i).center(2)) < 0.5
    %                 color = colors{i};
    %                 label = sprintf('Data %d', i);
    %                 break
    %             end
    %         end
    %         % Plot the center and radius
    %         plot(centerX, centerY, 'r+', 'MarkerSize', 10, 'LineWidth', 2,'Color', color, "DisplayName", label); axis square;
    %         viscircles([centerX, centerY], droplets(end).radius, 'EdgeColor', color); axis square;
    % 
    %         % Move to the next contour
    %         startIdx = startIdx + numPoints + 1;
    %     end
    %     title(sprintf('Timepoint %f', timepoint));
    % 
    %     % Display results
    %     % for i = 1:length(droplets)
    %     %     try
    %     %         fprintf('Droplet %d: Center = (%.2f, %.2f), Radius = %.6f\n', ...
    %     %         i, mean(droplets(i).contour(1, :)), mean(droplets(i).contour(2, :)), droplets(i).radius);
    %     %     end
    %     % end
    %     legend show;
    %     hold off;
    %     sprintf('%s/radii_at_t_%s.pdf', outdir, timepoint)
    %     print(gcf,sprintf('%s/radii_at_t_%f.pdf', outdir, timepoint),"-dpdf",'-fillpage')
    % end
end