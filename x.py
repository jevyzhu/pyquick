import time

i = 0
while True:
    i = i+1
    with open('x','a') as f:
        f.write(f'{i}\n')
    time.sleep(1)
