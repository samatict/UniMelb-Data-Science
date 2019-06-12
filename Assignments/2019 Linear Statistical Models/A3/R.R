# Question 4
setwd("C:\\Users\\Akira Wang\\Dropbox\\University\\Linear Statistical Models\\Lab Data")
df = read.csv("mile.csv")
# symbol plot
palette(c("blue","red"))
plot(df$Time~df$Year, pch=array(df$Gender), col=df$Gender)
# test for no interaction between two predictor values
amodel = lm(Time ~ Gender+Year, df)
imodel = lm(Time ~ Gender*Year+Gender+Year, df)
anova(amodel, imodel) # Interaction is very significant
# final fitted model
summary(imodel)
male = c(imodel$coefficients[1] + imodel$coefficients[2], imodel$coefficients[3] + imodel$coefficients[4])
female = c(imodel$coefficients[1], imodel$coefficients[3])
abline(male)
abline(female)
# point estimate of when female beats the male world record
-imodel$coefficients[2]/imodel$coefficients[4]
# male = female testable?

# 95% CI for the gap between Male and Female every year
ci = gmodels::estimable(imodel, c(0,0,0,1), conf.int=0.95)
c(ci$Lower, ci$Upper)
# Hypothesis that male decreases 0.3 every year
car::linearHypothesis(imodel, c(0,0,1,1), -0.3) # reject that the slope is -0.3. we can conclude that the record decreases even faster (given the slope is negative)





