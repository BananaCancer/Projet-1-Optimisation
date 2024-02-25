cftoolData = readtable("data\DataProjet2024.xlsx");
X_aval = table2array(Data(:,"Elav_m_"));
Y_deb_total = table2array(Data(:,"Qtot_m3_s_"));

y = preprocess(X_aval, "Elevation aval");
y = preprocess(Y_deb_total, "Débit total");

% L'élévation avale en fonction du débit total
f=fit(X_aval,Y_deb_total,'poly2');
plot(f);
hold on;
scatter(X_aval,Y_deb_total);

% La puissance produite en fonction de la hauteur de chute nette et du débit turbiné,
% et ce, pour chaque turbine.

% ==== PUISSANCE ====
X_puissance_1 = table2array(Data(:,"P1_MW_"));
X_puissance_2 = table2array(Data(:,"P2_MW_"));
X_puissance_3 = table2array(Data(:,"P3_MW_"));
X_puissance_4 = table2array(Data(:,"P4_MW_"));
X_puissance_5 = table2array(Data(:,"P5_MW_"));

% ==== CHUTE NETTE ====
Y_chute_nette_1 = table2array(Data(:,"HauteurNette1"));
Y_chute_nette_2 = table2array(Data(:,"HauteurNette2"));
Y_chute_nette_3 = table2array(Data(:,"HauteurNette3"));
Y_chute_nette_4 = table2array(Data(:,"HauteurNette4"));
Y_chute_nette_5 = table2array(Data(:,"HauteurNette5"));

% ==== DEBIT TURBINE ====
Z_debit_1 = table2array(Data(:,"Q1_m3_s_"));
Z_debit_2 = table2array(Data(:,"Q2_m3_s_"));
Z_debit_3 = table2array(Data(:,"Q3_m3_s_"));
Z_debit_4 = table2array(Data(:,"Q4_m3_s_"));
Z_debit_5 = table2array(Data(:,"Q5_m3_s_"));

% Plotting
figure;
scatter3(X_puissance_1, Y_chute_nette_1, Z_debit_1, 'filled');
xlabel('Puissance');
ylabel('Chute Nette');
zlabel('Débit Turbine');
title('Scatter Plot of Puissance, Chute Nette, and Débit Turbine for TURBINE 1');
grid on;

cftool;
