VARIABLE = 'var'
FUNCTION = 'func'
PROCEDURE = 'pro'
EXPRESSION = 'expr'
STATEMENT = 'stat'
PARAMETER = 'par'
ARRAY = 'arr'


class Symbol(object):
    def __init__(self, name, object_type, data_type, attribute=None, data_pointer=None):
        self.name = name
        self.object_type = object_type
        self.data_type = data_type
        if attribute is not None:
            for key, value in attribute.iteritems():
                self.__setattr__(key, value)
        self.data_pointer = data_pointer

    def __unicode__(self):
        return '%s, %s, %i' % (self.name, self.object_type, self.data_pointer)

    def __repr__(self):
        return '%s, %s, %i' % (self.name, self.object_type, self.data_pointer)
