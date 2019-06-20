import string
import wikipedia
import requests


class WikiParser():
    
    def __init__(self):
        self.S = requests.Session()
        self.pageerrors = []
        self.ambiguation = []
    
    def get_plot(self,raw_text):
        '''accepts a WikipediaPage object, and extracts the plot text(if there is any)
            and returns it in plain text, with no punctuation. If no plot text exists, return -1.
            
            Args:
                raw_text: WikipediaPage
                    the artiticle in a WikipediaPage format.
                
            Return:
                plottext: string
                    The plot section of the article in plain text format.'''
        fulltext = raw_text.content
        ind1 = fulltext.find('== Plot ==') + 10
        ind2 = fulltext.find('==',ind1)
        plottext = fulltext[ind1:ind2]
        plottext = plottext.replace('\n',' ').translate(str.maketrans('','',string.punctuation))
        if len(plottext) > 5:
            return plottext
        else:
            return -1

    def get_bio(self,raw_text):
        '''accepts a WikipediaPage object, and extracts the plot text(if there is any)
            and returns it in plain text, with no punctuation. If no plot text exists, return -1.
            
            Args:
                raw_text: WikipediaPage
                    the artiticle in a WikipediaPage format.
                
            Return:
                biotext: string
                    The publication history and character biography sections of the article in plain
                    text format.'''
        fulltext = raw_text.content
        ind1 = fulltext.find('== Publication history ==')
        if ind1 != -1:
            ind1 += 26
            ind2 = fulltext.find('== Other versions ==',ind1) + 1
            biotext = fulltext[ind1:ind2]
            biotext = biotext.replace('\n',' ').translate(str.maketrans('',''))
            if len(biotext) > 5:
                return biotext
            else:
                return -1
        else:
            return -1


    def get_category(self,cat):
        '''searches for a wikipedia category, and returns the first 100 memebers
        of the category.
            
            Args:
                cat: string
                The category to be searched. 
                
            Return:
                titles: list
                    the titles of the 100 category members in the search.'''
        
        URL = "https://en.wikipedia.org/w/api.php"

        TITLE = cat#"Category:Marvel Comics superheroes"

        PARAMS = {
            'action': "query",
            'list': 'categorymembers',
            'cmtitle': TITLE,
            'cmlimit': '100',
            'format': "json",
        }

        R = self.S.get(url=URL, params=PARAMS)
        data = R.json()
        titles =  [item['title'] for item in data['query']['categorymembers']]
        if 'continue' in data.keys():
            self.cmc = data['continue']['cmcontinue']
        else:
            self.cmc = -1
        return titles


    def continue_category(self,cat):
        '''searches for a wikipedia category previously searched, and returns the 
        next 100 memebers of the category. Requires that the category have been
        previously searched. 
            
            Args:
                cat: string
                    The category to be searched. 
                
            Return:
                titles: list
                    the titles of the next 100 category members in the search.'''
        
        
        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            'action': "query",
            'list': 'categorymembers',
            'cmtitle': cat,
            'cmcontinue': self.cmc,
            'cmlimit': '100',
            'format': "json",
        }

        R = self.S.get(url=URL, params=PARAMS)
        data = R.json()
        titles =  [item['title'] for item in data['query']['categorymembers']]
        if 'continue' in data.keys():
            self.cmc = data['continue']['cmcontinue']
        else:
            self.cmc = -1
        return titles

    def get_all_bios(self,pages,label):
        '''accepts a list of wikipedia page titles, and searchs for each one.
            The bio is then extracted from the page in a plaintext format, 
            and attached to a list.
            
            Args:
                pages: list
                    list of page titles to be searched. 
                label: string
                    label to be applied to each bio.
                
            Return:
                bios: list
                    list of dictionaries, each containing a bio for a character,
                    and a label for that bio.'''
        
        
        bios = []
        miss = 0

        for i,page in enumerate(pages):
            try:
                hero = wikipedia.page(page)
                bio = self.get_bio(hero)
                if bio != -1:
                    bios.append({'bio': bio, 'label': label})
            except wikipedia.exceptions.DisambiguationError:
                self.ambiguation.append(page)
            except wikipedia.exceptions.PageError:
                self.pageerrors.append(page)
            if ((i+1) % 10 == 0):
                print('.',end=" ")

        print(" ")
        return bios