# import required libraries
import unittest  # unittests themselves
import pandas as pd   # pandas for dataframe
import subject_match_class  # the class to be tested
import importlib  # update loaded classes implicitely
importlib.reload(subject_match_class)   # reload class
import math

# Definition of testvalues
## patientA matches only controlA by age with max_yeardiff=0 and by gender
## patientB matches controlB and controlC by gender and by age with max_yeardiff=2
## patientC matches controlB and controlC by gender and controlC by age with max_yeardiff=3
## patientD matches the same as patientA
## matching default max_yeardiff should be
# pA - cD
# pB - cC
# pC - none
# pD - cA

## matching max_yeardiff = 1
# pA - cA
# pB - cC
# pC - none
# pD - none

## matching max_yeardiff = 0
# pA - none
# pB - none
# pC - none
# pD - cA

## matching max_yeardiff = 4
# pA - cD
# pB - cB
# pC - cC
# pD - cA

patients_case_a = pd.DataFrame({'subjectID': ['patientA', 'patientB', 'patientC','patientD'], 'age': [ 21, 25, 30, 20], 'gender': ['m','f','f','m']})
controls_case_a = pd.DataFrame({'subjectID': ['controlA', 'controlB', 'controlC','controlD'], 'age': [ 20, 23, 26, 23], 'gender': ['m','f','f','m']})

# Initialization of the testcase, the class to be tested is here in self.results_case_a
class SubjectMatchTestCase(unittest.TestCase):
    """Tests for `subject_match_class.py`."""
    def setUp(self):
        self.results_case_a = subject_match_class.SubjectMatch(patients_case_a,controls_case_a)

# Here the actual tests begin
class TestInit(SubjectMatchTestCase):

    def test_if_pA_cD(self):
        """does patientA matches controlD?"""
        print(self.results_case_a.matching)
        self.assertEqual(self.results_case_a.matching.iloc[0]['patientID'], 'patientD')

#     def test_if_lights_on_is_seven(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.lights.on, 8)
#
#     def test_if_total_recording_time_is_three(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.total_recording_time, 3)
#
#     def test_if_sleep_onset_epoch_is_five(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_epochs.sleep_onset, 5)
#
#     def test_if_final_awakening_epoch_is_eight(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_epochs.final_awakening, 8)
#
#     def test_if_sleep_onset_latency_is_onehalfminutes(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_onset_latency, 1.5)
#
#     def test_if_sleep_period_time_is_onehalfminutes(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_period_time, 1.5)
#
#     def test_if_total_sleep_time_is_oneminute(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.total_sleep_time, 1)
#
#     def test_if_wake_after_sleep_onset_is_halfminute(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.wake_after_sleep_onset, 0.5)
#
#     def test_if_sleep_efficiency_is_forty(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_efficiency, 2/6*100)
#
#     def test_if_sleep_R_is_zero(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_stage_epochs.R, 0)
#
#     def test_if_sleep_N1_is_one(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_stage_epochs.N1, 1)
#
#     def test_if_sleep_N2_is_zero(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_stage_epochs.N2, 0)
#
#     def test_if_sleep_N3_is_one(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_stage_epochs.N3, 1)
#
#     def test_if_sleep_N3_is_halfminute(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.sleep_time_per_stage.N3, 0.5)
#
#     def test_if_sleep_N3_is_50(self):
#         """is the total recording time 3 minutes?"""
#         self.assertEqual(self.results_case_a.relative_sleep_time_per_stage.N3, 50)
#
#     def test_if_R_onset_latency_is_nan(self):
#         """is the total recording time 3 minutes?"""
#         self.assertTrue(math.isnan(self.results_case_a.onset_latency.R))
#
# # Edge Case b: lights off and on are zero
#     def test_if_lights_off_is_zero(self):
#         """is lights_off zero (immediate start of the recording)?"""
#         print(self.results_case_b.lights.off)
#         self.assertEqual(self.results_case_b.lights.off, 0)
#
#
#     def test_if_lights_on_is_six(self):
#         """Are there 6 epochs before lights on?"""
#         self.assertEqual(self.results_case_b.lights.on, 6)


if __name__ == '__main__':
    unittest.main()