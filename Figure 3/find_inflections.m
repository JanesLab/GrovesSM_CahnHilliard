function [inf_t, inf_r] = find_inflections(tt, rr, r_min, r_max, deg, showPlot)
%FIND_INFLECTIONS  Locate inflection points of a radius–time curve
%
%   [inf_t, inf_r] = FIND_INFLECTIONS(tt, rr, r_min, r_max)
%   finds the inflection points of the data (tt, rr) after fitting a
%   polynomial (default degree 5) only on the portion where
%        r_min ≤ rr ≤ r_max.
%
%   Optional args:
%       deg      – polynomial degree (default 5)
%       showPlot – logical flag (default true) to display a diagnostic plot
%
%   Outputs:
%       inf_t – row vector of inflection times
%       inf_r – row vector of corresponding radii

    % -------- default arguments -----------------------------------------
    if nargin < 5 || isempty(deg);       deg      = 5;      end
    if nargin < 6 || isempty(showPlot);  showPlot = true;   end

    % -------- basic checks ----------------------------------------------
    tt = tt(:);  rr = rr(:);
    if numel(tt) ~= numel(rr)
        error('tt and rr must be the same length.');
    end

    % -------- select window in r ----------------------------------------
    idx = find(rr >= r_min & rr <= r_max);   % contiguous for monotone decay
    if isempty(idx)
        error('No data points fall inside r ∈ [%.3f, %.3f].', r_min, r_max);
    end
    ttSeg = tt(idx);
    rrSeg = rr(idx);

    % -------- local polynomial fit --------------------------------------
    p      = polyfit(ttSeg, rrSeg, deg);     % coefficients of P(t)
    p_d2   = polyder(polyder(p));            % coefficients of P''(t)

    root_t = roots(p_d2);                    % solve P''(t)=0
    root_t = real(root_t(abs(imag(root_t)) < 1e-12));          % real roots only
    root_t = root_t(root_t >= min(ttSeg) & root_t <= max(ttSeg));

    inf_t  = root_t(:).';                    % row vector
    inf_r  = polyval(p, inf_t);              % radii at inflection times

    % -------- optional plotting -----------------------------------------
    if showPlot
        % figure;  
        xlabel('t'); ylabel('r');
        title(sprintf('Inflection search (poly deg = %d, r ∈ [%.2f, %.2f])', ...
                      deg, r_min, r_max));

        % plot(tt, rr, '.', 'DisplayName', 'raw data');
        tFit = linspace(min(ttSeg), max(ttSeg), 200);
        plot(tFit, polyval(p, tFit), 'LineWidth', 1.4, ...
             'DisplayName', sprintf('local poly (deg %d)', deg));
        plot(inf_t, inf_r, 's', 'MarkerFaceColor', 'r', ...
             'DisplayName', 'inflection pts');

        for k = 1:numel(inf_t)
            text(inf_t(k), inf_r(k), ...
                sprintf(' (%.3f, %.4f)', inf_t(k), inf_r(k)), ...
                'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
        end
        legend('Location','best');
        hold on;
    end
end