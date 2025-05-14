class tester:
    def __init__(self):
        print("__init__")

    def __del__(self):
        print("__del__")

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__")
        if exc_type:
            return False
        return True


with tester() as t:
    print("in with")
