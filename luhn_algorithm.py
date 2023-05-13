def is_card_number_valid(card_number):
    numbers_list = list(card_number)
    key = numbers_list[len(numbers_list)-1]
    numbers_list.pop(len(numbers_list)-1)
    numbers_list = [int(number) for number in numbers_list]
    sum = 0
    for i in range(len(numbers_list)):
        if (i + 1) % 2 != 0:
            if numbers_list[i]*2 >= 10:
                sum += numbers_list[i]*2 - 9
            else:
                sum += numbers_list[i]*2
        else:
            sum += numbers_list[i]
    return int(key) == 10 - ((sum % 10) % 10)
