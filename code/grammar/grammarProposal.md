# Grammar Proposal



## Poductions:

```xaml
<program> -> <statement_seq> <exp> | <exp>

<statement_seq> -> <statement> | <statement> <statement_seq>
<statement> -> <inline_func_def> | <block_func_def> | <type_def>

<!-- functions -->
<inline_func_def> -> function id ( <exp_list> ) => <exp> ; | function id ( ) => <exp> ;
<block_func_def> -> function id ( <exp_list> ) <block_exp> | function id ( ) <block_exp>
<block_exp> -> { <block_items> }
<block_items> -> <exp> ; | <exp> ; <block_items>
<exp_list> -> <exp> | <exp> , <exp_list>
    
<func_call> -> id ( <exp_list> )
    

<!-- variable assignment -->
<var_def> -> let <var_def_list> in <exp>
<var_def_list> -> id = <exp> | id = <exp> , <var_def_list>
<destr_assignment> -> id := <exp>

  
<!-- expression -->
<exp> -> <num_exp> | <str_exp> | <bool_exp> | print ( <exp> ) | <var_def> | <destr_assignment> 
    | <conditional_exp> | <range_exp> | <loop_exp> | <type_instance> | <block_exp> | ( <exp> )

<!-- types -->
<type_def> -> <type_header_def> | type id inherits id <type_body> 
  | type id ( <exp_list> ) inherits id ( <exp_list> ) <type_body>
<type_header_def> -> type id ( <exp_list> ) <type_body> | type id <type_body> 
<type_body> -> { <type_body_items> }
<type_body_items> ->  <type_body_prop> <type_body_func>  
  | <type_body_prop> <type_body_func> <type_body_items> 
<type_body_prop> -> id = <exp> ; | e
<type_body_func> -> id ( <exp_list> ) => <exp> | id ( ) => <exp> | id ( <exp_list> ) <block_exp> 
    | id ( ) <block_exp> | e
<type_instance> -> new id ( <exp_list> ) | new id ( )
<type_prop_func_call> -> id . id ( ) | id . id ( <exp_list> ) | id . id 
    
<!-- boolean and conditions -->
<bool_exp> -> <bool_const> | <exp> == <exp> | <exp> != <exp> | <exp> "lt" <exp> | <exp> "gt" <exp> 
    | <exp> "get" <exp> | <exp> "let" <exp> | <bool_exp> "|" <bool_exp> | <bool_exp> "&" <bool_exp> 
    | ! <bool_exp> 
<bool_const> -> true | false | id | <func_call> | <type_prop_func_call>
 
<conditionals_exp> -> if ( <bool_exp> ) <exp> else <exp> 
    | if ( <bool_exp> ) <exp> <elif_list> else <exp>
  
<elif_list> -> elif ( <bool_exp> ) <exp> | elif ( <bool_exp> ) <exp> <elif_list>
  
<!-- loops -->
<loop_exp> -> while ( <bool_exp> ) <exp> | for ( id in <range_exp> ) <exp>
<range_exp> -> range ( <num_exp> , <num_exp>)
  
<!-- num --> 
<num_exp> -> <num_exp> + <term> | <num_exp> - <term> | <term>
<term> -> <term> * <factor> | <term> / <factor> | <term> % <factor> | <factor>
<factor> -> <factor> ^ <const> | <const>
<const> -> ( <num_exp> ) | num | E | PI | <math_func> | id | <func_call> | <type_prop_func_call>

  
<math_func> -> sqrt ( <num_exp> ) | sin ( <num_exp> ) | cos ( <num_exp> ) 
    | exp ( <num_exp> ) | log ( <num_exp> , <num_exp> ) | rand ( ) 
  
<!-- str -->
<str_exp> -> string | <str_exp> @ string | <str_exp> @ <term> | id | <func_call>
  | <type_prop_func_call> | <str_exp> @@ string | <str_exp> @@ <term>


```
