def assignment_iterator():
    string_test = 'x := 20'

    for char in string_test:
        if char is ':':
            if char.next() is '=':
                print 'Assignment'
            else:
                return 'Equal'


if __name__ == '__main__':
    assignment_iterator()
