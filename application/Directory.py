class Directory:
    flowableSectionOrder = ['prefix', 'directory', 'pre-map-spacers', 'maps', 'maplookup', 'post-map-spacers', 'suffix']
    pages = {'prefix': [],
             'directory': [],
             'pre-map-spacers': [],
             'maps': [],
             'maplookup': [],
             'post-map-spacers': [],
             'suffix': []} # pages is a dict of DirectoryPage lists
    def __init__(self):
        pass
