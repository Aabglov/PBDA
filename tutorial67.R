library('ggplot2')
data = read.csv('/Users/keganrabil/Desktop/bikeShare.csv')
names = c('dattime','season','holiday','workingday','weather','temp','atemp','humidity','windspeed','casual','registered','sum')
colnames(data) = names
head(data)
str(data)
hour = as.integer(substr(data$dattime,12,13))
#table(hour)
#boxplot(data$sum~hour)

n = dim(data)[1]
labels = c(rep('casual',n),rep('registered',n))
df = data.frame(as.factor(rep(hour,2)),c(data$casual,data$registered),labels)
colnames(df) = c('hour','count','rider')

#plot = ggplot(data = df, aes(x = hour,y=count)) + geom_boxplot(fill='red') + facet_wrap(~rider)
#print(plot)

lm.obj = lm(registered ~ -1 + as.factor(hour),data=data)
#print(summary(lm.obj))
sigma_reg <- var(lm.obj$resid)
sigma <- var(data$registered)
R_2 <- (sigma - sigma_reg)/sigma
print(R_2)
r.obj = lm(registered ~ as.factor(hour) + workingday,data=data)
print(summary(r.obj))
c.obj = lm(casual ~ as.factor(hour) + workingday,data=data)
print(summary(c.obj))

print("11: ")
print("Proportion of Variance for Registered Model: ")
print((var(data$registered) - var(r.obj$resid))/var(data$registered))
print("Proportion of Variance for Casual Model: ")
print((var(data$casual) - var(c.obj$resid))/var(data$casual))
print("The Registered Model has greater predictive power")


print("12:")
print("Esimated number of Registered bikers at 8:00am on a workday:")
print(18.886 + 38.074 + 296.400)
print("Esimated number of Registered bikers at 8:00am on a workday:")
print(33.7195 + 11.2308 - 34.3560)

print("Esimated number of Registered bikers at 8:00am on a non-workday:")
print(18.886 + 296.400)
print("Esimated number of Registered bikers at 8:00am on a non-workday:")
print(33.7195 + 11.2308)


temp.obj = r.obj = lm(registered ~ as.factor(hour) + workingday + temp,data=data)
print(summary(temp.obj))
print("13: The estimated effect on registered users is 4 more users for every degree")

temp_var.obj = lm(registered ~  workingday + as.factor(hour) * temp,data=data)
print(summary(temp_var.obj))
print(anova(temp_var.obj))
print("14: temp does depend on hour of day")

print(temp_var.obj$coeff[27:49])
plot(temp_var.obj$coeff[27:49])
print("The temperature matters most around 5 or 6 pm")