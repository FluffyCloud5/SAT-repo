# Task 1
## Q1 
```python
import heapq
from collections import deque
import math

def min_battery_cost(graph, source):

    visited = {v: False for v in graph.keys()}
    dist = {v: math.inf for v in graph.keys()}
    dist[source] = 0
    pq = [(0,source)]
    while pq: 
        _,u = heapq.heappop(pq)
        if(visited[u] == True):
            continue
        visited[u] = True

        for v,w in graph[u]:
            if visited[v]:
                continue
            if(dist[v] == None or dist[v] > dist[u] + w ):
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v],v))
    return dist
```
## Q2
```python
{
  "A": 7,
  "B": 6,
  "C": 3,
  "D": 4,
  "E": 9,
  "F": 3,
  "G": 9,
  "L": 0
}
```

.
.
.
.
.
.
## Q3
### a)
```python
graph = {
'A': [('B', 0), ('C', 1)],
'B': [('C', 0)],
'C': []
}
```
Graph: 
.
.
.
.
.
.
.
.
.
.
Source: **A**

### b)
```python
{
  "A": 0,
  "B": 0,
  "C": 0
}
```
### c)
```python
{
  "A": 0,
  "B": 0,
  "C": 1
}
```
C has the wrong distance here, it should be zero but it is one.

## Q4

### a) 
I choose to not get rid of stale priority queue entries from the priority queue as priority queues don't allow for easy editing in the middle. Therefore instead of removing stale entries immediately when a faster route is found I instead chose to ignore them as visited once they are popped. 

### b) 
I encountered that the objects in the priority queue 'pq' are not just nodes but tuples with the nodes importance attached to it, when using heappop. I detected it through realising that their was a type error when plugging u into the visited dictionary as a key, and I fixed it by placing a dummy variable \'\_\' to catch the priority of u, meaning u was just the string representing a node. 

# Task 2 
## Q5 
```python
def pagerank(graph, d = 0.85, tol=1e-6, max_iter = 200):
    N = len(graph)
    PR = {v: 1/N for v in graph.keys()}
    out = {v: len(graph[v]) for v in graph.keys()}
    dangling = []
    incoming = {v: [] for v in graph.keys()}
    for v in graph.keys():
        for u in graph[v]:
            incoming[u].append(v)
        if not graph[v]: 
            dangling.append(v)
    def update(PR):
        new_PR = {v: 0 for v in graph.keys()}
		
        dangling_const = sum(PR[v] for v in dangling)*d/N
		
        for u in graph.keys(): 
            for v in incoming[u]:
                new_PR[u] += d*PR[v]/out[v]
            new_PR[u] += (1-d)/N + dangling_const
            
        return new_PR	
    def tolarance_reached(PR, new_PR):
        for u in graph.keys(): 
           if abs(PR[u] - new_PR[u]) >= tol:
                return False
        return True
    k = 0
    done = False
    while (not done and k < max_iter):
        new_PR = update(PR)
        if tolarance_reached(PR, new_PR):
            done = True
        PR = new_PR
        k += 1    
    return PR
```

## Q6 

### mini graph: 

| iteration | PR(L) | PR(A) | PR(B) | PR(C) | PR(D) |
| --------- | ----- | ----- | ----- | ----- | ----- |
| 0         | 0.2   | 0.2   | 0.2   | 0.2   | 0.2   |
| 1         | 0.234 | 0.149 | 0.149 | 0.319 | 0.149 |
#### dangling node contribution: 
 Dangling nodes: **D**. 
 so $\frac{d \times PR(D)}{N} = \frac{0.85\times0.2}{5} = 0.034$
#### jump case: 
$\frac{1-d}{N} = \frac{1-0.85}{5} = 0.03$
#### Working Out: 
PR(L)/out(L) = 0.2/2= 0.1
PR(A)/out(A) = 0.2/1= 0.2
PR(B)/out(B) = 0.2/2= 0.1
PR(C)/out(C) = 0.2/1= 0.2
PR(D)/out(D) = 0.2/0 = undefined

PR'(L) = $\frac{1-d}{N} + \frac{d \times PR(D)}{N} + d\times PR(C)/out(C) = 0.034+0.03 +0.85\times0.2 = 0.234$

PR'(A) = $\frac{1-d}{N} + \frac{d \times PR(D)}{N} + d\times PR(L)/out(L) = 0.034+0.03 +0.85\times0.1 = 0.149$

PR'(B) = $\frac{1-d}{N} + \frac{d \times PR(D)}{N} + d\times PR(L)/out(L) = 0.034+0.03 +0.85\times0.1 = 0.149$

PR'(C) = $\frac{1-d}{N} + \frac{d \times PR(D)}{N} + d(PR(A)/out(A) + PR(B)/out(B))$
$= 0.034+0.03 +0.85\times(0.2+0.1)$
$= 0.319$

PR'(D) = $\frac{1-d}{N} + \frac{d \times PR(D)}{N} + d\times PR(B)/out(B) = 0.034+0.03 +0.85\times0.1 = 0.149$

sum of PRs = 
$0.234 + 1.49 +1.49 + 0.319 + 1.49 = 0.23 + 1.5\times3+0.32 = 0.55 + 0.45 = 1$
#### Actual Output: 
```python
{
  "L": 0.1632,
  "A": 0.0993,
  "B": 0.0993,
  "C": 0.1567,
  "D": 0.0722
}
```
### Assigned Graph (10)

N = 7
start_value = 1/N = 1/7

| iteration | PR(L) | PR(A) | PR(B) | PR(C) | PR(D) | PR(E) | PR(F) |
| --------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 0         | 1/7   | 1/7   | 1/7   | 1/7   | 1/7   | 1/7   | 1/7   |
| 1         |       |       |       |       |       |       |       |

#### dangling node contribution: 
 Dangling nodes: **C**. 
 so $\frac{d \times PR(C)}{N} = \frac{17/20\times1/7}{5} = \frac{17}{700}$
#### jump case: 
$\frac{1-d}{N} = \frac{1-17/20}{7} = \frac{3}{140}$
#### Working Out: 
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
#### Actual Output: 
```python
{
  "A": 0.0687,
  "B": 0.0912,
  "C": 0.0833,
  "D": 0.0664,
  "E": 0.1177,
  "F": 0.0409,
  "L": 0.0597
}
```
## Q7

### a)
If dangling nodes are not handled, i.e. their rank is not redistributed back into the system, it simply means that the sum of all the pageranks will be less than one. One way to interpret this is to say their is another node in the graph that is a sink node from all dangling node with an arrow pointing to itself, kind of the 'what do the broadcasts do outside of this graph' kind of node. 

### b) 
Sum of pageranks = 0.8786... (graph 10)
	= 0.83 (mini graph) 
The sum is less than one because the rank of the dangling nodes has been lost. 
It is precisely these numbers as the $d \times PR($dangling node$)$ has been lost.
this can be seen as 
$1-d \times PR(C) =1-0.85/7 = 0.8786...$ (graph 10)
and: 
$1-d \times PR(D) =1-0.85/5 = 0.83$ (mini graph)


