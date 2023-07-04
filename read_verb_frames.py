import sys
import re

##read verb frames file
fp = open(sys.argv[1], "r")
verb_frames = fp.read().split("\n")
fp.close()

verb_frames_hash = {}
sid_hash = {}
verb_root_flag = 0
sid_flag = 0

for v in verb_frames:
	#print(v)
	v = v.strip()

	if(sid_flag):
		if( re.search(r'^(rh|ras|rsp|rd|r6|k[0-9][a-z]?) *[md] .*', v, re.IGNORECASE) ):
			v = re.sub(r' +', ' ', v)
			#print(v)
			m = re.search(r'^(rh|ras|rsp|rd|r6|k[1-7][apgst]?) ([md]) .*(\[\+?[a-z]+(, ?\+?[a-z]+)?(, ?\+?[a-z]+)?\]).*', v,  re.IGNORECASE)
			#m = re.search(r'^(k[1-7][apst]?) ([md]) .*', v)
			#print(m.group())
			krel_nec = m.group(1) + "\t" + m.group(2) + "\t" + m.group(3)	#krel + "\t" + "neccesity" + "\t" + ontology
			if(sid in sid_hash):
				sid_hash[sid].append(krel_nec)
			else:
				sid_hash[sid] = [krel_nec]
			#sid_flag = 0
			#print(v)
			#print(sid)
			#print(verb_root)
			#print(krel_nec)
			if(verb_root in verb_frames_hash):
				
				#print(tmp)
				#print(type(tmp))
				#print(verb_root + "|" + sid + "\t" + krel)
				verb_frames_hash[verb_root].append( sid )
				tmp = verb_frames_hash[verb_root]
				tmp = list(set(tmp))
				verb_frames_hash[verb_root] = tmp
				#print(type(verb_frames_hash[verb_root]))
			else:
				#lst = []
				#print(verb_root + "|" + sid + "\t" + krel)
				verb_frames_hash[verb_root] = [sid]
				#print(verb_frames_hash)
	if(verb_root_flag):
		if(re.search(r'^SID::', v)):
			m = re.search(r'^SID::(.*)', v)
			sid = m.group(1)
			#verb_root_flag = 0
			sid_flag = 1

	if(re.search(r'Verb::', v)):
		#print(v)
		m = re.search(r'Verb::(.*)', v)
		verb_root = m.group(1)
		#print(verb_root)
		verb_root_flag = 1
		sid_flag = 0
		#print(verb_root)

	if(re.search(r'\*+', v)):
		sid_flag = 0

#print(verb_frames_hash)
#print(sid_hash)

#read onto dict file
fp = open(sys.argv[2], "r")
onto_lines = fp.read().split("\n")
fp.close()

onto_dict_hash={}

for o in onto_lines:
	print(o)
	if(o == ""):
		continue
	o = o.strip()
	o = re.sub(r' +', ' ', o)
	arr = o.split(" ")
	onto_dict_hash[arr[0]] = arr[1]

#read input file
fp = open(sys.argv[3], "r")
lines = fp.read().split("\n")
fp.close()

sentence_flag = 0
for line in lines:
	#print(line)
	line = line.strip()
	line = re.sub(r' +', ' ',line)

	if(re.search(r'Sentence ?[0-9]+', line),  re.IGNORECASE):
		print(line)
		sentence_flag = 1

	if(sentence_flag):
		if(re.search(r'^DREL ?:', line)):
			line = re.sub(r'( |\t)+', ' ', line)
			m1 = re.search(r'DREL ?:.*\( ?(.*) ?: ?root ?>? ?([A-Za-z ]+)? ?\)?', line)
			search_verb_root = m1.group(1)
			search_verb_root = search_verb_root.strip()

			verb_type = m1.group(2).strip()
			#print("|" + search_verb_root + "|")

			krel_arr = re.findall(r'\(\{.*?\}\)_\(?(rh|ras|rsp|rd|r6|k[1-7][apgst]?)\)?', line)
			#search_krel = m2.group(1)
			#print(krel_arr)

			roots = re.findall(r'\{ ?([\u0900-\u09FF]+) ?, ?NN|NNP|PRP|RB|JJ ?\}', line)#({ ऊ , PRP })_k1 ({ घर , NN })_k2p 
			#print(roots)
			matching_sids_on_krel = []
			matching_sids_on_ont = []
			if(search_verb_root in verb_frames_hash):
				sid_val = verb_frames_hash[search_verb_root]
				for sid_t in sid_val:
					verb_frame_value = sid_hash[sid_t]
					#print(search_verb_root + ":" + ",".join(verb_frame_value))
					flag = 0
					for search_krel in krel_arr:
						for vf in verb_frame_value:
							vf_array = vf.split("\t")
							#print(vf_array[0], search_krel)
							if(search_krel == vf_array[0]):
								flag2 = 1
								break
								#print("Matching sid=%s on the basis of krel" %(vf_array[0]))
								#flag = 1
								#print(vf_array[3])
								#if(vf_array[3] != "[+any]"):
							else:
								flag = -1
						if(flag == 0 and flag2 == 1):
							matching_sids_on_krel.append(sid_t)
							for root in roots:		
								if(root in onto_dict_hash):
									#print(root,vf_array[2], onto_dict_hash[root])
									if(re.search(r''+vf_array[2], onto_dict_hash[root])):
										matching_sids_on_ont.append(sid_t)
				matching_sids_on_ont = list(set(matching_sids_on_ont))
				print("Matching sids only on krel basis:%s" %(", ".join(matching_sids_on_krel)))
				print("Matching sids on ontology basis:%s" %(", ".join(matching_sids_on_ont)))