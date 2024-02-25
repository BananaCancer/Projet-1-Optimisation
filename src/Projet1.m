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

cftool;
