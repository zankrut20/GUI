import os
import pickle
import PySimpleGUI as sg
sg.ChangeLookAndFeel('Dark')

class GUI:
    def __init__(self):
        self.layout = [[sg.Text('Search Term', size = (10, 1)), 
                        sg.Input(size = (45,1), focus = True, key = 'SEARCH'), 
                        sg.Radio('Contains', group_id = "choice", key = 'CONTAINS', default = True), 
                        sg.Radio('StartsWith', group_id = 'choice', key = 'STARTSWITH'), 
                        sg.Radio('EndsWith', group_id = "choice", key = 'ENDSWITH')],
                       [sg.Text('Root Path', size = (10, 1)), 
                        sg.Input('C:/', size = (45,1), key = 'PATH'), 
                        sg.FolderBrowse('Browse'), 
                        sg.Button('Re-Index', size = (10, 1), key = '_RE-INDEX_'), 
                        sg.Button('Search', size = (10, 1), bind_return_key = True, key = '_SEARCH_')],
                       [sg.Output(size = (100, 30))]]
        self.window = sg.Window('File Search Engine').Layout(self.layout)

class SearchEngine:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.matches = 0
        self.records = 0
    
    def creat_new_index(self, values):
        ''' create a new index and save to file '''
        root_path = values['PATH']
        self.file_index: list = [(root, files) for root, dirs, files in os.walk(root_path) if files]
        # save to file
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        ''' load existing index '''
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        ''' search for term based on search type '''
        # reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['SEARCH']

        # perform search
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if( values['CONTAINS'] and term.lower() in file.lower() or 
                    values['STARTSWITH'] and file.lower().startswith(term.lower()) or
                    values['ENDSWITH'] and file.lower().endswith(term.lower())):
                    
                    result = path.replace('\\','/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    continue

        # save search results
        with open('search_result.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')

def main():
    g = GUI()
    s = SearchEngine()
    s.load_existing_index()

    while True:
        event, values = g.window.read()

        if event is None:
            break
        if event == '_RE-INDEX_':
            s.creat_new_index(values)

            print()
            print('>> New Index has been created')
            print()

        if event == '_SEARCH_':
            s.search(values)

            # print results to output elements
            print()
            for result in s.results:
                print(result)

            print()
            print(' >> There were {:,d} mathes out of {:,d} records searched.'.format(s.matches, s.records))
            print()
            print(' >> This query produced the following mathces: \n')

if __name__ == '__main__':
    print("Starting program...")
    main()