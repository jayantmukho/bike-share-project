close all
clear variables

testData = dlmread('dataSets/testSet.csv');
yTest = testData(:,1);
xTest = testData(:,2:end);
mTest = length(yTest);
xTest = [ones(mTest,1) xTest];

sets = [500, 1000, 2000, 4000, 8000, 15000, 30000,  66404-mTest];
trainAvgErr = zeros(length(sets),1);
testAvgErr = trainAvgErr;
yTrainLoss = trainAvgErr;

for i =1:length(sets)
    filename = sprintf('dataSets/trainSet_%d.csv',sets(i));
    data = dlmread(filename);
    y = data(:,1);
    X = data(:,2:end);
    m = size(data,1);
    n = size(data,2);
    
    X = [ones(m,1) X];
    
    theta = (X'*X)\X'*y;
    
    ybarTrain = X*theta;
    trainErr = norm(y-ybarTrain)/m;
    trainAvgErr(i) = trainErr;
    yTrainLoss(i) = sum((ybarTrain-y).^2)/length(ybarTrain);
    
    ybarTest = xTest*theta;
    testErr = norm(yTest - ybarTest)/mTest;
    testAvgErr(i) = testErr;
    yTestLoss(i) = sum((ybarTest-yTest).^2)/length(ybarTest);
    
    fprintf('Training size= %d:\n',sets(i));
    fprintf('\tTraining error= %2.4f\n',trainAvgErr(i));
    fprintf('\tTest error= %2.4f\n',testAvgErr(i));
    
end
%%
figure(1)
semilogx(sets,trainAvgErr,sets,testAvgErr, sets, mean(y)/100*ones(length(sets),1),'k')
legend('Training Error', 'Test Error','Desired Error');
xlabel('Training set size');
ylabel({'$||y-\bar{y}||_2/m$'},'Interpreter','latex');
title('Error in Prediction of trip duration');
axis([sets(1) sets(end) 0 max(trainAvgErr)])

figure(2)
loglog(sets,yTrainLoss,sets,yTestLoss)%, sets, mean(y)/100*ones(length(sets),1),'k')
legend('Training Error', 'Test Error','Desired Error');
xlabel('Training set size');
ylabel({'$(y-\bar{y})^2/m$'},'Interpreter','latex');
title('Error in Prediction of trip duration');
