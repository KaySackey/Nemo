<%def name="left_sidebar()">
        % if tags:
            Words.
        % else:
            This shouldn't fail because mako defs open statements are treated as HTML.
        % endif