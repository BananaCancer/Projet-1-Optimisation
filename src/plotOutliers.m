function [] = plotOutliers(debit, chute, puissance, titleplot)
    figure;
    scatter3(debit, chute, puissance, '+')
    xlabel('Débit');
    ylabel('Chute nette');
    zlabel('Puissance');
    title(titleplot);
end

