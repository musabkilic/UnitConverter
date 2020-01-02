from decimal import Decimal
import json


prefixes = {
    ("yotta", "Y"): Decimal(1E+24),
    ("zetta", "Z"): Decimal(1E+21),
    ("exa", "E"): Decimal(1E+18),
    ("peta", "P"): Decimal(1E+15),
    ("tera", "T"): Decimal(1E+12),
    ("giga", "G"): Decimal(1E+9),
    ("mega", "M"): Decimal(1E+6),
    ("kilo", "k"): Decimal(1E+3),
    ("hecto", "h"): Decimal(1E+2),
    ("deka", "da"): Decimal(1E+1),
    ("", ""): Decimal(1E+0),
    ("deci", "d"): Decimal(1E-1),
    ("centi", "c"): Decimal(1E-2),
    ("milli", "m"): Decimal(1E-3),
    ("macro", "µ"): Decimal(1E-6),
    ("nano", "n"): Decimal(1E-9),
    ("pico", "p"): Decimal(1E-12),
    ("femto", "f"): Decimal(1E-15),
    ("atto", "a"): Decimal(1E-18),
    ("zepto", "z"): Decimal(1E-21),
    ("yocto", "y"): Decimal(1E-24)
}

units = json.load(open("units.json"))
unit_names = [y for x in units.values() for y in x["units"]]

def unitType(unit):
    for type, info in units.items():
        for name in info["units"]:
            for prefix, a in prefixes.items():
                for p in prefix:
                    if unit.startswith(p):
                        if unit[len(p):].startswith(name):
                            return type

def normalizeUnit(unit, amount):
    for prefix, a in prefixes.items():
        for p in prefix:
            if unit.startswith(p):
                for name in unit_names:
                    if unit[len(p):].startswith(name):
                        return a*amount, name

def unitToBase(unit, amount):
    unit_type = unitType(unit)
    base, conv_table = units[unit_type]["base"], units[unit_type]["units"]
    for name in conv_table:
        if unit.startswith(name):
            return amount / Decimal(eval(conv_table[name]))

def baseToUnit(unit, amount):
    unit_type = unitType(unit)
    base, conv_table = units[unit_type]["base"], units[unit_type]["units"]
    for name in conv_table:
        if unit.startswith(name):
            return amount * Decimal(eval(conv_table[name]))

def unitToPrefix(unit, amount):
    for prefix, a in prefixes.items():
        for p in prefix:
            if unit.startswith(p):
                for name in unit_names:
                    if unit[len(p):].startswith(name):
                        return amount/a

def convert(unit, target, amount):
    unit_type = unitType(unit)
    target_type = unitType(target)
    assert (unit_type == target_type), Exception("It's not possible to convert!!")
    amount_normalized, unit_normalized = normalizeUnit(unit, amount)
    _, target_normalized = normalizeUnit(target, 0)
    amount_based = unitToBase(unit_normalized, amount_normalized)
    amount_converted_normalized = baseToUnit(target_normalized, amount_based)
    amount_converted = unitToPrefix(target, amount_converted_normalized)
    return amount_converted


if __name__ == "__main__":
    unit = input("Unit to convert from: ").strip()
    target = input("Unit to convert to: ").strip()
    amount = Decimal(input("Amount: "))
    amount_converted = convert(unit, target, amount)
    print("{:.5f} {} = {:.5f} {}".format(amount, unit, amount_converted, target))
