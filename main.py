import os
import shutil

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

import csv
import json

def importCSV(path, **kwargs) -> list:
    output = []

    with open(path) as csvfile:
        reader = csv.reader(csvfile, **kwargs)
        for row in reader:
            output.append([c.strip() for c in row])

    return output


class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent

        self.frame = ttk.Frame()

        self.initialize()

        self.frame.pack(fill='both')

        self.title("Enter paths")
        self.geometry('%dx%d' % (500 , 300) )

    def initialize(self):
        self.grid()

        self.catalog = []

        self.loadConfig()

        self.pathsFrame = ttk.Frame(self.frame)
        
        self.paths = {}

        def browse(entry, type='file', **kwargs):
            path = ''
            print(kwargs)

            if type in ['dir', 'directory']:
                path = filedialog.askdirectory(**kwargs)
            else:
                path = filedialog.askopenfilename(**kwargs)

            entry.delete(0, 'end')
            entry.insert(0, path)

        def createRow(parent, name, title, type='file', extension='*.*', extensionName='any', row=0):

            self.paths[name] = {}
            self.paths[name]['label'] = ttk.Label(parent, text=title)
            self.paths[name]['var'] = tk.StringVar()
            self.paths[name]['entry'] = ttk.Entry(parent, textvariable=self.paths[name]['var'], width=30)

            if type == 'file':
                kwargs = {
                    'defaultextension': extension,
                    'filetypes': ((
                            (extensionName, extension),
                            ('any', '*.*')
                        )
                    )
                }
                print('file')
            else:
                kwargs = {}

            self.paths[name]['button'] = ttk.Button(
                parent,
                text='Browse',
                command=lambda : browse(
                    self.paths[name]['entry'],
                    type,
                    title=title,
                    **kwargs
                )
            )

            self.paths[name]['label'].grid(row=row, column=0, sticky='e', padx=2, pady=2)
            self.paths[name]['entry'].grid(row=row, column=1, sticky='w', pady=2)
            self.paths[name]['button'].grid(row=row, column=2, sticky='w', padx=2, pady=2)

            self.paths[name]['entry'].delete(0, 'end')
            self.paths[name]['entry'].insert(0, self.config[name])

        createRow(self.pathsFrame, name='catalog', title='Catalog', type='file', extension='*.csv', extensionName='MKT Catalog', row=0)
        createRow(self.pathsFrame, name='rawNabe', title='Raw Nabe', type='dir', row=1)
        createRow(self.pathsFrame, name='decompressedNabe', title='Decompressed Nabe', type='dir', row=2)
        createRow(self.pathsFrame, name='output', title='Output Directory', type='dir', row=3)

        self.pathsFrame.columnconfigure(1, weight=1)
        self.pathsFrame.grid(row=0)

        self.startButton = ttk.Button(self.frame, text='Start', command=self.start)
        self.startButton.grid(row=1)

        self.progressFrame = ttk.Frame(self, width=500)
        self.progress = {
            'bar': ttk.Progressbar(
                self.progressFrame,
                orient='horizontal',
                mode='determinate',
                length=200
            ),
            'label': ttk.Label(self.progressFrame, width=40)
        }

        self.progress['bar'].grid(column=0, row=0, padx=5)
        self.progress['label'].grid(column=1, row=0)
        # self.progressFrame.columnconfigure(0, weight=1)

        self.frame.grid_rowconfigure(2, weight=1)

        self.progressFrame.pack(side='bottom', fill='x')

    def start(self):
        def setUIState(state='disabled'):
            self.startButton.state([state])
            for path in self.paths:
                self.paths[path]['entry'].state([state])
                self.paths[path]['button'].state([state])

                self.config[path] = self.paths[path]['var'].get()

        setUIState('disabled')

        print(self.config)
        self.exportConfig()

        # try:
        self.readCatalog()
        # except:
        #     print('error')

        setUIState('!disabled')

    def readCatalog(self):

        # if len(os.listdir(self.config['output'])) > 0:
        #     print('directory is not empty')
        #     return

        self.getCatalog()

        self.progress['bar']['max'] = len(self.catalog) - 1

        wavpath = f'{self.config["output"]}/WAV'
        try:
            os.mkdir(wavpath)
        except:
            pass

        for r in range(1, len(self.catalog)):
            row = self.catalog[r]
            split = row[3].split('/')
            del split[0]
            del split[0]

            # split.insert(0, self.config['rawNabe'])

            path = '/'.join(split)
            filename = os.path.basename(row[0])
            destination = f'{self.config["output"]}/PCK/{filename}'
            rawSource = f'{self.config["rawNabe"]}/{path}'
            decompiledSource = f'{self.config["decompressedNabe"]}/{path}'

            self.progress['label'].config(text=filename)
            self.progress['bar']['value'] = r - 1
            print(path)

            self.update()

            if os.path.isfile(rawSource):
                print('exists')

                try:
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    shutil.copyfile(rawSource, destination)
                except:
                    pass

                try:
                    shutil.copytree(decompiledSource, f'{wavpath}/{os.path.splitext(filename)[0]}')
                except:
                    pass

            # print(row[3])

    def getCatalog(self):
        try:
            self.catalog = importCSV(self.config['catalog'], delimiter=',', quotechar='"')
        except:
            pass

    def initConfig(self):
        self.config = {
            'catalog': 'catalog.csv',
            'rawNabe': '',
            'decompressedNabe': '',
            'output': ''
        }

    def loadConfig(self, **kwargs):
        try:
            self.config = kwargs['config']
        except:
            try:
                with open('config.json', 'r') as file:
                    self.config = json.load(file)

                print(self.config)
            except:
                self.initConfig()
                self.exportConfig()

        # self.getCatalog()
        # print(self.catalog)
        

    def exportConfig(self):
        file = open('config.json', 'w+')
        json.dump(self.config, file, indent=2)

def main():
    app = App(None)
    app.mainloop()

main()

# filedialog.askopenfilename(title='', defaultextension="")