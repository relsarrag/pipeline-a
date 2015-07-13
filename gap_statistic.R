suppressMessages(library(clusterSim))

args <- commandArgs(trailingOnly=TRUE)
argData <- args[1]
argClustering <- args[2]
argCenters <- args[3]
argB <- args[4]
outFile <- args[5]

file <- invisible(read.csv(argData, sep=",", header=F))
clustering_data <- load(argClustering)
rowNo<-dim(file)
row.names(file) <- file[,1]
file<-file[,2:rowNo[2]]
matrix <- as.matrix(file)
best <- 0

counter1 <- 1
counter2 <- 2
for(k in 1:length(final_clusters)){
	clall <- cbind(final_clusters[[counter1]]$clusters, final_clusters[[counter2]]$clusters)
	gapIndexOutput <- index.Gap(matrix, clall, method="pam")
	if(gapIndexOutput$gap > 0){
		best <- k
		break
	}
	if(counter2 < length(final_clusters)){
		counter1 <- counter1 + 1
		counter2 <- counter2 + 1
	}
	#print("k:")
	#print(k)
	#print("c1:")
	#print(counter1)
	#print("c2:")
	#print(counter2)
	#print("          ")
}

#Write best to file
invisible(lapply(final_clusters[[best]], write, outFile, append=TRUE, ncolumns=length(final_clusters[[best]]$clusters)))