toy_data <- read.csv('toy1.csv')

# Does x predict (equal, zero, random, noisy)?
# I searched a _lot_ how to do this on one line.
# I'm convinced that, while it may be doable, it's far-off the beaten path.
# https://stats.stackexchange.com/questions/26585/how-to-do-a-generalized-linear-model-with-multiple-dependent-variables-in-r
summary(lm(equal~x, toy_data))   # yes    - high coeff, low Pr(>|t|)
summary(lm(zero~x, toy_data))    # no     - zero coeff
summary(lm(small~x, toy_data))   # yes    - low coeff , low Pr(>|t|)
summary(lm(random~x, toy_data))  # no     - low coeff , high Pr(>|t|)
summary(lm(noisy~x, toy_data))   # yesish - high coeff, medium Pr(>|t|)

#=====#

toy_data <- read.csv('toy2.csv')

# Does in[i] predict out?
summary(lm(out~in1+in2+in3+in4+in5, toy_data))
# in1: yes    - high coeff, low Pr(>|t|)
# in2: no     - low coeff , high Pr(>|t|)
# in3: yesish - low coeff , medium Pr(>|t|)
# in4: no     - low coeff , high Pr(>|t|)
# in5: yes    - high coeff, low Pr(>|t|)
# but note that these answers can change -- ie 1000 samples is too small to discern 3 real signals with a red herring and a _clearly unrelated_ null
