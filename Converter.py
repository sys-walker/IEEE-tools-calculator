#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ARREGLAR AQUESTA GUARRADA XDDD
import os,sys


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


def getSignMath(num):
    if "-" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 1, num
    elif "+" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 0, num
    else:
        return 0, num


def number(num, precision, signe, nbits, mbits):
    print("\n")
    IEEE_str = ""

    SIGNE, num = getSignMath(num)

    integer_part, decimal_part = str(num).split(".")

    integer_bin_part = str(toBinary(int(integer_part)))
    decimal_bin_part = decimal(float("0." + decimal_part), precision)  # passa a decimal la part decimal

    N = list((integer_bin_part + "." + decimal_bin_part))
    if N[0] == "1":  # comprova si el format de numero es 1bbbbb.bbbbbb
        print("Num binari:" + integer_bin_part + "." + decimal_bin_part)  # l'exponent sempre serà positiu
        exponent = N.index(".")  # indica quantes posicions ha de avança la '.'
        print("*Normalitzat: 0." + integer_bin_part + decimal_bin_part + "x2^" + str(exponent))

        bitocult = list(integer_bin_part + decimal_bin_part)  # crea la mantissa
        # bitocult = bitocult[1:]
        IEEE_str = IEEE(SIGNE, nbits, mbits, exponent, "".join(bitocult[1:]))  # mantissa ocultant el 1r bit

    else:  # el format de numero es 0.bbbbbb o 0.00--bbbbb

        normalize, exponent, elim = can_normalize(N)  # 'elim' es el numero de 0 a eliminar per conseguir 0.1bbbbb
        # 0.00001bbb ---> elim 6-----> 0.1bbbbb
        print("Num binari:" + integer_bin_part + "." + decimal_bin_part)  # l'exponent sempre serà negatiu
        if normalize == False:
            print("Normalitzat : can't normalize")
        else:
            bitocult = list("".join(N[elim:]))
            print("+Normalitzat 0." + "".join(bitocult) + " x 2^-" + str(exponent))

            bitocult = bitocult[1:]  # crea la mantissa ocultant el 1r bit

            IEEE_str = IEEE(SIGNE, nbits, mbits, -1 * exponent, "".join(bitocult))
    return IEEE_str


def numToIEEE():
    num = float(input("Numero >").replace(",", "."))
    size = int(input("precision >"))
    lst = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    number(num, size, int(lst[0]), int(lst[1]), int(lst[2]))
    return


def switch_banner(num):
    switcher = {
        0: "IEEE tools.",
        1: "Calculadora IEEE"
    }
    return switcher.get(num)


def banner(num):
    print(switch_banner(num))


def calculateExponentDecimalRepresentation(REB, nbits):
    RE = int(REB, 2)
    E = int(RE - pow(2, int(nbits) - 1))
    return E


def mostrarPositius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult,
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


def mostrarNegatius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult,
                    mantissaMenor_no_bitOcult):
    print("Numero Negatiu Major")
    print("Signe  = 1")
    print("Exponent:", menorExp, "que representa l'exponent " + str(dec_m_Exp))
    print("Mantissa:" + (mantissaMenor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMenor_no_bitOcult)
    print("Num.Positiu major=-" + mantissaMenor_no_bitOcult + "x2^" + str(dec_m_Exp))
    print("\nNegatiu Menor")
    print("Signe  = 1")
    print("Exponent:", maxExp, "que representa l'exponent +" + str(dec_M_Exp))
    print("Mantissa:" + (mantissaMajor_no_bitOcult).replace("0.1",
                                                            "") + ", que correspon a la mantissa " + mantissaMajor_no_bitOcult)
    print("Num.Negatiu menor=-" + mantissaMajor_no_bitOcult + "x2^" + str(dec_M_Exp))
    return


def rangeIEE():
    signe, nbits, mbits = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    os.system("clear")
    maxExp = "1" * int(nbits)
    menorExp = "".zfill(int(nbits))
    dec_M_Exp = calculateExponentDecimalRepresentation(maxExp, int(nbits))
    dec_m_Exp = calculateExponentDecimalRepresentation(menorExp, int(nbits))

    mantissaMajor_bitOcult = "1" * int(mbits)
    mantissaMenor_bitOcult = "".zfill(int(mbits))

    mantissaMajor_no_bitOcult = "0.1" + mantissaMajor_bitOcult
    mantissaMenor_no_bitOcult = "0.1" + mantissaMenor_bitOcult
    print("Rang dels exponents representables:")
    print("Exponent Major", maxExp, ",que correspon a l'exponent +" + str(dec_M_Exp))
    print("Exponent Major", menorExp, ",que correspon a l'exponent " + str(dec_m_Exp))
    print("\n")

    mostrarPositius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult, mantissaMenor_no_bitOcult)
    print("\n\n")
    mostrarNegatius(signe, maxExp, menorExp, dec_M_Exp, dec_m_Exp, mantissaMajor_no_bitOcult, mantissaMenor_no_bitOcult)
    return


def toDecimalBase(array, initial, increment):
    s = 0.0
    for i in range(len(array)):
        tmp = int(array[i]) * pow(2, initial)
        s = s + tmp
        print(array[i], "x2^", initial, "=", tmp)
        initial = initial + increment
    print("Total =", s)
    return s


def toDecimal(num_binari_punt_flotante):
    integer_part, decimal_part = num_binari_punt_flotante.split(".")

    integer_part = list(integer_part)
    # integer_part.reverse()

    decimal_part = list(decimal_part)

    # enter = Decimal(integer_part, 0, 1)
    # decimal= toDecimalBase(decimal_part,-1,-1)

    return str(toDecimalBase(integer_part, len(integer_part) - 1, -1) + toDecimalBase(decimal_part, -1, -1))


def toBinary(num_decimal):
    return bin(int(num_decimal))[2:]


def IEEEtoNum():
    # NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
    sbits, nbits, mbits = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    numIEE = list(input("Numero IEEE>"))

    check = len(numIEE) == (int(sbits) + int(nbits) + int(mbits))
    if check != True:
        print("discrepancia de numeros !!")
        return
    signe = numIEE[0:int(sbits)]
    exponent = numIEE[int(sbits):int(nbits) + 1]
    mantissa = numIEE[int(sbits) + int(nbits):]

    print("=========== Num IEE entrat ===============")
    print("signe", signe[0], "(+)" if signe[0] == "0" else "(-)")

    decimal_exp = calculateExponentDecimalRepresentation("".join(exponent), nbits)
    print("exponent", "".join(exponent), "-->", decimal_exp)
    print("Mantissa", "".join(mantissa))
    print("\nIEE-->Normalitzat: ", "+" if signe[0] == "0" else "-",
          "0.1" + "".join(mantissa) + "x2^" + str(decimal_exp))

    if decimal_exp == 0:  # positive exponent
        norm = list("0.1" + "".join(mantissa))
        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", toDecimal("".join(norm)))

    elif decimal_exp > 0:  # positive exponent

        norm = list("0.1" + "".join(mantissa))
        norm.pop(norm.index("."))
        norm.insert(decimal_exp + 1, ".")

        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", toDecimal("".join(norm)))
    elif decimal_exp < 0:  # negatve cases

        norm = "0.1" + "".join(mantissa)
        norm = norm.zfill(len(norm) + abs(decimal_exp))
        norm = list(norm)
        index = norm.index(".")
        norm.pop(index)
        norm.insert(index - abs(decimal_exp), ".")

        print("Normalitzat ---> binari decimal: +" + "".join(norm))
        print("Nomero en decimal:", "+" if signe[0] == "0" else "-", toDecimal("".join(norm)))
    else:
        pass

#############################################################################
def toIntArray(param):
    Array = list(param)
    A=[]
    for item in Array:
        if item == "1":
            A.append(1)
        else:
            A.append(0)
    return A


def sumarBinariMantisses(Astr, Bstr):
    A = toIntArray(Astr)
    B = toIntArray(Bstr)



    A.reverse()
    B.reverse()
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

    Total.reverse()
    return Total


def toString(Array):
    A = ""
    for item in Array:
        if item == 1:
            A +="1"
        else:
            A += "0"
    return A


def trimExtras(Total, Bstr):
    i = len(Total) - len(Bstr)
    Total = toString(Total)  # convierte en un string
    Total = list(Total)  # convierte en chars array
    Total.insert(i, ".")
    Total = "".join(Total)  # convierte en un string
    if "1." in Total:
        Total = list(Total)  # convierte en chars array
        rag = Total.index("1")
        Total = Total[rag:]
        Total = "".join(Total)  # convierte en un string

    else:
        Total = list(Total)  # convierte en chars array
        rag = Total.index(".")
        Total = Total[rag:]
        Total = "".join(Total)  # convierte en un string    ".bbbbbbb"
        Total = "0" + Total

    return Total


def sumadorMantisses(Astr, Bstr):
    Astr = Astr.replace("0.", "")
    Bstr = Bstr.replace("0.", "")
    if len(Astr) < len(Bstr):
        Astr = Astr.zfill(len(Bstr))
        Astr = list(Astr)
        Astr.reverse()
        Astr = "".join(Astr)

    else:
        Bstr = Bstr.zfill(len(Astr))
        Bstr = list(Bstr)
        Bstr.reverse()
        Bstr = "".join(Bstr)

    Total = sumarBinariMantisses(Astr, Bstr)

    # Formato IEE sin extras
    Total = trimExtras(Total, Bstr)

    return Total


def sumaIEE():
    mantissa_A="0.11"
    mantissa_B = "0.11"
    Total = sumadorMantisses(mantissa_A, mantissa_B)
    if "1." in Total:
        print("normalitzar")
    else:
        print("JA esta normalitzat")
    print(mantissa_A, "+", mantissa_B, "=", Total)
    return


def calculadoraIEE():
    while True:
        banner(1)
        print("Suma de números IEEE            [+]")
        print("Resta de números IEEE           [-]")
        print("Divisió de números IEEE         [*]")
        print("Multiplicació de números        [/]")
        print("Sortir de IEEE tools            [f]")
        print("<= Tornar enrere                [t]")
        opt = input(">")
        if opt == "+":
            os.system("clear")
            #sumaIEE()
            print("Aviat!!!")
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "-":
            os.system("clear")
            print("Aviat!!!")
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "*":
            os.system("clear")
            print("Aviat!!!")
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "/":
            os.system("clear")
            print("Aviat!!!")
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "f":
            sys.exit(0)
        elif opt == "t":
            return
        else:
            print("Unknown")
            input("\ncontinuar ...")
            os.system("clear")















if __name__ == '__main__':
    os.system("clear")
    while True:
        banner(0)
        print("Convertir Numero -->IEEE            [0]")
        print("Convertir IEEE -->Numero            [1]")
        print("Rang IEEE [Signe|Exponent|Mantissa] [2]")
        print("Calculadora IEE                     [3]")
        print("Sortir                              [x]")
        opt = input(">")
        if opt == "0":
            os.system("clear")
            numToIEEE()
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "1":
            os.system("clear")
            IEEEtoNum()
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "2":
            rangeIEE()
            input("\ncontinuar ...")
            os.system("clear")
        elif opt == "3":
            os.system("clear")
            calculadoraIEE()

            os.system("clear")
        elif opt == "x":
            break
        else:
            print("Unknown")
            input("\ncontinuar ...")
            os.system("clear")
