import subprocess

# set samples
## Open file of accession numberes
accessions_file = open('/ddnA/work/mjfos2r/big_transcriptome_attempt/hendrickson_foster_RNASeq_NCBI.txt', 'r')
## read in accession ids by line
accessions = accessions_file.read()
## print out each accession id
print(accessions)
## split list by newline 
sra_numbers = accessions.split('\n')
## close file
accessions_file.close()
## print list
print(sra_numbers)

## Okay now we can batch download em! 

for sra_id in sra_numbers:
	print('Downloading : ' + sra_id)
	prefetch = 'prefetch ' + sra_id
	print('command executed was ' + prefetch)
	subprocess.call(prefetch, shell=True)

## okay now to extract the .sra files into a directory called fastq for use by trinity.

for sra_id in sra_numbers:
	print("generating fastq: " + sra_id)
	fastq_dump = "parallel-fastq-dump --outdir /ddnA/mjfos2r/big_transcriptome_attempt/fastq --gzip --skip-technical --readids --read-filter pass --dumpbase --threads 48 --clip /ddna/mjfos2r/sratk-cache/sra/" + sra_id + ".sra"
	print('command executed: ' + fastq_dump)
	subprocess.call(fastq_dump, shell=True)

