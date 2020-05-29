#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def decimal(NUM, n):
    """
              Num= 0'65
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
        num = NUM * 2
        array = str(num).split('.')
        if int(array[0]) == 1:
            s = s + "1"
        else:
            s = s + "0"
        NUM = num - float(array[0])
        it = it + 1

    return s


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


def IEEE(signe, nbits, mbits, exponent, normalitzat):
                                                # nbits son els bits de l'exponent
                                                # mbits son els bits de la mantissa
                                                # normalitzat es la mantissa amb el bit ocult
    print("------------------------ IEEE ----------------------------------")

    RE = pow(2, (nbits - 1)) + exponent         # R(E) = 2^(n-1)+E
    REB = str(bin(int(RE))).replace("0b", "")   # R(E) en binari

    print("signe",  str(signe))                 # signe: 0(+) 1(-)

    it = 0
    maxim = nbits - len(REB)                    # python per no posa bits adicionals  2 en binari es 10,
    while (it < maxim):                         # pero si fem servir 4 xifres haurem de posar 0 adicionals
        REB = "0" + REB                         # aixi pasa de 10 a 0010, per aquesta part passa sempre que es necessari
        it = it + 1
    print("exponent binari", REB)

    N = list(normalitzat)                       # quan s'entra la mantissa normalitzada, es don per suposat que s'entra amb el bit ocult
    s = "".join(N[0:mbits])                     # llavors es selecciona el nombre de bits necessaris de la mantissa
                                                # mantissa 0101000011 (pero volem 6 xifres) 010100xxxx

    print("[" + str(signe) + "]" + "[" + REB + "]" + "[" + s + "]")
    return str(signe)+str(REB)+str(s)


def number(num, precision, signe, nbits, mbits):
    print("\n")
    IEEE_str = ""
    if "-" in str(num):
        tmp = list(str(num))                                            #comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))                                   #restaura el numero sense el signe negatiu
        SIGNE = 1
    else:
        SIGNE = 0


    integer_part, decimal_part = str(num).split(".")

    integer_bin_part = str(bin(int(integer_part))).replace("0b", "")    # passa a decimal la part entera

    decimal_bin_part = decimal(float("0." + decimal_part), precision)    # passa a decimal la part decimal

    N = list((integer_bin_part + "." + decimal_bin_part))
    if N[0] == "1":                                                      # comprova si el format de numero es 1bbbbb.bbbbbb
        print("Num binari:" + integer_bin_part + "." + decimal_bin_part) # l'exponent sempre serà positiu
        exponent = N.index(".")                                          # indica quantes posicions ha de avança la '.'
        print("*Normalitzat: 0." + integer_bin_part + decimal_bin_part + "x2^" + str(exponent))

        bitocult = list(integer_bin_part + decimal_bin_part)
        bitocult = bitocult[1:]                                         # crea la mantissa ocultant el 1r bit
        IEEE_str = IEEE(SIGNE, nbits, mbits, exponent, "".join(bitocult))

    else:                                                               # el format de numero es 0.bbbbbb o 0.00--bbbbb

        normalize, exponent, elim = can_normalize(N)                    # 'elim' es el numero de 0 a eliminar per conseguir 0.1bbbbb
                                                                        # 0.00001bbb ---> elim 6-----> 0.1bbbbb
        print("Num binari:" + integer_bin_part + "." + decimal_bin_part)# l'exponent sempre serà negatiu
        if normalize == False:
            print("Normalitzat : can't normalize")
        else:
            bitocult = list("".join(N[elim:]))
            print("+Normalitzat 0." + "".join(bitocult) + " x 2^-" + str(exponent))

            bitocult = bitocult[1:]                                     # crea la mantissa ocultant el 1r bit

            IEEE_str=IEEE(SIGNE, nbits, mbits, -1*exponent, "".join(bitocult))
    return IEEE_str



if __name__ == '__main__':
    num = float(input("Numero >").replace(",", "."))
    size = int(input("precision >"))
    lst = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    number(num, size, int(lst[0]), int(lst[1]), int(lst[2]))
