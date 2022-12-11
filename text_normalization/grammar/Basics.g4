lexer grammar Basics;

IBAN : COUNTRY_CODE (WHITE_SPACE|DASH|SLASH)? BANK_CODE (WHITE_SPACE|DASH|SLASH)? BBAN ;
COUNTRY_CODE : (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL) (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL) (WHITE_SPACE|DASH|SLASH)? DIGIT DIGIT;
BANK_CODE : (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL|DIGIT) (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL|DIGIT) (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL|DIGIT) (EN_ALPHA_CAPITAL|EN_ALPHA_SMALL|DIGIT) ;
BBAN : (DIGIT DIGIT DIGIT DIGIT (WHITE_SPACE|DASH|SLASH)?)+ DIGIT DIGIT? DIGIT? DIGIT? ;

ACC_NUMBER : DIGIT DIGIT DIGIT DIGIT (DASH|SLASH) DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT (DASH|SLASH) DIGIT DIGIT DIGIT (DASH|SLASH) DIGIT DIGIT DIGIT DIGIT (DASH|SLASH) DIGIT DIGIT DIGIT ;


PHONE : (('('?
                (PLUS_SIGN|'00')?
                DIGIT DIGIT DIGIT
           ')'?
           (WHITE_SPACE|DASH)?
           ('('? '0'? ')'?)? WHITE_SPACE? DIGIT)
	    |('('? '0' DIGIT ')'?))
	    (WHITE_SPACE|DASH)?
	    DIGIT DIGIT (DIGIT WHITE_SPACE?|DIGIT DIGIT WHITE_SPACE?) DIGIT DIGIT DIGIT DIGIT (WHITE_SPACE|PUNCTUACTION|NEWLINE);

EMAIL : EN_ALPHA_NUMERICS '@' EN_ALPHA_NUMERICS PERIOD EN_ALPHA_NUMERICS;

AR_ABBREV :(AR_ALPHA_NUMERIC '.' WHITE_SPACE?)+ (WHITE_SPACE | PERIOD | NEWLINE)  ;

AR_ALPHA_NUMERICS : AR_ALPHA_NUMERIC+;

AR_ALPHA_NUMERIC : [\u0621-\u065f]; //[\p{InARABIC}] includes question mark which introduces errors check #63

SEPARATOR : '\t'
          | '\\'
          | '/'
          ;

WHITE_LISTED_MARK :  '!' |
         '؟' |
         '?' |
         '(' |
         ')' |
         '{' |
         '}' |
         '<' |
         '>' |
         '[' |
         ']' |
         '"' |
         '\''|
         '؛' |
         ',' |
         '،' |
         ':' |
         ';' |
         '`' |
         '‘' |
         '~' |
         '|' |
         '’' ;

EN_ABBREV :((EN_ALPHA_CAPITAL '.'? WHITE_SPACE?)+ | (WHITE_SPACE (EN_ALPHA_SMALL '.'  WHITE_SPACE?)+))(WHITE_SPACE | PERIOD | NEWLINE)  ;

EN_ALPHA_NUMERICS : (EN_ALPHA_CAPITAL+ EN_ALPHA_SMALL+)
          |EN_ALPHA_SMALL+;

EN_ALPHA_SMALL : [a-z] ;
EN_ALPHA_CAPITAL : [A-Z] ;
DIGIT : [0-9] | [\u0660-\u0669] ;
DIGITS: DIGIT+ ;
PERIOD : '.' ;
PUNCTUACTION : '!' |
         '؟' |
         '?' |
         '(' |
         ')' |
         '{' |
         '}' |
         '<' |
         '>' |
         '[' |
         ']' |
         '"' |
         '\''|
         '؛' |
         ',' |
         '،' |
         ';' |
         '`' |
         '‘' |
         '~' |
         '|' |
         '’' |
         PERIOD ;
DASH : '-'|'–' ;
SLASH : '/' ;
PLUS_SIGN : '+' ;
WHITE_SPACE : (' ' | '\t')+  ;
NEWLINE : '\n' ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines