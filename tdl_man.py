from datetime import datetime

## Open ToDoList data and read content
tdl_data = "/home/dwest77/Documents/tdl/tdl_data.txt"
f = open(tdl_data,'r')
content = f.readlines()
f.close()

local_removals = []

# TDL entries have <ID>,<Name>,<Date>

def show_all(content, name='', dep=''):
    # Get current datetime
    today = datetime.now()
    now = today.strftime("%d/%m/%Y %H:%M:%S")

    print('To Do List: {}'.format(now))
    print('-----------------------------------')
    filter = []
    if name != '' or dep != '':
        for x, line in enumerate(content):
            if name != '' and name in line:
                filter.append(x)
            elif dep != '' and dep in line:
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
            # Description formatting
            buff = ''
            line = line.split(',')
            print(line[0] + ' ',end="")
            for x in range(0,100-len(line[1])):
                buff += ' '
            print(line[1] + buff,end="")
            if len(line) == 4:
                buff = ''
                for y in range(0,20-len(line[2])):
                    buff += ' '
                print(line[2] + buff,end="")
                print(line[3])
            else:
                buff = 'n/a'
                for y in range(0,17):
                    buff += ' '
                print(buff,end="")
                print(line[2])
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
    entry_name = input('New Item: ')
    entry_dep  = input('Dependencies: ')
    entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    new_entry = '{},{},{},{}\n'.format(entry_id, entry_name, entry_dep, entry_date)
    content.append(new_entry)
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
    if entry_id == '*':
        dep  = input('*Dependencies: ')
        new_content = []
        for line in content:
            line = line.split(',')
            new_line = '{},{},{},{}'.format(line[0], line[1], dep, line[2])
            new_content.append(new_line)
        content = new_content
    else:
        # Find old entry
        for x in range(len(content)):
            if entry_id == content[x].split(',')[0]:
                old_entry = content[x]
                new_index = x

        entry_name = input('*Name: ')
        if entry_name == '':
            entry_name = old_entry.split(',')[1]
        entry_dep  = input('*Dependencies: ')
        if entry_dep == '':
            entry_dep = old_entry.split(',')[2]
        entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

        # Assemble new entry str and append
        adj_entry = '{},{},{},{}\n'.format(entry_id, entry_name, entry_dep, entry_date)
        content[new_index] = adj_entry

    return content

def show_help():
    print('''
Help/Info - Accepted commands
>> add    - add new entry to ToDoList
>> rm     - remove existing entry by ID
>> show   - list all current entries including those to be removed on save
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

# Welcome to manager
print('\nTo Do List Manager v0.1 - dwest77\n')
# Entry for new fields
cmd = ''
while 'exit' not in cmd:
    cmd = input('>> ')

    # Show all entries command
    if 'show' in cmd:
        cmd_arr = cmd.split('-')
        try:
            name = cmd_arr[1]
            try:
                dep = cmd_arr[2]
            except:
                dep = ''
            if name == '*':
                name = ''
            show_all(content,name=name, dep=dep)
        except:
            show_all(content)
        
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
