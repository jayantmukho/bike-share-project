data = dlmread('full_params.csv',',');
data = data(1:66404,:);
data(:,1) = data(:,1)./60;
n = size(data,1);
nTest = 10000;
sets = [500, 1000, 2000, 4000, 8000, 15000, 30000,  n-nTest];

ind = randperm(n);
% dlmwrite('bayesNetData.csv',data(ind(1:10000),:));
%%
dlmwrite('testSet.csv',data(ind(1:nTest),:));

data=data(ind(nTest+1:end),:);
n = size(data,1);
ind = randperm(n);

for i=1:length(sets)
    filename = sprintf('trainSet_%d.csv',sets(i));
    dlmwrite(filename,data(ind(1:sets(i)),:));
end

