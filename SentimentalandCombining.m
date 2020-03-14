%Debugging Script
%tempDate = 0;
%count1 = 0;
%matrixDebug = [];
%for  row = 1:size(matrix, 1)
%    if (tempDate ~= matrix(row, 10))
%        count1 = count1 + 1;
%        tempDate = matrix(row, 10);
%        matrixDebug = [matrixDebug; matrix(row, 10)];
%    end
%end
%disp(count1);

taMatrix = dlmread('TechnicalIndicators.txt');

%Change these variables
combinedMatrix = [taMatrix'];

maxVector = max(abs(combinedMatrix));
diagMatrix = diag(maxVector);
combinedMatrix = combinedMatrix * inv(diagMatrix);


%RSI Selection
%selectedRows1 = find(combinedMatrix(:, 5) >= 0.7);
%selectedRows2 = find(combinedMatrix(:, 5) <= 0.3);

%Momenum 5 Selection
selectedRows1 = find(combinedMatrix(:, 3) >= 0.2);
selectedRows2 = find(combinedMatrix(:, 3) <= -0.2);

%Money Flow Movement
%selectedRows1 = find(combinedMatrix(:, 8) >= 0.2);
%selectedRows2 = find(combinedMatrix(:, 8) <= -0.2);

%Stochastic Selection
%selectedRows1 = find(combinedMatrix(:, 11) >= 0.7);
%selectedRows2 = find(combinedMatrix(:, 11) <= 0.3);

combinedMatrix = [combinedMatrix(selectedRows1, :); combinedMatrix(selectedRows2, :)];

%Remove Tweet Data except for Tweet Movement
%combinedMatrix = [combinedMatrix(:, 1:7) combinedMatrix(:, 14:30)];

%FiveFold Cross Validation
random = rand(size(combinedMatrix,1), 1);
random1 = (random < 0.2);
random2 = (random >= 0.2) & (random < 0.4);
random3 = (random >= 0.4) & (random < 0.6);
random4 = (random >= 0.6) & (random < 0.8);
random5 = (random >= 0.8);

%Exclude 1
outputModel = fitcsvm(combinedMatrix(~random1, 1:16), combinedMatrix(~random1, 17), 'BoxConstraint', 0.028038, 'KernelFunction', 'polynomial', 'PolynomialOrder', 3, 'Standardize', true);
%outputModel = fitcsvm(combinedMatrix(~random1, 1:16), combinedMatrix(~random1, 17), 'BoxConstraint', 2.6289, 'KernelFunction', 'linear', 'Standardize', false);
%outputModel = fitcsvm(combinedMatrix(~random1, 1:16), combinedMatrix(~random1, 17), 'OptimizeHyperparameters', 'all');
%outputModel = svmtrain(combinedMatrix(~random1, 17), combinedMatrix(~random1, 1:16), '-t 2 -c 50');

[label1] = predict(outputModel, combinedMatrix(random1, 1:16));
%[label1] = svmpredict(combinedMatrix(random1, 17), combinedMatrix(random1, 1:16), outputModel);

%Exclude 2
%outputModel = svmtrain(combinedMatrix(~random2, 17), combinedMatrix(~random2, 1:16), '-t 2 -c 50');
%outputModel = fitcsvm(combinedMatrix(~random2, 1:16), combinedMatrix(~random2, 17), 'BoxConstraint', 2.6289, 'KernelFunction', 'linear', 'Standardize', false);
outputModel = fitcsvm(combinedMatrix(~random2, 1:16), combinedMatrix(~random2, 17), 'BoxConstraint', 0.028038, 'KernelFunction', 'polynomial', 'PolynomialOrder', 3, 'Standardize', true);

%[label2] = svmpredict(combinedMatrix(random2, 17), combinedMatrix(random2, 1:16), outputModel);
[label2] = predict(outputModel, combinedMatrix(random2, 1:16));

%Exclude 3
%outputModel = svmtrain(combinedMatrix(~random3, 17), combinedMatrix(~random3, 1:16), '-t 2 -c 50');
%outputModel = fitcsvm(combinedMatrix(~random3, 1:16), combinedMatrix(~random3, 17), 'BoxConstraint', 2.6289, 'KernelFunction', 'linear', 'Standardize', false);
outputModel = fitcsvm(combinedMatrix(~random3, 1:16), combinedMatrix(~random3, 17), 'BoxConstraint', 0.028038, 'KernelFunction', 'polynomial', 'PolynomialOrder', 3, 'Standardize', true);

%[label3] = svmpredict(combinedMatrix(random3, 17), combinedMatrix(random3, 1:16), outputModel);
[label3] = predict(outputModel, combinedMatrix(random3, 1:16));

%Exclude 4
%outputModel = svmtrain(combinedMatrix(~random4, 17), combinedMatrix(~random4, 1:16), '-t 2 -c 50');
%outputModel = fitcsvm(combinedMatrix(~random4, 1:16), combinedMatrix(~random4, 17), 'BoxConstraint', 2.6289, 'KernelFunction', 'linear', 'Standardize', false);
outputModel = fitcsvm(combinedMatrix(~random4, 1:16), combinedMatrix(~random4, 17), 'BoxConstraint', 0.028038, 'KernelFunction', 'polynomial', 'PolynomialOrder', 3, 'Standardize', true);

%[label4] = svmpredict(combinedMatrix(random4, 17), combinedMatrix(random4, 1:16), outputModel);
[label4] = predict(outputModel, combinedMatrix(random4, 1:16));

%Exclude 5
%outputModel = svmtrain(combinedMatrix(~random5, 17), combinedMatrix(~random5, 1:16), '-t 2 -c 50');
%outputModel = fitcsvm(combinedMatrix(~random5, 1:16), combinedMatrix(~random5, 17), 'BoxConstraint', 2.6289, 'KernelFunction', 'linear', 'Standardize', false);
outputModel = fitcsvm(combinedMatrix(~random5, 1:16), combinedMatrix(~random5, 17), 'BoxConstraint', 0.028038, 'KernelFunction', 'polynomial', 'PolynomialOrder', 3, 'Standardize', true);

%[label5] = svmpredict(combinedMatrix(random5, 17), combinedMatrix(random5, 1:16), outputModel);
[label5] = predict(outputModel, combinedMatrix(random5, 1:16));

%Determining Accuracy of Model

predictionAccuracy1 = sum(label1 == combinedMatrix(random1, 17)) / length(combinedMatrix(random1, 17));
predictionAccuracy2 = sum(label2 == combinedMatrix(random2, 17)) / length(combinedMatrix(random2, 17));
predictionAccuracy3 = sum(label3 == combinedMatrix(random3, 17)) / length(combinedMatrix(random3, 17));
predictionAccuracy4 = sum(label4 == combinedMatrix(random4, 17)) / length(combinedMatrix(random4, 17));
predictionAccuracy5 = sum(label5 == combinedMatrix(random5, 17)) / length(combinedMatrix(random5, 17));

finalAccuracy = (predictionAccuracy1 + predictionAccuracy2 + predictionAccuracy3 + predictionAccuracy4 + predictionAccuracy5) / 5;

disp(finalAccuracy);
