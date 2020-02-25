import chardet

str_en = 'abc123'.encode('utf-8')  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
str_zh = '中文'.encode('utf-8')  # {'encoding': 'utf-8', 'confidence': 0.7525, 'language': ''}

print(chardet.detect(str_en))
print(chardet.detect(str_zh))


# s = "1/60"
# print(s)
# print('/' in s)
# (s0, s1) = s.split('/')
# print(s0)
# print(s1)