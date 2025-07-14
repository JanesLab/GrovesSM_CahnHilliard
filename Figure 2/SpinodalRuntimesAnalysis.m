clear
close all hidden
warning off

Spinodal_times = readtable('Job_specs_Rivanna_cleaned.csv');
mainfigmesh = 2^7;

%Set up logicals
SAV = strcmp(Spinodal_times.method,'SAV');
neumann = strcmp(Spinodal_times.boundary,'neumann');
periodic = strcmp(Spinodal_times.boundary,'periodic');

mainfig_times = Spinodal_times(SAV & Spinodal_times.GridSize(:) == ...
    mainfigmesh,[3:4 13 15]);

[p,tbl] = anovan(mainfig_times{:,4},{mainfig_times{:,1} mainfig_times{:,3}}, ...
    'varnames',{'language' 'boundary'});
p(2)