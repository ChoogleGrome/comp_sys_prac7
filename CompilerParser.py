from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        pass

    ############ HELPER FUNCS ############

    def varTypeCheck(self):
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
        

    def checkStatementType(self):
        """
        Checks if val is any of the statement types
        @return statement types or ParseException
        """       

        if self.have(None, "let"): 
            return "let"
        elif self.have(None, "if"):
            return "if"
        elif self.have(None, "while"):
            return "while"
        elif self.have(None, "do"):
            return "do"
        elif self.have(None, "return"):
            return "return"
        else:
            raise ParseException()
    
    ############ HELPER FUNCS ############

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """

        try:
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
            program.addChild(self.mustBe("keyword", "class"))
            program.addChild(self.mustBe("identifier", None))
            program.addChild(self.mustBe("symbol", "{"))

            while self.have("symbol", "}") is False:
                if self.have("keyword", "static") or self.have("keyword", "field"):
                    program.addChild(self.compileClassVarDec())
                elif self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method"):
                    program.addChild(self.compileSubroutine())

            program.addChild(self.mustBe("symbol", "}"))

        except ParseException:
            raise ParseException()

        return program

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """

        try:
            classVar = ParseTree("classVarDec", None)
            classVar.addChild(self.mustBe("keyword", self.classVarTypeCheck()))
            classVar.addChild(self.mustBe("keyword", self.varTypeCheck()))
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
            return "constructor"
        elif self.have(None, "function"): 
            return "function"
        elif self.have(None, "method"): 
            return "method"
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
            subroutine.addChild(self.mustBe("keyword", self.varTypeCheck()))
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
                params.addChild(self.mustBe("keyword", self.varTypeCheck()))
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
            body = ParseTree("subroutineBody", None)

            body.addChild(self.mustBe("symbol", "{"))
            while self.have("symbol", "}") is False:
                if self.have("keyword", "var"):
                    body.addChild(self.compileVarDec())
                elif self.have("keyword", "let") or self.have("keyword", "if") or self.have("keyword", "while") or self.have("keyword", "do") or self.have("keyword", "return"):
                    body.addChild(self.compileStatements())
            body.addChild(self.mustBe("symbol", "}"))
            
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
            varDec.addChild(self.mustBe("keyword", self.varTypeCheck()))
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

        try :
            statements = ParseTree("statements", None)

            if self.current().getType() != "keyword": raise ParseException()

            statementVal = self.checkStatementType()

            if statementVal == "let":
                statements.addChild(self.compileLet())
            elif statementVal == "if":
                statements.addChild(self.compileIf())
            elif statementVal == "while":
                statements.addChild(self.compileWhile())
            elif statementVal == "do":
                statements.addChild(self.compileDo())
            elif statementVal == "return":
                statements.addChild(self.compileReturn())

        except ParseException:
            raise ParseException()

        return statements 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """

        try:
            letTree = ParseTree("letStatement", None)

            letTree.addChild(self.mustBe("keyword", "let"))
            letTree.addChild(self.mustBe("identifier", None))
            letTree.addChild(self.mustBe("symbol", "="))
            letTree.addChild(self.compileExpression())
            letTree.addChild(self.mustBe("symbol", ";"))
        except ParseException:
            raise ParseException()

        return letTree 


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        try:
            ifTree = ParseTree("ifStatement", None)

            ifTree.addChild(self.mustBe("keyword", "if"))
            ifTree.addChild(self.mustBe("symbol", "("))
            ifTree.addChild(self.compileExpression())
            ifTree.addChild(self.mustBe("symbol", ")"))
            ifTree.addChild(self.mustBe("symbol", "{"))
            while self.have("symbol", "}") is False:
                ifTree.addChild(self.compileStatements())
            ifTree.addChild(self.mustBe("symbol", "}"))

            if self.have("keyword", "else") is True:
                ifTree.addChild(self.mustBe("keyword", "else"))
                ifTree.addChild(self.mustBe("symbol", "{"))
                while self.have("symbol", "}") is False:
                    ifTree.addChild(self.compileStatements())
                ifTree.addChild(self.mustBe("symbol", "}"))

        except ParseException:
            raise ParseException()

        return ifTree 

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        try:
            whileTree = ParseTree("whileStatement", None)

            whileTree.addChild(self.mustBe("keyword", "while"))
            whileTree.addChild(self.mustBe("symbol", "("))
            whileTree.addChild(self.compileExpression())
            whileTree.addChild(self.mustBe("symbol", ")"))
            whileTree.addChild(self.mustBe("symbol", "{"))
            while self.have("symbol", "}") is False:
                whileTree.addChild(self.compileStatements())
            whileTree.addChild(self.mustBe("symbol", "}"))

        except ParseException:
            raise ParseException()
        return whileTree 


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """

        try:
            doTree = ParseTree("doStatement", None)

            doTree.addChild(self.mustBe("keyword", "do"))
            doTree.addChild(self.compileExpression())
            doTree.addChild(self.mustBe("symbol", ";"))

        except ParseException:
            raise ParseException()
        return doTree 


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        try:
            returnTree = ParseTree("returnStatement", None)

            returnTree.addChild(self.mustBe("keyword", "return"))
            returnTree.addChild(self.compileExpression())
            returnTree.addChild(self.mustBe("symbol", ";"))

        except ParseException:
            raise ParseException()
        return returnTree


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """

        expression = ParseTree("expression", None)
        expression.addChild(self.mustBe("keyword", "skip"))

        return expression 


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

    def classVarTypeCheck(self):
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
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    # tokens.append(Token("keyword","class"))
    # tokens.append(Token("identifier","Main"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("symbol","}"))

    # tokens.append(Token("keyword", "static"))
    # tokens.append(Token("keyword", "int"))
    # tokens.append(Token("identifier", "a"))
    # tokens.append(Token("symbol", ";"))

    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","Main"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("keyword", "static"))
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", ";"))
    # tokens.append(Token("symbol","}"))

    tokens.append(Token("keyword", "function"))
    tokens.append(Token("keyword", "void"))
    tokens.append(Token("identifier", "myFunc"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", ")"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "var"))
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("keyword", "let"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", "="))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("keyword", "if"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ")"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "do"))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    tokens.append(Token("keyword", "else"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "return"))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    tokens.append(Token("keyword", "while"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ")"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "do"))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    tokens.append(Token("keyword", "do"))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("keyword", "return"))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("symbol","}"))

    # tokens.append(Token("keyword","class"))
    # tokens.append(Token("identifier","Main"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("keyword","function"))
    # tokens.append(Token("keyword","void"))
    # tokens.append(Token("identifier","test"))
    # tokens.append(Token("symbol","("))
    # tokens.append(Token("symbol",")"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("symbol","}"))
    # tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        # result = parser.compileSubroutine()
        print(result)
    except ParseException:
        print("Error Parsing!")
