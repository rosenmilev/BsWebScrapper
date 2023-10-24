from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import string
import pandas as pd


STOP_WORDS = {
	'english': [
		'with', 'myself', "she's", 'how', 'who', "mightn't", 'shouldn', 'own', "won't", 'why', 'under', 'then',
		'most', 'we', 'only', "should've", 'no', 'isn', 'those', 'was', 'through', 'they', 'of', 'while',
		'weren', 'she', 'herself', 'an', 'them', 'a', 'just', 'off', "you'll", 'be', 'did', 'once', "hasn't",
		'mightn', 'in', 'as', 't', 'him', 'because', 'is', 'what', 'll', 'same', 'wasn', 'over', "shan't",
		'whom', 'against', 'have', 'ain', "aren't", "haven't", 'me', 'her', 'you', 'hadn', 'until', 'ours',
		'nor', 'to', 'from', 'wouldn', 'out', "wouldn't", 'not', "you've", 'has', 'can', 'd', 'into', 'each',
		'y', 'some', "mustn't", 'more', 's', 'above', 've', 'haven', 'than', 'had', 'down', 'about', 'aren',
		'during', 'and', "you're", "needn't", 'below', 'again', 're', 'their', 'himself', "that'll", "wasn't",
		'all', 'very', 'on', "isn't", 'don', 'needn', 'theirs', "shouldn't", "didn't", 'its', 'are', 'won',
		'which', 'before', 'it', 'if', 'when', 'any', 'our', 'he', 'ourselves', 'further', 'such', 'so',
		'where', 'up', 'both', 'will', 'other', 'the', 'having', "it's", 'were', 'your', 'i', 'here', 'm',
		"hadn't", 'themselves', 'my', 'hers', 'his', 'between', 'doing', 'yours', 'hasn', 'mustn', 'ma', 'that',
		'or', 'few', 'for', "weren't", 'by', "you'd", 'being', 'yourselves', 'yourself', 'after', 'too',
		"don't", 'should', 'there', 'this', 'does', 'itself', 'doesn', 'at', 'these', 'shan', "couldn't",
		'didn', 'now', 'been', 'couldn', 'o', "doesn't", 'but', 'do', 'am'],
	'bulgarian': [
		"а", "автентичен", "аз", "ако", "ала", "бе", "без", "беше", "би", "бивш", "бивша",
		"бившо", "бил", "била", "били", "било", "благодаря", "близо", "бъдат", "бъде", "бяха",
		"в", "вас", "ваш", "ваша", "вероятно", "вече", "взема", "ви", "вие", "винаги", "внимава",
		"време", "все", "всеки", "всички", "всичко", "всяка", "във", "въпреки", "върху", "г", "ги",
		"главен", "главна", "главно", "глас", "го", "година", "години", "годишен", "д", "да", "дали",
		"два", "двама", "двамата", "две", "двете", "ден", "днес", "дни", "до", "добра", "добре",
		"добро", "добър", "докато", "докога", "дори", "досега", "доста", "друг", "друга", "други",
		"е", "евтин", "едва", "един", "една", "еднаква", "еднакви", "еднакъв", "едно", "екип",
		"ето", "живот", "за", "забавям", "зад", "заедно", "заради", "засега", "заспал", "затова",
		"защо", "защото", "и", "из", "или", "им", "има", "имат", "иска", "й", "каза", "как", "каква",
		"какво", "както", "какъв", "като", "кога", "когато", "което", "които", "кой", "който", "колко",
		"която", "къде", "където", "към", "лесен", "лесно", "ли", "лош", "м", "май", "малко", "ме",
		"между", "мек", "мен", "месец", "ми", "много", "мнозина", "мога", "могат", "може", "мокър",
		"моля", "момента", "му", "н", "на", "над", "назад", "най", "направи", "напред", "например", "нас",
		"не", "него", "нещо", "нея", "ни", "ние", "никой", "нито", "нищо", "но", "нов", "нова", "нови",
		"новина", "някои", "някой", "няколко", "няма", "обаче", "около", "освен", "особено", "от", "отгоре",
		"отново", "още", "пак", "по", "повече", "повечето", "под", "поне", "поради", "после", "почти",
		"прави", "пред", "преди", "през", "при", "пък", "първата", "първи", "първо", "пъти", "равен",
		"равна", "с", "са", "сам", "само", "се", "сега", "си", "син", "скоро", "след", "следващ", "сме",
		"смях", "според", "сред", "срещу", "сте", "съм", "със", "също", "т", "т.н.", "тази", "така",
		"такива", "такъв", "там", "твой", "те", "тези", "ти", "то", "това", "тогава", "този", "той",
		"толкова", "точно", "три", "трябва", "тук", "тъй", "тя", "тях", "у", "утре", "харесва", "хиляди",
		"ч", "часа", "че", "често", "чрез", "ще", "щом", "юмрук", "я", "як", "новини", "българия", 'ян', 'фев', 'мар',
		"апр", "април", "май", "юни", "юли", "авг", "август", "сеп", "септември", "окт", "октомври", "ное", "ноември",
		"дек", "декември", "януари", "февруари", "март", "новини", "спорт", "снимка", "снимки"
	]
}

PUNCTUATION = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
				'@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '...', "'", "``", "''"}

BULGARIAN_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъьюя'


# Tokenize all words in the scraped text
def tokenize_text_to_words(text):
	tokens = word_tokenize(text)
	return tokens


# Filter stop words, punctuation and words containing non-alphabetical symbols
def filter_words(tokens, language):
	filtered_tokens = [token.lower() for token in tokens if token.lower() not in PUNCTUATION]
	filtered_tokens = [token.lower() for token in filtered_tokens if token.lower() not in STOP_WORDS[language]]
	if language == 'bulgarian':
		filtered_tokens = [token.lower() for token in filtered_tokens if
						any(char in token.lower() for char in BULGARIAN_ALPHABET)]
	if language == 'english':
		filtered_tokens = [token.lower() for token in filtered_tokens if
						any(char in token.lower() for char in string.ascii_lowercase)]
	filtered_tokens = [token.lower() for token in filtered_tokens if not
						any(char in token.lower() for char in "`'.")]
	return filtered_tokens


# Determine 20 most used words and put them to dataframe
def get_keywords(tokens, n=20):
	freq_dist = FreqDist(tokens)
	main_keywords = freq_dist.most_common(n)
	return main_keywords
