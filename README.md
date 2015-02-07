vim-hackernews
==============

Browse [Hacker News](https://news.ycombinator.com) from inside Vim.

Uses [cheeaun's Unofficial Hacker News API](https://github.com/cheeaun/node-hnapi)
to retrieve home page stories and comments and
[FUCK YEAH MARKDOWN](http://fuckyeahmarkdown.com) for rendering HTML articles
as text.


Basic Usage
-----------

* Open the Hacker News home page in Vim by executing the `:HackerNews` command
* Press lowercase `o` to open links in Vim
* Press uppercase `O` to open links in default web browser
* Press lowercase `u` to go back (or whatever you've remapped `undo` to)
* Press `Ctrl+r` to go forward (or whatever you're remapped `redo` to)
* Execute the `:bd` command to close and remove the Hacker News buffer


Installation
------------

##### Pathogen (https://github.com/tpope/vim-pathogen)
```bash
git clone https://github.com/ryanss/vim-hackernews ~/.vim/bundle/vim-hackernews
```

##### Vundle (https://github.com/gmarik/vundle)
```
Plugin 'ryanss/vim-hackernews'
```

##### NeoBundle (https://github.com/Shougo/neobundle.vim)
```
NeoBundle 'ryanss/vim-hackernews'
```


License
-------

Code is available according to the MIT License
(see [LICENSE](https://github.com/ryanss/vim-hackernews/raw/master/LICENSE)).
