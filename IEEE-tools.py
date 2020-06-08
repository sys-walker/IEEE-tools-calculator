#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os,sys,signal

#Banner
def switch_banner(num):
    switcher = {
        0: "IEEE tools.",
        1: "Calculadora IEEE"
    }
    return switcher.get(num)
def banner(num):
    print(switch_banner(num))

#Utils subfunctions
def toDecimalBase(array, initial, increment):
    s = 0.0
    for i in range(len(array)):
        tmp = int(array[i]) * pow(2, initial)
        s = s + tmp
        print(array[i], "x2^", initial, "=", tmp)
        initial = initial + increment
    print("Total =", s)
    return s
#Utils
def stringBinary_to_binaryArray(binary_num_str):
    Array = list(binary_num_str)
    A=[]
    for item in Array:
        if item == "1":
            A.append(1)
        else:
            A.append(0)
    return A
def binary_toString(Array_binary_string_digits):
    A = ""
    for item in Array_binary_string_digits:
        if item == 1:
            A +="1"
        else:
            A += "0"
    return A
def integer_to_Binary(integer_str):
    return bin(int(integer_str))[2:]
def sumarBinari(binary_num_str_1, binary_num_str_2):
    A = stringBinary_to_binaryArray(binary_num_str_1)
    B = stringBinary_to_binaryArray(binary_num_str_2)

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
def binary_decimal_to_num(binary_floating_point_str):
    integer_part, decimal_part = binary_floating_point_str.split(".")
    integer_part = list(integer_part)
    decimal_part = list(decimal_part)
    return str(toDecimalBase(integer_part, len(integer_part) - 1, -1) + toDecimalBase(decimal_part, -1, -1))
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

#IEE utils
def normalize_IEE(Num):
    NumArray = list(Num)

    if NumArray[0] == "1":
        exp = Num.index(".")
        lst = Num.split(".")
        Norm = "0." + lst[0] + lst[1]
        return Norm,exp
    else:
        normalize, exponent, elim = can_normalize(NumArray)
        if normalize == False:
            print("Normalitzat : can't normalize")
            return "No Normalization",-1,False
        else:
            Norm = "0."+"".join(NumArray[elim:])
            return Norm, -exponent
def calculateExponentDecimalRepresentation(REB, nbits):
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

#additionIEE subfunctions
def sumadorMantisses(Astr, Bstr):
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

    Total = sumarBinariMantisses(Astr, Bstr)

    # Formato IEE sin extras
    Total = trimExtras(Total, point)

    return Total
def sumarBinariMantisses(Astr, Bstr):
    if len(Astr) < len(Bstr):
        Astr = Astr.zfill(len(Bstr))
    else:
        Bstr = Bstr.zfill(len(Astr))
    print("A=", Astr, "   B=", Bstr)

    Total = sumarBinari(Astr, Bstr)


    Total = binary_toString(Total)
    return Total
def trimExtras(Total, point):
    Total = list(Total)
    Total.insert(len(Total) - point, ".")
    rag_symb = "1" if "1." in "".join(Total) else "."
    rag = Total.index(rag_symb)
    Total = Total[rag:]
    Total = "".join(Total) if rag_symb == "1" else "0" + "".join(Total)
    return Total


# IEE_calculator menu options
def additionIEEE():
    mantissa_A="0.1"
    mantissa_B="0.1"
    Total = sumadorMantisses(mantissa_A, mantissa_B)
    if "1." in Total:
        Total,_=normalize_IEE(Total)
    elif ".0" in Total:
        Total, _ = normalize_IEE(Total)
    print(mantissa_A, "+", mantissa_B, "=", Total)
    return
def susbstractionIEEE():
    pass
def productIEEE():
    pass
def divisionIEEE():
    pass

#Range IEEE subfunctions
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

# numToIEEE subfunctions
def number(num, precision, signe, nbits, mbits):
    print("\n")
    SIGNE, num,symbol = getSignMath(num)
    integer_part, decimal_part = str(num).split(".")
    integer_bin_part = str(integer_to_Binary(int(integer_part)))
    decimal_bin_part = decimal_to_binary_str(float("0." + decimal_part), precision)
    print("Num binari: "+symbol + integer_bin_part + "." + decimal_bin_part)
    normalitzat, exp = normalize_IEE(integer_bin_part + "." + decimal_bin_part)
    mantissa_bitOcult = normalitzat.replace("0.1", "")
    print("Normalitzat: ", symbol + normalitzat, " x2^", exp)
    IEEE_str = represent_to_IEE(SIGNE, nbits, mbits, exp, mantissa_bitOcult)
    return IEEE_str
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
def getSignMath(num):
    if "-" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 1, num,"-"
    elif "+" in str(num):
        tmp = list(str(num))  # comprova i elimina el signe negatiu
        num = float("".join(tmp[1:]))  # restaura el numero sense el signe negatiu
        return 0, num,"+"
    else:
        return 0, num,"+"
# Main menu options
def numToIEEE():
    num = float(input("Numero >").replace(",", "."))
    #size = int(input("precision >"))
    lst = str(input("bits signe,bits exponent,bits mantissa >")).split(",")
    size =  int(lst[0])+int(lst[1])+((int(lst[1])+int(lst[2]))*2)
    number(num, size, int(lst[0]), int(lst[1]), int(lst[2]))
    return
def IEEEtoNum():

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

# Menus
def main():
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
            input("Aviat!!")

            #IEE_calculator()

            os.system("clear")
        elif opt == "x":
            break
        else:
            print("Unknown")
            input("\ncontinuar ...")
            os.system("clear")
def IEE_calculator():
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
            additionIEEE()
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
# signal signint Ctrl+c handler
def sigint_handler(signal, frame):
    sys.exit(0)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    os.system("clear")

    main()
