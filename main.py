from PositionalIndex import PositionalIndex
from GetDocText import DocText
import re
import string
import datetime

if __name__ == '__main__':

    # CREATING INDEX TABLE
    docstext = DocText().getdoctext()

    print('wait for processing...')

    uniquetokens = {}
    documentlist = {}
    docid = 0

    for i in docstext['textfilelist']:
        docid += 1
        documentlist[docid] = docstext['filesname'][docid - 1]
        dirtytokens = re.split(r'\s|\n', i.translate(
            str.maketrans('', '', string.punctuation)))
        cleartokens = list(filter(lambda t: t != '', dirtytokens))
        wordpos = 0

        for j in cleartokens:
            term = j.strip(' ').lower()
            wordpos += 1
            if term in uniquetokens:
                if docid in uniquetokens[term].doclist:
                    uniquetokens[term].doclist[docid].append(wordpos)
                else:
                    uniquetokens[term].doclist[docid] = [wordpos]
            else:
                uniquetokens[term] = PositionalIndex(term)
                uniquetokens[term].doclist[docid] = [wordpos]
    # CREATE LOG
    time = datetime.datetime.now().strftime("%Y-%m-%d %H'' %M' %S")
    logName = "./logs/" + str(time) + ".txt"
    with open(logName, "w") as log:
        log.write(str(time) + "\n\nFile indexing for current files are:(" +
                  str(docstext['filesname'].__len__()) + " files)\n\n")
        for index, fileName in enumerate(docstext['filesname']):
            log.write(str(index) + "- " + fileName + "\n")
        log.write("\n\nIndex Table for current files are:(" +
                  str(uniquetokens.__len__())+" unique words)\n\n")
        for i in uniquetokens:
            log.write(uniquetokens[i].term + " " +
                      str(uniquetokens[i].doclist) + "\n")

    for i in uniquetokens:
        print(uniquetokens[i].term, uniquetokens[i].doclist)

    # Get the Query
    print('\n\nQuery examples: \n1. a OR b AND c\n2. a WITH b WITH c\n3. a NEAR 3 b NEAR 4 c')
    input = input(print('\nEnter Query: '))

    with open(logName, "a") as log:
        log.write("\nThe Query is:\n" + input + "\n")

    inputlist = input.strip(' ')
    queryterms = re.split(
        r'\sAND\s|\sOR\s|\sWITH\s|\sNEAR\s', input.strip(' '))
    queryoperations = re.findall(
        '\sAND\s|\sOR\s|\sWITH\s|\sNEAR\s', input.strip(' '))

    new_input_list = [item.strip(' ').lower() for item in inputlist]
    new_query_terms = [item.strip(' ').lower() for item in queryterms]
    new_query_options = [item.strip(' ') for item in queryoperations]

    def anddef(t1, t2):
        result = []
        if t1 is None or t2 is None:
            return None
        for i in t1:
            for j in t2:
                if i == j:
                    result.append(i)
                elif i < j:
                    break
        return result

    def ordef(t1, t2):
        result = []
        if t1 is not None:
            for i in t1:
                if i not in result:
                    result.append(i)
        if t2 is not None:
            for i in t2:
                if i not in result:
                    result.append(i)
        return result

    def notdef(t1):
        result = []
        for i in documentlist:
            if i not in t1.doclist:
                result.append(i)
        return result

    def calc_and_or():
        result_term = []
        for i in new_query_terms:
            x = i.split(' ')
            if uniquetokens.__contains__(x[x.__len__() - 1]):
                if x.__contains__('not'):
                    y = notdef(uniquetokens[x[x.__len__() - 1]])
                    result_term.append(y)
                else:
                    result_term.append(
                        uniquetokens[x[x.__len__() - 1]].doclist.keys())
            else:
                result_term.append(None)

        final_result = result_term[0]
        position = 0
        for i in new_query_options:
            position += 1
            if i == 'AND':
                final_result = anddef(final_result, result_term[position])
            elif i == 'OR':
                final_result = ordef(final_result, result_term[position])

        print('RESULTS:')
        for i in final_result:
            print(documentlist[i])
        with open(logName, "a") as log:
            log.write("\nRESULTS:\n")
            for i in final_result:
                log.write(documentlist[i] + "\n")

    def withdef(t1, t2, t3):
        result = {}
        for item1 in t1.doclist:
            if t2.doclist.keys().__contains__(item1) & t3.doclist.keys().__contains__(item1):
                doc2 = t2.doclist[item1]
                doc3 = t3.doclist[item1]
                for i1 in t1.doclist[item1]:
                    i2 = i1 + 1
                    i3 = i1 + 2
                    if doc2.__contains__(i2) & doc3.__contains__(i3):
                        if item1 in result:
                            result[item1].append([i1, i2, i3])
                        else:
                            result[item1] = [i1, i2, i3]
        return result

    def neardef(t1, t2, t3, n1, n2):
        result = {}
        for item1 in t1.doclist:
            if t2.doclist.keys().__contains__(item1) & t3.doclist.keys().__contains__(item1):
                pos2 = t2.doclist[item1]
                pos3 = t3.doclist[item1]
                for i1 in t1.doclist[item1]:
                    i2 = i1 + n1
                    i3 = i2 + n2
                    for p2 in pos2:
                        if p2 <= i2 and p2 >= i1:
                            for p3 in pos3:
                                if p3 <= i3 and p3 >= i2:
                                    if item1 in result:
                                        result[item1].append([i1, p2, p3])
                                    else:
                                        result[item1] = [i1, p2, p3]
                                else:
                                    break
                        else:
                            break
        return result

    def calc_with_near():
        for i in new_query_terms:
            x = i.split(' ')
            if x.__contains__('not'):
                print('!!BAD QUERY!!')
                return None
        if 'WITH' in new_query_options:
            if uniquetokens.__contains__(new_query_terms[0]) and uniquetokens.__contains__(
                    new_query_terms[1]) and uniquetokens.__contains__(new_query_terms[2]):
                result = withdef(
                    uniquetokens[new_query_terms[0]], uniquetokens[new_query_terms[1]], uniquetokens[new_query_terms[2]])
                if result.__len__() == 0:
                    print(None)
                else:
                    for i in result:
                        print('RESULTS:')
                        print(documentlist[i])
                    with open(logName, "a") as log:
                        log.write("\nRESULTS:\n")
                        for i in result:
                            log.write(documentlist[i] + "\n")
            else:
                result = None
                print(result)

        elif 'NEAR' in new_query_options:
            n1 = new_query_terms[1].split(' ')[0]
            n2 = new_query_terms[2].split(' ')[0]
            if uniquetokens.__contains__(new_query_terms[0]) and uniquetokens.__contains__(
                new_query_terms[1].split(' ')[1]) and uniquetokens.__contains__(
                    new_query_terms[2].split(' ')[1]):
                result = neardef(uniquetokens[new_query_terms[0]], uniquetokens[new_query_terms[1].split(
                    ' ')[1]], uniquetokens[new_query_terms[2].split(' ')[1]], int(n1), int(n2))
                if result.__len__() == 0:
                    print(None)
                else:
                    for i in result:
                        print('RESULTS:')
                        print(documentlist[i])
                    with open(logName, "a") as log:
                        log.write("\nRESULTS:\n")
                        for i in result:
                            log.write(documentlist[i] + "\n")
            else:
                result = None
                print(result)

    print('Query Terms: ', new_query_terms)
    with open(logName, "a") as log:
        log.write("\nQuery Terms: \n" + str(new_query_terms) + "\n")

    if new_query_options.__contains__('WITH') & any(i in new_query_options for i in ['NEAR', 'AND', 'OR']):
        print('!!BAD QUERY!!')
    elif new_query_options.__contains__('NEAR') & any(i in new_query_options for i in ['WITH', 'AND', 'OR']):
        print('!!BAD QUERY!!')
    elif any(i in new_query_options for i in ['OR', 'AND']):
        calc_and_or()
    elif any(i in new_query_options for i in ['WITH', 'NEAR']):
        calc_with_near()
    else:
        print('!!BAD QUERY!!')
