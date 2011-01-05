<%def name="title()">
    Upload
</%def>

    % fieldset .'upload'
        % legend
            % strong
                Upload Files
        % div .'controls'
            % form #'upload form' action='#'
                % ul .'settings'
                    ${upload_form.as_ul()}
                % ul
                    % li | a .'start'  href="javascript:$('#uploadify').uploadifyUpload()"          || Start Upload
                    % li | a .'clear_queue' href="javascript:$('#uploadify').uploadifyClearQueue()" || Clear Queue
                    % li #'uploadify' || You have a problem with your javascript
        % div .'queue_wrapper'
            % div .'uploadifyQueue' #'uploadifyQueue'
                Testing Testing Testing
% if def:
   111111
% else:
    22222
% endif
