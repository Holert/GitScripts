#!/usr/bin/env Rscript 
# Created by: Lee Bergstrand 
# Descript: Converts BLAST TotalBLASTResultss from BackBlast into a heatmap.  
#             
# Requirements: - reshape2 and RColorBrewer modules
#----------------------------------------------------------------------------------------
library(reshape2)
library(RColorBrewer)
library(ape)
library(gplots)

# Sets the working directory. 
setwd("/Users/Jojo/Dropbox/Jojo/Postdoc/Metagenomics/Global_metagenomes_datasets/Binning/MyCC/Best_reciprocal_BLAST/RHA1")

# Gets a list files from the working directory.
fileList = list.files(path = getwd(), all.files = FALSE, pattern = "\\.out$") 

TotalBLASTResults = matrix(data = 0, nrow = 0, ncol = 7)

fileCounter = 1
while (fileCounter <= length(fileList)){
  BackBLASTResults = read.csv(fileList[fileCounter], header = FALSE, stringsAsFactors = TRUE) # Inport data from csv file from BackBLAST.py
  SubjectAccession = sub(".fast.csv.out$", "", fileList[fileCounter]) # Remove .csv suffix from csv filename. This should be the subject organism accession.
  SubjectAccessionColumn = matrix(data = SubjectAccession, nrow = nrow(BackBLASTResults), ncol = 1) # Makes a column that contains only the organism accession as data.
  BackBLASTResults  = cbind(BackBLASTResults, SubjectAccessionColumn) # Concatenates SubjectAccessionColumn to the BackBLAST results.
  BackBLASTResults[[2]] = as.character(BackBLASTResults[[2]]) # Some SubjectSeqIDs in BackBLAST results are purly numeric (example from JGI id numbers). 
  # This throws a warning when you attempt to append this numeric column in BackBLASTResults 
  # to a character column in TotalBLASTResults. The code left typecasts this coloumn to character.
  TotalBLASTResults = rbind(TotalBLASTResults, BackBLASTResults) # Concatenates the current csv files BLAST results to the total BLAST results.
  fileCounter = fileCounter + 1
}
colnames(TotalBLASTResults) = c("QuerySeqID", "SubjectSeqID", "PercentIdent", "Evalue", "QueryCoverage", "Bitscore", "TargetOrganism")

#check this function help to see what to do when multiple values occur
HeatmapMatrix = acast(TotalBLASTResults, QuerySeqID ~ TargetOrganism, value.var = "PercentIdent") # Converts TotalBLASTResults to wide format data matrix.
HeatmapMatrix[is.na(HeatmapMatrix)] = 0 # Replaces NA values with zero for heatmap function.
#colnames(HeatmapMatrix)
# Heatmapmatrix2 = HeatmapMatrix[, sort]
HeatmapMatrix = HeatmapMatrix[order(rownames(HeatmapMatrix)),] # Reorders rows by gene name.
 # Reorders rows by gene name

# test trees

# setwd("/Users/Jojo/Desktop/")

fulltree <- read.tree("/Users/Jojo/Dropbox/Jojo/Postdoc/Metagenomics/Global_metagenomes_datasets/Binning/MyCC/Best_reciprocal_BLAST/concatenated.tre")

pruned.tree<-drop.tip(fulltree, setdiff(fulltree$tip.label, colnames(HeatmapMatrix)))
# plot(pruned.tree)

# The Tree needs to be rooted so get the user to interactivly pick a root.
print("Please select a root.")
plot(pruned.tree, direction="downwards")
tree = root(pruned.tree, resolve.root = TRUE, interactive = TRUE)
#tree = root(pruned.tree, "imgm_2162886008.4")
print("Thanks, continuing...")

# The tree must be ultrametric to be able to be passed to hclust.
tree$edge.length[which(tree$edge.length == 0)] = 0.00001
tree <- chronopl(tree, lambda = 0.1, tol = 0)

dendrogram = as.dendrogram(as.hclust.phylo(tree))

cladeOrder = order.dendrogram(dendrogram)
cladeName =  labels(dendrogram)

# Rearanges matrix to match tip ordering of the dendrogram.
cladePosition = data.frame(cladeName, cladeOrder)
cladePosition = cladePosition[order(cladePosition$cladeOrder),]
newOrder = match(cladePosition$cladeName, colnames(HeatmapMatrix))
OrderedHeatmapMatrix = HeatmapMatrix[,newOrder]

OrderedHeatmapMatrix = OrderedHeatmapMatrix[order(rownames(OrderedHeatmapMatrix)), ] # Reorders rows by gene name.

ColourPal = brewer.pal(9,"YlGn") # Gets Colour Palete from R colour brewer.
ColourPal[1] = "#F4F5F6" # Swaps lowest colour for off white.
ColourPal = append(ColourPal, "#00311d")
heatmap.2(OrderedHeatmapMatrix, Rowv = NA, Colv = dendrogram, dendrogram = "column", col = ColourPal, 
          trace="none", xlab = "", ylab = "", margins = c(10,9))

#--------
# sorting columns

# by taxonomy

sort = c("0_Chol1_Empty.out",
         "imgm_2140918001.5",
         "imgm_2015219000.6",
         "img_3300000400_porifera.4",
         "img_3300002150_porifera.1",
         "img_3300002150_porifera.18",
         "img_3300002150_porifera.7",
         "img_3300002151_porifera.5",
         "img_3300002159_porifera.13",
         "img_3300002159_porifera.2",
         "img_3300002159_porifera.5",
         "img_3300002160_porifera.26",
         "img_3300002160_porifera.3",
         "img_3300002160_porifera.36",
         "img_3300002160_porifera.7",
         "img_3300002222_porifera.1",
         "img_3300002222_porifera.25",
         "img_3300002222_porifera.4",
         "imgm_3300000323.7",
         "imgm_3300000756.1",
         "imgm_3300001060.5",
         "imgm_3300001068.10",
         "imgm_3300001077_solid_waste.19",
         "imgm_3300001112.3",
         "imgm_3300001123.1",
         "imgm_3300001356.87",
         "imgm_3300001380.124",
         "imgm_3300001380.16",
         "imgm_3300001676.26",
         "imgm_3300001676.32",
         "imgm_3300001678.54",
         "imgm_3300001679.66",
         "imgm_3300001680.14",
         "imgm_3300001750.33",
         "imgm_3300002147_porifera.11",
         "imgm_3300002178.25",
         "imgm_3300002180.3",
         "imgm_3300002225.1",
         "imgm_3300002522.3",
         "imgm_3300002535.4",
         "imgm_3300002913.9",
         "imgm_3300002919.20",
         "imgm_3300002966.296",
         "imgm_3300002966.98",
         "CXWK01.1.49",
         "CXWK01.1.73",
         "img_3300002150_porifera.24",
         "img_3300002150_porifera.4",
         "img_3300002151_porifera.15",
         "img_3300002151_porifera.24",
         "img_3300002159_porifera.16",
         "img_3300002159_porifera.28",
         "img_3300002160_porifera.15",
         "img_3300002160_porifera.19",
         "img_3300002160_porifera.2",
         "img_3300002160_porifera.30",
         "imgm_3300001356.53",
         "imgm_3300002147_porifera.27",
         "imgm_3300002919.10",
         "imgm_3300002919.15",
         "mgm4455295.3.19",
         "imgm_3300002184.60",
         "imgm_3300002917.29",
         "CXWK01.1.13",
         "hydro_H1C.8",
         "imgm_3300001471.1",
         "imgm_3300001471.9",
         "imgm_3300001977_plants.15",
         "imgm_3300002966.210",
         "imgm_3300002966.29",
         "imgm_3300000971.5",
         "imgm_3300000975.1",
         "imgm_3300001006.10",
         "imgm_3300001051.5",
         "imgm_3300001105.14",
         "imgm_3300001114.2",
         "imgm_3300001115.1",
         "imgm_3300002522.1",
         "imgm_3300002535.1",
         "imgm_3300002772.11",
         "imgm_3300002773.5",
         "CXWJ01.1.1",
         "imgm_3300001105.16",
         "hydro_PW_MHGC_2012April2.2",
         "imgm_3300001990.14",
         "71117_WorMetLIZAISLAND_2.11",
         "71117_WorMetLIZAISLAND_2.2",
         "A27048-scaffolds.2",
         "hydro_H1C.4",
         "img_3300002150_porifera.11",
         "img_3300002150_porifera.13",
         "img_3300002151_porifera.2",
         "img_3300002151_porifera.26",
         "img_3300002151_porifera.33",
         "img_3300002151_porifera.37",
         "img_3300002159_porifera.3",
         "img_3300002159_porifera.7",
         "img_3300002160_porifera.34",
         "img_3300002222_porifera.21",
         "imgm_3300000226.9",
         "imgm_3300000239.9",
         "imgm_3300001354.23",
         "imgm_3300001356.79",
         "imgm_3300001678.37",
         "imgm_3300001678.60",
         "imgm_3300001680.15",
         "imgm_3300002147_porifera.1",
         "imgm_3300002178.5",
         "imgm_3300002913.32",
         "imgm_3300002919.34",
         "55016_WorMetmaBAHAMAS1.2",
         "55017_WorMetmaBAHAMAS2.1",
         "55047_WorMetfiPIANOSA2.1",
         "58706_WorMetexBAHAMAS1.1",
         "58706_WorMetexBAHAMAS1.6",
         "59454_WorMetilPIANOSA1.1",
         "60020_WorMetilPIANOSA2.5",
         "61187_WorMetilPIANOSA1.5",
         "67351_WorMetGr2BELIZE1.3",
         "67351_WorMetGr2BELIZE1.4",
         "71115_WorMetGr2BELIZE2.1",
         "71117_WorMetLIZAISLAND_2.1",
         "71117_WorMetLIZAISLAND_2.7",
         "img_3300002150_porifera.22",
         "img_3300002150_porifera.26",
         "img_3300002150_porifera.5",
         "img_3300002151_porifera.19",
         "img_3300002151_porifera.38",
         "img_3300002159_porifera.1",
         "img_3300002159_porifera.15",
         "img_3300002159_porifera.22",
         "img_3300002160_porifera.10",
         "img_3300002160_porifera.31",
         "img_3300002160_porifera.38",
         "img_3300002222_porifera.10",
         "img_3300002222_porifera.11",
         "img_3300002222_porifera.9",
         "imgm_2199352012_solid_waste.40",
         "imgm_3300001356.91",
         "imgm_3300001380.109",
         "imgm_3300001380.94",
         "imgm_3300001676.12",
         "imgm_3300001750.48",
         "imgm_3300002147_porifera.21",
         "imgm_3300002180.9",
         "imgm_3300002184.16",
         "imgm_3300002917.36",
         "imgm_3300002966.12",
         "JRYH01.1.26",
         "AERA01.1.7",
         "CXWK01.1.32",
         "imgm_3300001471.16",
         "imgm_3300001977_plants.7",
         "imgm_3300002184.20",
         "imgm_3300002239_plants.19",
         "CXWJ01.1.4",
         "imgm_3300002158.5",
         "imgm_3300001305.9",
         "imgm_3300001545.15",
         "imgm_3300002184.6",
         "imgm_3300002756.27",
         "imgm_3300002158.6",
         "imgm_3300001354.59",
         "imgm_3300002756.3",
         "A27048-scaffolds.68",
         "imgm_3300001749.1",
         "imgm_3300002154.20",
         "imgm_3300002225.35",
         "imgm_3300002756.15",
         "hydro_PW_MHGC_2012April2.49",
         "imgm_3300000975.4",
         "imgm_3300002180.33",
         "imgm_3300002756.25",
         "imgm_3300001123.6",
         "imgm_2048955003_solid_waste.4",
         "imgm_3300002756.2",
         "imgm_3300002184.12",
         "imgm_3300002225.8",
         "imgm_3300001749.56",
         "imgm_3300001749.57",
         "APMI01.1.48",
         "APMI01.1.53",
         "imgm_3300001904.30",
         "imgm_3300001990.28",
         "imgm_3300002067.72",
         "imgm_3300002239_plants.16",
         "CXWK01.1.46",
         "hydro_SyncrudeMLSB2011.97",
         "imgm_3300001354.65",
         "imgm_3300002184.39",
         "JRYH01.1.17",
         "JRYJ01.1.7",
         "imgm_2199352012_solid_waste.16",
         "hydro_PW_MHGC_2012April2.62",
         "imgm_2199352012_solid_waste.2",
         "JTFN01.1.3",
         "JTFO01.1.11",
         "imgm_3300002067.101",
         "hydro_TP62008_30ft.5",
         "JRYL01.1.13",
         "imgm_3300002158.1",
         "imgm_3300002158.2",
         "imgm_3300001130.4",
         "hydro_CO182.3",
         "JRYI01.1.32",
         "A27040-scaffolds.4",
         "imgm_3300001354.12",
         "imgm_3300002919.6",
         "imgm_3300001679.6",
         "imgm_3300000226.47",
         "imgm_3300000239.43",
         "JRYF01.1.4",
         "CEGE01.1.2",
         "imgm_3300002225.34",
         "CEGC01.1.2",
         "CEGE01.1.18",
         "hydro_CO183.9",
         "imgm_3300002772.9",
         "JTFP01.1.6",
         "20091_OlaalgELextract2_2.11",
         "55031_WorMetTyACAVOLI1.1",
         "imgm_2199352012_solid_waste.3",
         "imgm_3300002966.13",
         "imgm_2209111003_solid_waste.5",
         "imgm_2162886008.4")

#---------------
# setdiff(sort, colnames(HeatmapMatrix))
# class(sort)

#ColourPal = brewer.pal(9,"YlGn") # Gets Colour Palete from R colour brewer.
#ColourPal[1] = "#F4F5F6" # Swaps lowest colour for off white.
#ColourPal = append(ColourPal, "#00311d")
#heatmap.2(HeatmapMatrix2, Rowv=FALSE, Colv=FALSE, col = ColourPal, 
#          trace="none", xlab = "", ylab = "", margins = c(4,25), breaks=c(0,10,20,30,40,50,60,70,80,90,100))
