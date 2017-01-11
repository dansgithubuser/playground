def generator_generator(word):
	for i in range(14): yield word[i%len(word)]
generator=generator_generator('happily')
for i in generator: print(i)
