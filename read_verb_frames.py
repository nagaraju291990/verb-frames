import sys
import re
from itertools import zip_longest
##read verb frames file
fp = open(sys.argv[1], "r")
verb_frames = fp.read().split("\n")
fp.close()

verb_frames_hash = {}
sid_krel_hash = {}
sid_onto_hash = {}
sid_verb_class_hash = {}
verb_root_flag = 0
sid_flag = 0

for v in verb_frames:
	#print(v)
	v = v.strip()
	#v = v.lower()
	if(sid_flag):
		if(re.search(r'Verb_class::', v, re.IGNORECASE)):
			verb_class = re.sub(r'Verb_class::', '', v, re.IGNORECASE)
			verb_class = verb_class.lower()
			verb_class = verb_class.strip()
			sid_verb_class_hash[sid] = verb_class

		if( re.search(r'^(rh|ras|rsp|rd|r6|k[0-9][a-z]?) *[md] .*', v, re.IGNORECASE) ):
			v = re.sub(r' +', ' ', v)
			#print(v)
			m = re.search(r'^(rh|ras|rsp|rd|r6|k[1-7][apgst]?) ([md]) .*(\[\+?[a-z]+(, ?\+?[a-z]+)?(, ?\+?[a-z]+)?\]).*', v,  re.IGNORECASE)
			#m = re.search(r'^(k[1-7][apst]?) ([md]) .*', v)
			#print(m.group())
			krel_nec = m.group(1) # "\t" + m.group(2) + "\t" + m.group(3)	#krel + "\t" + "neccesity" + "\t" + ontology
			krel_onto = m.group(1) + "\t" + m.group(3)
			if(sid in sid_krel_hash):
				sid_krel_hash[sid].append(krel_nec)
			else:
				sid_krel_hash[sid] = [krel_nec]
			if(sid in sid_onto_hash):
				sid_onto_hash[sid].append(krel_onto)
			else:
				sid_onto_hash[sid] = [krel_onto]
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
	#print(o)
	if(o == ""):
		continue
	o = o.strip()
	o = re.sub(r' +', ' ', o)
	o = re.sub(r' \+', '+', o)
	arr = o.split(" ")
	#print(arr[0] + "|" + arr[1])
	onto_feature = arr[1]
	#onto_feature = re.sub(r'[\[\]]', '', onto_feature)
	#onto_features = onto_feature.split(",")
	onto_dict_hash[arr[0]] = onto_feature

#print(onto_dict_hash)
#read input file
fp = open(sys.argv[3], "r")
lines = fp.read().split("\n")
fp.close()

sentence_flag = 0
for line in lines:
	#print(line)
	line = line.strip()
	line = re.sub(r' +', ' ',line)
	#line = line.lower()

	if(re.search(r'Sentence ?[0-9]+', line),  re.IGNORECASE):
		print(line)
		sentence_flag = 1

	if(sentence_flag):
		if(re.search(r'^DREL ?:', line)):
			line = re.sub(r'( |\t)+', ' ', line)
			m1 = re.search(r'DREL ?:.*\( ?(.*) ?: ?root ?>? ?([A-Za-z ]+)? ?\)?', line)
			search_verb_root = m1.group(1)
			search_verb_root = search_verb_root.strip()

			search_verb_class = m1.group(2).strip().lower()
			#print("|" + verb_type + "|")

			krel_arr = re.findall(r'\(\{.*?\}\)_\(?(rh|ras|rsp|rd|r6|[Kk][1-7][apgst]?)\)?', line)
			#search_krel = m2.group(1)
			#print(krel_arr)

			chunks = re.findall(r'\((.*?)\)_(rh|ras|rsp|rd|r6|[Kk][1-7][apgst]?)', line)#[({ ऊ , PRP })_k1, ({ घर , NN })_k2p ]
			#print(chunks)
			matching_sids_on_krel = []
			matching_sids_on_ont = []
			matching_sids_on_verb_type = []
			if(search_verb_root in verb_frames_hash):
				sid_val = verb_frames_hash[search_verb_root]
				for sid_t in sid_val:
					verb_frame_value = sid_krel_hash[sid_t]
					#print(sid_t + ":" + search_verb_root + ":" + ",".join(verb_frame_value))
					flag = 0
					krel_arr.sort()
					verb_frame_value.sort()
					for index, (search_krel,vf) in enumerate(zip_longest(krel_arr, verb_frame_value, 
                                              fillvalue=object())):
						#for vf in verb_frame_value:
							#print(search_krel, vf)
							#vf_array = vf.split("\t")
							#print(vf_array[0], search_krel)
							if(search_krel != vf):
								flag = 1
							#else:
								#flag = -1
								#break
					if(flag == 0):
						matching_sids_on_krel.append(sid_t)
					if(len(matching_sids_on_krel) > 1):
						for sd in matching_sids_on_krel:
							#roots = re.search(r'')
							verb_frame_value = sid_onto_hash[sd]
							for vf in verb_frame_value:
								vf_array = vf.split("\t")
								for chunk in chunks:
									#print(chunk[1] + ":" + vf_array[0])
									if(chunk[1] == vf_array[0]):
										try:
											root = re.findall(r'.*{ ?(.*) ?, ?NN|NNP|PRP ?\}', chunk
											[0])[-1].strip()
										except:
											root = ''
										#print(root)
										if(root):
											#print("s"+chunk[1])
											#print(root)
											if(root in onto_dict_hash):
												print(vf_array[1] + '----' + onto_dict_hash[root])
												#if(re.search(r'' + vf_array[1], onto_dict_hash[root])):
												if(vf_array[1] == onto_dict_hash[root]):
													matching_sids_on_ont.append(sd)
				#matching_sids_on_ont = list(set(matching_sids_on_ont))
					if(len(matching_sids_on_ont) > 1):
						for sd in matching_sids_on_ont:
							if(sd in sid_verb_class_hash):
								#print(sid_verb_class_hash[sd] + '---' + search_verb_class)
								if(sid_verb_class_hash[sd] == search_verb_class):
									matching_sids_on_verb_type.append(sd)
					elif(len(matching_sids_on_ont) == 0 and len(matching_sids_on_krel) > 1):
						for sd in matching_sids_on_krel:
							if(sd in sid_verb_class_hash):
								#print(sid_verb_class_hash[sd] + '---' + search_verb_class)
								if(sid_verb_class_hash[sd] == search_verb_class):
									matching_sids_on_verb_type.append(sd)
				matching_sids_on_ont = list(set(matching_sids_on_ont))
				matching_sids_on_verb_type = list(set(matching_sids_on_verb_type))

				matching_sids_on_ont.sort()
				matching_sids_on_krel.sort()
				matching_sids_on_verb_type.sort()
				print("Matching sids only on krel basis:%s" %(", ".join(matching_sids_on_krel)))
				print("Matching sids on ontology basis:%s" %(", ".join(matching_sids_on_ont)))
				print("Matching sids on verb class basis:%s" %(", ".join(matching_sids_on_verb_type)))