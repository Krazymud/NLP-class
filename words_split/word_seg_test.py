# encoding=utf-8
import re
import jieba.posseg as pseg
# 加载字典
def load_word_list() -> None:
	max_length = 0
	word_dict = set()
	for line in open('./data/corpus.dict.txt',encoding='utf-8',errors='ignore').readlines():
		tmp = len(line)
		if(max_length < tmp):
			max_length = tmp
		word_dict.add(line.strip())
	return {
	 		'max_length':max_length,
	 		'word_dict':word_dict
	 		}

def load_ans() -> None:
	ans_dict = []
	for line in open('./data/corpus.standard.txt',encoding='utf-8',errors='ignore').readlines():
		for word in line.split():
			ans_dict.append(word)
	return ans_dict

wordDict = load_word_list()
ansDict = load_ans()
wordlist1 = []
wordlist2 = []
wordlist = []

# 最大正向匹配
def max_left_match(line) -> None:
	m = len(line) if wordDict['max_length'] > len(line) else wordDict['max_length']
	n = 0
	while n < len(line):
		while line[n:m] not in wordDict['word_dict'] and m > n + 1:
			m -= 1
		wordlist1.append(line[n:m])
		n = m
		m = len(line) if n + wordDict['max_length'] > len(line) else wordDict['max_length'] + n

# 逆向匹配
def max_right_match(line) -> None:
	tmpList = []
	m = len(line)
	n = 0 if wordDict['max_length'] > len(line) else len(line) - wordDict['max_length']
	while m > 0:
		while line[n:m] not in wordDict['word_dict'] and n < m - 1:
			n += 1
		tmpList.append(line[n:m])
		m = n
		n = 0 if wordDict['max_length'] > m else m - wordDict['max_length']
	tmpList.reverse()
	for w in tmpList:
		wordlist2.append(w)

# 双向匹配
def max_match(line) -> None:
	tmpList1 = []
	m = len(line) if wordDict['max_length'] > len(line) else wordDict['max_length']
	n = 0
	while n < len(line):
		while line[n:m] not in wordDict['word_dict'] and m > n + 1:
			m -= 1
		tmpList1.append(line[n:m])
		n = m
		m = len(line) if n + wordDict['max_length'] > len(line) else wordDict['max_length'] + n
	
	tmpList2 = []
	m = len(line)
	n = 0 if wordDict['max_length'] > len(line) else len(line) - wordDict['max_length']
	while m > 0:
		while line[n:m] not in wordDict['word_dict'] and n < m - 1:
			n += 1
		tmpList2.append(line[n:m])
		m = n
		n = 0 if wordDict['max_length'] > m else m - wordDict['max_length']
	tmpList2.reverse()

	if len(tmpList1) >= len(tmpList2):
		for w in tmpList2:
			wordlist.append(w)
	else:
		for w in tmpList1:
			wordlist.append(w)

# 评估
def assess() -> float:
	ansList = []
	wordlist1_tmp = []
	wordlist2_tmp = []
	wordlist_tmp = []
	length = 0
	for w in ansDict:
		ansList.append([length, length + len(w)])
		length += len(w)
	length = 0
	for w in wordlist1:
		wordlist1_tmp.append([length, length + len(w)])
		length += len(w)
	length = 0
	for w in wordlist2:
		wordlist2_tmp.append([length, length + len(w)])
		length += len(w)
	length = 0
	for w in wordlist:
		wordlist_tmp.append([length, length + len(w)])
		length += len(w)
	
	count = 0
	for w in wordlist1_tmp:
		if w in ansList:
			count += 1
	fmm_measure = (2 * (count / len(wordlist1_tmp)) * (count / len(ansList))) / ((count / len(wordlist1_tmp)) + (count / len(ansList)))
	count = 0
	for w in wordlist2_tmp:
		if w in ansList:
			count += 1
	bmm_measure = (2 * (count / len(wordlist2_tmp)) * (count / len(ansList))) / ((count / len(wordlist2_tmp)) + (count / len(ansList)))
	count = 0
	for w in wordlist_tmp:
		if w in ansList:
			count += 1
	measure = (2 * (count / len(wordlist_tmp)) * (count / len(ansList))) / ((count / len(wordlist_tmp)) + (count / len(ansList)))
	return [fmm_measure, bmm_measure, measure]


# 去标点
def del_punc(data) -> str:
	string = re.sub("[！？。；“”＃‘（）《》、*+，-]", "", data)
	return string

# 测试
def main():
	words = []
	# 三种方法分词
	for line in open('./data/corpus.sentence.txt',encoding='utf-8',errors='ignore').readlines():
		newline = del_punc(line.strip())
		words.append(pseg.cut(newline))
		max_left_match(newline)		#fmm
		max_right_match(newline)	#bmm
		max_match(newline)			#combine
	out1 = open('./data/corpus.out.fmm.txt', 'w', encoding='utf-8')
	out2 = open('./data/corpus.out.bmm.txt', 'w', encoding='utf-8')
	out3 = open('./data/corpus.out.txt', 'w', encoding='utf-8')
	for w in wordlist1:
		out1.write(w)
		out1.write('\n')
	for w in wordlist2:
		out2.write(w)
		out2.write('\n')
	for w in wordlist:
		out3.write(w)
		out3.write('\n')
	res = assess()
	print("result for fmm: ", res[0])
	print("result for bmm: ", res[1])
	print("result for combined-measure: ", res[2])
	print('\n')

	# 输出词性标注
	out4 = open('./data/corpus.pos.txt', 'w', encoding='utf-8')
	for w in words:
		for word, flag in w:
			out4.write(word)
			out4.write(' ')
			out4.write(flag)
			out4.write('\n')


if __name__ == '__main__':
	main()