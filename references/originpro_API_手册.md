# originpro Python 包 API 手册（离线生成）

> 由本机已安装的 `originpro` 包源码 docstring 自动生成，用于离线查阅/喂给 AI。在线官方文档：https://www.originlab.com/python/doc/originpro/annotated.html

- 包路径：`<Python>\Lib\site-packages\originpro`
- Python：3.13.14
- 版本：1.1.12

## 目录

- [originpro](#originpro) — 顶层入口（op.new, op.open, op.find_sheet …）
- [originpro.base](#originprobase)
- [originpro.worksheet](#originproworksheet)
- [originpro.matrix](#originpromatrix)
- [originpro.graph](#originprograph)
- [originpro.analysis](#originproanalysis)
- [originpro.image](#originproimage)
- [originpro.notes](#originpronotes)
- [originpro.project](#originproproject)
- [originpro.pe](#originprope)
- [originpro.imp](#originproimp)
- [originpro.dc](#originprodc)
- [originpro.config](#originproconfig)
- [originpro.utils](#originproutils)

## `originpro`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


## `originpro.base`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `BaseLayer`

base class for all Origin layers

基类：`BaseObject`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make layer/sheet active
    Parameters:
        none
    Returns:
        last_active layer index
    Examples:
        wks = op.find_sheet()
        wb = wks.get_book()
        wb.add_sheet()
        wks.activate()

**方法** `add_label(self, text, x=None, y=None)`

    Add a label to a layer.

    Parameters:
        text (str): The text of a text label
        x(float or None): The X coordinate of the left of the object
        y(float or None): The Y coordinate of the top of the object

    Returns:
        (Label)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        text = gl.add_label("hello", 4, 8)
        text.text = 'world'

**方法** `add_line(self, x1, y1, x2, y2)`

    Add a line to a layer.

    Parameters:
        x1(float or None): The begin X coordinate
        y1(float or None): The brgin Y coordinate
        x2(float or None): The end X coordinate
        y2(float or None): The end Y coordinate

    Returns:
        (Line)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        line = gl.add_line(5, 5, 6, 8)
        line.width = 5
        line.set_int('arrowendshape', 2)

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    delete the sheet/layer
    Parameters:
        none
    Returns:
        none
    Examples:
        wks1=op.new_sheet()
        wks1.destroy()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `label(self, name)`

    Get a Label instance by name.

    Parameters:
        name (str): name of the label to be attached
    Returns:
        (Label)

    Examples:
        g = op.new_graph()
        g[0].label('XB').remove()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove_label(self, label)`

    Remove a label from a layer.

    Parameters:
        label (Label or str): Instance of Label or name of label to remove

    Returns:
        None

    Examples:
        g = op.new_graph()
        g[0].remove_label('xb') # g[0] is 1st layer.

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `BaseObject`

base class for all Origin objects

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `BasePage`

base class for all Origin books and graph, it holds a PyOrigin Page

基类：`BaseObject`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `DBook`

base class for data books, like workbook and matrix book

基类：`BasePage`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `DSheet`

base class for data sheets, like worksheets and matrix sheets

基类：`BaseLayer`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make layer/sheet active
    Parameters:
        none
    Returns:
        last_active layer index
    Examples:
        wks = op.find_sheet()
        wb = wks.get_book()
        wb.add_sheet()
        wks.activate()

**方法** `add_label(self, text, x=None, y=None)`

    Add a label to a layer.

    Parameters:
        text (str): The text of a text label
        x(float or None): The X coordinate of the left of the object
        y(float or None): The Y coordinate of the top of the object

    Returns:
        (Label)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        text = gl.add_label("hello", 4, 8)
        text.text = 'world'

**方法** `add_line(self, x1, y1, x2, y2)`

    Add a line to a layer.

    Parameters:
        x1(float or None): The begin X coordinate
        y1(float or None): The brgin Y coordinate
        x2(float or None): The end X coordinate
        y2(float or None): The end Y coordinate

    Returns:
        (Line)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        line = gl.add_line(5, 5, 6, 8)
        line.width = 5
        line.set_int('arrowendshape', 2)

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    delete the sheet/layer
    Parameters:
        none
    Returns:
        none
    Examples:
        wks1=op.new_sheet()
        wks1.destroy()

**方法** `from_file(self, fname, keep_DC=True, dctype='', sel='', sparks=False)`

    Imports data from a file using a Data Connector.

    Parameters:
        fname (str): File path and name to import.
        keep_DC (bool): Keep the Data Connector in the book after import
        dctype (str): Data Connector name, like "Import Filter", "MATLAB", "NetCDF", if not specified, CSV or Excel connector will be used based on file name
        sel (str): selection in the file, this will depend on the connector
        sparks (bool): Allows sparklines or not, True will follow GUI setting to add sparklines, False will disable it completely
    Returns:
        None

    Examples:
        wks=op.find_sheet()
        fn=op.path('e') + 'Samples\\Import and Export\donations.csv'
        wks.from_file(fn, False)#remove connector after import to allow further edit of data
        wks2=op.new_sheet()
        wks2.from_file(op.path()+'test.xlsx')#assuming you have this in UFF(user files folder)

**方法** `get_book(self)`

    Must be implemented by dervied methods

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_labels(self, type_='L')`

    get_labels

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `has_DC(self)`

    Returns whether a sheet has a Data Connector.

    Parameters:

    Returns:
        (str) name of the Data Connector, like 'csv', 'excel'

    Examples:
        dc = wb.has_DC()
        if len(dc):
            print(f'sheet is connected using {dc}')

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `label(self, name)`

    Get a Label instance by name.

    Parameters:
        name (str): name of the label to be attached
    Returns:
        (Label)

    Examples:
        g = op.new_graph()
        g[0].label('XB').remove()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self, use_name=True)`

    Parameters:
        use_name(bool):
    Returns:
        Return the Origin Range String that identify Data Sheet object
    Examples:
        ws=op.find_sheet()
        print(ws.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove_DC(self)`

    Removes Data Connector from a sheet.

    Parameters:

    Returns:
        None

    Examples:
        wks.remove_DC()

**方法** `remove_label(self, label)`

    Remove a label from a layer.

    Parameters:
        label (Label or str): Instance of Label or name of label to remove

    Returns:
        None

    Examples:
        g = op.new_graph()
        g[0].remove_label('xb') # g[0] is 1st layer.

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_labels(self, labels, type_='L', offset=0)`

    set_labels

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `shape`：Parameters:
- 属性 `show`：Property getter returns show state of object.
- 属性 `tabcolor`：Parameters:
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `GObject`

This class represents an instance of a text object on a GLayer.

基类：`BaseObject`

**构造** `__init__(self, obj, layer)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `color`：Property getter returns the RGB color of the text object as a tuple (Red, Green, Blue)
- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove(self)`

    Deletes label.
    Parameters:
        none
    Returns:
        None
    Examples:
        gl=op.find_graph()[0]
        label = gl.label('xb')
        label.remove()

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `Label`

This class represents an instance of a text object on a GLayer.

基类：`GObject`

**构造** `__init__(self, obj, layer)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `color`：Property getter returns the RGB color of the text object as a tuple (Red, Green, Blue)
- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove(self)`

    Deletes label.
    Parameters:
        none
    Returns:
        None
    Examples:
        gl=op.find_graph()[0]
        label = gl.label('xb')
        label.remove()

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `text`：Property getter for object text.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `Line`

This class represents an instance of a text object on a GLayer.

基类：`GObject`

**构造** `__init__(self, obj, layer)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `color`：Property getter returns the RGB color of the text object as a tuple (Red, Green, Blue)
- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove(self)`

    Deletes label.
    Parameters:
        none
    Returns:
        None
    Examples:
        gl=op.find_graph()[0]
        label = gl.label('xb')
        label.remove()

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `type`：
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
- 属性 `width`：

## `originpro.worksheet`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020, 2021, 2022 OriginLab Corporation


### class `WBook`

This class represents an Origin Workbook, it holds an instance of a PyOrigin WorksheetPage.

基类：`DBook`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

**方法** `add_sheet(self, name='', active=True)`

    add a new worksheet to the workbook

    Parameters:
        name (str): the name of the new sheet. If not specified, default names will be used
        active (bool): Activate the newly added sheet or not

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
**方法** `unembed_sheet(self, sheet)`

    unembeds and activates embedded graph sheet
    if graph was embedded in worksheet by Add Graph as Sheet, this
    unembeds the page and deletes the worksheet.

    Parameters:
        sheet (int or str): sheet index, or sheet name
    Returns:
        (None)

    Example:
        book = op.find_book('w','Book1')
        book.unembed_sheet(1)
        #book.unembed_sheet('Graph1') #can also use using sheet name

- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `WSheet`

This class represents an Origin Worksheet, it holds an instance of a PyOrigin Worksheet.

基类：`DSheet`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make layer/sheet active
    Parameters:
        none
    Returns:
        last_active layer index
    Examples:
        wks = op.find_sheet()
        wb = wks.get_book()
        wb.add_sheet()
        wks.activate()

**方法** `add_label(self, text, x=None, y=None)`

    Add a label to a layer.

    Parameters:
        text (str): The text of a text label
        x(float or None): The X coordinate of the left of the object
        y(float or None): The Y coordinate of the top of the object

    Returns:
        (Label)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        text = gl.add_label("hello", 4, 8)
        text.text = 'world'

**方法** `add_line(self, x1, y1, x2, y2)`

    Add a line to a layer.

    Parameters:
        x1(float or None): The begin X coordinate
        y1(float or None): The brgin Y coordinate
        x2(float or None): The end X coordinate
        y2(float or None): The end Y coordinate

    Returns:
        (Line)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        line = gl.add_line(5, 5, 6, 8)
        line.width = 5
        line.set_int('arrowendshape', 2)

**方法** `as_date(self, col, fmt)`

    set col as date format

    Parameters:
        col (int or str): If int, column index. If str, column name, short name first, then long name.
        fmt (int or str): can be custom format string, or date display option as int

    Returns:
        (None)

    Examples:
        wks=op.find_sheet()
        data = [1,2,3,4,5,6]
        wks.from_list(0, data)
        wks.as_date(0, "yyyy'Q'q")
    See Also:

**方法** `as_time(self, col, fmt)`

    set col as time format

    Parameters:
        col (int or str): If int, column index. If str, column name, short name first, then long name.
        fmt (int or str): can be custom format string, or time display option as int

    Returns:
        (None)

    Examples:
        wks=op.find_sheet()
        data = [1.1,2.2,3.3,4.4,5.5,6.6]
        wks.from_list(0, data)
        wks.as_time(0, "D:hh':'mm':'ss TT")
    See Also:

**方法** `cell(self, row, col)`

    It returns the contents of a worksheet cell as a string.

    Parameters:
        row (int): the row index.
        col (int, str): if int, it is the column index, otherwise the column name

    Returns:
        (str) the contents of a worksheet cell as a string.
    Examples:
        wks=op.find_sheet()
        ls = [1,2,3]
        wks.from_list(0,ls)
        nVal = wks.cell(0,0)
        print(nVal)

**方法** `clear(self, c1=0, ncols=0, c2=-1)`

    Clear data in worksheet

    Parameters:
        c1 (int or str): starting col, if int, column index. If str, column name, short name first, then long name.
        ncols(int): number of columns to clear if > 0, cannot specify togeher with c2
        c2 (int or str): ending col, if int, column index. If str, column name, short name first, then long name.

    Returns:
        (int): 0 for success, otherwise an internal error code

    Examples:
        wks.clear()#clear all
        wks.clear(1)#clear from 2nd column to the end
        wks.clear(1,2)#clear from 2nd and 3rd

- 属性 `cols`：get the last column index in worksheet, this is the same as shape[1]
**方法** `cols_axis(self, spec='', c1=0, c2=-1, repeat=True)`

    Set column plotting designations with a string pattern.

    Parameters:
        spec (str): A combination of 'x', 'y', 'z', etc letters
        c1 (int or str): Starting column to set
        c2 (int or str): Last column to set. c2 < 0 sets to last column
        repeat (bool): Repeat the last designation letter or not

    Returns:
        None

    Examples:
        wks.cols_axis('nxy') # 1st col none, 2nd=x, others=y.
        wks.cols_axis() # Clear designations from all columns.

- 属性 `comments`：Property getter returns long name of object.
**方法** `del_col(self, c1, nc=1)`

    Delete worksheet columns

    Parameters:
        c1 (int or str): Starting column to delete, <0 supported as from the end
        nc (int):      Number of columns to delete starting from c1
    Examples:
        wks.del_col(0)# del col A
        wks.del_col('C', 2)#del col C and D

**方法** `destroy(self)`

    delete the sheet/layer
    Parameters:
        none
    Returns:
        none
    Examples:
        wks1=op.new_sheet()
        wks1.destroy()

**方法** `from_df(*args, **kwargs)`
**方法** `from_dict(self, data, col=0, row=0)`

    Set a dictionary into a Worksheet. Keys are not used for any purpose.

    Parameters:
        data (dict): The data to set
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name
        row (int): Row index to start setting the data

    Returns:
        None

    Examples:
        data ={'aa': [1,2,3], 'bb':[4,5,6]}
        wks.from_dict(data)
        wks.from_dict(data,'C')

**方法** `from_file(self, fname, keep_DC=True, dctype='', sel='', sparks=False)`

    Imports data from a file using a Data Connector.

    Parameters:
        fname (str): File path and name to import.
        keep_DC (bool): Keep the Data Connector in the book after import
        dctype (str): Data Connector name, like "Import Filter", "MATLAB", "NetCDF", if not specified, CSV or Excel connector will be used based on file name
        sel (str): selection in the file, this will depend on the connector
        sparks (bool): Allows sparklines or not, True will follow GUI setting to add sparklines, False will disable it completely
    Returns:
        None

    Examples:
        wks=op.find_sheet()
        fn=op.path('e') + 'Samples\\Import and Export\donations.csv'
        wks.from_file(fn, False)#remove connector after import to allow further edit of data
        wks2=op.new_sheet()
        wks2.from_file(op.path()+'test.xlsx')#assuming you have this in UFF(user files folder)

**方法** `from_list(self, col, data, lname='', units='', comments='', axis='', start=0)`

    Sets a list object into an Origin column, optionally specifying long name, units ,comments label row values.

    Parameters:
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name
        data (list): data to put into column
        lname (str): Optional column long name
        units (str): Optional column units
        comments (str): Optional column comments
        axis (str): empty will not set, otherwise set column designation for plotting,
                    can be X,Y,Z, or N(None), E(Yerr), M(Xerr), L(label)
                    see https://www.originlab.com/doc/Origin-Help/WksCol-SetDesignation
        start(int): row offset
    Returns:
        None

    Examples:
        data = [1,2,3,4,5]
        wks.from_list(1, data)
        wks.from_list('Intensity', data, units='a. u.', axis='Y')
        wks.from_list(0, data, start=2)

**方法** `from_list2(self, data, row=0, col=0)`

    set a block of cells

    Parameters:
        data (list): a list of lists of values
        row (int): starting row index
        col (int or str): starting col, by index of by name

    Returns:
        (None)

    Examples:
        wks=op.find_sheet()
        #append a row to worksheet
        data = [ [10], [40] ]
        wks.from_list2(data, wks.rows)
    See Also:
        to_list2

**方法** `get_book(self)`

    Returns parent book of sheet.

    Parameters:

    Returns:
        (WBook)

    Examples:
        wks2 = wks.get_book().add_sheet('Result')

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_label(self, col, type='L')`

    Return a column label row text.

    Parameters:
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name
        type (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Returns:
        (str)

    Examples:
        wks=op.find_sheet()
        comments = wks.get_label(1,'C')

**方法** `get_labels(self, type_='L')`

    Return columns label row text.

    Parameters:
        type_ (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Returns:
        (list)

    Examples:
        wks=op.find_sheet()
        comments = wks.get_labels('C')

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `has_DC(self)`

    Returns whether a sheet has a Data Connector.

    Parameters:

    Returns:
        (str) name of the Data Connector, like 'csv', 'excel'

    Examples:
        dc = wb.has_DC()
        if len(dc):
            print(f'sheet is connected using {dc}')

**方法** `header_rows(self, spec='')`

    Controls which worksheet label rows to show, same as LabTalk wks.labels string.

    Parameters:
        spec (str): A combination of letters. See https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters

    Returns:
        None

    Examples:
        wks.header_rows('lu')# Show only long-name and unit.
        wks.header_rows()# Remove all label rows, keep only heading.

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `label(self, name)`

    Get a Label instance by name.

    Parameters:
        name (str): name of the label to be attached
    Returns:
        (Label)

    Examples:
        g = op.new_graph()
        g[0].label('XB').remove()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_col_index(self, col, convert_negative=False)`

    convert a 0-offset index to LabTalk index which is 1-offset

    Parameters:
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name, <0 supported as from the end

    Return:
        (int) 1-offset column index

    Examples:
        ii = wks.lt_col_index('Intensity')
        if ii < 1:
            print('no such column')

**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self, use_name=True)`

    Parameters:
        use_name(bool):
    Returns:
        Return the Origin Range String that identify Data Sheet object
    Examples:
        ws=op.find_sheet()
        print(ws.lt_range())

**方法** `merge_label(self, type_='L', unmerge=False)`

    merge or unmerge specified label row
    Parameters:
        type_(string):can be 'L' for longname, 'U' for Units, 'C' for comments
        unmerge(bool):false for merge, true for unmerge
    Returns:
        (None)
    Examples:
        wks=op.find_sheet()
        arrLName = ['longname','longname']
        wks.set_labels(arrLName)
        wks.merge_label()

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

**方法** `move_cols(self, n, c1, ncols=1)`

    moves a contiguous set of columns

    Parameters:
        n (int): by how many positions to move; if negative, columns are moved left,
                 otherwise right.
        c1 (int): the index of the first columns in the contiguous set.
        ncols (int): the total number of columns in the contiguous set.

    Returns:
        (bool)    returns True for success.

    Examples:
        wks=op.find_sheet()
        wks.move_cols(2, 1, 3)    # it moves three columns, beginning with the second column,
                                # by two positions right.
    See Also:

- 属性 `name`：short name of the object
**方法** `plot_cloneable(self, template)`

    Plots workbook data into a cloneable graph template

    Parameters:
        template (str): Cloneable graph template name.
    Returns:
        (None)
    Example:
        ws = op.new_book('w', hidden = False)[0]
        ws.from_file(op.path('e') + r'Samples\Statistics\Automobile.dat', True)
        ws.plot_cloneable('mytemplate')

**方法** `remove_DC(self)`

    Removes Data Connector from a sheet.

    Parameters:

    Returns:
        None

    Examples:
        wks.remove_DC()

**方法** `remove_label(self, label)`

    Remove a label from a layer.

    Parameters:
        label (Label or str): Instance of Label or name of label to remove

    Returns:
        None

    Examples:
        g = op.new_graph()
        g[0].remove_label('xb') # g[0] is 1st layer.

**方法** `report_table(*args, **kwargs)`
- 属性 `rows`：Get the last row index in worksheet with data, hidden rows has no effect on this
**方法** `set_cell_note(self, row, col, text)`

    create or update a cell's Note

    Parameters:
        row (int):          the row index.
        col (int, str):     if int, it is the column index, otherwise the column name
        text (str):         The cell note content
    Returns:
        (None)
    Examples:
        wks=op.find_sheet()
        wks.set_cell_note(0,0,'test cell note')

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_formula(self, col, formula)`

    set column formula
    Parameters:
        col (int or str): If int, column index. If str, column name, short name first, then long name.
        formula(str): column formula (Fx) to set.
    Example:
        wks = op.find_sheet()
        wks.set_formula('B', 'A+1')

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_label(self, col, val, type='L')`

    Set a column label row text.

    Parameters:
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name
        val (str): the text to set
        type (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Examples:
        wks=op.find_sheet()
        wks.set_label('A','long name for col A')
        wks.set_label(1, 'for col B, add user parameter if not there', 'Channel')

**方法** `set_labels(self, labels, type_='L', offset=0)`

    Set columns label row text.

    Parameters:
        labels (list): the text to set
        type_ (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Examples:
        wks=op.find_sheet()
        wks.set_labels(['long name for col A', 'long name for col B'], 'L')

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `shape`：Parameters:
- 属性 `show`：Property getter returns show state of object.
**方法** `sort(self, col, dec=False)`

    Sort worksheet data by a specified column

    Parameters:
        col (int or str): If int, column index (1-offset). If str, column name, short name first, then long name.
        dec (bool): Ascending(False) or Descending(True)

    Returns:
        (int): 0 for success, otherwise an internal error code

    Examples:
        wks.sort('A')#sort using 1st col, ascending
        wks.sort(0, True)#sort using 1st col, descending

- 属性 `tabcolor`：Parameters:
**方法** `to_col_range(self, col)`

    Make Column range string
    Parameters:
        col(int or str): If int, column index. If str, tries short name and if not exists, tries column long name
    Returns:
        XY range string
    Examples:
        wks=op.find_sheet()
        wks.cols=3
        strRange = wks.to_col_range(1)

**方法** `to_df(*args, **kwargs)`
**方法** `to_list(self, col)`

    Creates a list object from the data in an Origin column.

    Parameters:
        col (int or str): If int, column index. If str, tries short name and if not exists, tries column long name

    Returns:
        (list)

    Examples:
        data1 = wks.to_list(1)
        data2 = wks.to_list('Intensity')

**方法** `to_list2(self, r1=0, r2=-1, c1=0, c2=-1)`

    get a block of cells as a list of lists

    Parameters:
        r1 (int): beginning row index
        r2 (int): ending row index (inclusive), -1 to the end
        c1 (int): beginning column index
        c2 (int): ending column index (inclusive), -1 to the end

    Returns:
        (list) list of lists of results

    Examples:
        #copy 1st row and append to last row
        ll = wks.to_list2(0,0)
        wks.from_list2(ll,wks.rows)

**方法** `to_xy_range(self, colx, coly, colyerr, colxerr='')`

    Make XY range string from columns
    Parameters:
        colx, coly, colyerr, colxerr:type can be int or str, If int, column index. If str, tries short name and if not exists, tries column long name

    Returns:
        XY range string
    Examples:
        wks=op.find_sheet()
        wks.cols=3
        strRange = wks.to_xy_range(0,1,2)

- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

## `originpro.matrix`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `MBook`

This class represents an Origin Matrix Book, it holds an instance of a PyOrigin MatrixPage.

基类：`DBook`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

**方法** `add_sheet(self, name='', active=True)`

    add a new matrix sheet to the matrix book

    Parameters:
        name (str): the name of the new sheet. If not specified, default names will be used
        active (bool): Activate the newly added sheet or not

    Return:
        (MSheet)

    Examples:
        mb = ma.get_book().add_sheet('Dot Product')
        print(mb.shape)

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
**方法** `show_image(self, show=True)`

    similar to MSheet, but set all sheets in matrix book

    Parameters:
        show (bool): If True, show as images

    Returns:
        None

    Examples:
        mb = op.find_book('m', 'MBook1')
        mb.show_image()

- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `MSheet`

This class represents an Origin Matrix Sheet, it holds an instance of a PyOrigin MatrixSheet.

基类：`DSheet`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make layer/sheet active
    Parameters:
        none
    Returns:
        last_active layer index
    Examples:
        wks = op.find_sheet()
        wb = wks.get_book()
        wb.add_sheet()
        wks.activate()

**方法** `add_label(self, text, x=None, y=None)`

    Add a label to a layer.

    Parameters:
        text (str): The text of a text label
        x(float or None): The X coordinate of the left of the object
        y(float or None): The Y coordinate of the top of the object

    Returns:
        (Label)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        text = gl.add_label("hello", 4, 8)
        text.text = 'world'

**方法** `add_line(self, x1, y1, x2, y2)`

    Add a line to a layer.

    Parameters:
        x1(float or None): The begin X coordinate
        y1(float or None): The brgin Y coordinate
        x2(float or None): The end X coordinate
        y2(float or None): The end Y coordinate

    Returns:
        (Line)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        line = gl.add_line(5, 5, 6, 8)
        line.width = 5
        line.set_int('arrowendshape', 2)

- 属性 `comments`：Property getter returns long name of object.
- 属性 `depth`：Parameters:
**方法** `destroy(self)`

    delete the sheet/layer
    Parameters:
        none
    Returns:
        none
    Examples:
        wks1=op.new_sheet()
        wks1.destroy()

**方法** `from_file(self, fname, keep_DC=True, dctype='', sel='', sparks=False)`

    Imports data from a file using a Data Connector.

    Parameters:
        fname (str): File path and name to import.
        keep_DC (bool): Keep the Data Connector in the book after import
        dctype (str): Data Connector name, like "Import Filter", "MATLAB", "NetCDF", if not specified, CSV or Excel connector will be used based on file name
        sel (str): selection in the file, this will depend on the connector
        sparks (bool): Allows sparklines or not, True will follow GUI setting to add sparklines, False will disable it completely
    Returns:
        None

    Examples:
        wks=op.find_sheet()
        fn=op.path('e') + 'Samples\\Import and Export\donations.csv'
        wks.from_file(fn, False)#remove connector after import to allow further edit of data
        wks2=op.new_sheet()
        wks2.from_file(op.path()+'test.xlsx')#assuming you have this in UFF(user files folder)

**方法** `from_img(self, img)`

    Convert image to Matrix

    Parameters:
        img(IPage): input image page
    Returns:
        None
    Examples:
        ms = op.find_sheet('m')
        img = op.find_image('Image1')
        ms.from_img(img)

**方法** `from_np(self, arr, dstack=False, mv=None)`

    Set a matrix sheet data from a multi-dimensional numpy array. Existing data and MatrixObjects will be deleted.

    Parameters:
        arr (numpy array): 2D for a single MatrixObject, and 3D for multiple MatrixObjects (rows, cols, N)
        dstack (bool):   True if arr as row,col,depth, False if depth,row,col
        mv(float, int): if specified, to set the internal missing value for each MatrixObject. This is needed when arr contains nan and not double type
    Returns:
        None

    Examples:
        ms = op.new_sheet('m')
        arr = np.array([[[1, 2, 3], [4, 5, 6]], [[11, 12, 13], [14, 15, 16]]])
        ms.from_np(arr)

**方法** `from_np2d(self, arr, index=0)`

    Transfers data from a numpy 2D array into a single MatrixObject.

    Parameters:
        arr (numpy array) 2D
        index (int): MatrixObject index in the MatrixLayer

    Returns:
        None

    Examples:
        index = 0
        ms = op.find_sheet('m')         # a matrix must be active
        npdata = ms.to_np2d(index)      # get as numpy array the data from one matrix object
        npdata *= 10                    # multiply every element by 10
        ms.from_np2d(npdata, index)     # set the modified array into the matrix object

**方法** `get_book(self)`

    Returns parent book of sheet.

    Parameters:

    Returns:
        (MBook)

    Examples:
        mb = ma.get_book().add_sheet()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_label(self, index, type_='L')`

    Return a Matrix object label text.

    Parameters:
        index (int ): Matrix object index or 'x', 'y' for sheet XY labels
        type_ (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Returns:
        (str)

    Examples:
        ms=op.find_sheet('m')
        comment = ms.get_label('y','C')

**方法** `get_labels(self, type_='L')`

    Return Matrix Objects label text.

    Parameters:
        type_ (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name

    Returns:
        (list)

    Examples:
        ms=op.find_sheet('M')
        comments = ms.get_labels('C')

**方法** `get_missing_value(self, index=0)`

    get the internal missing value, which is needed when data type is not double.
    Parameters:
        index(int): matrix object index
    Returns:
        (float) missing value
    Examples:
        ms=op.find_sheet('m')
        print(ms.get_missing_value())

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `has_DC(self)`

    Returns whether a sheet has a Data Connector.

    Parameters:

    Returns:
        (str) name of the Data Connector, like 'csv', 'excel'

    Examples:
        dc = wb.has_DC()
        if len(dc):
            print(f'sheet is connected using {dc}')

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `label(self, name)`

    Get a Label instance by name.

    Parameters:
        name (str): name of the label to be attached
    Returns:
        (Label)

    Examples:
        g = op.new_graph()
        g[0].label('XB').remove()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self, use_name=True)`

    Parameters:
        use_name(bool):
    Returns:
        Return the Origin Range String that identify Data Sheet object
    Examples:
        ws=op.find_sheet()
        print(ws.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove_DC(self)`

    Removes Data Connector from a sheet.

    Parameters:

    Returns:
        None

    Examples:
        wks.remove_DC()

**方法** `remove_label(self, label)`

    Remove a label from a layer.

    Parameters:
        label (Label or str): Instance of Label or name of label to remove

    Returns:
        None

    Examples:
        g = op.new_graph()
        g[0].remove_label('xb') # g[0] is 1st layer.

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_label(self, index, val, type_='L')`

    Set Matrix object label text.

    Parameters:
        index (int): Matrix object index or 'x', 'y' for sheet XY labels
        val   (list): the text to set
        type_  (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name
    Returns:
        none
    Examples:
        ms=op.find_sheet('m')
        ms.set_label('y', 'Lattitude')

**方法** `set_labels(self, labels, type_='L', offset=0)`

    Set Matrix objects label text.

    Parameters:
        labels (list): the text to set
        type_ (str): A column label row character (see https://www.originlab.com/doc/LabTalk/ref/Column-Label-Row-Characters) or a user defined parameter name
    Returns:
        none
    Examples:
        ms=op.find_sheet('m')
        ms.set_labels(['long name for col A', 'long name for col B'], 'L')

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `shape`：Parameters:
- 属性 `show`：Property getter returns show state of object.
**方法** `show_image(self, show=True)`

    Show MatrixObjects as images or as numeric values.

    Parameters:
        show (bool): If True, show as images

    Returns:
        None

    Examples:
        ms.show_image()
        ms.show_image(False)

**方法** `show_slider(self, show=True)`

    Show image slider for MatrixObjects.

    Parameters:
        show (bool): If True, show slider

    Returns:
        None

    Examples:
        mat.show_slider()
        mat.show_slider(False)

**方法** `show_thumbnails(self, show=True)`

    Show thumbnail images for a MatrixObjects.

    Parameters:
        show (bool): If True, show thumbnails

    Returns:
        None

    Examples:
        ms.show_thumbnails()
        ms.show_thumbnails(False)

- 属性 `tabcolor`：Parameters:
**方法** `to_np2d(self, index=0, order='C')`

    Transfers data from a single MatrixObject to a numpy 2D array.

    Parameters:
        index (int): MatrixObject index in the MatrixLayer
        order (str): Order of numpy array. 'C' for C-style row major order, 'F' for Fortran-style column major order

    Returns:
        (numpy array) 2D

    Examples:
        arr = ms.to_np2d(0)
        print(arr)
        arr = ms.to_np2d(0, 'R')
        print(arr)

**方法** `to_np3d(self, dstack=False, order='C')`

    Transfers data from a MatrixSheet to a numpy 3D array.

    Parameters:
        dstack (bool): True output arrays as row,col,depth, False if depth,row,col
        order (str): Order of numpy array. 'C' for C-style row major order, 'F' for Fortran-style column major order

    Returns:
        (numpy array) 3D

    Examples:
        arr=[]
        for i in range(10):
            tmp = np.arange(1,13).reshape(3,4)
            arr.append(tmp*(i+1))
        aa = np.dstack(arr)
        print(aa.shape)
        ma = op.new_sheet('m')
        ma.from_np(aa, True)

        bb = ma.to_np3d()
        print(bb.shape)
        mb = op.new_sheet('m')
        mb.from_np(bb)

        cc = ma.to_np3d(True)
        print(cc.shape)
        mc = op.new_sheet('m')
        mc.from_np(cc)
        mc.show_thumbnails()

- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
- 属性 `xymap`：Get Matrix xy values.

## `originpro.graph`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `Axis`

This class represents an instance of Axis on a GLayer.

**构造** `__init__(self, obj, ax)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `limits`：axis scale limits
- 属性 `scale`：get axis scale type
**方法** `set_limits(self, begin=None, end=None, step=None)`

    Sets scale from and to values for the axis

    Parameters:
        begin (float, tuple, list): The From value of limits, or specify [begin,end], or [begin,end,step]
        end (float): The To value of limits. None leaves the value unchanged.
        step (float): The Increment of the limits. None leaves the value unchanged.

    Returns:
        (tuple) from, to, increment

    Examples:
        ax.set_limits(step=0.3)
        ax.set_limits(5, 15)

- 属性 `sfrom`：get scale limit from value
- 属性 `sstep`：get scale limit increment
- 属性 `sto`：get scale limit to value
- 属性 `title`：Property getter for axis title.
**函数** `CopyPageRatio(ratio)`

    temporarily change System.copyPage.ratio
    Parameters:
        ratio(float):ratio when copy page
    Returns:
        (none)
    Examples:
        import originpro as op
        with op.CopyPageRatio(50) as cpr:
            print('set System.copyPage.ratio to',op.lt_int('System.copyPage.ratio'))
        print('set System.copyPage.ratio back to',op.lt_int('System.copyPage.ratio'))


### class `GLayer`

This class represents an Origin Graph Layer, it holds an instance of a PyOrigin GraphLAyer

基类：`BaseLayer`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make layer/sheet active
    Parameters:
        none
    Returns:
        last_active layer index
    Examples:
        wks = op.find_sheet()
        wb = wks.get_book()
        wb.add_sheet()
        wks.activate()

**方法** `add_label(self, text, x=None, y=None)`

    Add a label to a layer.

    Parameters:
        text (str): The text of a text label
        x(float or None): The X coordinate of the left of the object
        y(float or None): The Y coordinate of the top of the object

    Returns:
        (Label)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        text = gl.add_label("hello", 4, 8)
        text.text = 'world'

**方法** `add_line(self, x1, y1, x2, y2)`

    Add a line to a layer.

    Parameters:
        x1(float or None): The begin X coordinate
        y1(float or None): The brgin Y coordinate
        x2(float or None): The end X coordinate
        y2(float or None): The end Y coordinate

    Returns:
        (Line)

    Examples:
        gp = op.new_graph()
        gl = gp[0]
        line = gl.add_line(5, 5, 6, 8)
        line.width = 5
        line.set_int('arrowendshape', 2)

**方法** `add_mplot(self, ms, z, x=-1, y=-1, cm=-1, type=103)`

    plot a 3D parametric surface

    Parameters:
        ms (MSheet): matrix sheet with the data to plot
        z (int): matrix object index for Z
        x (int): matrix object index for X, must be > z
        y (int): matrix object index for Y, must be > z

    Examples:
        #assmues X,Y,Z contains the mesh grid data
        data=[]
        data.append(Z)
        data.append(X)
        data.append(Y)
        ms = op.new_sheet('m')
        ms.from_np(np.array(data))
        gl = op.new_graph(template='GLparafunc')[0]
        gl.add_mplot(ms, 0, 1, 2)

**方法** `add_plot(self, obj, coly=-1, colx=-1, colz=-1, type='?', colyerr=-1, colxerr=-1)`

    Add plot to graph layer
    Parameters:
        obj(WSheet): worksheet to plot from, or a DataRange
        coly(int or str): Y column to plot
        colx(int or str): X column, it not specified, X column on the left, can use '#' to indicate use row number as X
        colz(int or str): Z column to plot
        type(str): 'l'(Line Plot) 's'(Scatter Plot) 'y' (Line Symbols) 'c' (Column) '?' auto(template)
        colyerr(int or str): Y Error column to plot
        colxerr(int or str): X Error column to plot
    Returns:
        (Plot): the newly added Plot object

    Examples:
        gl = op.find_graph()[0]
        wks = op.find_sheet('w','Book1')
        p = gl.add_plot(wks,'C')
        p.color = '#5f0'
        gl.rescale()
        gl.add_plot(wks,1,3)#C(x), B(y)
        gl.add_plot(wks,1,'#')#B(y) vs Row Numbers

**方法** `axis(self, ax)`

    Creates a new Axis object

    Parameters:
        ax (str): One of 'x', 'y', or 'z'

    Returns:
        (Axis)

    Examples:
        ax = lay.axis('x')

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    delete the sheet/layer
    Parameters:
        none
    Returns:
        none
    Examples:
        wks1=op.new_sheet()
        wks1.destroy()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `group(self, group=True, begin=-1, end=-1)`

    Group/Ungroup data plots

    Parameters:
        begin(int): plot index, -1 is the same as 0
        end(int): -1 to the last, otherwise ending plot index (0-offset)
    Returns:
        None
    Examples:
        graph = op.new_graph(template='scatter')
        gl=graph[0]
        plot = gl.add_plot('[Book1]1!(A,B:C)', type='s')
        gl.group(True,0,1)
        plot = gl.add_plot('[Book1]1!(A,D:0)', type='l')
        gl.group(True,2,3)

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `label(self, name)`

    Get a Label instance by name.

    Parameters:
        name (str): name of the label to be attached
    Returns:
        (Label)

    Examples:
        g = op.new_graph()
        g[0].label('XB').remove()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Return the Origin Range String that identify Graph Layer object
    Parameters:
        none
    Returns:
        Origin Range String
    Examples:
        gl=op.find_graph()[0]
        print(gl.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `plot_list(self)`

    Returns list of Plot objects in the layer.

    Parameters:

    Returns:
        (list)

    Examples:
        items = lay.plot_list()
        item = lay.plot_list()[0]

**方法** `remove(self, obj: <built-in function any>)`

    remove object in the layer.

    Parameters:
        obj: Can be graph object or plot object

    Returns:
        None

    Examples:
        gl=op.find_graph()[0]
        label = gl.label('xb')
        label.remove()

**方法** `remove_label(self, label)`

    Remove a label from a layer.

    Parameters:
        label (Label or str): Instance of Label or name of label to remove

    Returns:
        None

    Examples:
        g = op.new_graph()
        g[0].remove_label('xb') # g[0] is 1st layer.

**方法** `remove_plot(self, plot)`

    Removes plot from layer.

    Parameters:
        plot (Plot or int) Instance of Plot or index of plot to remove

    Returns:
        None

    Examples:
        lay.remove_plot(3)

**方法** `rescale(self, skip='')`

    update limits to show all the data, including color scale range is colormap is used

    Parameters:
        skip(str): axis to skip(keep limits). Can be a combination of x,y,z,m where m is for colormap

    Returns:
        None

    Examples:
        gl=op.find_graph()[0]
        gl.rescale('x')#rescale Y only
        gl.rescale('m')#do not change colormap scale range

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

**方法** `set_xlim(self, begin=None, end=None, step=None)`

    Sets X axis scale begin(From), end(To) and step(Increment)

    Parameters:
        begin (float or None): axis new From or Begin value.
        end (float or None): axis new To or End value.
        step (float or None): axis new Step or Increment value.

    Returns:
        New axis limits

    Examples:
        g = op.new_graph()
        g[0].set_xlim(0, 1)
        g[0].set_xlim(step=0.2)

**方法** `set_ylim(self, begin=None, end=None, step=None)`

    Sets Y axis scale begin(From), end(To) and step(Increment)

    Parameters:
        begin (float or None): axis new From or Begin value.
        end (float or None): axis new To or End value.
        step (float or None): axis new Step or Increment value.

    Returns:
        New axis limits

    Examples:
        g = op.new_graph()
        g[0].set_ylim(1, 100, 20)
        g[0].set_ylim(begin=0)

**方法** `set_zlim(self, begin=None, end=None, step=None)`

    Sets Z axis scale begin(From), end(To) and step(Increment)

    Parameters:
        begin (float or None): axis new From or Begin value.
        end (float or None): axis new To or End value.
        step (float or None): axis new Step or Increment value.

    Returns:
        New axis limits

    Examples:
        g = op.new_graph()
        g[0].set_zlim(0, 5)
        g[0].set_zlim(step=1)

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
- 属性 `xlim`：Property getter for X axis limits.
- 属性 `xscale`：Property getter for X axis scale type.
- 属性 `ylim`：Property getter for Y axis limits.
- 属性 `yscale`：Property getter for Y axis scale type.
- 属性 `zlim`：Property getter for Z axis limits.
- 属性 `zscale`：Property getter for Z axis scale type.

### class `GPage`

This class represent an Origin Graph Page, it holds an instance of a PyOrigin GraphPage

基类：`BasePage`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

**方法** `add_layer(self, type=0)`

    Adds a new layer to GPage. Type is based on types specified here:https://www.originlab.com/doc/X-Function/ref/layadd
    but should use the index equivalent of listed types (e.g. `righty` would be 2)

    Parameters:
        type (int): Type of layer to add. See description above foir how to deduce

    Returns:
        (GLayer): the newly added graph layer

    Examples:
        g = op.find_graph('graph1')
        gl=g.add_layer(2) # righty
        gl.xlim=[-2,1]

- 属性 `comments`：Property getter returns long name of object.
**方法** `copy_page(self, fmt, res=300, ratio=100, tb=False)`

    Copy Graph Page as OLE object or Image

    Parameters:
        fmt (str): Image Format, can be PNG, EMF, DIB, HTML, JPG, or OLE
        res (int): DPI
        ratio (int): Size Factor (%)
        tb (bool): Background Transparency, for PNG only

    Returns:
        None
    examples:
        gl = op.find_graph('graph1')
        gl.copy_page('png', 600,100, True)

**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `save_fig(self, path='', type='auto', replace=True, width=0, ratio=0)`

    export to a file

    Parameters:
    -------
    path(str): if not specified, then to UFF, or if graph has theme, then last exported location in that graph.
                If specifed, can include file name with extention, which will then control image type
    type(str): if auto, then use graph last exported settings, otherwise 'png', 'emf' etc
    replace(bool): if file existed, silently replace or not
    width(int): Pixcels. 0 will use last exported setting only if type=auto, if not auto, better specify this.
    ratio (int): Size Factor (%), for emf and svg

    Return:
    -------
        if success, returns the fullpath file name generated, otherwise an empty string

    Examples
    -------
    >>> g = op.find_graph('graph1')
    >>> g.save_fig(op.path() + 'test1.png', width=500)
    >>> g.save_fig()#use last GUI export graph settings remembered inside graph, which may include path

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

### class `Plot`

This class represents an instance of a data plot in a GLayer.

基类：`BaseObject`

**构造** `__init__(self, obj, layer)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `change_data(self, wks, **kwargs)`

    change the data source for an existing data plot

    Parameters:
        wks (WSheet): the worksheet to use
        kwargs : columns and the corresponding axis
    Returns:
        None
    Examples:
        wks = op.find_sheet('w', 'Book1')
        gl = op.find_graph('Graph1')[0]
        dp = gl.plot_list()[0]
        dp.change_data(wks, x='C', y='D')

- 属性 `color`：returns the RGB color of the plot object as a tuple (Red, Green, Blue)
- 属性 `colorinc`：returns the color increment of the grouped plot object
- 属性 `colormap`：Returns the colormap name a string
- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

- 属性 `group`：Check if data plot in group or not.
**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Return the Origin Range String that identify Data Plot object
    Parameters:
        none
    Returns:
        Origin Range String
    Examples:
        gl=op.find_graph()[0]
        p=gl.plot_list()[0]
        print(p.lt_range())

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `remove(self)`

    Deletes plot.
    Parameters:
        none
    Returns:
        None
    Examples:
        gl=op.find_graph()[0]
        p = gl.plot_list()[0]
        p.remove()

**方法** `set_cmd(self, *args)`

    Execute labtalk set command for this data plot

    Parameters:
        args: set command options
    Returns:
        none
    Examples:
        wks = op.find_sheet('w', 'Book1')
        gl = op.find_graph('Graph1')[0]
        dp = gl.add_plot(wks, 1, 0)
        dp.set_cmd('-c 2', '-d 2') # line color as red, style as dot

**方法** `set_fill_area(self, above=-1, type=9, below=-1)`

    For line plots only, to set Fill Area Under curve option

    Parameters:
        above (int): fill color of "Pattern Above" (or "Pattern")
        type (int): fill area option, 9=Fill to next data plot – above below colors,  see https://www.originlab.com/doc/LabTalk/ref/Set-cmd#Specifying_Pattern
        below (int): fill color of "Pattern Below"


    Returns:
        none
    Examples:
        gl=op.find_graph()[0]
        p=gl.plot_list()[0]
        p.set_fill_area(2, 9, 3)

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_shapelist(self, name)`

    Set the shape list of the plot object

    Parameters:
        Shape list, can be theme file name, or integer list

    Returns:
        None

    Examples:
        p = g[0].add_plot(wks,'(0,1)')
        p.shapelist = 'Symbol Type Square and Circle' # theme file
        p.shapelist = [3, 2, 1]

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `shapelist`：The type of the None singleton.
- 属性 `show`：Property getter returns show state of object.
- 属性 `symbol_interior`：returns the symbol interior type. 0 = no symbol, 1=solid, 2=open, 3=dot center
- 属性 `symbol_kind`：returns the symbol shape, see the LabTalk get %C -k command
- 属性 `symbol_kindinc`：returns the symbol shape increment of the grouped plot object
- 属性 `symbol_size`：returns the symbol size, see the Labtalk get %C -z command
- 属性 `symbol_sizefactor`：returns the symbol size factor, 1 if not changing. This is useful when size is controlled by a worksheet column
- 属性 `transparency`：returns the plot's line or symbol transparency in percent
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
- 属性 `zlevels`：Returns the information about z-levels as a dictionary

## `originpro.analysis`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2021 OriginLab Corporation


### class `LinearFit`

class for performing Linear Fitting with Origin's internal fitting engine

**构造** `__init__(self)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `fix_intercept(self, val)`

    fix intercept to a value
    Parameters:
        val(float): intercept value
    Returns:
        none
    Examples:
        lr=op.LinearFit()
        lr.fix_intercept=0.6

**方法** `fix_slope(self, val)`

    fix slope to a value
    Parameters:
        val(float): slope value
    Returns:
        none
    Examples:
        lr=op.LinearFit()
        lr.fix_slope=0.6

**方法** `report(self, band=0)`

    perform the fitting and generate the report. You need to end the fitting by either calling result or report

    Parameters:
        band (int): confidence and prediction bands. 0=none,1=confidence,2=prediction,3=both

    Returns:
        (tuple): range strings of the report sheet and the fitted curves

    Examples:
        lr = op.LinearFit()
        lr.set_data(wks, 1, 2)
        r, c = lr.report(1)
        wReport=op.find_sheet('w', r)
        wCurves=op.find_sheet('w', c)

**方法** `result(self)`

    perform the fitting and return the parameters. You need to end the fitting by either calling result or report

    Return:
        (dict) fitting parameters and statistics from the fit

    Examples:
        lr = op.LinearFit()
        lr.set_data(wks, 1, 2)
        rr = lr.result()
        b       =rr['Parameters']['Slope']['Value']
        b_err   =rr['Parameters']['Slope']['Error']

**方法** `set_data(self, wks, x, y, err='')`

    set the XY data with optional error bar column
    Parameters:
        wks(worksheet):
        x,y(int or string):column index or name
        err(int or string):column index or name
    Returns:
        none
    Examples:
        lr = op.LinearFit()
        wks=op.find_sheet()
        lr.set_data(wks, 1, 2)


### class `NLFit`

class for performing Non-Linear Curve Fitting with Origin's internal fitting engine
The name of the fitting function already defined inside Origin must be provided to use this class

**构造** `__init__(self, func, method='auto')`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `fit(self, iter='')`

    iterate the fitting engine

    Parameters:
        iter (str or int): empty will iterate until converge, otherwise to specify the number of iterations
    Returns:
        none
    Examples:
        model = op.NLFit('Gauss')
        wks=op.find_sheet()
        model.set_data(wks, 0, 1)
        model.param_box()
        model.fit()

**方法** `fix_param(self, p, val)`

    fix a parameter to a value or to turn off the fixing

    Parameters:
        p(str): name of a parameter
        val(bool or float): use False to turn off parameter fixing, or specify a value to fix it to
    Returns:
        none
    Examples:
        model.fix_param('y0', 0)
        model.fix_param('xc', False)

**方法** `param_box(self)`

    open a modal dialog box to control fitting parameters and iterations.
    You can click the minimize button on the parameters dialog to manipulate the graph like zooming in, or use
    screen reader etc. Must still call fit() after.
    Parameters:
        none
    Returns:
        none
    Examples:
        model = op.NLFit('Gauss')
        wks=op.find_sheet()
        model.set_data(wks, 0, 1)
        model.param_box()

**方法** `report(self, autoupdate=False)`

    you need to end the fitting by either calling result or report
    Parameters:
        autoupdate(bool): setup recalculation on the report or not

    Returns:
        (tuple): range strings of the report sheet and the fitted curves

    Example:
        model.fit()
        r, c = model.report()
        Report=op.find_sheet('w', r)
        Curves=op.find_sheet('w', c)
        print(Report)
        print(Curves.shape)

**方法** `result(self)`

    you need to end the fitting by either calling result or report. If you need both, you need to call report first.
    Parameters:
        none
    Return:
        (dict) fitting parameters and statistics from the fit
    Examples:
        model = op.NLFit('Gauss')
        wks=op.find_sheet()
        model.set_data(wks, 0, 1)
        model.param_box()
        model.fit()

**方法** `set_data(self, wks, x, y, yerr='', xerr='', z='')`

    set the XY data with optional error bar column, or XYZ data
    Parameters:
        wks(worksheet):
        x,y(int or string):column index or name
        yerr,xerr,z(int or string):column index or name
    Returns:
        none
    Examples:
        model=op.NLFit('Gauss')
        wks=op.find_sheet()
        model.set_data(wks, 0, 1, xerr='D' )

**方法** `set_lbound(self, p, ctrl='>', val=None)`
**方法** `set_mdata(self, ms, z)`

    set the Matrix data
    Parameters:
        ms(matrix sheet):
        z(int or string):matrix object index or long name
    Returns:
        none
    Examples:
        aa = np.array([ [1, 2, 3.9], [4.1, 5, 6], [7, 8.5, 9] ])
        ma=op.new_sheet('m')
        ma.from_np(aa)
        model = op.NLFit('Plane')
        model.set_mdata(ma,1)

**方法** `set_param(self, p, val)`

    set a parameter value before fitting
    Parameters:
        p(str): name of a parameter
        val(float): value for the parameter
    Returns:
        none
    Examples:
        model.set_param('xc', 0.5)

**方法** `set_range(self, rg)`

    set data as range string
    Parameters:
        rg(string): range string
    Returns:
        none
    Examples:
        gl=op.find_graph()[0]
        dp=gl.plot_list()[0]
        model=op.NLFit('Lorentz')
        model.set_range(dp.lt_range())
        model.fit()

**方法** `set_ubound(self, p, ctrl='<', val=None)`

## `originpro.image`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2021 OriginLab Corporation


### class `IPage`

This class represents an Origin Image Window, it holds an instance of a PyOrigin ImagePage

基类：`BasePage`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `activate(self)`

    make page active
    Parameters:
        none
    Returns:
        none
    Examples:
        wb = op.find_book('w', 'Book2')
        wb.activate()

- 属性 `channels`：Parameters:
- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy the window
    Parameters:
        none
    Returns:
        none
    Examples:
        wb=op.new_book()
        wb.destroy()

**方法** `duplicate(self)`

    duplicate the window
    Parameters:
        none
    Returns:
        the newly created window object
    Examples:
        wb=op.new_book()
        wbDuplicate=wb.duplicate()

- 属性 `frames`：Parameters:
**方法** `from_file(self, fname)`

    load image(s) into the image window

    Parameters:
        fname(str): file path to an image file or with wildcard to a group of image files to be loaded into an image stack

    Returns:
        success of failure

    Examples:
        im = op.find_image('Image1')
        folder = op.path('e') + r'Samples\Image Processing and Analysis'
        fn = folder + r'\Flower.jpg'
        im.from_file(fn)
        #load image stack simply by wildcard
        im2 = op.find_image('Image2')
        fn = folder + r'\*.tif'
        im2.from_file(fn)

        import originpro as op
        url = r'https://download.osgeo.org/geotiff/samples/gdal_eg/cea.tif'
        iw=op.new_image()
        iw.from_file(url)

**方法** `from_np(self, arr, dstack=False)`

    Set an Image page data from a multi-dimensional numpy array.

    Parameters:
        arr (numpy array):
        dstack (bool):  True if arr as row,col,frames, False if frames,row,col

    Returns:
        None

    Notes:
        It must first call setup() method to initialize the image window

    Examples:
        img = op.new_image()
        data = np.array([[[1.0, 2.0],[3.0, 4.0]],[[5.0, 6.0],[7.0, 8.0]],[[9.0, 10.0],[11.0, 12.0]]])
        #print(data.shape)
        img.setup(1, True, 0)
        img.from_np(data, False)

**方法** `from_np2d(self, arr, frame)`

    Transfers data from a 2D numpy array into one frame of an ImagePage.
    The image must be multiframe, otherwise nothing is returned.
    The size (width, height) of the supplied data must match the size of the image.

    Parameters:
        frame (int) the index of the image frame

    Returns:
        (bool) success or failure

    Examples:
        im2=iw.to_np2d(1)
        im2*=10
        iw.from_np2d(im2,2)

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

**方法** `is_active(self)`

    Returns whether book is currently active
    Parameters:
        none
    Returns:
        bool that indicate if the book is active
    Examples:
        wb=op.new_book()
        print(wb.is_active())

**方法** `is_open(self)`

    Returns whether book is neither hidden, nor minimized.

    Parameters:

    Returns:
        (bool)

    Examples:
        b = wb.is_open()

- 属性 `layer`：Parameters:
- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `lt_range(self)`

    Parameters:
        none
    Returns:
        return the Origin Range String that iddentify page object
    Examples:
        wb=op.new_book()
        print(wb.lt_range())

**方法** `merge(self)`

    merge a image with 3 or 4 frames in Image Window to a single image
    Parameters:
        none
    Returns:
        none
    Examples:
        img=op.find_image()#you should use imgstack.xfc to prepare a image with 3 or 4 frames first
        img.merge()

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `rgb2gray(self)`

    convert image window to grayscale
    Parameters:
        none
    Returns:
        none
    Examples:
        img=op.new_image()
        fn=op.path('e') + r'Samples\Image Processing and Analysis\Flower.jpg'
        img.from_file(fn)
        img.rgb2gray()

**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

**方法** `setup(self, channels, multiframe, channelType=-1)`

    It allows simple initialization by specifying the number of channels
    and whether it should be multiframe or not. The existing image
    held in the object (if present) is wiped out.

    Parameters:
        channels(int): the number of channels (1, 3 or 4).
        multiframe(bool): whethwer it should be multiframe (Image Stack) or not.
        channelType (int, optional): the variable type of the channel.
                                    Possible values are:
                                        0 : float64
                                        1 : float32
                                        8 : uint16
                                    For all the other values the channel size will be set
                                    to uint8.

    Returns (bool): success or not

    Examples:
        img = op.new_image()
        data = np.array([[[1.0, 2.0],[3.0, 4.0]],[[5.0, 6.0],[7.0, 8.0]],[[9.0, 10.0],[11.0, 12.0]]])
        #print(data.shape)
        img.setup(1, True, 0)
        img.from_np(data, False)

- 属性 `show`：Property getter returns show state of object.
- 属性 `size`：width and height of the image
**方法** `split(self)`

    split a color image into RGB channels
    Parameters:
        none
    Returns:
        none
    Examples:
        img=op.new_image()
        fn=op.path('e') + r'Samples\Image Processing and Analysis\Flower.jpg'
        img.from_file(fn)
        img.split()

**方法** `to_np(self)`

    Transfers data from an ImagePage to a numpy array.

    Parameters:

    Returns:
        (numpy array)

    Examples:
        npimg = im.to_np()

**方法** `to_np2d(self, frame)`

    Transfers data from one frame of an ImagePage to a 2D numpy array.
    The image must be multiframe, otherwise nothing is returned.

    Parameters:
        frame (int) the index of the image frame

    Returns:
        (numpy array)

    Examples:
        im2=iw.to_np2d(1)

- 属性 `type`：Parameters:
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree

## `originpro.notes`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `Notes`

Origin Notes Window

基类：`BaseObject`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `append(self, text, newline=True)`

    Append text to Notes window.

    Parameters:
        text (str): Text to append.
        newline (bool): Add new line character if true.
    Returns:
        None

    Examples:
        nt.append('hello world')

- 属性 `comments`：Property getter returns long name of object.
**方法** `destroy(self)`

    Destroy Notes window.

    Parameters:

    Returns:
        None

    Examples:
        nt.destroy()

**方法** `exp_html(self, fname)`

    Export Notes window as HTML files.

    Parameters:
        fname (str): Output HTML file name.
    Returns:
        Error code, 0 for success.

    Examples:
        nt.exp_html('D:/hello.html')

**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `load(self, fname, askreplace=False)`

    Load file into Notes window.

    Parameters:
        fname (str): Input file full path.
        askreplace (bool): Ask if replace current content if True
    Returns:
        Error code, 0 for success.

    Examples:
        nt.load('D:/hello.html')

**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `syntax`：Get Notes syntax
- 属性 `text`：Get Notes window text
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
- 属性 `view`：Get Notes view mode

## `originpro.project`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation

**函数** `find_book(type='w', name='') -> Union[originpro.worksheet.WBook, originpro.matrix.MBook]`

    Find the work or matrixbook by name (short name) and return a WBook or MBook object.

    Parameters:
        type (str): Specify 'w' for WBook object or 'm' for MBook object
        name (str or int): Name of book. If empty, then active book. If int, then from the collection of books by index

    Returns:
        (WBook or MBook or None)

    Examples:
        wb = op.find_book()#if active book is a workbook
        mb = op.find_book('m', 'MBook2')

**函数** `find_graph(name='') -> originpro.graph.GPage`

    Find the named graph (short name) and return a GPage object.

    Parameters:
        name (str or int) Name of graph. If empty, then active graph, if int, then index into graph page collection

    Returns:
        (GPage or None)

    Examples:
        g = op.find_graph('Graph2')
        glayer=op.find_graph()[0]

**函数** `find_image(name='') -> originpro.image.IPage`

    Find the named Image Window and return a IPage object.

    Parameters:
        name (str or int) Name of Image Window. If empty, then active Image Page, int, then index into Image Page collection

    Returns:
        (IPage or None)

    Examples:
        import numpy as np
        im = op.find_image('Image1')
        data = im.to_np()
        dataUpsideDown = np.flip(data, 1)
        im.from_np(dataUpsideDown)

**函数** `find_notes(name='') -> originpro.notes.Notes`

    Find the named Notes Window and return a Notes object.

    Parameters:
        name (str) Name of Image window. If empty, then active Notes window.

    Returns:
        (Notes or None)

    Examples:
        nt1 = op.find_notes('Notes')
        nt2 = op.find_notes()

**函数** `find_sheet(type='w', ref='') -> Union[originpro.worksheet.WSheet, originpro.matrix.MSheet]`

    Find the Sheet referenced by ref (an Origin range string). Default will return active worksheet.

    Parameters:
        type (str): Specify 'w' for WBook object or 'm' for MBook object
        ref (str or int): [book]sheet, an Origin range specification. Can also be just book name to assume active sheet,
                    so the following are the same if book has only one sheet
                    '[book1]1', '[book1]1!', 'book1'

                    You may also pass in an integer for the book index, like 0 for the first book

    Returns:
        (WSheet or MSheet or None)

    Examples:
        wks1 = op.find_sheet()   #when active book that is a workbook
        wks2 = op.find_sheet('w', '[Book1]Sheet2')   #when you need a specific sheet
        m1 = op.find_sheet('m')   #when active is a matrix book
        m2 = op.find_sheet('m','MBook1')   #when there is only one sheet, use simpler notation
        wks3 = op.find_sheet('w',0)# see if there is any workbook at all

**函数** `get_page(type, index=0) -> Union[originpro.worksheet.WBook, originpro.matrix.MBook, originpro.graph.GPage, originpro.image.IPage]`

    get WBook, MBook, GPage, IPage by index
    Parameters:
        none
    Returns:
        WBook or MBook or GPage or IPage None
    Examples:
        w=op.get_page('w', 0)//there should a workbook exist

**函数** `graph_list(select='f', inc_embed=False) -> List[originpro.graph.GPage]`

    Returns a list object of GPages representing graphs in the current folder, graphs open in current folder, or graphs in project.

     Parameters:
        select (str): Specify 'f' for current folder, 'o' for graphs open in current folder, or 'p' for graphs in project
        inc_embed (bool): Include embedded graphs in the list, this is supported for 'p' only

    Returns:
        (list) list of GPage objects

    Examples:
        graphs1 = op.graph_list('p', True)
        graphs2 = op.graph_list('f')

**函数** `load_book(fname) -> Union[originpro.worksheet.WBook, originpro.matrix.MBook]`

    Loads a work or matrixbook from file and returns a WBook or MBook object.

    Parameters:
        fname (str): File path and name. If file name only, the load from UFF

    Returns:
        (WBook or MBook or None)

    Examples:
        wb1 = op.load_book('My Analysis Template.ogwu')#from user file folder
        wb2 = op.load_book(op.path('e')+r'Samples\Batch Processing\Peak Analysis.ogw')

**函数** `new(asksave=False)`

    Starts a new project.

    Parameters:
        asksave (bool)P: If True, prompt user to save current project is it is modified

    Returns:
        None

    Examples:
        op.new()
        op.new(True)

**函数** `new_book(type='w', lname='', template='', hidden=False) -> Union[originpro.worksheet.WBook, originpro.matrix.MBook]`

    Create a new workbook or matrixbook.

    Parameters:
        type(str): Specify 'w' for WBook object or 'm' for MBook object
        lname (str): Long Name of the book
        template (str): Template name. May exclude extension. Does not support OGWU files (e.g. analysis templates). In that case, use load_book.
        hidden (bool): True makes newly created book hidden

    Returns:
        (WBook or MBook or None)

    Examples:
        wb1 = op.new_book()
        wb2 = op.new_book('w', 'My Template')
        mb = op.new_book('m', hidden=True)

    See Also:
        load_book

**函数** `new_graph(lname='', template='', hidden=False) -> originpro.graph.GPage`

    Create a new empty graph optionally from a template.

    Parameters:
        lname (str): Long Name of the graph
        template (str): Template name. May exclude extension. If not specified, use origin.otp.
        hidden (bool): True makes newly created graph hidden

    Returns:
        (GPage or None)

    Examples:
        g1 = op.new_graph()
        g2 = op.new_graph('My Graph')
        g3 = op.new_graph(template=op.path('e') + '3Ys_Y-Y-Y.otp')

**函数** `new_image(lname='', hidden=False) -> originpro.image.IPage`

    Create a new image window

    Parameters:
        lname (str): Long Name of the new window
        hidden (bool): True makes newly created window hidden
    Returns:
        IPage or None
    Examples:
        im = op.new_image()

**函数** `new_notes(name='') -> originpro.notes.Notes`

    Create a new Notes window

    Parameters:
        lname (str): Name of the new window
    Returns:
        Notes or None
    Examples:
        nt = op.new_notes()

**函数** `new_sheet(type='w', lname='', template='', hidden=False) -> Union[originpro.worksheet.WSheet, originpro.matrix.MSheet]`

    Create a new work or matrixbook and return the first sheet as a WSheet or MSheet.

    Parameters:
        type (str): Specify 'w' for WBook object or 'm' for MBook object
        lname (str): Long Name of the book
        template (str): Template name. May exclude extension
        hidden (bool): True makes newly created book hidden

    Returns:
        (WSheet or MSheet or None)

    Examples:
        wks1 = op.new_sheet()
        wks2 = op.new_sheet('w', 'My Template.otwu')
        mxs = op.new_sheet('m', hidden=True)

**函数** `open(file, readonly=False, asksave=False)`

    Opens an Origin project file.

    Parameters:
        file (str): File path and name
        readonly (bool): Opern the file as read-only
        asksave (bool): If True, prompt user to save current project is it is modified

    Returns:
        (bool) True if project is successfully loaded

    Examples:
        op.open('C:\path\to\My Project.opju')

**函数** `pages(type_='') -> Union[originpro.worksheet.WBook, originpro.matrix.MBook, originpro.graph.GPage, originpro.image.IPage]`

    All pages in project.
    Parameters:
        type_ (str): Page type, can be 'w', 'm', 'g', 'i'
    Returns:
        Page Objects
    Examples:
        wps=op.pages('w')
        w1=next(wps)
        wshet=w1[0]

**函数** `save(file='')`

    Saves the current project. If no file name given, then save to current project file.

    Parameters:
        file (str): Path and file name to save the project as. Save to current project file if blank.

    Returns:
        (bool) True if project is successfully saved

    Examples
        op.save('C:\path\to\My Project.opju')
        op.save()


## `originpro.pe`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `Folder`

Origin Folder in Project Explorer

基类：`BaseObject`

**构造** `__init__(self, obj)`

    Initialize self.  See help(type(self)) for accurate signature.

- 属性 `comments`：Property getter returns long name of object.
**方法** `get_float(self, prop)`

    Get object's LabTalk float property
    Parameters:
        prop(string): float prop like symbol.size, details on Origin objects' reference pages
    Returns:
        object's float property
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        print(p.get_float('symbol.size'))

**方法** `get_int(self, prop)`

    Get object's LabTalk int property
    Parameters:
        prop(string):int prop line
        [cmap.stretchpal, cmap.linkpal symbol.kind], details on Origin objects' reference pages
    Returns:
        object's int property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_int('nrows'))

**方法** `get_str(self, prop)`

    Get object's LabTalk string property
    Parameters:
        prop(string): string prop like
        [cmap.palette, colorlist,  name], details on Origin objects' reference pages
    Returns:
        object's string property
    Examples:
        wks1 = op.new_sheet()
        print(wks1.get_str('name'))

**方法** `index(self)`

    interal index in corresponding collection of the object
    Parameters:
        none
    Returns:
        interal index
    Examples:
        wks1 = op.new_sheet()
        print(wks1.index())

- 属性 `lname`：Property getter returns long name of object.
**方法** `lt_exec(self, labtalk)`

    executes a LabTalk statement.

    Parameters:
        labtalk (str): LabTalk statement

    Returns:
        None

    Examples:
        wb.lt_exec('page.longname$="lt_exec example"')
        wks.lt_exec(r'expASC path:="c:\test\signal.csv";') #you can execute X-Function here

**方法** `method_float(self, name, arg='')`

    execute object's LabTalk method that has a float return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (float)LabTalk method's return value
    Examples:
        wks1 = op.new_sheet()
        rowid=wks1.method_float('UserParam', '++test') #add user parameter row "test", and return its index on worksheet

**方法** `method_int(self, name, arg='')`

    execute object's LabTalk method that has an int return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (int)LabTalk method's return value
    Examples:
        wks1 = op.find_sheet()
        issel = wks1.method_int('isColSel', '3') #return if 3rd col is selected

**方法** `method_str(self, name, arg='')`

    execute object's LabTalk method that has a string return
    Parameters:
        name(string):prop string, details on Origin objects' reference pages
        arg:property value
    Returns:
        (string)LabTalk method's return value
    Examples:
        wks = op.new_sheet()
        row, col = 1,1
        wks.set_cell_note(row,col,'test Note')
        cnote = wks.method_str('GetNote',f'{row+1},{col+1}')

- 属性 `name`：short name of the object
**方法** `pages(self, type_='') -> Union[originpro.worksheet.WBook, originpro.matrix.MBook, originpro.graph.GPage, originpro.image.IPage]`

    All pages in folder.
    Parameters:
        type_ (str): Page type, can be 'w', 'm', 'g', 'i'
    Returns:
        Page Objects
    Examples:
    for wb in op.pages('w'):
        for wks in wb:
            print(f'Worksheet {wks.lt_range()} has {wks.rows} rows')

- 属性 `path`：Full path of folder
**方法** `set_float(self, prop, value)`

    Set object's LabTalk float property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        p=op.find_graph()[0].plot_list()[0]
        p.set_float('symbol.size', 4.5)

**方法** `set_int(self, prop, value)`

    Set object's LabTalk int property
    Parameters:
        prop(string):prop string, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_int('nrows', 10)

**方法** `set_str(self, prop, value)`

    Set object's LabTalk string property
    Parameters:
        prop(string):can be int/float/string property, details on Origin objects' reference pages
        value:property value
    Returns:
        none
    Examples:
        wks1 = op.new_sheet()
        wks1.set_str('name','test_set_str')

- 属性 `show`：Property getter returns show state of object.
- 属性 `userprops`：Parameters:
- 属性 `usertree`：    Return User Tree as ElementTree
**函数** `active_folder()`

    Active Folder in Project Explorer
    Parameters:
        none
    Returns:
       Folder Objects
    Examples:
        fd=op.pe.active_folder()

**函数** `cd(path=None)`

    Change Project Explorer directory
    Parameters:
        path (str): Path of the directory to move into
    Returns:
        Current path
    Examples:
        path=op.pe.search('Graph1',0)
        op.pe.cd(path)

**函数** `mkdir(path, chk=False)`

    Create new folder in Project Explorer
    Parameters:
        path (str): Name of the path to be created; if folder already exists and chk is False, then it is enumerated, but if chk is True, then will not create new
        chk (bool): Specify if check folder exists or not. If set to True, then will not force create enumerated new one if already existed
    Returns:
        Path created
    Examples:
        path=op.pe.search('Graph1',0)
        op.pe.cd(path)
        op.pe.mkdir('Folder2', True)

**函数** `move(name, path)`

    Move page or folder to specified folder in Project Explorer
    Parameters:
        name (str): Name of the existing page or folder
        path (str): path of the location where the page should be moved to
    Returns:
        None
    Examples:
        path=op.pe.search('Graph1',0)
        op.pe.cd(path)
        op.pe.mkdir('Folder2', True)
        op.pe.move('Folder2','/UNTITLED/')

**函数** `root_folder()`

    Root Folder in Project Explorer
    Parameters:
        none
    Returns:
       Page Objects
    Examples:
        fd=op.pe.root_folder()

**函数** `search(name='', kind=0)`

    Get current Project Explorer path or path of specified window
    Parameters:
        name (str): Name of the page/folder to be searched for
        kind (int): Page Short Name if 0, Subfolder Name if 1
    Returns:
        Current path if page/folder is empty, or path where page/folder is located
    Examples:
        op.pe.search('Graph1',0)


## `originpro.imp`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation

**函数** `get_sheet(index=0, _type='w') -> Union[originpro.worksheet.WSheet, originpro.matrix.MSheet]`

    This is for importing into multiple sheets, to get the needed sheet by index.
    For exmaple a file with multiple blocks.

    Parameters:
        index(int): sheet index in a multisheet group, 0,1,2
        type (str): Specify 'w' for WBook object or 'm' for MBook object
    Returns:
        (WSheet or MSheet or None)

    Examples:
        wks1 = op.imp.get_sheet()   #when active book that is a workbook
        wks2 = op.imp.get_sheet(1)

**函数** `prepare_range(objs_count, sheet_index=0)`

    Prepare column ranges for Connector import
    Parameters:
        objs_count(int):
        sheet_index(int):
    Returns:
        the first column index in column range
    Examples:
        op.imp.prepare_range(3,0) #This function must be used with the
                                  #COConnMultipleSheetsMonitorBase class


## `originpro.dc`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `Connector`

Data Connector
Parameters:
    wks (DSheet): the worksheet or martix sheet to use the connector
    dctype(str):  Name of the connector, CSV, Excel etc
    keep_DC(bool): Keep the connector after import
Example:
    import originpro as op
    f = op.path('e')+r'Samples\Import and Export\S15-125-03.dat'
    wks = op.find_sheet()
    dc = op.Connector(wks)
    ss = dc.settings()
    partial = ss['partial']
    partial[op.attrib_key('Use')]='1'
    partial['row']='10:20'
    dc.imp(f)

**构造** `__init__(self, wks, dctype='', keep_DC=True)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `imp(self, fname='', sel='', sparks=False)`

    Import file
    Parameters:
        fname(string): source file name
        sel(string):selection
    Returns:
        none
    Examples:
        wks=op.find_sheet()
        dc=op.Connector(wks)
        f=op.path('e')+r'Samples\Import and Export\ASCII Simple.dat'
        dc.imp(f)

**方法** `new_sheet(self, name)`

    Import a new selection into a new sheet

    Parameters:
        name(str): selection, for example an Excel sheet name

    Returns:
        None
    Examples:
        dc.imp(f, sel='Oil')
        dc.new_sheet('Natural Gas')

**方法** `settings(self)`

    Parameters:
        none
    Returns:
        Import settings
    Examples:
        wks=op.find_sheet()
        dc=op.Connector(wks)
        ss=dc.settings()

- 属性 `source`：Property getter returns the source of Data Connector

## `originpro.config`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation


### class `APP`

OriginExt.Application() wrapper

**构造** `__init__(self)`

    Initialize self.  See help(type(self)) for accurate signature.

**方法** `Attach(self)`

    Attach to exising Origin instance

**方法** `Detach(self)`

    Detach from Origin instance

**方法** `Exit(self, releaseonly=False)`

    Exit if Application exists

**函数** `check_ignore_warnings(func)`

## `originpro.utils`

originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation

**函数** `active_obj(name)`

    Get active object
    Parameters:
        name(string):object type name
    Returns:
        active object
    Examples:
        page=op.active_obj('Page')

**函数** `attach()`

    Attach to exising Origin instance
    Parameters:
        none
    Return:
        none
    Example:
        op.attach()

**函数** `attrib_key(name)`

    Make attribute key from name

**函数** `color_col(offset=1, type='m')`

    Generate Origin's internal OColor to use in data plot's color setting
    Parameters:
        offset (int): worksheet column offset to the plot's Y column
        type (str): 'm' for Colormap, 'n' = Indexing, 'r' = RGB
    Returns:
        OColor
    Examples:
        plot.color = op.color_col()# use next column to Y as color map values
        plot.color = op.color_col(1,'n') #use index color, column needs to contain 1,2,3 etc
        plot.colormap="fire"

**函数** `detach()`

    Detach Origin instance
    Parameters:
        none
    Return:
        none
    Example:
        op.detach()

**函数** `evaluate_FDF(ffname, indepvars, parameters)`

    Evaluate FDF function
    Parameters:
        ffname (str): Name of the Fitting Function
        indepvars(list): Independent Variables values, can be list of list if multiple independents
        parameters(list): Parameter values
    Returns:
        A list of Dependent Variable values
    Examples:
        vx = [1, 2, 3]
        vy = op.evaluate_FDF('Gauss', vx, [1, 2, 3, 4])

**函数** `exit()`

    exit the application
    Parameters:
        none
    Return:
        none
    Example:
        op.exit()

**函数** `file_dialog(type, title='')`

    open a file dialog to pick a single file
    Parameters:
        type (str): 'i' for image, 't' for text, 'o' for origin, or a file extension like '*.png'

    Returns:
        if user cancel, an empty str, otherwise the selected file path
    Examples:
        fn=op.file_dialog('o')
        fn=op.file_dialog('*.png;*.jpg;*.bmp')

**函数** `get_file_ext(fname)`

    Given a full path file name, return the file extension.

    Parameters:
        fname (str): Full path file name

    Returns:
        (str) File extension

    Examples:
        ext = op.get_file_ext('C:\path\to\somefile.dat')

**函数** `get_file_parts(fname)`

    Given a full path file name, return the path, file name, and extension as a Python list object.

    Parameters:
        fname (str): Full path file name

    Returns:
        (list) Contains path, file name, and extension

    Examples:
        parts = op.get_file_parts('C:\path\to\somefile.dat')

**函数** `get_lt_str(vname)`

    Parameters:
        vname (str): a LabTalk string
    Returns:
        return a LabTalk string variable value. To get LabTalk numeric values,
        use lt_int or lt_float
    Examples:
        #AppData path for the installed Origin
        >>> op.get_lt_str('%@Y')
    See Also:
        lt_int, lt_float

**函数** `get_show()`

    If the Application is visible or not
    Parameters:
        none
    Return:
        True if visible, otherwise False
    Example:
        op.get_show()

**函数** `last_backslash(fpath, action)`

    Add or trim a backslash to/from a path string.

    Parameters:
        fpath (str): Path
        action (str): Either 'a' for add backslash or 't' for trim backslash

    Returns:
        (str) Path either with added backslash or without trimmed backslash

    Examples:
        >>>op.last_backslash(op.path(), 't')

**函数** `lt_delete_tree(name)`

    Delete a Labtalk tree
    Parameters:
        name(string):name of the Labtalk tree
    Returns:
        none
    Examples:
        op.lt_delete_tree('tr')

**函数** `lt_dict_to_tree(dd, treename, add_tree=False, check_attributes=False)`

    Converts dictionary dd to an xml tree string and sets the value of a LabTalk tree variable
    to the xml tree string. If bAddTreeVar is False and the tree variable does not already exist,
    the tree variable will not be added. Pass True as bAddTreeVar if you want to make sure that
    the tree variable is added first if it does not exist.
    Parameters:
        dd (dictionary)
        treename(str): the name of the tree variable
        add_tree:If True, the tree variable will be added if it does not exist
        check_attributes(bool):whether to check attributes
    Returns:
        none
    Examples:
        dd={'name':'bob', 'age':14, 'class':'p1'}
        op.lt_dict_to_tree(dd,'tr',True)

**函数** `lt_empty_tree()`

    Parameters:
        none
    Returns:
        An empty Labtalk tree
    Examples:
        tr=op.lt_empty_tree()

**函数** `lt_exec(labtalk)`

    run LabTalk script
    Parameters:
        labtalk(string):LabTalk script
    Returns:
        bool value that indicate Whether the script is run successfully
    Examples:
        op.lt_exec('impasc -dm')

**函数** `lt_float(formula)`

    Parameters:
        formula (str): any LaTalk expression
    Returns:
        the result of a LabTalk expression
    Examples:
        #Origin Julian days value
        >>>op.lt_float('date(1/2/2020)')
        #get Origin version number
        >>>op.lt_float('@V')

    See Also:
        get_lt_str, lt_int

**函数** `lt_int(formula)`

    Parameters:
        formula (str): any LaTalk expression
    Returns:
        the result of a LabTalk expression as int, see lt_float()
    Examples:
        >>> op.lt_int('color("green")')

    See Also:
        get_lt_str, lt_float

**函数** `lt_tree_to_dict(name, add_attributes=False)`

    Get Labtalk tree as dict
    Parameters:
        name (str): Name of the Labtalk tree
        add_attributes(bool): add the attributes from the tree as nodes
    Returns:
        dict to hold Labtalk tree content
    Examples:
        wks = op.new_sheet()
        data = [1,2,3,4,5]
        wks.from_list(0, data)
        wks.from_list(1, data)
        op.lt_exec('fitlr (1,2)')
        dd = op.lt_tree_to_dict('fitlr')

**函数** `make_DataRange(*args, rows=None)`

    Make Origin DataRange object

**函数** `messagebox(msg, cancel=False)`

    open a message box
    Parameters:
        msg(str): the text to prompt
        cancel(bool): True if OK Cancel, False if just OK

    Return:
        False if has cancel button and user click Cancel

    Examples:
        nn = op.messagebox('this is a test', True)
        if not nn:
            op.messagebox('you clicked cancel')
        else:
            op.messagebox('you click ok')

**函数** `modi_col(offset=1)`

    Generate Origin's internal modifier (uint) value to use in data plot's various setting
    Parameters:
        offset (int): worksheet column offset to the plot's Y column
    Returns:
        uint
    Examples:
        plot.symbol_size = op.modi_col(1)# use next column to Y as symbol size
        plot.symbol_kind = op.modi_col(2)

**函数** `ocolor(rgb)`

    convert color to Origin's internal OColor

    Parameters:
        rgb: names or index of colors supported in Origin.
                      name          index    (Red, Green, Blue)
                      'Black'           1       000,000,000
                      'Red'             2       255,000,000
                      'Green'           3       000,255,000
                      'Blue'            4       000,000,255
                      'Cyan'            5       000,255,255
                      'Magenta'         6       255,000,255
                      'Yellow'          7       255,255,000
                      'Dark Yellow'     8       128,128,000
                      'Navy'            9       000,000,128
                      'Purple'          10       128,000,128
                      'Wine'            11      128,000,000
                      'Olive'           12      000,128,000
                      'Dark Cyan'       13      000,128,128
                      'Royal'           14      000,000,160
                      'Orange'          15      255,128,000
                      'Violet'          16      128,000,255
                      'Pink'            17      255,000,128
                      'White'           18      255,255,255
                      'LT Gray'         19      192,192,192
                      'Gray'            20      128,128,128
                      'LT Yellow'       21      255,255,128
                      'LT Cyan'         22      128,255,255
                      'LT Magenta'      23      255,128,255
                      'Dark Gray'       24      064,064,064
             it can be in formmat as well, for example, '#f00' for red.
             when the input is a tuple, it should be
             if rgb is tuple of intergers between 0 and 255,
             the color is set by RGB (Red, Green, Blue).

    Returns:
        (int) OColor
    Example:
        print(op.ocolor('Gray'))

**函数** `olab_download(file)`

    download a file from Originlab website with blocking so
    function will not return until it is done or encountering an error
    Parameters:
        file (str or int): file name with extention or the fid,
                           which you can find out from Template Center
    Returns:
        0 if downloaded
        1 if already downloaded and nothing to do
        <0 error
    Examples:
        n=op.olab_download('RaisedReliefMap.otpu')
        n=op.olad_download(939)

**函数** `org_ver()`

    Parameters:
        none
    Returns:
        Origin Version as float
    Examples:
        print(op.org_ver())

**函数** `origin_class(name)`

    Get Origin base class
    Parameters:
        name(string):Origin class name
    Returns:
         Origin base class
    Examples:
        ranges=op.origin_class('DataRange')

**函数** `path(type='u')`

    Returns one of the Origin pre-defined paths: User Files folder, Origin EXe folder,
    project folder, Project attached file folder.

    Parameters:
        type (str): 'u'(User Files folder), 'e'(Origin Exe folder), 'p'(project folder),
                    'a'(Attached file folder), 'c'(Learning Center)

    Returns:
        (str) Contains folder path

    Examples:
        uff = op.path()
        op.open(op.path('c')+ r'Graphing\Trellis Plots - Box Charts.opju')

**函数** `set_lt_str(vname, value)`

    sets a LabTalk string variable value.
    Parameters:
        vname(string):LabTalk variable name
        value:
    Returns:
        bool value that indicate Whether the value is set successfully
    Examples:
        fpath = op.file_dialog('*.log')
        op.set_lt_str('fname', fpath)
        tmp=op.get_lt_str('fname')
        print(tmp)
    See Also:
        get_lt_str

**函数** `set_lt_var(name, value)`

    sets a LabTalk numeric variable value. This is usually used for setting system variables
    Parameters:
        name(string):LabTalk numeric variable name
        value:
    Return:
        none
    Example:
        op.set_lt_var("@IAS",5)#set import using multi-thread for files 5M or larger
    See Also:
        lt_float, set_lt_str

**函数** `set_show(show=True)`

    Show or Hide the Application
    Parameters:
        show(bool):
    Return:
        none
    Example:
        op.get_show()

**函数** `to_rgb(orgb)`

    convert an Origin OColor to r, g, b

    Parameters:
        orgb(int): OColor from Origin's internal value

    Returns:
        (tuple) r,g,b
    Example:
        print(op.to_rgb(20))#128,128,128

**函数** `wait(type='r', sec=0)`

    Wait for recalculation to finish or a specified number of seconds.

    Parameters:
        type (str): Either 'r' to wait for recalculation to finish or
                    's' to wait for specified seconds
        sec (float): Number of seconds to wait is 's' specified for type

    Returns:
        None

    Examples:
        op.wait()#wait for Origin to update all the recalculations
        op.wait('s', 0.2)#gives 0.2 sec for graphs to finish updating

