# Problem : Array a
# array b

a = [1, 2, 3]
b = [2, 3, 100]
c = []

index_c = 0

for item_a in a:
    for item_b in b:
        if item_a==item_b:
            c.append(item_a)
print(c)

c_dict = {
    "a": a,
    "b": b 
}

print(type(c_dict["a"]))

# 


