function [] = preprocess(x, name)
%PREPROCESS Summary of this function goes here
%   Detailed explanation goes here
    y = sum(ismissing(x));
    fprintf('Il y a %d données manquantes pour la variable %s.\n', y, name);
    figure;
    boxplot(x);
end

