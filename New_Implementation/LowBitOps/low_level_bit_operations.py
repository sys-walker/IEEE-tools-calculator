def low_level_extra_zeros_remover(number: str) -> str:
    """
    Low level extra zeros remover
    Its auxiliary funtion of low_level_bit_adder

    :param number: number - a char sequence
    :type number: str
    :return: number without zeros 0000bbbbb -> bbbbb
    :rtype: str

    WARNINGS:
    - DO NOT TOUCH THIS COULD BREAK LOW LEVEL BINARY ADDER !!
    - IF EXTRAS ZEROS ARE NEEDED IT MUST BE ADDED OUTSIDE
    """
    NotAllZeros=False
    for bit in number:
        if bit != "0":
            NotAllZeros=True
            break

    if NotAllZeros==False:
        return "0"
    else:
        n = 0
        for elem in number:
            if elem != "0":
                break
            else:
                n += 1
        return number.replace('0', '', n)


def low_level_bit_adder(sumand_a: str, summand_b: str) -> str:
    """
    Low bit addition

    :param sumand_a: the first operand  -a char sequence
    :param summand_b: the first operand - a char sequence
    :type sumand_a: str
    :type  summand_b: str
    :return: the sum, as a string
    :rtype: tuple

    WARNINGs:
    - DO NOT TOUCH THIS COULD BREAK LOW LEVEL BINARY ADDER !!
    - THIS WILL ALWAYS ERASE EXTRA ZEROS 0000bbbbb -> bbbbb IF EXTRAS ARE NEEDED IT MUST BE ADDED OUTSIDE
    - TO REMOVE EXTRAS FROM RESULT IT MUST BE MODIFIED OUTSIDE OF THIS FUNCTION
    """
    if (sumand_a == "0" and summand_b == "0"):
        return "0"
    diff = len(sumand_a) - len(summand_b)
    if (diff > 0):
        summand_b = "".zfill(diff) + summand_b
    else:
        sumand_a = "".zfill(-diff) + sumand_a

    sumand_a = list(map(int, sumand_a))
    summand_b = list(map(int, summand_b))

    lenMax = len(sumand_a) + 1
    carry = 0
    Total = [0 for _ in range(lenMax)]
    for idx in reversed(range(0, len(sumand_a))):
        d = (sumand_a[idx] + summand_b[idx] + carry) // 2
        Total[idx + 1] = (sumand_a[idx] + summand_b[idx] + carry) - 2 * d
        carry = d
    Total[0] = carry

    Total = "".join(map(str, Total))
    Total = low_level_extra_zeros_remover(Total)
    return "".join(Total)


def low_level_bit_left_shifter(number: str, offset:int=0) -> str:
    """
    Low level bit shifter
    Shift bits to the left, by adding n 0s on the right.

    :param number: number in binary format
    :param offset: number of zeros to add to the right side
    :type number: str
    :type offset: int
    :return: number shifted
    :rtype: str

    """
    if offset<=0:
        return number
    else:
        return number+"0"*offset


def low_level_bit_inverter(number: str) -> str:
    """
    Low level bit inverter

    :param number: number - a char sequence
    :type number: str
    :return: number wit inverted bits
    :rtype: str
    """
    s=""
    for bit in number:
        if bit == "0":
            s+="1"
        else:
            s+="0"
    return s


if __name__ == '__main__':
    pass
