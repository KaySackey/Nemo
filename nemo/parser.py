import re

from mako.util import FastEncodingBuffer
from exceptions import NemoException
from pyparsing import (Word, Keyword, Literal, OneOrMore, Optional, \
                      restOfLine, alphas, ParseException, Empty, \
                      Forward, ZeroOrMore, Group, CharsNotIn, White, delimitedList, quotedString, alphanums, Combine  )
import pyparsing
from nodes import Node, NemoNode, NemoRoot, MakoNode, Leaf, MakoEndTag

from exceptions import NemoException

class Buffer(FastEncodingBuffer):
    def __init__(self, encoding=None, errors='strict', unicode=True):
        super(Buffer, self).__init__(encoding, errors, unicode)
        self.writelines = self.data.extend

class BaseParser(object):
    """
        I am a parser. There are many like me, but I am the first.
    """
    def __init__(self, debug=False):
        self.debug = debug

    def _init(self, raw):
        self._c = None
        self._last_c = None
        self._raw = raw

    def _next(self):
        self._last_c = self._c
        self._c = next(self._raw)

    def parse(self, source):
        self._init(iter(source))

    def buffer_value(self):
        return self.buffer.getvalue()


class NemoParser(BaseParser):
    """
        I parse every line in a multi-lined string given to me via parse()
        I return a transformed string where every Nemo expression has been converted to a valid Mako expression.
        Internally, I use nodes to define the AST as I understand it.
    """
    def parse(self, source):
        self.arg_parser = NemoArgumentParser()
        self._init(iter(source.splitlines()))

        # Base Node
        head = NemoRoot()
        self._line_number = 0
        self._current_node = head
        while True:
            try:
                self._next()
                self._line_number += 1
            except StopIteration:
                # out = StringIO()
                out = Buffer()
                head.write(out)
                return out.getvalue()

            self._parse_line()


    def _parse_line(self):
        """ Parses a single line, and returns a node representing the active context
            Further lines processed are expected to be children of the active context, or children of its accestors.

            ------------------------------------------------

            Basic grammar  is as follows:
            line = <mako>|<nemo>|<string>

            <mako>
            We don't parse normally parse tags, so the following info is sketchy.
            Mako tags are recognized as anythign that starts with:
                - <%
                - %>
                - %CLOSETEXT
                - </%

            Mako Control tags however are parsed, and required to adhere to the same indentation rules as Nemo tags.

            mako_control = <start>|<middle>|<end>
            start = (for|if|while)  <inner>:
            middle = (else|elif):
            end = endfor|endwhile

            nemo = % ( <mako_control>|<nemo_statement> )
            nemo_statement = .<quote><string><quote>|#<quote><string><quote>|<words>

            <quote> = '|"
                Notes: Quotes are required to be balanced.
                       Quotes preceded by a \ are ignored.
            <string> = *
            words = \w+
        """
        #if self.debug: print '\t ' +  str(self._current_node)

        # PyParser setParseAction's actually execute during parsing,
        # So we need closures in order to change the current scope

        
        def depth_from_indentation(function):
            """ Set the depth as the start of the match """
            def wrap(start, values):
                #print 'Depth %d | %d %s' %(self._depth, start, values)
                #self._depth = start
                self._current_node = function(values)
                #print self._current_node
                return ''

            return wrap
        
        def depth_from_match(function):
            """ Set the depth as the start of the match """
            def wrap(start, values):
                #print 'Depth %d | %d %s' %(self._depth, start, values)
                #print self._current_node
                self._depth = start
                self._current_node = function(values)
                #print self._current_node
                return ''

            return wrap        

        def depth_from_nemo_tag(function):
            """ Start of the match is where the nemo tag is. Pass the other values to the wrapped function """
            def wrap(start, values):
                # print 'Depth %d | %d %s' %(self._depth, start, values)
                self._depth = start
                tokens = values[1]
                self._current_node = function(tokens)
                #print self._current_node
                return ''

            return wrap



        # Match HTML
        from pyparsing import NotAny, MatchFirst
        html = restOfLine
        html.setParseAction(depth_from_indentation(self._add_html_node))

        # Match Mako control tags
        nemo_tag    = Literal('%')

        begin       = Keyword('for')    | Keyword('if')     | Keyword('while')
        middle      = Keyword('else')   | Keyword('elif')
        end         = Keyword('endfor') | Keyword('endif')  | Keyword('endwhile')
        control     = nemo_tag + (begin | middle | end)

        begin.setParseAction(depth_from_indentation(self._add_nesting_mako_control_node) )
        middle.setParseAction(depth_from_indentation(self._add_mako_middle_node))
        end.setParseAction(depth_from_indentation(self._add_mako_control_leaf))

        # Match Nemo tags
        argument_name = Word(alphas,alphanums+"_-:")
        argument_value = quotedString
        regular_argument = argument_name + Literal('=') + argument_value

        class_name = Literal('.').setParseAction(lambda x: 'class=')
        id_name = Literal('#').setParseAction(lambda x: 'id=')
        special_argument = (class_name | id_name) + argument_value
        argument = Combine(special_argument) | Combine(regular_argument)

        # Match single Nemo statement (Part of a multi-line)
        inline_nemo_html   = Word(alphas) + Group(ZeroOrMore(argument))
        inline_nemo_html.setParseAction(depth_from_match(self._add_nemo_node))

        # Match first nemo tag on the line (the one that may begin a multi-statement expression)        
        nemo_html = nemo_tag + Group(Word(alphanums+"_-:") + Group(ZeroOrMore(argument)))
        nemo_html.setParseAction(depth_from_nemo_tag(self._add_nemo_node))

        # Match a multi-statement expression. Nemo statements are seperated by |. Anything after || is treated as html
        separator   = Literal('|').suppress()
        html_separator   = Literal('||') # | Literal('|>')
        nemo_list =  nemo_html + ZeroOrMore( separator + inline_nemo_html )
        inline_html = html.copy()
        inline_html.setParseAction(depth_from_match(self._add_inline_html_node))
        nemo_multi =  nemo_list + Optional(html_separator + inline_html)

        # Match empty Nemo statement
        empty       = nemo_tag + Empty()
        empty.setParseAction(depth_from_indentation(self._add_blank_nemo_node))

        # Match unused Mako tags
        mako_tags   = Literal('<%') | Literal('%>') | Literal('%CLOSETEXT') | Literal('</%')
        mako        = mako_tags
        mako_tags.setParseAction(depth_from_indentation(self._add_html_node))

        # Matches General
        nemo        =  (control | nemo_multi | empty)
        line        =   mako_tags | nemo | html

        # Depth Calculation (deprecated?)
        self._depth = len(self._c) - len(self._c.strip())

        #try:
        line.parseString(self._c)

        #except ParseException:
            # Finally if we couldn't match, then handle it as HTML
            #add_html_node(self._c)

    """
        This group of functions transforms the AST.
        They are expected to return the active node
    """
    def _add_to_tree(self, node, active_node):
        if node.depth > active_node.depth:
            active_node.add_child(node)
        else:
            self._place_in_ancestor(node, active_node)

        return node            

    def _add_control_leaf_to_tree(self, node, active_node):
        if node.depth > active_node.depth:
            active_node.add_child(node)
            return active_node

            # The following check is disabled
            # --------

            # Leafs cannot appear on a higher indentation point than the active node
            # That would be ambiguous
            #raise NemoException('\nIncorrect indentation\n' + \
            #                    'at:\n\t%s\n' % active_node + \
            #                    'Followed by:\n\t%s\n' % node + \
            #                    'Parent:\n\t%s' % active_node.parent )
        else:
            """Try to assign node to one of the ancestors of active_node"""
            testing_node = active_node

            while testing_node is not None:
                # Close against the first element in the tree that is inline with you
                if testing_node.depth == node.depth:
                    # We are trying to close against the root element
                    if not testing_node.parent:
                        raise NemoException('\nIncorrect indentation\n' + \
                                    'at:\n\t%s\n' % node + \
                                    'attempted to close against:\n\t%s' % testing_node )
                    else:
                        parent = testing_node.parent
                        parent.add_child(node)

                        # Todo: Remove this check
                        testing_node.check_as_closer(node, active_node)
                        
                        return testing_node.parent
                elif testing_node.depth < node.depth:
                    raise NemoException('\nIncorrect indentation\n' + \
                                'at:\n\t%s\n' % node + \
                                'attempted to close against:\n\t%s' % testing_node )
                testing_node = testing_node.parent
            else:
                # This should never be reached because NemoRoot has a depth of -1
                raise NemoException('\nIncorrect indentation\n' + \
                                    'at:\n\t%s\n' % active_node + \
                                    'Followed by:\n\t%s\n' % node + \
                                    'Parent:\n\t%s' % parent )
            #result = self._place_in_ancestor(node, active_node)
            #result.check_as_closer(node, active_node)
            #return result

    def _add_html_to_tree(self, node, active_node):
        is_blank = not node.value or node.value.isspace()
        deeper_indented = node.depth > active_node.depth

        if is_blank or deeper_indented:
            active_node.add_child(node)
            
            return active_node
        else:
            return self._place_in_ancestor(node, active_node)


    def _place_in_ancestor(self, node, active_node):
        """Try to assign node to one of the ancestors of active_node"""
        parent = active_node
        while parent is not None:
            if parent.depth < node.depth:
                parent.add_child(node)
                
                return parent

            parent = parent.parent
        else:
            # This should never be reached because NemoRoot has a depth of -1
            raise NemoException('\nIncorrect indentation\n' + \
                                'at:\n\t%s\n' % active_node + \
                                'Followed by:\n\t%s\n' % node + \
                                'Parent:\n\t%s' % parent )

    """
        This group of functions transforms the AST.
        They correspond to the type of node currently being parsed.
        They are expected to return a node if the current scope changes.
    """

    def _add_html_node(self, tokens):
        if self.debug: print "%s | html %s " % (self._line_number, self._c)
        # This isn't a mako expression
        # So if it is on the same indentation level or greater as the active scope, then add it as a child of that.
        # Otherwise we'll close scope and add it
        leaf = Leaf(self._c, self._depth, self._line_number)
        return self._add_html_to_tree(leaf, self._current_node)

    def _add_inline_html_node(self, tokens):
        html = tokens[0]
        if self.debug: print "%s | html %s " % (self._line_number, html)
        # This isn't a mako expression
        # So if it is on the same indentation level or greater as the active scope, then add it as a child of that.
        # Otherwise we'll close scope and add it
        leaf = Leaf(html, self._depth, self._line_number)
        return self._add_html_to_tree(leaf, self._current_node)


    def _add_blank_nemo_node(self, tokens):
        if self.debug: print '%s | blank' % self._line_number
        # This a blank line. Treat it as an end tag or ignore it if it appears under the root
        if not self._current_node.is_root:
            self._current_node = self._current_node.parent

        return self._current_node

    def _add_nemo_node(self, tokens):
        keyword = tokens[0]
        arguments = u' '.join(tokens[1])

        if self.debug:
            print "%s | nemo %s " % (self._line_number, self._c),
            print "\t[ Parsing: %s %s ]" %(keyword, arguments)

        node = NemoNode( (keyword, arguments), self._depth, self._line_number)
        
        return self._add_to_tree(node, self._current_node)

    def _add_nesting_mako_control_node(self, tokens):
        if self.debug: print "%s | start %s " % (self._line_number, self._c)
        node = MakoNode(self._c, self._depth, self._line_number)

        return self._add_to_tree(node, self._current_node)

    def _add_mako_middle_node(self, tokens):
        if self.debug: print "%s | middle %s " % (self._line_number, self._c)
        node = MakoNode(self._c, self._depth, self._line_number)

        return self._add_to_tree(node, self._current_node)

    def _add_mako_control_leaf(self, tokens):
        if self.debug: print "%s | end %s " % (self._line_number, self._c)
        if not self._current_node.is_root:
            self._current_node = self._current_node.parent

        node = MakoEndTag(self._c, self._depth, self._line_number)

        return self._add_control_leaf_to_tree(node, self._current_node)


class NemoArgumentParser(BaseParser):
    """
        Parse arguments on the same line as a nemo expression and return as string containing their converted form.
        E.g.
            % div .'hello' #'world' href="/dev/null"
            Will be sent to this parser as: .'hello' #'world' href="/dev/null"
            Then the parser will return: class='hello' id='world' href="/dev/null"

        Aside from converting . to class, and # to id, the parser also checks that quotations are balanced and that
        arguments are given in a proper form.
    """
    def _slurp_till(self, end_delimiters):
        """ Read until a given delimiter is found in a string iterator.
        Keeps white space, and ignores the end_delimiter if it is preceded by \
        Return a string
        """
        cc = None
        if type(end_delimiters) in [str, unicode]:
            end_delimiters = [end_delimiters]

        while True:
            try:
                self._next()
            except StopIteration:
                raise NemoException('Expected delimiter %s but EOL found instead' % end_delimiters)

            self.buffer.write(self._c)

            for end in end_delimiters:
                if self._c == end and self._last_c != '\\':
                    return

    def parse(self, source):
        self.buffer = Buffer()
        self._init(raw=iter(source))
        quotes = ['\'', '"']
        expect = None

        while True:
            try:
                self._next()
            except StopIteration:
                break

            if expect is None:
                # Match class token (.) or id token (#)
                if self._c == ' ':
                    self.buffer.write(self._c)
                elif self._c == '.':
                    expect = quotes
                    self.buffer.write('class=')
                elif self._c == '#':
                    expect = quotes
                    self.buffer.write('id=')
                else:
                    # Slurp up attribute name til we see a quote
                    self.buffer.write(self._c)
                    self._slurp_till(quotes)

                    # Slurp up attribute value till we see another of the same quote
                    delimiter_found = self._c
                    self._slurp_till(delimiter_found)
            else:
                if self._c not in expect:
                    raise NemoException('Expected one of: %s but received %s' % (expect, c))
                if expect is quotes:
                    delimiter_found = self._c

                    # Write quote to buffer, then slurp up til the next quote
                    self.buffer.write(delimiter_found)
                    arg = self._slurp_till(delimiter_found)

                    # We have a keyword/arg combination complete so go back to expecting nothing
                    expect = None

        return self.buffer.getvalue()

def nemo(a_string):
    """ Hook for Mako pre-processing """
    return NemoParser().parse(a_string)