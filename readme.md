points: 6,32/10 

**Implementační dokumentace k 2. úloze do IPP 2021/2022**\
**Jméno a příjmení: Dominik Klon**\
**Login: xklond00**

## Návrh
Původním návrhem bylo vytvořit interpret založený primárně na třídách a správném objektovně
orientovaném postupu. Chtěl jsem vytvořit různé třídy pro instrukce, argumenty a
proměnné. Všechno mělo být prováděno skrz jeden for cyklus, který měl postupně projít
XML, uložit si instrukce, každá instance instrukce měla vykonat svoji funkci a přitom vytvářet
objekty podle třídy pro proměnné a pro argumenty.

## Interní reprezentace
Program je rozdělen na hlavní část pojmenovanou **interpret.py**, ve které se nachází
načtení argumentů z konzole, ověření struktury XML a dále dva cykly.
V prvním cyklu se vytváří instance třídy `Instructions`, které se ukládají do
seznamu `instruction_list`, který slouží pro jejich lepší indexaci, tj. pro funkcionalitu
skoků a návěstí. Dále se v dané smyčce ověřuje, jestli volané instrukce z XML existují
a zdali mají správný počet argumentů. \
Druhý while cyklus je hlavní smyčka programu, která postupně vykonává všechny instrukce,
které program dostal v XML. Index `i` se mění podle toho, zdali byl zavolán nějaký skok či ne. \
Dále řešení obsahuje knihovnu **interpret_library**, ve které jsou soubory
terminal_args.py, interpret_core.py, variable_operations.py a xml_checked.py. \
**Terminal_args.py** slouží k zabalení funkcí pro práci s argumenty, aby nepřekážely v interpret.py. \
Soubor **xml_checked.py** v sobě obsahuje funkce pro kontrolu xml a celkově většinu ošetření
pro chyby s návratovým kódem 31 a 32. \
**Variable_operations.py** slouží pro práci s proměnnými a
symboly. Obsahuje funkce pro hledaní, nastavování a dostávání hodnot z proměnných. Taky obsahuje
funkci `declare` pro jejich deklaraci. Každá práce s proměnnými prochází přes funkci `search`, 
která si zjistí rámec, pokusí se v něm nalézt danou proměnou podle jména a v případě neúspěchu vyvolá
chybu. \
Soubor **interpret_core.py** obsahuje definici třídy `Instruction` a podpůrné funkce. Obsahuje
jádro projektu a nachází se v něm většina funkcionality. V této třídě nalezneme metodu `execute`, 
která v sobě obsahuje všechen kód pro vykonání každé instrukce ze zadání. Z atributu třídy zjistí opcode a 
pomocí jednoho velkého *if-elif-else* bloku vybere aktuálně volanou funkci. Tento blok
je rozdělen podle počtu argumentů pro instrukce. Pro každý argument je vytvořen vlastní slovník, který
obsahuje typ a obsah argumentu.
Tento slovník se pak dále používá pro nastavování hodnot proměnných, nebo k přímému vypsání instrukcí *write*.\
Proměnné jsou reprezentovány seznamem slovníků, který každý obsahuje jméno, typ a hodnotu proměnné. 
S tímto listem pak pracuje dříve zmíněný soubor variable_operations. Pro 3 druhy proměnných existují
3 seznamy (atributy třídy), pro globální `gf_var_list`, pro dočasné `tf_var_list` a všechny dočasné se
stávají lokálními po přesunutí na zásobník (v podobě seznamu) `lf_var_stack`. Program rozlišuje druh proměnných podle prefixu před zavináčem, a tak ho
také mění podle toho, v jakém je proměnná rámci. Důležitým atributem instance třídy je také
proměnná `_numb`, ve které se nachází číslo instrukce. Toto číslo je pak měněno při zavolání instrukce
obsahující skoky. Návěstí jsou uložena v seznamu slovníků, kde každý obsahuje
název a číslo instrukce skoku. Skoky si podle názvu vyhledají číslo návěstí. Toto číslo je pak získáno voláním funkce `get_position_of_next_instruction` ve while
cyklu souboru interpret.py a dynamicky mění pořadí vykonávaných instrukcí. 

## Postup řešení
Jako první jsem začal s kontrolou vstupního XML a argumentů z terminálu. Vytvořil jsem pro ně separátní soubory a vyčlenil je z interpret.py.
Dále jsem napsal třídu `Instructions`, která původně pouze projížděla jednotlivé opcody a vypisovala je. Učil jsem se na ní funkcionalitu OOP a přemýšlel, jak ho
správně zakomponovat do svého řešení. 
Dále jsem vytvořil třídy Argument a Variable, ale nakonec jsem usoudil, že pro jejich funkcionalitu budou stačit pouze slovníky 
(čehož jsem v pozdější fázi litoval). Veškerá funkcionalitu jsem tedy napsal nebo volal z třídy `Instruction`. K jednotlivým podmínka v metodě
`execute` jsem postupně přidával funkcionalitu a k zamezení redundantnosti kódu jsem vytvořil soubor pro práci s proměnnými.
Později se ukázalo, že soubor pokrývá celkovou práci se symboly, ale název `variable_operations` již zůstal.
Stejně jako jsem si v pozdní fázi uvědomil, že slovníky proměnných a funkce z `variable_operations` by šlo zapouzdřit do
jedné třídy. Na změnu implementace již bylo bohužel pozdě. Jako poslední jsem psal různé sémantické kontroly, jako je
použití správného typu u instrukce nebo zamezení duplikace proměnných. Program jsem testoval manuálně, obměnami stejných souborů. Bohužel
jsem si každý z testů neukládal separátně, čehož jsem později taktéž litoval.
