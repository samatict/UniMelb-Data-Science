# Question 5
y = c(5.5,5.9,6.5,5.9,8,9,10,10.8)
X = matrix(c(rep(1,8),7.2,10,9,5.5,9,9.8,14.5,8,8.7,9.4,
             10,9,12,11,12,13.7,5.5,4.4,4,7,5,6.2,5.8,3.7),8,4)

Xscaled = scale(X[,-1]) # No intercept parameter (Piazza)
yscaled = scale(y, scale=FALSE) # Only centering, no scale (Piazza)
r = dim(t(Xscaled)%*%Xscaled)
n = dim(Xscaled)[1]

aic = c()
lambdas = seq(0, 0.5, by=0.01)

library(matrixcalc)

for (i in lambdas){
  lambda = diag(i, r)
  
  ridgeb = solve(t(Xscaled)%*%Xscaled + lambda, t(Xscaled)%*%yscaled)
  SSRes = t(yscaled-Xscaled%*%ridgeb)%*%(yscaled-Xscaled%*%ridgeb)
  
  H = Xscaled%*%solve(t(Xscaled)%*%Xscaled + lambda)%*%t(Xscaled)
  
  aic = c(aic, n*log(SSRes/n) + 2*matrix.trace(H))
}

plot(lambdas, aic, col='orange', type='l')
lambda_aic = lambdas[which.min(aic)]
lambda_aic

# library(glmnet)
# fit.ridge <- glmnet(x = Xscaled, y = yscaled, alpha = 0)
# plot(fit.ridge, xvar = "lambda", label = T)
# cv.ridge <- cv.glmnet(x = Xscaled, y = yscaled, alpha = 0)
# cv.ridge$lambda.min

