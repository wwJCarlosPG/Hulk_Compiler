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

<!-- variable assignment -->
<var_def> -> let <var_def_list> in <in_options>
<in_options> -> <exp> | <block_exp> | <var_def> | ( <in_options> )
<var_def_list> -> id = <var_assignation> | id = <var_assignation> , <var_def_list>
<var_assignation> -> <exp> | <var_def>
<destr_assignment> -> id := <exp>

  
<!-- expression -->
<exp> -> <num_exp> | <str_exp> | <bool_exp> | print ( <exp> ) | <var_def> | <destr_assignment> 
    | <conditional_exp> | <range_exp> | <loop_exp> | <type_instance> | <block_exp>

<!-- types -->
<type_def> -> <type_header_def> | type id inherits id <type_body> 
  | type id ( <exp_list> ) inherits id ( <exp_list> ) <type_body>
<type_header_def> -> type id ( <exp_list> ) <type_body> | type id <type_body> 
<type_body> -> { <type_body_items> }
<type_body_items> ->  <type_body_props> <type_body_funcs>  
  | <type_body_props> <type_body_funcs> <type_body_items> 
<type_body_props> -> id = <exp> ; | id = <exp> ; <type_body_props> | e
<type_body_funcs> -> id ( <exp_list> ) => <exp> | id ( ) => <exp> | id ( <exp_list> ) <block_exp> 
    | id ( ) <block_exp> | e
<type_instance> -> new id ( <exp_list> )
<type_prop_func_call> -> id . id ( ) | id . id 
    
<!-- boolean and conditions -->
<bool_exp> -> <bool_const> | <exp> == <exp> | <exp> != <exp> | <exp> "lt" <exp> | <exp> "gt" <exp> 
    | <exp> "get" <exp> | <exp> "let" <exp> | <bool_exp> "|" <bool_exp> | <bool_exp> "&" <bool_exp> 
    | ! <bool_exp> 
<bool_const> -> true | false | id | <func_call> | <type_prop_func_call>
 
<conditionals_exp> -> if ( <bool_exp> ) <body_options> else <body_options> 
    | if ( <bool_exp> )  <body_options> <elif_list> else <body_options>
  
<elif_list> -> elif ( <bool_exp> ) <body_options> | elif ( <bool_exp> ) <body_options> <elif_list>
<body_options> -> <exp> | <block_exp> 
  
<!-- loops -->
<loop_exp> -> while ( <bool_exp> ) <body_options> | for ( id in <range_exp> ) <body_options>
<range_exp> -> ( <num_exp> , <num_exp>)
  
<!-- num --> 
<num_exp> -> <num_exp> + <term> | <num_exp> - <term> | <term>
<term> -> <term> * <factor> | <term> / <factor> | <term> % <factor> | <factor>
<factor> -> <factor> ^ <const> | <factor>
<const> -> ( <num_exp> ) | num | E | PI | <math_func> | id | <func_call> | <type_prop_func_call>
<func_call> -> id ( <exp_list> )
  
<math_func> -> sqrt ( <num_exp> ) | sin ( <num_exp> ) | cos ( <num_exp> ) 
    | exp ( <num_exp> ) | log ( <num_exp> , <num_exp> ) | rand ( ) 
  
<!-- str -->
<str_exp> -> string | <str_exp> @ string | <str_exp> @ <const> | id | <func_call> | ( string ) 
  | <type_prop_func_call> | <str_exp> @@ string | <str_exp> @@ <const>
<exp_list> -> <exp> | <exp> , <exp_list> 
    
```
