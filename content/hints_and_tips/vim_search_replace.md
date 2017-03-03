Title: Vim search and replace across many files
Date: 2015-12-03 12:00
Category: hint
Slug: hints/vim_search_replace
Author: Phil Elson


A powerful combination of commands for search and replace across multiple files with Vim.

<!-- PELICAN_END_SUMMARY -->


http://vim.wikia.com/wiki/Opening_multiple_files_from_a_single_command-line
http://vim.wikia.com/wiki/Search_and_replace_in_multiple_buffers


```
:arg **/*.cpp

:argdo %s/pattern/replace/ge | update   

```
