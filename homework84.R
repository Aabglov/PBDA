data = read.csv("/Users/keganrabil/Desktop/PBDA/Data/rSquared.csv")
dotchart(data$R2,data$State,cex=0.5)