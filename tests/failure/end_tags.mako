End tags always close against thie first item found in the tree that is inline with them.
This should be illegal, since the for tag will close against the li tag:

    % ul
        % for i in range(5):
            % li #'item_${i}'  |> ITEM ${i}
            % endfor