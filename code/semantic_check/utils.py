
class pseudo_graph:
    def __init__(self, adyacacence_list):
        self.relations = self.invert_dict(adyacacence_list)
        pass

    def there_is_error(self, nodes):
        for item in self.relations:
            if item == 'error':
                return True
        return 'error' in nodes
    
    @staticmethod
    def invert_dict(dictionary):
        inverted_dict = {}
        for key, values in dictionary.items():
            for value in values:
                inverted_dict[value] = key
        return inverted_dict        
    
    def find_paths(self, nodes):
        paths = []
        for node in nodes:
            paths.append(self.create_path(node))
        return paths
        
    def create_path(self, v):
        path_v = []
        while v != 'object':
            path_v.append(v)
            p_v = self.relations[v]    
            v = p_v
        path_v.append('object')
        return list(reversed(path_v))

    def find_LCA(self, nodes):
        if self.there_is_error(nodes):
            return 'error'
        paths = self.find_paths(nodes)
        if not paths:
            return None 
        min_len = min(len(path) for path in paths)
        i = 0
        while i < min_len:
            if all(path[i] == paths[0][i] for path in paths if path != paths[0]):
                current = paths[0][i]
            else: return paths[0][i-1]
            i += 1
        return current
        
def get_graph(statements: list):
    adyacence_list = dict()

    for item in statements:
        if item.parent:
            parent = Temp(item.parent.name, item.parent.parent)
            if parent.id in adyacence_list:
                adyacence_list[parent.id].append(item.id)
            else: 
                adyacence_list[parent.id] = [item.id]
    return adyacence_list

class Temp():
    def __init__(self, id, parent=None):
        self.id = id
        self.parent = parent