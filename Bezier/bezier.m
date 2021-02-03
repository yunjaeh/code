function bezierPt = bezier()
% function bezierPt = bezier(xPts, yPts)
    xPts = [0, 1, 2, 3];
    yPts = [0, 2, 3, 0];
    
    t = linspace(0,1,100);
    n = length(xPts)-1;        % Bezier Order
    
    xBezier = zeros(1,length(t));
    yBezier = zeros(1,length(t));
    
    % Bezier coefficients
    for i=0:n
        c(i+1) = nchoosek(n,i);
        c(i+1)
        xBezier = xBezier + c(i+1) * (t.^i) .* ((1-t).^(n-i))*xPts(i+1);
        yBezier = yBezier + c(i+1) * (t.^i) .* ((1-t).^(n-i))*yPts(i+1);
    end
    
    figure();
    hold on
    plot(xPts, yPts,'bo--');
    plot(xBezier,yBezier,'k','linewidth',2);
    figure();
    subplot(1,2,1);
    plot(xBezier);
    subplot(1,2,2);
    plot(yBezier);

end