
# Data element in vocabulary
class Dat_voc_khru_bo:
    def __init__(self, lesson, indx, sub_indx,voc_th, voc_eng):
        self.lesson = lesson        # Lesson counter
        self.indx  = indx           # Word counter
        self.sub_indx = sub_indx    # Word sub-counter
        self.voc_th = voc_th        # Thai word @ counter @ sub-counter (list)
        self.voc_eng = voc_eng      # Eng translations of word @ counter @ sub-counter (list of list)

    def flush(self):
        def __init__(self):
            members = [getattr(self, attr) for attr in dir(self) if not attr.startswith("__")]
            print (members)

# Input/output data construct.
# str_raw = input string, usually copy/paste from pdf. May be lesson vocab., lesson homework,
# Patreaon, etc.
class StrData:
    def __init__(self, str_raw, line_list, line_list_len, block_list, data_list):
        self.str_raw = str_raw
        self.line_list = line_list
        self.line_list_len = line_list_len
        self.block_list = block_list
        self.data_list = data_list

    # Raw String split into lines + Number of lines
    def str_lines(self):
        self.line_list=self.str_raw.splitlines()
        self.line_list_len=len(self.line_list)

    # Replaces in input string in_str the substring consisting
    # of repetitive string "search_substr" with
    # string of equal length of repetitive rep_substr.
    def replace_rep_str(self, search_substr, rep_substr):
        in_str_buff = []
        # Transfer in string to list buffer
        for lett in self.str_raw:
            in_str_buff.append(lett)
        i = 0
        seq_beg = 0
        seq_end = 0
        seq_on = False
        for j in range(len(in_str_buff)):
            if in_str_buff[j] == search_substr:
                if not seq_on:
                    seq_beg = j
                    seq_end = j
                    seq_on = True
                else:
                    seq_end = j
            else:
                if seq_on:
                    if seq_end - seq_beg > 0:
                        for k in range(seq_beg, seq_end + 1):
                            in_str_buff[k] = rep_substr
                    seq_beg = j
                    seq_end = j
                    seq_on = False
        if seq_end - seq_beg > 0:
            for k in range(seq_beg, seq_end + 1):
                in_str_buff[k] = rep_substr
        out_str = ""
        for k in range(len(in_str_buff)):
            out_str = out_str + in_str_buff[k]
        return out_str


# Code specific to vocabulary input, khru Bo.
# Extract a list of "Dat_voc_khru_bo" objects, each of them belonging
# to a vocabulary entry.
class Voc_khru_bo(StrData):
    def __init__(self, str_raw, line_list, line_list_len, block_list, data_list):
        super().__init__(str_raw, line_list, line_list_len, block_list, data_list)

    # Find lesson number in vocabulary. Specific to khru Bo vocabulary.
    def lesson(self):
        lesson = self.line_list[0].split(" ")[1]
        return lesson

    # Extract the list "block_list", a collection of lists of lines
    # which are referred to as "blocks". Each "block" corresponds in khru Bo's
    # lesson vocabulary format to one thai key word.
    def blocks(self):
        # Code specific to vocabulary input, khru Bo.
        # Each list of lines corresponds to one word
        self.block_list=[]
        block=[]
        block_ctr=0
        line_ctr=1
        while self.line_list[line_ctr][0] != "…":
            # First character in line = Dec -> Block Increment
            if self.line_list[line_ctr][0].isdecimal():
                # Block Buffer (block) nicht leer bedeutet block gehört nicht zu erstem Block
                if len(block) != 0:
                    # Block Buffer and block_list anhängen, block leeren, block_ctr inkrementieren
                    self.block_list.append(block)
                    block=[]
                    block_ctr+=1
                    block=[self.line_list[line_ctr]]
                else:
                    # Block buffer empty. This can only happen in very first block.
                    block.append(self.line_list[line_ctr])
            else:
                # First charcter in line != Dec -> line is not first line of buffer
                block.append(self.line_list[line_ctr])
            line_ctr+=1
        # Last block must be appended separately because loop terminates prior
        self.block_list.append(block)

    # Decompose blocks into data clusters, each corresponding to one thai word
    # Assumption data formatted according to lesson vocabulary khru Bo (template)
    def block_data(self):
        # buff is a container for vocabulary counter in vocabulary file, sub-counter,
        # thai word, english translations.
        buff = Dat_voc_khru_bo("", "", "", "", "")
        s = []
        # Run over collection (list) of blocks
        for blocks in self.block_list:
            # Read lesson counter in header line of vocabulary file.
            buff.lesson=self.lesson()
            # .sub_index is a list of sub-indices. Each sub-index belongs to a sub-entry
            # (lines in block) below the main vocabulary item (1st line in block).
            buff.sub_indx = []
            # Thai vocabulary belonging to main vocabulary are collected in list .voc_th.
            # Each item in list corresponds to one sub-entry (lines in block) below the main vocabulary item
            # (1st line in block).
            buff.voc_th = []
            # For each Thai vocabulary sub-entry there will be a list of translations.
            buff.voc_eng = []
            # Line counter of current block
            i = 0
            for block_lines in blocks:
                # Line is first line in a block
                if i==0:
                    # Read main vocabulary counter
                    buff.indx = block_lines.split(". ")[0]
                    # Read leading Thai vocabulary item
                    buff.voc_th.append(block_lines.split(". ")[1].split(" ")[0])
                    # Append list of translation of leading Thai vocabulary item
                    buff.voc_eng.append(block_lines.split(". ")[1].split(" ",2)[2].split(","))
                    # Append sub_index value = 0 as i==0 corresponds to the first line in the block
                    buff.sub_indx.append(0)
                # i != 0, i.e. the current line of the block corresponds to secondary vocabulary item.
                else:
                    # Catch case that less than 3 items result on split.
                    if len(block_lines.split(" ",2)) == 3:
                            buff.voc_eng.append(block_lines.split(" ",2)[2].split(","))
                    else:
                        buff.voc_eng.append(buff.voc_eng[i-1],)
                    # Add first substring to Thai items
                    buff.voc_th.append(block_lines.split(" ",2)[0])
                    buff.sub_indx.append(i)
                #s.append(Dat_voc_khru_bo(buff.lesson, buff.indx, buff.sub_indx, buff.voc_th, buff.voc_eng))
                i=i+1
            s.append(Dat_voc_khru_bo(buff.lesson, buff.indx, buff.sub_indx, buff.voc_th, buff.voc_eng))
        for v in s:
            print(v.lesson, v.indx, v.sub_indx, v.voc_th, v.voc_eng)


# Declare string as instance of data container
string = Voc_khru_bo("""Vocabulary 15
1. กำลังจะ gam-lang-jà to be going to,to be about to
2. ...แรก …râek first
...ที่สอง …têe-sǒrng second
3. คง(จะ) kong(jà) might,may, possibly,probably
4. เกือบ gèuap almost,nearly
5. หลำย… lǎai… many
6. ก่อน..... gòrn.... before (doing something)
.....ก่อน ....gòrn previous,former,first
7. เมื่อก่อน mêua-gòrn before,in the past
แต่ก่อน dtàe-gòrn
8. หลังจำก... lǎng-jàak.... after (doing something)
หลังจำกนั้น lǎng-jàak-nán after that
9. ตอนสำยๆ dtorn-sǎai-sǎai late in the morning
10. ตอนค่ำๆ dtorn-kâm-kâm about 7 – 8 pm.
11. ดึก dèuk late at night
12. ตอนกลำงวัน dtorn-glaang-wan daytime
13. ตอนกลำงคืน dtorn-glaang-keun nighttime
14. เดี๋ยวนี้ dǐao-née right now, nowadays
15. ตรงนี้ dtrong-née right here
16. นัด nát to make an appointment
มีนัด mee-nát to have an appointment
17. ขำย kǎai to sell
18. เก็บ gèp to keep,to collect,to save
เก็บไว้ gèp-wái to save something for future use
เก็บ....ไว้ gèp…wái
19. บ่น bòn to grumble, to mutter
20. แน่ใจ nâe-jai sure (I am sure.)
แน่นอน nâe-norn sure,for sure,certain,of course
21. สั้น sân short (measurement), shortly
22. ยำว yaao long (measurement)
23. นำน naan long (time)
24. ใจดี jai-dee kind
25. ใจเย็น jai-yen calm
26. ใจร้อน jai-rórn hot-tempered
27. หัวหน้ำ hǔa-nâa boss,leader
28. โรงงำน roong-ngaan factory
29. โรงหนัง roong-nǎng cinema
30. มหำวิทยำลัย ma-hǎa-wít-ta-yaa-lai university
อำจำรย์ aa-jaan teacher,instructor,professor
นักศึกษำ nák-sèuk-sǎa university student
………………………………………………………………………………..
………………………………………………………………………………..
………………………………………………………………………………..""", "", "", "", "")
string.str_raw = string.replace_rep_str(".","-")
# Split raw data input string str_raw into lines
string.str_lines()
# Decompose raw input string into vocabulary blocks
string.blocks()
# Dcompose vocabulary blocks into data clusters
string.block_data()





