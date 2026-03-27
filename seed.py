"""Populate the database with lessons and quiz questions."""
from app import create_app, db
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion

app = create_app()

lessons_data = [
    {
        "id": "lesson-1",
        "title": "Hello, C++",
        "description": "Write your very first C++ program and understand the basic structure.",
        "difficulty": "beginner",
        "xp_reward": 50,
        "estimated_minutes": 10,
        "display_order": 1,
        "content": "# Hello, C++\n\nEvery C++ program starts with a `main()` function.\n\n```cpp\n#include <iostream>\nint main() {\n    std::cout << \"Hello, World!\";\n    return 0;\n}\n```\n\n**Key concepts:**\n- `#include <iostream>` imports the input/output library\n- `std::cout` prints text to the console\n- `return 0` means the program ended successfully",
        "code_template": '#include <iostream>\n\nint main() {\n    // Write your first C++ program!\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
    },
    {
        "id": "lesson-2",
        "title": "Variables & Data Types",
        "description": "Learn how to store and manipulate data using variables.",
        "difficulty": "beginner",
        "xp_reward": 75,
        "estimated_minutes": 15,
        "display_order": 2,
        "content": "# Variables & Data Types\n\nVariables store data. Each variable has a type.\n\n```cpp\nint age = 21;\ndouble price = 9.99;\nchar grade = 'A';\nstd::string name = \"Alice\";\nbool isStudent = true;\n```\n\n**Common types:** `int`, `double`, `char`, `string`, `bool`",
        "code_template": '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Declare variables of different types\n    int age = 21;\n    double gpa = 3.8;\n    string name = "Student";\n\n    cout << name << " is " << age << " years old." << endl;\n    cout << "GPA: " << gpa << endl;\n\n    return 0;\n}',
    },
    {
        "id": "lesson-3",
        "title": "Control Flow",
        "description": "Use if-else statements to make decisions in your programs.",
        "difficulty": "beginner",
        "xp_reward": 100,
        "estimated_minutes": 20,
        "display_order": 3,
        "content": "# Control Flow\n\nUse `if`, `else if`, and `else` to make decisions.\n\n```cpp\nif (score >= 90) {\n    cout << \"A\";\n} else if (score >= 80) {\n    cout << \"B\";\n} else {\n    cout << \"C\";\n}\n```",
        "code_template": '#include <iostream>\nusing namespace std;\n\nint main() {\n    int score = 85;\n\n    if (score >= 90) {\n        cout << "Grade: A" << endl;\n    } else if (score >= 80) {\n        cout << "Grade: B" << endl;\n    } else {\n        cout << "Grade: C" << endl;\n    }\n\n    return 0;\n}',
    },
    {
        "id": "lesson-4",
        "title": "Loops",
        "description": "Repeat actions using for and while loops.",
        "difficulty": "beginner",
        "xp_reward": 100,
        "estimated_minutes": 20,
        "display_order": 4,
        "content": "# Loops\n\n`for` loops run a set number of times. `while` loops run until a condition is false.\n\n```cpp\nfor (int i = 0; i < 5; i++) {\n    cout << i << endl;\n}\n```",
        "code_template": '#include <iostream>\nusing namespace std;\n\nint main() {\n    // For loop\n    for (int i = 1; i <= 5; i++) {\n        cout << "Count: " << i << endl;\n    }\n\n    return 0;\n}',
    },
    {
        "id": "lesson-5",
        "title": "Functions",
        "description": "Organize your code into reusable functions.",
        "difficulty": "intermediate",
        "xp_reward": 125,
        "estimated_minutes": 25,
        "display_order": 5,
        "content": "# Functions\n\nFunctions let you reuse code.\n\n```cpp\nint add(int a, int b) {\n    return a + b;\n}\n```",
        "code_template": '#include <iostream>\nusing namespace std;\n\nint add(int a, int b) {\n    return a + b;\n}\n\nint main() {\n    cout << "3 + 4 = " << add(3, 4) << endl;\n    return 0;\n}',
    },
    {
        "id": "lesson-6",
        "title": "Arrays & Vectors",
        "description": "Store collections of data with arrays and vectors.",
        "difficulty": "intermediate",
        "xp_reward": 125,
        "estimated_minutes": 25,
        "display_order": 6,
        "content": "# Arrays & Vectors\n\nArrays store fixed-size collections. Vectors are dynamic.\n\n```cpp\n#include <vector>\nvector<int> nums = {1, 2, 3};\nnums.push_back(4);\n```",
        "code_template": '#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> scores = {90, 85, 78};\n    scores.push_back(92);\n\n    for (int s : scores) {\n        cout << s << " ";\n    }\n    cout << endl;\n\n    return 0;\n}',
    },
    {
        "id": "lesson-7",
        "title": "Pointers & References",
        "description": "Understand memory addresses and references in C++.",
        "difficulty": "advanced",
        "xp_reward": 150,
        "estimated_minutes": 30,
        "display_order": 7,
        "content": "# Pointers & References\n\nPointers store memory addresses. References are aliases.\n\n```cpp\nint x = 10;\nint* ptr = &x;  // pointer\nint& ref = x;   // reference\n```",
        "code_template": '#include <iostream>\nusing namespace std;\n\nint main() {\n    int x = 42;\n    int* ptr = &x;\n\n    cout << "Value: " << x << endl;\n    cout << "Address: " << ptr << endl;\n    cout << "Via pointer: " << *ptr << endl;\n\n    return 0;\n}',
    },
    {
        "id": "lesson-8",
        "title": "Classes & Objects",
        "description": "Introduction to object-oriented programming in C++.",
        "difficulty": "advanced",
        "xp_reward": 175,
        "estimated_minutes": 35,
        "display_order": 8,
        "content": "# Classes & Objects\n\nClasses group data and functions together.\n\n```cpp\nclass Dog {\npublic:\n    string name;\n    void bark() { cout << name << \" says Woof!\"; }\n};\n```",
        "code_template": '#include <iostream>\nusing namespace std;\n\nclass Student {\npublic:\n    string name;\n    int age;\n\n    void introduce() {\n        cout << "Hi, I am " << name << ", age " << age << endl;\n    }\n};\n\nint main() {\n    Student s;\n    s.name = "Alice";\n    s.age = 20;\n    s.introduce();\n\n    return 0;\n}',
    },
]

quiz_data = [
    # Lesson 1
    {"id": "q1", "lesson_id": "lesson-1", "question": "What does `#include <iostream>` do?", "options": ["Declares a variable", "Imports the input/output library", "Starts the program", "Defines a function"], "correct_index": 1, "explanation": "The #include directive imports the iostream library for input/output operations."},
    {"id": "q2", "lesson_id": "lesson-1", "question": "What does `cout` do in C++?", "options": ["Reads input", "Outputs text to the console", "Declares a variable", "Includes a library"], "correct_index": 1, "explanation": "cout is the standard output stream in C++."},
    {"id": "q3", "lesson_id": "lesson-1", "question": "What does `return 0` mean in main()?", "options": ["The program crashed", "The program ended successfully", "A syntax error", "Nothing"], "correct_index": 1, "explanation": "Returning 0 from main indicates successful execution."},
    # Lesson 2
    {"id": "q4", "lesson_id": "lesson-2", "question": "Which type stores decimal numbers?", "options": ["int", "char", "double", "bool"], "correct_index": 2, "explanation": "double stores floating-point (decimal) numbers."},
    {"id": "q5", "lesson_id": "lesson-2", "question": "What is the value of `bool isReady = true;`?", "options": ["0", "1 (true)", "\"true\"", "null"], "correct_index": 1, "explanation": "In C++, true is a boolean literal with numeric value 1."},
    {"id": "q6", "lesson_id": "lesson-2", "question": "Which keyword declares a constant variable?", "options": ["var", "let", "const", "static"], "correct_index": 2, "explanation": "The const keyword makes a variable read-only."},
    # Lesson 3 - Control Flow
    {"id": "q7", "lesson_id": "lesson-3", "question": "Which keyword is used to handle a condition that is false?", "options": ["if", "else", "while", "switch"], "correct_index": 1, "explanation": "The else keyword handles the case when the if condition is false."},
    {"id": "q8", "lesson_id": "lesson-3", "question": "What does `else if` allow you to do?", "options": ["End the program", "Check multiple conditions", "Declare a variable", "Create a loop"], "correct_index": 1, "explanation": "else if lets you check additional conditions after the initial if."},
    {"id": "q9", "lesson_id": "lesson-3", "question": "What will this print if score = 85? if (score >= 90) cout << 'A'; else if (score >= 80) cout << 'B'; else cout << 'C';", "options": ["A", "B", "C", "Nothing"], "correct_index": 1, "explanation": "85 is >= 80 but not >= 90, so it prints B."},

    # Lesson 4 - Loops
    {"id": "q10", "lesson_id": "lesson-4", "question": "What does a for loop require?", "options": ["A condition only", "Initialization, condition, and increment", "Just an increment", "A function call"], "correct_index": 1, "explanation": "A for loop has three parts: initialization, condition, and increment."},
    {"id": "q11", "lesson_id": "lesson-4", "question": "How many times does this loop run? for (int i = 0; i < 5; i++)", "options": ["4", "5", "6", "0"], "correct_index": 1, "explanation": "The loop runs from i=0 to i=4, which is 5 times."},
    {"id": "q12", "lesson_id": "lesson-4", "question": "When does a while loop stop?", "options": ["After 10 iterations", "When its condition becomes false", "When break is called only", "Never"], "correct_index": 1, "explanation": "A while loop continues until its condition evaluates to false."},

    # Lesson 5 - Functions
    {"id": "q13", "lesson_id": "lesson-5", "question": "What keyword is used to return a value from a function?", "options": ["send", "output", "return", "give"], "correct_index": 2, "explanation": "The return keyword sends a value back to the caller."},
    {"id": "q14", "lesson_id": "lesson-5", "question": "What is the return type of this function? int add(int a, int b)", "options": ["void", "float", "int", "string"], "correct_index": 2, "explanation": "The return type is declared before the function name, which is int here."},
    {"id": "q15", "lesson_id": "lesson-5", "question": "What is the main benefit of using functions?", "options": ["They slow down the program", "They make code reusable", "They replace variables", "They are required in C++"], "correct_index": 1, "explanation": "Functions allow you to write code once and reuse it multiple times."},

    # Lesson 6 - Arrays & Vectors
    {"id": "q16", "lesson_id": "lesson-6", "question": "Which method adds an element to the end of a vector?", "options": ["add()", "append()", "push_back()", "insert()"], "correct_index": 2, "explanation": "push_back() adds an element to the end of a vector."},
    {"id": "q17", "lesson_id": "lesson-6", "question": "What is the difference between an array and a vector?", "options": ["Arrays are faster", "Vectors are dynamic in size", "Arrays can store more data", "There is no difference"], "correct_index": 1, "explanation": "Vectors can grow and shrink dynamically, while arrays have a fixed size."},
    {"id": "q18", "lesson_id": "lesson-6", "question": "Which header is needed to use vectors?", "options": ["<array>", "<list>", "<vector>", "<collection>"], "correct_index": 2, "explanation": "You need to include <vector> to use the vector class."},

    # Lesson 7 - Pointers & References
    {"id": "q19", "lesson_id": "lesson-7", "question": "What does the & operator do when used in a declaration?", "options": ["Multiplies two values", "Creates a reference", "Dereferences a pointer", "Declares a constant"], "correct_index": 1, "explanation": "When used in a declaration, & creates a reference (alias) to a variable."},
    {"id": "q20", "lesson_id": "lesson-7", "question": "How do you declare a pointer to an integer?", "options": ["int& ptr", "int* ptr", "ptr int", "pointer<int> ptr"], "correct_index": 1, "explanation": "int* ptr declares a pointer to an integer using the * symbol."},
    {"id": "q21", "lesson_id": "lesson-7", "question": "What does the * operator do when used with a pointer?", "options": ["Gets the address", "Dereferences to get the value", "Declares a pointer", "Multiplies only"], "correct_index": 1, "explanation": "The * operator dereferences a pointer to access the value at that memory address."},

    # Lesson 8 - Classes & Objects
    {"id": "q22", "lesson_id": "lesson-8", "question": "What keyword is used to define a class in C++?", "options": ["struct", "object", "class", "type"], "correct_index": 2, "explanation": "The class keyword is used to define a class in C++."},
    {"id": "q23", "lesson_id": "lesson-8", "question": "What does the public keyword mean in a class?", "options": ["Members are hidden", "Members are accessible from outside the class", "Members are constants", "Members are static"], "correct_index": 1, "explanation": "public means the members can be accessed from outside the class."},
    {"id": "q24", "lesson_id": "lesson-8", "question": "What is an object?", "options": ["A function inside a class", "An instance of a class", "A type of variable", "A loop structure"], "correct_index": 1, "explanation": "An object is an instance of a class — a concrete realization of the class blueprint."},
]

with app.app_context():
    # Only seed if lessons table is empty
    if Lesson.query.count() == 0:
        for data in lessons_data:
            db.session.add(Lesson(**data))
        for data in quiz_data:
            db.session.add(QuizQuestion(**data))
        db.session.commit()
        print("Seeded database with lessons and quiz questions.")
    else:
        print("Database already has data, skipping seed.")
