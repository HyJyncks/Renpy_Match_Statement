# Renpy Match Statement
The bulk of this file is a simple implementation of a match-like workflow for renpy script. It uses the same `match` `case` and `_` keywords, `_` being the wildcard. As of right now it only supports cases in blocks, meaning you need a colon, return and indent to process what happens. The statement compares a variable against the cases and returns the block of renpy code to advance the script. Obviously, this isn't, and shouldn't, be limited to number values. This is just the simplest way to demonstrate

```py

default x = 0


label start:

    "This is the first line of dialogue. Have a random number!"
    $ x = renpy.random.randint(0, 3)
    match x:
        case 0:
            "You got zero! Try again"
            jump start
        case 1:
            "You got 1! Let's move on"
        case 2 | 3:
            "Uh oh, 2 or 3 means you lose."
            return
        case _:
            "How did you even get here??"
```

The wildcard also works in lists, from what I've tested, ie `[1, 2, _]` would match the list `[1, 2, 453]` (or any value of any kind). My testing has been limited, as this was just me learning how to use Renpy CDS.

# Installation

To "install" just add the `0_statements.rpy` to your `game/` folder. It is a CDS and needs to be loaded earlier than when it's used in the game. So ideally, you leave this in the game folder.

## Bonus

There is also a statement for `notify` in there as well, which adds that to renpy script as well. Eliminating the `$ renpy.notify(...)` and instead allowing you to do:
```py
default z = 123
label start:
    "Hello!"
    notify "The narrator said hello, and z equals [z]"
```
You'll need to modify the notify screen to allow variable interpolation (and text tags) but that's simple enough to do and not in the scope of this little bit of code.
