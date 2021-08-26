#include <bits/stdc++.h>
using namespace std;

vector<vector<pair<int, int>>> adj;

map<string, int> id;

const long long INF = 1e18;

void bellmanFord(int src, vector<long long> &d, vector<int> &nxt)
{
    fill(d.begin(), d.end(), INF);
    d[src] = 0;
    int n = int(adj.size());
    vector<int> prv(n, -1);
    for (int _ = 0; _ <= n; _++)
    {
        for (int u = 0; u < n; u++)
        {
            for (pair<int, int> p : adj[u])
            {
                int v = p.first, cost = p.second;
                if (d[v] > d[u] + cost)
                {
                    d[v] = d[u] + cost;
                    prv[v] = u;
                }
            }
        }
    }

    for (int i = 0; i < n; i++)
    {
        if (i == src)
        {
            nxt[i] = src;
        }
        else
        {
            int at = i;
            while (prv[at] != src)
            {
                at = prv[at];
            }
            nxt[i] = at;
        }
    }
}

void distanceFinder(string src)
{
    int s = id[src];
    int n = int(adj.size());

    vector<long long> d(n);
    vector<int> nxt(n);
    bellmanFord(s, d, nxt);

    vector<string> ip(n);
    for (auto pp : id)
    {
        ip[pp.second] = pp.first;
    }

    for (auto pp : id)
    {
        int i = pp.second;
        cout << src << ", " << pp.first << ", " << d[i] << ", " << ip[nxt[i]] << endl;
    }
    cout << endl;
}

void updateRouterCost(string from, string to, int increase, string src)
{
    int n = int(adj.size());

    vector<string> ip(n);
    for (auto pp : id)
    {
        ip[pp.second] = pp.first;
    }

    vector<long long> d_before(n);
    vector<int> nxt_before(n);
    bellmanFord(id[src], d_before, nxt_before);

    int u = id[from], v = id[to];
    for (auto &pp : adj[u])
    {
        if (pp.first == v)
        {
            pp.second += increase;
        }
    }
    for (auto &pp : adj[v])
    {
        if (pp.first == u)
        {
            pp.second += increase;
        }
    }

    vector<long long> d_after(n);
    vector<int> nxt_after(n);
    bellmanFord(id[src], d_after, nxt_after);

    vector<int> case1, case2;

    for (int i = 0; i < n; i++)
    {
        if (d_after[i] == d_before[i])
        {
            case1.push_back(i);
        }
        else
        {
            case2.push_back(i);
        }
    }

    sort(case1.begin(), case1.end(), [&](int x, int y) { return ip[x] < ip[y]; });
    sort(case2.begin(), case2.end(), [&](int x, int y) { return ip[x] < ip[y]; });

    cout << "Case-1" << endl;
    for (int x : case1)
    {
        cout << src << ", " << ip[x] << ", " << d_after[x] << ", " << ip[nxt_after[x]] << endl;
    }
    cout << "Case-2" << endl;
    for (int x : case2)
    {
        cout << src << ", " << ip[x] << ", " << d_after[x] << ", " << ip[nxt_after[x]] << endl;
    }
    cout << endl;

    for (auto &pp : adj[u])
    {
        if (pp.first == v)
        {
            pp.second -= increase;
        }
    }
    for (auto &pp : adj[v])
    {
        if (pp.first == u)
        {
            pp.second -= increase;
        }
    }
}

void addRouter(string ip, vector<string> ns, vector<int> costs, string src)
{
    id[ip] = int(adj.size());
    adj.push_back({});

    int n = int(adj.size());
    vector<string> ips(n);
    for (auto pp : id)
    {
        ips[pp.second] = pp.first;
    }

    for (int i = 0; i < int(ns.size()); i++)
    {
        int to = id[ns[i]], cost = costs[i];
        adj[n - 1].push_back({to, cost});
        adj[to].push_back({n - 1, cost});
    }
    vector<long long> d(n, INF);
    vector<int> nxt(n);
    bellmanFord(id[src], d, nxt);
    for (auto pp : id)
    {
        cout << src << ", " << pp.first << ", " << d[pp.second] << ", " << ips[nxt[pp.second]] << endl;
    }
    cout << endl;

    for (int i = 0; i < int(ns.size()); i++)
    {
        int to = id[ns[i]];
        adj[to].pop_back();
    }
    adj.pop_back();
    id.erase(ip);
}

int main()
{
    ifstream fin("Topology.txt");

    {
        int cur_id = 0;
        string s;
        while (fin >> s)
        {
            int from = (id.count(s) ? id[s] : id[s] = cur_id++);
            if (cur_id > (int)adj.size())
                adj.push_back({});
            int n;
            fin >> n;
            for (int i = 0; i < n; i++)
            {
                int cost;
                fin >> s >> cost;
                int to = (id.count(s) ? id[s] : id[s] = cur_id++);
                if (cur_id > (int)adj.size())
                    adj.push_back({});
                adj[from].push_back({to, cost});
                adj[to].push_back({from, cost});
            }
            fin >> s;
            assert(s == "End");
        }
    }

    distanceFinder("10.1.2.10");
    updateRouterCost("10.1.3.10", "10.1.4.10", 10, "10.1.2.10");
    addRouter("10.1.6.10", {"10.1.5.10", "10.1.4.10"}, {3, 4}, "10.1.2.10");

    return 0;
}
