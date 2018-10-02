### Random Undersampling 

import xlrd
import os
import random
import csv 
import numpy as np

from imblearn.under_sampling import RandomUnderSampler

RANDOM_STATE = 42

# Datset directory
directory = "../sigmetris/data"

# Read the dataset files and store separately based on two classes
def read_file(filename):
	# Give the location of the file 
	loc = (filename) 
	  
	# To open Workbook 
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 

	# Feature value list
	feature_values = []
	# Target value list
	target_values = []
	# Number of minority class examples
	minor = 0
	for i in range(sheet.nrows):
		instance = sheet.row_values(i)

		values = instance[:-1]
		target = instance[-1]

		if target != 0:
			minor += 1

		# Store the training example in list
		feature_values.append(values)
		target_values.append(target)
			
	# Return the final training set lists
	return np.array(feature_values).astype(np.float), np.array(target_values).astype(np.float), minor	

def main():
	new_dir = os.path.join(directory, 'original')
	for file in os.listdir(new_dir):
		filename = os.path.join(new_dir, file)
		print('\n\t\t\t'+filename)
		data, target, minor = read_file(filename)

		# Get the new undersampled size for the majority class
		ratio = round((len(data)-minor)*0.1)
		print('total: '+str(len(data))+' minor: '+str(minor))
		# print ('ratio: '+str(ratio))

		# Fit the training data for the undersampled size and get new resampled training set
		rus = RandomUnderSampler(random_state=RANDOM_STATE, ratio={0: minor})
		rus.fit(data, target)
		X_resampled, y_resampled = rus.sample(data, target)
		print('resampled total: '+str(len(X_resampled)))

		# Print number of buggy and number of non buggy
		bug = len([y for y in y_resampled if y == 1])
		not_bug = len(y_resampled) - bug

		print('not buggy: '+str(not_bug)+' buggy: '+str(bug))

		new_filename = os.path.join(directory+'/random_sampled', file[0]+'_random.csv')

		with open(new_filename, 'w') as f:
			writer = csv.writer(f)

			for d, t in zip(X_resampled, y_resampled):
				instance = np.append(d, t)
				writer.writerow(instance)
			
if __name__ == '__main__':
	main()
