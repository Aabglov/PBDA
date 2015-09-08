Data = read.table('employerMoney.txt',sep=',',as.is=TRUE)
colnames(Data) = c('Company','Rep','Dem','Other','Total')
head(Data)
print(Data[,1])
s = c(176,128,115,143,114,75,158,65,70,47,12,153,149,100,83,52,42,126,50,189)
D = Data[s,]
D = D[order(D$Rep+D$Dem),]
rep = D$Rep/10^5
dem = D$Dem/10^5
mx = max(rep+dem)
names=D[,1]
n = length(rep)
par(mar=c(5,12,4,2) + .1,oma=c(0,1,0,0))
plot(x=c(0,mx),y=c(1,n),yaxt='n',xlab="Dollars - 100,000's",cex.axis=.65,typ='n', ylab='',cex.lab=.8)
axis(side=2,at=seq(1,n),labels=names, las=2,cex.axis=.65)
plot(x = c(0,max(rep+dem)),y=c(1,n),yaxt='n',xlab="Dollars - 100,000's",cex.axis=.65,typ='n',ylab='',cex.lab=.8)
axis(side=2,at=seq(1,n),labels=names,las=2,cex.axis=.65)
for(i in 1:n){
lines(y=c(i,i),x=c(0,rep[i]),col='red',lwd=3)
lines(y=c(i,i),x=c(rep[i],rep[i]+dem[i]),col='blue',lwd=3)
}