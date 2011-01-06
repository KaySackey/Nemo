% span
    % if hello:
        Testing if wierd indentations are accepted by the inner tags

    % else:
         This should be nested inside the span if it somehow succeeds.
    % endif

    <div>
        % if hello:
            Testing if weird indentations are accepted here.
        % else:
            This should fail under current rules.

            However, I'm not sure that it *should* fail in general.
            Because this is perfectly readable indentation.

            Maybe under a rule type: Permissive?
        % endif
    </div>