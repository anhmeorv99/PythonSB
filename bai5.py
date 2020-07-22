# Urbina cho rằng Trump khó có thể "hạ bệ" Biden.
# "Nếu bạn nhìn vào những nơi Trump đánh mất ủng hộ và nơi mà Biden đang giành được điều đó,
# cựu phó tổng thống Mỹ đang tạo ra sự ủng hộ liên tục và sâu rộng", Urbina nói.
import re


def find_tokens_1(paragraph_token):
    string_encode = ''.join(paragraph_token)
    results = re.findall(r'1{1,}', string_encode)
    if string_encode[0:2] == '10':
        results.pop(0)
    return results


def find_tokens_10(paragraph_token):
    string_encode = ''.join(paragraph_token)
    results = []
    while re.search(r'(10){2,}', string_encode)!=None:
        string_temp = ''
        result = re.search(r'(10){2,}', string_encode)
        results.append(result.group())
        for i in range(len(result.group())):
            string_temp += 'x'
            string_encode = string_encode.replace(result.group(),string_temp)
    #print(results)
    return results


def sentence_string(paragraph):
    if paragraph != '':
        return paragraph.split('.')
    else:
        return []


def sentence_tokens(sentence):
    if sentence != '':
        return sentence.split()
    else:
        return []


def encode_string(sentence):
    result = []
    if sentence != '':
        tokens = sentence_tokens(sentence)
        for token in tokens:
            if token == '':
                result.append('x')
            elif token[0].isupper() or token[0] == '\"' or token[-1] == '\"':
                result.append('1')
            else:
                result.append('0')
    return result


def encode_sentence(paragraph):
    paragraph_token = []
    for sentence in paragraph:
        result = encode_string(sentence)
        paragraph_token.append(result)
    return paragraph_token


def decode_key_word_1(paragraph_token, sentence, results):
    result_set = set()
    string_encode = ''.join(paragraph_token)
    if string_encode[0:2] == '10':
        string_encode = string_encode.replace('10', 'x0', 1)

    for result in results:
        string_temp = ''
        if result != '':

            index = string_encode.find(result)

            if len(result) > 1:
                string_result = ' '.join(sentence[index:index + len(result)])

                result_set.add(string_result)
                for i in range(index, index + len(result)):
                    string_temp += 'x'
                string_encode = string_encode.replace(result, string_temp, 1)
            elif len(result) == 1:
                result_set.add(sentence[index])
                string_encode = string_encode.replace(result, 'x', 1)
    # print(string_encode)
    return result_set


def decode_key_word_10(paragraph_token, sentence, results):
    result_set = set()
    string_encode = ''.join(paragraph_token)

    for result in results:
        string_temp = ''
        if result != '':
            index = string_encode.find(result)
            string_result = ' '.join(sentence[index:index + len(result)])

            result_set.add(string_result)
            for i in range(index, index + len(result)):
                string_temp += 'x'
            string_encode = string_encode.replace(result, string_temp, 1)

    return result_set

paragraph = "\"Khả năng xảy ra khủng hoảng hậu Bầu Cử chưa từng thấy ở nước Mỹ là khá lớn\", Larry Diamond, chuyên gia về các thể chế dân chủ tại Viện Hoover, tổ chức nghiên cứu bảo thủ ở Stanford, California, Mỹ, phát biểu trong một cuộc phỏng vấn gần đây với CNN."
sentences = sentence_string(paragraph)
binary_sentences = encode_sentence(sentences)

for x, s in enumerate(sentences):
    sentence = sentence_tokens(s)
    end_result = decode_key_word_1(binary_sentences[x], sentence, find_tokens_1(binary_sentences[x]))
    end_result1 = decode_key_word_10(binary_sentences[x], sentence, find_tokens_10(binary_sentences[x]))
    print(end_result)
