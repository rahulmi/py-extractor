import urllib2,urllib
from BeautifulSoup import BeautifulSoup
import re,sys,cookielib
from optparse import OptionParser
sys.path.append("/home/rahul/py_extractor/")
from Level1.name_case_utility import name_resolver
from Level1.extractor_utils import Party_Type_Info,CaseParameter,CaseStatistics
from Level1.parse_case_info import parse_case_details


class CaseDetails_Level2:
	
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
		
		self.url="http://ec2-174-129-101-141.compute-1.amazonaws.com:8080"
		self.number_of_case_hit=number_of_cases_to_hit
		#case year.
		self.case_year=case_year 
		#case prefix
		self.case_prefix=case_prefix
		#case number.
		self.start_case_number=start_case_number
		self.total_hit=number_of_cases_to_hit + start_case_number
		self.url_opener=None
		self.complete_case_num=None

	def build_url_opener(self):
		
		"""
		Creates the instance of OpenerDirector class to open all the url present in the program and add client 
		browser information(user agent) into header so that all the request looks like it comming from the browser
		and finally return that object
		
		Returns: returns instance of opendirector class.       
		"""
		cookies = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
		user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'
		opener.addheaders = [('User-agent',user_agent)]
		return opener
		
	def parse_case_login_page(self):
		
		"""
		This function parses login page and extract CSRF name and value from  the form and 
		the other  parameter and logged into the site.
		It returns case search page url 
		
		Returns: Url to case search page.
		
		"""
		
		page=self.url_opener.open(self.url)
		page_obj=BeautifulSoup(page)
		text=page_obj.find(text="Login")
		#collects link part of anchor tag and add with url.
		link=text.findPrevious()['href']
		#login page url.
		login_url=self.url+link
		
		login_page=self.url_opener.open(login_url)
		login_obj=BeautifulSoup(login_page)
		login_csrf_token_name=login_obj.body.form.input['name']
		login_csrf_token_value=login_obj.body.form.input['value']
		
		#post parameter to login page.
		query_args = {login_csrf_token_name:login_csrf_token_value, 'username': 'admin', 'password': 'admin', 'this_is_the_login_form':'1'}
		encoded_args = urllib.urlencode(query_args)
		open_case_search_page=self.url_opener.open(login_url,encoded_args)
		url_case_search_page= open_case_search_page.geturl()
		return url_case_search_page
	
	def	loop_to_total_case_to_hit(self,url):
		
		""" 
		(i)This function runs a loop from start case number to  number of
	    cases to hit and call hit case url function for each
		case number. 
		(ii)Its creating object of class CaseParameter and assigning statistics details. 
		
		Args: Url of case search page.
		
		"""
		
		for case_num in range(self.start_case_number,self.total_hit):
			self.case_hit_url(url,case_num)
			
		CaseStatistics().display_case_statistics()
		
	def case_hit_url(self,temp_url, temp_case_num):
		
		"""
        (I) This function takes the case search page url and case number as input and using this parameter along with csrf value
            open the resultant case page.
            
        (II)call the function loop_to_multiple_result with resultant page parse object. 
        
        Args: I) Url to case search page.
              II)Case number to be hit.
	    """
	    
		#convert case number to 6 digit formate.
		formatted_case_num="%06d"%temp_case_num 
		#full case number with prefix year. 
		self.complete_case_num=self.case_year+self.case_prefix+formatted_case_num
		case_search_url=temp_url
		open_case_search_page=self.url_opener.open(case_search_url)
		parse_obj_case_search_page=BeautifulSoup(open_case_search_page)
		case_search_csrf_token_name=parse_obj_case_search_page.body.form.input['name']
		case_search_csrf_token_value=parse_obj_case_search_page.body.form.input['value']
		
		#post parameter to case search page.
		case_query_params={case_search_csrf_token_name:case_search_csrf_token_value,'case_id':self.complete_case_num}
		encoded_params = urllib.urlencode(case_query_params)
		open_resultant_case_search_page=self.url_opener.open(case_search_url,encoded_params)
		parse_obj_resultant_case_search_page=BeautifulSoup(open_resultant_case_search_page)
		self.loop_to_multiple_result(parse_obj_resultant_case_search_page)
		
	def loop_to_multiple_result(self,multiple_result_page):
		
		"""
		This function takes the parse object of multiple result page and parse all the link present inside page 
		and call case parse details function  to collects all the information from the case details page.  
		
		Args: Parse object of resultant court case page.
		
		"""
		#checking for the invalid case number.
		for case_link in multiple_result_page.findAll('li'):
			
		    if multiple_result_page.find(text='Invalid case number.'):
				print "Invalid case number",self.complete_case_num
				print "\n"
				CaseStatistics.total_invalid_case=CaseStatistics.total_invalid_case+1
				return
			#finding all the links inside the page and with domain url.
		    case_url=self.url+case_link.findNext('a')['href']
		    #open the case detail page.
		    case_details_page = self.url_opener.open(case_url)
		    parse_case_details(case_details_page)
		
	

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
        casedetail_obj=CaseDetails_Level2(case_year,case_prefix,start_case_number,number_of_cases_to_hit)
        #calling this function to get opener object and set into class casedetails.
        url_opener=casedetail_obj.build_url_opener()
        casedetail_obj.url_opener=url_opener
        #calling classdetail method
        url=casedetail_obj.parse_case_login_page() 
        casedetail_obj.loop_to_total_case_to_hit(url)
        
		
if __name__=='__main__':
    main()	
