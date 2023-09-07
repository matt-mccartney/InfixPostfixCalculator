from advanced_calculator import AdvancedCalculator
from calculator import Calculator
from stack import Stack

if __name__ == "__main__":
    import doctest
    doctest.run_docstring_examples(Stack, globals(), verbose=True)
    doctest.run_docstring_examples(Calculator, globals(), verbose=True)
    doctest.run_docstring_examples(AdvancedCalculator, globals(), verbose=True)