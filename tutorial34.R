library(maps)
fileName = '/Users/keganrabil/Desktop/PBDA/week 13/Data/reducer.output'
D = read.table(fileName,header=FALSE,sep=',')
head(D)
dim(D)
names = c("FIPS","White","Black","Asian","NativeAmer","Hispanic","age","gender","education","income","BMI","diabetes")
length(names)
colnames(D) = names

p = seq(from = .0, by=.1, to=1)
y = D$Hispanic
ints <- quantile(y,p)
ints <- ints[5:length(ints)]
D$colorBuckets = as.numeric(cut(y, ints)   )

colormatched = D$colorBuckets[match(county.fips$fips,D[,1])]
colors = topo.colors(length(ints),alpha=1)
map("county",col=colors[colormatched],fill=TRUE,resolution=0,lty=1)