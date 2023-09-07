# Calculator App

This is a calculator application that can evaluate mathematical expressions in infix notation. It supports basic arithmetic operations, parentheses, and variables.

## Features

- Evaluate infix expressions with numbers, operators, and parentheses
- Converts infix expressions to postfix notation internally before evaluating 
- Supports addition, subtraction, multiplication, division, and exponentiation
- Follows order of operations and operator precedence
- Handles negative numbers correctly
- Advanced calculator supports variables and multi-line expressions
- Displays step-by-step state as it evaluates expressions
- Written in Python using custom stack and calculator classes

## Getting Started

The project contains the following files:

- `stack.py` - Implements a stack data structure 
- `calculator.py` - Calculator class that evaluates infix expressions
- `advanced_calculator.py` - Advanced calculator with variables  
- `main.py` - Example usage and tests

To run the app:

1. Clone the repository
2. Run `python main.py`

Try out the different calculator instances and sample expressions provided in `main.py`.

## Usage

The `Calculator` class takes an infix expression string as input. 

```python
calc = Calculator()
calc.setExpr("5 + 3 * (10 / (12 / (3 + 1) - 1))") 
result = calc.calculate()
```

The `AdvancedCalculator` class takes a multi-line string with variable assignments and expressions separated by semicolons.

```python
adv = AdvancedCalculator()
adv.setExpression("""
A = 5;
B = 10; 
C = A + B;
return C * 2
""")
result = adv.calculateExpressions()
```

See `main.py` for more examples.

## Implementation Details

- `Stack` class implements a basic stack data structure using a linked list
- Infix expressions converted to postfix notation using shunting yard algorithm
- Postfix expressions evaluated using a stack 
- Advanced calculator maps variable names to values in a dictionary
- Expressions checked for validity before evaluation

The stack, calculator, and advanced calculator are designed for loose coupling - each class contains only core logic related to its purpose.

## Credits

This project was created as a homework assignment for a CS class at Penn State. The instructions and specifications were provided by the professor.
