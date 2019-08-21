Subject Matching Tool
========================================

This is a command line tool for finding the best matching controls for a group
of patients.

 matches patients and controls according age and gender

```
 cli:
   cwlVersion: v1.0-extended
   class: pythonclass
   baseCommand: result = subject_match_class.SubjectMatch(patients_df,controls_df,max_yeardiff)

   inputs:
     patients_df:
       type: pandas.DataFrame
       inputBinding:
           position: 0
       doc: "pandas dataframe with colums ['subjectID','age','gender'], age in years, gender='m','f','o','u'"
     controls_df:
       type: pandas.DataFrame
       inputBinding:
         position: 1
       doc: "pandas dataframe with colums ['subjectID','age','gender'], age in years, gender='m','f','o','u'"
     max_yeardiff:
       type: int?
       inputBinding:
         positions: 2
       doc: "acceptable devation from age in year in both directions, default = 2"
   outputs:
     results.matching:
       type: pandas.DataFrame
       doc: ""pandas dataframe with colums 'patientID', 'age_p', 'gender_p','controlID', 'age_c', 'gender_c']."

   s:author:
     - class: s:Person
       s:identifier:  https://orcid.org/0000-0002-7238-5339
       s:email: mailto:dagmar.krefting@htw-berlin.de
       s:name: Dagmar Krefting
 
   s:dateCreated: "2019-07-19"
   s:license: https://spdx.org/licenses/Apache-2.0 
 
   s:keywords: edam:topic_3063, edam:topic_2082
     doc: 3063: medical informatics, 2082: matrix
   s:programmingLanguage: python3
 
   $namespaces:
     s: https://schema.org/
     edam: http://edamontology.org/
 
   $schemas:
     - https://schema.org/docs/schema_org_rdfa.html
     - http://edamontology.org/EDAM_1.18.owl

```
