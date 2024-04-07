
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
                program10, program11, program12, program13, program14,
                program15]

    
    if case_number is None:
        return all_cases
    else:
        if case_number >= len(all_cases) or case_number < 0:
            raise Exception("Invalid case number")
        return [all_cases[case_number]]


program0 = '''
type Point(x: number, y: number){
    x = x;
    y = y;

    getX() => self.x
    getY() => self.y
    fib(n: number): number => if (n == 0 | n == 1) 1 else self.fib(n-1) + self.fib(n-2);
}
let p = new Point(0, 1) in{
    p.fib(9);
}
'''
program1 = '''
function fib(n: number): number => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
fib(9)
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
program15 = '''
    function tan(x: number): number => sin(x) / cos(x);
    function cot(x: number) => 1 / tan(x);
    function operate(x: number, y: number) {
        print(x + y);
        print(x - y);
        print(x * y);
        print(x / y);
    }
    function fib(n: number): number => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
    function fact(x: number) => let f = 1 in for (i in range(1, x+1)) f := f * i;
    function gcd(a: number, b: number): number => while (a > 0)
            let m = a % b in {
                b := a;
                a := m;
            };


    type Point(x:number,y:number) {
        x = x;
        y = y;

        getX() => self.x;
        getY() => self.y;

        setX(x) => self.x := x;
        setY(y) => self.y := y;
    }
    type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
        rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
    }
    type Knight(firstname, lastname) inherits Person(firstname, lastname) {
        name() => "Sir" @@ base();
    }
    type Person(firstname, lastname) {
        firstname = firstname;
        lastname = lastname;

        name() => self.firstname @@ self.lastname;
        hash() {
            5;
        }
    }
    type Superman{
    }
    type Bird{
    }
    type Plane {
    }
    type A {
        hello() => print("A");
    }

    type B inherits A {
        hello() => print("B");
    }

    type C inherits A {
        hello() => print("C");
    }

    {
        42;
        print(42);
        print((((1 + 2) ^ 3) * 4) / 5);
        print("Hello World");
        print("The message is \\"Hello World\\"");
        print("The meaning of life is " @ 42);
        print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));
        {
            print(42);
            print(sin(PI/2));
            print("Hello World");
        };


        print(tan(PI) ** 2 + cot(PI) ** 2);

        let msg = "Hello World" in print(msg);
        let number = 42, text = "The meaning of life is" in
            print(text @ number);
        let number = 42 in
            let text = "The meaning of life is" in
                print(text @ number);
        let number = 42 in (
            let text = "The meaning of life is" in (
                    print(text @ number)
                )
            );
        let a = 6, b = a * 7 in print(b);
        let a = 6 in
            let b = a * 7 in
                print(b);
        let a = 5, b = 10, c = 20 in {
            print(a+b);
            print(b*c);
            print(c/a);
        };
        let a = (let b = 6 in b * 7) in print(a);
        print(let b = 6 in b * 7);
        let a = 20 in {
            let a = 42 in print(a);
            print(a);
        };
        let a = 7, a = 7 * 6 in print(a);
        let a = 7 in
            let a = 7 * 6 in
                print(a);
        let a = 0 in {
            print(a);
            a := 1;
            print(a);
        };
        let a = 0 in
            let b = a := 1 in {
                print(a);
                print(b);
            };
        let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
        let a = 42 in print(if (a % 2 == 0) "even" else "odd");
        let a = 42 in
            if (a % 2 == 0) {
                print(a);
                print("Even");
            }
            else print("Odd");
        let a = 42, mod = a % 3 in
            print(
                if (mod == 0) "Magic"
                elif (mod % 3 == 1) "Woke"
                else "Dumb"
            );
        let a = 10 in while (a >= 0) {
            print(a);
            a := a - 1;
        };

        for (x in range(0, 10)) print(x);


        let pt = new Point(0,0) in
            print("x: " @ pt.getX() @ "; y: " @ pt.getY());
        let pt = new Point(3,4) in
            print("x: " @ pt.getX() @ "; y: " @ pt.getY());
        let pt = new PolarPoint(3,4) in
            print("rho: " @ pt.rho());

        let p = new Knight("Phil", "Collins") in
            print(p.name());
        let p: Person = new Knight("Phil", "Collins") in print(p.name());
        let x: number = 42 in print(x);

        let x = new Superman() in
            print(
                if (x is Bird) "It's bird!"
                elif (x is Plane) "It's a plane!"
                else "No, it's Superman!"
            );
        let x = 42 in print(x);
        let total = ({ print("Total"); 5; }) + 6 in print(total);
        let x : A = if (rand() < 0.5) new B() else new C() in
            if (x is B)
                let y : B = x as B in {
                    y.hello();
                }
            else {
                print("x cannot be downcasted to B");
            };
    }'''
