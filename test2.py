
def locate_n(locate_list, n):
    return locate_list[n]

def test(a, n):
    assert locate_n(locate_list=a, n=n)==a[n]

test(a=[1,3,5,7,9],n=3)

# 1: baised: 2-Ts
# 2: Unbaised: fair 

# 5 times - all tails
# P(C|N = (TTTTT)) = P(C).P(N)

# (0.5)^5