    <form id="login" action="#" method="post">
        <h1>Member Login</h1>

        <label for="id_login-username">Username:</label>
        <input type="text" name="username" id="id_login-username" value="" size="23" class="required" />

        <label for="id_login-password">Password:</label>
        <input type="password" name="password" id="id_login-password" size="23" class="required" />

        <label><input name="remember_me" id="remember_me" type="checkbox" checked="checked" value="forever" /> &nbsp;Remember me</label>

        <input type="submit" name="submit" value="Login" class="bt_login" />

        <a class="lost_password" href="#">Lost your password?</a>

        <img src="" class="tiny spinner" style="display: none"/>
        <div class="results" style="display:none"></div>
    </form>

    <script type="text/javascript">
        $("#login").validate({
         submitHandler: function(form) {
            var $form = $(form);
            var $form_results = $form.find('.results');
            run_ajax({
                within: $form,
                dataType: 'json',
                url: "",
                data: $form.serialize(),
                success: function(response){
                    if(response['status'] == 'ok'){
                        $('.login .message').html(response['data']); // Deliver the login message
                        $('.toggle.top').hide();                    // Do not allow the panel to be toggled any more
                        $('.toggle.top .close').click();            // Close the panel
                    }
                    else{
                        $form_results.html(response['data']);
                    }
                }
            });

            return false;
         }
        });
    </script>