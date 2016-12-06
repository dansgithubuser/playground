def mean_and_deviation(x):
	from math import sqrt
	m=sum(x)/float(len(x))
	return m, sqrt(sum([(i-m)**2 for i in x]))

def person_familiarity(familiarity, person, team):
	return sum([familiarity[person][i] for i in team])

def team_familiarity(familiarity, team):
	return sum([person_familiarity(familiarity, i, team) for i in team])

def persons_familiarity(familiarity, teams):
	result=[]
	for team in teams:
		for person in team:
			result.append(person_familiarity(familiarity, person, team))
	return result

def teams_familiarity(familiarity, teams):
	return [team_familiarity(familiarity, i) for i in teams]

def fitness_equal_persons(familiarity, teams):
	m, d=mean_and_deviation(persons_familiarity(familiarity, teams))
	return -d+m

def fitness_equal_teams(familiarity, teams):
	m, d=mean_and_deviation(teams_familiarity(familiarity, teams))
	return -d+m

def fitness(familiarity, teams, extra_value=lambda teams: 0):
	return (
		fitness_equal_persons(familiarity, teams)
		+
		fitness_equal_teams(familiarity, teams)
		+
		extra_value(teams)
	)

def find(teams, person):
	for i in range(len(teams)):
		for j in range(len(teams[i])):
			if teams[i][j]==person: return i, j
	raise Exception("person isn't in team!")

def swap(teams, person_a, person_b):
	import copy
	new_teams=copy.deepcopy(teams)
	ai, aj=find(teams, person_a)
	bi, bj=find(teams, person_b)
	new_teams[ai][aj]=teams[bi][bj]
	new_teams[bi][bj]=teams[ai][aj]
	return new_teams

def matrix_from_score(population, f=min):
	familiarity={}
	for person_a, score_a in population.items():
		familiarity[person_a]={}
		for person_b, score_b in population.items():
			familiarity[person_a][person_b]=min(score_a, score_b)
	return familiarity

def assign_teams(familiarity, n_teams, extra_value=lambda teams: 0):
	#start with random assignment
	import random
	items=familiarity.items()
	random.shuffle(items)
	teams=[[] for i in range(n_teams)]
	for i in range(len(items)):
		teams[i%n_teams].append(items[i][0])
	#try all switches until nothing improves
	while True:
		did_something=False
		for i in familiarity:
			for j in familiarity:
				new_teams=swap(teams, i, j)
				if fitness(familiarity, new_teams, extra_value)>fitness(familiarity, teams, extra_value):
					teams=new_teams
					did_something=True
		if not did_something: break
	#done
	return teams

def show(familiarity, teams):
	for i in range(len(teams)):
		print('team {}: {}'.format(i, team_familiarity(familiarity, teams[i])))
		for person in teams[i]:
			print('\t{}: {}'.format(person, person_familiarity(familiarity, person, teams[i])))
	m, d=mean_and_deviation(persons_familiarity(familiarity, teams))
	print('average person familiarity: {}'.format(m))
	print('deviation in person familiarity: {}'.format(d))

if __name__=='__main__':
	import random
	population={i: i for i in range(30)}
	print('population: {}'.format(population))
	familiarity=matrix_from_score(population)
	teams=assign_teams(familiarity, 6)
	show(familiarity, teams)
