Title: cf-units get (La)TeX unit repr... and a UDUNITS-2 parser to boot
Date: 2019-02-15
Category: field-notes
Tags: cf-units, UDUNITS-2
Slug: cf_units_tex
Author: Phil Elson

I recently worked on a feature to allow [cf-units](https://github.com/SciTools/cf-units) to produce a [TeX](https://en.wikipedia.org/wiki/TeX) representation of a unit so that it can be quickly copy-and-pasted into a LaTeX document, or simply visualised nicely with [matplotlib's LaTeX writer](https://matplotlib.org/users/usetex.html).

It turns out that "doing it right" was quite involved, and has ultimately led to some really interesting opportunities for those who use UDUNITS-2. This article expliains what was involved, and briefly discusses some of those opportunities.

<!-- PELICAN_END_SUMMARY -->

### tl;dr

If you came here to find out how to turn your UDUNITS-2 compatible unit into a (La)TeX string, you need
python 3 and [cf-units](https://github.com/SciTools/cf-units) (version ``>=2.1``):

```
>>> from cf_units.tex import tex
>>> print(tex('microW per s'))
'\frac{{\mu}W}{s}'
```

Read on if you want to find out about the journey to this functionality...

### Motivation

The cf-units implementation goes out of its way to ensure common Earth Sciences units are preserved as much as possible when interfacing with UDUNITS-2. For example, specific humidity is the density of water vapor (kg/m3) divided by the density of all air, and [is commonly expressed in "grams per killogram"](https://www.e-education.psu.edu/meteo300/node/519). It seems that expressing the unit as "grams per killogram" rather than a dimensionless unit helps to avoid doubt about whether the quantity is a mass ratio [or a volume ratio](https://earthscience.stackexchange.com/questions/5033), and so I've had a number of people state that expressing the unit as "g/kg" is prefered.

Unfortunately, when *parsing* the unit "g km-1" UDUNITS-2 does the reasonable thing of simplifying it to its dimensionless form. There is no way for UDUNITS-2 to hold on to this information - the [parsing is tightly bound to the units-system in operation](https://github.com/Unidata/UDUNITS-2/issues/81). In order to turn "g/kg" into a TeX representation, we will therefore first need to parse the string ourselves.

### UDUNITS-2 parsing

The UDUNITS-2 includes a Backus–Naur form of its [unit grammar](https://www.unidata.ucar.edu/software/udunits/udunits-2.0.4/udunits2lib.html#Grammar), so you might think that we can use this directly in a parser generator such as [bison](http://www.gnu.org/software/bison/). Unfortunately, the documented grammar doesn't actually reflect what is implemented in UDUNITS-2 ([issue](https://github.com/Unidata/UDUNITS-2/issues/81)) as the actual rules are much more sensitive to state than they first appear.

For example, in UDUNITS-2 ``m2.3`` is equivalent to the unit ``3*m^2`` whereas ``2.3m`` is ``2.3 * m``, and so we can't tokenize floats unless we know the context of what we have already seen.

Writing a parser often involves two independent steps: tokenizing the input with a lexer, and then parsing the tokens using a grammar (for example, if parsing a spoken language the lexer would turn characters into words, and the parser would turn words into gramatically correct sentences). In the UDUNITS-2 case it would simplify the grammar rules if we can encapsulate some of the necessary state into the lexer's rules. It is for this reason (combined with ease of use and desired target language for the generated parser) that I choose to use [ANTLR](https://www.antlr.org/) as my parser generator.


### ANTLR

ANTRL is "ANother Tool for Language Recognition" and is "a powerful parser generator for reading, processing, executing, or translating structured text or binary files". Whilst it is written in Java, it can generate parsers for a number of desired languages, including Python.

It took me several days to become familiar enough with the tool to use ANTLR to its full potential (coming from a place of having never written a formal grammar before), but I ultimately was able to take the documented UDUNITS-2 grammar and translate it to a ANTLR (v4) compatible form.

The **most** important thing that I did whilst developing the grammar was to have a comprehensive test suite of cases - I ended up with [several hundred forms of unit supported by UDUNITS-2](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/tests/integration/parse/test_parse.py#L26-L144).
Not only did this help me quickly learn the ANTLR ropes, but I was also able to spot performance regressions when handling left-recursive cases (for example, ``meters second-1`` is actually two separate units joined together by the rule ``unit: base_unit | (unit whitespace+ base_unit)``) ([actual rule](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/udunits2Parser.g4#L24)).

One issue I did encounter with ANTLR and its handling of state (known as lexer modes) is that there was a lot of duplication that would result in a grammar that was very easy to forget to update in all places. For this reason, I ended up templating the lexer rules using Jinja2 - allowing me to define the concepts once and apply them in several places ([example](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/udunits2Lexer.g4.jinja#L139-L141) and [jinja code](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/compile.py#L52-L77)). It seems that this might become a core part of the grammar language in the future, but for now the Jinja2 approach worked well for me.


### Parse tree into an abstract representation


Once I'd produced the ANTLR rules, it is easy to turn this into a parser in any of the supported langagues. In my case I chose the Python 3 target.

For the lexer:

```
java -jar <antlr-jarfile> -Dlanguage=Python3 udunits2Lexer.g4 -o ./parser/
```

And I chose to implement the parser itself using the visitor pattern rather than the [listener pattern](https://github.com/antlr/antlr4/blob/master/doc/listeners.md), this choice made it a little bit easier for me to create a context-free abstract representation later on:

```
java -jar <antlr-jarfile> -Dlanguage=Python3 udunits2Parser.g4 -no-listener -visitor -o ./parser/
```

With all of this in place, I went about producing a clean abstract representation of the unit that I could produce based on the parse tree. I implemented [basic nodes for an expression graph](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/graph.py#L19-L111), and a [Visitor to construct the graph](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/__init__.py#L42-LL167).

Finally, I had a simple unit representation that could be used for any purpose - including converting to (La)TeX. As an illustrative example, the unit ``kg m / s^2`` is shown below:

![A demonstration of the abstract unit expression]({attach}images/cf_units_tex_nodes.svg)

### Abstract graph to (La)TeX

Once I had the graph in the form illustrated above, converting it to TeX is relatively straightforward.
Out trusty friend the Visitor pattern makes light work of it with so few node types.

As an exercise for the reader, you may like to have a go yourself... Take the following expression produced with cf-units [expression nodes](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/graph.py):

```
import cf_units._udunits2_parser.graph as g

expr = g.Divide(lhs=g.Terminal(content='m'), 
                rhs=g.Terminal(content='s'))
```

Using the knowledge that Terminal nodes have a ".content" attribute, whereas binary nodes have a ``.lhs`` and a ``.rhs`` attribute, convert the expression into the following string:

```
\frac{m}{s}
```

You may wish to use the [Visitor base class](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/graph.py#L114-L140) provided (available as ``g.Visitor`` in the above code).

If you want more interesting cases, you can generate arbitrary expression graphs from UDUNITS-2 compatible strings:

```
>>> import cf_units._udunits2_parser as p
>>> p.parse('kg.m/s-2')
Divide(lhs=Multiply(lhs=Identifier(content='kg'), rhs=Identifier(content='m')), rhs=Raise(lhs=Identifier(content='s'), rhs=Number(content=-2)))
```

**Solution**: The actual implementation to turn an expression graph into TeX form is [available here](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/_udunits2_parser/graph.py#L114-L140).


### Opportunities of a working UDUNITS-2 grammar

#### CF conventions

The [Climate-Forecast (CF) conventions](http://cfconventions.org/) are designed to promote the processing and sharing of files created using the NetCDF API. The conventions are the common denominator of much of the open source Earth Sciences stack, so if you've ever used any Earth Sciences NetCDF data or tools, the chances are you've used the CF conventions. 

It has always struck me as odd that, when refering to metadata regarding the units of measure, the CF conventions [defer to an implementation](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html#units) (UDUNITS-2) rather than citing a specification or formal grammar.

Perhaps the grammar produced for this work could be adopted by the CF conventions, and UDUNITS-2 move to becoming the reference implementation rather than the standard itself?


#### Online unit validation

Once an ANTLR grammar has been defined, it is relatively easy to generate a parser for any of [ANTLR's runtime languages](https://github.com/antlr/antlr4/blob/4.7.2/doc/targets.md). This includes Python, C++, and JavaScript targets.
We could therefore quickly produce a browser based tool to validate UDUNITS-2 units on the client-side.

I put together a quick proof of concept that takes UDUNITS-2 compatible unit specifications and parses them entirely client-side. In theory this could be the basis for implementing a UDUNITS-2 like system natively in the browser. If you'd like to learn more tweet a request (@pypelson) for a write-up.

#### Alternative simplification and factoring

UDUNITS-2 comes with unit simplification and factorization, but there are tools out there that are even more powerful for this purpose. Once such tool is [SymPy](https://www.sympy.org/en/index.html). Given the ease of traversing the expression graph we now have for our unit, constructing a SymPy expression is relatively simple. I'm confident that we could combine this with the XML files that are shipped with UDUNITS-2 to entirely replace the UDUNITS-2 implementation, should we need to do such a thing.

A less controversial option is to improve the handling of offseted units. For example, degrees Celcisus (°C) is [defined by UDUNITS](https://github.com/Unidata/UDUNITS-2/blob/v2.2.27.6/lib/udunits2-derived.xml#L127-L136) to be ``Kelvin + 273.15``, yet offset units such as this [lose their offset when squared](https://github.com/Unidata/UDUNITS-2/issues/82) - if we were to use a tool such as SymPy to preserve the quantities we'd be able to benefit from its strong mathematical heritage and preserve these quantities.


### Python 3 only

This is the first feature that has been added to cf-units which is Python 3 only. The decision was pragmatic as cf-units isn't *quite* ready to drop legacy Python (though it is coming) but it was more work to get ANTLR to produce a Python 2 compatible parser.

Having syntactically invalid Python 2 code in a repository that supports Python 2 comes with a few challenges. We must ensrue that the Python 3 code is *never* imported (else you get a ``SyntaxError``, not an ``ImportError``).
This involves some care when handling packaging and test discovery. In the latter case it was necessary to define a [conftest](https://github.com/SciTools/cf-units/blob/v2.1.1/cf_units/conftest.py) to prevent pytest from importing the Python 3 files in order to discover tests it can run.

## Conclusion

It has been an interesting journey solving this problem. Having never written a full-blown parser before the ANTLR experience has been a real journey of discovery - I started out writing more and more parser rules to cover the corner cases, until I realised that a refactor of the lexer rules would make most of them redundant (a bit like how the more you know of the scipy stack, the shorter your code gets). I believe the [UDUNITS-2](https://www.unidata.ucar.edu/software/udunits/) library, and the Python wrapper [cf-units](https://github.com/SciTools/cf-units), are great choices for the CF conventions, but that it would also be healthy for the conventions to reference a specific grammar and base unit set, and for the conventions to cite UDUNITS-2 as a *reference implementation* rather than the specification itself.


Have a go with cf-units and its (La)TeX generation - there are definitely still cases that the grammar doesn't support, but on the whole it has excellent coverage.
If you have other ideas about how we can make use of this new capability, let me know (comments or via twitter).
