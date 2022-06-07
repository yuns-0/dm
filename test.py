import time

f = open("test.txt", 'a')
for i in range(100):
    f.write(f"hello {i}")
    print(i)
    time.sleep(10)
        

f.close()