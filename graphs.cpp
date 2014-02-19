#include <iostream>
#include <list>
#include <numeric>
#include <fstream>
using namespace std;

const int MAXV = 100;
const int INF = INT_MAX/2;
 
struct Edge
{
  int v, w;
  Edge() {}
  Edge(int _v, int _w) : v(_v), w(_w) { }
};

struct Graph
{
  int nv;
  list<Edge> edges[MAXV+1];
  Graph(int n) : nv(n) { }
  
  void insert_edge(int a, int b, int w)
  {
    edges[a].push_back(Edge(b, w));
  }
  
  void insert_undirected_edge(int a, int b, int w)
  {
	insert_edge(a, b, w);
	insert_edge(b, a, w);
  }

  // returns  the weight of the MST
  int prim(int start) 
  {
    bool intree[MAXV+1];
    int parent[MAXV+1];
    int distance[MAXV+1];

    int i, v, weight, dist, u;
    list<Edge>::const_iterator it;

    for (i = 1; i <= nv; i++) {
      parent[i] = -1;
      distance[i] = INF;
      intree[i] = false;
    }

    v = start;
    distance[v] = 0;

    while (!intree[v]) {
      intree[v] = true;
      
      for (it = edges[v].begin(); it != edges[v].end(); it++) {
		u = (*it).v;
		weight = (*it).w;
		if (distance[u] > weight && !intree[u]) {
		  distance[u] = weight;
		  parent[u] = v;
		}
      }

      v = 0;
      dist = INF;
      for (i = 1; i <= nv; i++)
		if (dist > distance[i] && !intree[i]) {
			v = i;
			dist = distance[i];
		}
	
    }
    
    // print tree edges
    cout << "Print tree structure:" << endl;
    for (i = 1; i <= nv; i++) {
		// start vertex has no parent
		if (i == start)
			continue;
		cout << "(" << parent[i] << ", " << i << ")" << endl;
	}
 
    return accumulate(distance+1, distance+nv+1, 0);
  }
  
  void dijkstra(int start) 
  {
    bool discovered[MAXV+1];
    int parent[MAXV+1];
    int distance[MAXV+1];

    int i, v, weight, dist, u;
    list<Edge>::const_iterator it;

    for (i = 1; i <= nv; i++) {
      parent[i] = -1;
      distance[i] = INF;
      discovered[i] = false;
    }

    v = start;
    distance[v] = 0;

    while (!discovered[v]) {
      discovered[v] = true;
	  
	  // scan v's adjacency list to update distances
      for (it = edges[v].begin(); it != edges[v].end(); it++) {
		u = (*it).v;
		weight = (*it).w;
		if (distance[u] > weight+distance[v]) {
		  distance[u] = weight+distance[v];
		  parent[u] = v;
		}
      }

	  // find next node to explore (the closest one)
      v = 0;
      dist = INF;
      for (i = 1; i <= nv; i++)
		if (dist > distance[i] && !intree[i]) {
			v = i;
			dist = distance[i];
		}
	
    }
    
    // print tree edges
    cout << "Printing parent to each node:" << endl;
    for (i = 1; i <= nv; i++) {
		// start vertex has no parent
		if (i == start)
			continue;
		cout << "(" << parent[i] << ", " << i << ")" << endl;
	}
 
    //return accumulate(distance+1, distance+nv+1, 0);
  }

};

// returns a pointer to a new allocated graph
Graph *read_graph_from_stdin(bool directed)
{
	// input structure: first line contains # of nodes, next lines edges pairs with weight
	int n;
	int x, y, w;
	cin >> n;
	Graph *g = new Graph(n);
	while(cin >> x >> y >> w) {
		if (directed)
			g->insert_edge(x, y, w);
		else
			g->insert_undirected_edge(x, y, w);
	}
}

int main()
{
  bool directed = true;
  Graph *g = read_graph_from_stdin(directed);
  g->prim(1);
	
  return 0;
}
