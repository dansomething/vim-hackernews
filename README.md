vim-hackernews [![Build Status](https://img.shields.io/travis/ryanss/vim-hackernews.svg)](https://travis-ci.org/ryanss/vim-hackernews) [![Version](https://img.shields.io/badge/version-0.2-orange.svg)](https://github.com/ryanss/vim-hackernews/releases/tag/v0.2) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ryanss/vim-hackernews/raw/master/LICENSE)
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
* The HackerNews command takes an optional parameter to view items other
  than the top stories on the front page: `ask`, `show`, `shownew`, `jobs`,
  `best`, `active`, `newest`, `noobstories`, `<item id>`, or `<search query>`
* Press lowercase `o` to open links in Vim
* Press uppercase `O` to open links in default web browser
* Numbered lines with story titles on the front page link to the story url
* Comment lines on the front page link to the comments url
* Press uppercase `F` to fold current comment thread
* Press lowercase `u` to go back
* Press `Ctrl+r` to go forward
* Execute the `:bd` command to close and remove the Hacker News buffer


Enhanced Motions
----------------

Uppercase `J` and `K` are mapped to helpful new motions based on what type of
content is on the screen:

* Move to next/prev item when viewing the front page. (If the cursor is on a
  numbered line with story title the cursor will move to the next/prev numbered
  line with story title. If the cursor is on a comment line it will move to the
  next/prev comment line.)
* Move to next/prev comment when viewing comments.
* Move to next/prev paragraph when viewing the text version of articles.


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
