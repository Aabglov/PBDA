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

model <- knn(train,test,cl=y,k=1,prob=TRUE)

print(summary(model))

cv <- knn.cv(train,cl=y,k=1,prob=TRUE)

print(summary(cv))