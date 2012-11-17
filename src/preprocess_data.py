import nltk, re, string, sys, time
from nltk.stem.lancaster import LancasterStemmer
import xml.etree.ElementTree as ET

def getPreprocessedDescription(desc):
    word_list = nltk.word_tokenize(child[7].text or '');
    # remove stop words
    filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
    # remove punctuation from existing words, and remove words containing numbers
    processed_words = [w.translate(None, string.punctuation) for w in filtered_words if not re.search('[0-9]', w)]
    # stem the words, removing any that are only one character
    stemmed_words = [st.stem(w) for w in processed_words if len(st.stem(w)) > 1]
    return ' '.join(stemmed_words)
    

def getDate(date):
    tokens = date.split(':')
    year = int(tokens[0])
    month = int(tokens[1])
    day = int(tokens[2])

    date = "%d-%d-%d" %(year,month,day) 
    try:
        time.strptime(date, "%Y-%m-%d")
    except ValueError:
        date = ''

    return date

categories = ['ALL OTHER OFFENSES', 'ARSON', 'ASSAULT OFFENSES',
              'BREAKING AND ENTERING', 'BURGLARY', 'COUNTERFEITING',
              'DESTRUCTION OF PROPERTY', 'DISORDERLY CONDUC',
              'DRIVING UNDER THE INFLUENCE', 'DRUG', 'DRUNKENNESS',
              'EMBEZZLEMENT', 'HOMICIDE OFFENSES', 'KIDNAPPING',
              'LARCENY', 'LIQUOR LAW VIOLATIONS', 'MOTOR VEHICLE THEFT',
              'PEEPING TOM', 'PORNOGRAPHY', 'ROBBERY', 'RUNAWAY',
              'SEX OFFENSES', 'DISORDERLY CONDUCT']

months = ['January', 'Febuary', 'March', 'Aprial', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

if len(sys.argv) is not 3:
    print 'Error: invalid argument list.'
    sys.exit(1)

categoryId = {i:j+1 for j,i in enumerate(categories)}
monthNumber = {i:j+1 for j,i in enumerate(months)}

tree = ET.parse(sys.argv[1])
root = tree.getroot()
st = LancasterStemmer()
    
csvf = open(sys.argv[2],'w')
csvf.write('Category,CrimeGroup,Description,City,State,Zip,Latitude,Longitude,Date\n')

i = 0
total = len(root)
for child in root:
    i += 1
    
    category = categoryId[child[6][0].text]
    crimeGroup = child[6][1].text
    description = getPreprocessedDescription(child[7].text or '')
    city = child[8][1].text or ''
    state = child[8][2].text or ''
    zipcode = child[8][3].text or ''
    latitude = child[8][6][0].text
    longitude = child[8][6][1].text
    date = getDate(child[5].text)

    # swap latitude/longitude if need be
    if (float(latitude)<30 or float(longitude)>-60) and (float(latitude)<-60 or float(longitude>30)):
        latitude,longitude = longitude,latitude

    line = ','.join([str(category),crimeGroup,description,
                     city,state,zipcode,latitude,longitude,date]) + '\n'
    csvf.write(line.encode('utf-8'))
    print '\r', i, '/', total, ' retreived',
csvf.close()
