library(class)

file <- "/Users/keganrabil/Desktop/PBDA/wis_bc.txt"
x <- read.table(file, header = FALSE, sep = ",")
d <- as.data.frame(x)
x <- data.matrix(d)
# Format output from 4,2 to 1,0
x[,11] <- (x[,11] /2 ) - 1
data <- x[,2:10]


# Split data into training set (80%) and test set (20%)
index <- round(dim(data)[1] * 0.8)
train <- data[1:index,]
y <- x[1:index,11]
test <- data[index:dim(data)[1],] 
test_y <- x[index:dim(data)[1],11] 

for(i in 0:4){
	k = 2^i
	model <- knn(train,test,cl=y,k=k,prob=TRUE)
	cv <- knn.cv(train,cl=y,k=k,prob=TRUE)
	print(paste0("k: ",k))
	#print(summary(cv))
	#print(summary(model))
	pred <- as.numeric(levels(model))[model]
	print(paste0("Error KNN:",sum((pred - test_y)^2)/length(test_y)))
	pred <- as.numeric(levels(cv))[cv]
	print(paste0("Error CV:",sum((pred - y)^2)/length(y)))
	print("")
}

print("The error for the knn model goes down as k increases, but for the cv model the error begins to climb again after k=16, indicating overfitting.  However, the cv model error does go down after k=2, indicating underfitting when k=1 or k=2")