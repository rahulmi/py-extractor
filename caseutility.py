import re

def name_resolver(party_name):
	"""
	This function seperating the defendant and plaintiff names into prefix,firstname,middlename,lastname,suffix
	and returns tuple(prefix,lastname,firstname,middlename,suffix).
	"""
	first_name=None
	last_name=None
	middle_name=None
	prefix=None
	suffix=None
	#search patterns for prefix and suffix.
	prefix_pattern=re.compile(r'(^|\s)(mr\.|mr|ms\.|ms|mrs\.|mrs|md|m\.d\.|dr|d\.r\.)(\s|\.|$)',re.I)
	suffix_pattern=re.compile(r'(^|\s)(jr|jr\.|sr\.|sr|I|II|III|IV|V|VIII|VII|VI)(\s|\.\s|$)',re.I)
	#searching prefix and putting into prefix variable
	match_prefix=re.search(prefix_pattern,party_name)
	if match_prefix:
		prefix=match_prefix.group()
	#searching suffix and putting into suffix variable.	
	match_suffix=re.search(suffix_pattern,party_name)
	if match_suffix:
		suffix=match_suffix.group()
		
	#replacing prefix and suffix with space.so that we can get the original name.
	match_str=re.sub(prefix_pattern," ",party_name)
	name=re.sub(suffix_pattern," ",match_str)
	#spliting name into three parts(last first middle).
	name_list=name.split(None,2)
	if len(name_list)==1:
		first_name=name_list[0]
	if len(name_list)==2:
		first_name=name_list[1]
		last_name=name_list[0]
	if len(name_list)==3:
		first_name=name_list[1]
		last_name=name_list[0]
		middle_name=name_list[2]
	name_tuple=(prefix,last_name,first_name,middle_name,suffix)
	return name_tuple
