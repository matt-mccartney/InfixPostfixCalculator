class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          
class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top:Node = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):

        return self.top == None

    def __len__(self): 

        count = 0
        current = self.top
        while current is not None:
            count += 1
            current = current.next
        return count

    def push(self,value):

        new = Node(value)
        new.next = self.top
        self.top = new

    def pop(self):

        top_node = self.top
        if top_node is not None:
            self.top = self.top.next
            return top_node.value
        return None

    def peek(self):

        if self.isEmpty():
            return None
        return self.top.value