"""3차 시험 모의 문제 채점. 연습 파일(mac · judge · summary · account · safe · tally)이나 풀이를 README 표대로 검사한다.

    python3 check.py            # 내가 쓴 연습 파일 검사
    python3 check.py --solution # 풀이/solution.py 검사 (풀이가 표와 맞는지)

이 파일은 채점용이라 import를 쓴다. 시험 답에는 import를 쓰지 않는다.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CROSS = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
X = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
DATA = {
    "filters": {"size_3": {"cross": CROSS, "x": X}},
    "patterns": {
        "size_3_0": {"input": CROSS, "expected": "+"},
        "size_3_1": {"input": X, "expected": " X "},
        "size_3_2": {"input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "expected": "cross"},
        "size_5_0": {"input": [[0] * 5 for _ in range(5)], "expected": "x"},
    },
}


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(name, fn):
    try:
        ok, got = fn()
    except NotImplementedError:
        ok, got = False, "아직 안 씀"
    except Exception as e:  # noqa: BLE001
        ok, got = False, f"{type(e).__name__}: {e}"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {got}"))
    return ok


def expect_error(f):
    try:
        f()
    except ValueError:
        return True, "ValueError"
    return False, "ValueError가 안 남"


def main():
    sol = "--solution" in sys.argv
    p = lambda f: os.path.join(HERE, "풀이", "solution.py") if sol else os.path.join(HERE, f)
    m1, m2, m3 = load(p("mac.py")), load(p("judge.py")), load(p("summary.py"))
    results = [
        run("1-1 mac 2x2", lambda: (m1.mac([[1, 2], [3, 4]], [[1, 0], [0, 1]]) == 5, None)),
        run("1-2 mac cross·cross", lambda: (m1.mac(CROSS, CROSS) == 5, None)),
        run("1-3 mac float", lambda: (m1.mac([[0.5, 0.5], [0.5, 0.5]], [[1, 1], [1, 1]]) == 2.0, None)),
        run("1-4 mac 크기 오류", lambda: expect_error(lambda: m1.mac([[1, 2, 3]], [[1, 2, 3]]))),
        run("2-1 judge CROSS", lambda: (m2.judge(CROSS, CROSS, X) == "Cross", m2.judge(CROSS, CROSS, X))),
        run("2-2 judge X", lambda: (m2.judge(X, CROSS, X) == "X", m2.judge(X, CROSS, X))),
        run("2-3 judge 가운데만", lambda: (m2.judge([[0, 0, 0], [0, 1, 0], [0, 0, 0]], CROSS, X) == "UNDECIDED", None)),
        run("2-4 judge epsilon", lambda: (m2.judge([[0.3, 0.1, 0.0], [0.2, 0.0, 0.0], [0.0, 0.0, 0.0]], CROSS, X) == "UNDECIDED", None)),
    ]
    want = {"total": 4, "pass": 2, "fail": 2, "fails": ["size_3_2", "size_5_0"]}
    results.append(run("3-1 summarize", lambda: (m3.summarize(DATA) == want, m3.summarize(DATA))))

    # 문제 5~7 (README 4-2절, 1 · 2주차 범위, 짐작으로 만든 연습)
    m5, m6, m7 = load(p("account.py")), load(p("safe.py")), load(p("tally.py"))

    def account_flow():
        a = m5.Account("kim", 100)
        got = (a.owner, a.deposit(50), a.withdraw(30), a.balance)
        return got == ("kim", 150, 120, 120), got

    results += [
        run("5-1 Account 넣고 빼기", account_flow),
        run("5-2 Account 기본 잔액 0", lambda: (m5.Account("lee").balance == 0, m5.Account("lee").balance)),
        run("5-3 Account 0 이하 넣기", lambda: expect_error(lambda: m5.Account("a").deposit(0))),
        run("5-4 Account 잔액보다 많이 빼기", lambda: expect_error(lambda: m5.Account("a", 10).withdraw(11))),
        run("5-5 Account 음수 시작", lambda: expect_error(lambda: m5.Account("a", -1))),
        run("6-1 to_int 숫자", lambda: (m6.to_int("42") == 42, m6.to_int("42"))),
        run("6-2 to_int 공백", lambda: (m6.to_int(" -7 ") == -7, m6.to_int(" -7 "))),
        run("6-3 to_int 글자 → 기본값", lambda: (m6.to_int("abc") == 0, m6.to_int("abc"))),
        run("6-4 to_int 소수 → 기본값", lambda: (m6.to_int("3.5", -1) == -1, m6.to_int("3.5", -1))),
        run("6-5 to_int None → 기본값", lambda: (m6.to_int(None, 9) == 9, m6.to_int(None, 9))),
    ]
    t_in = ["Cross", " x", "cross", "", "X", "  ", "cross"]
    t_want = {"total": 5, "counts": {"cross": 3, "x": 2}, "most": "cross"}
    results += [
        run("7-1 tally 세기", lambda: (m7.tally(t_in) == t_want, m7.tally(t_in))),
        run("7-2 tally 동점은 사전순", lambda: (m7.tally(["b", "a", "b", "a"])["most"] == "a", m7.tally(["b", "a", "b", "a"]))),
        run("7-3 tally 빈 목록", lambda: (m7.tally([]) == {"total": 0, "counts": {}, "most": None}, m7.tally([]))),
    ]
    print(f"\n{sum(results)}/{len(results)} 통과 · 문제 4 · 8(글 답)은 README 5절 답과 직접 맞춰 본다")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
