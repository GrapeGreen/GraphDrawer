from tkinter import *
root = Tk()

r = 10

class graph:
    def __init__(self):
        self.n = 0
        self.g = []

    def add_vertex(self):
        self.n += 1
        self.g.append([])

    def add(self, u, v):
        u -= 1
        v -= 1
        self.g[u].append(v)
        self.g[v].append(u)

    def print(self):
        pass

    def find(self):
        self.d = [[-1] * (1 << self.n) for i in range(self.n)]
        self.order = []
        for i in range(self.n):
            if self.dfs(i, i, 0) == 1:
                return self.order
        return []

    def dfs(self, u, st, mask):
        mask |= (1 << u)
        if mask == (1 << self.n) - 1:
            if st not in self.g[u]:
                return 0
            self.order.append(st + 1)
            self.order.append(u + 1)
            return 1
        if self.d[u][mask] >= 0: return (self.d[u][mask] == 1) and 1 or 0
        for v in self.g[u]:
            if (mask >> v) & 1 == 0 and self.dfs(v, st, mask):
                self.d[u][mask] = 1
                self.order.append(u + 1)
                return 1
        self.d[u][mask] = 0
        return 0


g = graph()

cv = Canvas(root, height = 1200, width = 1200, bg = "grey80")

crd = []

curr = 0
def add_vertex(event):
    global curr
    crd.append((event.x, event.y))
    g.add_vertex()
    cv.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill = "blue", outline = "grey80")
    for v in g.g[curr]:
        if (v < curr):
            cv.create_line(crd[v], crd[curr], fill = "blue")
    curr += 1
    redraw(event)

def draw_edge(u, v):
    cv.create_oval(crd[u], crd[v], outline = "grey80", fill = "green")

def delete_vertex(event):
    global curr
    global j
    j = -1
    if (curr == 0): return
    curr -= 1
    if not (crd[curr][0] - r <= event.x <= crd[curr][0] + r and crd[curr][1] - r <= event.y <= crd[curr][1] + r):
        curr += 1
        return
    global g
    cv.create_oval(crd[curr][0] - r, crd[curr][1] - r, crd[curr][0] + r, crd[curr][1] + r, fill = "grey80", outline = "grey80")
    for v in g.g[curr]:
        if (v < curr):
            cv.create_line(crd[v], crd[curr], fill = "grey80")
            cv.create_oval(crd[v][0] - r, crd[v][1] - r, crd[v][0] + r, crd[v][1] + r, fill = "blue", outline = "grey80")
    for v in g.g[curr]:
        g.g[v].remove(curr)
    g.g.pop()
    crd.pop()
    g.n -= 1
    redraw(event)

cv.bind("<Double-Button-1>", add_vertex)
cv.bind("<Double-Button-3>", delete_vertex)
cycle = Button(root)
erase_cycle = Button(root)

def get_cycle(event):
    redraw(event)
    if (g.n <= 1): return
    u = g.find()
    if len(u) == 0:
        print('no cycle.')
        return
    for i in range(len(u) - 1):
        cv.create_line(crd[u[i] - 1], crd[u[i + 1] - 1], fill = "red")
        cv.create_oval(crd[u[i] - 1][0] - r, crd[u[i] - 1][1] - r, crd[u[i] - 1][0] + r, crd[u[i] - 1][1] + r, fill = "blue")
        cv.create_oval(crd[u[i + 1] - 1][0] - r, crd[u[i + 1] - 1][1] - r, crd[u[i + 1] - 1][0] + r, crd[u[i + 1] - 1][1] + r, fill="blue")
    print('cycle found successfully!')

def redraw(event):
    for i in range(curr):
        cv.create_oval(crd[i][0] - r, crd[i][1] - r, crd[i][0] + r, crd[i][1] + r, fill = "blue", outline = "grey80")
        for v in g.g[i]:
            if (v < i):
                cv.create_line(crd[v], crd[i], fill = "blue")

j = -1
def make_edge(event):
    global j
    redraw(event)
    if (j == -1):
        for i in range(curr):
            if crd[i][0] - r <= event.x <= crd[i][0] + r and crd[i][1] - r <= event.y <= crd[i][1] + r:
                j = i
                break
        return

    for i in range(curr):
        if crd[i][0] - r <= event.x <= crd[i][0] + r and crd[i][1] - r <= event.y <= crd[i][1] + r:
            if i in g.g[j]:
                cv.create_line(crd[i], crd[j], fill = "grey80")
                g.g[j].remove(i)
                g.g[i].remove(j)
            else:
                g.g[j].append(i)
                g.g[i].append(j)
                cv.create_line(crd[i], crd[j], fill="blue")
            cv.create_oval(crd[i][0] - r, crd[i][1] - r, crd[i][0] + r, crd[i][1] + r, fill="blue", outline="grey80")
            cv.create_oval(crd[j][0] - r, crd[j][1] - r, crd[j][0] + r, crd[j][1] + r, fill="blue", outline="grey80")
            break
    j = -1


cv.bind("<Button-3>", make_edge)

cycle["text"] = "get_cycle"
erase_cycle["text"] = "reset"
cycle.bind("<Button-1>", get_cycle)
erase_cycle.bind("<Button-1>", redraw)
cycle.pack()
erase_cycle.pack()
cv.pack()

root.mainloop()