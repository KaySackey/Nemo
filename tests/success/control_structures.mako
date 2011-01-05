    % if who is 'on first':
        Begin!
        % a .'1' href='${url}' data-attr-value="me"
            Tag 1?
            % span
                Testing
        Middle!
        % a .'2'
            Tag 2?
            % span
                Testing please
        End!

    % elif what is on 'second':

        % a .'2' href='${url}'
            This line is inside the tag.
    % else:
        I am misquoting this I'm sure.
    % endif

    This one is outside the tag.
    So is this!

    % a .'hi'
        This is inside the second tag. But the second tag is outside the first tag.