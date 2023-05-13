import logging


def is_card_number_valid(card_number: str) -> bool:
    """Checks if the last digit of a numeric sequence is a check digit

    Args:
        card_number (str):

    Returns:
        bool: comparison value of last digit and check digit
    """
    logging.basicConfig(filename="luhn_algorithm.log", level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    try:
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
    except Exception as e:
        logging.exception(f"Exception: {e}")
        raise e
