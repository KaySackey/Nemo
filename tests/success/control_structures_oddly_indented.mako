        % if blah:
    % a .'1' href='${url}'
        This line is inside the tag. Even with weird nesting
    % else:
    % a .'2' href='${url}'
        This line is inside the tag.
                % endif
    This one is outside the tag.
    So is this!
% a .'hi'
    This is inside the second tag. But the second tag is outside the first tag.