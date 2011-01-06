===================
Introducing Nemo
===================
----------------------------
Clarity on the web
----------------------------

This is Nemo
::

    % fieldset .'upload'
        % legend | strong || Upload Files
        % div .'controls'
            % form #'upload form' action='#'
                % ul .'settings'
					${upload_form.as_ul()}
                % ul
                    % li | a .'start'  href="javascript:upload()" || Start Upload
                    % li | a .'clear_queue' href="javascript:clear()" || Clear Queue
                    % li #'uploadify' || You have a problem with your javascript
        % div .'queue_wrapper'
            % div .'uploadifyQueue' #'uploadifyQueue'

This is what it produces
::

		<fieldset class="upload">
			<legend><strong>Upload Files</strong></legend>
			<div class="controls">
				<form id="upload_form" action="#">
					<ul class="settings">
						${upload_form.as_ul()}
					</ul>

					<ul>
						<li><a class='start' href="javascript:upload()">Start Upload</a></li>
						<li><a class='clear_queue' href="javascript:clear()">Clear Queue</a></li>
						<li id="uploadify">You have a problem with your javascript</li>
					</ul>
				</form>
			</div>

			<div class='queue_wrapper'>
				<div class='uploadifyQueue' id="uploadifyQueue"></div>
			</div>
		</fieldset>

Looks like Haml_, eh?
But this is also Nemo:
::

	% ul
		<li> Hello world! </li>
		%li
			Hello Universe!

And here's what it produces
::

   <ul >
        <li> Hello world! </li>
       <li >
            Hello Universe!
       </li>
   </ul>

Can Haml do that?

Background
==============

This project is inspired by PyHaml_. I have looked at PyHaml before, and found that:
	- It is not pythonic in nature
	- It is overly restrictive
	- It is not as pretty as it could be

As such, I set out to create an alternative 12 frantic hours of coding later, I have *something* that may possibly be called alpha.


Nemo is intended as an aid, not a shortcut, not a crutch, not a way to avoid learning HTML.
In order to write proper Nemo, you still have to know HTML and as such it'll get out of your way
if you just want to write HTML.

However, if you want to write it fast, write in Nemo and let it do the heavy lifting for you.



Usage
===================

First, place this module somewhere in your python path.
Pip/Easy_install will be supported

Django Integration
----------------------
- Install Djmako to get a Django template loaders for Mako.
  ::

		pip install djmako

- Add 'Nemo' to your Django sites package. It will automatically use the following defaults:
  ::

		MAKO_TEMPLATE_DIRS=(os.path.join(settings.SITE_ROOT, 'templates'),)
		MAKO_TEMPLATE_OPTS=dict(input_encoding='utf-8',
					output_encoding='utf-8',
					module_directory=os.path.join(settings.SITE_ROOT, 'cache'),
					preprocessor=Nemo
		)

  But you can override this in your settings.py.
  Only the preprocessor is mandatory to use Nemo and it lives in Nemo.parser

- Now in your views
  ::

		from Nemo import render_to_response, render_to_string

  Then use those as replacements for the Django driven ones.
  Also, if you're used to using Mako, you can use these functions to render a single Mako def_ (like for an Ajax view)
  ::

		def my_view(request):
			return render_to_response('templates\list.Mako', def_name='item')


Other projects
------------------
::

	from Nemo.parser import Nemo
	t = Template(filename=filename,
		preprocessor=Nemo,
		input_encoding='utf-8',
		output_encoding='utf-8',)
	print t.render()

Reference
===================

Nemo uses utf-8 internally by default, and expects you will at least use unicode as the input encoding for your templates.

Nemo Tags
-----------------------------------
Any line that starts with a % sign will be interpreted as a Nemo tag

Playing well with Mako
-----------------------------------
Nemo allows for all Mako code and control structures.
However, Mako control structures have to follow the same indentation rules as Nemo code.

Attributes
-----------------------------------
To output HTML, Nemo is written like this:
::

	% <element type> <attributes 0 ... 1>

Where attributes are written as <name> = <value>

In the case of the attributes class and id, Nemo provides two short forms:
- #  denotes an id
- .  denotes a class

They are used without assignment markers. For example, the following two statements are equivilent
::

	% div .'example' #'first'
	% div class='example' id='first'


Caveats:
	- Nemo will not check for duplicated attributes.
	- You can only use Mako syntax within strings or HTML nodes.
	  You can't use it to write your attribute names, like this:
	  ::

			% li ${name}=${value}

	  It will be converted to an empty node
	  ::

			<li />

To compare, this limitation is present in Haml (afaik) as well.

Indentation Rules
-----------------------------------
- All grouped control tags must appear on the same line. These are:
	- if / elif / else / endif
	- for / endfor
	- while / endwhile
- The scope of a Nemo block is determined by indentation.
  Thus all of its contents, including bare HTML must be indented to the right of it.
  It doesn't matter precisely how much a bare HTML block is indented, and consistency is unimportant.

HTML Escaping
-----------------------------------
Nemo intends to make it easy for you to drop down to HTML at any point.
In the general case, there is no explicit escaping and any line that doesn't start with % is treated as HTML.

The exception is Mako end-tags:
	- %>
	- %CLOSETEXT

These are treated as HTML and go unprocessed even though they begin with a % sign.

For example:
	- You can write this as a valid Nemo block::

		% ul
			<li ${get_my_attributes()} > Custom </li>

	- Or write inline javascript. Or write inline CSS.
	- Or drop in other code that will be processed *later*  by another agent (e.g. Mako code).

One fun consequence is that multi-line blocks are allowed *without* any extra escaping.

Remember doing this in Haml?
::

	%whoo
	  %hoo= h(                       |
		"I think this might get " +  |
		"pretty long so I should " + |
		"probably make it " +        |
		"multiline so it doesn't " + |
		"look awful.")               |
	  %p This is short.

Well here's how you do it in Nemo:
::

	%whoo
	  % hoo
			I think this might get
			pretty long so I should
			probably make it
			multiline so it doesn't
			look awful.
	  % p This is short

Chaining Nemo Expressions
-----------------------------------
Nemo tags can be chained using '|' as a separator.
To output HTML at the end, place either '||' before the HTML.
Anything after those markers will be output on a line of its own, at the beginning of the line and subject to further processing by Mako.

Nemo::

		%li .'toggle top'
			% a .'open' href='#' |> Login | Register
			% a .'close' href='#' style='display: none;' || Close Panel

HTML::

		<li class="toggle top">
			<a class="open" href="#">Log In | Register</a>
			<a class="close" href="#"  style="display: none;">Close Panel</a>
		</li>

As a result, you can use Mako for expression substitution in the same line as Nemo tags.
For example:
::

	% span || 1 + 2 = ${1 + 2}

Will become:
::

	<span>'12'</span>


Closing Tags
-----------------------------------
There are three ways a Nemo tag will be closed prematurely (e.g. before the end of parsing the document).

Automatic
~~~~~~~~~~~~~~~~~~~~~
Also, all tags without content are automatically closed.

Example::

			% li

Generates::

			% <li />

Implied Closure
~~~~~~~~~~~~~~~~~~~~~
An HTML block or something that's treated as such (e.g. a Mako tag) appears at a lesser indentation.

Example::

			% ul
				% li
					How deep can I go?
				Not that deep, sorry.
			I fear for you both.

Generates::

			<ul>
				<li> How deep can I go? </li>
				Not that deep sorry.
			</ul>
			I fear for you both.

Explicit Closure
~~~~~~~~~~~~~~~~~~~~~
To explicitly close a tag, simply place an empty Nemo tag (%) on a subsequent line at the same indentation
For example:
::

	% li
		We are happy people!
	%
		I'm outside, so... not so happy, here.

Generates:
::

	<li>
		We are happy people
	</li>
		I'm outside so not so happy here.

Debugging
======================================================
 - A lot of work has been put into Nemo to make it fail fast upon ambiguity, and yet generate good error messages.
   Anyone who's used an OCaml parser can agree when I say this is fundamental to a good parser[#]


 - Errors are tracked back to the source line that caused them
   If possible, Nemo will also tell you what it expected at that point.

   For more basic errors, you might see this an an exception traceback.
   ::

			   [8|Line: 6][        % endfor]
				^		^			^
				|		|			|
				Depth	Line #		Source content

	This kind of traceback is usually produced by ambiguous indentation.



Arguments against using Nemo & Responses
======================================================
"I know HTML"
	Good, this makes it easier to write it and gets out of your way if you don't want to use it.
	This means you don't have to convert the entirety of your document to Nemo first, just the parts you want to.

"I hate indentation"
	This would be a valid argument if Nemo was for Rubyists, or C-philes, or PHPers,
	or programmers versed in a lingua fraca that doesn't include significant white space.

	However Nemo is for Pythonistas by a Pythonista.
	My editor already handles white-space---including smart indentation during pasting code. Doesn't yours?

"I don't like that Disney fish and/or I'm afraid that they'll sue you for using its name"
	Haven't you heard of Captain Nemo, aka Prince Dakkar?
	Besides that 'Disney fish' Nemo is a type of Mako shark.
	We have to remember our roots, keep it real, be still Jenny on the block, ecetera and so forth. =)

"I like Haml"
	This is a can of worms I'll talk about later.

"I want Seasides' canvas"
	Let's get a beer together.


Future
======================================================

Syntax
--------------------------------------
Currently '||' is the only way to break out of a multi-line Nemo statement and get it to nest the subsequent HTML on the rest of the line.
However, it is a common case to directly print template variables.

The '| >' terminator will indicate to Nemo that the rest characters should be treated as a python one-liner that returns a string.

Finally, this will be possible:
::

	% div .'profile'
		% div .'left column'
			% div #'date' 		|> print_date
			% div #'address'  	|> current_user.address
		% div .'right column'
			% div #'email'  	|> current_user.email
			% div #'bio' 		|> current_user.bio


Strict Mode
---------------------------------------
Right now Nemo is running in 'Permissive' mode, in that it will always try to make sense of your document.
That means it may improperly nest things if you mix tabs & spaces.

I have something coded up called "strict mode", that essential forces everything to have proper indentation without any laxity.

Other Implementations?
--------------------------------------
Nemo can easily be extend to support other engines.
	- Django
	- Jinja
	- Cheetah
	- Spitfire
	- Genshi
	- etc.

Nemo is a preprocessor over Mako, and isn't tied too deeply into it (except for importing FastBufferReader from Mako).


Links:
----------------------
- Mako_
- Haml_

.. _def: http://www.makotemplates.org/docs/defs.html
.. _Mako: http://www.makotemplates.org/
.. _Haml: http://haml-lang.com/
.. _PyHaml: https://github.com/mikeboers/PyHAML