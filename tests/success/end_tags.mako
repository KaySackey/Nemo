Test that mako end tags close agaisnt the appropriate scope.
The endfor should close against the for tag, not the ul.

    % ul
        % for i in range(5):
            % li #'item_${i}'  |> ITEM ${i}
        % endfor