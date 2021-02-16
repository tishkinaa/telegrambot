# with open('Quistions.csv', 'r', encoding='utf-8-sig') as f:
#     capitals_str = f.read()
# capitals_lst = capitals_str.split('\n')
# for i, c in enumerate(capitals_lst):
#     capitals_lst[i] = c.split('\t')
#
# with open('result.csv', 'w') as f:
#     for c in capitals_lst:
#         f.writelines(f'{c[0]};{c[1]}\n')

with open('Quistions.csv', 'r') as f:
    questions_list = f.read()
questions_list = questions_list.split('\n')
questions_list = [c.split(';') for c in questions_list]
questions_list.pop()
print(questions_list)