import subprocess
import pandas
import glob

# set path to output directory 'metadata/'
path2output='/ddnA/work/mjfos2r/big_transcriptome_attempt/metadata/'
# set samples
## Open file of accession numbers, originally hendrickson_foster_RNASeq_NCBI.txt :)
accessions_file = open('/ddnA/work/mjfos2r/big_transcriptome_attempt/textfiles/target_sorted.txt', 'r')
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

# init empty dataframe for the following loop
metaDataFrame = pandas.DataFrame()

for sra_id in sra_numbers:
		print("")
		print("getting experiment metainfo for the following SRA file: " + sra_id)
		print("")
	# set command based on path to sra file downloaded with prefetch, translate to tsv
		getMeta = "esearch -db sra -query " + sra_id + " | efetch -format runinfo | tr \',\' \'\\t\' < /dev/stdin"
		print('command executed: ' + getMeta)
	# set var to intake the translated tsv, call a shell subprocess and run the above command, capture the output as text and store in outMD
		outputMetaData = subprocess.run(getMeta, shell=True, capture_output=True, text=True)
		print("stdout below:")
	# print out the stdout which should be our translated TSV file :)
		print(outputMetaData.stdout)
	# lets make the filename dep on iteration for this metadata:)
		tsv_out = path2output + sra_id + "_metadata.tsv"
	# open the above file for writing
		with open(tsv_out, 'w') as tsv:
	# write the tsv file:)
				tsv.write(outputMetaData.stdout)

# okay now that we have all of our tsv files written, lets pull em back in with glob
metadata_files = glob.glob('*.tsv')
print(metadata_files)

# setting two empty dataframes for the below loop
metaDF = pandas.DataFrame()
tempDF = pandas.DataFrame()

# I could have done this in R so much easier. I am determined to use the python i just learned though.
for tsv in metadata_files:
	# read in the tsv file, set to temp
		tempDF = pandas.read_csv(tsv, sep='\t')
	# add it to the big dataframe for later use
		metaDF = pandas.concat([metaDF, tempDF], ignore_index=True)

# lets look at the library paired-ness of all the stuff we downloaded
print(metaDF[['Run', 'LibraryLayout']])
# lets write all of the metadata to a tsv file for later use
pandas.DataFrame(metaDF).to_csv(path2output + 'allMetadata.tsv', sep='\t')
# and lets write the paired-ness for use in formatting fixing, (i don't expect to but i know it's inevitable)
pandas.DataFrame(metaDF[['Run', 'LibraryLayout']]).to_csv(path2output + 'all_libtype.tsv', sep='\t')
