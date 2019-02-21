Title: Recursive search and replace
Date: 2018-05-21 12:00
Category: hint
Slug: hints/search-and-replace
Author: Phil Elson

I had a need to recursively search and replace for a particular string within a git repository.
A combination of find and sed is all that is needed, but one must be careful to avoid modifying the contents of the ".git" directory (I accidentally did this, and effectively destroyed my clone).

The command necessary on my OSX, in all its glory:

```

LC_ALL=C find . \
    -path ./.git -prune \
    -o -type f \
    -exec sh -c 'sed -i "" -- "s|old|new|g" {};' \;

```

Unfortunately, this has the effect of adding newlines at the end of each file that doesn't have them.
This can be seen in a number of StackOverflow questions, such as 
[this one](https://stackoverflow.com/questions/13325138/why-does-sed-add-a-new-line-in-osx).

Instead of sed therefore, perl can be used instead:

```
LC_ALL=C find . \
    -path ./.git -prune \
    -o -type f \
    -exec sh -c 'perl -pi -e "s|old|new|g" {};' \;
```
