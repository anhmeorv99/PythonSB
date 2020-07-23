# Urbina cho rằng Trump khó có thể "hạ bệ" Biden.
# "Nếu bạn nhìn vào những nơi Trump đánh mất ủng hộ và nơi mà Biden đang giành được điều đó,
# cựu phó tổng thống Mỹ đang tạo ra sự ủng hộ liên tục và sâu rộng", Urbina nói.
import re


def find_tokens_1(paragraph_token):                         # Tìm token có dạng 1,11,111,1111...
    string_encode = ''.join(paragraph_token)
    results = re.findall(r'1{1,}', string_encode)
    if string_encode[0:2] == '10':
        results.pop(0)
    return results


def find_tokens_10(paragraph_token):                    #tìm token dạng 1010, 101010,....
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


def sentence_string(paragraph):                     # cắt đoạn văn thành các câu
    if paragraph != '':
        return paragraph.split('.')
    else:
        return []


def sentence_tokens(sentence):                  #cắt câu văn thành các từ tố
    if sentence != '':
        return sentence.split()
    else:
        return []


def encode_string(sentence):                    #mã hóa các đoạn token (câu) thành dạng 0,1 . nếu phần tử đầu có dấu " thì vẫn mã hóa là 1
    result = []
    if sentence != '':
        tokens = sentence_tokens(sentence)
        for index,token in enumerate(tokens):
            if token == '':
                result.append('x')
            elif token[0].isupper():
                result.append('1')
            elif  '\"' in token and index==0:
                result.append('1')
            else:
                result.append('0')
    return result


def encode_sentence(paragraph):             # mã hóa đoạn văn
    paragraph_token = []
    for sentence in paragraph:
        result = encode_string(sentence)
        paragraph_token.append(result)
    return paragraph_token


def decode_key_word_1(paragraph_token, sentence, results):                  # giải mã dạng 1,111,1111,...
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


def decode_key_word_10(paragraph_token, sentence, results):                 #giải mã đoạn 1010, 101010...
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


def replace_tokens(token):                              # chuẩn hóa token về dạng a_b_c....
    speacial_char = set(re.findall('\W', token))
    for s_char in speacial_char:
        token = token.replace(s_char,'_')
    return token


def encode_quotation(paragraph):                        # mã hóa đoạn văn có dấu "
    array_split_space = paragraph.split(' ') #can use sentence_tokens()
    for index,x in enumerate(array_split_space):                 #encode
        if '\"' in x:
            array_split_space[index] ='1'
        else:
            array_split_space[index] ='0'
    return array_split_space


def decode_quotation(list_token,list_encode_token):             #giải mã đoạn có dấu nháy và kiểm tra có >10 từ hay không?
    list_quotation_index = []
    list_quotation = []
    for index,token in enumerate(list_encode_token):
        if token == '1':
            list_quotation_index.append(index)
    for index in range(0,len(list_quotation_index)-1,2):
        if list_quotation_index[index+1] - list_quotation_index[index] < 9 :
            result = '_'.join(list_token[list_quotation_index[index]:list_quotation_index[index+1]+1])

            list_quotation.append(result)
    return list_quotation


def output(paragraph):
    sentences = sentence_string(paragraph)
    binary_sentences = encode_sentence(sentences)
    list_results = []  # kết quả của câu văn có chứa key_word
    for x, s in enumerate(sentences):
        sentence = sentence_tokens(s)
        end_result = decode_key_word_1(binary_sentences[x], sentence, find_tokens_1(binary_sentences[x]))
        end_result1 = decode_key_word_10(binary_sentences[x], sentence, find_tokens_10(binary_sentences[x]))
        if end_result != set() and end_result not in list_results:
            list_results.append(end_result)
        if end_result1 != set() and end_result not in list_results:
            list_results.append(end_result1)


    std_list_results = []
    for set_item in list_results:
        for item in set_item:
            item = replace_tokens(item)
            if item not in std_list_results:
                std_list_results.append(item)
    array_test = encode_quotation(paragraph)
    end_result2 = decode_quotation(sentence_tokens(paragraph), array_test)  # kết quả của đoạn có dấu nháy < 10

    for item in end_result2:
        item = replace_tokens(item)
        if item not in std_list_results:
            std_list_results.append(item)

    return std_list_results


paragraph = "Trước hết, hãy bắt đầu với VCS. VCS là gì? VCS là \"viết tắt\" của Version Control System \"viết tắt\" dịch là Hệ thống quản lý phiên bản. Sỡ dĩ được gọi như vậy là vì các VCS sẽ lưu trữ tất cả các file trong dự án và ghi lại toàn bộ lịch sử thay đổi của file, mỗi sự thay đổi được lưu lại sẽ được phiên bản hóathành một version (phiên bản). (Để ý giúp mình từ “được lưu lại”, mình sẽ giải thích thêm ở phần Commit)."


test = output(paragraph)
print(test)









