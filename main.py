from scipy.stats import beta

a = 7.2
b = 2.3
m, v = beta.stats(a, b, moments="mv")
mean = beta.mean(a=a, b=b)
var = beta.var(a=a, b=b)
print("The mean is " + str(m))
print("The variance is " + str(v))

prob = 1 - beta.cdf(a=a, b=b, x=.90)
print("The probability of having a variance over 90% is " + str(prob))
