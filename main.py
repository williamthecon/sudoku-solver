import time

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
			if xn < 3 and yn < 3:
				fs[0].append(x)
			elif xn < 6 and yn < 3:
				fs[1].append(x)
			elif xn < 9 and yn < 3:
				fs[2].append(x)
			elif xn < 3 and yn < 6:
				fs[3].append(x)
			elif xn < 6 and yn < 6:
				fs[4].append(x)
			elif xn < 9 and yn < 6:
				fs[5].append(x)
			elif xn < 3 and yn < 9:
				fs[6].append(x)
			elif xn < 6 and yn < 9:
				fs[7].append(x)
			elif xn < 9 and yn < 9:
				fs[8].append(x)

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
    t = "\n".join([" ".join(f) for f in field])
    print(t)
