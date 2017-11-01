import unittest
from contextlib import contextmanager
from io import StringIO

import sys

from Schaken import *


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def removews(s):
    return s.replace(" ","").replace("\t","").replace("\n","").lower()

class Test(unittest.TestCase):
    def setUp(self):
        self.p = Pion(WIT)
        self.t = Toren(ZWART)

    def test_schaakstuk(self):
        self.assertEqual(str(self.p), "Witte pion")
        self.assertEqual(str(self.t), "Zwarte toren")

    def test_Schaakbord_operaties(self):
        S = Schaakbord()
        S.plaats(self.p, (2, 1))
        S.plaats(self.t, (8, 1))
        self.assertEqual(S.waar_is(self.t), (8, 1))
        S.verplaats(self.p, (4, 1))
        self.assertEqual(S.stuk_op((2, 1)), None)
        self.assertEqual(S.stuk_op((4, 1)), self.p)

    def test_Schaakbord_begin(self):
        S = Schaakbord()
        S.zet_begin_positie()
        expected = """	a	b	c	d	e	f	g	h
8	Rb	Nb	Bb	Qb	Kb	Bb	Nb	Rb
7	Pb	Pb	Pb	Pb	Pb	Pb	Pb	Pb
6	.	.	.	.	.	.	.	.
5	.	.	.	.	.	.	.	.
4	.	.	.	.	.	.	.	.
3	.	.	.	.	.	.	.	.
2	Pw	Pw	Pw	Pw	Pw	Pw	Pw	Pw
1	Rw	Nw	Bw	Qw	Kw	Bw	Nw	Rw
"""
        self.assertEqual(removews(str(S)), removews(expected))

    def test_geldige_zetten_pion(self):
        S = Schaakbord()
        S.zet_begin_positie()
        p = S.stuk_op((2, 1))
        self.assertEqual(set(p.geldige_zetten(S)), set([(3, 1), (4, 1)]))
        S.verplaats(p, (4, 1))
        self.assertEqual(p.geldige_zetten(S), [(5, 1)])
        S.verplaats(p, (5, 1))
        self.assertEqual(p.geldige_zetten(S), [(6, 1)])
        S.verplaats(p, (6, 1))
        self.assertEqual(p.geldige_zetten(S), [(7, 2)])
        S.verplaats(p, (7, 2))
        self.assertEqual(set(p.geldige_zetten(S)), set([(8, 1), (8, 3)]))

    def test_speel(self):
        S = Schaakbord()
        S.zet_begin_positie()
        p = S.stuk_op((2, 1))
        with captured_output() as (out, err):
            S.speel(p, (5, 2))

        output = out.getvalue().strip()
        expected = ["Ongeldige zet: Witte pion kan enkel verplaatst worden naar: [(3, 1), (4, 1)]","Ongeldige zet: Witte pion kan enkel verplaatst worden naar: [(4, 1), (3, 1)]"]
        assert((output in expected))
        with captured_output() as (out, err):
            S.speel(p, (4, 1))
        output = out.getvalue().strip()
        expected = ""
        self.assertEqual(output, expected)
        self.assertEqual(S.stuk_op((2, 1)), None)

    def test_schaak(self):
        S = Schaakbord()
        pw = Pion(WIT)
        kz = Koning(ZWART)
        pz = Pion(ZWART)
        kw = Koning(WIT)
        S.plaats(pw, (7, 3))
        S.plaats(pz, (7, 5))
        S.plaats(kz, (8, 4))
        S.plaats(kw, (6, 3))
               
        self.assertEqual(S.schaak(ZWART), True)
        self.assertEqual(S.schaak(WIT), False)

    def test_schaakmat(self):
        S = Schaakbord()
        pw1 = Pion(WIT)
        kz = Koning(ZWART)
        tw = Toren(WIT)
        qw = Koningin(WIT)

        S.plaats(kz, (8, 8))
        S.plaats(pw1, (7, 7))
        S.plaats(tw,(8,1))
        S.plaats(qw,(6,8))

        self.assertEqual(S.schaak(ZWART), True)
        self.assertEqual(S.schaakmat(ZWART), True)

t=Test()
t.setUp()
t.test_schaakstuk()
t.test_Schaakbord_operaties()
t.test_Schaakbord_begin()
t.test_geldige_zetten_pion()
t.test_speel()
t.test_schaak()
t.test_schaakmat()
print("All tests succeeded")
