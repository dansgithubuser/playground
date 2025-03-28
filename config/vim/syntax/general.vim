syn match balanced /[()\[\]{}<>'"]/
highlight balanced ctermfg=Green

syn match separator /[,:=._/]/
highlight separator ctermfg=23

syn match number /[0-9]/
highlight number ctermfg=DarkGrey

syn match capital /[A-Z]/
highlight capital cterm=bold

syn match divider /\v[=-]{3,}.*[=-]{3,}/
highlight divider ctermbg=17
