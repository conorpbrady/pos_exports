class LineItem:
    
    def __init__(self, k, n,v=0):
        self.key = k
        self.name = n
        self.values = v

    def total(self):
        return self.values

    def write_output(self, cat_string, a=None):
        if a is None:
            a = self.values
        return [cat_string, self.name, 'NULL', '{:.2f}'.format(a)]

    def __str__(self):
        return "{}// {}: {:.2f}".format(self.key,self.name,self.total())

    __repr__ = __str__

class LineItemByCategory(LineItem):

    major_groups = {}

    def __init__(self, k, n):
        self.values = {}
        for cat_k,cat_v in self.major_groups.items():
            self.values[cat_k] = 0
        super().__init__(k,n,self.values)

    def total(self):
        s = 0
        for k,v in self.values.items():
            s += v
        return s

    def write_output(self, cat_string, sum_values=True):
        if(sum_values):
            result = super().write_output(self.total())
        else:
            result = []
            for k,v in self.values.items():
                key_name = LineItemByCategory.major_groups[k]
                result.append([cat_string, self.name, key_name, '{:.2f}'.format(v)])
        return result
