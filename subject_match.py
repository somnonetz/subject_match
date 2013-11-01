"""
Subject Match

Patient - control matching using Minimum Weighted Bipartite Matching.

The input files should be CSV format where the first row is the header names and
the first column is the subject_id. A list of "<patient_id> matches
<control_id>" will be printed to standard out.

Usage: 
  subject_match.py -c <controls.csv> -p <patients.csv>
  subject_match.py -c <controls.csv> -p <patients.csv> -d <delimitter>
  subject_match.py --controls <controls.csv> --patients <patients.csv>

Options:
-h --help                   Show this screen.
-c <file> --controls=<file> The file containing a csv of control subject data.
-p <file> --patients=<file> The file containing a csv of patient subject data.
-d <delimiter>              The delimiter used in the csv file.  [default: ,]
--version                   Show version.

"""
from docopt import docopt
import hungarian
import numpy as np
import pandas as pd
import random

def whiten_value(x, mean, std):
    """
    Whitens (zero mean & divide by std) a given value.
    """
    y = (x - mean)/std
    return y

def whiten_matrix(raw_data, variables_to_whiten):
    """
    Whitens the given variables of a matrix.
    """
    for x in variables_to_whiten:
        mean = raw_data[x].mean()
        std = raw_data[x].std()
        raw_data[x] = raw_data[x].apply(whiten_value, args = (mean, std))
    return raw_data

def square(x):
    return x*x

def pad_data(subject_data, pad_size):
    """
    Adds a number of dummy rows to a matrix with elements = 10.
    """
    dummy_index = ["dummy%s" % i for i in xrange(pad_size)]
    row_count = subject_data.shape[0]
    dummy_data = pd.DataFrame(index=xrange(row_count,row_count+pad_size), columns=subject_data.columns)
    dummy_data['id'] = np.array(dummy_index)
    # The rest of the data is whitened, so values of 10 or more are
    # unlikely. Thus, we fill the dummy values with 100, that way all
    # differences with them will be maximal and the dummies will not be selected
    # for a match.
    dummy_data = dummy_data.fillna(100)
    subject_data = pd.concat([subject_data, dummy_data])
    return subject_data

def make_num_subjects_controls_eq(patients, controls):
    """
    Ensure we'll have a square cost matrix by padding dummy subjects as needed.
    """
    if controls.shape[0] > patients.shape[0]:
        # pad the patients
        pad_size = controls.shape[0] - patients.shape[0]
        patients = pad_data(patients, pad_size)
    else:
        # pad the controls
        pad_size = patients.shape[0] - controls.shape[0]
        controls = pad_data(controls, pad_size)

    return patients, controls

def create_cost_matrix(white_data, subject_type_col_name):
    """
    Takes a 4D matrix of squared differences and sums across them.
    """
    controls = white_data[white_data[subject_type_col_name]<1]
    patients = white_data[white_data[subject_type_col_name]>0]
    
    (patients, controls) = make_num_subjects_controls_eq(patients,
                                                         controls)

    cost_matrix = pd.DataFrame(index=patients[patients.columns[0]],
                               columns=controls[patients.columns[0]])
    for patients_index, patients_row in patients.iterrows():
        for controls_index, controls_row in controls.iterrows():
            diff = patients_row[1:] - controls_row[1:]
            sq_diff = diff.apply(square)
            cost_matrix.iat[patients_index,controls_index] = sq_diff.sum()

    return cost_matrix

def find_matched_pairs(cost_matrix):
    """
    Apply Hungarian method to cost matrix to get best matched pairs.
    """
    (row_assigns, column_assigns) = hungarian.lap(cost_matrix)
    return row_assigns 

def read_data(patients_file, controls_file, delimiter, subject_type_col_name):
    """
    Read in data, add subject_type column, and retrun concat data.
    """
    patient_data = pd.read_csv(patients_file, sep=delimiter)
    patient_data[subject_type_col_name] = 1
    control_data = pd.read_csv(controls_file, sep=delimiter)
    control_data[subject_type_col_name] = 0
    raw_data = pd.concat([patient_data, control_data])
    return raw_data

def create_subject_type_col_name():
    """
    Create a random and hopefully unique column name like subject_typexxx
    """
    random.seed()
    subject_type_col_name = "subject_type%s" % random.randrange(1000,9999)
    return subject_type_col_name


def calculate_match_from_files(patients_file, controls_file, delimiter):
    """
    Find matching controls for patients by minimizing the sum of ^2 difference
    in their variables.
    """
    subject_type_col_name = create_subject_type_col_name()
    raw_data = read_data(patients_file,
                         controls_file,
                         delimiter,
                         subject_type_col_name)
    white_data = whiten_matrix(raw_data, raw_data.columns[1:])
    cost_matrix = create_cost_matrix(white_data, subject_type_col_name)
    row_assigns = find_matched_pairs(cost_matrix)
    assignments = {}
    for i in row_assigns:
        patient = cost_matrix.index[i]
        control = cost_matrix.columns[row_assigns[i]]
        if "dummy" not in patient and "dummy" not in control:
            assignments[patient] = control
    return assignments

def print_assignments(assignments):
    """
    Print a list of patients with matching control.
    """
    for (i, value) in assignments.iteritems():
        print "%s matches %s" % (i, value)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Bipartite Matching 0.1')
    assignments = calculate_match_from_files(arguments['--patients'],
                                             arguments['--controls'],
                                             arguments['-d'])
    print_assignments(assignments)
