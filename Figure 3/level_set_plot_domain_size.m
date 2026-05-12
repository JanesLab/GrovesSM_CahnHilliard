function [rr, tt] = level_set_plot_domain_size(dt, indir, total_time, everyR, epsilon_name, R0, L, folder, Nx)
    timesteps=total_time/dt;
    name=sprintf('nx%s_L%s_R0%s_eps%s_phi',string(Nx),string(L),string(R0), string(epsilon_name))
    dtout=10;
    % Nx = 2^8;Ny=2^8;
    Nx=str2double(Nx);
    Ny = Nx;
    hx = str2double(L)/Nx
    hy = str2double(L)/Ny
    x  = hx*(0:Nx-1);           
    y  = hy*(0:Ny-1);
    [xx,yy] = meshgrid(x,y); 
    T0=0;
    tt=0;rr=0;
    phi = readmatrix(sprintf('%s/%s.csv', indir, name));%,'FileType','text');
    % phi = readmatrix("/Users/smgroves/Documents/GitHub/jlCHSolver/output.txt");
    phidims = size(phi);
    phidims(3) = phidims(1)/phidims(2); %Determine number of frames captured
    phidims(1) = phidims(2); %Determine size of square grid
    phi = reshape(phi,phidims(1),phidims(3),phidims(2)); %Reshape multidimensional array
    phi = shiftdim(phi,2); %Shift dimensions to move frames to the third dimension

    for i = 0:everyR:phidims(3)-1 %%changed just to look at unfinished sims; needs to be changed back to 10!
        T=i*dtout*dt;
        % t = Nx*i+1 : Nx*(i+1);
        % psi = Psi(t,:);
        phi_tmp = phi(:,:,i+1);
        % Find and plot the 0.5 contour
        figure('visible', 'off');
        [~, h] = contour(x, y, phi_tmp, [0 0]);
        % Extract the x and y coordinates of the 0 contour
        contour_data = h.ContourMatrix;
        col = 1;
        x_contour = [];
        y_contour = [];
        while col < size(contour_data, 2)
            num_points = contour_data(2, col);
            cols = col + (1:num_points);
            
            x_contour = [x_contour, contour_data(1, cols)];
            y_contour = [y_contour, contour_data(2, cols)];
            
            col = col + num_points + 1;  % Move to next segment
        end
        % x_contour = contour_data(1, 2:end); 
        % y_contour = contour_data(2, 2:end);
        %necessary for when the droplet isn't centered
        x_center = mean(x_contour);
        y_center = mean(y_contour);

        distances = sqrt((x_contour - x_center).^2 + (y_contour - y_center).^2);
        % distances = sqrt((x_contour-0.5).^2 + (y_contour-0.5).^2);
        radius = mean(distances);
        close
        tt(i/everyR+1) = T0 + T;
        rr(i/everyR+1) = radius;
    end
    % clear h; 

    %% Plot the figure
        fig = figure('visible', 'off');
            plot(tt,rr, ...
                                        ':', ...
                'LineWidth',1.5);set(gca,'FontSize',16);
            title(sprintf('Radius at 0.5 level set \n %s',name))
            xlabel('t');ylabel('R');
            filename = sprintf('%s/%s/radius_0.5_%s.png',indir,folder, name);
            saveas(fig, filename);
end