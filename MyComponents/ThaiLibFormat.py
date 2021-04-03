
# Data associated with a primary thai word in khru Bo vocabulary files
class DatVocKruBo:
    def __init__(self, lesson, indx, sub_indx,voc_th, voc_eng):
        self.lesson = lesson                        # Lesson counter
        self.indx = indx                            # Word counter = vocabulary file index of primary word
        self.sub_indx = sub_indx                    # Word sub-counter = counter of associated words
        self.voc_th = voc_th                        # Thai words @ counter @ sub-counter [list]
        self.voc_eng = voc_eng                      # Eng translations of words @ counter @ sub-counter [list of list]

    def flush(self):
        def __init__(self):
            members = [getattr(self, attr) for attr in dir(self) if not attr.startswith("__")]
            print (members)


# String data handling for Kru Bo vocabulary imports.
class VocabularyKruBoLesson:
    def __init__(self, str_raw):
        self.str_raw = str_raw                      # Input raw string. Usually copy/past from pdf
        self.line_list = []                         # List of lines in input strings
        self.line_list_len = 0                      # Number of lines in line_List
        self.block_list = []                        # List of word blocks
        self.data_list = []

    # Split input string into list of lines
    def str_lines(self):
        self.line_list=self.str_raw.splitlines()
        self.line_list_len=len(self.line_list)

    # Look in input string ("self.str_raw") for sequences of len>1 of the string
    # search_substr, and replaces said sequences with sequence of the same length of the
    # replacement string rep_substr.
    def replace_rep_str(self, search_substr, rep_substr):
        in_str_buff = []
        # Transfer input string to a list buffer. String thus transformed to list of characters
        for lett in self.str_raw:
            in_str_buff.append(lett)

        # Initialize tracking variables
        i = 0
        seq_beg = 0
        seq_end = 0
        seq_on = False

        # Start for loop over length of in_str_buff
        for j in range(len(in_str_buff)):

            # search_substr detected at current position...
            if in_str_buff[j] == search_substr:

                # First occurrence of search_substr
                if not seq_on:
                    seq_beg = j                     # Store start pointer of sequence
                    seq_end = j                     # Update end pointer of sequence
                    seq_on = True                   # Switch flag seq_on, position is in sequence
                else:
                    seq_end = j                     # Update end pointer

            # ...search_substr not detected at current position
            else:

                # seq_on flag is ON, meaning a sequence of search_substr has just ended
                if seq_on:

                    # Sequence had length > 1, and thus must be replaced.
                    if seq_end - seq_beg > 0:
                        # Replace sequence by sequence of character "rep_substr"
                        for k in range(seq_beg, seq_end + 1):
                            in_str_buff[k] = rep_substr
                    # Update seq_beg, seq_end, flag according to situation
                    seq_beg = j
                    seq_end = j
                    seq_on = False

        # Catch special case of input string ending with "search_substr"
        if seq_end - seq_beg > 0:
            for k in range(seq_beg, seq_end + 1):
                in_str_buff[k] = rep_substr

        # Map list buffer back onto a string
        out_str = ""
        for k in range(len(in_str_buff)):
            out_str = out_str + in_str_buff[k]

        # Return output string
        return out_str

    # Find lesson number in vocabulary. Specific to khru Bo vocabulary.
    def lesson(self):
        lesson = self.line_list[0].split(" ")[1]    # Split lesson number from header line
        return lesson

    # Construct the list "block_list", a list of lists of lines
    # which are referred to as "vocabulary blocks". Each "vocabulary block" corresponds to one
    # primary Thai word.
    def vocabulary_block_decompose(self):
        self.block_list=[]                          # Initialize list of "blocks"
        block=[]                                    # Initialize block buffer
        block_ctr=0                                 # Initialize block counter
        line_ctr=1                                  # Initialize line_ctr to first line after header

        # Scan through lines until "…" is detected (khru Bo marker for EOI)
        while self.line_list[line_ctr][0] != "…":

            # If first character of line is decimal -> Increment block index
            if self.line_list[line_ctr][0].isdecimal():

                # Buffer not empty means it cannot be first block. Transfer buffer to block_list.
                if len(block) != 0:
                    self.block_list.append(block)   # Append block to block list
                    block_ctr+=1                    # Increment block counter
                    block = []                      # Empty block buffer
                    block=[self.line_list[line_ctr]] # Initialize block with current line

                # Block buffer empty. Thus very first block.
                else:
                    block.append(self.line_list[line_ctr])

            # First character of line is NOT decimal. Current line NOT first line of block
            else:
                block.append(self.line_list[line_ctr])
            line_ctr+=1

        # Last block must be appended separately because loop terminates prior
        self.block_list.append(block)

    # Decompose block lists into data clusters, each corresponding to one thai word,
    # and each such cluster organized according to data type VocKruBo.
    def block_data(self):

        buff = DatVocKruBo("", "", "", "", "")      # Define buffer of data type "VocKruBo"
        s = []                                      # Collection of data type "VocKruBo"

        # Run over collection of vocabulary blocks
        for blocks in self.block_list:

            buff.lesson=self.lesson()               # Read lesson counter in header line of vocabulary file.
            buff.sub_indx = []                      # Initialize collection of sub-entry indices
            buff.voc_th = []                        # Initialize collection of thai words
            buff.voc_eng = []                       # Initialize collection of english translation collections
            i = 0                                   # Line counter of current block

            # Run over lines in current block
            for block_lines in blocks:

                # Line is first line in a block
                if i==0:
                    # Read main vocabulary counter
                    buff.indx = block_lines.split(". ")[0]
                    # Read leading Thai vocabulary item
                    buff.voc_th.append(block_lines.split(". ")[1].split(" ")[0])
                    # Append list of translation of leading Thai vocabulary item (ignore phonetic string)
                    buff.voc_eng.append(block_lines.split(". ")[1].split(" ",2)[2].split(","))
                    # Append to sub_index a value = 0, as i==0 corresponds to the first line in the block
                    buff.sub_indx.append(0)

                # i != 0, i.e. the current line of the block corresponds to secondary vocabulary item.
                else:
                    # Regular situation : block line, split by " " contains 3 elements (Thai Wrd, phonetics,english)
                    if len(block_lines.split(" ",2)) == 3:
                            buff.voc_eng.append(block_lines.split(" ",2)[2].split(","))
                    # Exception : No english translation given => apply translation of previous line
                    else:
                        buff.voc_eng.append(buff.voc_eng[i-1],)
                    # Add first substring to Thai items
                    buff.voc_th.append(block_lines.split(" ",2)[0])
                    buff.sub_indx.append(i)
                #s.append(Dat_voc_khru_bo(buff.lesson, buff.indx, buff.sub_indx, buff.voc_th, buff.voc_eng))
                i=i+1

            # Append latest record DatVocKhruBo
            s.append(DatVocKruBo(buff.lesson, buff.indx, buff.sub_indx, buff.voc_th, buff.voc_eng))

        # for v in s:
        #    print(v.lesson, v.indx, v.sub_indx, v.voc_th, v.voc_eng)
        return s


# Declare string as instance of data container
string = VocabularyKruBoLesson("""Vocabulary 15
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
………………………………………………………………………………..""")

# Replace sequences of >1 "." with sequence of "-" of equal length
string.str_raw = string.replace_rep_str(".","-")
# Split raw data input string str_raw into lines
string.str_lines()
# Decompose raw input string into "vocabulary blocks"
string.vocabulary_block_decompose()
# Decompose vocabulary blocks into data clusters and print result
for v in string.block_data():
    print(v.lesson, v.indx, v.sub_indx, v.voc_th, v.voc_eng)