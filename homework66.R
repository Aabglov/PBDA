library('DAAG')
head(ais)
str(ais)

plot(ais$pcBfat,ais$ssf)

males = which(ais$sex=='m')
points(ais$pcBfat[males],ais$ssf[males],col='blue',pch=16)
points(ais$pcBfat[-males],ais$ssf[-males],col='red',pch=16)

#lm.obj = lm(pcBfat[males]~ssf[males],data=ais)
#abline(lm.obj,col='red')
abline(lm(ais$ssf~ais$pcBfat))