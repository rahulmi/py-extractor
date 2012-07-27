from BeautifulSoup import BeautifulSoup
from name_case_utility import name_resolver
from extractor_utils import Party_Type_Info,CaseParameter,CaseStatistics

def parse_case_details(casedetail_page):
	
	"""
	    This function extracting the case parameter for each case
	   	(i) case number and case name.
        (ii)basic case details
        (iii)list of Plaintiff and list of dependant and their attorneys for each case.
        (iv)calling name resolver function to seperate name into(prefix,lastname,firstname,lastname,suffix) order.		
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
	#calculates total success case.
	CaseStatistics.total_success_case=CaseStatistics.total_success_case+1
	casedetail_parse_obj=BeautifulSoup(casedetail_page)
	#execute when invalid case found.
	if casedetail_parse_obj.findAll(text="Invalid case number."):
		print "Invalid case number"
		print "\n"
		CaseStatistics.total_invalid_case=CaseStatistics.total_invalid_case+1
		CaseStatistics.total_success_case=CaseStatistics.total_success_case-1
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
			CaseStatistics.total_plaintiff=CaseStatistics.total_plaintiff+1
			
		if  'Defendant' in element.string:
			#calling name resolver function of caseutility script and passing plaintiff name.
			name_resolved_defendant_tuple=name_resolver(str(element.next.next))
			defendant_resolved_name_list.append(name_resolved_defendant_tuple)
			case_defendant_list.append(str(element.next.next))
			CaseStatistics.total_defendant=CaseStatistics.total_defendant+1
			
		if  'Attorney' in element.string:
			#checking previous element of attorney if contain plaintiff, add to plaintiff attorney else defendant.
		    fpe=element.findPreviousSiblings('b')
		    if 'Plaintiff' in fpe[0].string:
		        list_plaintiff_attorney.append(str(element.next.next))
		        #checking attorney is not None
		        if element.next.next!='None':
					CaseStatistics.total_plaintiff_attorney=CaseStatistics.total_plaintiff_attorney+1
					
		    if 'Defendant' in fpe[0].string:
		        list_defendant_attorney.append(str(element.next.next))
		        #checking attorney is not None
		        if element.next.next!='None':
					CaseStatistics.total_defendant_attorney=CaseStatistics.total_defendant_attorney+1
					
			#Execute if Defendant have address
		    if "Defendant"  not in fpe[0].string and "Plaintiff" not in fpe[0].string:
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
