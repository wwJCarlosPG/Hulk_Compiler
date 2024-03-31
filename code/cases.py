
def get_cases(case_number=None):
    """
    Returns a list of test programs or a specific program based on the case number.

    Args:
        case_number (int, optional): The desired test case number. Must be an integer value.
            If not provided, returns all test cases.

    Returns:
        list or str: A list of test programs if `case_number` is None,
            or a specific program based on the case number.

    Raises:
        Exception: If `case_number` is a negative number or greater than or equal to the number of available cases.
            Indicates that the provided case number is invalid.
    """
    all_cases = [program0, program1, program2, program3, program4,
                program5, program6, program7, program8, program9,
                program10, program11, program12, program13, program14]
    
    if case_number is None:
        return all_cases
    else:
        if case_number >= len(all_cases) or case_number < 0:
            raise Exception("Invalid case number")
        return [all_cases[case_number]]


program0 = '''
type Animal([name]){
    name = name;
    sound() => "Make Sound";
}
type Dog(name,color) inherits Animal(name, apsasp){
    name = name;
}
type Cat(name, skin) {
    name = name;
    skin = skin;
};
if (x == 0)print("4") elif(x<5) {print(64);} else{4;}
'''
program1 = '''
while(x<=4){
    print(x); 
    x:="6";}
'''
program2 = '''
type Point(x, y) {
    x_prop = x;
    y_prop = y;
};
function AbsoluteMove(x, steps) => x + steps;
print("OK")
'''
program3 = '''
type Animal(name){
    name = name;
    sound() => "Make Sound";
}
type Dog(name,color) inherits Animal(name, apsasp){
    name = name;
}
type Cat(name, skin) {
    name = name;
    skin = skin;
};
print("OK")
'''

program4 = '''
    let a  = 10 in while (b<=0){   
        print(a);
        a:=a-1;
    
    }
'''

program5 = '''
    function gcd(a, b) {
        while (a > 0){
            let m = a % b in {
                b := a;
                a := m;
            };
        };
    }
    for (x in range(gcd(6,2), 10)) print(x)
'''
program6 = '''
    function fib(n: number) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
    4
'''
program7 = '''
    function A() => let x=5 in {print(5);};
    print(5)
'''
program8 ='''
    function A(){
        let x=5 in print(5);
    }
    print(5);
'''

program9 = '''
type Animal(name) inherits Firulai(name){
    name = name;
    sound() => "Make Sound";
}
type Dog(name) inherits Animal(name){
    name = name;
}
type Firulai(name) inherits Dog(name) {
    name = name;
    skin = skin;
};
print("CYCLEEE")
'''
program10 ='''
    type Animal(name){
        name = name;
        sound() => "Make Sound";
    }
    type Dog(name) inherits Animal(name){
        name = name;
    }
    function A(a: number, b: number): number{
        let x: Dog = new Dog("Pep") in {
            let y = x as Animal in 2;
        };
    }
    print(5);
'''
program11 = '''
    type Bird {
    }

    type Plane {
    }

    type Bird {
    }

    let x = new Superman() in
        print(
            if (x is Bird) "It's bird!"
            elif (x is Plane) "It's a plane!"
            else "No, it's Superman!"
        );
'''
program12 = '''
    type Point(x: number){
        x_attr = x;
        f(x) => self.x_attr;
        g(x: number) => self.f(76) + x;
    }
    function A(a: number, b){
        let p = new Point(a) in {
            a + p.g(100);
        };
    }
    print(5);
'''

program13 = '''
    function f(x:bool) => while (x){
    print(x);
    }
    4
    
'''

program14 = '''
    function f(x:bool) => while (x){
    print(x);
    };
    function f(x:int) => print(x);
    4
'''