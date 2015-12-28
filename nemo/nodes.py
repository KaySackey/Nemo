from exceptions import NemoException

PERMISSIVE = True

class Node(object):
    is_root = False
    follows_indentation_rules = True

    def __init__(self, value, depth, line_number):
        self.value = value
        self.depth = depth # This is the indentation depth, not the tree depth
        self.line_number = line_number

        self.parent = None
        self.children = []
        self.siblings = []

    def add_child(self, node):
        raise NotImplemented()

    def check_as_closer(self, node, active_node):
        """
           The passed in node was added as your child, and is attempting to close your scope.
           Is this allowed?
        """
        raise NemoException('\nIncorrect indentation\n' + \
                            'at:\n\t%s\n' % node + \
                            'Tried to close against:\n\t%s\n' % self + \
                            'Within active scope of:\n\t%s' % active_node )

    def write(self, buffer):
        raise NotImplemented()

    def __str__(self):
        return str(unicode(self))

    def __unicode__(self):
        return u'[%d|Line: %d][%s]' % (self.depth, self.line_number, self.value)


class NemoNode(Node):
    @property
    def value(self):
        return '%s %s' % (self._keyword, self._arguments)

    @value.setter
    def value(self, value):
        self._keyword, self._arguments = value

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def _padding(self):
        return [' ' for i in xrange(1, self.depth)]

    def write(self, buffer):
        buffer.write('\n')
        buffer.writelines( self._padding() )
        # Open Tag
        buffer.writelines( ['<', self._keyword, ' ', self._arguments ] )

        if len(self.children) is 0:
            # This tag is automatically closed inline
            buffer.write(' />')
        else:
            # Close Open Tag
            buffer.write('>')

            self._write_children(buffer)

            # Write close Tag
            buffer.write('\n')
            buffer.writelines( self._padding() )
            buffer.writelines( ['</', self._keyword, '>'] )


    def check_indentation_rules(self, children):
        depth_seen = None
        for child in children:
            # Ensure child is at correct depth
            # If this is disabled then depth.failure and inner_tag_indentation.failure will both succeed
            # It is dubious if we want this
            # Todo: Permissive mode
            if child.follows_indentation_rules and not PERMISSIVE:
                if depth_seen is None:
                    depth_seen = child.depth
                elif child.depth is not depth_seen:
                    raise NemoException('\nIncorrect indentation\n' + \
                                         'at:\n\t%s\n' % child + \
                                         'within:\n\t%s\n' % self + \
                                         'expected indentation of %d ' % depth_seen)

            yield child

    def check_open_close_on_mako_nodes(self, children):
        open_mako_context = None
        for child in children:
            child_type = type(child)

            # Check child nodes for open/close semantics
            if child_type is MakoNode and open_mako_context is None:
                open_mako_context = child
            if child_type is MakoEndTag:
                if open_mako_context is None:
                    # Closer w/o an open context
                    raise NemoException('\nEnd tag without open context\n' + \
                                        'at:\n\t%s\n' % child + \
                                        'within:\n\t%s\n' % self )
                # Close context
                open_mako_context = None

            yield child

        if open_mako_context is not None:
            # Open context without a closer
            raise NemoException('\nOpen tag without a closer found:\n' + \
                                'at:\n\t%s\n' % open_mako_context + \
                                'within:\n\t%s\n' % self )
        
            
    def _write_children(self, buffer):
        """
           Write child nodes onto the buffer.
           Ensure that all non-leaf (end tags, raw strings), occur on the same depth
        """
        children = self.check_open_close_on_mako_nodes(
                   self.check_indentation_rules(
                        self.children))

        for child in children:
            # Write the child
            child.write(buffer)

class MakoNode(NemoNode):
    """
        I represent a tag in Mako. Either an opening tag, or a middle tag.
        I can have children.
    """
    def __init__(self, value, depth, line_number):
        super(MakoNode, self).__init__(value=(value, ''), depth=depth, line_number=line_number)

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def write(self, buffer):
        buffer.write("\n")
        buffer.write(self.value)


        self._write_children(buffer)

    def check_as_closer(self, node, active_node):
        """
        Originally this was slated to be removed because it only provided security against bugs we hadn't tested against.
        In practice (the last 4 years), it proved to be invaluable in
        providing better error messages than otherwise would be available.

        It didn't uncover any real bugs, but it showed incorrect indentation at a better level than would otherwise be provided.

        Technically removing this wouldn't result in invalid code immediately,
        but it'll let you write poorly Nemo and forget about it.
        Then later on, you'll end up writing more seemingly valid code which will
        caused an error in previously written statements.

        Unlike in HAML, we've chosen to cause an error as soon as possible,
        rather than implicitly swallowing the error node.
        """

        # Debugging
        #print node
        #print self
        # The node passed in should be a MakoNode or a MakoLeaf at the same indentation level

        # Who is closing?
        if self is active_node:
            # I am the active node, so I am the unambiguous choice to be closed at this time
            return      

        potentially_closed = active_node.parent
        while potentially_closed is not None:

            #print 'Checking: %s' % potentially_closed
            if potentially_closed.depth == node.depth:
                # <potentially_closed> is definitely being closed by <node>, and all is well
                # Todo: Perform type checking to make sure MakoNodes only close against other MakoNodes
                return
            elif potentially_closed.depth < node.depth:
                # How am is <node> closing someone at a lower depth than it?
                raise NemoException('\nIncorrect indentation\n' + \
                                    'at:\n\t%s\n' % node + \
                                    'Tried to close against::\n\t%s\n' % self + \
                                    'Within active scope of:\n\t%s' % active_node )

            potentially_closed = potentially_closed.parent

class NemoRoot(NemoNode):
    """
        I represent the root element of a Nemo AST
        Ideally, there should only be one instance of around during parsing.
    """
    is_root = True

    def __init__(self):
        super(NemoRoot, self).__init__(('Nemo Root', None), -1, 0)

    def write(self, buffer):
        self._write_children(buffer)

    def _write_children(self, buffer):
        """
           Write child nodes onto the buffer.
           Tags within the root can occur on any depth you feel like.
           Todo: Check if this messes things up if your tags under the root are ambiguously aligned
        """

        children = self.check_open_close_on_mako_nodes(
                        self.children)

        for child in children:
            # Write the child
            child.write(buffer)        

class Leaf(Node):
    """
        I am a leaf, I cannot have children. If I do, then it is an error
    """
    follows_indentation_rules = False

    def write(self, buffer=None):
        buffer.write("\n")
        buffer.write(self.value)

    def add_child(self, node):
        # This should never be called
        raise NemoException('Parser error. Tried to add node:\n\t%s to leaf: \n\t%s' % (node, self))

class MakoEndTag(Leaf):
    """
    I represent a closign tag in Mako.
    I am a Leaf without children.
    """
    follows_indentation_rules = True
    pass
