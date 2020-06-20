#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(banner_option):
    banner = ""
    if banner_option == 0:
        banner = '\033[1m' + '| IEEE 754 tools |' + '\033[0m'
    elif banner_option == 1:
        banner = '\033[1m' + '| Calculadora IEEE 754 |' + '\033[0m'

    print(banner)


# Utils subfunctions
def to_decimal_base(array, initial, increment):
    s = 0.0
    for i in range(len(array)):
        tmp = int(array[i]) * pow(2, initial)
        s = s + tmp
        print(array[i], "x2^", initial, "=", tmp)
        initial = initial + increment
    print("Total =", s)
    return s


# Utils


def integer_to_binary(integer_str):
    return bin(int(integer_str))[2:]


def binary_decimal_to_num(binary_floating_point_str):
    integer_part, decimal_part = binary_floating_point_str.split(".")
    integer_part = list(integer_part)
    decimal_part = list(decimal_part)
    return str(to_decimal_base(integer_part, len(integer_part) - 1, -1) + to_decimal_base(decimal_part, -1, -1))


def decimal_to_binary_str(integer_decimal_num, n):
    """
              NUM= 0'65
              n = n vegades
              0'65 *2 = 1,3 => 1
              0'3 *2 = 0,6 => 0
              0'6 *2 = 1,2 => 1
              0'2 *2 = 0,4 => 0
              0'4 *2 = 0,8 => 0
              ....
    """
    it = 0
    s = ""
    while it < n:
        num = integer_decimal_num * 2
        array = str(num).split('.')
        if int(array[0]) == 1:
            s = s + "1"
        else:
            s = s + "0"
        integer_decimal_num = num - float(array[0])
        it = it + 1

    return s


# IEE utils
def normalize_IEEE(num):
    num_array = list(num)

    if num_array[0] == "1":
        exp = num.index(".")
        lst = num.split(".")
        norm = "0." + lst[0] + lst[1]
        return norm, exp
    else:
        normalize, exponent, elim = can_normalize(num_array)
        if normalize == False:
            print("Normalitzat : can't normalize")
            return "No Normalization", -1, False
        else:
            norm = "0." + "".join(num_array[elim:])
            return norm, -exponent


def calculate_exponent_decimal_representation(REB, nbits):
    RE = int(REB, 2)
    E = int(RE - pow(2, int(nbits) - 1))
    return E


def represent_to_IEE(signe, nbits, mbits, exponent, normalitzat):
    # nbits son els bits de l'exponent
    # mbits son els bits de la mantissa
    # normalitzat es la mantissa amb el bit ocult
    print("------------------------ IEEE ----------------------------------")

    RE = pow(2, (nbits - 1)) + exponent  # R(E) = 2^(n-1)+E
    REB = bin(int(RE))[2:]
    print("signe", str(signe))  # signe: 0(+) 1(-)
    REB = REB.zfill(nbits)
    REB = str(REB)
    print("exponent binari", REB)

    N = list(normalitzat)  # quan s'entra la mantissa normalitzada, es don per suposat que s'entra amb el bit ocult
    s = "".join(N[0:mbits])  # llavors es selecciona el nombre de bits necessaris de la mantissa
    # mantissa 0101000011 (pero volem 6 xifres) 010100xxxx
    print("mantissa", s)
    print("[" + str(signe) + "]" + "[" + REB + "]" + "[" + s + "]")
    return str(signe) + str(REB) + str(s)


# additionIEE subfunctions

def low_level_extra_zeros_remover(num_bits_str):
    n = 0
    for elem in num_bits_str:
        if elem != "0":
            break
        else:
            n += 1
    return num_bits_str.replace('0', '', n)


def low_level_bit_adder(num1_bits_str, num2_bits_str):
    # DO NOT TOUCH THIS COULD BROKE BINARY ADDER
    # THIS WILL ALWAYS ERASE EXTRA ZEROS 0000bbbbb -> bbbbb IF EXTRAS ARE NEEDED IT MUST BE ADDED OUTSIDE
    # TO REMOVE EXTRAS FROM RESULT THAT MUST BE MODIFIED OUTSIDE FROM THIS FUNCTION
    if len(num1_bits_str) < len(num2_bits_str):
        num1_bits_str = num1_bits_str.zfill(len(num2_bits_str))
    else:
        num2_bits_str = num2_bits_str.zfill(len(num1_bits_str))
    A = list(reversed(list(map(int, num1_bits_str))))
    B = list(reversed(list(map(int, num2_bits_str))))

    lenMax = max(len(A), len(B)) * 2
    tmp = [0 for _ in range(lenMax)]
    it_tmp = lenMax - 1
    for i in range(len(A)):
        tmp[it_tmp] = A[i] + B[i]
        it_tmp -= 1
    tmp.reverse()

    carry = 0
    Total = []
    for x in range(lenMax):
        T = tmp[x] + carry
        if T == 2:
            carry = 1
            Total.append(0)
        elif T == 3:
            carry = 1
            Total.append(1)
        else:
            carry = 0
            Total.append(T)
    Total = "".join(map(str, reversed(Total)))
    Total = low_level_extra_zeros_remover(Total)
    return "".join(Total)


def low_level_bit_inverter(bits_str):
    # THIS IS USED TO SUBSTRACT DOING ADDITION
    # DO NOT TOUCH THIS COULD BROKE IEEE 754 CALCULATOR
    # IF THIS MODIFIED COULD BE BROKEN MAKE YOU SURE WHAT ARE YOU DOING
    # TO REMOVE EXTRAS, THEY MUST BE MODIFIED OUTSIDE THIS FUNCTION
    bits_str = list(bits_str)
    for i in range(len(bits_str)):
        if (bits_str[i] == "1"):
            bits_str[i] = "0"
        else:
            bits_str[i] = "1"

    return "".join(bits_str)


def low_level_bit_substractor(num1_bits_str, substraendo_bits_str):
    # DO NOT TOUCH THIS COULD BROKE IEEE 754 CALCULATOR
    # IF THIS MODIFIED COULD BE BROKEN MAKE YOU SURE WHAT ARE YOU DOING
    # TO REMOVE EXTRAS, THEY MUST BE MODIFIED OUTSIDE THIS FUNCTION

    if len(num1_bits_str) < len(substraendo_bits_str):
        num1_bits_str = num1_bits_str.zfill(len(substraendo_bits_str))
    else:
        substraendo_bits_str = substraendo_bits_str.zfill(len(num1_bits_str))

    substraendo_bits_str = low_level_bit_inverter(substraendo_bits_str)
    substraendo_bits_str = low_level_bit_adder(substraendo_bits_str, "1")
    t = low_level_bit_adder(num1_bits_str, substraendo_bits_str)

    if len(t) > len(num1_bits_str):
        t = t[1:]

    return t


'''def sumador_mantisses(Astr, Bstr):
    point = -1
    if len(Astr) < len(Bstr):
        Astr = list(Astr)
        Astr.reverse()
        Astr = "".join(Astr)
        Astr = Astr.zfill(len(Bstr))
        Astr = list(Astr)
        Astr.reverse()
        Astr = "".join(Astr)
        Astr = list(Astr)
        point = Astr.index(".")
        point = len(Astr) - point - 1
        Astr = "".join(Astr)


    else:
        Bstr = list(Bstr)
        Bstr.reverse()
        Bstr = "".join(Bstr)
        Bstr = Bstr.zfill(len(Astr))
        Bstr = list(Bstr)
        Bstr.reverse()
        Bstr = "".join(Bstr)
        Bstr = list(Bstr)
        point = Bstr.index(".")
        point = len(Bstr) - point - 1
        Bstr = "".join(Bstr)

    Astr = Astr.replace("0.", "")
    Bstr = Bstr.replace("0.", "")

    total = sumar_binari_mantisses(Astr, Bstr)

    # Formato IEE sin extras
    total = trim_extras(total, point)

    return total
    pass
def sumar_binari_mantisses(Astr, Bstr):
    if len(Astr) < len(Bstr):
        Astr = Astr.zfill(len(Bstr))
    else:
        Bstr = Bstr.zfill(len(Astr))
    print("A=", Astr, "   B=", Bstr)

    total = add_binary(Astr, Bstr)

    total = binary_to_string(total)
    return total
    pass'''


# IEE_calculator menu options
def addition_IEEE():
    '''mantissa_A = "0.1"
    mantissa_B = "0.1"
    Total = sumador_mantisses(mantissa_A, mantissa_B)
    if "1." in Total:
        Total, _ = normalize_IEEE(Total)
    elif ".0" in Total:
        Total, _ = normalize_IEEE(Total)
    print(mantissa_A, "+", mantissa_B, "=", Total)'''
    return


def susbstraction_IEEE():
    pass


def product_IEEE():
    pass


def division_IEEE():
    pass


# Range IEEE subfunctions
def mostrar_positius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult,
                     mantissaMenor_no_bitOcult):
    print("Numero Positiu Major")
    print("Signe  = 0")
    print("Exponent:", maxExp, "que representa l'exponent +" + str(dec_M_Exp))
    print("Mantissa:" + (mantissaMajor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMajor_no_bitOcult)
    print("Num.Positiu major=+" + mantissaMajor_no_bitOcult + "x2^" + str(dec_M_Exp))
    print("\nNumero Positiu Menor")
    print("Signe  = 0")
    print("Exponent:", menorExp, "que representa l'exponent " + str(dec_m_Exp))
    print("Mantissa:" + (mantissaMenor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMenor_no_bitOcult)
    print("Num.Positiu menor=+" + mantissaMenor_no_bitOcult + "x2^" + str(dec_m_Exp))
    return


def mostrar_negatius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult,
                     mantissaMenor_no_bitOcult):
    print("Numero Negatiu Major")
    print("Signe  = 1")
    print("Exponent:", menorExp, "que representa l'exponent " + str(dec_m_Exp))
    print("Mantissa:" + (mantissaMenor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMenor_no_bitOcult)
    print("Num.Negatiu major=-" + mantissaMenor_no_bitOcult + "x2^" + str(dec_m_Exp))
    print("\nNegatiu Menor")
    print("Signe  = 1")
    print("Exponent:", maxExp, "que representa l'exponent +" + str(dec_M_Exp))
    print("Mantissa:" + (mantissaMajor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMajor_no_bitOcult)
    print("Num.Negatiu menor=-" + mantissaMajor_no_bitOcult + "x2^" + str(dec_M_Exp))
    return


# numToIEEE subfunctions
def number(num, precision, exp_bits, mant_bits):
    print("\n")
    signe, num, symbol = get_sign_math(num)
    integer_part, decimal_part = str(num).split(".")
    integer_bin_part = str(integer_to_binary(int(integer_part)))
    decimal_bin_part = decimal_to_binary_str(float("0." + decimal_part), precision)
    print("Num binari: " + symbol + integer_bin_part + "." + decimal_bin_part)
    normalitzat, exp = normalize_IEEE(integer_bin_part + "." + decimal_bin_part)
    mantissa_bitOcult = normalitzat.replace("0.1", "")
    print("Normalitzat: ", symbol + normalitzat, " x2^", exp)
    represent_to_IEE(signe, exp_bits, mant_bits, exp, mantissa_bitOcult)


def can_normalize(N):
    count = 0  # conta quants llocs s'a desplac'at el decimal
    elim = 0  # elimina les posicions fins al primer 1 | 0.00001bbb ---> 1bbbbb
    can_be_normalized = False
    for i in range(0, len(N), 1):
        if N[i] == "1":
            can_be_normalized = True
            break
        elim = elim + 1

    for i in range(N.index(".") + 1, len(N), 1):
        if N[i] == "1":
            break
        count = count + 1
    return can_be_normalized, count, elim


def get_sign_math(num):
    if "-" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 1, num, "-"
    elif "+" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 0, num, "+"
    else:
        return 0, num, "+"


# Main menu options
def num_to_IEEE():
    num = float(input("Numero: ").replace(",", "."))
    exp = int(input("Bits exponent: "))
    mant = int(input("Bits mantissa: "))
    precision = 1 + exp + ((exp + mant) * 2)
    number(num, precision, exp, mant)


def IEEE_to_num():
    signe_bits, exponent_bits, mantissa_bits = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    num_IEE = list(input("Numero IEEE>"))

    check = len(num_IEE) == (int(signe_bits) + int(exponent_bits) + int(mantissa_bits))
    if check != True:
        print("discrepancia de numeros !!")
        return
    signe = num_IEE[0:int(signe_bits)]
    exponent = num_IEE[int(signe_bits):int(exponent_bits) + 1]
    mantissa = num_IEE[int(signe_bits) + int(exponent_bits):]

    print("=========== Num IEE entrat ===============")
    print("signe", signe[0], "(+)" if signe[0] == "0" else "(-)")

    decimal_exp = calculate_exponent_decimal_representation("".join(exponent), exponent_bits)
    print("exponent", "".join(exponent), "-->", decimal_exp)
    print("Mantissa", "".join(mantissa))
    print("\nIEE-->Normalitzat: ", "+" if signe[0] == "0" else "-",
          "0.1" + "".join(mantissa) + "x2^" + str(decimal_exp))

    if decimal_exp == 0:  # positive exponent
        norm = list("0.1" + "".join(mantissa))
        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", binary_decimal_to_num("".join(norm)))

    elif decimal_exp > 0:  # positive exponent

        norm = list("0.1" + "".join(mantissa))
        norm.pop(norm.index("."))
        norm.insert(decimal_exp + 1, ".")

        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", binary_decimal_to_num("".join(norm)))
    elif decimal_exp < 0:  # negatve cases

        norm = "0.1" + "".join(mantissa)
        norm = norm.zfill(len(norm) + abs(decimal_exp))
        norm = list(norm)
        index = norm.index(".")
        norm.pop(index)
        norm.insert(index - abs(decimal_exp), ".")

        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", binary_decimal_to_num("".join(norm)))
    else:
        pass


def range_IEEE():
    signe, nbits, mbits = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    clear()
    max_exp = "1" * int(nbits)
    min_exp = "".zfill(int(nbits))
    dec_max_exp = calculate_exponent_decimal_representation(max_exp, int(nbits))
    dec_min_exp = calculate_exponent_decimal_representation(min_exp, int(nbits))

    mantissa_major_bit_ocult = "1" * int(mbits)
    mantissa_menor_bit_ocult = "".zfill(int(mbits))

    mantissa_major_no_bit_ocult = "0.1" + mantissa_major_bit_ocult
    mantissa_menor_no_bit_ocult = "0.1" + mantissa_menor_bit_ocult
    print("Rang dels exponents representables:")
    print("Exponent Major", max_exp, ",que correspon a l'exponent +" + str(dec_max_exp))
    print("Exponent Major", min_exp, ",que correspon a l'exponent " + str(dec_min_exp))
    print("\n")

    mostrar_positius(signe, max_exp, min_exp, dec_max_exp, dec_min_exp, mantissa_major_no_bit_ocult,
                     mantissa_menor_no_bit_ocult)
    print("\n\n")
    mostrar_negatius(signe, max_exp, min_exp, dec_max_exp, dec_min_exp, mantissa_major_no_bit_ocult,
                     mantissa_menor_no_bit_ocult)
    return


def select_menu_option(option):
    clear()
    if isinstance(option, str):
        print(option)
    else:
        if option():
            return
    input("\nContinuar ...")
    clear()


def IEE_calculator():
    while True:
        clear()
        print_banner(1)
        print("Suma de números IEEE            [+]")
        print("Resta de números IEEE           [-]")
        print("Divisió de números IEEE         [*]")
        print("Multiplicació de números IEEE   [/]")
        print("Tornar enrere                   [t]")
        print("Sortir                          [x]")
        opt = input("> ")
        if opt == "+":
            select_menu_option("Not Implemented Yet")
        elif opt == "-":
            select_menu_option("Not Implemented Yet")
        elif opt == "*":
            select_menu_option("Not Implemented Yet")
        elif opt == "/":
            select_menu_option("Not Implemented Yet")
        elif opt == "t":
            return True
        elif opt == "x":
            sys.exit(0)


def main():
    while True:
        clear()
        print_banner(0)
        print("Convertir: Numero --> IEEE           [0]")
        print("Convertir: IEEE   --> Numero         [1]")
        print("Rang IEEE                            [2]")
        print("Calculadora IEEE                     [3]")
        print("Sortir                               [x]")
        opt = input("> ")
        if opt == "0":
            select_menu_option(num_to_IEEE)
        elif opt == "1":
            select_menu_option(IEEE_to_num)
        elif opt == "2":
            select_menu_option(range_IEEE)
        elif opt == "3":
            select_menu_option(IEE_calculator)
        elif opt == "x":
            sys.exit(0)


if __name__ == '__main__':
    try:
        main()

    # Exception handling
    except KeyboardInterrupt:  # Ctrl-C
        print("Keyboard Interruption")
    except SystemExit:  # sys.exit()
        if str(sys.exc_info()[1]) != "0":
            print("System Exit")
            raise
        else:
            clear()
