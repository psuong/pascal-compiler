class Symbol(object):
    def __init__(self, name, object_type, data_type, attribute=None, data_pointer=None):
        self.name = name
        self.object_type = object_type
        self.data_type = data_type
        self.attribute = attribute
        self.data_pointer = data_pointer
        self.attribute = attribute

    def __unicode__(self):
        return '(%s, %s, %i)' % (self.name, self.object_type, self.data_pointer)

    def __repr__(self):
        return '(%s, %s, %i)' % (self.name, self.object_type, self.data_pointer)
