"""Mini NPU 심화 연습 — MAC 기반 2D 컨볼루션 · 판정 클래스 · data.json (짐작으로 만든 연습)

풀이 방법: practice.py의 pass 부분을 채운 뒤 `python check.py` 로 채점한다. (IDLE: check.py 열고 F5)
외부 라이브러리(import)는 사용하지 않는다. 파일 읽기 · 쓰기도 하지 않는다.
잘못된 입력이면 예외를 내지 말고 None(또는 문제에 적힌 값)을 돌려준다.
"""


# =============================================================================
# 문제 1. 2D 컨볼루션 함수 — MAC을 창(window)마다 반복한다
#   행렬은 2차원 리스트, 값은 int 또는 float. 직사각형일 수도 있다.
#   결과 행렬은 새 리스트로 돌려준다. (입력을 바꾸지 않는다, 줄끼리 같은 리스트를 공유하지 않는다)
# =============================================================================
def shape(m):
    """행렬의 (행 수, 열 수) 튜플을 돌려준다.

    리스트가 아니거나, 비었거나([] 또는 [[]]), 줄 길이가 서로 다르면 None.
    예) shape([[1, 2, 3], [4, 5, 6]]) → (2, 3)
        shape([[1, 2], [3]]) → None
    """
    if not isinstance(m, list) or len(m) == 0:
        return None
    cols = None
    for row in m:
        if not isinstance(row, list) or len(row) == 0:
            return None
        if cols is None:
            cols = len(row)
        elif len(row) != cols:
            return None
    return (len(m), cols)


def zeros(rows, cols):
    """rows × cols 크기의 0 행렬을 돌려준다. rows나 cols가 1보다 작으면 None.

    주의: 각 행은 서로 다른 리스트여야 한다.
    예) zeros(2, 3) → [[0, 0, 0], [0, 0, 0]]
    """
    if rows < 1 or cols < 1:
        return None
    return [[0] * cols for _ in range(rows)]


def mac(a, b):
    """모양이 같은 두 행렬의 같은 자리끼리 곱해 모두 더한다. 모양이 다르거나 잘못된 행렬이면 None.

    예) mac([[1, 2], [3, 4]], [[1, 0], [0, 1]]) → 5
        mac([[1, 2, 3]], [[1, 1, 1]]) → 6
    """
    sa = shape(a)
    if sa is None or sa != shape(b):
        return None
    total = 0
    for i in range(sa[0]):
        for j in range(sa[1]):
            total += a[i][j] * b[i][j]
    return total


def window(img, top, left, h, w):
    """img에서 (top, left)부터 h줄 × w칸을 잘라 새 행렬로 돌려준다.

    img가 잘못됐거나, h · w가 1보다 작거나, top · left가 음수이거나, img 밖으로 나가면 None.
    예) img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        window(img, 1, 1, 2, 2) → [[5, 6], [8, 9]]
        window(img, 2, 2, 2, 2) → None
    """
    s = shape(img)
    if s is None or h < 1 or w < 1 or top < 0 or left < 0:
        return None
    if top + h > s[0] or left + w > s[1]:
        return None
    result = []
    for i in range(top, top + h):
        result.append(img[i][left:left + w])
    return result


def pad(img, p):
    """img의 위 · 아래 · 왼쪽 · 오른쪽에 0을 p칸씩 두른 새 행렬. p가 음수이거나 img가 잘못됐으면 None.

    p = 0이면 같은 값의 새 행렬(복사본).
    예) pad([[1, 2], [3, 4]], 1) → [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
    """
    s = shape(img)
    if s is None or p < 0:
        return None
    result = zeros(s[0] + 2 * p, s[1] + 2 * p)
    for i in range(s[0]):
        for j in range(s[1]):
            result[i + p][j + p] = img[i][j]
    return result


def out_size(n, k, stride=1, padding=0):
    """한 변이 n인 입력에 한 변이 k인 커널을 쓸 때 출력 한 변의 길이.

    식: (n + 2 × padding − k) // stride + 1
    n · k · stride가 1보다 작거나, padding이 음수이거나, 커널이 (패딩한) 입력보다 크면 None.
    예) out_size(5, 3) → 3, out_size(5, 3, 2) → 2, out_size(5, 3, 1, 1) → 5, out_size(2, 3) → None
    """
    if n < 1 or k < 1 or stride < 1 or padding < 0:
        return None
    span = n + 2 * padding - k
    if span < 0:
        return None
    return span // stride + 1


def conv2d(img, kernel, stride=1, padding=0):
    """img에 kernel을 컨볼루션한 결과 행렬을 돌려준다. (커널은 뒤집지 않는다 — 딥러닝 방식)

    1) padding만큼 0을 두른다  2) 커널을 왼쪽 위부터 stride 칸씩 옮긴다
    3) 칸마다 mac(창, kernel)을 적는다. 출력 크기는 out_size와 같다.
    img · kernel이 잘못됐거나 출력 크기를 낼 수 없으면 None.
    예) conv2d([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, 1]]) → [[6, 8], [12, 14]]
        conv2d([[1, 0], [0, 0]], [[1, 2], [3, 4]]) → [[1]]   (뒤집으면 4가 된다)
    """
    si, sk = shape(img), shape(kernel)
    if si is None or sk is None:
        return None
    oh = out_size(si[0], sk[0], stride, padding)
    ow = out_size(si[1], sk[1], stride, padding)
    if oh is None or ow is None:
        return None
    src = pad(img, padding)
    result = []
    for i in range(oh):
        row = []
        for j in range(ow):
            row.append(mac(window(src, i * stride, j * stride, sk[0], sk[1]), kernel))
        result.append(row)
    return result


def flip(kernel):
    """커널을 180도 돌린 새 행렬(위아래 + 좌우 뒤집기). 수학의 '진짜 컨볼루션'은 이렇게 뒤집은 커널로 계산한다.

    잘못된 행렬이면 None.
    예) flip([[1, 2], [3, 4]]) → [[4, 3], [2, 1]]
    """
    s = shape(kernel)
    if s is None:
        return None
    result = []
    for i in range(s[0] - 1, -1, -1):
        row = []
        for j in range(s[1] - 1, -1, -1):
            row.append(kernel[i][j])
        result.append(row)
    return result


def relu(m):
    """음수를 0으로 바꾼 새 행렬. 잘못된 행렬이면 None.

    예) relu([[-1, 2], [0, -0.5]]) → [[0, 2], [0, 0]]
    """
    if shape(m) is None:
        return None
    return [[v if v > 0 else 0 for v in row] for row in m]


def max_pool(m, size=2):
    """size × size 칸마다 가장 큰 값 하나를 남긴다. (stride = size, 끝에 남는 줄 · 칸은 버린다)

    size가 1보다 작거나 m보다 크거나 m이 잘못됐으면 None.
    예) m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        max_pool(m, 2) → [[6, 8], [14, 16]]
        max_pool(m, 3) → [[11]]
    """
    s = shape(m)
    if s is None or size < 1 or size > s[0] or size > s[1]:
        return None
    result = []
    for bi in range(s[0] // size):
        row = []
        for bj in range(s[1] // size):
            best = m[bi * size][bj * size]
            for i in range(bi * size, bi * size + size):
                for j in range(bj * size, bj * size + size):
                    if m[i][j] > best:
                        best = m[i][j]
            row.append(best)
        result.append(row)
    return result


# =============================================================================
# 문제 2. ConvClassifier — 필터 여러 개로 패턴을 판정하는 클래스 (딕셔너리 · 리스트)
#   점수 = conv2d(패턴, 필터) 결과에서 가장 큰 값 (stride 1, padding 0)
#   → 그림 어디에든 그 모양이 있으면 점수가 높다
# =============================================================================
def normalize_label(raw):
    """라벨을 정리한다: 앞뒤 공백을 지우고 소문자로. '+'는 'cross'로 바꾼다.

    문자열이 아니거나 정리한 뒤 빈 문자열이면 None.
    예) ' Cross ' → 'cross', '+' → 'cross', 'X' → 'x', '' → None, None → None
    """
    if not isinstance(raw, str):
        return None
    s = raw.strip().lower()
    if s == "":
        return None
    if s == "+":
        return "cross"
    return s


class ConvClassifier:
    """필터와 패턴을 이름으로 저장하고, 컨볼루션 점수로 판정 · 집계한다."""

    def __init__(self, eps=1e-9):
        self.eps = eps
        self.filters = {}    # {필터 이름(정리된 라벨): 커널}
        self.patterns = {}   # {패턴 이름: {"data": 2차원 리스트, "expected": 정리된 라벨}}

    def add_filter(self, name, kernel):
        """필터를 저장하고 True. 다음 중 하나라도 해당하면 저장하지 않고 False.

        - normalize_label(name)이 None
        - 정리한 이름이 이미 있음
        - kernel이 잘못된 행렬 (shape가 None)
        저장할 때 이름은 정리된 라벨로 쓴다.
        """
        label = normalize_label(name)
        if label is None or label in self.filters or shape(kernel) is None:
            return False
        self.filters[label] = kernel
        return True

    def add_pattern(self, name, data, expected):
        """패턴을 저장하고 True. 다음 중 하나라도 해당하면 저장하지 않고 False.

        - 이미 같은 이름이 있음
        - normalize_label(expected)가 None이거나, 그런 이름의 필터가 없음
        - data가 잘못된 행렬이거나, 어떤 필터보다 행 · 열이 작음 (컨볼루션을 못 함)
        expected는 정리된 라벨로 저장한다.
        """
        if name in self.patterns:
            return False
        label = normalize_label(expected)
        if label is None or label not in self.filters:
            return False
        s = shape(data)
        if s is None:
            return False
        for kernel in self.filters.values():
            sk = shape(kernel)
            if s[0] < sk[0] or s[1] < sk[1]:
                return False
        self.patterns[name] = {"data": data, "expected": label}
        return True

    def load_data(self, data):
        """data.json을 읽은 dict에서 필터와 패턴을 한 번에 넣는다.

        data = {"filters": {이름: 커널, ...}, "patterns": [{"id": ..., "input": ..., "expected": ...}, ...]}
        - 필터를 먼저 모두 넣고, 패턴을 목록 순서대로 넣는다 (add_filter / add_pattern 사용).
        - 패턴 항목이 dict가 아니거나 id · input · expected 중 하나라도 없으면 건너뛴다.
        - data에 "filters"나 "patterns"가 없으면 빈 것으로 본다.
        돌려줄 값: {"filters": 넣은 필터 수, "patterns": 넣은 패턴 수, "skipped": [못 넣은 패턴 id]}
          (id가 없는 항목은 "#번호"(0부터)로 적는다)
        """
        if not isinstance(data, dict):
            data = {}
        added_f = 0
        for name, kernel in data.get("filters", {}).items():
            if self.add_filter(name, kernel):
                added_f += 1
        added_p = 0
        skipped = []
        for index, item in enumerate(data.get("patterns", [])):
            if not isinstance(item, dict) or "id" not in item:
                skipped.append("#" + str(index))
                continue
            if "input" not in item or "expected" not in item:
                skipped.append(item["id"])
                continue
            if self.add_pattern(item["id"], item["input"], item["expected"]):
                added_p += 1
            else:
                skipped.append(item["id"])
        return {"filters": added_f, "patterns": added_p, "skipped": skipped}

    def scores(self, name):
        """패턴 하나의 필터별 점수 {필터 이름: 점수}. 없는 이름이면 None.

        점수 = conv2d(패턴, 커널) 결과에서 가장 큰 값.
        """
        if name not in self.patterns:
            return None
        data = self.patterns[name]["data"]
        result = {}
        for label, kernel in self.filters.items():
            fm = conv2d(data, kernel)
            best = fm[0][0]
            for row in fm:
                for v in row:
                    if v > best:
                        best = v
            result[label] = best
        return result

    def classify(self, name):
        """패턴 하나를 판정해 아래 딕셔너리를 돌려준다. 없는 이름이면 None.

        {"name": 이름, "scores": {필터: 점수}, "verdict": 판정, "expected": 정답 라벨, "passed": 판정 == 정답}
        판정: 가장 높은 점수의 필터 이름. 1등과 2등의 차이가 eps보다 작으면 'UNDECIDED'.
              필터가 하나뿐이면 그 이름.
        """
        sc = self.scores(name)
        if sc is None:
            return None
        ranked = sorted(sc.items(), key=lambda kv: kv[1], reverse=True)
        verdict = ranked[0][0]
        if len(ranked) >= 2 and abs(ranked[0][1] - ranked[1][1]) < self.eps:
            verdict = "UNDECIDED"
        expected = self.patterns[name]["expected"]
        return {"name": name, "scores": sc, "verdict": verdict,
                "expected": expected, "passed": verdict == expected}

    def classify_all(self):
        """모든 패턴의 classify 결과를 저장한 순서대로 리스트로 돌려준다."""
        results = []
        for name in self.patterns:
            results.append(self.classify(name))
        return results

    def summary(self):
        """(전체 개수, 통과 개수, 실패 개수) 튜플."""
        results = self.classify_all()
        passed = 0
        for r in results:
            if r["passed"]:
                passed += 1
        return (len(results), passed, len(results) - passed)

    def get_failed(self):
        """실패한 패턴의 이름만 저장한 순서대로 리스트로 돌려준다."""
        names = []
        for r in self.classify_all():
            if not r["passed"]:
                names.append(r["name"])
        return names

    def count_by_verdict(self):
        """판정별 개수 {필터 이름마다: 개수, 'UNDECIDED': 개수}. 0개인 키도 반드시 넣는다."""
        counts = {}
        for label in self.filters:
            counts[label] = 0
        counts["UNDECIDED"] = 0
        for r in self.classify_all():
            counts[r["verdict"]] += 1
        return counts


if __name__ == "__main__":
    c = ConvClassifier()
    c.add_filter("cross", [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    c.add_filter("x", [[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    c.add_pattern("p1", [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], "+")
    print(c.classify("p1"))
