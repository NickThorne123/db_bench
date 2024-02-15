### Overview

This piece of documentation outlines the rules and conventions that developers must follow when writing code or engaging in the software required for this project. These rules below define the characteristics necessary to maintain a uniform software solution and to facilitate collaboration among developers maintaining clean, readable, secure, and efficient practices.

This document is split into 4 main components, these being the branch naming conventions, the Joel Test (used to implement good software practices), coding conventions and documentation standards that members of the team must follow.

### Branch Naming Conventions

The GitHub development flow will be used so individuals can create a branch for issues they are working on. 

The branch will be named like the following example: `nt_123_short_desc` 

Breaking this down, 
1. `nt` will be the developer's initials
2. `123` will be the Issue Number 
3. There will then be a one or two word description of the issue. 

Projects will move from In-Progress to In-Review Upon pushing changes up to a Pull Request. Which will then run through CI/CD pipeline and be reviewed by another member of the group

### Joel Test

The project will try and adhere to the 'Joel Test' of good software practice.

The Joel Test is a very simple and quick test that rates the quality of your software team. Rather than including open-ended responses, this test has 12 yes-or-no questions that determine whether your programming team is up to par. A score of 12 is perfect. 11 is considered tolerable, and 10 or below is unacceptable. These 12 questions are as follows:

#### 1. Do you use source control?

Source control (or version control) tracks and manages changes made to code. Changes are marked by a tag, known as the "revision number." The original code is deemed "revision 1," and, after the first round of edits, it becomes known as "revision 2," and so on.

Source control is important because programmers can work together on code and track changes over time. This makes it easier to highlight mistakes and correct them before they cause major problems. And, since the source code gets uploaded into every programmer's hard drive, it's much harder to lose revisions.

#### 2. Can you make a build in one step?

A "build in one step" is the ability to combine multiple sections of code, written by various programmers, into one top-level program or tool. As you build, the source code of various tools or features should combine into a single program that can run on its own.

It's important to have a "build in one step" because large programs take more time to complete if they're written by a single person. Instead, it's faster to divide it up into multiple sections, so work can be distributed between several developers. In the end, all the sections and sub-sections are combined into an all-inclusive program.

#### 3. Do you make daily builds?

When using source control, it's easy for programmers to break the build when writing new code. What's even worse is when they don't realize it's broken. A broken build can stall production until the issue is recognized and resolved. To safeguard against this, your team should be conducting daily builds to verify if anything has broken.

If something shows up during the daily build, programmers can check the code that got added or modified to figure out what broke it. Then, fixing the code becomes the responsibility of the person who added that change. This system ensures that errors are noted and fixed as soon as possible and that each programmer can navigate the build.

#### 4. Do you have a bug database?

It's impossible to remember every bug in the code -- especially when there can be so many. For instance, if you click a link and realize it's dead, that action may be automatically saved into a bug database. Since bugs can be reported in a variety of ways, it's important to collect all reported bugs into one database because, if not, they may get forgotten and never fixed.

Additionally, bug databases can work as knowledge bases for programmers. You can use the bug database to see if a similar problem has been reported and if there are steps on how to fix the issue.

#### 5. Do you fix bugs before writing new code?

When writing, you may prefer to write first and edit mistakes later. Many programmers have a similar mindset when it comes to writing code and would prefer to fix bugs after the original code is written. However, this can lead to major flaws, making it more important to prioritize bug-fixing than writing new code.

The longer you wait to fix a bug, the harder it will be to remember where the bug occurred. Fixing it the same day will take minutes while fixing a bug that was written weeks or months ago will be stressful. And, if the product has already shipped, you'll have to recall it and waste copious funds.

Additionally, it's much easier to predict how long it will take to write new code than it will take to fix a bug. This is because fixing a bug depends on when that code was written and how long it will take to track it down. Instead, if bugs are fixed immediately, you can schedule more time to write new code.

#### 6. Do you have an up-to-date schedule?

It's essential to know when code is going to be complete. It's simply unacceptable to leave this to the programmers' leisure. Advertisements, shipments, and even the general satisfaction of customers all ride on code being written in an efficient timeframe.

Having a schedule makes your programmers' work easier. With a schedule, programmers can sort through the list of features to add and weed out the unnecessary ones that will take up too much time. This will ensure your programmers are hitting deadlines and working on code that's essential to your product's success.

#### 7. Do you have a spec?

Product specs are blueprints that describe exactly what the product will do, what it should look like, and how it will perform. Additionally, these guidelines can help product management optimize the product's features for your target audience. They'll outline all the information about the product, so every member of the product development team will know exactly what to create.

When products aren't built from specs, they're more likely to have bugs, be poorly designed, or take too long to build. This wastes time and money, making it risky to write code without having a spec. Whether it's written by your programmers or external writers who are hired for the job, specs should be written and approved before programming begins.

#### 8. Do programmers have quiet working conditions?

According to Spolsky, it's important for software workers -- among other knowledge workers -- to get "in the zone" to get productive work done. Being intently focused is great, but it's a difficult state to attain. After all, it takes the average employee about 15 minutes to start working at one's maximum productivity level.

The simplest distractions can lead to a severe lack of productivity. Overhearing conservations, taking phone calls, and being interrupted by coworkers can result in 15 to 30 minutes of wasted time. So, giving programmers quiet offices, rather than open cubicles, can lead to more production.

#### 9. Do you use the best tools money can buy?

The best companies provide their employees with the best tools. Without them, your employees won't be able to produce a high-quality product. If you want your software development team to succeed, then it's important to invest in the best software development tools.

#### 10. Do you have testers?

It's vital that your software team has testers -- about one per every two or three programmers. Without testers, you may be sending out defective products or wasting money by having programmers. Additionally, testers help refocus your programmers', so they can spend more time coding and troubleshooting.

#### 11. Do new candidates write code during their interview?

You probably wouldn't hire someone for a job without seeing if they can perform that job. For instance, would you ever hire a graphic designer without seeing their creative portfolio? Or, would you hire a baker to make your wedding cake without first tasting their samples?

The sentiment should be applied to programmers. Of course, you can still select candidates based on their resumes, references, personalities, or answers to interview questions. However, their ability to write code during the interview should be the most important. After all, that's what they'll be doing all day.

#### 12. Do you do hallway usability testing?

Hallway usability testing is when you stop someone who walks by you in the hallway and ask them to use the code you just finished writing. Having five random people test out your code will show you 95% of the usability problems with your code.

User interfaces are hard to assess when you're the one who has been staring at it for hours on end. It's important to get fresh eyes on your code to point out issues you may have overlooked. And, since hallway usability testing is both quick and free, you can continuously test your code until it's perfect.

[More Info Here](https://blog.hubspot.com/service/joel-test)

### Coding Conventions

The coding conventions for this project will follow is the PEP 8 Conventions - This is documentation that provides guidelines and best practices on how to write Python code. This can be viewed here: [PEP 8 Documentation](https://peps.python.org/pep-0008/#introduction). However I will pull out the main features within this document.

When coding standards are properly defined and implemented, developers, even those who have just joined the team, can easily find their way around the code base. Ideally, wanting our source code to look like a single developer has written, debugged, and maintained it.  

#### Code Layout

1. File Header - File headers will be at the top of every file and include the following information: 
   * FileName - Will be the name of the file
   * FileType - Will be the type of file i.e. py (python), cs (c#), js (JavaScript)
   * Created By - Who it was created by. Formatted as Surname, First Name
   * Created On - The date and time it was created on in a dd/mm/yyyy hh:mm:ss AM/PM format
   * Last Modified - The date and time it was last modified on in a dd/mm/yyyy hh:mm:ss AM/PM format
   * Description - Brief description on what the file does

   An example can be seen below:

```
   # File Header --------------------------------------
   # FileName:      main.py
   # FileType:      Python File
   # Created By:    Roberts, Kyle
   # Created On:    01/02/2024 6:00:00 PM
   # Last Modified: 01/02/2024 6:30:16 PM
   # Description:   This is a file TODO
   # End Header ---------------------------------------
```

2. Imports - Imports will be put at the top of the file, putting a blank line between each group of imports. Imports should be grouped in the following order. Standard library imports, related third party imports, local application/library specific imports.An example of this can be seen below:

```
   import os
   import warnings

   import pandas as pd   
   from sklearn.decomposition import PCA
   from sklearn.preprocessing import StandardScaler, MinMaxScaler
   from sklearn.cluster import KMeans

   from local_module import local_class
   from local_package import local_function
```

3. Indentation - Indentation refers to the spaces at the beginning of a code line. Where in other programming languages the indentation in code is for readability only, the indentation in Python is very important. Python uses indentation to indicate a blocks of code. Use 4 spaces per indentation level. There needs to be at least 2 blank spaces between methods, with the new method starting on the 3rd line.

   Extra blank lines may be used (sparingly) to separate groups of related functions. Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations) and the use of blank lines in functions, needs to also be done sparingly, but should be there to indicate logical sections.

   Finally, a line break needs to be done before a binary operator called Knuth's style an example of this can be seen below:

```
   # Easy to match operators with operands
   income = (gross_wages
             + taxable_interest
             + (dividends - qualified_dividends)
             - ira_deduction
             - student_loan_interest)
```

#### Naming Conventions 

| Type | Naming Convention | Examples |
| :-- | :---------------: | :------: |
| Functions | Use a lowercase word or words. Separate words by underscores to improve readability | function, my_function |
| Variable | Use a lowercase single letter, word, or words. Separate words with underscores to improve readability. Needs to be a clear and concise explanation of what the variable does or stores | x, var, my_variable, clickhouse_dataset |
| Class | Start each word with a capital letter. Do not separate words with underscores. This style is called camel case or pascal case | Model, MyClass |
| Method | Use a lowercase word or words. Separate words with underscores to improve readability. Needs to be a clear and concise explanation of what the method does (don't worry about character length) | class_method, method, loads_postgres_database |
|Constant | Use an uppercase single letter, word, or words. Separate words with underscores to improve readability | CONSTANT, MY_CONSTANT, MY_LONG_CONSTANT |
| Module | Use a short, lowercase word or words. Separate words with underscores to improve readability. | module.py, my_module.py  |
| Package | Use a short, lowercase word or words. Do not separate words with underscores | package, mypackage |
#### Comments 

Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes. The first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!).A comment must be short and straightforward, and sensible adding value to your code. You should add comments to give code overviews and provide additional information that is not readily available in the code itself, containing only information that is relevant to reading and understanding the program.

1. Docstrings - Docstrings or triple-quoted string literals will be used to provide descriptions of classes, functions(Methods) and constructors. These should be a brief description of what each method does. These can be a single line or a multi-line and should begin with a capital letter and end in a period. Examples can be seen below:

```
    """ Description of method here. """
    def method():
        print("Hello there")
```

```
    """
    Bigger Description of
    a method is placed here.
    """
    def method():
        print("Hello there")
```

2. Single Line Comments - Single Line Comments will primarily be comments that are written over Python statements to clarify what they are doing. An example be seen below:

```
   # Program to print the user's name
   name = input('Enter your name')
   print(name)
```

3. Inline Comments - An Inline comment should be a concise comment on the same line as the code they describe and are useful when you are using any formula or any want to explain the code line in short. They should be separated by at least two spaces. An Example can be seen below:

```
   plt.plot(xtest, ytest, color='green', linewidth=1, label='Actual Price')        # plotting the initial datapoints
```

4. Block Comments - Blocks comments will be used to create a file header at the top of every new python file that is created and when it was last modified. An example of this can be seen below:

```
   # FileName:      main.py
   # FileType:      Python File
   # Created By:    Roberts, Kyle
   # Created On:    01/02/2024 6:00:00 PM
   # Last Modified: 01/02/2024 6:30:16 PM
   # Description:   This file in the main python file
```
#### Strings

This application will follow the convention of using double quoted strings as opposed to single quoted strings. An example of this can be seen below:

```
print("The quick brown fox jumps over the lazy dog")
```

#### Whitespace in Expressions and Statements

Immediately inside parentheses, brackets or braces:

```
spam(ham[1], {eggs: 2})
```

Between a trailing comma and a following close parenthesis:

```
foo = (0,)
```

Immediately before a comma, semicolon, or colon:

```
if x == 4: print(x, y); x, y = y, x
```

Immediately before the open parenthesis that starts the argument list of a function call:

```
spam(1)
```

Immediately before the open parenthesis that starts an indexing or slicing:

```
dct['key'] = lst[index]
```

More than one space around an assignment (or other) operator to align it with another:

```
x = 1
y = 2
long_variable = 3
```

Don’t use spaces around the = sign when used to indicate a keyword argument, or when used to indicate a default value for an unannotated function parameter:

```
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

#### Example Python File
Overall what a python file could look like using the PEP8 conventions below:

```
# FileName:      main.py
# FileType:      Python File
# Created By:    Roberts, Kyle
# Created On:    01/02/2024 6:00:00 PM
# Last Modified: 01/02/2024 6:30:16 PM
# Description:   This is a file TODO

import os
import warnings

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from local_module import local_class
from local_package import local_function

""" Plots a line graph for the user """
def plot_a_line_graph():
    dataset = pd.read_csv("somecsv.csv")

    # gets x and y values specific columns
    x = dataset.iloc[:, 0:260].values
    y = dataset.iloc[:, 100].values 

    xplot = []
    for i in range(1, len(x)):
        xplot.append(i)

    plt.plot(xplot, y, color='green', linewidth=1, label='Actual Price')        # plotting the initial datapoints
    plt.show()


""" 
Allows a user to view their income based off 
the passed in parameters used to calculate it.
"""
def view_and_calculate_income(gross_wages, taxable_interest, dividends, ira_deduction):
    # Calculates income based on the below features
    income = (gross_wages
             + taxable_interest
             + dividends
             - ira_deduction)
    print(income)

```

#### Final Remarks to keep in mind


Code Line Length: Limit the length of lines to help improve readability. PEP8 recommends no more then 79, however up to 120 is acceptable if needed.

Function/Method Length: Try to keep functions/methods short and focused on a specific task. Long functions should be broken down into smaller, more manageable ones.

Error Handling: Implement proper error handling and communicate errors clearly. The goal is to identify and properly respond to errors and exceptions. When there are clear guidelines for reporting, logging, and handling errors, your code becomes more reliable and, over time, more error-proof. 

File Organization: Organize code into logical sections or modules. Follow a consistent file and directory structure.

### Documentation Standards

The documentation standards are the guidelines and best practices for creating and maintaining clear, consistent, and useful documentation for this project. This includes how to organize and structure information, how to format and style content. Furthermore, this document should be used as an example of how to format documentation for this project.

#### Styling Headers

For main headers such as the examples in this document; Overall, Coding Standards and Documentation Standards. The heading size will be the 'h3' designation or in text ``` ### ```. For sub-headers these will be 'h4' or in text ```####```. Some examples in this document include; styling headers, comments and example python file.

#### Styling Code

To style code of different lines, a user needs too use 3 apostrophes ``` at the start and end of the code block. With the code being styled and formatted in the way it is present on an IDE with the correct indentations and spacing's. 

#### Styling Bullet Points

Bullet points can be styled in 1 of two ways, if the user intends to make a numbered list, like in the branch naming conventions. It should be as follows:

1. Example 1
2. Example 2

If the user intended to use classic bullet points they need to use the * character in order to achieve this. An example of how this would look can be seen below:

* Bullet Point 1
* Bullet Point 2

#### Adding in Links

In an effort to make URL/URI links more readable for a developer, the link will be given link text, followed by the URL/URI. To do this a user would need to place the link text in square brackets ```[]``` proceeded by round brackets or parentheses ```()```. Combined they will look like this ```[]()```.

If a developer opts to name the link in the square bracket, it will be displayed as blue hyperlink, which is underlined. As seen above, in an example linking to PEP8 documentation.

#### Adding Photos

To add a photo into markdown, it follows the same pattern as adding a link, with the only exception being an exclamation mark the brackets. An example looks like this ```![]()```. 

A user can choose to add a name to the photo or leave it blank. But to add a photo I would suggest a user leaves a line spacing before and after the picture to allow it to be formatted correctly. As seen in the example below:

![](https://github.com/NickThorne123/db_bench/assets/115091926/86b7f67d-d398-4276-a94a-2921466d7c8c)

Because if not, then the formatting can looks off as seen below:

Wrong Format
![](https://github.com/NickThorne123/db_bench/assets/115091926/6390effe-006c-44cf-b968-3b27da4c0ce7)
Messes up the format
