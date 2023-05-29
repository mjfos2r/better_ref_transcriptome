#!/bin/bash
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 72:00:00
#SBATCH -p checkpt
#SBATCH -A loni_pgtrain3
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#job starts here
date 
echo "Job started!"
echo " "
echo "loading modules"
echo " "
module list
echo " "
echo "currently in: $PWD"
echo "moving to /work/mjfos2r/denovo/trinity/trinity_rRNA_culled/clustering"
cd /work/mjfos2r/denovo/trinity/trinity_rRNA_culled/clustering
echo " "
echo "currently in: $PWD"
echo " "
echo "running vsearch to cluster transcripts"
vsearch --threads 48 --log LOGFile \
--cluster_fast ../codingregions/Trinity.fasta.transdecoder.cds \
--id 0.90 \
--centroids centroids.fasta \
--uc clusters.uc
echo "clustering done!"
echo " "
echo "Job Done!"
date
exit 0
