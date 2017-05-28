# A comprehensive catalog of software smells

##Dependencies
The python implementation depends on **yattag** (http://www.yattag.org) library.

##Compilation and execution
Specify the path variables in the Main.py, and execute it using python3. I used PyCharm CE for developing and executing the program.

## The template to specify a smell
You may add new smells, categories, and references to the collection. The new items must follow the template specified below.

```
[smell]
[smell-id]XX
[smell-category]category such as 'Code smells', 'Configuration smells'
[smell-subcategory]subcategories such as 'Design smells', 'Architecture smells', 'Test smells'
[smell-name]smell name
[smell-description]description of the smell (one line; could be multiple statements)
[smell-aka]also known as (one line; could be multiple statements)
[smell-ref]main reference in which it was defined
[smell-end]
```

##Template for defining smell categories
```
[define-smell-category]
[smell-category-id]
[smell-category-name]
[smell-category-parent]empty for root level smell categories
[define-smell-category-end]
```

##Template for defining references
```
[reference]
[ref-id]
[ref-text]
[ref-image]
[ref-url]
[ref-end]
```