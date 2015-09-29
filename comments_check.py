#A script to check the comments for students in ECE220

#input: code file pointer

from collections import Counter
from re import split
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("StudentCodeDir", help="The student code's root directory should be .../studentCode")
# args = parser.parse_args()
# root_dir = args.StudentCodeDir
#
# print(root_)

BANNER = "-" * 35
dic = {'of':12.85, 'to':26.64, 'in':13.02}
def format_print(counter, is_reverse=False):
    lst = counter.items()
    fd = open("commentdata.txt", 'w')
    sorted(lst, key=lambda t: t[1])
    print ("[Unique Words: %d]" % len(lst), file=fd)
    print ("%-16s | %16s" % ("Word", "Count"), file = fd)
    print (BANNER, file = fd)
    for word, count in lst:
        print ("%-16s | %16d" % (word, count), file = fd)
    fd.close

def count_words(filename, counter):
    with open(filename, "rU") as f:
        for line in f:
            line = line.strip().lower()
            if not line:
                continue
            counter.update(x for x in split("[^a-zA-Z']+", line) if x)
    return counter

def count_word(f, counter, freqlist):
    for line in f:
        line = line.strip().lower()
        if not line:
            continue
        counter.update(x for x in split("[^a-zA-Z']+", line) if x in freqlist and x != ' ')
    return counter

def count_word_in_new_counter(f, freqlist):
    counter = Counter()
    for line in f:
        line = line.strip().lower()
        if not line:
            continue
        counter.update(x for x in split("[^a-zA-Z']+", line) if x)
    for word in freqlist:
        if word in counter:
            if counter[word] > dic[word]*0.3:
                continue
            else:
                return 1
        else:
            return 0
    return 4

def style_point(studentfile, freqlist):
    return 4 if count_word_in_new_counter(studentfile, freqlist) else 0

def main():
# here starts the main

#use a list of word as words to inspect
    freqfp = open("frequentlist.txt", 'r')
    freqli = freqfp.read().splitlines()
    student_comment_statusfd = open("student_comment_status.txt", "w")



# open the student list and initialize the counter
    fd = open("students.txt", 'r')
    id_list = fd.read().splitlines()
    fd.close
    counter = Counter()

# error student
    err_fd = open('error_student.txt', 'w')

#prompt for input
    start_id = input("Enter start student ID: ")
    end_id = input("Enter end student ID: ")

#get the list of student into a buffer
    curr_id = id_list[0]
    index = 0
    while curr_id != start_id:
        index += 1
        curr_id = id_list[index]

#check the mpfile of the student

    while curr_id != end_id:
        try:
            curr_id = id_list[index]
        except Exception as e:
            print(index)

        script_dir = os.path.dirname(__file__)
        mp_path = curr_id + "/mp1.asm"
        mp_path = os.path.join(script_dir, mp_path)
        try:
            mp_fp = open(mp_path,'r')
            #count_word(mp_fp, counter, freqli)
            print(curr_id + '   ' + str(count_word_in_new_counter(mp_fp, freqli)) , file = student_comment_statusfd)

            mp_fp.close
        except IOError as err:
            print(curr_id, file = err_fd)
            index += 1
            continue

        index += 1

    format_print(counter, is_reverse=False)

#format_print(count_words("test.txt"), is_reverse=False)

if __name__ == '__main__':
    main()
