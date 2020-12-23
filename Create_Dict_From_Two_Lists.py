var = 'a'
list_1 = [(chr(ord(var) + i)) for i in range(26)]
list_2 = [x*2 for x in list_1]
test_dict = {key: list_2[list_1.index(key)] for key in list_1}
double_alphabet = test_dict
