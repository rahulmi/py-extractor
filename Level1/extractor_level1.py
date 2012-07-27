#Program to find case details and statistics.
import urllib2
from BeautifulSoup import BeautifulSoup
import re,sys
from optparse import OptionParser
from extractor_utils import CaseStatistics
from parse_case_info import parse_case_details

class CaseDetails(object):
	"""
	This class parsing all the case details: case summary ,parties information(number of plaintiff and defendant),
	
	 Input parameter:
	 Name                     DataType
	 case year                 string
	 case prefix               string
	 start case number         int
	 number of cases to hit    int
	"""
	
	def __init__(self,case_year,case_prefix,start_case_number,number_of_cases_to_hit):
		self.case_url="http://ec2-174-129-101-141.compute-1.amazonaws.com:8080"
		self.number_of_case_hit=number_of_cases_to_hit
		#case year.
		self.case_year=case_year 
		#case prefix
		self.case_prefix=case_prefix
		#case number.
		self.start_case_number=start_case_number
		self.total_hit=number_of_cases_to_hit + start_case_number
	
		
	def parse_case_page(self):
		"""
		This function parses case index page and extract parameter name and value from form and 
		add with url and returns case url
		"""
		open_page=urllib2.urlopen(self.case_url)
		page_obj=BeautifulSoup(open_page)
		form_name=page_obj.body.form.input['name']
		form_value=page_obj.body.form.input['value']
		url=self.case_url+"/?"+form_name+"="+form_value
		return url
		
		
	def	loop_to_total_case_to_hit(self,url):
		""" 
		(i)This function runs a loop from start case number to  number of
	    cases to hit and call parse_case_details function for each
		case number. 
		(ii)Its creating object of class CaseParameter and assigning statistics details. 
		"""
		for case_num in range(self.start_case_number,self.total_hit):
			self.case_hit_url(url,case_num)
			
		CaseStatistics().display_case_statistics()
			
	def case_hit_url(self,temp_url, temp_case_num):
		"""
		    This function extracting the case parameter for each case
		   	(i) case number and case name.
	        (ii)basic case details
	        (iii)list of Plaintiff and list of dependant and their attorneys for each case.
	        (iv)calling name resolver function to seperate name into(prefix,lastname,firstname,lastname,suffix) order.
	        	        
	        Inuput parameter:
	        1)url
	        2)case number
	    """
		#convert case number to 6 digit formate.
		formatted_case_num="%06d"%temp_case_num 
		casedetail_url=temp_url+"&case_id="+self.case_year+self.case_prefix+formatted_case_num
		casedetail_page=urllib2.urlopen(casedetail_url)
		parse_case_details(casedetail_page)

		
def main():
	"""
	This is the main function of the program called at the beginning of the program.
	parse the command line argument(--year=12 --prefix=AB --start_case_number=1 --number_of_cases_to_hit=10) and pass them to casedetails object.
	"""
	if len(sys.argv)<5:
		print "Please pass the command line parameter ex:(--year=12 --prefix=AB --start_case_number=1 --number_of_cases_to_hit=10)"
		sys.exit(1)
	else:
		parser=OptionParser()
		#defining and parsing command line arguments.
		parser.add_option("-y","--year",help="case year")
		parser.add_option("-p","--prefix",help="case prefix ")
        parser.add_option("-c","--start_case_number",help="Start case number")
        parser.add_option("-n","--number_of_cases_to_hit",help="Number of cases to hit")
        cmd_para=parser.parse_args()
        case_year=cmd_para[0].year
        case_prefix=cmd_para[0].prefix
        start_case_number=int(cmd_para[0].start_case_number)
        number_of_cases_to_hit=int(cmd_para[0].number_of_cases_to_hit)
        #creating object of casedetail class
        casedetail_obj=CaseDetails(case_year,case_prefix,start_case_number,number_of_cases_to_hit)
        #calling classdetail method
        url=casedetail_obj.parse_case_page() 
        casedetail_obj.loop_to_total_case_to_hit(url)
        
		
if __name__=='__main__':
    main()	
 
    	

