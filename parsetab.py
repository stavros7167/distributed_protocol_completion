
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ACCEPTING COMMA ENVIRONMENT EQUALS FILE INCLUDE INPUTS INPUT_ENABLED INPUT_STATES LEFT_BRACE LEFT_BRACKET LEFT_PAREN LIVENESS NAME OUTPUTS OUTPUT_STATES PROCESS RECEIVE RIGHT_BRACE RIGHT_BRACKET RIGHT_PAREN SAFETY SEND STATES STRONG_FAIRNESS STRONG_NON_BLOCKINGautomata : include automata\n                | function automata\n                | definition automata\n                | instantiation automata\n                | strong_non_blocking automata\n                | include\n                | function\n                | definition\n                | instantiation\n                | strong_non_blocking\n                | errorinclude : INCLUDE FILEstrong_non_blocking : STRONG_NON_BLOCKING LEFT_BRACKET names RIGHT_BRACKETdefinition : PROCESS NAME inner\n                  | ENVIRONMENT NAME inner\n                  | LIVENESS NAME inner\n                  | SAFETY NAME innerinner : LEFT_BRACE                optional_states                optional_input_states                optional_output_states                inputs                optional_input_enabled                outputs                initial optional_accepting                edges                RIGHT_BRACE\n    inputs : INPUTS LEFT_BRACKET names RIGHT_BRACKEToptional_input_enabled : INPUT_ENABLED LEFT_BRACKET names RIGHT_BRACKEToptional_input_enabled : outputs : OUTPUTS LEFT_BRACKET names RIGHT_BRACKEToptional_states : STATES LEFT_BRACKET names RIGHT_BRACKEToptional_states : optional_input_states : INPUT_STATES LEFT_BRACKET names RIGHT_BRACKEToptional_input_states : optional_output_states : OUTPUT_STATES LEFT_BRACKET names RIGHT_BRACKEToptional_output_states : optional_accepting : ACCEPTING LEFT_BRACKET names RIGHT_BRACKEToptional_accepting : instantiation : NAME EQUALS NAME LEFT_PAREN names RIGHT_PARENfunction : PROCESS NAME LEFT_PAREN names RIGHT_PAREN inner\n                | ENVIRONMENT NAME LEFT_PAREN names RIGHT_PAREN inner\n                | LIVENESS NAME LEFT_PAREN names RIGHT_PAREN inner\n                | SAFETY NAME LEFT_PAREN names RIGHT_PAREN inner\n    names : NAME COMMA namesnames : NAME\n             |initial : NAME NAMEedges : edge edgesedges : edge : NAME NAME SEND NAME\n            | NAME NAME RECEIVE NAMEedge : NAME NAME SEND NAME STRONG_FAIRNESS\n            | NAME NAME RECEIVE NAME STRONG_FAIRNESS'
    
_lr_action_items = {'STRONG_FAIRNESS':([103,104,],[105,106,]),'INPUT_STATES':([27,40,66,],[-24,49,-23,]),'RIGHT_BRACKET':([20,30,31,42,48,52,57,58,67,70,74,75,78,79,83,84,89,94,99,],[-38,-37,43,-38,-38,-36,66,-38,71,-38,-38,80,-38,85,-38,90,95,-38,102,]),'STATES':([27,],[39,]),'LEFT_BRACE':([15,24,25,26,51,54,55,56,],[27,27,27,27,27,27,27,27,]),'FILE':([8,],[21,]),'RIGHT_PAREN':([28,30,33,35,37,41,42,44,45,46,47,52,53,],[-38,-37,-38,-38,-38,51,-38,-38,54,55,56,-36,62,]),'LEFT_PAREN':([15,24,25,26,32,],[28,33,35,37,44,]),'INPUT_ENABLED':([68,85,],[73,-19,]),'COMMA':([30,],[42,]),'$end':([2,3,4,5,6,9,14,16,17,18,19,21,22,29,34,36,38,43,61,62,63,64,65,97,],[-9,-10,0,-6,-7,-8,-11,-4,-5,-1,-2,-12,-3,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'INPUTS':([27,40,50,59,66,71,80,],[-24,-26,-28,69,-23,-25,-27,]),'RECEIVE':([96,],[100,]),'STRONG_NON_BLOCKING':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[7,7,7,7,7,7,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'EQUALS':([10,],[23,]),'RIGHT_BRACE':([81,86,88,92,93,98,102,103,104,105,106,],[-30,-41,-39,97,-41,-40,-29,-43,-42,-45,-44,]),'OUTPUT_STATES':([27,40,50,66,71,],[-24,-26,60,-23,-25,]),'INCLUDE':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[8,8,8,8,8,8,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'ENVIRONMENT':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[1,1,1,1,1,1,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'NAME':([0,1,2,3,5,6,9,11,12,13,20,21,23,28,29,33,34,35,36,37,38,42,43,44,48,58,61,62,63,64,65,70,74,76,78,81,82,83,86,88,91,93,94,95,97,100,101,102,103,104,105,106,],[10,15,10,10,10,10,10,24,25,26,30,-12,32,30,-15,30,-14,30,-16,30,-17,30,-13,30,30,30,-33,-31,-32,-34,-35,30,30,82,30,-30,88,30,91,-39,96,91,30,-22,-18,103,104,-29,-43,-42,-45,-44,]),'PROCESS':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[11,11,11,11,11,11,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'OUTPUTS':([68,72,85,90,],[-21,77,-19,-20,]),'LIVENESS':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[12,12,12,12,12,12,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'SEND':([96,],[101,]),'SAFETY':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[13,13,13,13,13,13,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'error':([0,2,3,5,6,9,21,29,34,36,38,43,61,62,63,64,65,97,],[14,14,14,14,14,14,-12,-15,-14,-16,-17,-13,-33,-31,-32,-34,-35,-18,]),'ACCEPTING':([81,88,],[87,-39,]),'LEFT_BRACKET':([7,39,49,60,69,73,77,87,],[20,48,58,70,74,78,83,94,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,2,3,5,6,9,],[6,6,6,6,6,6,]),'definition':([0,2,3,5,6,9,],[9,9,9,9,9,9,]),'instantiation':([0,2,3,5,6,9,],[2,2,2,2,2,2,]),'initial':([76,],[81,]),'inputs':([59,],[68,]),'outputs':([72,],[76,]),'strong_non_blocking':([0,2,3,5,6,9,],[3,3,3,3,3,3,]),'optional_output_states':([50,],[59,]),'optional_input_enabled':([68,],[72,]),'edges':([86,93,],[92,98,]),'edge':([86,93,],[93,93,]),'optional_accepting':([81,],[86,]),'automata':([0,2,3,5,6,9,],[4,16,17,18,19,22,]),'optional_input_states':([40,],[50,]),'inner':([15,24,25,26,51,54,55,56,],[29,34,36,38,61,63,64,65,]),'optional_states':([27,],[40,]),'include':([0,2,3,5,6,9,],[5,5,5,5,5,5,]),'names':([20,28,33,35,37,42,44,48,58,70,74,78,83,94,],[31,41,45,46,47,52,53,57,67,75,79,84,89,99,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> automata","S'",1,None,None,None),
  ('automata -> include automata','automata',2,'p_automata','parser.py',138),
  ('automata -> function automata','automata',2,'p_automata','parser.py',139),
  ('automata -> definition automata','automata',2,'p_automata','parser.py',140),
  ('automata -> instantiation automata','automata',2,'p_automata','parser.py',141),
  ('automata -> strong_non_blocking automata','automata',2,'p_automata','parser.py',142),
  ('automata -> include','automata',1,'p_automata','parser.py',143),
  ('automata -> function','automata',1,'p_automata','parser.py',144),
  ('automata -> definition','automata',1,'p_automata','parser.py',145),
  ('automata -> instantiation','automata',1,'p_automata','parser.py',146),
  ('automata -> strong_non_blocking','automata',1,'p_automata','parser.py',147),
  ('automata -> error','automata',1,'p_automata','parser.py',148),
  ('include -> INCLUDE FILE','include',2,'p_include','parser.py',153),
  ('strong_non_blocking -> STRONG_NON_BLOCKING LEFT_BRACKET names RIGHT_BRACKET','strong_non_blocking',4,'p_strong_non_blocking','parser.py',173),
  ('definition -> PROCESS NAME inner','definition',3,'p_definition','parser.py',183),
  ('definition -> ENVIRONMENT NAME inner','definition',3,'p_definition','parser.py',184),
  ('definition -> LIVENESS NAME inner','definition',3,'p_definition','parser.py',185),
  ('definition -> SAFETY NAME inner','definition',3,'p_definition','parser.py',186),
  ('inner -> LEFT_BRACE optional_states optional_input_states optional_output_states inputs optional_input_enabled outputs initial optional_accepting edges RIGHT_BRACE','inner',11,'p_inner','parser.py',247),
  ('inputs -> INPUTS LEFT_BRACKET names RIGHT_BRACKET','inputs',4,'p_inputs','parser.py',271),
  ('optional_input_enabled -> INPUT_ENABLED LEFT_BRACKET names RIGHT_BRACKET','optional_input_enabled',4,'p_input_enabled','parser.py',275),
  ('optional_input_enabled -> <empty>','optional_input_enabled',0,'p_input_enabled_empty','parser.py',279),
  ('outputs -> OUTPUTS LEFT_BRACKET names RIGHT_BRACKET','outputs',4,'p_outputs','parser.py',283),
  ('optional_states -> STATES LEFT_BRACKET names RIGHT_BRACKET','optional_states',4,'p_states','parser.py',287),
  ('optional_states -> <empty>','optional_states',0,'p_states_empty','parser.py',291),
  ('optional_input_states -> INPUT_STATES LEFT_BRACKET names RIGHT_BRACKET','optional_input_states',4,'p_input_states','parser.py',295),
  ('optional_input_states -> <empty>','optional_input_states',0,'p_input_states_empty','parser.py',299),
  ('optional_output_states -> OUTPUT_STATES LEFT_BRACKET names RIGHT_BRACKET','optional_output_states',4,'p_output_states','parser.py',303),
  ('optional_output_states -> <empty>','optional_output_states',0,'p_output_states_empty','parser.py',307),
  ('optional_accepting -> ACCEPTING LEFT_BRACKET names RIGHT_BRACKET','optional_accepting',4,'p_accepting','parser.py',311),
  ('optional_accepting -> <empty>','optional_accepting',0,'p_accepting_empty','parser.py',315),
  ('instantiation -> NAME EQUALS NAME LEFT_PAREN names RIGHT_PAREN','instantiation',6,'p_instantiation','parser.py',371),
  ('function -> PROCESS NAME LEFT_PAREN names RIGHT_PAREN inner','function',6,'p_function','parser.py',379),
  ('function -> ENVIRONMENT NAME LEFT_PAREN names RIGHT_PAREN inner','function',6,'p_function','parser.py',380),
  ('function -> LIVENESS NAME LEFT_PAREN names RIGHT_PAREN inner','function',6,'p_function','parser.py',381),
  ('function -> SAFETY NAME LEFT_PAREN names RIGHT_PAREN inner','function',6,'p_function','parser.py',382),
  ('names -> NAME COMMA names','names',3,'p_names_many','parser.py',387),
  ('names -> NAME','names',1,'p_names_single','parser.py',391),
  ('names -> <empty>','names',0,'p_names_single','parser.py',392),
  ('initial -> NAME NAME','initial',2,'p_initial','parser.py',396),
  ('edges -> edge edges','edges',2,'p_edges_many','parser.py',402),
  ('edges -> <empty>','edges',0,'p_edges_empty','parser.py',406),
  ('edge -> NAME NAME SEND NAME','edge',4,'p_edge','parser.py',410),
  ('edge -> NAME NAME RECEIVE NAME','edge',4,'p_edge','parser.py',411),
  ('edge -> NAME NAME SEND NAME STRONG_FAIRNESS','edge',5,'p_edge_with_strong_fairness','parser.py',415),
  ('edge -> NAME NAME RECEIVE NAME STRONG_FAIRNESS','edge',5,'p_edge_with_strong_fairness','parser.py',416),
]