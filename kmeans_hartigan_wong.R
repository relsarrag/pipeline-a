library(cluster)

args <- commandArgs(trailingOnly=TRUE)
argData <- args[1] #Square A3
argCenters <- args[2] #25
argIter <- args[3]
argNstart <- args[4]
outFile <- args[5]
numTimes <- args[6]

outFile <- paste(strsplit(outFile, "\\.")[0], strsplit(argData, "\\.")[0])
outFile <- paste(outFile, ".dat")

#Chosen final clusters
centers_1 <- strtoi(argCenters) - 1
final_clusters = vector(mode="list", length=centers_1)

#Reads the file into a matix
file <- read.csv(argData, sep=",", header=F)
rowNo<-dim(file)
row.names(file)<-file[,1]
file<-file[,2:rowNo[2]]
matrix <- as.matrix(file)

#Find best clusteing solution for every number of centers
for (k in 2:argCenters) {
	#Storage for intermediate clustering attempts
	cluster_attempts_sil = vector(mode="list", length=numTimes)	
	cluster_attempts_vec = vector(mode="list", length=numTimes)	
	seeds = vector(mode="list", length=numTimes)
	
	#Attemts clustering n~(numTimes) times, resetting the seed each time, and finds the silhouette index
	for (i in 1:numTimes) {
		rand_seed <- runif(1, 100, 100000000)
		set.seed(rand_seed)
		clustering <- kmeans(matrix, centers=k, iter.max=argIter, nstart=argNstart, algorithm=c("Hartigan-Wong"))
		clusters <- clustering$cluster
		sil.index <- silhouette(clusters, dist(matrix))
		sil_index_summary <- summary(sil.index, FUN=mean)
		sil_coeff <- sil_index_summary$avg.width
		cluster_attempts_sil[i] <- sil_coeff
		clustering_list = list(clusters)
		cluster_attempts_vec[i] <- clustering_list
		seeds[i] <- rand_seed
		}
		
	#Find best Cluster for given center among the attempted clustering solutions for the current center
	curr_best = 1
	current_comparison = -2
	for(n in 1:length(cluster_attempts_sil)){
		if(cluster_attempts_sil[[n]] > current_comparison){
			current_comparison <- cluster_attempts_sil[n]
			current_best <- n
		}
	}
	
	#Saves the best clustering attempt to vector
	best_sil <- cluster_attempts_sil[[curr_best]]
	best_vec <- cluster_attempts_vec[[curr_best]]
	best_seed <- seeds[[curr_best]]
	final_clusters[[k-1]] <- list(cluster=k, silhouette=best_sil, clusters=best_vec, seed=best_seed)
	
	#Prints the final results for each number of clusters
	#print("Current Center:")
	#print(k)
	#print("Best Sil:")
	#print(best_sil)
	#print("Best Vec:")
	#print(best_vec)
	#print("Used Seed:")
	#print(best_seed)
	#print("          ")
}
#Write final clustering solutions (one for each attempted center) to a file
save(final_clusters, file=outFile)
