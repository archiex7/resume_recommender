# -*- coding: utf-8 -*-
import logging
import platform
import os


class Logger:
    def __init__(self, name, log_file=None, log_level=logging.INFO):
        """
        Initialize the logger.

        Args:
            name (str): The name of the logger.
            log_file (str, optional): Path to the log file. If None, logs will be printed to console.
            log_level (int, optional): Logging level (e.g., logging.DEBUG, logging.INFO, etc.).
        """
        self.logger = logging.getLogger(name)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(log_level)

        # Create a formatter
        formatter = logging.Formatter('[%(asctime)s] - p%(process)s - { %(pathname)s:%(lineno)d - %(funcName)s - %(module)s } - %(name)s - %(levelname)s - %(message)s')

        # Create a handler (console or file)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, message, level=logging.INFO):
        """
        Log a message.

        Args:
            message (str): The log message.
            level (int, optional): Logging level (e.g., logging.DEBUG, logging.INFO, etc.).
        """
        self.logger.log(level, message)


def copy(from_path, to_path):
    os_system = platform.system().lower()
    if os_system == 'windows':
        os.system(f'copy {from_path} {to_path}')
        # print(f'copy from "{from_path}" to "{to_path}"')
    elif os_system == 'linux':
        os.system(f'cp {from_path} {to_path}')
        # print(f'cp from "{from_path}" to "{to_path}"')
    else:
        print(f'for os_system "{os_system}": not implemented yet!')


def full2half(ustring):
    """Convert full-width characters to half-width characters"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # Convert back to full-width if not in half-width range
            rstring += uchar
        else:
            rstring += chr(inside_code)
    return rstring


def half2full(ustring):
    """Convert half-width characters to full-width characters"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x0020:  # Space character
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        rstring += chr(inside_code)
    return rstring

# # Test the functions
# ustring = "ＡＢＣ１２３"
# print("Original full-width string:", ustring)
# print("Converted to half-width:", full2half(ustring))
# print("Converted back to full-width:", half2full(full2half(ustring)))


def convert_characters(text):
    # '⼤學' == '大學'  # False
    """
    The characters ‘⼤’ and ‘大’ are different in Unicode, which is why the comparison ‘⼤’ == ‘大’ returns False.

    ‘⼤’ is a CJK (Chinese, Japanese, Korean) Radicals Supplement character. Its Unicode code point is U+2F24.
    ‘大’ is a CJK Unified Ideographs character, often used in written Chinese and Japanese. Its Unicode code point is U+5927.
    Even though these characters may look similar or identical in some fonts, they are considered distinct characters in Unicode. Therefore, when you compare them using the == operator in Python, the result is False.
    """
    mapping = {
        '⼤': '大',
        '⼠': '士',
        '⾼': '高',
        '⼆': '二',
        '⽤': '用',
        '⾦': '金',
        '⾏': '行',
        '⼼': '心',
        '親': '親',
        '英': '英',
        '⼯': '工',
        '⺠': '民',
        '⼝': '口',
        # '⼯作經驗': '工作經驗',
        '⽇': '日',
        '⿊': '黑',
    }  # Add more mappings as needed
    return ''.join(mapping.get(c, c) for c in text)


def get_file_name(file_str):
    """split pdf file name to name"""
    name = file_str.split('_')[0]
    return name


def get_104_id(file_str):
    """split pdf file name to 104_id"""
    pid = file_str.split('_')[1]
    return pid


# text = '⼤學'
# converted_text = convert_characters(text)
# print(converted_text)  # Outputs: '大學'
#
# code_point = 0x2F24  # Unicode 碼點
# character = chr(code_point)
# print(character)  # '⼤'
#
# code_point = 0x5927  # Unicode 碼點
# character = chr(code_point)
# print(character)  # '大'


# in python, how can i convert similar characters from CJK Radicals Supplement characters to CJK Unified Ideographs characters?
# import unicodedata
# # Define your CJK Radicals Supplement character
# radical_supplement_char = '⻖'  # Get the name of the character
# name = unicodedata.name(radical_supplement_char)  # The name should be something like 'CJK RADICAL C-SIMPLIFIED TURTLE' # You can then replace 'RADICAL' with 'UNIFIED IDEOGRAPH' to get the corresponding ideograph
# ideograph_name = name.replace('RADICAL', 'UNIFIED IDEOGRAPH')  # Then you can use the unicodedata.lookup function to get the ideograph character
# ideograph_char = unicodedata.lookup(ideograph_name)
# # print(ideograph_char)
