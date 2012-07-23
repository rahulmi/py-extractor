#Program to find case details and statistics.
import urllib2
from BeautifulSoup import BeautifulSoup
import re,sys
from optparse import OptionParser
from caseutility import name_resolver

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
		self.total_plaintiff=0
		self.total_defendant=0
		self.total_invalid_case=0
		self.total_success_case=0
		self.total_plaintiff_attorney=0
		self.total_defendant_attorney=0
		

		
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
			self.parse_case_details(url,case_num)
			
		case_statistic=CaseStatistics()
		case_statistic.total_plaintiff=self.total_plaintiff
		case_statistic.total_defendant=self.total_defendant
		case_statistic.total_invalid_case=self.total_invalid_case
		case_statistic.total_success_case=self.number_of_case_hit-self.total_invalid_case
		case_statistic.total_plaintiff_attorney=self.total_plaintiff_attorney
		case_statistic.total_defendant_attorney=self.total_defendant_attorney
		case_statistic.display_case_statistics()

	def parse_case_details(self,temp_url, temp_case_num):
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
		case_num=""
		case_name=""
		case_filing_date=""
		case_type=""
		case_filing_court=""
		case_status=""
		case_plaintiff_list=[]
		case_defendant_list=[]
		list_plaintiff_attorney=[]
		list_defendant_attorney=[]
		defendant_address_list=[]
		#collects the tuples of format(prefix,lastname,firstname,lastname,suffix).
		plaintiff_resolved_name_list=[]
		defendant_resolved_name_list=[]
		#convert case number to 6 digit formate.
		formatted_case_num="%06d"%temp_case_num 
		casedetail_url=temp_url+"&case_id="+self.case_year+self.case_prefix+formatted_case_num
		casedetail_page=urllib2.urlopen(casedetail_url)
		casedetail_parse_obj=BeautifulSoup(casedetail_page)
		
		#execute when invalid case found.
		if casedetail_parse_obj.findAll(text="Invalid case number."):
			print "Invalid case number",self.case_year+self.case_prefix+formatted_case_num
			print "\n"
			self.total_invalid_case=self.total_invalid_case+1
			return
		    
		#traversing all the b node in the casedetail page and collecting in list.    
		bnode=casedetail_parse_obj.findAll('b')
		#extracting all the parameters of the case.
		for element in bnode:
			if 'Case Number' in element.string:
				case_num=element.next.next
				case_name=case_num.next.next
				
			if 'Filing Date' in element.string:
				case_filing_date=element.next.next
				
			if 'Case Type' in element.string:
				case_type=element.next.next
				
			if 'Filing Court' in element.string:
				case_filing_court=element.next.next
				
			if 'Status' in element.string:
				case_status=element.next.next
				
			if  'Plaintiff' in element.string:
				#calling name resolver function of caseutility script and passing defendant name.
				name_resolved_plaintiff_tuple=name_resolver(str(element.next.next))
				plaintiff_resolved_name_list.append(name_resolved_plaintiff_tuple)
				case_plaintiff_list.append(str(element.next.next))
				self.total_plaintiff=self.total_plaintiff+1
				
			if  'Defendant' in element.string:
				#calling name resolver function of caseutility script and passing plaintiff name.
				name_resolved_defendant_tuple=name_resolver(str(element.next.next))
				defendant_resolved_name_list.append(name_resolved_defendant_tuple)
				case_defendant_list.append(str(element.next.next))
				self.total_defendant=self.total_defendant+1
				
			if  'Attorney' in element.string:
				#checking previous element of attorney if contain plaintiff, add to plaintiff attorney else defendant.
			    fpe=element.findPreviousSiblings('b')
			    if 'Plaintiff' in fpe[0].string:
			        list_plaintiff_attorney.append(str(element.next.next))
			        #checking attorney is not None
			        if element.next.next!='None':
						self.total_plaintiff_attorney=self.total_plaintiff_attorney+1
			    if 'Defendant' in fpe[0].string:
			        list_defendant_attorney.append(str(element.next.next))
			        #checking attorney is not None
			        if element.next.next!='None':
						self.total_defendant_attorney=self.total_defendant_attorney+1
			    if "Defendant"  not in fpe[0].string and "Plaintiff" not in fpe[0].string:
					#Execute if Defendant have address.
			        list_defendant_attorney.append(str(element.next.next))
			        defendant_address_list.append(str(fpe[0].string))
			    
		
		party_info=Party_Type_Info()
		party_info.plaintiff_resolved_name_list=plaintiff_resolved_name_list
		party_info.defendant_resolved_name_list=defendant_resolved_name_list
		party_info.plaintiff_list=case_plaintiff_list
		party_info.defendant_list=case_defendant_list
		party_info.plaintiff_attorney_list=list_plaintiff_attorney
		party_info.defendant_attorney_list=list_defendant_attorney
		party_info.defendant_address_list=defendant_address_list
						
		#object of class caseparameter to store case data				
		case_data=CaseParameter()  
		#removing newline character from the end of the string.
		case_data.case_num=case_num.replace("\n","")
		#removing newline character from the end of the string.
		case_data.case_name=case_name.replace("\n","")
		case_data.case_filing_date=case_filing_date  
		case_data.case_type=case_type
		case_data.case_filing_court=case_filing_court
		case_data.case_status=case_status   
		case_data.case_plaintiff=case_plaintiff_list
		case_data.case_defendant=case_defendant_list
		case_data.plaintiff_attorney=list_plaintiff_attorney
		case_data.defendant_attorney=list_defendant_attorney			
		case_data.display_case_details()
		party_info.display_party_info()


class CaseParameter:
	"""
	This class contain all the case data and methods to display data.
	"""
	
	def __init__(self):
		
		self.case_num=None
		self.case_name=None
		self.case_filing_date=None
		self.case_type=None
		self.case_filing_court=None
		self.case_status=None
		self.case_plaintiff_list=[]
		self.case_defendant_list=[]
		self.list_plaintiff_attorney=[]
		self.list_defendant_attorney=[]

	#display case data.
	def display_case_details(self):
		
		print "Case Number       :",self.case_num
		print "Case Name         :",self.case_name
		print "Filing Date       :",self.case_filing_date
		print "Case Type         :",self.case_type
		print "Filing Court      :",self.case_filing_court
		print "Status            :",self.case_status
		print "Plaintiff         :",self.case_plaintiff
		print "Plaintiff Attorney:",self.plaintiff_attorney
		print "Defendant         :",self.case_defendant
		print "Defendant Attorney:",self.defendant_attorney
		print "\n\n"


class CaseStatistics:
	"""
	This class contain case statistics data and methods to display data.
	"""
	
	def __init__(self):
		
		self.total_plaintiff=None
		self.total_defendant=None
		self.total_invalid_case=None
		self.total_success_case=None
		self.total_plaintiff_attorney=None
		self.total_defendant_attorney=None
		
	#display case statistics.	
	def display_case_statistics(self):
		
		print "total plaintiff          :",self.total_plaintiff
		print "total plaintiff attorneys:",self.total_plaintiff_attorney
		print "total defendant          :",self.total_defendant
		print "total defendant attorneys:",self.total_defendant_attorney
		print "total invalid case       :",self.total_invalid_case
		print "total success case       :",self.total_success_case
		
class Party_Type_Info:
	"""
	This class store the defendants and plaintiffs and their first, middle, last, prefix, suffix, fullname, attorney
	and other properties. 
	"""
	
	def __init__(self):
	
		self.plaintiff_list=[]
		self.defendant_list=[]
		self.plaintiff_resolved_name_list=[]
		self.defendant_resolved_name_list=[]
		self.plaintiff_attorney_list=[]
		self.defendant_attorney_list=[]
		self.defendant_address_list=[]
    
	def display_party_info(self):
		
		print "Plaintiff Name          :",self.plaintiff_list
		print "Plaintiff Resolved Name :",self.plaintiff_resolved_name_list
		print "Plaintiff Attorney      :",self.plaintiff_attorney_list
		print "Defendant Name          :",self.defendant_list
		print "Defendant Resolved Name :",self.defendant_resolved_name_list
		print "Defendant Address       :",self.defendant_address_list
		print "Defendant Attorney      :",self.defendant_attorney_list
		print "\n\n"
		
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
 
    	

