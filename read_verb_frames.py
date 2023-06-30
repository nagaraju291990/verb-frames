import sys
import re

fp = open(sys.argv[1], "r")
verb_frames = fp.read().split("\n")
fp.close()

verb_frames_hash = {}
verb_root_flag = 0
sid_flag = 0

for v in verb_frames:
	#print(v)
	v = v.strip()

	if(sid_flag):
		if( re.search(r'^(rh|ras|rsp|rd|r6|k[0-9][a-z]?) *[md] .*', v, re.IGNORECASE) ):
			v = re.sub(r' +', ' ', v)
			#print(v)
			m = re.search(r'^(rh|ras|rsp|rd|r6|k[1-7][apgst]?) ([md]) .*(\[\+[a-z]+(,\+[a-z]+)?\]).*', v,  re.IGNORECASE)
			#m = re.search(r'^(k[1-7][apst]?) ([md]) .*', v)
			#print(m.group())
			krel_nec = m.group(1) + "\t" + m.group(2) + "\t" + m.group(3)	#krel + "\t" + "neccesity" + "\t" + ontology
			sid_flag = 0
			#print(v)
			#print(sid)
			#print(verb_root)
			#print(krel_nec)
			if(verb_root in verb_frames_hash):
				tmp = verb_frames_hash[verb_root]
				#print(tmp)
				#print(type(tmp))
				#print(verb_root + "|" + sid + "\t" + krel)
				verb_frames_hash[verb_root].append( sid + "\t" + krel_nec)
				#print(type(verb_frames_hash[verb_root]))
			else:
				#lst = []
				#print(verb_root + "|" + sid + "\t" + krel)
				verb_frames_hash[verb_root] = [sid + "\t" + krel_nec]
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

#print(verb_frames_hash)

fp = open(sys.argv[2], "r")
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
			m1 = re.search(r'DREL ?:.*\( ?(.*) ?: ?root ?\)', line)
			search_verb_root = m1.group(1)
			search_verb_root = search_verb_root.strip()
			#print("|" + search_verb_root + "|")

			m2 = re.search(r'DREL.*\(\{.*\}\)_\(?(k[1-7][apgst]?)\)?', line)
			search_krel = m2.group(1)
			#print(search_krel)

			matching_sids_on_krel = []
			matching_sids_on_ont = []
			if(search_verb_root in verb_frames_hash):
				verb_frame_value = verb_frames_hash[search_verb_root]
				#print(search_verb_root + ":" + ",".join(verb_frames_hash[search_verb_root]))
				for vf in verb_frame_value:
					vf_array = vf.split("\t")
					if(search_krel == vf_array[1]):
						#print("Matching sid=%s on the basis of krel" %(vf_array[0]))
						matching_sids_on_krel.append(vf_array[0])
						#print(vf_array[3])
						if(vf_array[3] != "[+any]"):
							matching_sids_on_ont.append(vf_array[0])
			print("Matching sids only on krel basis:%s" %(", ".join(matching_sids_on_krel)))
			print("Matching sids on ontology basis:%s" %(", ".join(matching_sids_on_ont)))