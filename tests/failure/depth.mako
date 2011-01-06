%ul
    0
    %li #'one'
               %li #'two'
                I am a child of one.
        %li #'three'
            Two is the active node, and should be my parent.
            But it is of a higher depth.
            I try to make my parent one, but it is of a lower depth than me.
            So I fail with an indentation error.
    % li #'four'
        I will not be reached, but I should be sibling of one.