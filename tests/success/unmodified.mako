	<%def name="a(**kwargs)">
		<%
            lst = [ "%s='%s'"%(k,v) for k, v in kwargs.items()]
            args = ' '.join(lst)
		%>

		<a ${args}> ${caller.body()} </a>
	</%def>


	<%self:a _class='hello' href='#'>
		Login | Register
	</%self:a>