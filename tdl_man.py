from datetime import datetime

## Open ToDoList data and read content
tdl_data = "/home/dwest77/Documents/tdl_manager/tdl_data.txt"
f = open(tdl_data,'r')
content = f.readlines()
f.close()

local_removals = []

# TDL entries have <ID>,<Name>,<Date>

# For formatting item entries in list
def buffer(item, length):
    buff=''
    if len(item) >= length:
        item = item[:length]
    else:
        for x in range(0,length-len(item)):
            buff += ' '
    return str(item+buff)

def show_all(content, name='',tpe='', dep=''):
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
            if id in local_removals:
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
    if len(local_removals) != 0:

        # Formatting for local removals
        print('To be removed: ',end='')
        for lr in local_removals:
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
    print(content)
    return content

def remove_entry(content):
    # Schedule entry removals for next list save
    # So accidental removals are reversable

    # Reshow all current entries
    show_all(content)
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
    local_removals.append(id)

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

def save_data(content):
    # Write tdl data to output file

    word = ''
    for line in content:
        id = line.split(',')[0]
        # Write only non-removal items to save string
        if id not in local_removals:
            word += line

    # Write savestring to file
    g = open(tdl_data,'w')
    g.write(word)
    g.close()

def show_kwargs(content, cmd):
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
    show_all(content,name=name, tpe=tpe, dep=dep)

# Welcome to manager
print('\nTo Do List Manager v0.1 - dwest77\n')
# Entry for new fields
cmd = ''
while 'exit' not in cmd:
    cmd = input('>> ')

    # Show all entries command
    if 'show' in cmd:
        if cmd == 'show':
            show_all(content)
        else:
            show_kwargs(content,cmd)
    # Add entry to list
    elif cmd == 'add':
        content = add_entry(content)
    # Remove entry from list
    elif cmd == 'rm':
        remove_entry(content)
    # Ammend existing entry by ID
    elif cmd == 'ammend':
        content = ammend_entry(content)
    elif cmd == 'help':
        show_help()
    # Do nothing
    elif cmd == '':
        pass
    # Exit software
    elif 'exit' in cmd:
        print('Exiting')
    # Valid commands only
    else:
        print('-tdl: Unrecognised command - "{}"'.format(cmd))

# Save data on shutdown unless specified otherwise
if 'q' not in cmd:
    save_data(content)
    print('Shutdown and save complete')
else:
    print('Shutdown (no save) complete')
