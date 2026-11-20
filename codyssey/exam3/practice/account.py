# 문제 5. 계좌 클래스 (짐작으로 만든 연습) — README 4-2절 문제 5
# 규칙: 파이썬 3, import 없이, 파일 읽기·쓰기 없이.


class Account:
    def __init__(self, owner, balance=0):
        raise NotImplementedError

    def deposit(self, amount):
        raise NotImplementedError

    def withdraw(self, amount):
        raise NotImplementedError
