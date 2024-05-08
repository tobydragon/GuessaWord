
def create_individual_word_count_map(filepath):
	with open(filepath, "r", encoding="utf8") as word_file:
		lines = word_file.readlines()
	word_map = {}
	for line in lines:
		for word in line.split():
			if word in word_map:
				word_map[word] += 1
			else:
				word_map[word] = 1
	return word_map


def find_words_with_lettercount(word_map, count):
	return [word for word in word_map if len(word) == count and word.isalpha()]


def main():
	# this word list from: https://github.com/meetDeveloper/freeDictionaryAPI
	print(find_words_with_lettercount(create_individual_word_count_map("data/english.txt"), 5))


main()
