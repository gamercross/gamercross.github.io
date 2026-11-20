# README 5절의 풀이 (문제 1~3 한 파일)
EPS = 1e-9


def mac(pattern, filt):
    n = len(pattern)
    if n == 0 or len(filt) != n:
        raise ValueError("size mismatch")
    for row_p, row_f in zip(pattern, filt):
        if len(row_p) != n or len(row_f) != n:
            raise ValueError("not square")
    total = 0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def judge(pattern, cross, x, eps=EPS):
    a = mac(pattern, cross)
    b = mac(pattern, x)
    if abs(a - b) < eps:
        return "UNDECIDED"
    return "Cross" if a > b else "X"


def normalize(label):
    s = str(label).strip().lower()
    if s in ("+", "cross"):
        return "Cross"
    if s == "x":
        return "X"
    raise ValueError("unknown label: " + str(label))


def summarize(data):
    filters = data.get("filters", {})
    patterns = data.get("patterns", {})
    passed = 0
    fails = []
    for key, case in patterns.items():
        try:
            n = key.split("_")[1]
            f = filters["size_" + n]
            ok = judge(case["input"], f["cross"], f["x"]) == normalize(case["expected"])
        except (KeyError, IndexError, ValueError):
            ok = False
        if ok:
            passed += 1
        else:
            fails.append(key)
    return {"total": len(patterns), "pass": passed, "fail": len(fails), "fails": sorted(fails)}


# ---- 문제 5~7 (README 4-2절, 짐작으로 만든 연습) ----

class Account:
    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("balance must be >= 0")
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if amount > self.balance:
            raise ValueError("not enough balance")
        self.balance -= amount
        return self.balance


def to_int(text, default=0):
    try:
        return int(str(text).strip())
    except ValueError:
        return default


def tally(items):
    counts = {}
    for item in items:
        word = str(item).strip().lower()
        if word == "":
            continue
        counts[word] = counts.get(word, 0) + 1
    most = None
    for word in sorted(counts):
        if most is None or counts[word] > counts[most]:
            most = word
    return {"total": sum(counts.values()), "counts": counts, "most": most}
