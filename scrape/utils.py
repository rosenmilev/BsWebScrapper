from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import string
import pandas as pd


STOP_WORDS = {
	'english': {
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
		'didn', 'now', 'been', 'couldn', 'o', "doesn't", 'but', 'do', 'am'},
	'german': {
		'aus', 'habe', 'deinem', 'hier', 'vor', 'ihren', 'bist', 'allen', 'dort', 'sehr', 'uns', 'im', 'anderr',
		'das', 'wirst', 'auch', 'demselben', 'einigen', 'auf', 'ihr', 'was', 'für', 'welchem', 'hatten', 'weil',
		'um', 'über', 'als', 'waren', 'nichts', 'deiner', 'an', 'euer', 'unseren', 'während', 'würden', 'seines',
		'unseres', 'unter', 'jener', 'in', 'soll', 'alles', 'jedem', 'sind', 'sollte', 'aber', 'jede', 'nach',
		'durch', 'keine', 'derselben', 'einiger', 'zwischen', 'sonst', 'andere', 'er', 'gewesen', 'werde',
		'ihrer', 'alle', 'kann', 'meinen', 'welchen', 'weg', 'jeden', 'sein', 'wieder', 'unsere', 'eure', 'ein',
		'meinem', 'dieselben', 'jeder', 'meiner', 'von', 'nun', 'manche', 'hinter', 'machen', 'dies', 'dessen',
		'zwar', 'anderm', 'anders', 'die', 'bei', 'eurem', 'jenes', 'dann', 'dieses', 'mein', 'wollte', 'zu',
		'mit', 'haben', 'keinem', 'viel', 'deines', 'mich', 'würde', 'solche', 'weiter', 'welche', 'eures',
		'manchen', 'welches', 'hatte', 'euren', 'solchem', 'hin', 'manchem', 'seiner', 'keinen', 'mir', 'sich',
		'derer', 'also', 'einige', 'wenn', 'werden', 'dich', 'kein', 'etwas', 'jedes', 'desselben', 'warst',
		'daß', 'dem', 'denselben', 'es', 'eurer', 'gegen', 'deinen', 'ihm', 'jenen', 'jetzt', 'können',
		'mancher', 'ihrem', 'ander', 'keines', 'musste', 'anderes', 'so', 'unser', 'zum', 'meines', 'will',
		'nicht', 'des', 'dir', 'einigem', 'damit', 'hab', 'euch', 'solches', 'zur', 'seine', 'könnte', 'denn',
		'einem', 'einiges', 'ohne', 'sie', 'derselbe', 'ihres', 'diesen', 'dasselbe', 'deine', 'dieser', 'muss',
		'ich', 'ist', 'dein', 'dazu', 'du', 'vom', 'ins', 'solchen', 'bin', 'ihn', 'ihnen', 'meine', 'jene',
		'unserem', 'war', 'seinen', 'bis', 'seinem', 'einer', 'den', 'hat', 'sondern', 'wie', 'wo', 'der', 'wir',
		'noch', 'anderem', 'solcher', 'und', 'dieselbe', 'ihre', 'eines', 'jenem', 'einen', 'keiner', 'da',
		'nur', 'oder', 'allem', 'aller', 'einig', 'wird', 'anderen', 'welcher', 'ob', 'eine', 'man', 'manches',
		'wollen', 'doch', 'einmal', 'diesem', 'andern', 'dass', 'indem', 'anderer', 'selbst', 'diese', 'am'},
	'bulgarian': {
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
		"дек", "декември", "януари", "февруари", "март", "новини", "спорт"
	}
}

PUNCTUATION = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
				'@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '...', "'"}


# Tokenize all words in the scraped text
def tokenize_text_to_words(text):
	tokens = word_tokenize(text)
	filtered_tokens = [token.lower() for token in tokens if token.lower() not in PUNCTUATION]
	return filtered_tokens


# Filter the stop words and determine 20 most used words and put them to dataframe
def get_keywords(tokens, language, n=20):
	filtered_tokens = [token.lower() for token in tokens if token.lower() not in STOP_WORDS[language]]
# Removing irrelevant words containing apostrophe
	filtered_tokens = [token.lower() for token in filtered_tokens if not any(char in token.lower() for char in "',.`")]
# Filter non-bulgarian words
	if language == 'bulgarian':
		filtered_tokens = [token.lower() for token in filtered_tokens if not
						any(char in token.lower() for char in string.ascii_lowercase)]
# Filter words containing numbers
	filtered_tokens = [token.lower() for token in filtered_tokens if not
						any(char in token.lower() for char in string.digits)]
	freq_dist = FreqDist(filtered_tokens)
	main_keywords = freq_dist.most_common(n)
	# df_keywords = pd.DataFrame(main_keywords, columns=['keyword', 'frequency'])
	return main_keywords




