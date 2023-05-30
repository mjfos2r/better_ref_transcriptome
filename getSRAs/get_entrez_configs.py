import subprocess
import pandas
import glob

# set path to output directory 'metadata/'
path2output='/ddnA/work/mjfos2r/big_transcriptome_attempt/metadata/'
# set samples
accessions_file = open('/ddnA/work/mjfos2r/big_transcriptome_attempt/textfiles/target_sorted.txt', 'r') # Open file of accession numbers, originally hendrickson_foster_RNASeq_NCBI.txt :)
line = accessions_file.readline() # read in accession ids by line
sra_numbers = []
for line in accessions_file:
		line = line.strip() # strip whitespace and EOL that causes malignant behavior
		print(line) # print out each accession id
		sra_numbers.append(line) # append line to sra_numbers
accessions_file.close() # close file

print(sra_numbers) # print list

metaDataFrame = pandas.DataFrame() # init empty dataframe for the following loop

for sra_id in sra_numbers:
		print("")
		print("getting experiment metainfo for the following SRA file: " + sra_id)
		print("")
		getMeta = "esearch -db sra -query " + sra_id + " | efetch -format runinfo | tr \',\' \'\\t\' < /dev/stdin" # set command based on path to sra file downloaded with prefetch, translate to tsv
		print('command executed: ' + getMeta)
		outputMetaData = subprocess.run(getMeta, shell=True, capture_output=True, text=True) # set var to intake the translated tsv, call a shell subprocess and run the above command, capture the output as text and store in outMD
		print("stdout below:")
		print(outputMetaData.stdout) # print out the stdout which should be our translated TSV file :)
		tsv_out = path2output + sra_id + "_metadata.tsv" # lets make the filename dep on iteration for this metadata:)

		with open(tsv_out, 'w') as tsv: # open the above file for writing
				tsv.write(outputMetaData.stdout) # write the tsv file:)

# okay now that we have all of our tsv files written, lets pull em back in with glob
metadata_files = glob.glob(path2output + '*.tsv')
print(metadata_files)

# setting two empty dataframes for the below loop
metaDF = pandas.DataFrame()
tempDF = pandas.DataFrame()

# I could have done this in R so much easier. I am determined to use the python i just learned though.
for tsv in metadata_files:
		tempDF = pandas.read_csv(tsv, sep='\t') # read in the tsv file, set to temp
		metaDF = pandas.concat([metaDF, tempDF], ignore_index=True) # add it to the big dataframe for later use

print(metaDF[['Run', 'LibraryLayout']]) # lets look at the library paired-ness of all the stuff we downloaded
pandas.DataFrame(metaDF).to_csv(path2output + 'allMetadata.tsv', sep='\t') # lets write all of the metadata to a tsv file for later use
pandas.DataFrame(metaDF[['Run', 'LibraryLayout']]).to_csv(path2output + 'all_libtype.tsv', sep='\t') # and lets write the paired-ness for use in formatting fixing, (i don't expect to but i know it's inevitable)

