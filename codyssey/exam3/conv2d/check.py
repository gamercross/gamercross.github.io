"""
심화 연습 채점기 (MAC 기반 2D 컨볼루션 · ConvClassifier · data.json)

IDLE  : 이 파일을 열고 F5. practice.py와 data.json을 채점한다.
터미널: python3 check.py             문제 1~3 모두
        python3 check.py 1 3         골라서
        python3 check.py --solution  풀이/solution.py와 풀이/data.json을 채점 (채점기 확인용)

문제마다 (통과 수 / 전체 수) × 100 점, 총점은 문제별 평균이다.
data.json(문제 3)은 내 코드가 아니라 풀이의 ConvClassifier로 검사한다.
이 파일은 채점용이라 import를 쓴다. 답에는 import를 쓰지 않는다.
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHOW_DETAIL = True      # False 로 바꾸면 틀린 케이스 이름을 숨긴다 (진짜 시험처럼)

CROSS = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
X = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
P_CROSS = [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
P_X = [[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]]
P_DOT = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
M44 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
M33 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


# ---------------------------------------------------------------------------
# 도우미
# ---------------------------------------------------------------------------
def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def same(got, want):
    if is_num(got) and is_num(want):
        return abs(got - want) < 1e-9
    if isinstance(want, (list, tuple)):
        return isinstance(got, type(want)) and len(got) == len(want) and all(
            same(g, w) for g, w in zip(got, want))
    if isinstance(want, dict):
        return isinstance(got, dict) and set(got) == set(want) and all(same(got[k], want[k]) for k in want)
    return type(got) is type(want) and got == want


def run_case(thunk, want, hint=True):
    try:
        got = thunk()
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}" + ("  (예외 대신 None을 돌려줘야 한다)" if hint else "")
    if callable(want):
        ok = bool(want(got))
        return ok, "" if ok else f"돌려준 값 {got!r}"
    if same(got, want):
        return True, ""
    return False, f"기대 {want!r}, 돌려준 값 {got!r}"


def load(path):
    spec = importlib.util.spec_from_file_location("mod_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def untouched(fn, arg):
    """fn(arg)가 arg를 바꾸지 않는지 본다."""
    before = json.dumps(arg)
    if fn(arg) is None:
        return False
    return json.dumps(arg) == before


def rows_independent(m):
    if not isinstance(m, list) or len(m) < 2:
        return False
    m[0][0] = 999
    return m[1][0] != 999


# ---------------------------------------------------------------------------
# 문제 1
# ---------------------------------------------------------------------------
def cases_p1(m):
    return [
        ("shape 2×3", lambda: m.shape([[1, 2, 3], [4, 5, 6]]), (2, 3)),
        ("shape 1×1", lambda: m.shape([[1]]), (1, 1)),
        ("shape 빈 리스트", lambda: m.shape([]), None),
        ("shape [[]]", lambda: m.shape([[]]), None),
        ("shape 줄 길이 다름", lambda: m.shape([[1, 2], [3]]), None),
        ("shape 리스트 아님", lambda: m.shape("abc"), None),
        ("zeros 2×3", lambda: m.zeros(2, 3), [[0, 0, 0], [0, 0, 0]]),
        ("zeros 0", lambda: m.zeros(0, 3), None),
        ("zeros 줄이 서로 따로", lambda: rows_independent(m.zeros(3, 3)), True),
        ("mac 2×2", lambda: m.mac([[1, 2], [3, 4]], [[1, 0], [0, 1]]), 5),
        ("mac 직사각형", lambda: m.mac([[1, 2, 3]], [[1, 1, 1]]), 6),
        ("mac 십자가끼리", lambda: m.mac(CROSS, CROSS), 5),
        ("mac float", lambda: m.mac([[0.1, 0.2]], [[1, 1]]), 0.3),
        ("mac 모양 다름", lambda: m.mac([[1, 2]], [[1], [2]]), None),
        ("mac 빈 입력", lambda: m.mac([], []), None),
        ("window 가운데 2×2", lambda: m.window(M33, 1, 1, 2, 2), [[5, 6], [8, 9]]),
        ("window 한 줄", lambda: m.window(M33, 0, 0, 1, 3), [[1, 2, 3]]),
        ("window 밖으로", lambda: m.window(M33, 2, 2, 2, 2), None),
        ("window 음수", lambda: m.window(M33, -1, 0, 2, 2), None),
        ("window h 0", lambda: m.window(M33, 0, 0, 0, 2), None),
        ("window 원본 안 바뀜", lambda: (lambda a: (lambda w: (w[0].__setitem__(0, 0), a[1][1] == 5)[1])(m.window(a, 1, 1, 2, 2)))([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), True),
        ("pad 1칸", lambda: m.pad([[1, 2], [3, 4]], 1),
         [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]),
        ("pad 직사각형", lambda: m.pad([[1, 2, 3]], 1), [[0, 0, 0, 0, 0], [0, 1, 2, 3, 0], [0, 0, 0, 0, 0]]),
        ("pad 0칸은 복사본", lambda: (lambda a: (lambda b: b == a and b is not a and b[0] is not a[0])(m.pad(a, 0)))([[1, 2], [3, 4]]), True),
        ("pad 음수", lambda: m.pad([[1]], -1), None),
        ("out_size 기본", lambda: m.out_size(5, 3), 3),
        ("out_size stride 2", lambda: m.out_size(5, 3, 2), 2),
        ("out_size padding 1", lambda: m.out_size(5, 3, 1, 1), 5),
        ("out_size 나머지 버림", lambda: m.out_size(4, 3, 2), 1),
        ("out_size 커널이 큼", lambda: m.out_size(2, 3), None),
        ("out_size stride 0", lambda: m.out_size(5, 3, 0), None),
        ("out_size padding 음수", lambda: m.out_size(5, 3, 1, -1), None),
        ("conv2d 예시", lambda: m.conv2d(M33, [[1, 0], [0, 1]]), [[6, 8], [12, 14]]),
        ("conv2d 커널 안 뒤집음", lambda: m.conv2d([[1, 0], [0, 0]], [[1, 2], [3, 4]]), [[1]]),
        ("conv2d stride 2", lambda: m.conv2d(M44, [[1, 1], [1, 1]], 2), [[14, 22], [46, 54]]),
        ("conv2d padding 1", lambda: m.conv2d([[1] * 3 for _ in range(3)], [[1] * 3 for _ in range(3)], 1, 1),
         [[4, 6, 4], [6, 9, 6], [4, 6, 4]]),
        ("conv2d 직사각형", lambda: m.conv2d([[1, 2, 3], [4, 5, 6]], [[1, 1]]), [[3, 5], [9, 11]]),
        ("conv2d 십자가 5×5 가운데", lambda: m.conv2d(P_CROSS, CROSS)[1][1], 5),
        ("conv2d 커널이 큼", lambda: m.conv2d([[1, 2], [3, 4]], CROSS), None),
        ("conv2d 잘못된 커널", lambda: m.conv2d(M33, [[1], [1, 2]]), None),
        ("flip 2×2", lambda: m.flip([[1, 2], [3, 4]]), [[4, 3], [2, 1]]),
        ("flip 한 줄", lambda: m.flip([[1, 2, 3]]), [[3, 2, 1]]),
        ("flip 원본 안 바뀜", lambda: untouched(m.flip, [[1, 2], [3, 4]]), True),
        ("flip 잘못된 행렬", lambda: m.flip([]), None),
        ("relu 예시", lambda: m.relu([[-1, 2], [0, -0.5]]), [[0, 2], [0, 0]]),
        ("relu 원본 안 바뀜", lambda: untouched(m.relu, [[-1, 2], [3, -4]]), True),
        ("relu 잘못된 행렬", lambda: m.relu([[1], [1, 2]]), None),
        ("max_pool 2", lambda: m.max_pool(M44, 2), [[6, 8], [14, 16]]),
        ("max_pool 3 (남는 칸 버림)", lambda: m.max_pool(M44, 3), [[11]]),
        ("max_pool 5×5에 2", lambda: m.max_pool([[i * 5 + j for j in range(5)] for i in range(5)], 2), [[6, 8], [16, 18]]),
        ("max_pool 음수만", lambda: m.max_pool([[-1, -2], [-3, -4]], 2), [[-1]]),
        ("max_pool size 0", lambda: m.max_pool(M44, 0), None),
        ("max_pool size 너무 큼", lambda: m.max_pool(M44, 5), None),
    ]


# ---------------------------------------------------------------------------
# 문제 2
# ---------------------------------------------------------------------------
def make(m, filters=(("cross", CROSS), ("x", X))):
    c = m.ConvClassifier()
    for name, k in filters:
        c.add_filter(name, k)
    return c


def cases_p2(m):
    def base():
        c = make(m)
        c.add_pattern("p_cross", P_CROSS, "+")
        c.add_pattern("p_x", P_X, " X ")
        c.add_pattern("p_dot", P_DOT, "cross")
        return c

    bad_data = {
        "filters": {"Cross": CROSS, "x": X, "": X},
        "patterns": [
            {"id": "a", "input": P_CROSS, "expected": "+"},
            {"id": "b", "input": P_X},
            "이건 dict가 아니다",
            {"id": "c", "input": P_X, "expected": "o"},
            {"input": P_X, "expected": "x"},
            {"id": "a", "input": P_X, "expected": "x"},
            {"id": "d", "input": [[1, 0], [0, 1]], "expected": "x"},
            {"id": "e", "input": P_X, "expected": "x"},
        ],
    }

    return [
        ("normalize ' Cross '", lambda: m.normalize_label(" Cross "), "cross"),
        ("normalize '+'", lambda: m.normalize_label("+"), "cross"),
        ("normalize 'X'", lambda: m.normalize_label("X"), "x"),
        ("normalize 'LINE'", lambda: m.normalize_label("LINE"), "line"),
        ("normalize 빈 글", lambda: m.normalize_label(""), None),
        ("normalize 공백만", lambda: m.normalize_label("   "), None),
        ("normalize None", lambda: m.normalize_label(None), None),
        ("normalize 숫자", lambda: m.normalize_label(3), None),
        ("add_filter 성공", lambda: m.ConvClassifier().add_filter("Cross", CROSS), True),
        ("add_filter 이름 정리해 저장", lambda: (lambda c: (c.add_filter(" Cross ", CROSS), list(c.filters)))(m.ConvClassifier()), (True, ["cross"])),
        ("add_filter 겹친 이름", lambda: (lambda c: c.add_filter("CROSS", X))(make(m)), False),
        ("add_filter 잘못된 커널", lambda: m.ConvClassifier().add_filter("a", [[1], [1, 2]]), False),
        ("add_filter 이름 없음", lambda: m.ConvClassifier().add_filter(None, CROSS), False),
        ("add_pattern 성공", lambda: make(m).add_pattern("p", P_CROSS, "+"), True),
        ("add_pattern 정답 정리해 저장", lambda: (lambda c: (c.add_pattern("p", P_X, " X "), c.patterns["p"]["expected"]))(make(m)), (True, "x")),
        ("add_pattern 겹친 이름", lambda: (lambda c: (c.add_pattern("p", P_CROSS, "+"), c.add_pattern("p", P_X, "x")))(make(m)), (True, False)),
        ("add_pattern 없는 필터 이름", lambda: make(m).add_pattern("p", P_CROSS, "o"), False),
        ("add_pattern 정답 None", lambda: make(m).add_pattern("p", P_CROSS, None), False),
        ("add_pattern 필터보다 작음", lambda: make(m).add_pattern("p", [[1, 0], [0, 1]], "x"), False),
        ("add_pattern 잘못된 행렬", lambda: make(m).add_pattern("p", [[1, 0, 0], [1]], "x"), False),
        ("load_data 정상", lambda: m.ConvClassifier().load_data(
            {"filters": {"cross": CROSS, "x": X}, "patterns": [{"id": "a", "input": P_CROSS, "expected": "+"}]}),
         {"filters": 2, "patterns": 1, "skipped": []}),
        ("load_data 잘못된 항목 건너뜀", lambda: m.ConvClassifier().load_data(bad_data),
         {"filters": 2, "patterns": 2, "skipped": ["b", "#2", "c", "#4", "a", "d"]}),
        ("load_data 빈 dict", lambda: m.ConvClassifier().load_data({}), {"filters": 0, "patterns": 0, "skipped": []}),
        ("scores 십자가 패턴", lambda: base().scores("p_cross"), {"cross": 5, "x": 3}),
        ("scores X 패턴", lambda: base().scores("p_x"), {"cross": 3, "x": 5}),
        ("scores 없는 이름", lambda: base().scores("nope"), None),
        ("classify 십자가", lambda: base().classify("p_cross"),
         {"name": "p_cross", "scores": {"cross": 5, "x": 3}, "verdict": "cross", "expected": "cross", "passed": True}),
        ("classify 동점 UNDECIDED", lambda: base().classify("p_dot")["verdict"], "UNDECIDED"),
        ("classify 동점은 FAIL", lambda: base().classify("p_dot")["passed"], False),
        ("classify 필터 하나", lambda: (lambda c: (c.add_pattern("p", P_X, "cross"), c.classify("p")["verdict"])[1])(make(m, (("cross", CROSS),))), "cross"),
        ("classify 없는 이름", lambda: base().classify("nope"), None),
        ("classify_all 순서", lambda: [r["name"] for r in base().classify_all()], ["p_cross", "p_x", "p_dot"]),
        ("summary", lambda: base().summary(), (3, 2, 1)),
        ("get_failed", lambda: base().get_failed(), ["p_dot"]),
        ("count_by_verdict 0개 키 포함", lambda: (lambda c: (c.add_pattern("q", P_CROSS, "+"), c.count_by_verdict())[1])(make(m)),
         {"cross": 1, "x": 0, "UNDECIDED": 0}),
        ("count_by_verdict 셋", lambda: base().count_by_verdict(), {"cross": 1, "x": 1, "UNDECIDED": 1}),
        ("빈 분류기 summary", lambda: m.ConvClassifier().summary(), (0, 0, 0)),
    ]


# ---------------------------------------------------------------------------
# 문제 3: data.json (풀이의 ConvClassifier로 검사)
# ---------------------------------------------------------------------------
def cases_p3(ref, path):
    state = {}

    def parsed():
        if not os.path.exists(path):
            return "파일 없음: " + path
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            return "빈 파일"
        try:
            state["data"] = json.loads(text)
        except ValueError as e:
            return "JSON 문법 오류: " + str(e)
        return True

    def d():
        if "data" not in state:
            raise ValueError("data.json을 읽지 못함")
        return state["data"]

    def norm(name):
        return ref.normalize_label(name)

    def kernels_ok():
        fs = d()["filters"]
        return all(ref.shape(k) == (3, 3) and all(is_num(v) for row in k for v in row) for k in fs.values())

    def patterns_ok():
        return all(isinstance(p, dict) and ref.shape(p.get("input")) == (5, 5)
                   and all(is_num(v) for row in p["input"] for v in row) for p in d()["patterns"])

    def ids_unique():
        ids = [p.get("id") for p in d()["patterns"]]
        return all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids)

    def every_filter_used():
        used = {norm(p.get("expected")) for p in d()["patterns"]}
        return all(norm(n) in used for n in d()["filters"])

    def loaded():
        c = ref.ConvClassifier()
        state["clf"] = c
        return c.load_data(d())

    def all_pass():
        c = state.get("clf") or ref.ConvClassifier()
        if "clf" not in state:
            c.load_data(d())
        total, passed, failed = c.summary()
        return failed == 0 and total > 0 or c.get_failed()

    return [
        ("data.json 읽기 (JSON 문법)", parsed, True),
        ("맨 위가 dict이고 filters(dict) · patterns(list)", lambda: isinstance(d(), dict) and isinstance(d().get("filters"), dict) and isinstance(d().get("patterns"), list), True),
        ("필터 2개 이상, cross와 x 포함", lambda: len(d()["filters"]) >= 2 and {"cross", "x"} <= {norm(n) for n in d()["filters"]}, True),
        ("필터는 모두 3×3 숫자", kernels_ok, True),
        ("패턴 6개 이상", lambda: len(d()["patterns"]) >= 6, True),
        ("패턴은 모두 dict, input은 5×5 숫자", patterns_ok, True),
        ("id는 글자이고 겹치지 않음", ids_unique, True),
        ("expected에 '+' 표기가 하나 이상", lambda: any(isinstance(p.get("expected"), str) and p["expected"].strip() == "+" for p in d()["patterns"]), True),
        ("필터마다 expected로 한 번 이상 쓰임", every_filter_used, True),
        ("load_data에서 건너뛴 패턴 없음", lambda: (lambda r: r["skipped"] == [] and r["patterns"] == len(d()["patterns"]) or r)(loaded()), True),
        ("모든 패턴 PASS (UNDECIDED 없음)", all_pass, True),
    ]


# ---------------------------------------------------------------------------
# 실행
# ---------------------------------------------------------------------------
def grade(title, cases, hint=True):
    """None을 기대하는 케이스는 같은 함수의 다른 케이스를 하나라도 맞혀야 점수로 친다.
    (pass만 둔 빈 함수도 None을 돌려주기 때문)"""
    print(f"\n== {title} ==")
    results = []
    real_ok = set()
    for desc, thunk, want in cases:
        ok, why = run_case(thunk, want, hint)
        fn = desc.split()[0]
        results.append((desc, fn, want is None, ok, why))
        if ok and want is not None:
            real_ok.add(fn)
    passed = 0
    for desc, fn, wants_none, ok, why in results:
        if ok and wants_none and fn not in real_ok:
            ok, why = False, "None만 맞음 (함수를 아직 안 쓴 것 같다)"
        if ok:
            passed += 1
        elif SHOW_DETAIL:
            print(f"  FAIL  {desc}: {why}")
    score = round(passed * 100 / len(cases))
    print(f"  {passed}/{len(cases)} 통과 → {score}점")
    return score


def main(argv):
    sol = "--solution" in argv
    picks = {int(a) for a in argv if a.isdigit()}
    code_path = os.path.join(HERE, "풀이", "solution.py") if sol else os.path.join(HERE, "practice.py")
    data_path = os.path.join(HERE, "풀이", "data.json") if sol else os.path.join(HERE, "data.json")
    ref = load(os.path.join(HERE, "풀이", "solution.py"))
    try:
        mod = load(code_path)
    except Exception as e:  # noqa: BLE001
        print(f"{os.path.basename(code_path)} 불러오기 실패: {type(e).__name__}: {e}")
        mod = None

    with open(code_path, encoding="utf-8") as f:
        text = f.read()
    if "\nimport " in text or "\nfrom " in text:
        print("! 답 파일에 import가 있다 (시험에서는 쓰지 않는다)")

    scores = []
    if mod is not None and (not picks or 1 in picks):
        scores.append(grade("문제 1 · 2D 컨볼루션 함수 10개", cases_p1(mod)))
    if mod is not None and (not picks or 2 in picks):
        scores.append(grade("문제 2 · normalize_label + ConvClassifier", cases_p2(mod)))
    if not picks or 3 in picks:
        scores.append(grade("문제 3 · data.json 직접 쓰기", cases_p3(ref, data_path), hint=False))
    if scores:
        print(f"\n총점 (문제별 평균): {sum(scores) / len(scores):.1f}점")


if __name__ == "__main__":
    main(sys.argv[1:])
