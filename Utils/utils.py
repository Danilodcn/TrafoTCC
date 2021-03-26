class QueryDictError(Exception):
    pass


class QueryDict(dict):
    def __init__(self, *args, **kw):
        super(QueryDict, self).__init__(*args, **kw)
    
    def __getattr__(self, attr):
        try: 
            return self.__getitem__(attr)
        except: 
            raise QueryDictError(f"Não Existe essa chave: {attr}")
        
    def __setatt__(self, attr, value):
        print(f"setei aqui: {attr} = {value}")
        self.__setitem__(attr, value)

    def __dir__(self):
        return self.keys()