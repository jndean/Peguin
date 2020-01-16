# Peguin

A general purpose PEG (Parsing Expression Grammar) parser generator, which I wrote so I could generate an "infinite-lookahead" parser for [railway](https://github.com/jndean/railway) code to replace the old LR(1) one. The main program, _parsergenerator.py_, takes any grammar file (files with the .peg extension in this repository) and produces python code which can parse (pre-tokenised) files that adhere to the described grammar rules. It takes a lot from the [blog posts](https://medium.com/@gvanrossum_83706/peg-parsers-7ed72462f97c) on PEG parsers by Guido van Rossum.

As an example, the rule defining how to parse railway if statements in one of these grammars looks like this:

```peg
if_stmt : 'if' '(' expression ')' NEWLINE
              statement*
          ('else' NEWLINE
              statement* {t2} )?
          'fi' '(' expression? ')'
          { If(t2, t5, t6, t9) };
```



### Partially self-hosting?

When writing the parser generator, I had to write something which would parse a grammar file and turn it into a parser. If only I had a way to generate a parser for those grammar files... 

The _bootstrapparsergenerator.py_ defines a very restricted form of the parser generator which I hand coded, and doesn't support 'fancy' operators like Repeat, Optional, Join, Greedy etc. I then wrote the metagrammar in _Grammars/metagrammar.peg_, which is a grammar defining how to fully parse grammar files (.peg files) but itself only using the restricted set of features available in the bootstrapper. The final _parsergenerator.py_ is then the result of running the bootstrap parser generator on the metagrammar. It is able to parse its own grammar and generate itself, hence my claim that it is partially self-hosted.



### Join and Greedy?

Most of the operators available for writing grammars will be familiar from other places, for example the two Repeat operators ( __*__ and __+__) , the Optional operator (__?__) and the Or operator (__|__). I did make up some new ones, Join and Greedy, which made my life easier in the railway parser generator but might be a bit superficial. 

The Join operator (__^__) is a binary operator which generates a rule to match lists, whose elements match the left hand argument and are separated by the tokens matching the right hand argument. The list may be empty, so a join rule will always match. For example, to parse a comma-separated tuple of expressions you can write this rule:

```PEG
tuple : '(' expression ^ ',' ')' {t1};
```

rather than some rule using the Repeat and Or operators such as:

```PEG
tuple : '(' expression (',' expression {t1})* ')' { [t1] + t2 }
      | '(' ')'                                   { []        };
```

The Greedy operator (__$__) is another binary operator acting like an Or operator, except rather than short-circuiting after any option matches, it will try to parse all options and return the one which consumed the most tokens. I use it to generate parsing rules for the "call chains" in railway code, where calls are strung together by arrows but the arrows can go in either direction. Here are 3 examples of valid railway call chains.

```railway
call make_data() => call compress() => uncall decrypt(key)
uncall make_data() <= uncall compress() <= call decrypt(key)
call dothings(arg1, arg2)
```

The following rule does not parse all these chains correctly

```PEG
call_chain : call_block ^ '=>' | call_block ^ '<=' ;
```

because, if the chain uses left arrows like the second example, the right arrow part of the rule runs first, manages to parse a list of one call_blocks (before it hits the left arrow token and returns), and so the whole Or statement and hence the whole call_chain rule returns having consumed only the first call_block. With the greedy operator I can write the rule like this

```PEG
call_chain : (call_block ^ '=>') $ (call_block ^ '<=');
```

which ensures both versions are attempted and the one that consumes the most tokens is selected. The brackets are for clarity, they are not necessary due to the precedence of the operators.

### Docs

There are no docs. If you want a parser generator, PEG or otherwise, you should google a serious one, like [TatSu](https://github.com/neogeny/TatSu).