def transliterate(name, lang="ru"):
    """
    Транслитерация с русского на английский и обратно
    Транслитерация обратно может работать некорректно
    """
    # Словарь с заменами
    associations = {
        "ru": {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "yo",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "i",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "h",
            "ц": "c",
            "ч": "ch",
            "ш": "sh",
            "щ": "sch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "u",
            "я": "ya",
            "А": "A",
            "Б": "B",
            "В": "V",
            "Г": "G",
            "Д": "D",
            "Е": "E",
            "Ё": "YO",
            "Ж": "ZH",
            "З": "Z",
            "И": "I",
            "Й": "I",
            "К": "K",
            "Л": "L",
            "М": "M",
            "Н": "N",
            "О": "O",
            "П": "P",
            "Р": "R",
            "С": "S",
            "Т": "T",
            "У": "U",
            "Ф": "F",
            "Х": "H",
            "Ц": "C",
            "Ч": "CH",
            "Ш": "SH",
            "Щ": "SCH",
            "Ъ": "",
            "Ы": "y",
            "Ь": "",
            "Э": "E",
            "Ю": "U",
            "Я": "YA",
            ",": "",
            "?": "",
            " ": "_",
            "~": "",
            "!": "",
            "@": "",
            "#": "",
            "$": "",
            "%": "",
            "^": "",
            "&": "",
            "*": "",
            "(": "",
            ")": "",
            "-": "",
            "=": "",
            "+": "",
            ":": "",
            ";": "",
            "<": "",
            ">": "",
            "'": "",
            '"': "",
            "\\": "",
            "/": "",
            "№": "",
            "[": "",
            "]": "",
            "{": "",
            "}": "",
            "ґ": "",
            "ї": "",
            "є": "",
            "Ґ": "g",
            "Ї": "i",
            "Є": "e",
            "—": "",
        },
        "en": {
            "A": "А",
            "B": "Б",
            "C": "Ц",
            "CH": "Ч",
            "D": "Д",
            "E": "Э",
            "F": "Ф",
            "G": "Г",
            "H": "Х",
            "I": "Й",
            "K": "К",
            "L": "Л",
            "M": "М",
            "N": "Н",
            "O": "О",
            "P": "П",
            "R": "Р",
            "S": "С",
            "SCH": "Щ",
            "SH": "Ш",
            "T": "Т",
            "U": "Ю",
            "V": "В",
            "YA": "Я",
            "YO": "Ё",
            "Z": "З",
            "ZH": "Ж",
            "a": "а",
            "b": "б",
            "c": "ц",
            "ch": "ч",
            "d": "д",
            "e": "э",
            "f": "ф",
            "g": "г",
            "h": "х",
            "i": "й",
            "k": "к",
            "l": "л",
            "m": "м",
            "n": "н",
            "o": "о",
            "p": "п",
            "r": "р",
            "s": "с",
            "sch": "щ",
            "sh": "ш",
            "t": "т",
            "u": "ю",
            "v": "в",
            "y": "Ы",
            "ya": "я",
            "yo": "ё",
            "z": "з",
            "zh": "ж",
            ",": "",
            "?": "",
            " ": "_",
            "~": "",
            "!": "",
            "@": "",
            "#": "",
            "$": "",
            "%": "",
            "^": "",
            "&": "",
            "*": "",
            "(": "",
            ")": "",
            "-": "",
            "=": "",
            "+": "",
            ":": "",
            ";": "",
            "<": "",
            ">": "",
            "'": "",
            '"': "",
            "\\": "",
            "/": "",
            "№": "",
            "[": "",
            "]": "",
            "{": "",
            "}": "",
            "ґ": "",
            "ї": "",
            "є": "",
            "Ґ": "g",
            "Ї": "i",
            "Є": "e",
            "—": "",
        },
    }
    if lang not in associations:
        raise ValueError("Unknown language")
    # Циклически заменяем все буквы в строке
    for key in associations[lang]:
        name = name.replace(key, associations[lang][key])
    return name.lower()
