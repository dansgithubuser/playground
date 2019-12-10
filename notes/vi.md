# dan's vim cheat sheet
## basics
get your commit message done

<pre>
:w -- write to file
:q -- quit
:q! -- quit without writing
:wq -- write and quit
:cq -- quit with nonzero return code (abort the commit)

i -- enter insert mode
esc -- exit mode

h, j, k, l -- move by character
</pre>

## essential
cannot be built out of basics

<pre>
:<b>n</b> -- move to <b>n</b>th line of file
ctrl-G -- show info about cursor position, including column number

v -- visual selection
y -- yank
"+y -- yank to clipboard (" means register, + is clipboard register)
p -- put
<, > -- unindent, indent
. -- repeat last edit

:echo has('visualextra')
ctrl-v -- block selection
I -- insert, edit one line, hit esc, changes should propagate to other lines (UI might not update)
c -- change block selection

u -- undo
ctrl-R -- redo

/<b>regex</b> -- search for <b>regex</b> (afterward, n for next, N for previous)
:s/<b>pattern</b>/<b>replacement</b> -- replace <b>pattern</b> with <b>replacement</b> on current line
:.,$s/<b>pattern</b>/<b>replacement</b>/gc -- replace all (g) <b>pattern</b> with <b>replacement</b> on
	lines from current (.) to last ($), ask for confirmation (c)
n -- next match
N -- previous match

on search:
	- use \v to enable "very magic" mode, which makes regexes feel like regexes in other languages
	- use /\v&lt;<b>word</b>&gt; to search for whole-words only (word, not swords)
	- use \C to force case-sensitive
on regexes:
	- + must be escaped with \, unlike *

@: -- repeat last command
q: -- interactive command history

q<b>letter</b><b>commands</b>q -- record macro
@<b>letter</b> -- play macro
@@ -- play last macro
</pre>

## common convenience
nonessential but important for comfortable usage

<pre>
I -- insert at beginning of line
A -- insert at end of line

r -- replace one character

w, b -- move by word
0, $ -- move to beginning, end of line
^ -- move to beginning of indented line
gg, G -- move to beginning, end of file
ctrl-U, ctrl-D -- move by half-page

x -- delete
dd -- delete line
J -- join lines

V -- visual selection by line
</pre>

## .vimrc
Use a .vimrc file to customize your experience. Keep it in version control and make note of which plugins it depends on. Be careful about alienating yourself from vanilla vim. You can see my .vimrc file [here](https://github.com/dansgithubuser/playground/blob/master/dan), search for `_vimrc`.

## plugins
Vim 8 introduced easy plugin support. Installing a plugin should be no more complicated than cloning it into the correct spot. Plugins are especially useful for custom syntax highlighting.

## uncommon convenience
for when the rest is muscle memory

<pre>
o -- create new line below and insert
O -- create new line above and insert

R -- enter replace mode

W, B -- move to space
ctrl-Y, ctrl-E -- move screen by line
H, M, L -- move cursor to top, middle, low line of screen
zt, zz, zb -- move screen so current line is in top, middle, or bottom of screen
m<c> -- set bookmark <c>
`<c> -- go to bookmark <c>
</pre>

### mapping
Mapping is most useful in your `.vimrc`, so let's look at an example in that context.

`nnoremap ,s :SemanticHighlightToggle<cr>`
- Semantically, the `nnoremap` splits into:
	- `n` normal mode
	- `nore` no recursion (stop looking for further maps once this one is evaluated)
	- `map` map
- comma followed by a letter is a fairly uncluttered namespace
- the command here is from github.com/jaxbot/semantic-highlight.vim
- the `<cr>` executes the command (literal carriage return)
