from datetime import datetime
import os

## Open ToDoList data and read content
tdl_data = "/home/dwest77/Documents/tdl_manager/tdl_data.txt"
tdl_backup = "/home/dwest77/Documents/tdl_manager/tdl_backup.txt"
f = open(tdl_data,'r')
content = f.readlines()
f.close()

# TDL entries have <ID>,<Name>,<Date>

def backup():
    os.system('cp {} {}'.format(tdl_data, tdl_backup))

def recombine(arr):
    word = ''
    for item in arr:
        word += str(item) + ','
    return word[:-1]

# For taking a specified reordering pattern to reassign ids
def reorder(content):
    new_pattern = input("Reorder old IDs: ")
    new_p = new_pattern.split(" ")
    if len(new_p) != len(content):
        print('Not All IDs included in reassignment - exiting reorder')
        return content
    new_content = []
    for index, new_id in enumerate(new_p):
        line = content[int(new_id)]
        larr = line.split(',')
        larr[0] = int(index)
        line = recombine(larr)
        new_content.append(line)

    return new_content

# For formatting item entries in list
def cascade(content,lrs):
    id_counter = 0
    for x in range(len(content)):
        line = content[x]
        id = str(line.split(',')[0])

        # Remember to reset removal list
        for y in range(len(lrs)):
            if lrs[y] == id:
                lrs[y] = str(id_counter)
        entry = line[len(id):]
        entry = str(id_counter) + entry
        content[x] = entry
        id_counter += 1
    return content, lrs

def buffer(item, length):
    buff=''
    if len(item) >= length:
        item = item[:length]
    else:
        for x in range(0,length-len(item)):
            buff += ' '
    return str(item+buff)

def show_all(content, lrs, name='',tpe='', dep=''):
    # Get current datetime
    today = datetime.now()
    now = today.strftime("%d/%m/%Y %H:%M:%S")
    print('')
    print('To Do List: {}'.format(now))
    print(buffer('ID',3),end="")
    print(buffer('Item',80),end="")
    print(buffer('Type',20),end="")
    print(buffer('Dependency',20),end="")
    print('Date')
    print('----------------------------------------------------------------------------------------------------------------------------------------------')
    filter = []
    if name != '' or dep != '' or tpe != '':
        for x, line in enumerate(content):
            if name != '' and name in line:
                filter.append(x)
            elif dep != '' and dep in line:
                filter.append(x)
            elif tpe != '' and tpe in line:
                filter.append(x)
    # For all entries
    for x, line in enumerate(content):
        if filter == [] or (filter != [] and x in filter):
        
            # Get entry id
            id = line.split(',')[0]

            # Display items scheduled for removal with '*' at front
            if id in lrs:
                print('*',end='')
            ## Output formatting so all entries use 100 char descriptions
            
            # Format id=0,name=1,type=2,dependencies=3,date=4
            line = line.split(',')
            print(buffer(line[0],3),end="")
            print(buffer(line[1],80),end="")
            print(buffer(line[2],20),end="")
            print(buffer(line[3],20),end="")
            print(line[4])
    print('')
    # List entries scheduled for removal by id
    if len(lrs) != 0:

        # Formatting for local removals
        print('To be removed (ID): ',end='')
        for lr in lrs:
            print(lr + ' ',end='')
        print('')
    print('')

def add_entry(content):
    # Add new entry by <ID>,<Name>,<Date>
    today = datetime.now()

    # Extract most recent ID from latest entry
    try:
        last_entry = content[-1]
        entry_id = int(last_entry.split(',')[0])+1
    except:
        entry_id = 0

    # Get entry name as input and assemble date in readable format
    entry_name = input('New Item (80 char): ')
    entry_type = input('Type (20 char): ')
    entry_dep  = input('Dependencies (20 char): ')
    entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    new_entry = '{},{},{},{},{}\n'.format(entry_id, entry_name, entry_type, entry_dep, entry_date)
    content.append(new_entry)
    return content

def remove_entry(content,lrs):
    # Schedule entry removals for next list save
    # So accidental removals are reversable

    # Reshow all current entries
    show_all(content, lrs)
    is_valid = False
    
    # Accept valid entries for ID only
    while not is_valid:
        id = input('Remove (ID) >> ')

        # Search list for ID entered
        for line in content:
            if id + ',' in line:
                is_valid = True
        
        # Statement for invalid IDs
        if not is_valid:
            print('-tdl: Unrecognised ID - enter existing ID for removal')

    # Add valid ID to list for later removal
    lrs.append(str(id))
    return lrs

def ammend_entry(content):
    # Add new entry by <ID>,<Name>,<Date>
    today = datetime.now()

    is_valid = False
    
    # Accept valid entries for ID only
    while not is_valid:
        entry_id = input('Ammend (ID) >> ')

        # Search list for ID entered
        if entry_id != '*':
            for line in content:
                if entry_id == line.split(',')[0]:
                    is_valid = True
        else:
            is_valid = True
        
        # Statement for invalid IDs
        if not is_valid:
            print('-tdl: Unrecognised ID - enter existing ID for ammendment')
    # Get entry name as input and assemble date in readable format

    # Find old entry
    for x in range(len(content)):
        if entry_id == content[x].split(',')[0]:
            old_entry = content[x]
            new_index = x

    entry_name = input('*Name: ')
    if entry_name == '':
        entry_name = old_entry.split(',')[1]
    entry_type = input('*Type: ')
    if entry_type == '':
        entry_type = old_entry.split(',')[2]
    entry_dep  = input('*Dependencies: ')
    if entry_dep == '':
        entry_dep = old_entry.split(',')[3]
    entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    adj_entry = '{},{},{},{},{}\n'.format(entry_id, entry_name, entry_type, entry_dep, entry_date)
    content[new_index] = adj_entry

    return content

def show_help():
    print('''
Help/Info - Accepted commands
>> add    - add new entry to ToDoList
>> rm     - remove existing entry by ID
>> show   - list all current entries including those to be removed on save
        name="Name of item"
        dep="Dependencies
        type="Type of item"
>> ammend - ammend descritpion of existing entry by ID
>> exit   - exit and save data
>> exit q - exit without saving (refresh removals list)
    ''')

def save_data(content,lrs):
    # Write tdl data to output file

    word = ''
    newcontent = []
    for line in content:
        id = line.split(',')[0]
        # Write only non-removal items to save string
        if id not in lrs:
            word += line
            newcontent.append(line)


    # Write savestring to file
    g = open(tdl_data,'w')
    g.write(word)
    g.close() 
    return newcontent

def show_kwargs(content, cmd, lrs):
    is_entering = False
    kwargs = []
    entry = ''
    for char in cmd[5:]:
        if char == '"' and is_entering:
            is_entering = False
            kwargs.append(entry)
            entry = ''
        elif char == '"' and not is_entering:
            is_entering = True
        elif char == ' ' and not is_entering:
            kwargs.append(entry)
            entry = ''
        else:
            entry += char
    kwargs.append(entry)
    name, tpe, dep = '','',''
    for kw in kwargs:
        if 'name=' in kw:
            name = kw.replace('name=','')
        elif 'type=' in kw:
            tpe = kw.replace('type=','')
        elif 'dep=' in kw:
            dep = kw.replace('dep=','')
    show_all(content, lrs,name=name, tpe=tpe, dep=dep)

lrs = []

# Welcome to manager
print('\nTo Do List Manager v0.1 - dwest77\n')
# Entry for new fields
cmd = ''
while 'exit' not in cmd:
    cmd = input('>> ')

    # Show all entries command
    if 'show' in cmd:
        if cmd == 'show':
            show_all(content, lrs)
        else:
            show_kwargs(content,cmd, lrs)
    # Add entry to list
    elif cmd == 'add':
        content = add_entry(content)
    # Remove entry from list
    elif cmd == 'rm':
        lrs = remove_entry(content, lrs)
    # Ammend existing entry by ID
    elif cmd == 'ammend':
        content = ammend_entry(content)
    elif cmd == 'help':
        show_help()
    # Do nothing
    elif cmd == '':
        pass
    # Save Entries
    elif cmd == 'reorder':
        content = save_data(content, lrs)
        lrs = []
        show_all(content, lrs)
        content = reorder(content)
        content = save_data(content, lrs)
        lrs = []
    elif cmd == 'save':
        content,lrs = cascade(content,lrs)
        content = save_data(content, lrs)
        lrs = []
    elif cmd == 'cascade':
        content,lrs = cascade(content,lrs)
    # Exit software
    elif 'exit' in cmd:
        print('Exiting')
    # Valid commands only
    else:
        print('-tdl: Unrecognised command - "{}"'.format(cmd))

# Save data on shutdown unless specified otherwise
if 'q' not in cmd:
    content,lrs = cascade(content,lrs)
    c = save_data(content,lrs)
    backup()
    print('Shutdown and save complete')
else:
    print('Shutdown (no save) complete')
