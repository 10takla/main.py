import eel


class Predicat():
    def __init__(self, form):
        self.form = form.replace(' ', '')
        self.cvantors = []

    def draw(self, arr=[], k=0):
        form = self.form
        word = ''
        for i in range(len(form)):
            word += form[i]
            if form[i] == '{':
                word = '{'
            if form[i] == '}':
                arr += [word]
                form = form.replace(word, '+')
                k += 1
                self.form = form
                self.draw(arr, k)
                break
        arr += [word]
        for i in ['{', '}']:
            for j in range(len(arr)):
                if i in arr[j]:
                    arr[j] = arr[j].replace(i, '')
        self.form = sorted(set(arr), key=lambda x: arr.index(x))

    def con(self):
        form_str = self.form[:]
        # очистить от +
        tmp = []
        for i in range(len(form_str)):
            if len(form_str[i]) != 1:
                tmp += [form_str[i]]
        form_str = tmp
        # вывести формулу
        for i, word in enumerate(form_str):
            for j in range(len(word)):
                if word[j] == '+':
                    form_str[i] = word.replace('+', '{' + form_str[i - 1] + '}')
        return form_str[-1]

    def calc(self):
        self.draw()
        text = ''
        for i in range(1, 8):
            eval('self.itap' + str(i) + '()')
            text += 'этап ' + str(i) + ':' + ''.join(self.cvantors) + self.con() + '<br>'
        return text

    def itap1(self):
        for i, word in enumerate(self.form):
            if '→' in word:
                word = word.split('→')
                word = '|' + word[0] + '|∨' + word[1]
                self.form[i] = word
            if '_' in word:
                word = word.split('_')
                word = '{|' + word[0] + '|∨' + word[1] + '}&{|' + word[1] + '|∨' + word[0] + '}'
                self.form[i] = word

    def itap2(self):
        for i, word in enumerate(self.form):
            if '|' in word:
                for j in range(len(word)):
                    if word[j] == '|':
                        if word[j + 1] == '|':
                            for t in range(j + 2, len(word)):
                                if word[t] == '|':
                                    self.form[i] = self.form[i][:j] + self.form[i][j + 1:]
                                    self.form[i] = self.form[i][:t - 1] + self.form[i][t + 1:]
                        else:
                            for t in range(j + 1, len(word)):
                                if word[t] == '∃':
                                    self.form[i] = self.form[i][:t - 1] + '∀' + self.form[i][t + 1:]
                                    self.form[i] = self.form[i][:t + 3] + '|' + self.form[i][t + 3:]
                                if word[t] == '∀':
                                    self.form[i] = self.form[i][:t - 1] + '∃' + self.form[i][t + 1:]
                                    self.form[i] = self.form[i][:t + 3] + '|' + self.form[i][t + 3:]
                                if word[t] == '∨':
                                    self.form[i] = self.form[i][:t] + '|&|' + self.form[i][t + 1:]
                                if word[t] == '&':
                                    self.form[i] = self.form[i][:t] + '|∨|' + self.form[i][t + 1:]
                                if word[t] == '|':
                                    break
                    break

    def itap3(self):
        pass

    def itap4(self):
        self.cvantors = []
        for i, word in enumerate(self.form):
            s = ''
            for j in range(len(word)):
                if word[j] == '∀' or word[j] == '∃':
                    for y in range(j, len((word))):
                        s += word[y]
                        if word[y] == ')':
                            self.cvantors += [s]
                            self.form[i] = word.replace(s, '')
                            break
        self.cvantors = list(reversed(self.cvantors))



    def itap6(self):
        for i, word in enumerate(self.form):
            if '∨' in self.form[i] and '∨' in self.form[i + 1]:
                arr1 = self.form[i].split('∨')
                arr2 = self.form[i + 1].split('∨')
                tmp = arr1[1]
                arr1[1] = arr1[0]
                arr1[0] = arr2[0]
                arr2[0] = arr2[1]
                arr2[1] = tmp
                arr1 = '∨'.join(arr1)
                arr2 = '∨'.join(arr2)
                self.form[i] = arr1
                self.form[i + 1] = arr2

    def itap7(self):
        tmp = []
        for i in self.cvantors:
            if '∀' not in i:
                tmp += [i]
        self.cvantors = tmp


eel.init("web")


@eel.expose
def to_python(form):
    print(form)

    text = Predicat(form).calc()
    eel.to_js(text)


eel.start("index.html", size=(1000, 500))
