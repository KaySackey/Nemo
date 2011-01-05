% span
    % if hello:
        Testing if wierd indentations are accepted by the inner tags

    % else:
         This should be nested inside the span if it somehow succeeds.
    % endif

            % if hello:
                Testing if wierd indentations are accepted here.
            % else:
                This should fail
            % endif