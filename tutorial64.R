library(DAAG)
library(scatterplot3d)
#head(ais)
#str(ais)
plot(ais$ssf,ais$pcBfat)
abline(lm(ais$pcBfat~ais$ssf))
abline(a=1.13066,b=0.157912,col='blue')
abline(a=4.115,b=0.15618,col='red')


males = which(ais$sex == 'm')
females = as.integer(ais$sex == 'f')

points(ais$ssf[males],ais$pcBfat[males],col='blue',pch=16)
points(ais$ssf[-males],ais$pcBfat[-males],col='red',pch=16)

lm.obj = lm(ais$pcBfat~ais$ssf+females)
#lm.obj = lm(ais$pcBfat[-males]~ais$ssf[-males])
#print(summary(lm.obj))
#print(confint(lm.obj))

print("# 9:")
print(" Estimated Difference: 2.984386")
print(" Confidence Interval: [2.6172729, 3.351498]")
print(" 0 is NOT in the CI, thus we believe there is a true difference")


print ("#10:")
print(" Female Model: 0.968")
print(" Male Model: 0.927")

#boxplot(ais$pcBfat~ais$sport,cex.axis=0.8,ylab='Percent Bodyfat')

#scatterplot3d(ais$ferr,ais$pcBfat,ais$ssf)
d <- data.frame(y=ais$ferr, x1= ais$pcBfat, x2=ais$ssf, x3=females)
lm.obj = lm(y ~ ., data=d)
print(summary(lm.obj))
print("#15: ")
print(" Adjusted Coefficient of Determination: ")
print(summary(lm.obj)$adj.r.squared)
print(" Percent Body Fat: 0.531 : There is little to no evidence of linear relationship")
print(" Skin Thickness: 0.958 : There is little to no evidence of linear relationship")
print(" Females: 2.09e-06 : There is strong evidence of linear relationship")

#d <- data.frame(y=ais$ferr, x1= ais$pcBfat, x2=females)
#lm.obj = lm(y ~ ., data=d)
#print(summary(lm.obj))

print("#16: ")
print(" Percent Body Fat: 0.0208 : There is some evidence of linear relationship")
print(" Females: 1.68e-09 : There is strong evidence of linear relationship")

print("#17: ")
print(lm.obj$resid)

resid <- lm.obj$resid
boxplot(resid~ais$sport,cex.axis=0.8,ylab='Ferritins Level')


print("18: ")
print("The two sports with higher than expected levesl of Ferritins are Gym and Tennis")