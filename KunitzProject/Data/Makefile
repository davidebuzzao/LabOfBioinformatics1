#################################################################
###      Kunitz-type domain Project (Pfam code: PF00014)	  ###
#################################################################

# The Kunitz-type domains are serine protease inhibitors, as family of the largest and most widely distributed superfamily of protease inhibitors (PIs).
# They are stable as standalone peptides, able to recognise specific protein structures, and also work as competitive PIs in their free form. 
# These properties have led to attempt at developing biopharmaceutical drugs in the last years. Building a sequence-profile-based HMM for predicting 
# and discriminating new unstudied Kunitz-type domains has been the main aim of this work. 
# The user needs to care just of the preparation of a csv table of the search results of suitable structures from RCSB PDB, and the summary of a PDBeFold 
# search with a selected template structure (5PTI). Positive and negative datasets are produced starting from gzipped multi-fasta that can be downloaded 
# from the UniProtKB. Also necessary are the PDB seqres txt file and the complete SwissProt database, uncompressed.

SHELL := /bin/bash

## Path definition
SCRIPTS := /Users/davidebuzzao/GitHub/LabOfBioinformatics1/KunitzProject/Scripts/
WD1 := /Users/davidebuzzao/GitHub/LabOfBioinformatics1/KunitzProject/Data/
WD2 := /Users/davidebuzzao/GitHub/LabOfBioinformatics1/KunitzProject/Data/PDB_files/
DB := /Users/davidebuzzao/Bioinformatica_Bologna/Second_semester/LB1/db/

## DataBase section
DB_PDBfasta := $(DB)PDB_seqres.db
DB_UNIPROTfasta := $(DB)uniprot_sprot.fasta

## Scripts section
PDB_FASTA := $(SCRIPTS)get_PDBfasta.py
UNIPROT_FASTA := $(SCRIPTS)get_UNIPROTfasta.py
SORT_CLUST := $(SCRIPTS)sort_cluster.py
PDB_ATOM_CHAIN := $(SCRIPTS)get_ATOM-chain_PDB.py
CONF_MAT := $(SCRIPTS)evalConfusion_matrix.py
HSEARCH_TBLOUT := $(SCRIPTS)clean_hmmsearch_tblout.py
BONF_CORR := $(SCRIPTS)evalBonferroni_correction.py
ROC_CURVE := $(SCRIPTS)evalROC_PRcurves.py
DSSP := $(SCRIPTS)get_DSSP.py 

# User-dependent variables 
COVERAGE := 95
SEQ_ID := 99
THR := 0.000001
TABRES := tabularResults.csv
FLDSUM := PDB_efold5PTI.txt
KUNITZ := PF00014.txt
NON_KUNITZ := NON_PF00014.txt


ROC1 := ROC_PR_CURVES1.plot
ROC2 := ROC_PR_CURVES2.plot

all: ROC_PR_CURVES1.plot

####################################################
###    Performance computation:		 			 ###
###		- Confusion Matrix						 ###
###		- Receiving Operating Characteristic and ###
###		  Precision-Recall Curves				 ###
####################################################

ROC_PR_CURVES1.plot : $(ROC_CURVE) conf_mat.tab
	python3 $^

conf_matTESTset.txt : negative_TESTset_BONF_COR.hmmsearch positive_TESTset_BONF_COR.hmmsearch
	cat <(sort -gk 3 $<) <(sort -gk 3 positive_TESTset_BONF_COR.hmmsearch) > $@

conf_mat.tab : $(CONF_MAT) conf_matCVset.tab
	python3 $^ NO $(THR)

conf_matCVset.txt : $(CONF_MAT) conf_matCVset.tab
	python3 $^ YES > $@

conf_matCVset.tab : negative_CVset_BONF_COR.hmmsearch positive_CVset_BONF_COR.hmmsearch
	cat <(sort -gk 3 $<) <(sort -gk 3 positive_CVset_BONF_COR.hmmsearch) > $@

#########################
### HMMSEARCH section ###
#########################

### Reinclusion of excluded hits from Hmmsearch output.
### Counteracting the problem of multiple comparisons applying the Bonferroni Correction.
negative_TESTset_BONF_COR.hmmsearch : $(BONF_CORR) negative_TESTset.clean.hmmsearch negative_exclTESTset.list negative_TESTset.list
	cat <(python3 $< negative_TESTset.clean.hmmsearch $$(cat negative_TESTset.list | wc -l | bc)) \
	 	<(awk '{print $$0, "1.0 1.0 0"}' negative_exclTESTset.list) > $@

negative_CVset_BONF_COR.hmmsearch : $(BONF_CORR) negative_CVset.clean.hmmsearch negative_exclCVset.list negative_CVset.list
	cat <(python3 $< negative_CVset.clean.hmmsearch $$(cat negative_CVset.list | wc -l | bc)) \
	 	<(awk '{print $$0, "1p.0 1.0 0"}' negative_exclCVset.list) > $@

positive_TESTset_BONF_COR.hmmsearch : $(BONF_CORR) positive_TESTset.clean.hmmsearch positive_exclTESTset.list positive_TESTset.list
	cat <(python3 $< positive_TESTset.clean.hmmsearch $$(cat positive_TESTset.list | wc -l | bc)) \
	 	<(awk '{print $$0, "1.0 1.0 1"}' positive_exclTESTset.list) > $@

positive_CVset_BONF_COR.hmmsearch : $(BONF_CORR) positive_CVset.clean.hmmsearch positive_exclCVset.list positive_CVset.list
	cat <(python3 $< positive_CVset.clean.hmmsearch $$(cat positive_CVset.list | wc -l | bc)) \
	 	<(awk '{print $$0, "1.0 1.0 1"}' positive_exclCVset.list) > $@

### Finding out excluded hits from HMMSEARCH output.
positive_exclCVset.list : positive_CVset.list positive_CVset.clean.hmmsearch
	comm -23 <(sort $<) <(cut -d " " -f 1 positive_CVset.clean.hmmsearch | sort) > $@

positive_exclTESTset.list : positive_TESTset.list positive_TESTset.clean.hmmsearch
	comm -23 <(sort $<) <(cut -d " " -f 1 positive_TESTset.clean.hmmsearch | sort) > $@

negative_exclCVset.list : negative_CVset.list negative_CVset.clean.hmmsearch
	comm -23 <(sort $<) <(cut -d " " -f 1 negative_CVset.clean.hmmsearch | sort) > $@

negative_exclTESTset.list : negative_TESTset.list negative_TESTset.clean.hmmsearch
	comm -23 <(sort $<) <(cut -d " " -f 1 negative_TESTset.clean.hmmsearch | sort) > $@

### Evaluating the Kunitz-type family membership of proteins in the datasets by the using of HMMSEARCH
positive_CVset.clean.hmmsearch : MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).hmm positive_CVset.fasta
	hmmsearch --tblout positive_CVset.hmmsearch --max -E 1000000000 --domE 1000000000 --noali $^ > /dev/null
	python3 $(HSEARCH_TBLOUT) positive_CVset.hmmsearch $@ > /dev/null

positive_TESTset.clean.hmmsearch : MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).hmm positive_TESTset.fasta
	hmmsearch --tblout positive_TESTset.hmmsearch --max -E 1000000000 --domE 1000000000 --noali $^ > /dev/null
	python3 $(HSEARCH_TBLOUT) positive_TESTset.hmmsearch $@ > /dev/null

negative_CVset.clean.hmmsearch : MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).hmm negative_CVset.fasta
	hmmsearch --tblout negative_CVset.hmmsearch --max -E 1000000000 --domE 1000000000 --noali $^ > /dev/null
	python3 $(HSEARCH_TBLOUT) negative_CVset.hmmsearch $@ > /dev/null

negative_TESTset.clean.hmmsearch : MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).hmm negative_TESTset.fasta
	hmmsearch --tblout negative_TESTset.hmmsearch --max -E 1000000000 --domE 1000000000 --noali $^ > /dev/null
	python3 $(HSEARCH_TBLOUT) negative_TESTset.hmmsearch $@ > /dev/null

##############################################
###  		 	2-FOLD CV test		       ###
###  Preparation POSITIVE and NEGATIVE set ###
###     Preparation training and Test set  ###
##############################################

negative_CVset.fasta : $(UNIPROT_FASTA) negative_CVset.list $(DB_UNIPROTfasta)
	python3 $^ $@

negative_TESTset.fasta : $(UNIPROT_FASTA) negative_TESTset.list $(DB_UNIPROTfasta)
	python3 $^ $@

positive_CVset.fasta : $(UNIPROT_FASTA) positive_CVset.list $(DB_UNIPROTfasta)
	python3 $^ $@

positive_TESTset.fasta : $(UNIPROT_FASTA) positive_TESTset.list $(DB_UNIPROTfasta)
	python3 $^ $@

negative_TESTset.list : negative_set.list negative_CVset.list 
	comm -23 <(sort $<) <(sort negative_CVset.list) > $@

negative_CVset.list : negative_set.list 
	sort -R $< | head -$$(echo $$(cat negative_set.list | wc -l) "/2" | bc) > $@

positive_TESTset.list : positive_set.list positive_CVset.list 
	comm -23 <(sort $<) <(sort positive_CVset.list) > $@

positive_CVset.list : positive_set.list 
	sort -R $< | head -$$(echo $$(cat positive_set.list | wc -l) "/2" | bc) > $@

negative_set.list : $(NON_KUNITZ)
	grep -v '^$$' $< | sort -Ru > $@

positive_set.list : remove_blast.list $(KUNITZ) 
	comm -23 <(sort $(KUNITZ)) <(sort $<) > $@


remove_blast.list : PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.blast
	awk '{if ($$3==100) print $$0}' $^| awk -F "|" '{print $$2}' | sort -u > $@

PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.blast : PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.fasta PF00014.fasta
	makeblastdb -in PF00014.fasta -dbtype prot
	blastp -query $< -db PF00014.fasta -out $@ -outfmt 7

PF00014.fasta : $(UNIPROT_FASTA) $(KUNITZ) $(DB_UNIPROTfasta)
	python3 $^ $@

PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.fasta : $(PDB_FASTA) PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list
	python3 $< <(sed 's/:/_/g' PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list) $(DB_PDBfasta) $@

#############################
### 	MUSTANG-3.2.3	  ###
#############################

## Building the HMM starting from a MSA with MUSTANG-3.2.3
MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).hmm : MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).afasta PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list 
	hmmbuild $@ $< > /dev/null

## Preparing the fasta sequences for the MSA to give it as input for MUSTANG-3.2.3. 
## The sequences are representative of clusters coming from a clusterization
## procedure with a given coverage and sequence identity.
MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID).afasta : PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES-MUSTANG.list cleaning_PDB
	mustang-3.2.3 -f $< -F fasta -o MSA_MUSTANG_c$(COVERAGE)_i$(SEQ_ID) -s OFF -r ON

PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES-MUSTANG.list : PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list
	cat <(echo ">$(WD2)") <(awk -F ":" '{print "+"toupper($$1)".cleanpdb"}' $<) > $@

cleaning_PDB : $(PDB_ATOM_CHAIN) PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list $(WD2)%.pdb
	python3 $< PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list $(WD2)
	mv *.cleanpdb $(WD2)

%.pdb : PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list
	cat $< | awk -F ":" '{print toupper($$1)}' | xargs -I '{}' -P 8 -n 1 \
		wget -nv -nc -P PDB_files/ https://files.rcsb.org/download/'{}'.pdb

#####################
###	  PDB-efold   ###
#####################

## Building the HMM starting from a MSA retrieved in fasta format with a remote launched PDBefold MSA
MSA_PDBefold_c$(COVERAGE)_i$(SEQ_ID).hmm : MSA_PDBefold_c$(COVERAGE)_i$(SEQ_ID).fasta PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list 
	hmmbuild $@ $< > /dev/null

## Preparing the fasta sequences for the MSA. The sequences are representative of clusters coming 
## from a clusterization procedure with a given coverage and sequence identity.
PDB_c$(COVERAGE)_i$(SEQ_ID)_BEST_RES.list : PDB_c$(COVERAGE)_i$(SEQ_ID).sorted
	cut -d ' ' -f 2 $^ | cut -d ':' -f 1 | sed 's/_/:/g' > $@

PDB_c$(COVERAGE)_i$(SEQ_ID).sorted: $(SORT_CLUST) PDB_search.list PDB_c$(COVERAGE)_i$(SEQ_ID).clust 
	python3 $^ > $@

PDB_c$(COVERAGE)_i$(SEQ_ID).clust: PDB_common.fasta
	blastclust -i $^ -o $@ -L 0.$(COVERAGE) -S $(SEQ_ID)

PDB_common.fasta: $(PDB_FASTA) PDB_common.list $(DB_PDBfasta)
	python3 $^ $@

PDB_common.list: PDB_search.list PDB_efold5PTI.list
	comm -12 <(cut -f 1 -d " " PDB_search.list) PDB_efold5PTI.list > $@

PDB_search.list: PDB_search.tmp.list
	tail -n +1 $^ | cut -d "," -f 1,2,3 | awk '{print tolower($$1)"_"$$2, $$3}' | sort -k 1 > $@

## BASICS ##

PDB_efold5PTI.list: $(FLDSUM)
	tail -n +6 $^ | awk '{print $$NF}' | sed 's/:/_/g' | sort -k 1 > $@ 

# Pfam Accession Number PF00014
# and Resolution is between 0.0 and 3.0 Å
# and Sequence Length is between 40 and 80
# and Protein Wild Type
PDB_search.tmp.list: $(TABRES)
	sed 's/, NEUTRON DIFFRACTION//g' $^ | cut -d "," -f 1,2,4,6 | sed 's/"//g; s/,/ /g; /^$$/d' | sort -nk 3 | tail -n +3 > $@ 

.PHONY: all clean cleanall

clean:
	rm -f *.list *.sorted *fasta* c[0-9][0-9]_s[0-9][0-9]_* *.rms_rot *.dtout *.blast

cleanall: 
	rm -f *.list *.fasta *.afasta *.clust *.sorted *.hmm *.hmmsearch c[0-9][0-9]_i[0-9][0-9]_* *.rms_rot *.dtout *.tab *.blast
	rm -f PDB_files/*