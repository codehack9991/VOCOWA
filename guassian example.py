# update = measurements
# predict = motions
# note every update/ (sensor measurement) decreases sigma(increases certainty)
# exactly opp for predict/ motion


def update(mean1, var1, mean2, var2):
    new_mean = float(var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1./(1./var1 + 1./var2)
    return [new_mean, new_var]


def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

for i in range(len(motion)):
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)

print [mu, sig]

# mu is expected position of the object
# sigma is the margin of error, so we wanna keep it low, sigma < 1-2 cm
