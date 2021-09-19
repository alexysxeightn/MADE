def roman_to_arabic(roman_num):
        arabic_num = 0
        TABLE = {'I' : 1, 'V' : 5, 'X' : 10, 'L' : 50}
        i = 0
        while i < len(roman_num) - 1:
            if TABLE[roman_num[i + 1]] > TABLE[roman_num[i]]:
                arabic_num += TABLE[roman_num[i + 1]] - TABLE[roman_num[i]]
                i += 2
            else:
                arabic_num += TABLE[roman_num[i]]
                i += 1
        if i < len(roman_num):
                arabic_num += TABLE[roman_num[len(roman_num) - 1]]
        return arabic_num
     
n = int(input())
kings = []
     
for _ in range(n):
    name_of_king, num_of_king_roman = map(str, input().split())
    num_of_king_arabic = roman_to_arabic(num_of_king_roman)
    kings.append((name_of_king, num_of_king_roman, num_of_king_arabic))
     
kings = sorted(kings, key = lambda x: (x[0], x[2]))
kings = [i[0] + ' ' + i[1] for i in kings]
     
print(*kings, sep = '\n')
