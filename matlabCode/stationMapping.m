stations = dlmread('data/station_sf.csv',',',1,0);
n = size(stations,1);
dist = zeros(n,1);

for i=1:n   
    for j=1:n       
        dist(i) = dist(i) + ((stations(i,2) - stations(j,2))^2+...
            (stations(i,3) - stations(j,3))^2)^.5;
    end
end

stations = [stations(:,1) dist];
dlmwrite('stationMapping.csv',stations)
