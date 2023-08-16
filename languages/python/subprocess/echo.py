while True:
    try:
        print(repr(input()))
    except EOFError:
        break
