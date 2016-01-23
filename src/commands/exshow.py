#!/usr/bin/python3
import sys
import os.path
import base64

import extratermclient

def SendMimeTypeData(filename, mimeType, charset):
    extratermclient.startFileTransfer(mimeType, charset, filename)
    with open(filename,'rb') as fhandle:
        contents = fhandle.read(3*10240)    # This must be a multiple of 3 to keep concatinated base64 working.
        while len(contents) != 0:
            print(base64.b64encode(contents).decode(),end='')
            contents = fhandle.read(3*10240)
    extratermclient.endFileTransfer()

mimeTypeMap = {
    "bmp": "image/bmp",
    "dib": "image/bmp",
    "png": "image/png",
    "gif": "image/gif",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "jpe": "image/jpeg",
    "jif": "image/jpeg",
    "jfif": "image/jpeg",
    "jfi": "image/jpeg",
    "webp": "image/webp"
}

# This little database is from CodeMirros' meta.js file which summerizes the supported syntax highlighting modes.
modeInfo = [
    {"name": "APL", "mime": "text/apl", "mode": "apl", "ext": ["dyalog", "apl"]},
    {"name": "PGP", "mimes": ["application/pgp", "application/pgp-keys", "application/pgp-signature"], "mode": "asciiarmor", "ext": ["pgp"]},
    {"name": "ASN.1", "mime": "text/x-ttcn-asn", "mode": "asn.1", "ext": ["asn", "asn1"]},
    {"name": "Asterisk", "mime": "text/x-asterisk", "mode": "asterisk", "file": "^extensions\.conf$"},
    {"name": "Brainfuck", "mime": "text/x-brainfuck", "mode": "brainfuck", "ext": ["b", "bf"]},
    {"name": "C", "mime": "text/x-csrc", "mode": "clike", "ext": ["c", "h"]},
    {"name": "C++", "mime": "text/x-c++src", "mode": "clike", "ext": ["cpp", "c++", "cc", "cxx", "hpp", "h++", "hh", "hxx"], "alias": ["cpp"]},
    {"name": "Cobol", "mime": "text/x-cobol", "mode": "cobol", "ext": ["cob", "cpy"]},
    {"name": "C#", "mime": "text/x-csharp", "mode": "clike", "ext": ["cs"], "alias": ["csharp"]},
    {"name": "Clojure", "mime": "text/x-clojure", "mode": "clojure", "ext": ["clj"]},
    {"name": "Closure Stylesheets (GSS)", "mime": "text/x-gss", "mode": "css", "ext": ["gss"]},
    {"name": "CMake", "mime": "text/x-cmake", "mode": "cmake", "ext": ["cmake", "cmake.in"], "file": "^CMakeLists.txt$"},
    {"name": "CoffeeScript", "mime": "text/x-coffeescript", "mode": "coffeescript", "ext": ["coffee"], "alias": ["coffee", "coffee-script"]},
    {"name": "Common Lisp", "mime": "text/x-common-lisp", "mode": "commonlisp", "ext": ["cl", "lisp", "el"], "alias": ["lisp"]},
    {"name": "Cypher", "mime": "application/x-cypher-query", "mode": "cypher", "ext": ["cyp", "cypher"]},
    {"name": "Cython", "mime": "text/x-cython", "mode": "python", "ext": ["pyx", "pxd", "pxi"]},
    {"name": "Crystal", "mime": "text/x-crystal", "mode": "crystal", "ext": ["cr"]},
    {"name": "CSS", "mime": "text/css", "mode": "css", "ext": ["css"]},
    {"name": "CQL", "mime": "text/x-cassandra", "mode": "sql", "ext": ["cql"]},
    {"name": "D", "mime": "text/x-d", "mode": "d", "ext": ["d"]},
    {"name": "Dart", "mimes": ["application/dart", "text/x-dart"], "mode": "dart", "ext": ["dart"]},
    {"name": "diff", "mime": "text/x-diff", "mode": "diff", "ext": ["diff", "patch"]},
    {"name": "Django", "mime": "text/x-django", "mode": "django"},
    {"name": "Dockerfile", "mime": "text/x-dockerfile", "mode": "dockerfile", "file": "^Dockerfile$"},
    {"name": "DTD", "mime": "application/xml-dtd", "mode": "dtd", "ext": ["dtd"]},
    {"name": "Dylan", "mime": "text/x-dylan", "mode": "dylan", "ext": ["dylan", "dyl", "intr"]},
    {"name": "EBNF", "mime": "text/x-ebnf", "mode": "ebnf"},
    {"name": "ECL", "mime": "text/x-ecl", "mode": "ecl", "ext": ["ecl"]},
    {"name": "Eiffel", "mime": "text/x-eiffel", "mode": "eiffel", "ext": ["e"]},
    {"name": "Elm", "mime": "text/x-elm", "mode": "elm", "ext": ["elm"]},
    {"name": "Embedded Javascript", "mime": "application/x-ejs", "mode": "htmlembedded", "ext": ["ejs"]},
    {"name": "Embedded Ruby", "mime": "application/x-erb", "mode": "htmlembedded", "ext": ["erb"]},
    {"name": "Erlang", "mime": "text/x-erlang", "mode": "erlang", "ext": ["erl"]},
    {"name": "Factor", "mime": "text/x-factor", "mode": "factor", "ext": ["factor"]},
    {"name": "Forth", "mime": "text/x-forth", "mode": "forth", "ext": ["forth", "fth", "4th"]},
    {"name": "Fortran", "mime": "text/x-fortran", "mode": "fortran", "ext": ["f", "for", "f77", "f90"]},
    {"name": "F#", "mime": "text/x-fsharp", "mode": "mllike", "ext": ["fs"], "alias": ["fsharp"]},
    {"name": "Gas", "mime": "text/x-gas", "mode": "gas", "ext": ["s"]},
    {"name": "Gherkin", "mime": "text/x-feature", "mode": "gherkin", "ext": ["feature"]},
    {"name": "GitHub Flavored Markdown", "mime": "text/x-gfm", "mode": "gfm", "file": "^(readme|contributing|history).md$"},
    {"name": "Go", "mime": "text/x-go", "mode": "go", "ext": ["go"]},
    {"name": "Groovy", "mime": "text/x-groovy", "mode": "groovy", "ext": ["groovy"]},
    {"name": "HAML", "mime": "text/x-haml", "mode": "haml", "ext": ["haml"]},
    {"name": "Haskell", "mime": "text/x-haskell", "mode": "haskell", "ext": ["hs"]},
    {"name": "Haskell (Literate)", "mime": "text/x-literate-haskell", "mode": "haskell-literate", "ext": ["lhs"]},
    {"name": "Haxe", "mime": "text/x-haxe", "mode": "haxe", "ext": ["hx"]},
    {"name": "HXML", "mime": "text/x-hxml", "mode": "haxe", "ext": ["hxml"]},
    {"name": "ASP.NET", "mime": "application/x-aspx", "mode": "htmlembedded", "ext": ["aspx"], "alias": ["asp", "aspx"]},
    {"name": "HTML", "mime": "text/html", "mode": "htmlmixed", "ext": ["html", "htm"], "alias": ["xhtml"]},
    {"name": "HTTP", "mime": "message/http", "mode": "http"},
    {"name": "IDL", "mime": "text/x-idl", "mode": "idl", "ext": ["pro"]},
    {"name": "Jade", "mime": "text/x-jade", "mode": "jade", "ext": ["jade"]},
    {"name": "Java", "mime": "text/x-java", "mode": "clike", "ext": ["java"]},
    {"name": "Java Server Pages", "mime": "application/x-jsp", "mode": "htmlembedded", "ext": ["jsp"], "alias": ["jsp"]},
    {"name": "JavaScript", "mimes": ["text/javascript", "text/ecmascript", "application/javascript", "application/x-javascript", "application/ecmascript"],
     "mode": "javascript", "ext": ["js"], "alias": ["ecmascript", "js", "node"]},
    {"name": "JSON", "mimes": ["application/json", "application/x-json"], "mode": "javascript", "ext": ["json", "map"], "alias": ["json5"]},
    {"name": "JSON-LD", "mime": "application/ld+json", "mode": "javascript", "ext": ["jsonld"], "alias": ["jsonld"]},
    {"name": "JSX", "mime": "text/jsx", "mode": "jsx", "ext": ["jsx"]},
    {"name": "Jinja2", "mime": "null", "mode": "jinja2"},
    {"name": "Julia", "mime": "text/x-julia", "mode": "julia", "ext": ["jl"]},
    {"name": "Kotlin", "mime": "text/x-kotlin", "mode": "clike", "ext": ["kt"]},
    {"name": "LESS", "mime": "text/x-less", "mode": "css", "ext": ["less"]},
    {"name": "LiveScript", "mime": "text/x-livescript", "mode": "livescript", "ext": ["ls"], "alias": ["ls"]},
    {"name": "Lua", "mime": "text/x-lua", "mode": "lua", "ext": ["lua"]},
    {"name": "Markdown", "mime": "text/x-markdown", "mode": "markdown", "ext": ["markdown", "md", "mkd"]},
    {"name": "mIRC", "mime": "text/mirc", "mode": "mirc"},
    {"name": "MariaDB SQL", "mime": "text/x-mariadb", "mode": "sql"},
    {"name": "Mathematica", "mime": "text/x-mathematica", "mode": "mathematica", "ext": ["m", "nb"]},
    {"name": "Modelica", "mime": "text/x-modelica", "mode": "modelica", "ext": ["mo"]},
    {"name": "MUMPS", "mime": "text/x-mumps", "mode": "mumps"},
    {"name": "MS SQL", "mime": "text/x-mssql", "mode": "sql"},
    {"name": "MySQL", "mime": "text/x-mysql", "mode": "sql"},
    {"name": "Nginx", "mime": "text/x-nginx-conf", "mode": "nginx", "file": "nginx.*\.conf$"},
    {"name": "NSIS", "mime": "text/x-nsis", "mode": "nsis", "ext": ["nsh", "nsi"]},
    {"name": "NTriples", "mime": "text/n-triples", "mode": "ntriples", "ext": ["nt"]},
    {"name": "Objective C", "mime": "text/x-objectivec", "mode": "clike", "ext": ["m", "mm"]},
    {"name": "OCaml", "mime": "text/x-ocaml", "mode": "mllike", "ext": ["ml", "mli", "mll", "mly"]},
    {"name": "Octave", "mime": "text/x-octave", "mode": "octave", "ext": ["m"]},
    {"name": "Oz", "mime": "text/x-oz", "mode": "oz", "ext": ["oz"]},
    {"name": "Pascal", "mime": "text/x-pascal", "mode": "pascal", "ext": ["p", "pas"]},
    {"name": "PEG.js", "mime": "null", "mode": "pegjs", "ext": ["jsonld"]},
    {"name": "Perl", "mime": "text/x-perl", "mode": "perl", "ext": ["pl", "pm"]},
    {"name": "PHP", "mime": "application/x-httpd-php", "mode": "php", "ext": ["php", "php3", "php4", "php5", "phtml"]},
    {"name": "Pig", "mime": "text/x-pig", "mode": "pig", "ext": ["pig"]},
    {"name": "Plain Text", "mime": "text/plain", "mode": "null", "ext": ["txt", "text", "conf", "def", "list", "log"]},
    {"name": "PLSQL", "mime": "text/x-plsql", "mode": "sql", "ext": ["pls"]},
    {"name": "Properties files", "mime": "text/x-properties", "mode": "properties", "ext": ["properties", "ini", "in"], "alias": ["ini", "properties"]},
    {"name": "Python", "mime": "text/x-python", "mode": "python", "ext": ["py", "pyw"]},
    {"name": "Puppet", "mime": "text/x-puppet", "mode": "puppet", "ext": ["pp"]},
    {"name": "Q", "mime": "text/x-q", "mode": "q", "ext": ["q"]},
    {"name": "R", "mime": "text/x-rsrc", "mode": "r", "ext": ["r"], "alias": ["rscript"]},
    {"name": "reStructuredText", "mime": "text/x-rst", "mode": "rst", "ext": ["rst"], "alias": ["rst"]},
    {"name": "RPM Changes", "mime": "text/x-rpm-changes", "mode": "rpm"},
    {"name": "RPM Spec", "mime": "text/x-rpm-spec", "mode": "rpm", "ext": ["spec"]},
    {"name": "Ruby", "mime": "text/x-ruby", "mode": "ruby", "ext": ["rb"], "alias": ["jruby", "macruby", "rake", "rb", "rbx"]},
    {"name": "Rust", "mime": "text/x-rustsrc", "mode": "rust", "ext": ["rs"]},
    {"name": "Sass", "mime": "text/x-sass", "mode": "sass", "ext": ["sass"]},
    {"name": "Scala", "mime": "text/x-scala", "mode": "clike", "ext": ["scala"]},
    {"name": "Scheme", "mime": "text/x-scheme", "mode": "scheme", "ext": ["scm", "ss"]},
    {"name": "SCSS", "mime": "text/x-scss", "mode": "css", "ext": ["scss"]},
    {"name": "Shell", "mime": "text/x-sh", "mode": "shell", "ext": ["sh", "ksh", "bash"], "alias": ["bash", "sh", "zsh"], "file": "^PKGBUILD$"},
    {"name": "Sieve", "mime": "application/sieve", "mode": "sieve", "ext": ["siv", "sieve"]},
    {"name": "Slim", "mimes": ["text/x-slim", "application/x-slim"], "mode": "slim", "ext": ["slim"]},
    {"name": "Smalltalk", "mime": "text/x-stsrc", "mode": "smalltalk", "ext": ["st"]},
    {"name": "Smarty", "mime": "text/x-smarty", "mode": "smarty", "ext": ["tpl"]},
    {"name": "Solr", "mime": "text/x-solr", "mode": "solr"},
    {"name": "Soy", "mime": "text/x-soy", "mode": "soy", "ext": ["soy"], "alias": ["closure template"]},
    {"name": "SPARQL", "mime": "application/sparql-query", "mode": "sparql", "ext": ["rq", "sparql"], "alias": ["sparul"]},
    {"name": "Spreadsheet", "mime": "text/x-spreadsheet", "mode": "spreadsheet", "alias": ["excel", "formula"]},
    {"name": "SQL", "mime": "text/x-sql", "mode": "sql", "ext": ["sql"]},
    {"name": "Squirrel", "mime": "text/x-squirrel", "mode": "clike", "ext": ["nut"]},
    {"name": "Swift", "mime": "text/x-swift", "mode": "swift", "ext": ["swift"]},
    {"name": "MariaDB", "mime": "text/x-mariadb", "mode": "sql"},
    {"name": "sTeX", "mime": "text/x-stex", "mode": "stex"},
    {"name": "LaTeX", "mime": "text/x-latex", "mode": "stex", "ext": ["text", "ltx"], "alias": ["tex"]},
    {"name": "SystemVerilog", "mime": "text/x-systemverilog", "mode": "verilog", "ext": ["v"]},
    {"name": "Tcl", "mime": "text/x-tcl", "mode": "tcl", "ext": ["tcl"]},
    {"name": "Textile", "mime": "text/x-textile", "mode": "textile", "ext": ["textile"]},
    {"name": "TiddlyWiki ", "mime": "text/x-tiddlywiki", "mode": "tiddlywiki"},
    {"name": "Tiki wiki", "mime": "text/tiki", "mode": "tiki"},
    {"name": "TOML", "mime": "text/x-toml", "mode": "toml", "ext": ["toml"]},
    {"name": "Tornado", "mime": "text/x-tornado", "mode": "tornado"},
    {"name": "troff", "mime": "troff", "mode": "troff", "ext": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]},
    {"name": "TTCN", "mime": "text/x-ttcn", "mode": "ttcn", "ext": ["ttcn", "ttcn3", "ttcnpp"]},
    {"name": "TTCN_CFG", "mime": "text/x-ttcn-cfg", "mode": "ttcn-cfg", "ext": ["cfg"]},
    {"name": "Turtle", "mime": "text/turtle", "mode": "turtle", "ext": ["ttl"]},
    {"name": "TypeScript", "mime": "application/typescript", "mode": "javascript", "ext": ["ts"], "alias": ["ts"]},
    {"name": "Twig", "mime": "text/x-twig", "mode": "twig"},
    {"name": "VB.NET", "mime": "text/x-vb", "mode": "vb", "ext": ["vb"]},
    {"name": "VBScript", "mime": "text/vbscript", "mode": "vbscript", "ext": ["vbs"]},
    {"name": "Velocity", "mime": "text/velocity", "mode": "velocity", "ext": ["vtl"]},
    {"name": "Verilog", "mime": "text/x-verilog", "mode": "verilog", "ext": ["v"]},
    {"name": "VHDL", "mime": "text/x-vhdl", "mode": "vhdl", "ext": ["vhd", "vhdl"]},
    {"name": "XML", "mimes": ["application/xml", "text/xml"], "mode": "xml", "ext": ["xml", "xsl", "xsd"], "alias": ["rss", "wsdl", "xsd"]},
    {"name": "XQuery", "mime": "application/xquery", "mode": "xquery", "ext": ["xy", "xquery"]},
    {"name": "YAML", "mime": "text/x-yaml", "mode": "yaml", "ext": ["yaml", "yml"], "alias": ["yml"]},
    {"name": "Z80", "mime": "text/x-z80", "mode": "z80", "ext": ["z80"]},
    {"name": "mscgen", "mime": "text/x-mscgen", "mode": "mscgen", "ext": ["mscgen", "mscin", "msc"]},
    {"name": "xu", "mime": "text/x-xu", "mode": "mscgen", "ext": ["xu"]},
    {"name": "msgenny", "mime": "text/x-msgenny", "mode": "mscgen", "ext": ["msgenny"]}
  ];
  
def FilenameToTextMimetype(name):
    lowerfilename = name.lower()
    if '.' in lowerfilename:
        extension = lowerfilename.split('.')[-1]
        for modeRecord in modeInfo:
            if "ext" in modeRecord and extension in modeRecord["ext"]:
                if "mime" in modeRecord:
                    return modeRecord["mime"]
                else:
                    if "mimes" in modeRecord:
                        return modeRecord["mimes"][0]
    return None

def FilenameToImageMimetype(name):
    lowerfilename = name.lower()
    if '.' in lowerfilename:
        extension = lowerfilename.split('.')[-1]
        if extension in mimeTypeMap:
            return mimeTypeMap[extension]
    return None
    

def Show(filename):
    if os.path.exists(filename):
        charset = None
        mimeType = FilenameToTextMimetype(os.path.basename(filename))
        if mimeType is not None:
            charset = "utf8"
        else:
            mimeType = FilenameToImageMimetype(os.path.basename(filename))
            if mimeType is None:
                mimeType = "text/plain"
                charset = "utf8"
        SendMimeTypeData(filename, mimeType, charset)
        return 0
    else:
        print("Unable to open file {0}.".format(filename))
        return 3

def main():
    if not extratermclient.isExtraterm():
        print("Sorry, you're not using Extraterm.")
        return 1

    for filename in sys.argv[1:]:
        return Show(filename)

main()
