function [] = preprocess(x, names, titleplot)
%PREPROCESS Summary of this function goes here
%   Detailed explanation goes here
    for i = 1:length(x)
        a = sum(ismissing(x{i}));
        b = sum(isoutlier(x{i}));
        c = sum(x{i} == 0);
        outliers = isoutlier(x{i});
        d = sum(x{i}(outliers) == 0);
        fprintf('Il y a %d données aberrantes (hors nulles) pour la variable %s.\n', b-d, names(i));
        fprintf('Il y a %d valeurs aberrantes nulles pour la variable %s.\n', d, names(i));
    end
    figure;
    boxplot([x{1}, x{2}, x{3}, x{4}, x{5}])
    xticklabels(names);
    title(titleplot)
end

