import os


class DocText:

    def getdoctext(self):

        files = os.listdir('./docs/')
        textfilelist = list()

        for filename in files:
            with open('./docs/' + filename, 'r') as contents:
                textfilelist.append(contents.read())

        return {'textfilelist': textfilelist, 'filesname': files}
