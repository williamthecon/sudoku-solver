import time
import pyautogui as pag
import keyboard as kb

def get_empty(field):
    empty = [(x, y) if field[y][x] == " " else None for y, _1 in enumerate(field) for x, _2 in enumerate(_1)]
    for i in range(empty.count(None)):
        empty.remove(None)
    return empty

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

    try:
        e = get_empty(field)[0]
    except IndexError:
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

def calc_ps(_h, _w):
	ws = [312, 391, 473, 556, 636, 718, 801, 882, 964]
	hs = [196, 272, 354, 440, 518, 599, 684, 763, 845]
	w1 = ws[_w] + 17
	h1 = hs[_h] + 8
	w2 = ws[_w] + 60
	h2 = hs[_h] + 70
	p1 = (w1, h1)
	p2 = (w2, h2)

	return p1, p2

def roundabout(n):
	l = []
	for i in range(-5, 6):
		l.append(n + i)

	return l

def any_in(l1, l2):
	for l in l1:
		if l in l2:
			return True

	return False

def sort_out_similar(s):
	l = []
	hs = []
	for i in s:
		r = roundabout(i[1])
		if not any_in(r, hs):
			l.append(i)

		hs.append(i[1])

	return l

def nearest_point(x):
	ws = [312, 391, 473, 556, 636, 718, 801, 882, 964, 9999]
	hs = [196, 272, 354, 440, 518, 599, 684, 763, 845, 9999]
	for n, _w in enumerate(ws):
		if _w > x[0]:
			w = n-1
			break
	for n, _h in enumerate(hs):
		if _h > x[1]:
			h = n-1
			break

	return w, h

def get_field():
	field = [[" " for i in range(9)] for j in range(9)]

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/1.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "1"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/2.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "2"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/3.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "3"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/4.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "4"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/5.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "5"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/6.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "6"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/7.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "7"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/8.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "8"

	for x in sort_out_similar([(i.left, i.top) for i in pag.locateAllOnScreen("locates/9.png", confidence=0.9)]):
		w, h = nearest_point(x)
		field[h][w] = "9"

	return field

def get_differences(f1, f2):
	d = {str(i): [] for i in range(1, 10)}
	for yn, y in enumerate(f1):
		for xn, x in enumerate(y):
			if x != f2[yn][xn]:
				d[f2[yn][xn]].append((xn, yn))
	return d

def auto_klassik():
	while not kb.is_pressed("p"):
		while True:
			if kb.is_pressed("p"):
				quit()
			x = pag.locateOnScreen("locates/ad_weg.png", confidence=0.8)
			if x is not None:
				pag.click(pag.center(x))
			x = pag.locateOnScreen("locates/fertig_erkennung.png", confidence=0.9)
			if x is not None:
				break
			time.sleep(.1)
		s = time.perf_counter()
		field = get_field()
		print(time.perf_counter() - s)
		fprint(field)
		print(field)

		s = time.perf_counter()
		nfield = loop(field)
		print(time.perf_counter() - s)
		fprint(nfield)

		if kb.is_pressed("p"):
			break

		selects = {"1": (348, 1001), "2": (431, 1001), "3": (509, 999), "4": (600, 999), "5": (674, 996), "6": (761, 996), "7": (844, 998), "8": (923, 998), "9": (1005, 1003)}
		difs = get_differences(field, nfield)
		for s, ps in difs.items():
			pag.click(selects[s])
			for p in ps:
				p1, p2 = calc_ps(p[1], p[0])
				pag.click(p1)

		while True:
			pag.click((170, 490))
			if kb.is_pressed("p"):
				quit()
			x = pag.locateOnScreen("locates/erneut_spielen.png", confidence=0.9)
			if x is not None:
				break
			time.sleep(.1)
		pag.click(pag.center(x))
		pag.moveTo((1, 1))

def scan_and_solve():
	while not kb.is_pressed("p"):
		time.sleep(.1)
	s = time.perf_counter()
	field = get_field()
	print(time.perf_counter() - s)
	fprint(field)
	print(field)

	s = time.perf_counter()
	nfield = loop(field)
	print(time.perf_counter() - s)
	fprint(nfield)

auto_klassik()
#field = [[' ', '9', '7', '2', ' ', '6', ' ', '3', '1'], [' ', ' ', ' ', '1', ' ', '5', '4', ' ', '6'], [' ', ' ', ' ', ' ', '9', ' ', ' ', '5', ' '], ['7', ' ', ' ', ' ', ' ', ' ', '9', ' ', '3'], ['9', ' ', '3', ' ', '8', ' ', ' ', '6', ' '], [' ', '5', '2', ' ', '6', '3', ' ', '7', ' '], [' ', '6', '9', ' ', ' ', '1', '5', '2', ' '], ['1', ' ', '5', '6', ' ', ' ', '3', ' ', ' '], ['3', ' ', '4', '8', ' ', ' ', '6', '1', '7']]
#print(check_field(field))
