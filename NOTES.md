Design Notes for pyTab Project
==============================


# 2019-03-08
Some thoughts about how the reading and writing of tabs should be handled. My
original thinking was to handle this entirely through the main program, but now
I am thinking that is makes sense to define a file convention within the tab
class itself, thus abstracting it from the main program. So, I will maintain
the skeleton that currently exists, calling for `open()` and `save()` class
methods. 

In addition, there probably needs to be a method to set the tab info.
At present, the tab information will be held in a dictionary data spec of the
class instance. This will facilitate reading in files, storing their
information, and then writing back to them again. 

In general, I need to be careful not to try and replicate a fully-functional
GUI too much, as the immediate goal is to get to a useable prototype.


# 2019-03-11
I need to figure out what I want the arguments to the `get_tab()` and
`save_tab()` methods to be. Crucially, I need to revisit how keyword arguments
and dictionaries interact so that there are keyword arguments to `save_tab()`
that align with the `info` class data container which is a dictionary.

I think a solution will involve having a function that takes keyword arguments
and correctly assigns them to the `info` class data container (what is the
correct terminology here?).

UPDATE: I went ahead with this strategy of having keyword arguments that can be
passed through the `get_tab()` and `save_tab()` functions using `**kwargs` and
then onto the `set_info()` method such that the tab information can be updated
through calls to any of these class methods.


# 2019-03-21
I need to decide on how the text file convention should be specified and the
best way is to write to the file. Should I define/use a template? Or are a
series of `file.write('<string>')` statements fine? A question for another day.


# 2019-04-09
I am now questioning whether the decision to overwrite the output file should
be handled in the main program rather than in the `save_tab` method. From the
perspective of a class module that could be used in a arbitrary context, the
decision to prompt for user input seems ill advised.


# 2019-05-21
The `write`, `forward`, and `backward` methods of the tab class all currently
print a portion of the tab before exiting. This is undesirable from the
perspective of using the tab class outside of the pyTab main program. These
print commands (which are already a class method) should be moved the pyTab
main program itself.
