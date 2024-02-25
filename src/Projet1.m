data = readtable("data\DataProjet2024.xlsx")

elav = table2array(data(:,"Elav_m_"))
qtot = table2array(data(:,"Qtot_m3_s_"))



y = preprocess(elav, "Elevation aval");
y = preprocess(qtot, "Débit total");


cftool