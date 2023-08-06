from math import floor

def get_empty(field):
	for y, _1 in enumerate(field):
		for x, _2 in enumerate(_1):
			if field[y][x] == " ":
				return (x, y)
	return None

def check_field(field):
	fs = [[] for i in range(9)]
	for yn, y in enumerate(field):
		for xn, x in enumerate(y):
			fs[floor(floor(xn / 3) + floor(yn / 3) * 3 - 1)].append(x)

			if x != " " and (y.count(x) > 1 or x in [i[xn] for i in field[yn+1:]]):
				return False

	for f in fs:
		for i in f:
			if f.count(i) > 1 and i != " ":
				return False

	return True

def loop(field):
	if not check_field(field):
        	return None

	e = get_empty(field)
	if e is None:
		return field
	
	for i in range(1, 10):
		nfield = [[k for k in j] for j in field]
		nfield[e[1]][e[0]] = str(i)
		z = loop(nfield)
		if z is not None:
			return z

	return None

def fprint(field):
	for yn, y in enumerate(field):
		if yn % 3 == 0 and yn != 0:
		    print("------+-------+------")
			
		for xn, x in enumerate(y):
			if xn % 3 == 0 and xn != 0:
				print("|", end=" ")
			print(x, end=" ")
		print()

