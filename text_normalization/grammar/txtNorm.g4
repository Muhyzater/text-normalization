grammar txtNorm;
import Basics, Date, Units;

text      : paragraph+ EOF ;

paragraph : entity+ (NEWLINE | EOF)  ;

entity    : WHITE_SPACE
          | date
          | time
          | currency
          | measurement
          | number
          | floating_num
          | phone
          | ar_acronym
          | en_acronym
          | word
          | symbol
          | iban
          | account
          | email
          | sequence_of_digits;

iban : IBAN;

account : ACC_NUMBER ;

phone : PHONE ;

email : EMAIL ;

date : DATE_BULK ;

time : TIME_BULK ;

currency :  CURRENCY_BULK ;

measurement : MEASUREMENT_BULK ;

sequence_of_digits :  SEQUENCE_OF_DIGITS;


ar_acronym : AR_ABBREV ;

en_acronym : EN_ABBREV ;

word :  WHITE_SPACE? (EN_ALPHA_NUMERICS | AR_ALPHA_NUMERICS | WHITE_LISTED_MARK | SEPARATOR | PERIOD | PUNCTUACTION |WHITE_SPACE| MEASUREMENT_UNIT | DASH | SLASH)+ ;

symbol : CURRENCY_UNIT
       | TIME_UNIT
       //| MEASUREMENT_UNIT
       | SYMBOL ;

number : NUMBER_BULK ;

floating_num : FLOATING_NUMBER_BULK ;

CURRENCY_BULK : ((CURRENCY_UNIT WHITE_SPACE? (NUMBER_BULK|FLOATING_NUMBER_BULK))
         | ((NUMBER_BULK|FLOATING_NUMBER_BULK) WHITE_SPACE? CURRENCY_UNIT))  ;

MEASUREMENT_BULK : (NUMBER_BULK|FLOATING_NUMBER_BULK) WHITE_SPACE? MEASUREMENT_UNIT (WHITE_SPACE | PUNCTUACTION | NEWLINE ); // (WHITE_SPACE | PERIOD | EOF | NEWLINE);

DATE_BULK : (DIGIT DIGIT? (DASH|'/')
        (DIGIT DIGIT? ((DASH|'/') DIGITS
            (WHITE_SPACE? ('\u0647\u0640'|'\u0647'|'\u0645')?)?)?)?)
	|((DIGIT DIGIT? WHITE_SPACE (AR_ALPHA_NUMERIC+ WHITE_SPACE)?)?
	    MONTH_NAME (WHITE_SPACE AR_ALPHA_NUMERIC+)?
	    (WHITE_SPACE DIGIT DIGIT? DIGIT? DIGIT? (WHITE_SPACE? ('\u0647\u0640'|'\u0647'|'\u0645')?)?)?)
	|(DIGIT DIGIT? DIGIT? DIGIT? WHITE_SPACE? ('\u0647\u0640'|'\u0647'|'\u0645') (WHITE_SPACE | PUNCTUACTION | NEWLINE ));

//(' ' | '\t' | PERIOD | EOF | NEWLINE) ;

TIME_BULK : NUMBER_BULK ':' NUMBER_BULK (':' NUMBER_BULK)? WHITE_SPACE? ((TIME_UNIT (WHITE_SPACE | PUNCTUACTION | NEWLINE )) |
                                                                                                    ('\u0635\u0628\u0627\u062D\u0627' '\u064B'?) | //ﺺﺑﺎﺣﺍً or ﺺﺑﺎﺣﺍ
                                                                                                    ('\u0645\u0633\u0627\u0621' '\u064B'?) //مساءً or مساء
                                                                                                    )? ;

FLOATING_NUMBER_BULK : (DASH|PLUS_SIGN)?  (DIGITS ((','|PERIOD) (DIGITS|DIGIT))+) ;

NUMBER_BULK : (DASH|PLUS_SIGN)? DIGITS ;

NEWLINE            : ('\r'? '\n' | '\r')+ ;
SEQUENCE_OF_DIGITS : (DIGITS (SLASH|DASH))+ DIGITS  ;