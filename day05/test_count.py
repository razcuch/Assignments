import pytest
from count_nuc import statistic
def test_count1():
    res=statistic("AGCGTGCAGXTXTXAG")
    assert res=={"A": 3, "T": 3, "G": 5, "C": 2, "Unknown": 3}

def test_cout2():
    res=statistic("AGCATCGAA") 
    assert res== {"A": 4, "T": 1, "G": 2, "C": 2, "Unknown": 0}  