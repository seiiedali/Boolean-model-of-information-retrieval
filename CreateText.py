import wikipedia

class File:

    def create():
        s = list()

        for i in range(0, 3):
            s.append(input("ENTER WIKIPEDIA PAGE TITLE: "))

        print("LOADING...")

        for i in range(0, 3):
            p = wikipedia.page(i)
            print("SAVING TO {}.txt".format(s[i]))
            with open('./docs/{}.txt'.format(s[i]), 'w+', encoding='utf-8') as f:
                f.write(p.content)
            print('SAVED')
        print('End')

File.create()