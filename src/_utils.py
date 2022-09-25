import typing
import decimal
import datetime
import time
import re


def parse_date(date_str: str, date_fmt: str = "Ymd", *args) -> datetime.date:
    val = datetime.date(*(time.strptime(date_str, date_fmt)[0:3]))
    return val


def parse_decimal(decimal_str: str, *args) -> decimal.Decimal:
    val = decimal.Decimal(decimal_str)
    return val


def parse_boolean(boolean_str: str, *args) -> bool:
    return bool(int(boolean_str))


def parse_int(int_str: str, *args) -> int:
    return int(int_str)


def parse_str(src_str: str, *args) -> str:
    return src_str


def parse_float(float_str: str, *args) -> float:
    return float(float_str)


type_parsers = {"date": parse_date,
                "decimal": parse_decimal,
                "int": parse_int,
                "str": parse_str,
                "float": parse_float,
                "bool": parse_boolean}


def parse_list(list_str: str,
               list_fmt: str = "str[,]",
               *args) -> typing.List[typing.Any]:
    list_type, list_fmt, _ = re.split("\[|\]", list_fmt)
    list_str = list_str.split(list_fmt)

    val = [type_parsers[list_type](val_str) for val_str in list_str]

    return val


type_parsers["list"] = parse_list


def parse_parameter(par_val : str) -> typing.Tuple[str, typing.Any]:
    par_type, val = par_val.split("=")        

    par_name, par_type, _ = re.split("<|>", par_type)
    par_type = par_type.split(" ")
    if len(par_type) > 1:
        par_type, par_args = par_type
    else:
        par_type = par_type[0]
        par_args = None

    val = type_parsers[par_type](val, par_args)

    return par_name, val
