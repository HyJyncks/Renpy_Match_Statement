python early:
    
    def parse_notif(lexer):
        words = lexer.string()
        return words

    def exec_notif(po):
        renpy.notify(po)

    def lint_notif(po):
        tags = renpy.check_text_tags(po)
        if tags:
            renpy.error(tags)

    renpy.register_statement("notify", parse = parse_notif, execute = exec_notif, lint = lint_notif)


    def parse_match(lex):

        # Empty dict for variable:renpy block pairs
        blocks = {}

        # Tells match to require a variable, colon, and block
        var = lex.require(lex.simple_expression, "variable")
        lex.require(":")
        lex.expect_eol()
        lex.expect_block("match")
        sub = lex.subblock_lexer()

        # Loop through the sub block
        while sub.advance():
            with sub.catch_error():
                
                # Require the case, save the item to compare, require a colon, and save the block of renpy code
                sub.keyword("case")
                comp = sub.require(sub.simple_expression, "case")
                sub.require(":")
                sub.expect_eol()
                sub.expect_block("case")
                rb = sub.subblock_lexer().renpy_block()
                blocks[comp] = rb

        return (var, blocks)


    def exec_match(po): # For testing
        var, blocks = po

    # Handle what to show next
    def next_match(po):
        var, blocks = po
        var = eval(var)

        for ke in blocks.keys():

            # Eval the key for easy comparison later
            newkey = eval(ke)

            # First check if any keys are equal to the variable
            if newkey == var:
                return blocks[ke]

            # Check the 'or' operator "|"
            if "|" in ke:
                if any(eval(z.strip())==var for z in ke.split("|")):
                    return blocks[ke]

            # If it's a list, compare individual values
            if type(var) == list or type(var) == tuple and len(var)==len(newkey):

                # Try to avoid error if newkey is not an iterable
                try:
                    if all(i1 == i2 or i2 == _ for (i1, i2) in zip(var, newkey)):
                        return blocks[ke]
                except:
                    pass

        # If case has underscore wildcard execute block if no matches occur
        if "_" in blocks.keys():
            return blocks["_"]

    # Lint only occurs during lint check
    def lint_match(po):

        var, blocks = po

        try:
            eval(var)
        except Exception:
            renpy.error(f"Value {var} is not defined.")
        
        for ke in blocks.keys():

            if "|" in ke:
                for ite in ke.split("|"):
                    try:
                        eval(ite.strip())
                    except Exception:
                        renpy.error(f"Case value {ite} is not a valid datatype")
            else:
                try:
                    eval(ke)
                except Exception:
                    renpy.error(f"Case value {ke} is not a valid datatype.")


    renpy.register_statement("match", parse=parse_match, next = next_match, lint = lint_match, block = True, execute = exec_match)