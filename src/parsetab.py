
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ABS AND ANDBIT ARRAY CADENA CHAR CHAR_ CORDER CORIZQ DIFERENTE DIV DOLAR DOSPUNTOS EXIT FLOAT GOTO ID IF IGUAL IGUALQUE INT LABEL LLAVEDER LLAVEIZQ MAIN MAS MAYORIGUAL MAYORQUE MENORIGUAL MENORQUE MENOS MODULO NOTBIT NOTLOGICA NUMERAL NUMERO OR ORBIT PARDER PARIZQ POR PRINT PUNTOCOMA READ SHIFTDER SHIFTIZQ UNSET XOR XORBITS : AA : MAIN DOSPUNTOS SENTENCIASSENTENCIAS   : SENTENCIAS SENTENCIASENTENCIAS     : SENTENCIASENTENCIA    : ETIQUETASENTENCIA    :  INSTRUCCIONESSENTENCIA    :  DECLARACIONESETIQUETA   : LABEL error DOSPUNTOSETIQUETA   : LABEL DOSPUNTOSINSTRUCCIONES    : PRINT PARIZQ error PARDER PUNTOCOMA\n                        | IF PARIZQ error PARDER GOTO LABEL PUNTOCOMA\n                        | UNSET PARIZQ error PARDER PUNTOCOMA\n                        | EXIT error PUNTOCOMA\n                        | GOTO error  PUNTOCOMAINSTRUCCIONES    : PRINT PARIZQ EXPRESION PARDER PUNTOCOMA\n                        | IF PARIZQ EXPRESION PARDER GOTO LABEL PUNTOCOMA\n                        | UNSET PARIZQ ID PARDER PUNTOCOMA\n                        | EXIT PUNTOCOMA\n                        | GOTO LABEL PUNTOCOMADECLARACIONES  : ID ARRAY_ARRAY_    :  error IGUAL EXPRESION PUNTOCOMAARRAY_    :  CORCHETES IGUAL error PUNTOCOMA\n                | IGUAL error PUNTOCOMAARRAY_    :  CORCHETES IGUAL EXPRESION PUNTOCOMA\n                | IGUAL EXPRESION PUNTOCOMACORCHETES : CORCHETES CORCHETECORCHETES : CORCHETECORCHETE : CORIZQ F CORDEREXPRESION    :  ATOMICOEXPRESION    :  FUNCIONEXPRESION    :  OPERACIONOPERACION    : F error F\n                    | MENOS error\n                    | NOTLOGICA error\n                    | NOTBIT error\n                    | ANDBIT errorOPERACION    : F OPERADOR F\n                    | MENOS F\n                    | NOTLOGICA F\n                    | NOTBIT F\n                    | ANDBIT FATOMICO     : FFUNCION      : ABS PARIZQ EXPRESION PARDER\n                    | READ PARIZQ PARDER\n                    | PARIZQ TIPO PARDER ID\n                    | ARRAY PARIZQ PARDEROPERADOR     :   MAS\n                        | MENOS\n                        | DIV\n                        | POR\n                        | MODULO\n                        | AND\n                        | OR\n                        | XOR\n                        | IGUALQUE\n                        | DIFERENTE\n                        | MAYORIGUAL\n                        | MENORIGUAL\n                        | MAYORQUE\n                        | MENORQUE\n                        | ANDBIT\n                        | ORBIT\n                        | XORBIT\n                        | SHIFTIZQ\n                        | SHIFTDER TIPO    : INT\n                | FLOAT\n                | CHARF  : NUMEROF  : IDF  : ID CORCHETESF  : CADENAF  : CHAR_'
    
_lr_action_items = {'MAIN':([0,],[3,]),'$end':([1,2,5,6,7,8,9,17,19,26,27,33,54,55,58,109,110,115,116,124,125,126,127,128,133,134,],[0,-1,-2,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'DOSPUNTOS':([3,10,18,],[4,19,33,]),'LABEL':([4,5,6,7,8,9,13,17,19,26,27,33,54,55,58,109,110,115,116,122,123,124,125,126,127,128,133,134,],[10,10,-4,-5,-6,-7,23,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,131,132,-12,-17,-21,-22,-24,-11,-16,]),'PRINT':([4,5,6,7,8,9,17,19,26,27,33,54,55,58,109,110,115,116,124,125,126,127,128,133,134,],[11,11,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'IF':([4,5,6,7,8,9,17,19,26,27,33,54,55,58,109,110,115,116,124,125,126,127,128,133,134,],[12,12,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'UNSET':([4,5,6,7,8,9,17,19,26,27,33,54,55,58,109,110,115,116,124,125,126,127,128,133,134,],[14,14,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'EXIT':([4,5,6,7,8,9,17,19,26,27,33,54,55,58,109,110,115,116,124,125,126,127,128,133,134,],[15,15,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'GOTO':([4,5,6,7,8,9,17,19,26,27,33,54,55,58,104,105,109,110,115,116,124,125,126,127,128,133,134,],[13,13,-4,-5,-6,-7,-3,-9,-18,-20,-8,-14,-19,-13,122,123,-23,-25,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'ID':([4,5,6,7,8,9,17,19,20,21,24,26,27,29,32,33,45,46,47,48,54,55,58,59,62,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,109,110,114,115,116,124,125,126,127,128,133,134,],[16,16,-4,-5,-6,-7,-3,-9,43,43,57,-18,-20,43,43,-8,43,43,43,43,-14,-19,-13,43,43,43,43,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,43,-23,-25,129,-10,-15,-12,-17,-21,-22,-24,-11,-16,]),'error':([10,13,15,16,20,21,24,29,31,40,43,45,46,47,48,49,50,51,62,63,94,113,],[18,22,25,28,35,52,56,60,-27,71,-70,96,98,100,102,-69,-72,-73,111,-26,-71,-28,]),'PARIZQ':([11,12,14,20,21,29,41,42,44,59,62,92,],[20,21,24,34,34,34,92,93,95,34,34,34,]),'PUNTOCOMA':([15,22,23,25,31,37,38,39,40,43,49,50,51,60,61,63,69,70,94,96,97,98,99,100,101,102,103,106,107,108,111,112,113,117,118,120,121,129,130,131,132,],[26,54,55,58,-27,-29,-30,-31,-42,-70,-69,-72,-73,109,110,-26,115,116,-71,-33,-38,-34,-39,-35,-40,-36,-41,124,125,126,127,128,-28,-32,-37,-44,-46,-45,-43,133,134,]),'IGUAL':([16,28,30,31,63,113,],[29,59,62,-27,-26,-28,]),'CORIZQ':([16,30,31,43,63,94,113,],[32,32,-27,32,-26,32,-28,]),'ABS':([20,21,29,59,62,92,],[41,41,41,41,41,41,]),'READ':([20,21,29,59,62,92,],[42,42,42,42,42,42,]),'ARRAY':([20,21,29,59,62,92,],[44,44,44,44,44,44,]),'MENOS':([20,21,29,31,40,43,49,50,51,59,62,63,92,94,113,],[45,45,45,-27,74,-70,-69,-72,-73,45,45,-26,45,-71,-28,]),'NOTLOGICA':([20,21,29,59,62,92,],[46,46,46,46,46,46,]),'NOTBIT':([20,21,29,59,62,92,],[47,47,47,47,47,47,]),'ANDBIT':([20,21,29,31,40,43,49,50,51,59,62,63,92,94,113,],[48,48,48,-27,87,-70,-69,-72,-73,48,48,-26,48,-71,-28,]),'NUMERO':([20,21,29,32,45,46,47,48,59,62,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,],[49,49,49,49,49,49,49,49,49,49,49,49,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,49,]),'CADENA':([20,21,29,32,45,46,47,48,59,62,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,],[50,50,50,50,50,50,50,50,50,50,50,50,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,50,]),'CHAR_':([20,21,29,32,45,46,47,48,59,62,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,],[51,51,51,51,51,51,51,51,51,51,51,51,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,51,]),'MAS':([31,40,43,49,50,51,63,94,113,],[-27,73,-70,-69,-72,-73,-26,-71,-28,]),'DIV':([31,40,43,49,50,51,63,94,113,],[-27,75,-70,-69,-72,-73,-26,-71,-28,]),'POR':([31,40,43,49,50,51,63,94,113,],[-27,76,-70,-69,-72,-73,-26,-71,-28,]),'MODULO':([31,40,43,49,50,51,63,94,113,],[-27,77,-70,-69,-72,-73,-26,-71,-28,]),'AND':([31,40,43,49,50,51,63,94,113,],[-27,78,-70,-69,-72,-73,-26,-71,-28,]),'OR':([31,40,43,49,50,51,63,94,113,],[-27,79,-70,-69,-72,-73,-26,-71,-28,]),'XOR':([31,40,43,49,50,51,63,94,113,],[-27,80,-70,-69,-72,-73,-26,-71,-28,]),'IGUALQUE':([31,40,43,49,50,51,63,94,113,],[-27,81,-70,-69,-72,-73,-26,-71,-28,]),'DIFERENTE':([31,40,43,49,50,51,63,94,113,],[-27,82,-70,-69,-72,-73,-26,-71,-28,]),'MAYORIGUAL':([31,40,43,49,50,51,63,94,113,],[-27,83,-70,-69,-72,-73,-26,-71,-28,]),'MENORIGUAL':([31,40,43,49,50,51,63,94,113,],[-27,84,-70,-69,-72,-73,-26,-71,-28,]),'MAYORQUE':([31,40,43,49,50,51,63,94,113,],[-27,85,-70,-69,-72,-73,-26,-71,-28,]),'MENORQUE':([31,40,43,49,50,51,63,94,113,],[-27,86,-70,-69,-72,-73,-26,-71,-28,]),'ORBIT':([31,40,43,49,50,51,63,94,113,],[-27,88,-70,-69,-72,-73,-26,-71,-28,]),'XORBIT':([31,40,43,49,50,51,63,94,113,],[-27,89,-70,-69,-72,-73,-26,-71,-28,]),'SHIFTIZQ':([31,40,43,49,50,51,63,94,113,],[-27,90,-70,-69,-72,-73,-26,-71,-28,]),'SHIFTDER':([31,40,43,49,50,51,63,94,113,],[-27,91,-70,-69,-72,-73,-26,-71,-28,]),'PARDER':([31,35,36,37,38,39,40,43,49,50,51,52,53,56,57,63,65,66,67,68,93,94,95,96,97,98,99,100,101,102,103,113,117,118,119,120,121,129,130,],[-27,69,70,-29,-30,-31,-42,-70,-69,-72,-73,104,105,106,107,-26,114,-66,-67,-68,120,-71,121,-33,-38,-34,-39,-35,-40,-36,-41,-28,-32,-37,130,-44,-46,-45,-43,]),'CORDER':([31,43,49,50,51,63,64,94,113,],[-27,-70,-69,-72,-73,-26,113,-71,-28,]),'INT':([34,],[66,]),'FLOAT':([34,],[67,]),'CHAR':([34,],[68,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'S':([0,],[1,]),'A':([0,],[2,]),'SENTENCIAS':([4,],[5,]),'SENTENCIA':([4,5,],[6,17,]),'ETIQUETA':([4,5,],[7,7,]),'INSTRUCCIONES':([4,5,],[8,8,]),'DECLARACIONES':([4,5,],[9,9,]),'ARRAY_':([16,],[27,]),'CORCHETES':([16,43,],[30,94,]),'CORCHETE':([16,30,43,94,],[31,63,31,63,]),'EXPRESION':([20,21,29,59,62,92,],[36,53,61,108,112,119,]),'ATOMICO':([20,21,29,59,62,92,],[37,37,37,37,37,37,]),'FUNCION':([20,21,29,59,62,92,],[38,38,38,38,38,38,]),'OPERACION':([20,21,29,59,62,92,],[39,39,39,39,39,39,]),'F':([20,21,29,32,45,46,47,48,59,62,71,72,92,],[40,40,40,64,97,99,101,103,40,40,117,118,40,]),'TIPO':([34,],[65,]),'OPERADOR':([40,],[72,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> S","S'",1,None,None,None),
  ('S -> A','S',1,'p_init','grammar.py',193),
  ('A -> MAIN DOSPUNTOS SENTENCIAS','A',3,'p_main','grammar.py',219),
  ('SENTENCIAS -> SENTENCIAS SENTENCIA','SENTENCIAS',2,'p_sentencias_lista','grammar.py',240),
  ('SENTENCIAS -> SENTENCIA','SENTENCIAS',1,'p_sentecias_sentencia','grammar.py',260),
  ('SENTENCIA -> ETIQUETA','SENTENCIA',1,'p_sentencia_eti','grammar.py',278),
  ('SENTENCIA -> INSTRUCCIONES','SENTENCIA',1,'p_sentencia_instr','grammar.py',295),
  ('SENTENCIA -> DECLARACIONES','SENTENCIA',1,'p_sentencia_decla','grammar.py',310),
  ('ETIQUETA -> LABEL error DOSPUNTOS','ETIQUETA',3,'p_etiqueta_error','grammar.py',325),
  ('ETIQUETA -> LABEL DOSPUNTOS','ETIQUETA',2,'p_etiqueta','grammar.py',328),
  ('INSTRUCCIONES -> PRINT PARIZQ error PARDER PUNTOCOMA','INSTRUCCIONES',5,'p_instrucciones_error','grammar.py',343),
  ('INSTRUCCIONES -> IF PARIZQ error PARDER GOTO LABEL PUNTOCOMA','INSTRUCCIONES',7,'p_instrucciones_error','grammar.py',344),
  ('INSTRUCCIONES -> UNSET PARIZQ error PARDER PUNTOCOMA','INSTRUCCIONES',5,'p_instrucciones_error','grammar.py',345),
  ('INSTRUCCIONES -> EXIT error PUNTOCOMA','INSTRUCCIONES',3,'p_instrucciones_error','grammar.py',346),
  ('INSTRUCCIONES -> GOTO error PUNTOCOMA','INSTRUCCIONES',3,'p_instrucciones_error','grammar.py',347),
  ('INSTRUCCIONES -> PRINT PARIZQ EXPRESION PARDER PUNTOCOMA','INSTRUCCIONES',5,'p_instrucciones','grammar.py',350),
  ('INSTRUCCIONES -> IF PARIZQ EXPRESION PARDER GOTO LABEL PUNTOCOMA','INSTRUCCIONES',7,'p_instrucciones','grammar.py',351),
  ('INSTRUCCIONES -> UNSET PARIZQ ID PARDER PUNTOCOMA','INSTRUCCIONES',5,'p_instrucciones','grammar.py',352),
  ('INSTRUCCIONES -> EXIT PUNTOCOMA','INSTRUCCIONES',2,'p_instrucciones','grammar.py',353),
  ('INSTRUCCIONES -> GOTO LABEL PUNTOCOMA','INSTRUCCIONES',3,'p_instrucciones','grammar.py',354),
  ('DECLARACIONES -> ID ARRAY_','DECLARACIONES',2,'p_declaraciones','grammar.py',442),
  ('ARRAY_ -> error IGUAL EXPRESION PUNTOCOMA','ARRAY_',4,'p_array1_error','grammar.py',464),
  ('ARRAY_ -> CORCHETES IGUAL error PUNTOCOMA','ARRAY_',4,'p_array_error','grammar.py',467),
  ('ARRAY_ -> IGUAL error PUNTOCOMA','ARRAY_',3,'p_array_error','grammar.py',468),
  ('ARRAY_ -> CORCHETES IGUAL EXPRESION PUNTOCOMA','ARRAY_',4,'p_array','grammar.py',471),
  ('ARRAY_ -> IGUAL EXPRESION PUNTOCOMA','ARRAY_',3,'p_array','grammar.py',472),
  ('CORCHETES -> CORCHETES CORCHETE','CORCHETES',2,'p_corchete_lista','grammar.py',517),
  ('CORCHETES -> CORCHETE','CORCHETES',1,'p_corchetes_corchete','grammar.py',543),
  ('CORCHETE -> CORIZQ F CORDER','CORCHETE',3,'p_corchete','grammar.py',566),
  ('EXPRESION -> ATOMICO','EXPRESION',1,'p_expresion_ato','grammar.py',585),
  ('EXPRESION -> FUNCION','EXPRESION',1,'p_expresion_fun','grammar.py',598),
  ('EXPRESION -> OPERACION','EXPRESION',1,'p_expresion_ope','grammar.py',613),
  ('OPERACION -> F error F','OPERACION',3,'p_operacion_error','grammar.py',628),
  ('OPERACION -> MENOS error','OPERACION',2,'p_operacion_error','grammar.py',629),
  ('OPERACION -> NOTLOGICA error','OPERACION',2,'p_operacion_error','grammar.py',630),
  ('OPERACION -> NOTBIT error','OPERACION',2,'p_operacion_error','grammar.py',631),
  ('OPERACION -> ANDBIT error','OPERACION',2,'p_operacion_error','grammar.py',632),
  ('OPERACION -> F OPERADOR F','OPERACION',3,'p_operacion','grammar.py',635),
  ('OPERACION -> MENOS F','OPERACION',2,'p_operacion','grammar.py',636),
  ('OPERACION -> NOTLOGICA F','OPERACION',2,'p_operacion','grammar.py',637),
  ('OPERACION -> NOTBIT F','OPERACION',2,'p_operacion','grammar.py',638),
  ('OPERACION -> ANDBIT F','OPERACION',2,'p_operacion','grammar.py',639),
  ('ATOMICO -> F','ATOMICO',1,'p_numero','grammar.py',738),
  ('FUNCION -> ABS PARIZQ EXPRESION PARDER','FUNCION',4,'p_funcion','grammar.py',753),
  ('FUNCION -> READ PARIZQ PARDER','FUNCION',3,'p_funcion','grammar.py',754),
  ('FUNCION -> PARIZQ TIPO PARDER ID','FUNCION',4,'p_funcion','grammar.py',755),
  ('FUNCION -> ARRAY PARIZQ PARDER','FUNCION',3,'p_funcion','grammar.py',756),
  ('OPERADOR -> MAS','OPERADOR',1,'p_operador','grammar.py',828),
  ('OPERADOR -> MENOS','OPERADOR',1,'p_operador','grammar.py',829),
  ('OPERADOR -> DIV','OPERADOR',1,'p_operador','grammar.py',830),
  ('OPERADOR -> POR','OPERADOR',1,'p_operador','grammar.py',831),
  ('OPERADOR -> MODULO','OPERADOR',1,'p_operador','grammar.py',832),
  ('OPERADOR -> AND','OPERADOR',1,'p_operador','grammar.py',833),
  ('OPERADOR -> OR','OPERADOR',1,'p_operador','grammar.py',834),
  ('OPERADOR -> XOR','OPERADOR',1,'p_operador','grammar.py',835),
  ('OPERADOR -> IGUALQUE','OPERADOR',1,'p_operador','grammar.py',836),
  ('OPERADOR -> DIFERENTE','OPERADOR',1,'p_operador','grammar.py',837),
  ('OPERADOR -> MAYORIGUAL','OPERADOR',1,'p_operador','grammar.py',838),
  ('OPERADOR -> MENORIGUAL','OPERADOR',1,'p_operador','grammar.py',839),
  ('OPERADOR -> MAYORQUE','OPERADOR',1,'p_operador','grammar.py',840),
  ('OPERADOR -> MENORQUE','OPERADOR',1,'p_operador','grammar.py',841),
  ('OPERADOR -> ANDBIT','OPERADOR',1,'p_operador','grammar.py',842),
  ('OPERADOR -> ORBIT','OPERADOR',1,'p_operador','grammar.py',843),
  ('OPERADOR -> XORBIT','OPERADOR',1,'p_operador','grammar.py',844),
  ('OPERADOR -> SHIFTIZQ','OPERADOR',1,'p_operador','grammar.py',845),
  ('OPERADOR -> SHIFTDER','OPERADOR',1,'p_operador','grammar.py',846),
  ('TIPO -> INT','TIPO',1,'p_tipo','grammar.py',878),
  ('TIPO -> FLOAT','TIPO',1,'p_tipo','grammar.py',879),
  ('TIPO -> CHAR','TIPO',1,'p_tipo','grammar.py',880),
  ('F -> NUMERO','F',1,'p_f_numero','grammar.py',892),
  ('F -> ID','F',1,'p_f_id','grammar.py',904),
  ('F -> ID CORCHETES','F',2,'p_f_idARRAY','grammar.py',916),
  ('F -> CADENA','F',1,'p_f_cadena','grammar.py',934),
  ('F -> CHAR_','F',1,'p_f_char','grammar.py',946),
]
