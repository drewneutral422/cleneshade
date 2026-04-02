import math

def add(a, b):
    # Cleneshade passes arguments as strings, so we convert them
    result = float(a) + float(b)
    print(f"[Math] Result: {result}")
    return result

def sqrt(n):
    result = math.sqrt(float(n))
    print(f"[Math] Square Root: {result}")
    return result

def pi():
    print(f"[Math] PI: {math.pi}")