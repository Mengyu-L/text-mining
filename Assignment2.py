from mediawiki import MediaWiki
import re
import math


'''
    In this module, I want to find the more important words for each data structure
    like array, heap, and so on.
'''


''' here is some work for initialization
    doc_word is used to turn punctuation marks into spaces for subsequent operations
    and MediaWiki is the api of wiki data source
'''
doc_word = r'\.|,|\?|!|=|\(|\)|\n|\"|\}| '

wikipedia = MediaWiki()

'''
    There are some data structures

    doclist is the list of website names
    doclen is the length of doclist
    
    allset is a dictionary that records different words in each data structure
    The members of allset are lots of maps. Their keys are the string of data structures' name
    and values are a set which is contains different words in the website
    allset['Array'] is the set that contains all different words in wiki/Array

    alldict is a dictionary. The members are maps. Their keys are the string of data structures' name
    and the values are some dictionaries. The dictionary's keys are words in the website
    and the values are the word's count

    scoredict is similar to alldict. The difference is that the values of dictionary in scoredict
    are word's tf-idf score
'''

doclist = ['Linked List','Array','Hash table','Queue (abstract data type)','Priority queue','Heap (data structure)','Binary Tree','Graph (abstract data type)']
doclen = len(doclist)
allset = {}
alldict = {}
allcount = {}
scoredict = {}
overview = {'Linked List':['linked','list'],'Array':['array'],'Hash table':['hash','table'],'Queue (abstract data type)':['queue'],'Priority queue':['queue'],'Heap (data structure)':['heap'],'Binary Tree':['binary','tree',],'Graph (abstract data type)':['graph']}

'''
    For each data structure, get the website content as a string
'''
for string in doclist:
    
    tmp = wikipedia.page(string)

    '''
        turn punctuation marks into spaces
    '''
    s = re.sub(doc_word,' ',tmp.content)
    s.lower()

    '''
        split to get each word
    '''
    lst = s.split(' ')

    '''
        dic is the dictionary that belongs to this string to record word and its count
        the count means the sum of words in dic
    '''
    dic = {}
    count = 0
    for item in lst:
        '''
            jump when word is alphabet or number
        '''
        if item == '' or len(item) == 1 or item in overview[string]:
            continue
        
        if (item[0] >= 'a' and item[0] <= 'z'):
            if item in dic:
                dic[item] += 1
            else:
                dic[item] = 1
            count += 1
        else:
            pass

    '''
        store some results
    '''
    allcount[string] = count

    '''
        sorted by the count of each word and retain the 30th items
    '''
    dic = sorted(dic.items(),key = lambda items:items[1],reverse = True)
    alldict[string] = dic[:30]
    allset[string] = set([item[0] for item in dic])
    scoredict[string] = {}

    '''
        calculate the tf scores
    '''
    for item in dic[:30]:
        scoredict[string][item[0]] = item[1]/count
    #print(string)
    #print(dic[:30])

'''
    calculate the idf scores
'''
for string in doclist:
    for item in alldict[string]:
        doccount = 0
        word = item[0]
        '''
            for each word in the website of string
            if it is appear in the website of otherstring,count self-increasing
        '''
        for otherstring in doclist:
            if string == otherstring:
                continue
            
            else:
                
                if word in allset[otherstring]:
                    doccount += 1
        #print(string,word,scoredict[string][word],doccount)
        '''
            multiply the two scores
        '''
        scoredict[string][word] *= 100*doclen/((doccount+1)**4)

'''
    show the most five important words of each data structure
'''
for string in doclist:
    scoredict[string] = sorted(scoredict[string].items(),key = lambda items:items[1],reverse = True)
for string in doclist:
    print(string)
    for item in scoredict[string][:5]:
        print(item)
