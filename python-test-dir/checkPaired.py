import os
import subprocess
import gzip

#######         
# SET GLOBAL VARIABLES HERE
##              
# set path to reads here! 
path = "/ddnA/work/mjfos2r/big_transcriptome_attempt/fastq"

# This is what trinity says to use. Its like 300 files though and idk which are paired and which are single....

#separateInterleaved = 'gunzip -c ' + interleaved_file + ' | paste - - - - - - - - | tee >(cut -f 1-4 | tr '\t' '\n' | gzip > ' + read1_outfile') | cut -f 5-8 | tr '\t' '\n' | gzip -c > '+ read2_outfile')'

def getFiles(path):
  #ok lets try to get a list of files present at path
    try:
        file_list = os.listdir(path) #okay so create file_list based on the files present at path
        print("files present in '" + path + "' :")
        print(file_list) # print out the files present
        return(file_list)
    except NameError: # raise exception if path is not defined.
        print("path variable is not set! please tell me where to look for fastq files and try again!!")
    except os.error: # raise exception if there's an error with the above os.listdir command.
        raise Exception("Error building file list from the given path. Make sure the path is formatted correctly!")

def checkPairing(file_list):
    single_files_list = open('single_files_list.txt', 'w')
    paired_files_list = open('paired_files_list.txt', 'w')

    print("number of files present: ", len(file_list))

    for sra in file_list: #start looping through sras in file_list
        if sra.endswith(".fastq.gz"):
            numLines = 'fastq-dump -X 1 -Z --split-spot ' + sra + '| wc -l'
            print('command executed: ' + numLines)
            lines = subprocess.check_output(numLines, shell=True)
    # get number of lines and use to check if paired or not``
            if lines == 4:
                print(sra + ' is single end')
                print("No separation required!")
                single_file = sra
                single_files_list.writelines(single_file)
                return(single_file)
            else:
                print(sra + ' is paired end')
                paired_file = sra
                paired_files_list.writelines(paired_file)
                return(paired_file)
    print("files before check: ", len(file_list))
    print("single files saved to: ", single_files_list)
    print("paired files saved to: ", paired_files_list)
    print("number of single files: ", len(single_files_list))
    print("number of paired files: ", len(paired_files_list))

    if (len(single_files_list) + len(paired_files_list) == len(file_list)):
        print("all is good, single files + paired files is equal to list of all files")
    else:
        print("something went wrong, single files + paired files !== all files")
        return(1)

def sepPaired(paired_file):
    read1_outfile = gzip.open(os.path.splitext(basename(paired_file))[0] + '_1.fastq.gz', 'wb')
    read2_outfile = gzip.open(os.path.splitext(basename(paired_file))[0] + '_2.fastq.gz', 'wb')

    #get all lines from the paired file, then save to seqlines.
    seqlines = paired_file.readlines()
    #init two empty lists for read1 and read2
    read1_lines = []
    read2_lines = []
    # set iterator to 0 
    i = 0

    while gzip.open(paired_file, 'wb'):
        for lines in seqlines:
            for i in range(0, len(seqlines), 8):
                read1_lines = seqlines[i:i+4]
                read2_lines = seqlines[i+4:i+8]
                read1_outfile.writelines(read1_lines)
                read2_outfile.writelines(read2_lines)