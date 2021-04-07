from low_level_bit_operations import *


def bit_adder(num_a: str, num_b: str) -> str:
    return low_level_bit_adder(num_a, num_b)


def bit_substractor(minuend: str, subtrahend_: str) -> str:
    if low_level_extra_zeros_remover(minuend) == low_level_extra_zeros_remover(subtrahend_):
        return "0"

    subtrahend = low_level_extra_zeros_remover(subtrahend_)

    length = max(len(minuend), len(subtrahend))

    minuend = minuend.zfill(length)
    subtrahend = subtrahend.zfill(length)

    subtrahend = bit_twos_complement(subtrahend)
    result = low_level_bit_adder(minuend, subtrahend)
    result = low_level_extra_zeros_remover(result)

    if len(result) != len(minuend):
        return result[1:]
    else:
        return result


def bit_ones_complement(num: str) -> str:
    return low_level_bit_inverter(num)


def bit_twos_complement(num: str) -> str:
    return low_level_bit_adder(low_level_bit_inverter(num), "1")


if __name__ == '__main__':
    print(bit_substractor("110", "1"), "<-xd")
