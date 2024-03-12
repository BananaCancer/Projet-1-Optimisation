clc;
clear all;
close all;

Data = readtable("data\DataProjet2024.xlsx");
Y_aval = table2array(Data(:,"Elav_m_"));
X_deb_total = table2array(Data(:,"Qtot_m3_s_"));



% La puissance produite en fonction de la hauteur de chute nette et du débit turbiné,
% et ce, pour chaque turbine.

% ==== PUISSANCE ====
Z_puissance_1 = table2array(Data(:,"P1_MW_"));
Z_puissance_2 = table2array(Data(:,"P2_MW_"));
Z_puissance_3 = table2array(Data(:,"P3_MW_"));
Z_puissance_4 = table2array(Data(:,"P4_MW_"));
Z_puissance_5 = table2array(Data(:,"P5_MW_"));

% ==== CHUTE NETTE ====
Y_chute_nette_1 = table2array(Data(:,"HauteurNette1"));
Y_chute_nette_2 = table2array(Data(:,"HauteurNette2"));
Y_chute_nette_3 = table2array(Data(:,"HauteurNette3"));
Y_chute_nette_4 = table2array(Data(:,"HauteurNette4"));
Y_chute_nette_5 = table2array(Data(:,"HauteurNette5"));

% ==== DEBIT TURBINE ====
X_debit_1 = table2array(Data(:,"Q1_m3_s_"));
X_debit_2 = table2array(Data(:,"Q2_m3_s_"));
X_debit_3 = table2array(Data(:,"Q3_m3_s_"));
X_debit_4 = table2array(Data(:,"Q4_m3_s_"));
X_debit_5 = table2array(Data(:,"Q5_m3_s_"));

preprocess({Z_puissance_1, Z_puissance_2, Z_puissance_3, Z_puissance_4, ...
    Z_puissance_5}, ["Turbine 1", ...
    "Turbine 2", ...
    "Turbine 3", ...
    "Turbine 4", ...
    "Turbine 5"], ...
    "Distribution de la puissance créée pour chaque turbine")

preprocess({Y_chute_nette_1, Y_chute_nette_2, Y_chute_nette_3, ...
    Y_chute_nette_4, Y_chute_nette_5}, ["Turbine 1", ...
    "Turbine 2", ...
    "Turbine 3", ...
    "Turbine 4", ...
    "Turbine 5"], ...
    "Distribution de la chute nette pour chaque turbine")

preprocess({X_debit_1, X_debit_2, X_debit_3, ...
    X_debit_4, X_debit_5}, ["Turbine 1", ...
    "Turbine 2", ...
    "Turbine 3", ...
    "Turbine 4", ...
    "Turbine 5"], ...
    "Distribution du débit pour chaque turbine")

figure;
y = sum(ismissing(Y_aval));
boxplot(Y_aval);
title(["Distribution de l'élévation aval"]);
xticklabels("Elevation aval");
fprintf('Il y a %d données manquantes pour la variable élévation aval.\n', ...
    y);

figure;
y = sum(ismissing(X_deb_total));
boxplot(X_deb_total);
title(["Distribution du débit total"]);
xticklabels("Débit total");
fprintf('Il y a %d données manquantes pour la variable débit total.\n', y);

plotOutliers(X_debit_1, Y_chute_nette_1, Z_puissance_1, ...
    "Puissance en fonction du débit et de la chute nette pour la turbine 1")

plotOutliers(X_debit_2, Y_chute_nette_2, Z_puissance_2, ...
    "Puissance en fonction du débit et de la chute nette pour la turbine 2")

plotOutliers(X_debit_3, Y_chute_nette_3, Z_puissance_3, ...
    "Puissance en fonction du débit et de la chute nette pour la turbine 3")

plotOutliers(X_debit_4, Y_chute_nette_4, Z_puissance_4, ...
    "Puissance en fonction du débit et de la chute nette pour la turbine 4")

plotOutliers(X_debit_5, Y_chute_nette_5, Z_puissance_5, ...
    "Puissance en fonction du débit et de la chute nette pour la turbine 5")