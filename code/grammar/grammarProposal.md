# Grammar Proposal



## Poductions:

```xaml
<!-- program -->
<program> -> <statement_seq> <exp> <optional_semicolon> | <exp> <optional_semicolon>
<statement_seq> -> <statement> | <statement> <statement_seq>
<statement> -> <inline_func_def> ; | <block_func_def> <optional_semicolon> 
    | <type_def> <optional_semicolon>

<optional_semicolon> -> ; | e

<!-- functions -->
<inline_func_def> -> function id ( <id_list> ) => <exp> | function id ( <id_list> ) : id => <exp>
    | function id ( ) => <exp> | function id ( ) : id => <exp>
<block_func_def> -> function id ( <id_list> ) <block_exp> 
    | function id ( <id_list> ) : id <block_exp>
    | function id ( ) <block_exp>
    | function id ( ) : id <block_exp>
<block_exp> -> { <block_items> }
<block_items> -> <exp> ; | <exp> ; <block_items>
    
<exp_list> -> <exp> | <exp> , <exp_list>
<id_list> -> id | id : id | id , <id_list> | id : id , <id_list>


<!-- variable assignment -->
<var_def> -> let <var_def_list> in <exp>
<var_def_list> -> id = <exp> | id : id = <exp> 
    | id = <exp> , <var_def_list> | id : id = <exp> , <var_def_list>
<destr_assignment> -> id := <exp>

  
<!-- expression -->
<exp> -> print ( <exp> ) | <var_def> | <destr_assignment> | <conditional_exp> | <loop_exp> 
  | <type_instance> | <block_exp> | <bool_exp> 


<!-- types -->
<type_def> -> <type_header_def> | type id inherits id <type_body>
  | type id ( <id_list> ) inherits id ( <exp_list> ) <type_body>
<type_header_def> -> type id ( <id_list> ) <type_body> | type id <type_body> 
<type_body> -> { } | { <type_body_items> }
<type_body_items> ->  <type_body_prop> | <type_body_func>
<type_body_prop> -> id = <exp> ; | id : id = <exp> ;
<type_body_func> -> id ( <id_list> ) => <exp> ; | id ( ) => <exp> ; | id ( <id_list> ) <block_exp> ;
    | id ( ) <block_exp> ;
<type_instance> -> new id ( <exp_list> ) | new id ( )


<!-- conditionals -->
<conditionals_exp> -> if ( <bool_exp> ) <exp> else <exp> 
    | if ( <bool_exp> ) <exp> <elif_list> else <exp>
<elif_list> -> elif ( <bool_exp> ) <exp> | elif ( <bool_exp> ) <exp> <elif_list>
  
 
<!-- loops -->
<loop_exp> -> while ( <bool_exp> ) <exp> | for ( id in <range_exp> ) <exp>
<range_exp> -> range ( <num_exp> , <num_exp> )


<!-- boolean -->
<bool_exp> -> <bool_exp> "|" <bool_term> | <bool_term>
<bool_term> -> <bool_term> "&" <bool_factor> | <bool_factor>
<bool_factor> -> "!" <bool_factor> | <bool_cmp> 
<bool_cmp> -> <bool_cmp> "lt" <bool_const> | <bool_cmp> "gt" <bool_const> 
    | <bool_cmp> "get" <bool_const> | <bool_cmp> "let" <bool_const> 
    | <bool_cmp> == <bool_const> | <bool_cmp> != <bool_const> | <bool_const>
<bool_const> -> <str_exp>


<!-- str -->
<str_exp> -> <str_exp> @ <str_const> | <str_exp> @@ <str_const> | <str_const>
<str_const> -> <num_exp>


<!-- num --> 
<num_exp> -> <num_exp> + <term> | <num_exp> - <term> | <term>
<term> -> <term> * <factor> | <term> / <factor> | <term> % <factor> | <factor>
<factor> -> <factor> ^ <const> | <atom>
<atom> -> <atom> as id | <atom> is id | <const>
<const> -> ( <num_exp> ) | num | E | PI | <math_func> | <base_element>


<!-- base_element --> 
<base_element> -> true | false | string | id | <fun_call> | <type_func_call> | <self_call> | <base_call>


<!-- calls -->
<func_call> -> id ( <exp_list> )
<type_func_call> -> id . id ( ) | id . id ( <exp_list> )
<self_call> -> self . id | self . id ( ) | self . id ( <exp_list> )
<base_call> -> base ( ) | base ( <exp_list> )


<!-- math_func -->
<math_func> -> sqrt ( <num_exp> ) | sin ( <num_exp> ) | cos ( <num_exp> ) 
    | exp ( <num_exp> ) | log ( <num_exp> , <num_exp> ) | rand ( ) 

```
