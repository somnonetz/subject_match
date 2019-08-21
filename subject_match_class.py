# matches patients and controls according age and gender
#
# cli:
#   cwlVersion: v1.0-extended
#   class: pythonclass
#   baseCommand: result = subject_match_class.SubjectMatch(patients_df,controls_df,max_yeardiff)
#
#   inputs:
#     patients_df:
#       type: pandas.DataFrame
#       inputBinding:
#           position: 0
#       doc: "pandas dataframe with colums ['subjectID','age','gender'], age in years, gender='m','f','o','u'"
#     controls_df:
#       type: pandas.DataFrame
#       inputBinding:
#         position: 1
#       doc: "pandas dataframe with colums ['subjectID','age','gender'], age in years, gender='m','f','o','u'"
#     max_yeardiff:
#       type: int?
#       inputBinding:
#         positions: 2
#       doc: "acceptable devation from age in year in both directions, default = 2"
#   outputs:
#     results.matching:
#       type: pandas.DataFrame
#       doc: ""pandas dataframe with colums 'patientID', 'age_p', 'gender_p','controlID', 'age_c', 'gender_c']."
#
#   s:author:
#     - class: s:Person
#       s:identifier:  https://orcid.org/0000-0002-7238-5339
#       s:email: mailto:dagmar.krefting@htw-berlin.de
#       s:name: Dagmar Krefting
# 
#   s:dateCreated: "2019-07-19"
#   s:license: https://spdx.org/licenses/Apache-2.0 
# 
#   s:keywords: edam:topic_3063, edam:topic_2082
#     doc: 3063: medical informatics, 2082: matrix
#   s:programmingLanguage: python3
# 
#   $namespaces:
#     s: https://schema.org/
#     edam: http://edamontology.org/
# 
#   $schemas:
#     - https://schema.org/docs/schema_org_rdfa.html
#     - http://edamontology.org/EDAM_1.18.owl
#

#%% import libraries
import pandas as pd
import numpy as np

#%% class definition
class SubjectMatch:


    def __init__(self, patients, controls, max_yeardiff=2):
        self._patients = patients
        self._controls = controls
        self._max_yeardiff = max_yeardiff
        self._matching = None


    #%%
    @property     # a method that is presented to the user like an attribute
    def matching(self):
        """return or calculate and return age and gender matching"""

        # check if already calculated
        if self._matching is not None:
            return self._matching

        # split into gender-matched subgroups
        genders = ['m','f','o']
        self._matching = pd.DataFrame(columns=['patientID', 'age_p', 'gender_p','controlID','age_c','gender_c'])
        for gender in genders:
            patients_gender =  self._patients[self._patients['gender'] == gender]
            controls_gender = self._controls[self._controls['gender'] == gender]
            print(gender)
            print(len(patients_gender))
            print(len(controls_gender))
            if (len(patients_gender) > 0) & (len(controls_gender) > 0):
            # call function to calculate matching
                self._matching_tmp = self._calc_matching(patients_gender,controls_gender,self._max_yeardiff)
                self._matching = self._matching.append(self._matching_tmp)

        return self._matching

    @staticmethod
    def _calc_matching(patients,controls,max_yeardiff,debug=True):
        """find the candidates and choose the one that fits best"""
        final_matches = pd.DataFrame(columns=['patientID', 'age_p', 'gender_p','controlID','age_c','gender_c'])
        patients_age = np.array(patients['age'])
        controls_age = np.array(controls['age'])
        # create matrix, this gives you one patient per row, with as many columns as the controls
        patients_age_matrix = np.tile(patients_age,(len(controls_age),1)).transpose()
        # create matrix  with the age differences
        age_diff = abs(patients_age_matrix - controls_age)

        # mask with max_yeardiff
        age_diff_mask = (age_diff <= max_yeardiff).astype(int)
        if debug:
            print('patient_age_matrix:')
            print(patients_age_matrix)
            print('age_diff:')
            print(age_diff)
            print('age_diff_mask:')
            print(age_diff_mask)
            print('sum(sum(age_diff_mask)): ', end="")
            print(sum(sum(age_diff_mask)))

        # loop until no matches exist any longer
        while sum(sum(age_diff_mask)) > 0:
            # sum along the columns (getting an array in the length of the controls
            # find the index of the patients, where a patient has only one control that matches
            patient_singlematch = np.where(sum(age_diff_mask.transpose()) == 1)
            patient_singlematch = patient_singlematch[0]
            # debug info
            if debug:
                print('sum(age_diff_mask.transpose()): ',end="")
                print(sum(age_diff_mask.transpose()))
                print('patient_singlematch: ', end="")
                print(patient_singlematch)
                print('len(patient_singlematch): ',end="")
                print(len(patient_singlematch))
                print('len(final_matches): ', end="")
                print(len(final_matches))
            # if this list is not empty, set patient
            if len(patient_singlematch) > 0:
                current_patient = patient_singlematch[0]
                next_row = len(final_matches)
                # set this patient to the final_matches dataframe, first entry to a new row, the following to the same row
                final_matches.loc[next_row,'patientID'] = patients.iloc[current_patient]['subjectID']
                final_matches.loc[len(final_matches)-1,'age_p'] = patients.iloc[current_patient]['age']
                final_matches.loc[len(final_matches)-1,'gender_p'] = patients.iloc[current_patient]['gender']

                # debug info
                if debug:
                    print(patients.iloc[current_patient]['subjectID'])
                    # find the matching control
                    print(age_diff_mask[patient_singlematch[0], :])

                # get the corresponding control
                patient_singlematch_control_idx = np.where(age_diff_mask[patient_singlematch[0],:] == 1)
                current_control = patient_singlematch_control_idx[0][0]
                #set controls
                final_matches.loc[len(final_matches)-1,'controlID'] = controls.iloc[current_control]['subjectID']
                final_matches.loc[len(final_matches)-1,'age_c'] = controls.iloc[current_control]['age']
                final_matches.loc[len(final_matches)-1,'gender_c'] = controls.iloc[current_control]['gender']

                # debug info
                if debug:
                    print('patient_singlematch_control_idx: ', end="")
                    print(patient_singlematch_control_idx[0])
                    print('controls.iloc[current_control][subjectID]')
                    print(controls.iloc[current_control]['subjectID'])

                # remove this control from the age_diff_mask and set the age diff to 100 (to never be the minimum
                age_diff_mask[:, current_control] = 0
                age_diff[:, current_control] = 100

                if debug:
                    print('age_diff_mask after deletion of control')
                    print(age_diff_mask)
                    print(age_diff)

            # if only multiple matching controls exist
            else:
                # choose the next patient
                patient_match = np.where(sum(age_diff_mask.transpose()) > 1)
                patient_match = patient_match[0]
                current_patient = patient_match[0]
                # set this patient to the final_matches dataframe
                final_matches.loc[len(final_matches),'patientID'] = patients.iloc[current_patient]['subjectID']
                final_matches.loc[len(final_matches)-1,'age_p'] = patients.iloc[current_patient]['age']
                final_matches.loc[len(final_matches)-1,'gender_p'] = patients.iloc[current_patient]['gender']

                # debug info
                if debug:
                    print('patient_match: ', end="")
                    print(patient_match[0])
                    print(min(age_diff[patient_match[0], :]))

                # find the best matching control
                selected_patient = age_diff[patient_match[0],:]
                patient_match_control_idx = np.where(selected_patient == min(selected_patient))
                current_control = patient_match_control_idx[0][0]
                # set the selected control to final_matches
                final_matches.loc[len(final_matches)-1,'controlID'] = controls.iloc[current_control]['subjectID']
                final_matches.loc[len(final_matches)-1,'age_c'] = controls.iloc[current_control]['age']
                final_matches.loc[len(final_matches)-1,'gender_c'] = controls.iloc[current_control]['gender']

                # remove this control from the age_diff_mask
                age_diff_mask[:, current_control] = 0
                age_diff_mask[current_patient, :] = 0
                age_diff[:, current_control] = 100

                if debug:
                    print(selected_patient)

        return final_matches
