library('ggplot2')
data = read.csv('/Users/keganrabil/Desktop/bikeShare.csv')
names = c('dattime','season','holiday','workingday','weather','temp','atemp','humidity','windspeed','casual','registered','sum')
colnames(data) = names
head(data)

n = dim(data)[1]
labels = c(rep('casual',n),rep('registered',n))
hour = as.integer(substr(data$dattime,12,13))
#df = data.frame(as.factor(rep(hour,2)),c(data$casual,data$registered),labels)
#colnames(df) = c('hour','count','rider')

c.obj = lm(casual ~ as.factor(hour) + as.factor(workingday) + as.factor(holiday),data=data)
print(summary(c.obj))

df = data.frame(c.obj$fitted,c.obj$resid,hour)
colnames(df) = c('Fitted','Residuals','Hour')

plt = ggplot(df, aes(x=Fitted, y=Residuals)) + geom_point(alpha=.2,pch=16)
plt = plt + xlab("Fitted Values") + ylab("Residuals")
print(plt)

print("4a:")
print("    Yes, there is evidence of lack of fit due to the fact that the small fitted values all have positive residuals.")
print("4b:")
print("     Yes, the residuals increase as the fitted values increase")
print("4c: ")
print("     The greatest value the residual can take is -fitted value, so the lower boundary of the model follows a line with slope of -1")

qqnorm(scale(c.obj$resid),main=NULL,pch=16,cex=.8)
abline(a=0,b=1)

print("5:")
print("     Yes, the sample quantiles differ significantly from the theoretical from 2-4")

acf(c.obj$resid)

datetime=strptime(as.character(data$dattime),format="%Y-%m-%d %H:%M:%S")
elapsedDays = as.integer(julian(datetime)-14975)

df = data.frame(elapsedDays,c.obj$resid)
colnames(df) = c('Day','Residuals')
plt = ggplot(df, aes(x=Day,y=Residuals)) + geom_point(alpha=.2,pch=16)
plt = plt + xlab("Day") + ylab("Residuals") + geom_hline(yintercept=0)
plt = plt + geom_smooth()
print(plt)

print("8:")
print("     The patterns are seasonal.  The over-estimates occur during the summer when biking is more common.  The under estimation occurs during winter when it is more difficult and less comfortable to bike.")

print("9: ")
c.obj = lm(casual ~ as.factor(hour) + as.factor(workingday) + as.factor(holiday) + as.factor(season),data=data)
df = data.frame(elapsedDays,c.obj$resid)
colnames(df) = c('Day','Residuals')
plt = ggplot(df, aes(x=Day,y=Residuals)) + geom_point(alpha=.2,pch=16)
plt = plt + xlab("Day") + ylab("Residuals") + geom_hline(yintercept=0)
plt = plt + geom_smooth()
print(plt)

print("    The inclusion of season as a variable greatly reduced the variance in the model")