Subject Matching Tool
========================================

This is a command line tool for finding the best matching controls for a group
of patients using Minimum Weighted Bipartite Matching.

Description
-----------
When matching patients with controls the aim is to minimize the differences
between the two groups. One method is to match each patient to the closest
control, which may not result in the minimal overall differnce. A different
approach, aimed at minimizing the sum of differences between each subject and
its matched control can be performed using the minimum weighted bipartite
matching algorithm.

Installation
------------
Clone the repository:
    git clone git@github.com/msscully/subject_match

Create a virtualenv
If using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (And you should be!) 
    mkvirtualenv subject_match

Otherwise

    cd subject_match
    virtualenv env
    source env/bin/activate

Install dependencies

    pip install -r requirements.txt

And you're good to go!

Usage
-----
subject_match.py -c <controls.csv> -p <patients.csv>
subject_match.py -c <controls.csv> -p <patients.csv> -d <delimitter>
subject_match.py --controls <controls.csv> --patients <patients.csv>

-h --help                   Show this screen.
-c <file> --controls=<file> The file containing a csv of control subject data.
-p <file> --patients=<file> The file containing a csv of patient subject data.
-d <delimiter>              The delimiter used in the csv file.  [default: ,]
--version                   Show version.

A list of "<patient_id> matches <control_id>" will be printed to stdout.

The input files should have the form:

    id,var1,var2,var3
    frank,0,23,100
    tim,0,44,98
    
License
-------

Released under MIT license. See LICENSE
