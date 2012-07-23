#!/bin/sh
LOGFILE=Extracted_`date`.log
cd /home/rahul/Desktop/july-Data/16-07-2012/
python casedetails.py --year=12 --prefix=AB --start_case_number=1 --number_of_cases_to_hit=10 > $LOGFILE 2>&1
exit 0
