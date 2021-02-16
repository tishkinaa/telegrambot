



class User:
    def __init__(self, name):
        self.name = name
        self.userlist = [1, 2, 3, 4, 5]
    def __eq__(self, other):
        if self.name == other:
            return True
        else:
            return False



users = {}

users['Anton'] = User('Anton')
users['Victor'] = User('Victor')

print(users['Anton'].userlist.pop())
print(users['Anton'].userlist)


dict = {'1': 'odin', '2': 'dva'}

print(dict)


def my_f():
    global dict
    dict = {}

my_f()
print(dict)