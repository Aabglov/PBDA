
data <- read.csv('/Users/keganrabil/Desktop/PBDA/week 11/Data/plottingData.csv',header=FALSE)
colnames(data) = c('State','Prevalence','Incidence')
plot(c(5,14),c(0,.5),type='n',xlab='2007 Estimated Prevalence',ylab='Estimated Incidence')
abline(a=0,b=1)
text(x=data[,2],y=data[,3],labels=data[,1],cex=0.8)