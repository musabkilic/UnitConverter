from decimal import Decimal
import json


prefixes = [
    ("", "", Decimal(1E+0)),
    ("yotta", "Y", Decimal(1E+24)),
    ("zetta", "Z", Decimal(1E+21)),
    ("exa", "E", Decimal(1E+18)),
    ("peta", "P", Decimal(1E+15)),
    ("tera", "T", Decimal(1E+12)),
    ("giga", "G", Decimal(1E+9)),
    ("mega", "M", Decimal(1E+6)),
    ("kilo", "k", Decimal(1E+3)),
    ("hecto", "h", Decimal(1E+2)),
    ("deka", "da", Decimal(1E+1)),
    ("deci", "d", Decimal(1E-1)),
    ("centi", "c", Decimal(1E-2)),
    ("milli", "m", Decimal(1E-3)),
    ("macro", "µ", Decimal(1E-6)),
    ("nano", "n", Decimal(1E-9)),
    ("pico", "p", Decimal(1E-12)),
    ("femto", "f", Decimal(1E-15)),
    ("atto", "a", Decimal(1E-18)),
    ("zepto", "z", Decimal(1E-21)),
    ("yocto", "y", Decimal(1E-24))
]

units = json.load(open("units.json"))
unit_names = {y:x for x in units.values() for y in x["units"]}

def convert(amount, unit, target):
    unit = unit.strip()
    target = target.strip()
    unit_C, unitA = unitComplex(unit)
    target_C, targetA = unitComplex(target)
    #print(unitA, targetA)
    assert (unit_C == target_C), Exception(f"It's not possible to convert: {repr(unit)} to {repr(target)}!!")
    amount_converted = amount*unitA/targetA
    return amount_converted

def getComplex(unit):
    for _p, __p, a in prefixes:
        for p in [_p, __p]:
            if unit.startswith(p):
                if unit[len(p):] in unit_names:
                    name = unit[len(p):]
                    return unit_names[name]["complex"], a/Decimal(eval(unit_names[name]["units"][name]))
    assert False, Exception(f"Can't find unit on unit list: {repr(unit)}!!")

def unitComplex(unit):
    C = {}
    a = 1
    unit = unit.replace(" per ", " / ")
    if "/" in unit:
        mul, div = unit.split("/")
        for i in div.split("*"):
            i = i.strip()
            l = 1
            if "^" in i:
                l = int(i.split("^")[-1])
                i = i[:i.index("^")]
            c, _a = getComplex(i)
            for j, k in c.items():
                C[j] = C.get(j, 0) - k * l
            a /= _a
    else:
        mul = unit
        div = ""

    for i in mul.split("*"):
        i = i.strip()
        l = 1
        if "^" in i:
            l = int(i.split("^")[-1])
            i = i[:i.index("^")]
        c, _a = getComplex(i)
        for j, k in c.items():
            C[j] = C.get(j, 0) + k * l
        a *= _a

    return {a:b for a, b in C.items() if b!=0}, a


if __name__ == "__main__":
    TEST_CASES = [
        "3, cm, m",
        "9, m/s, km/h",
        "3, ampere, coulomb per second",
        "1, meter, feet",
        "1, inches, feet",
        "7, grams, kilogram",
        "1, kg/s^2*m, atm",
        "3, cm, s"
    ]
    _input = input("Amount, Unit, Target: ")
    if _input == "!TEST SUITE":
        for amount, unit, target in [x.split(",") for x in TEST_CASES]:
            amount = Decimal(amount)
            amount_converted = convert(amount, unit, target)
            print("{:.5f} {} = {:.5f} {}".format(amount, unit, amount_converted, target))
    else:
        amount, unit, target = _input.split(",")
        amount = Decimal(amount)
        amount_converted = convert(amount, unit, target)
        print("{:.5f} {} = {:.5f} {}".format(amount, unit, amount_converted, target))
