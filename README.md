# python sqlite wrapper

Simple python sqlite wrapper. I like to use sqlite for some of my little pet or test applications. 
Because it's easy and fast. 
I also like to operate with data in JSON like format.<br>
Therefore, over time, I received such a wrapper with frequently used functions.

## Installation

Just put the file **wrapper.py** in your project directory and **import** into the file you need.

## Dependencies

Just Python standard library.

## Examples

<div style="display: flex;flex-direction:column;" id="content">
    <a href="#connect"> > connect()</a>
    <a href="#create_table"> > create_table()</a>
    <a href="#set_table"> > set_table()</a>
    <a href="#push"> > push()</a>
    <a href="#push_array"> > push_array()</a>
    <a href="#get"> > get()</a>
    <a href="#where"> > * "WHERE" options</a>
    <a href="#exist"> > exist()</a>
    <a href="#delete"> > delete()</a>
    <a href="#update"> > update()</a>
    <a href="#drop_table"> > drop_table()</a>
    <a href="#query"> > query()</a>
    <a href="#close"> > close()</a>
</div>

<br>

___

<br>

<h3 id="connect">connect()</h3>

```
import wrapper
    
DB = wrapper.SQLite()

DB.connect('test.db')
    
DB.close()
```
Connect your **.db** file or file will be created with given name.
 
<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="create_table">create_table()</h3>

```
import wrapper

DB = wrapper.SQLite()
DB.connect('test.db')

table_data = {
    'name' : 'users',
    'query' : 'ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, ROLE TEXT, NUMBER INTEGER'
}

DB.create_table(table_data)

DB.close()
```
Function accepts data with table **name** (string) and **query** with column parameters (string).
<br>
**Result (columns in created table "users"):**
<br>

|ID   |NAME |ROLE |NUMBER|
|:---:|:---:|:---:| :---:|
|  -  |  -  |  -  |  -   |

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="set_table">set_table()</h3>

```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

DB.close()
```
Function **set_table()** sets the table you will work with.
```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

columns = DB.set_table('users')

print(columns)

DB.close()
```

You can assign this function to a variable and it will return a list of column names:
```
['ID', 'NAME', 'ROLE', 'NUMBER']
```

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="push">push()</h3>

```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

data = {
    'name': 'John',
    'role': 'admin',
    'number': 33
}

DB.push(data)

DB.close()
```
Insert single data.<br>
**Result:**
|ID   |NAME |ROLE |NUMBER|
|:---:|:---:|:---:| :---:|
|  1  |John |admin|  33  |

Сan also be assigned to a variable and it will return the **ID** of the inserted data:

```
...
id = DB.push(data)
print(id)
```
**Result:**
```
1
```

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="push_array">push_array()</h3>

```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

data_array = [
    {
        'name': 'John',
        'role': 'admin',
        'number': 33
    },
    {
        'name': 'Steven',
        'role': 'user',
        'number': 11
    },
    {
        'name': 'Chris',
        'role': 'user',
        'number': 22
    }
]
DB.push_array(data_array)

DB.close()
```
Insert an array of data.
<br>
**Result:**
|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |

Сan also be assigned to a variable and it will return the count of the inserted data rows:

```
...
count = DB.push_array(data_array)
print(count)
```
**Result:**
```
3
```

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="get">get()</h3>

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |
```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

res = DB.get()

print(res)

DB.close()
```
Function **get()** without **options** will return all data from the table.<br>
**Result:**
```
[{'ID': 1, 'NAME': 'John', 'ROLE': 'admin', 'NUMBER': 33}, {'ID': 2, 'NAME': 'Steven', 'ROLE': 'user', 'NUMBER': 11}, {'ID': 3, 'NAME': 'Chris', 'ROLE': 'user', 'NUMBER': 22}]
```

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="where">"WHERE" options</h3>

Now about **options**. You can use "WHERE" **options** with **get()**, **update()**, **delete()**, **exist()** functions. For all of these functions, the "WHERE" **options** work in the same way.
```
...
res = DB.get({'role': user, 'number': 22})
print(res)
```
**Result:**
```
[{'ID': 3, 'NAME': 'Chris', 'ROLE': 'user', 'NUMBER': 22}]
```
You can just pass the SQL string:
```
...
res = DB.get('WHERE role = "user" AND number = 22')
print(res)
```
The result will be the same:
```
[{'ID': 3, 'NAME': 'Chris', 'ROLE': 'user', 'NUMBER': 22}]
```
You can also add a **delimiter** to the key through "__" and it will be used instead of the "=" sign in the "WHERE" options:
```
res = DB.get({'id__<': 3, 'number__>': 10})
print(res)
```
Its equal to "WHERE id < 3 AND number > 10"<br>
**Result:**
```
[{'ID': 2, 'NAME': 'Steven', 'ROLE': 'user', 'NUMBER': 11}]
```
**Eventually**. For complex "WHERE" options, use the SQL syntax string. Although the basic **wrapper options** requests cover more than.

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="exist">exist()</h3>

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |
```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

res = DB.get({'role': 'admin'})

print(res)

DB.close()
```
**Result:**
```
[{'ID': 1, 'NAME': 'John', 'ROLE': 'admin', 'NUMBER': 33}]
```
But:
```
...
res = DB.get({'role': 'manager'})
print(res)
```
**Result:**
```
False
```
The only difference between **exist()** and **get()** is that if there is no corresponding data, it returns **False** instead of an empty array.

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="delete">delete()</h3>

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |
```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

DB.delete({'role': 'admin'})

DB.close()
```
Removes rows that match the **"WHERE" options**
<br>
**Result:**
|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="update">update()</h3>

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |
```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

DB.update({'name': 'Steven'},{'role':'admin'})

DB.close()
```
Updates rows that match the **"WHERE" OPTIONS** , with the received data
<br>
**Result:**
|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|admin|  11  |
|  3  |Chris |user |  22  |

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="drop_table">drop_table()</h3>

```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

DB.drop_table()

DB.close()
```
Removes the setted table

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="query">query()</h3>

"Manual mode"

**Arguments:**
<br>
<ol>
  <li>SQL string</li>
  <ol>
    <li>eg. "SELECT * FROM users WHERE role = 'admin'"</li>
  </ol>
  <li>Fetch parameters</li>
  <ol>
    <li><b>"one"</b> for ".fetchone()"</li>
    <li><b>"many"</b> for ".fetchmany()"</li>
    <li><b>"all"</b> for ".fetchmall()"</li>
    <li><b>None</b> for use without it</li>
  </ol>
  <li>Data</li>
</ol>

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |

```
import wrapper

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

data = DB.query("SELECT * FROM users WHERE role = 'admin'", "all")

print(data)

DB.close()
```
**Result:**
```
[(1, 'John', 'admin', 33),]
```

<br>

```
import wrapper

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

data = ['Harvy', 'user', 99]

DB.query("INSERT INTO users (NAME, ROLE, NUMBER) VALUES (?,?,?)", None, data)

DB.close()
```
**Result:**

|ID   |NAME  |ROLE |NUMBER|
|:---:|:---: |:---:| :---:|
|  1  |John  |admin|  33  |
|  2  |Steven|user |  11  |
|  3  |Chris |user |  22  |
|  4  |Harvy |user |  99  |

<br>
<br>
<a href="#content"> ^ back</a>

<br>

___

<br>

<h3 id="close">close()</h3>

Сloses the database connection.

```
import wrapper 

DB = wrapper.SQLite()
DB.connect('test.db')

DB.set_table('users')

DB.get()

DB.close()
```

<br>
<br>
<a href="#content"> ^ back</a>
