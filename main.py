
import string
from Token import Tokens
from Elements import Symbol,KeyWord,integerNum,desimalNum,Hex,Doubles_OPERATORS,Single_OPERATORS
from prettytable import PrettyTable

charID = {x for x in string.ascii_letters + string.digits + '_'}
start_charID  = {x for x in string.ascii_letters + '_'}
SHOW_WHITESPACES = False
prettytableList:list = []
def find_id(text: str, startindex: int):
    result = ''
    if text[startindex] not in start_charID:
        return None

    while startindex < len(text) and text[startindex] in charID :
        result += text[startindex]
        startindex += 1

    if result and result not in KeyWord:
        return Tokens(lexeme=result, token="T_Id", index=startindex)

    return None


def find_keyword(text: str, startindex: int):
    result = ''

    while startindex < len(text) and text[startindex] in charID :
        result += text[startindex]
        startindex += 1

    if result and result in KeyWord:
        return Tokens(lexeme=result, token=KeyWord[result], index=startindex)

    return None


def find_comments(text: str, startindex: int):
    is_comment = text[startindex: startindex + 2] == '//'
    if not is_comment:
        return None

    result = ''

    while startindex < len(text) and text[startindex] != '\n':
        result += text[startindex]
        startindex += 1

    if result and text[startindex] == '\n':
        return Tokens(lexeme=result, token='T_Comment', index=startindex)

    return None


#دسیمال در مقادیر عددی
def find_decimal(text, startindex):

    if text[startindex] not in integerNum :
        return None

    sign = ''
    if text[startindex] in ['-', '+']:
        sign = text[startindex]
        startindex += 1

    result = ''


    while startindex < len(text):
        if text[startindex] in desimalNum:
            result += text[startindex]
            startindex += 1
        else:
            break

    if not result:
        return None

    else:
        return Tokens(lexeme=sign + result, token='T_Decimal', index=startindex)

#هگزا دسیمال در مقادیر عددی
def find_hex(text, startindex):
    hex_sign = text[startindex: startindex + 2]
    is_hex = hex_sign in ['0x', '0X']
    if not is_hex:
        return None
    else:
        startindex += 2


    result = ''

    while startindex < len(text):
        if text[startindex].lower() in Hex:
            result += text[startindex]
            startindex += 1
        else:
            break

    if not result:
        return None


    else:
        lexeme = hex_sign + result
        return Tokens(lexeme=lexeme, token='T_Hexadecimal', index=startindex)


def find_single_char(text, startindex):
    if text[startindex] != "'":
        return None

    startindex += 1
    result = ''
    while startindex < len(text) and text[startindex] != "'":
        char = text[startindex]
        result += char
        if char == '\\':
            startindex += 1
            result += text[startindex]

        startindex += 1

    if startindex < len(text) and text[startindex] == "'" \
            and (len(result) in [0, 1] or (len(result) == 2 and result[0] == '\\')):

        startindex += 1
        return Tokens(lexeme="'" + result + "'", token='T_Character', index=startindex)

    return None


def find_string(text, startindex):
    if startindex == 271:
        pass
    if text[startindex] != '"':
        return None

    startindex += 1
    result = ''
    while startindex < len(text) and text[startindex] != '"':
        char = text[startindex]
        result += char
        if char == '\\':
            startindex += 1
            result += text[startindex]

        startindex += 1

    if startindex < len(text) and text[startindex] == '"':
        startindex += 1
        return Tokens(lexeme='"' + result + '"', token='T_String', index=startindex)

    return None


def create_operator_finder_function(operator, token_type):
    def finder_function(text, startindex):
        result = ''
        for i in range(len(operator)):
            if startindex >= len(text):
                return None
            result += text[startindex]
            startindex += 1

        if result == operator:
            return Tokens(lexeme=operator, token=token_type, index=startindex)

        return None

    return finder_function


def find_whitespaces(text, startindex):
    result = ''
    while startindex < len(text) and text[startindex] in string.whitespace:
        result += text[startindex]
        startindex += 1

    if not len(result):
        return None

    return Tokens(lexeme=result, token='T_Whitespace', index=startindex)


def main(text, start_index):
    function_list = [
        find_keyword,
        find_id,
        find_comments,
        find_hex,
        find_decimal,
        find_single_char,
        find_string,
        find_whitespaces,
    ]
    table = PrettyTable()
    str = ''
    global prettytableList


    for key, value in Doubles_OPERATORS.items():
        function_list.append(create_operator_finder_function(key, value))

    for key, value in Single_OPERATORS.items():
        function_list.append(create_operator_finder_function(key, value))

    for key, value in Symbol.items():
        function_list.append(create_operator_finder_function(key, value))

    while start_index < len(text):
        token_founded = False
        for func in function_list:
            token = func(text, start_index)
            if token is not None:
                if (token.token == "T_Whitespace" and not SHOW_WHITESPACES):
                   str+=f"{token.index}: whitespace -> {token.token}"
                   prettytableList.append([token.index,'whitespace', token.token])

                else:
                    str+=f"{token.index}: {token.lexeme} -> {token.token}"
                    prettytableList.append([token.index,token.lexeme, token.token])

                start_index = token.index
                token_founded = True
                break

        if not token_founded:
            print(f"index={start_index}: Invalid code!")
            break

    for row in prettytableList:
        table.add_row(row)

    # Print the table
    print(table)


if __name__ == "__main__":
    #read file
    with open("test1.txt", 'r') as file:
        text = file.read()

    main(text, 0)
