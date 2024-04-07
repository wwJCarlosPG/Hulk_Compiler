class Context:
    def __init__(self) -> None:
        self.types = {}
        self.scope = Scope()
    
    # ----------------
    # TYPES MINI CRUD
    # ----------------

    def create_type(self, name, value):
        self.types[name] = value

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        return None   # i think this will never happen

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.functions = {}
        self.variables = {}
        
    # ----------------------------------
    # VARIABLE AND FUNCTIONS MINI CRUD
    # ----------------------------------
        
    # VARIABLE SECTION
    def create_variable(self, name, value):
        self. functions[name] = value

    def edit_variable(self, name, new_value):
        if name in self.variables:
            self.variables[name] = new_value
        else:
            parent: Scope = self.parent
            if parent:
                parent.edit_variable(name, new_value)

    def get_variable(self, name):
        if self.variables[name]:
            return self.variables[name]
        else:
            parent: Scope = self.parent
            if parent: 
                return parent.get_variable(name)

    # FUNCTION SECTION
    def create_function(self, name, value):
        # this works to define functions and redefine functions
        self.functions[name] = value

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        return 
    

    

