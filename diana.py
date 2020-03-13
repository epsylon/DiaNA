#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
DiaNA - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with DiaNA; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
VERSION = "v0.1_beta"
RELEASE = "16032020"
SOURCE1 = "https://code.03c8.net/epsylon/diana"
SOURCE2 = "https://github.com/epsylon/diana"
CONTACT = "epsylon@riseup.net - (https://03c8.net)"
"""
DNA-equiv:
 A <-> T
 C <-> G
"""
import re, os, glob, random, time, math 

brain_path = "datasets/brain.in" # in/out brain-tmp file
genomes_path = 'datasets/' # genome datasets raw data
genomes_list_path = "datasets/genome.list" # genome list
dna_letters = ["A", "T", "G", "C", "N"] # dna alphabet [n for ANY nucl.]
genomes = {} # main sources dict: genome_name
seeds_checked = [] # list used for random checked patterns
repeats = {} # repetitions 'tmp' dict: genome_name:(repets,pattern)
known_patterns = [] # list used for known patterns
estimated_max_range_for_library_completed = 20 # [MAX. LENGTH] for range [PATTERN]
estimated_patterns_for_library_completed = 1466015503700 # x = y+4^z
estimated_quantity_per_pattern_for_library_completed = int(estimated_patterns_for_library_completed / estimated_max_range_for_library_completed)

def convert_size(size):
    if (size == 0):
        return '0 B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return s, size_name[i]

def search_pattern_with_human():
    pattern = input("[HUMAN] [SEARCH] Pattern (ex: attacg): ").upper()
    print("\n"+"-"*5 + "\n")
    create_new_pattern(pattern) # create new pattern

def try_pattern_against_all_genomes(pattern):
    patterns_found = 0
    for k, v in genomes.items():
        if pattern in v:
            t = len(re.findall(pattern, v))
            print (" *", k +":", "-> [",t,"times ]")
            repeats[k] = t, pattern
            patterns_found = patterns_found + 1
            print("")
    if patterns_found == 0:
        print("[INFO] -> Not any found! ... [EXITING!]\n")

def sanitize_dna_pattern(pattern):
    valid_pattern = True
    for c in pattern:
        if c == "A":
            pass
        elif c == "T":
            pass
        elif c == "G":
            pass
        elif c == "C":
            pass
        elif c == "N":
            pass
        else:
            valid_pattern = False
    return valid_pattern

def teach_ai():
    mode = input("[TRAIN-AI] MODE -> (H)uman, (A)utomata: ").upper()
    if not os.path.isfile(brain_path):
        create_initial_seed_file()
    if mode == "H": # human mode
        teach_ai_human_mode()
    else: # libre AI
        teach_ai_automata_mode() # automata mode

def teach_ai_human_mode(): # search/discard patterns with human interaction & generate local database
    search_patterns_lesson_with_a_human()

def search_patterns_lesson_with_a_human():
    print("\n"+"-"*30)
    print("\n[TRAIN-AI] [HUMAN] [STOP] this mode; just entering whatever invalid pattern (ex: 'exit' or 'q').\n")
    key = "K" # continue
    while key == "K":
        pattern = input("[TRAIN-AI] [HUMAN] [LOOP] [SEARCH] Pattern (ex: attacg): ").upper()
        print("\n"+"-"*5 + "\n")
        key = search_pattern_on_lesson(pattern)
        if key == "Z": # stop
            break

def search_pattern_on_lesson(pattern):
    valid_pattern = sanitize_dna_pattern(pattern)
    if valid_pattern == True:
        key = search_pattern_on_local_database(pattern) # search pattern on local database
    else:
        print("[ERROR] -> Invalid DNA pattern ... [EXITING!]\n")
        key = "Z" # stop
    return key

def search_pattern_on_local_database(pattern):
    f=open(brain_path, 'r')  
    memory = f.read().replace('\n',' ')
    f.close()
    patterns_known = 0
    if not "'"+pattern+"'" in memory: # always create new patterns
        create_new_pattern(pattern) # create new pattern
        patterns_known = patterns_known + 1
    else:
        for k, v in genomes.items(): # create patterns found for new genomes
            if k not in memory:
                create_new_pattern(pattern) # create new pattern
                patterns_known = patterns_known + 1
    if patterns_known == 0:
        print("[TRAIN-AI] [AUTOMATA] [LOOP] [RESULTS] -ALREADY- [LEARNED!] ... -> [GOING FOR NEXT!]\n")
    print("-"*5 + "\n")
    key = "K" # continue
    return key

def create_initial_seed_file():
    f=open(brain_path, 'w')
    f.write("")
    f.close()    

def create_new_pattern(pattern): # append it to brain
    valid_pattern = sanitize_dna_pattern(pattern)
    if valid_pattern == True:
        if pattern not in known_patterns:
            known_patterns.append(pattern)
            try_pattern_against_all_genomes(pattern)
    f=open(brain_path, 'a')    
    f.write(str(repeats)+os.linesep) # add dict as str
    f.close()

def teach_ai_automata_mode(): # search patterns by bruteforcing ranges & generate local database
    search_patterns_lesson_with_an_ai()

def search_patterns_lesson_with_an_ai():
    print("\n"+"-"*30)
    print("\n[TRAIN-AI] [AUTOMATA] [STOP] this mode; pressing 'CTRL+z'.\n")
    ranges = input("[TRAIN-AI] [AUTOMATA] [SEARCH] Set range (x<y) for pattern deep searching (ex: 2-8): ")
    print ("")
    valid_range, ranged_permutations = check_for_deep_searching_ranges(ranges)
    if str(valid_range) == "OK!":
        ranged_ending = False
        print("-"*15)
        print("\n[TRAIN-AI] [AUTOMATA] [SEARCH] Number of [PERMUTATIONS] estimated: [ "+str(ranged_permutations)+" ]\n")
        print("-"*15+"\n")
        num_pat = 0
        time.sleep(10)
        while ranged_ending == False: # try to STOP it using: CTRL-z
            try:
                pattern, ranged_ending = generate_random_pattern(ranges, ranged_permutations) # generate random seed
                if pattern:
                    num_pat = num_pat + 1
                    print("[TRAIN-AI] [AUTOMATA] [LOOP] [SEARCH] Generating [RANDOM!] ["+str(num_pat)+"/"+str(ranged_permutations)+"] pattern: [ " + str(pattern) + " ]\n")
                    if not num_pat == ranged_permutations:
                        search_pattern_on_lesson(pattern)
                    else:
                        search_pattern_on_lesson(pattern)
                        print("[TRAIN-AI] [AUTOMATA] [RESULTS]: REVIEWED -> [ "+str(ranged_permutations)+" PERMUTATIONS ] ... -> [EXITING!]\n")
                        ranged_ending = True
            except:
                pass
    else:
        print("-"*15+"\n")
        print("[TRAIN-AI] [AUTOMATA] [ERROR] -> [INVALID!] Deep Learning [RANGE] -> "+valid_range+" ... [EXITING!]\n")

def generate_random_pattern(ranges, ranged_permutations):
    ranged_length = 0
    try:
        range_low = int(ranges.split("-")[0])
        range_high = int(ranges.split("-")[1])
        for i in range(range_low, range_high+1):
            ranged_length = ranged_length + 1
            if ranged_length == ranged_permutations: # all possible variables have been bruteforced/checked! -> exit
                pattern = None
                ranged_ending = True
                return pattern, ranged_ending
            else:
                ranged_ending = False
                seed = [random.randrange(0, 4) for _ in range(i)] # generate "random" seed
                if seed not in seeds_checked:
                    seeds_checked.append(seed)
                    pattern = ""
                    for n in seed:
                        if n == 0:
                            pattern += "A"
                        elif n == 1:
                            pattern += "C"
                        elif n == 2:
                            pattern += "T"
                        else:
                            pattern += "G"
                    return pattern, ranged_ending
    except:
        print("[TRAIN-AI] [AUTOMATA] [ERROR] -> [INVALID!] Deep Learning [RANGE] ... [EXITING!]\n")
        pattern = None
        ranged_ending = True
        return pattern, ranged_ending

def check_for_deep_searching_ranges(ranges):
    try:
        range_low = ranges.split("-")[0]
        range_high = ranges.split("-")[1]
    except:
        valid_range = "'bad format'"
    try:
        range_low = int(range_low)
    except:
        valid_range = "'low range' should be an integer"
    try:
        range_high = int(range_high)
    except:
        valid_range = "'high range' should be an integer"
    try:
        if range_low < range_high:
            if range_low > 1: # always range > 1
                valid_range = "OK!"
            else:
                valid_range = "'low range' should be > than 1"
        else:
            valid_range = "'low range' should be < than 'high range'"
    except:
        valid_range = "'bad format'"
    try:
        ranged_permutations = math_ranged_permutations(range_low, range_high)
    except:
        ranged_permutations = 0
        valid_range = "'bad format'"
    return valid_range, ranged_permutations

def math_ranged_permutations(range_low, range_high): # calculate ranged_permutations
    ranged_permutations = 0
    for i in range(range_low, range_high+1):
        ranged_permutations = ranged_permutations + (4**i)
    return ranged_permutations

def libre_ai(): # show statistics / download new genomes / keep crossing new genomes with local database / search for new patterns (non stop!)
    if not os.path.isfile(brain_path):
        create_initial_seed_file()
    memory = examine_stored_brain_memory() 
    if memory != "":
        #print("[LIBRE-AI] [STOP] this mode; pressing 'CTRL+z'.\n")
        libre_ai_show_statistics(memory) # show statistics

def libre_ai_show_statistics(memory):
    print("[LIBRE-AI] [REPORTING] [STATISTICS] ... -> [STARTING!]\n")
    print("-"*15 + "\n")
    total_genomes = 0
    total_adenine = 0
    total_guanine = 0
    total_cytosine = 0
    total_thymine = 0
    total_any = 0
    secuence_length = 0
    secuences_list = {}
    largest = None
    largest_len = 0
    shortest_len = 0
    average = None
    shortest = None
    for k, v in genomes.items():
        secuence_length = len(v)
        secuences_list[k] = str(secuence_length)
        total_genomes = total_genomes + 1
        total_adenine = total_adenine + v.count("A")
        total_guanine = total_guanine + v.count("G")
        total_cytosine = total_cytosine + v.count("C")
        total_thymine = total_thymine + v.count("T")
        total_any = total_any + v.count("N")
    largest = max(secuences_list, key=secuences_list.get)
    shortest = min(secuences_list, key=secuences_list.get) 
    for k, v in genomes.items():
        if k == largest:
            largest_len = len(v)
        elif k == shortest:
            shortest_len = len(v)
        else:
            pass
    path = genomes_path # genome datasets raw data
    l = glob.glob(genomes_path+"*") # black magic!
    latest_collection_file = max(l, key=os.path.getctime)
    latest_collection_date = time.ctime(os.path.getmtime(latest_collection_file))
    total_nucleotids = [total_adenine, total_guanine, total_cytosine, total_thymine, total_any]
    num_total_nucleotids = total_adenine + total_guanine + total_cytosine + total_thymine + total_any
    nucleotid_more_present = max(total_nucleotids)
    print("[LIBRE-AI] [REPORTING] -STORAGE- [STATISTICS]: \n")
    extract_storage_sizes()
    print(" * [LATEST UPDATE]: '"+str(latest_collection_date)+"'\n")
    print("   + File: '"+str(latest_collection_file)+"'\n")
    print("-"*5 + "\n")
    print("[LIBRE-AI] [REPORTING] -COLLECTION- [STATISTICS]: \n")
    extract_total_patterns_learned_from_local(memory)
    print("\n"+"-"*5 + "\n")
    print("[LIBRE-AI] [REPORTING] -ANALYSIS- [STATISTICS]: \n")
    print(" * Total [DNA SECUENCES]: [ "+str(total_genomes)+" ]\n")
    print("   + [LARGEST]: "+str(largest)+ " [ "+str(largest_len)+" bp linear RNA ]")
    print("   + [SHORTEST]: "+str(shortest)+ " [ "+str(shortest_len)+" bp linear RNA ]\n")
    print(" * Total [NUCLEOTIDS]: [ "+str(num_total_nucleotids)+" ]\n")
    if nucleotid_more_present == total_adenine:
        print("   + [A] Adenine  : "+str(total_adenine)+" <- [MAX]")
    else:
        print("   + [A] Adenine  : "+str(total_adenine))
    if nucleotid_more_present == total_guanine:
        print("   + [G] Guanine  : "+str(total_guanine)+" <- [MAX]")
    else:
        print("   + [G] Guanine  : "+str(total_guanine))
    if nucleotid_more_present == total_cytosine:
        print("   + [C] Cytosine : "+str(total_cytosine)+" <- [MAX]")
    else:
        print("   + [C] Cytosine : "+str(total_cytosine))
    if nucleotid_more_present == total_thymine:
        print("   + [T] Thymine  : "+str(total_thymine)+" <- [MAX]")
    else:
        print("   + [T] Thymine  : "+str(total_thymine))
    if total_any > 0:
        if nucleotid_more_present == total_any:
            print("   + [N]  *ANY*   : "+str(total_any)+" <- [MAX]\n")
        else:
            print("   + [N]  *ANY*   : "+str(total_any)+"\n")
    print("-"*5 + "\n")
    extract_pattern_most_present_local(memory)

def convert_memory_to_dict(memory): # [index] = genome_name, pattern, num_rep
    memory_dict = {}
    index = 0
    for m in memory:
        regex_record = "'(.+?)': (.+?), '(.+?)'" # regex magics! - extract first each record 
        pattern_record = re.compile(regex_record)
        record = re.findall(pattern_record, m)
        for r in record: # now extract each field
            index = index + 1
            name = str(r).split("', '(")[0]
            genome_name = str(name).split("'")[1]
            repeats = str(r).split("', '(")[1]
            genome_repeats = str(repeats).split("',")[0]
            pattern = str(repeats).split("',")[1]
            genome_pattern = pattern.replace(" ", "")
            genome_pattern = genome_pattern.replace("'", "")
            genome_pattern = genome_pattern.replace(")", "")  
            memory_dict[index] = genome_name, genome_pattern, genome_repeats # generate memory_dict!
    return memory_dict

def extract_pattern_most_present_local(memory):
    memory_dict = convert_memory_to_dict(memory)
    if memory_dict:
        print("[LIBRE-AI] [REPORTING] -RESEARCHING- [STATISTICS]: \n")
        total_patterns_found = 0
        total_genomes = 0
        for k, v in memory_dict.items():
            total_patterns_found = total_patterns_found + 1
        for k, v in genomes.items():
            total_genomes = total_genomes + 1
        print(" * [ "+str(total_patterns_found)+" ] [PATTERNS FOUND!] in: [ "+str(total_genomes)+ " ] [DNA SECUENCES]\n")

def extract_storage_sizes():
    total_dataset_size = 0
    total_files_size = 0
    total_list_size = 0
    for file in glob.iglob(genomes_path + '**/*', recursive=True):
        if(file.endswith(".genome")):
            total_dataset_size = total_dataset_size + len(file)
        elif(file.endswith(".in")):
            total_brain_size = len(file)
        elif(file.endswith(".list")):
            total_list_size = len(file)
    if total_dataset_size > 0:
        total_files_size = int(total_files_size) + int(total_dataset_size)
        dataset_s, dataset_size_name = convert_size(total_dataset_size)
        total_dataset_size = '%s %s' % (dataset_s,dataset_size_name)
    if total_brain_size > 0:
        total_files_size = int(total_files_size) + int(total_brain_size)
        brain_s, brain_size_name = convert_size(total_brain_size)
        total_brain_size = '%s %s' % (brain_s,brain_size_name)
    if total_list_size > 0:
        total_files_size = int(total_files_size) + int(total_list_size)
        list_s, list_size_name = convert_size(total_list_size)
        total_list_size = '%s %s' % (list_s,list_size_name)
    total_s, total_size_name = convert_size(total_files_size)
    total_files_size = '%s %s' % (total_s,total_size_name)
    print(" * Total [FILE SIZES]: "+str(total_files_size)+"\n")
    if total_dataset_size:
        print("   + [DATASET]: "+str(total_dataset_size))
    if total_list_size:
        print("   + [LIST]: "+str(total_list_size))
    if total_brain_size:
        print("   + [BRAIN]: "+str(total_brain_size)+"\n")

def extract_total_patterns_learned_from_local(memory):
    total_patterns = 0
    for m in memory:
        total_patterns = total_patterns + 1
    print(" * [SETTINGS] Using [MAX. LENGTH] for range [PATTERN] = "+str(estimated_max_range_for_library_completed)+"\n")
    if total_patterns < estimated_patterns_for_library_completed:
        library_completion = (total_patterns/estimated_patterns_for_library_completed)*100
        print("   + [LIBRARY COMPLETED]: [ "+str('%.20f' % library_completion)+"% ]")
        if total_patterns > 0:
            print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" / "+str(estimated_patterns_for_library_completed)+" ] \n")
        else:
            print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" / "+str(estimated_patterns_for_library_completed)+" ]")
    else:
        total_current_library_completion = (total_patterns/estimated_patterns_for_library_completed)*100
        library_completion = 100
        print("   + [LIBRARY COMPLETED]: [ "+str(library_completion)+"% ]")
        print("   + [CURRENT LIBRARY]  : [ "+str('%.00f' % total_current_library_completion)+"% ] -> [ATTENTION!]: INCREASED [MAX. LENGTH] for range [PATTERN] -> REQUIRED!")
        if total_patterns > 0:
            print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" ]\n")
        else:
            print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" ]")
    pattern_len_1 = 0
    pattern_len_2 = 0
    pattern_len_3 = 0
    pattern_len_4 = 0
    pattern_len_5 = 0
    pattern_len_6 = 0
    pattern_len_7 = 0
    pattern_len_8 = 0
    pattern_len_9 = 0
    pattern_len_10 = 0
    pattern_len_11 = 0
    pattern_len_12 = 0
    pattern_len_13 = 0
    pattern_len_14 = 0
    pattern_len_15 = 0
    pattern_len_16 = 0
    pattern_len_17 = 0
    pattern_len_18 = 0
    pattern_len_19 = 0
    pattern_len_20 = 0
    for m in memory:
        pattern_len = m.split(", '")[1]
        pattern_len = pattern_len.split("')")[0]
        pattern_len = len(pattern_len)
        if pattern_len == 1:
            pattern_len_1 = pattern_len_1 + 1
        elif pattern_len == 2:
            pattern_len_2 = pattern_len_2 + 1
        elif pattern_len == 3:
            pattern_len_3 = pattern_len_3 + 1
        elif pattern_len == 4:
            pattern_len_4 = pattern_len_4 + 1
        elif pattern_len == 5:
            pattern_len_5 = pattern_len_5 + 1
        elif pattern_len == 6:
            pattern_len_6 = pattern_len_6 + 1
        elif pattern_len == 7:
            pattern_len_7 = pattern_len_7 + 1
        elif pattern_len == 8:
            pattern_len_8 = pattern_len_8 + 1
        elif pattern_len == 9:
            pattern_len_9 = pattern_len_9 + 1
        elif pattern_len == 10:
            pattern_len_10 = pattern_len_10 + 1
        elif pattern_len == 11:
            pattern_len_11 = pattern_len_11 + 1
        elif pattern_len == 12:
            pattern_len_12 = pattern_len_12 + 1
        elif pattern_len == 13:
            pattern_len_13 = pattern_len_13 + 1
        elif pattern_len == 14:
            pattern_len_14 = pattern_len_14 + 1
        elif pattern_len == 15:
            pattern_len_15 = pattern_len_15 + 1
        elif pattern_len == 16:
            pattern_len_16 = pattern_len_16 + 1
        elif pattern_len == 17:
            pattern_len_17 = pattern_len_17 + 1
        elif pattern_len == 18:
            pattern_len_18 = pattern_len_18 + 1
        elif pattern_len == 19:
            pattern_len_19 = pattern_len_19 + 1
        else:
            pattern_len_20 = pattern_len_20 + 1
    if pattern_len_1 < 101:
        progression_len_1 = pattern_len_1 * "*"
    else:
        progression_len_1 = 100 * "*+"+str(pattern_len_1-100)
    if pattern_len_2 < 101:
        progression_len_2 = pattern_len_2 * "*"
    else:
        progression_len_2 = 100 * "*+"+str(pattern_len_2-100)
    if pattern_len_3 < 101:
        progression_len_3 = pattern_len_3 * "*"
    else:
        progression_len_3 = 100 * "*+"+str(pattern_len_3-100)
    if pattern_len_4 < 101:
        progression_len_4 = pattern_len_4 * "*"
    else:
        progression_len_4 = 100 * "*"+" 100+"+str(pattern_len_4-100)
    if pattern_len_5 < 101:
        progression_len_5 = pattern_len_5 * "*"
    else:
        progression_len_5 = 100 * "*+"+str(pattern_len_5-100)
    if pattern_len_6 < 101:
        progression_len_6 = pattern_len_6 * "*"
    else:
        progression_len_6 = 100 * "*+"+str(pattern_len_6-100)
    if pattern_len_7 < 101:
        progression_len_7 = pattern_len_7 * "*"
    else:
        progression_len_7 = 100 * "*+"+str(pattern_len_7-100)
    if pattern_len_8 < 101:
        progression_len_8 = pattern_len_8 * "*"
    else:
        progression_len_8 = 100 * "*+"+str(pattern_len_8-100)
    if pattern_len_9 < 101:
        progression_len_9 = pattern_len_9 * "*"
    else:
        progression_len_9 = 100 * "*+"+str(pattern_len_9-100)
    if pattern_len_10 < 101:
        progression_len_10 = pattern_len_10 * "*"
    else:
        progression_len_10 = 100 * "*+"+str(pattern_len_10-100)
    if pattern_len_11 < 101:
        progression_len_11 = pattern_len_11 * "*"
    else:
        progression_len_11 = 100 * "*+"+str(pattern_len_11-100)
    if pattern_len_12 < 101:
        progression_len_12 = pattern_len_12 * "*"
    else:
        progression_len_12 = 100 * "*+"+str(pattern_len_12-100)
    if pattern_len_13 < 101:
        progression_len_13 = pattern_len_13 * "*"
    else:
        progression_len_13 = 100 * "*+"+str(pattern_len_13-100)
    if pattern_len_14 < 101:
        progression_len_14 = pattern_len_14 * "*"
    else:
        progression_len_14 = 100 * "*+"+str(pattern_len_14-100)
    if pattern_len_15 < 101:
        progression_len_15 = pattern_len_15 * "*"
    else:
        progression_len_15 = 100 * "*+"+str(pattern_len_15-100)
    if pattern_len_16 < 101:
        progression_len_16 = pattern_len_16 * "*"
    else:
        progression_len_16 = 100 * "*+"+str(pattern_len_16-100)
    if pattern_len_17 < 101:
        progression_len_17 = pattern_len_17 * "*"
    else:
        progression_len_17 = 100 * "*+"+str(pattern_len_17-100)
    if pattern_len_18 < 101:
        progression_len_18 = pattern_len_18 * "*"
    else:
        progression_len_18 = 100 * "*+"+str(pattern_len_18-100)
    if pattern_len_19 < 101:
        progression_len_19 = pattern_len_19 * "*"
    else:
        progression_len_19 = 100 * "*+"+str(pattern_len_19-100)
    if pattern_len_20 < 101:
        progression_len_20 = pattern_len_20 * "*"
    else:
        progression_len_20 = 100 * "*+"+str(pattern_len_20-100)
    if pattern_len_1 > 0:
        print("     - [length = 1]  | "+progression_len_1 + " [ "+str(pattern_len_1)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_2 > 0:
        print("     - [length = 2]  | "+progression_len_2 + " [ "+str(pattern_len_2)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_3 > 0:
        print("     - [length = 3]  | "+progression_len_3 + " [ "+str(pattern_len_3)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_4 > 0:
        print("     - [length = 4]  | "+progression_len_4 + " [ "+str(pattern_len_4)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_5 > 0:
        print("     - [length = 5]  | "+progression_len_5 + " [ "+str(pattern_len_5)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_6 > 0:
        print("     - [length = 6]  | "+progression_len_6 + " [ "+str(pattern_len_6)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_7 > 0:
        print("     - [length = 7]  | "+progression_len_7 + " [ "+str(pattern_len_7)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_8 > 0:
        print("     - [length = 8]  | "+progression_len_8 + " [ "+str(pattern_len_8)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_9 > 0:
        print("     - [length = 9]  | "+progression_len_9 + " [ "+str(pattern_len_9)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_10 > 0:
        print("     - [length = 10] | "+progression_len_10 + " [ "+str(pattern_len_10)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_11 > 0:
        print("     - [length = 11] | "+progression_len_11 + " [ "+str(pattern_len_11)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_12 > 0:
        print("     - [length = 12] | "+progression_len_12 + " [ "+str(pattern_len_12)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_13 > 0:
        print("     - [length = 13] | "+progression_len_13 + " [ "+str(pattern_len_13)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_14 > 0:
        print("     - [length = 14] | "+progression_len_14 + " [ "+str(pattern_len_14)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_15 > 0:
        print("     - [length = 15] | "+progression_len_15 + " [ "+str(pattern_len_15)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_16 > 0:
        print("     - [length = 16] | "+progression_len_16 + " [ "+str(pattern_len_16)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_17 > 0:
        print("     - [length = 17] | "+progression_len_17 + " [ "+str(pattern_len_17)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_18 > 0:
        print("     - [length = 18] | "+progression_len_18 + " [ "+str(pattern_len_18)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_19 > 0:
        print("     - [length = 19] | "+progression_len_19 + " [ "+str(pattern_len_19)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    if pattern_len_20 > 0:
        print("     - [length => 20] | "+progression_len_20 + " [ "+str(pattern_len_20)+" / "+str(estimated_quantity_per_pattern_for_library_completed)+" ]")
    return memory

def list_genomes_on_database():
    print("[LIST] [REPORTING] [DNA SECUENCES] ... -> [STARTING!]\n")
    print("-"*15 + "\n")
    f=open(genomes_list_path, 'w')
    for k, v in genomes.items():
        print ("*"+str(k)+ "-> [ "+str(len(v))+" bp linear RNA ]")
        print ("  + [A] Adenine  :", str(v.count("A")))
        print ("  + [G] Guanine  :", str(v.count("G")))
        print ("  + [C] Cytosine :", str(v.count("C")))
        print ("  + [T] Thymine  :", str(v.count("T")))
        f.write(str("*"+ str(k)+ " -> [ "+str(len(v))+"bp linear RNA ]\n"))
        f.write(str("  + [A] Adenine  : " + str(v.count("A"))+"\n"))
        f.write(str("  + [G] Guanine  : " + str(v.count("G"))+"\n"))
        f.write(str("  + [C] Cytosine : " + str(v.count("C"))+"\n"))
        f.write(str("  + [T] Thymine  : " + str(v.count("T"))+"\n"))
        if v.count("N") > 0:
            print ("  + [N]  *ANY*   :", str(v.count("N")))
            f.write(str("  + [N]  *ANY*   : "+ str(v.count("N"))+"\n"))
        print ("")
        f.write("\n")
    print("-"*15 + "\n")
    print ("[LIST] [INFO] [SAVED!] at: '"+str(genomes_list_path)+"'... -> [EXITING!]\n")
    f.close()

def examine_stored_brain_memory():
    memory = [] # list used as hot-memory
    f=open(brain_path, 'r')
    for line in f.readlines():
        if line not in memory:
            memory.append(line)
    f.close()
    if memory == "": # first time run!
        print ("[LIBRE-AI] [INFO] Not any [BRAIN] present ... -> [BUILDING ONE!]\n")
        print("-"*15 + "\n")
        for i in range(2, 11+1):
            seed = [random.randrange(0, 4) for _ in range(i)] # generate "static" genesis seed
            if seed not in seeds_checked:
                seeds_checked.append(seed)
                pattern = ""
                for n in seed:
                    if n == 0:
                        pattern += "A"
                    elif n == 1:
                        pattern += "C"
                    elif n == 2:
                        pattern += "T"
                    else:
                        pattern += "G"
                print("[LIBRE-AI] [SEARCH] Generating [RANDOM] pattern: " + str(pattern) + "\n")
                create_new_pattern(pattern) # create new pattern
        print("-"*15 + "\n")
        print ("[LIBRE-AI] [INFO] A new [BRAIN] has been created !!! ... -> [ADVANCING!]\n")
        f=open(brain_path, 'r')
        memory = f.read().replace('\n',' ')
        f.close()
    return memory

def print_banner():
    print("\n"+"="*50)
    print(" ____  _       _   _    _     ")
    print("|  _ \(_) __ _| \ | |  / \    ")
    print("| | | | |/ _` |  \| | / _ \   ")
    print("| |_| | | (_| | |\  |/ ___ \  ")
    print("|____/|_|\__,_|_| \_/_/   \_\ by psy")
    print('\n"Search and Recognize patterns in DNA sequences"')
    print("\n"+"="*50)
    print("+ GENOMES DETECTED:", str(num_files))
    print("="*50)
    print("\n"+"-"*15+"\n")
    print(" * VERSION: ")
    print("   + "+VERSION+" - (rev:"+RELEASE+")")
    print("\n * SOURCES:")
    print("   + "+SOURCE1)
    print("   + "+SOURCE2)
    print("\n * CONTACT: ")
    print("   + "+CONTACT+"\n")
    print("-"*15+"\n")
    print("="*50)

# sub_init #
num_files=0
for file in glob.iglob(genomes_path + '**/*', recursive=True):
    if(file.endswith(".genome")): 
        num_files = num_files + 1
        f=open(file, 'r')  
        genome =  f.read().replace('\n',' ')
        genomes[file.replace("datasets/","")] = genome.upper() # add genome to main dict
        f.close()
print_banner() # show banner
option = input("\n+ CHOOSE: (S)earch, (L)ist, (T)rain or (R)eport: ").upper()
print("")
print("="*50+"\n")
if option == "S": # search pattern
    search_pattern_with_human()
elif option == "L": # list genomes
    list_genomes_on_database()
elif option == "T": # teach AI
    teach_ai()
else: # libre AI
    libre_ai()
print ("="*50+"\n")
