fileName = '.../Consumer_Complaints.csv'
#x = read.table(fileName,sep=',',header=TRUE)
f = file(fileName,open="r")
names = readLines(f,n=1)
names = strsplit(names,',')
#print(names)
productVector = as.character()
countVector = as.numeric()
trVector = as.numeric()
block <- readLines(f,n=10)
lst = strsplit(block[1],',')
#print(lst)
#print(lst[[1]][2])
counter = 0
while(length(block<-readLines(f,n=1000)) > 0){
	counter = counter + 1
	print(c(counter,length(block)))
	for(i in 1:length(block)){
		lst = strsplit(block[i],',')
		product = lst[[1]][2]
		tr = lst[[1]][16] == 'Yes'
		#print(c(i,product))
		if(product %in% productVector == FALSE){
			productVector = c(productVector,product)
			countVector = c(countVector,1)
			trVector = c(tr,trVector)
		}else{
			w = which(productVector==product)
			countVector[w] = countVector[w] + 1
			trVector[w] = trVector[w] + tr
		}
	}
}
close(f)

index = order(countVector)
productVector = productVector[index]
countVector = countVector[index]
trVector = trVector[index]


df = data.frame(productVector,countVector,round(countVector/sum(countVector),2),round(trVector/countVector,3))
print(df)