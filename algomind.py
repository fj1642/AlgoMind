
import time
import tracemalloc
import heapq
import random
import ipywidgets as widgets
from IPython.display import display

# --- 1. Algorithm Metadata (Fixed Syntax Warnings with Raw Strings) ---
algorithms = [
    {"name": "Merge Sort", "type": "sorting", "class": "P", "time": "O(n log n)", "space": "O(n)"},
    {"name": "Quick Sort", "type": "sorting", "class": "P", "time": "O(n log n)", "space": "O(log n)"},
    {"name": "Dijkstra", "type": "graph", "class": "P", "time": r"O(V \log V + E)", "space": "O(V)"},
    {"name": "Backtracking (Permutations)", "type": "combinatorial", "class": "NP", "time": "O(n!)", "space": "O(n)"},
    {"name": "Subset Sum (DP)", "type": "dp", "class": "NP-Complete", "time": r"O(n \cdot \text{sum})", "space": r"O(n \cdot \text{sum})"},
    {"name": "Hamiltonian Path (Naive)", "type": "optimization", "class": "NP-Hard", "time": "O(n!)", "space": "O(n)"}
]

# --- 2. Algorithm Implementations ---

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr)//2]
    return quick_sort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quick_sort([x for x in arr if x > pivot])

def dijkstra(graph_data, start=0):
    graph, n = graph_data
    dist = {node: float('inf') for node in range(n)}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]: continue
        for neighbor, weight in graph.get(node, []):
            if dist[neighbor] > d + weight:
                dist[neighbor] = d + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))
    return dist

def subset_sum(data):
    nums, target = data
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]
    return dp[target]

def backtracking_perm(arr):
    if len(arr) <= 1: return [arr]
    res = []
    for i in range(len(arr)):
        m = arr[i]
        rem = arr[:i] + arr[i+1:]
        for p in backtracking_perm(rem):
            res.append([m] + p)
    return res

def hamiltonian_path_naive(graph_data):
    graph, n = graph_data
    def solve(curr, visited):
        if len(visited) == n: return True
        for neighbor, _ in graph.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                if solve(neighbor, visited): return True
                visited.remove(neighbor)
        return False
    # Start from node 0 as a simplification
    return solve(0, {0})

# --- 3. Robust Classification Engine ---

def classify_problem(desc):
    """
    Checks keywords in order of specificity (Hardest/Most unique first).
    """
    desc = desc.lower()

    # Priority 1: Optimization (Hamiltonian / TSP)
    if any(k in desc for k in ["hamiltonian", "tsp", "salesman", "visit all", "visit every", "cycle"]):
        return "optimization", "NP-Hard"

    # Priority 2: DP (Subset Sum / Knapsack)
    if any(k in desc for k in ["subset", "sum", "knapsack", "partition", "target value"]):
        return "dp", "NP-Complete"

    # Priority 3: Combinatorial (Backtracking)
    if any(k in desc for k in ["permutation", "arrangement", "combinations", "backtrack"]):
        return "combinatorial", "NP"

    # Priority 4: Graph (Shortest Path)
    if any(k in desc for k in ["shortest path", "route", "dijkstra", "distance", "navigation", "map"]):
        return "graph", "P"

    # Priority 5: Sorting
    if any(k in desc for k in ["sort", "order", "alphabetical", "sequence", "smallest to largest"]):
        return "sorting", "P"

    return "sorting", "P" # Fallback

# --- 4. Utilities ---

def get_function(name):
    mapping = {
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Dijkstra": dijkstra,
        "Subset Sum (DP)": subset_sum,
        "Backtracking (Permutations)": backtracking_perm,
        "Hamiltonian Path (Naive)": hamiltonian_path_naive
    }
    return mapping.get(name)

def generate_data(problem_type, n):
    if problem_type == "sorting":
        return [random.randint(1, 10000) for _ in range(n)]
    elif problem_type in ["graph", "optimization"]:
        graph = {i: [] for i in range(n)}
        for i in range(n):
            for _ in range(2): # 2 edges per node
                graph[i].append((random.randint(0, n-1), random.randint(1, 10)))
        return graph, n
    elif problem_type == "dp":
        # Ensure target sum isn't too large for the DP table
        return [random.randint(1, 20) for _ in range(min(n, 20))], 100
    elif problem_type == "combinatorial":
        return list(range(min(n, 8))) # Factorial limit
    return None

def measure(func, data):
    tracemalloc.start()
    start = time.perf_counter()
    try:
        func(data)
        success = True
    except Exception:
        success = False
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"time": end - start, "memory": peak / 1024 / 1024, "success": success}

def select_algorithm(desc, n):
    prob_type, prob_class = classify_problem(desc)
    candidates = [a for a in algorithms if a["type"] == prob_type]

    best = None
    best_time = float("inf")

    for algo in candidates:
        func = get_function(algo["name"])
        if not func: continue

        test_data = generate_data(prob_type, n)
        perf = measure(func, test_data)

        if perf["success"] and perf["time"] < best_time:
            best_time = perf["time"]
            best = (algo, perf["time"], perf["memory"])

    return best

# --- 5. Interface ---

desc_box = widgets.Text(placeholder='e.g., find a hamiltonian path', description='Problem:')
size_box = widgets.IntSlider(value=10, min=5, max=500, step=5, description='Size:')
button = widgets.Button(description="Analyze & Select", button_style='info')
output = widgets.Output()

def on_click(b):
    output.clear_output()
    with output:
        if not desc_box.value:
            print("Please enter a problem description.")
            return

        print(f"Detecting problem type...")
        result = select_algorithm(desc_box.value, size_box.value)

        if result:
            algo, t, mem = result
            print(f"✅ RECOMMENDED: {algo['name']}")
            print("-" * 35)
            print(f"Complexity: {algo['class']} | {algo['time']}")
            print(f"Benchmarked Time: {t:.6f}s")
            print(f"Peak Memory: {mem:.4f} MB")
        else:
            print("Could not match an algorithm to that description.")

button.on_click(on_click)
display(desc_box, size_box, button, output)
