import autoit
import time
import re
import regex as re
#pip install -U pyautoit
class DownloadHD:
    def __init__(self):
        self.dicchar = None
        self.bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                    ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                    ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                    ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                    ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                    ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                    ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                    ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                    ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                    ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                    ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                    ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]
        self.bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

        self.nguyen_am_to_ids = {}
        self.uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
        self.unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"
       
    def PrintFile(self):
        autoit.send("^p",0)
        time.sleep(100000)
        autoit.send("{ENTER}",0)
        time.sleep(5)
        autoit.send(self.name,0)
        time.sleep(5)
        autoit.send("{ENTER}",0)
        time.sleep(10)
    
    def loaddicchar(self):
        self.dicchar = {}
        char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
            '|')
        charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
            '|')
        for i in range(len(char1252)):
            self.dicchar[char1252[i]] = charutf8[i]
        return self.dicchar

    def convert_unicode(self,txt):
        return re.sub(
            r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
            lambda x: self.dicchar[x.group()], txt)

    def vn_word_to_telex_type(self,word):
        for i in range(len(self.bang_nguyen_am)):
            for j in range(len(self.bang_nguyen_am[i]) - 1):
                self.nguyen_am_to_ids[self.bang_nguyen_am[i][j]] = (i, j)
                
        dau_cau = 0
        new_word = ''
        for char in word:
            x, y = self.nguyen_am_to_ids.get(char, (-1, -1))
            if x == -1:
                new_word += char
                continue
            if y != 0:
                dau_cau = y
            new_word += self.bang_nguyen_am[x][-1]
        new_word += self.bang_ky_tu_dau[dau_cau]
        return new_word


    def vn_sentence_to_telex_type(self,sentence):
        words = sentence.split()
        for index, word in enumerate(words):
            words[index] = self.vn_word_to_telex_type(word)
        return ' '.join(words)

    def chuan_hoa_dau_tu_tieng_viet(self,word):
        if not self.is_valid_vietnam_word(word):
            return word

        chars = list(word)
        dau_cau = 0
        nguyen_am_index = []
        qu_or_gi = False
        for index, char in enumerate(chars):
            x, y = self.nguyen_am_to_ids.get(char, (-1, -1))
            if x == -1:
                continue
            elif x == 9:  # check qu
                if index != 0 and chars[index - 1] == 'q':
                    chars[index] = 'u'
                    qu_or_gi = True
            elif x == 5:  # check gi
                if index != 0 and chars[index - 1] == 'g':
                    chars[index] = 'i'
                    qu_or_gi = True
            if y != 0:
                dau_cau = y
                chars[index] = self.bang_nguyen_am[x][0]
            if not qu_or_gi or index != 1:
                nguyen_am_index.append(index)
        if len(nguyen_am_index) < 2:
            if qu_or_gi:
                if len(chars) == 2:
                    x, y = self.nguyen_am_to_ids.get(chars[1])
                    chars[1] = self.bang_nguyen_am[x][dau_cau]
                else:
                    x, y = self.nguyen_am_to_ids.get(chars[2], (-1, -1))
                    if x != -1:
                        chars[2] = self.bang_nguyen_am[x][dau_cau]
                    else:
                        chars[1] = self.bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else self.bang_nguyen_am[9][dau_cau]
                return ''.join(chars)
            return word

        for index in nguyen_am_index:
            x, y = self.nguyen_am_to_ids[chars[index]]
            if x == 4 or x == 8:  # ê, ơ
                chars[index] = self.bang_nguyen_am[x][dau_cau]
                # for index2 in nguyen_am_index:
                #     if index2 != index:
                #         x, y = nguyen_am_to_ids[chars[index]]
                #         chars[index2] = bang_nguyen_am[x][0]
                return ''.join(chars)

        if len(nguyen_am_index) == 2:
            if nguyen_am_index[-1] == len(chars) - 1:
                x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[0]]]
                chars[nguyen_am_index[0]] = self.bang_nguyen_am[x][dau_cau]
                # x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
                # chars[nguyen_am_index[1]] = bang_nguyen_am[x][0]
            else:
                # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
                # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
                x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[1]]]
                chars[nguyen_am_index[1]] = self.bang_nguyen_am[x][dau_cau]
        else:
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
            x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = self.bang_nguyen_am[x][dau_cau]
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[2]]]
            # chars[nguyen_am_index[2]] = bang_nguyen_am[x][0]
        return ''.join(chars)


    def is_valid_vietnam_word(self,word):
        chars = list(word)
        nguyen_am_index = -1
        for index, char in enumerate(chars):
            x, y = self.nguyen_am_to_ids.get(char, (-1, -1))
            if x != -1:
                if nguyen_am_index == -1:
                    nguyen_am_index = index
                else:
                    if index - nguyen_am_index != 1:
                        return False
                    nguyen_am_index = index
        return True


    def chuan_hoa_dau_cau_tieng_viet(self,sentence):
        sentence = sentence.lower()
        words = sentence.split()
        for index, word in enumerate(words):
            cw = re.sub(r'(^\p{P})([p{L}.]\p{L}+)(\p{P}*$)', r'\1!@#\2!@#\3', word).split('!@#')
            #cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
            if len(cw) == 3:
                cw[1] = self.chuan_hoa_dau_tu_tieng_viet(cw[1])
            words[index] = ''.join(cw)
        return ' '.join(words)

        