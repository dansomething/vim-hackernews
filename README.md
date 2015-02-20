vim-hackernews [![Build Status](https://travis-ci.org/ryanss/vim-hackernews.svg)](https://travis-ci.org/ryanss/vim-hackernews)
==============

Browse [Hacker News](https://news.ycombinator.com) inside Vim.

![Hacker News Front Page in Vim](https://github.com/ryanss/vim-hackernews/raw/master/screenshots/vim-hackernews-home.png)

![Hacker News Comments in Vim](https://github.com/ryanss/vim-hackernews/raw/master/screenshots/vim-hackernews-item.png)

Uses [cheeaun's Unofficial Hacker News API](https://github.com/cheeaun/node-hnapi)
to retrieve home page stories and comments and
[FUCK YEAH MARKDOWN](http://fuckyeahmarkdown.com) for rendering HTML articles
as text.


Basic Usage
-----------

* Open the Hacker News front page in Vim by executing the `:HackerNews` command
* Move between items on the front page with uppercase `J` and `K`
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


Running Tests
-------------

```bash
$ vim -c Vader! tests.vader
```


Contributions
-------------

[Issues](https://github.com/ryanss/vim-hackernews/issues) and
[Pull Requests](https://github.com/ryanss/vim-hackernews/pulls) are always
welcome!


License
-------

Code is available according to the MIT License
(see [LICENSE](https://github.com/ryanss/vim-hackernews/raw/master/LICENSE)).
