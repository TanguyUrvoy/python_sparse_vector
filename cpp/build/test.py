import sparse_vector as sv

toto = sv.SparseVec("{ 5 : 6 ,7:3 }")

print(toto[3])
print(toto[5])

print(toto)

tata = sv.SparseVec(list(range(10)))

print(tata[3])

print(tata)


x = sv.SparseVec("5:-1,3:1,8:0")
y = sv.SparseVec("3:2")

if x < y:
    print(x," < ", y)
else:
    print("Not ", x," < ", y)
    
    
z = sv.SparseVec("")


if x < z:
    print(x," < ", z)
else:
    print("Not ", x," < ", z)
    
print("x=",z)
print("y=",y)
    
print("x += y")    
x += y


print("x=",z)
print("y=",y)
   
    
    
print("z=",z)
print("y=",y)
    
print("z += y")    
z += y


print("z=",z)
print("y=",y)



    
