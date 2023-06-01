from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        pass
    

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """

        try:
            self.mustBe("keyword", "class")
            ret = self.compileClass()
        except ParseException:
            raise ParseException()
    

        return ret
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """

        try:
            program = ParseTree("class", None)
            program.addChild(Token("keyword", "class"))
            program.addChild(self.mustBe("identifier", None))
            program.addChild(self.mustBe("symbol", "{"))

            while self.have("symbol", "}") is False:
                if self.have("keyword", "static") or self.have("keyword", "field"):
                    self.compileClassVarDec()
                elif self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method"):
                    self.compileSubroutine()

            program.addChild(self.mustBe("symbol", "}"))

        except ParseException:
            raise ParseException()

        return program
    
    def staticOrField(self):
        """
        Checks if val is either static or field
        @return "static" or "field" or ParseException
        """

        if self.have(None, "static"): 
            return "static"
        elif self.have(None, "field"): 
            return "field"
        else: 
            raise ParseException()

    def varType(self):
        """
        Checks if val is any of the var types
        @return Var types or ParseException
        """

        if self.have(None, "int"): 
            return "int"
        elif self.have(None, "char"):
            return "char"
        elif self.have(None, "boolean"):
            return "boolean"
        elif self.have(None, "void"):
            return "void"
        else:
            raise ParseException()
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """

        try:
            classVar = ParseTree("classVarDec")
            classVar.addChild(self.mustBe("keyword", self.staticOrField()))
            classVar.addChild(self.mustBe("keyword", self.varType()))
            classVar.addChild(self.mustBe("identifier", None))
            classVar.addChild(self.mustBe("symbol", ";"))
        except ParseException:
            raise ParseException()

        return classVar 
    
    def subroutineTypeCheck(self):
        """
        Checks if val is any of the subroutine accepted types
        @return subroutine accepted types or ParseException
        """

        if self.have(None, "constructor"): 
            return "static"
        elif self.have(None, "function"): 
            return "field"
        elif self.have(None, "method"): 
            return "field"
        else: 
            raise ParseException()
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """

        try:
            subroutine = ParseTree("subroutine", None)
            subroutine.addChild(self.mustBe("keyword", self.subroutineTypeCheck()))
            subroutine.addChild(self.mustBe("keyword", self.varType()))
            subroutine.addChild(self.mustBe("identifier", None))
            subroutine.addChild(self.mustBe("symbol", "("))
            if self.have("symbol", ")") is False:
                subroutine.addChild(self.compileParameterList())
            subroutine.addChild(self.mustBe("symbol", ")"))
            subroutine.addChild(self.compileSubroutineBody())
        except ParseException:
            raise ParseException()

        return subroutine 
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """

        try:
            params = ParseTree("parameterList", None)
            while self.have("symbol", ")") is False:
                params.addChild(self.mustBe("keyword", self.varType()))
                params.addChild(self.mustBe("identifier", None))
                if self.have("symbol", ","):
                    params.addChild(self.mustBe("symbol", ","))
        
        except ParseException:
            raise ParseException()

        return params 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """

        try:
            body = ParseTree("subroutineBody")

            body.addChild(self.mustBe("symbol", "{"))
            while self.have("symbol", "}") is False:
                if self.have("keyword", "var"):
                    body.addChild(self.compileVarDec())
                elif self.have("keyword", "let") or self.have("keyword", "if") or self.have("keyword", "while") or self.have("keyword", "do") or self.have("keyword", "return"):
                    body.addChild(self.compileStatements())
                
        except ParseException:
            raise ParseException()
        
        return body 
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """

        try:
            varDec = ParseTree("varDec", None)
            varDec.addChild(self.mustBe("keyword", "var"))
            varDec.addChild(self.mustBe("keyword", self.varType()))
            varDec.addChild(self.mustBe("identifier", None))
            varDec.addChild(self.mustBe("symbol", ";"))
        except ParseException:
            raise ParseException()

        return varDec 
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        return None 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        return None 

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        return None 


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 


    def next(self):
        """
        Advance to the next token
        """
        if self.tokens is not None:
            del self.tokens[0]
        return


    def current(self):
        """
        Return the current token
        @return the token
        """

        if self.tokens is not None:
            return self.tokens[0]

        return None


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """

        currentToken = self.current()

        if currentToken == None:
            return False
        
        if currentToken.getType() == expectedType or expectedType == None:
            if currentToken.getValue() == expectedValue or expectedValue == None:
                return True
 
        return False


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """

        if self.have(expectedType, expectedValue):
            currentToken = self.current()
            self.next()
            return currentToken
        
        raise ParseException("Not Matching")

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","Main"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    # tokens.append(Token("keyword", "static"))
    # tokens.append(Token("keyword", "int"))
    # tokens.append(Token("identifier", "a"))
    # tokens.append(Token("symbol", ";"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
