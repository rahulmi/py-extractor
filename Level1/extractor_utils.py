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


	#display case data.
	def display_case_details(self):
		
		print "Case Number       :",self.case_num
		print "Case Name         :",self.case_name
		print "Filing Date       :",self.case_filing_date
		print "Case Type         :",self.case_type
		print "Filing Court      :",self.case_filing_court
		print "Status            :",self.case_status
		print "\n"


class CaseStatistics:
	
	"""
	This class contain case statistics data and methods to display data.
	"""
	
	total_plaintiff=0
	total_defendant=0
	total_invalid_case=0
	total_success_case=0
	total_plaintiff_attorney=0
	total_defendant_attorney=0
		
	#display case statistics.	
	def display_case_statistics(self):
		
		print "total plaintiff          :",CaseStatistics.total_plaintiff
		print "total plaintiff attorneys:",CaseStatistics.total_plaintiff_attorney
		print "total defendant          :",CaseStatistics.total_defendant
		print "total defendant attorneys:",CaseStatistics.total_defendant_attorney
		print "total invalid case       :",CaseStatistics.total_invalid_case
		print "total success case       :",CaseStatistics.total_success_case
		
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
		print "\n"
