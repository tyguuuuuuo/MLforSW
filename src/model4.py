
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn import metrics 

### Runs C4.5 Decision Tree Classifier on the training data
### and tests with the test data for miclassification
def run_model(X, X_t):

	print("\t\t\txxxxx Decsion Tree model xxxxx")
	X_train = []
	y_train = []
	for i in range(len(X)):
		X_train.append(X[i][1:])
		y_train.append(X[i][0])

	X_test = []
	y_test = []
	for i in range(len(X_t)):
		X_test.append(X_t[i][1:])
		y_test.append(X_t[i][0])

	# Instantiate C4.5 decision tree Classifier and fit the training data to the model
	dt = DecisionTreeClassifier(min_samples_split=5, random_state=99)
	dt.fit(
	    np.array(X_train),
	    np.array(y_train)
	)
	y_pred = dt.predict(np.array(X_test))
	# print(X_test.shape[0])
	
	# Print results for misclassification and accuracy
	print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
	      .format(
	          np.array(X_test).shape[0],
	          (np.array(y_test) != y_pred).sum(),
	          100*(1-(np.array(y_test) != y_pred).sum()/np.array(X_test).shape[0])
	))

	print("F1 score for this model: "+str(metrics.f1_score(np.array(y_test), y_pred)))
	
	fpr, tpr, thresholds = metrics.roc_curve(np.array(y_test), y_pred, pos_label=1)
	print("Area under curve for this model: "+str(metrics.auc(fpr, tpr)))