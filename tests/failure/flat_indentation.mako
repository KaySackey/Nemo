% if False:
    % for 1 in xrange(0, 10):
        I should not fail.
    % endfor

    % for 1 in xrange(0, 10):
    #
        I should fail because the statement above closes the for loop.
        Because of this. The endfor below will want to become a child of the if statement.

        For loops (and all mako control loops) have to be explicitly closed.

        Like Nemo statements they must appear on their own line, following indentation rules.
        And like Nemo statements, their contents must all be placed at a deeper indenation.
        
    % endfor
% else:
    Nothing intersting here.
% endif