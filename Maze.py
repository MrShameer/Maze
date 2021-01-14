import random
from tkinter import *

master = Tk()
north = 0
south = 1
east = 2
west = 3

s=int(input("Size: "))
w = Canvas(master, width=s*40, height=s*40)
cell =[[0 for x in range(4)] for y in range(s*s)]

for i in range(s*s):
	cell[i][north] = i-s
	cell[i][south] = i+s
	cell[i][east] = i+1
	cell[i][west] = i-1

for i in range(s):
	cell[i][north] = -1
	cell[s*s-i-1][south] = -1

for i in range(0,s*s,++s):
	cell[s*s-i-1][east] = -1
	cell[i][west] = -1

set = [-1 for i in range(s*s)]

def same(r1,r2):#union
	if set[r2]<set[r1]:
		set[r1]=r2
	else:
		if set[r1]==set[r2]:
			set[r1]-=1
		set[r2]=r1

def find(x):
	if set[x]<0:
		return x
	else:
		set[x] = find(set[x])
		return set[x]

def connected():
	count = 0
	for i in range(0,len(set),1):
		if set[i]<0:
			count+=1

		if count>1:
			return False
	return True

def clear(): #break walls
	while connected() == False:
		cell1 = random.randint(0,s*s-1)
		w1 = random.randint(0,3)
		cell2 = cell[cell1][w1]

		if cell2 !=-1 and cell2 != s*s:
			if find(cell1) != find(cell2):
				cell[cell1][w1]=s*s

				if w1 == north or w1 == east:
					cell[cell2][w1 + 1] = s*s

				if w1 == south or w1 == west:
					cell[cell2][w1 - 1] = s*s	
				same(find(cell1),find(cell2))
	if s%2==0:
		d=s-2
	else:
		d=s-1

	cell[d//2][north]=s*s;
	cell[s*s-d//2-1][south]=s*s; #s*(s-1)+((s*s-(s*d//2+s-1)-1)//s
	cell[s*(d//2+1)-1][east]=s*s; #s*d//2+s-1
	cell[s*(s-d//2-1)][west]=s*s; #s*s-(s*d//2+s-1)-1
	
def screen():
	w.pack()
	dist = 30 #length of line
	cells = 0
	start = 20 #starting point on frame
	for i in range(s):
		for j in range(s):
			if cell[cells][north] != s*s:
				w.create_line(dist*j+start,dist*i+start,dist*j+dist+start,dist*i+start)
			if cell[cells][south] != s*s:
				w.create_line(dist*j+start,dist*i+dist+start,dist*j+dist+start,dist*i+dist+start)
			if cell[cells][east] != s*s:
				w.create_line(dist*j+dist+start,dist*i+start,dist*j+dist+start,dist*i+dist+start)
			if cell[cells][west] != s*s:
				w.create_line(dist*j+start,dist*i+start,dist*j+start,dist*i+dist+start)
			cells+=1

	block = w.create_rectangle(dist/5+start,dist/5+start,dist-dist/5+start,dist-dist/5+start, outline="#fb0", fill="#fb0")
	spot=0
	def move(spot):
		nonlocal block
		w.delete(block)
		col = spot%s
		row = spot//s
		block = w.create_rectangle(dist/5+dist*col+start,dist/5+dist*row+start,(dist*col+dist+start)-dist/5,(dist*row+dist+start)-dist/5,outline="#fb0", fill="#fb0")
	def key_pressed(event):
		nonlocal spot
		if event.char == 'w' or event.keysym=='Up':
			if cell[spot][north] == s*s:
				spot -= s
				move(spot)
		elif event.char == 's' or event.keysym=='Down':
			if cell[spot][south] == s*s:
				spot += s
				move(spot)
		elif event.char == 'd' or event.keysym=='Right':
			if cell[spot][east] == s*s:
				spot += 1
				move(spot)
		elif event.char == 'a' or event.keysym=='Left':
			if cell[spot][west] == s*s:
				spot -= 1
				move(spot)
		master.mainloop()
	master.bind("<Key>",key_pressed)
	mainloop()

clear()
screen()

