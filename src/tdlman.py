from datetime import datetime
import os, sys
import json
import numpy as np

HELP = '''
Help/Info - Accepted commands
>> add    - add new entry to ToDoList
>> rm     - remove existing entry by ID
>> show   - list all current entries including those to be removed on save
        name="Name of item"
        dep="Dependencies
        type="Type of item"

>> ammend  - ammend descritpion of existing entry by ID
>> cascade - relabel items so ID gaps are closed (0,4,5 -> 0,1,2)
>> reorder - specify item reordering (0 2 5 1 3 4)

>> save   - save current list without exiting the program
>> exit   - exit and save data
>> exit q - exit without saving (refresh removals list)
    '''

# TDL entries have <ID>,<Name>,<Date>

def getSortedIntKeys(mydict):
    raw = mydict.keys()
    ints = []
    try:
        for key in raw:
            ints.append(int(key))
        return sorted(ints)
    except ValueError:
        print('Error: Invalid ID in dict')
        return sorted(raw)

def backup(tdl_data, tdl_backup):
    os.system('cp {} {}'.format(tdl_data, tdl_backup))

def recombine(arr):
    word = ''
    for item in arr:
        word += str(item) + ','
    return word[:-1]

# For taking a specified reordering pattern to reassign ids
def reorder(json_contents, reorder_str=False):
    if reorder_str:
        new_pattern = reorder_str
    else:
        new_pattern = input("Reorder old IDs: ")
    new_p = new_pattern.split(" ")
    json_contents_n = {}

    if len(new_p) != len(json_contents):
        print('Not All IDs included in reassignment - exiting reorder')
        return json_contents

    for x, key in enumerate(getSortedIntKeys(json_contents)):
        new_key = new_p[x]
        json_contents_n[str(key)] = json_contents[new_key]

    return json_contents_n

# For formatting item entries in list
def cascade(json_contents):
    json_new = {}
    json_con_keys = getSortedIntKeys(json_contents)
    for index, key in enumerate(json_con_keys):
        json_new[str(index)] = json_contents[str(key)]
    return json_new

def buffer(item, length):
    buff=''
    if len(item) >= length:
        item = item[:length]
    else:
        for x in range(0,length-len(item)):
            buff += ' '
    return str(item+buff)

def titleList():
    today = datetime.now()
    now = today.strftime("%d/%m/%Y %H:%M:%S")
    print('')
    print('To Do List: {}'.format(now))
    print(buffer('ID',4),end="")
    print(buffer('Type',21),end="")
    print(buffer('Format',21),end="")
    print(buffer('Item',61),end="")
    print(buffer('Dependency',21),end="")
    print('Date')
    print('---------------------------------------------------------------------------------------------------------------------------------------------------')

def showAll(json_contents, name='',tpe='', dep='', ob=''):
    # Get current datetime
    titleList()
    # For all entries
    for id in json_contents.keys():
        entry = json_contents[id]
        nfilter = (entry['Description'] == name or name == '')
        dfilter = (entry['Dependency'] == dep or dep == '')
        tfilter = (entry['Type'] == tpe or tpe == '')
        if nfilter or dfilter or tfilter:
        
            try:
                if entry['rm']:
                    print('*',end='')
            except:
                pass
            
            # Format id=0,name=1,type=2,dependencies=3,date=4
            print(
                buffer(id,3),
                buffer(entry['Type'],20),
                buffer(entry['Format'],20),
                buffer(entry['Description'],60),
                buffer(entry['Dependency'],20),
                entry['Date']
            )
            print('')
    print('')

def addEntry(json_contents):
    # Add new entry by <ID>,<Name>,<Date>
    today = datetime.now()
    # Extract most recent ID from latest entry
    entry_id = np.max(np.array(list(json_contents.keys()),dtype=int))+1

    # Get entry name as input and assemble date in readable format
    entry_name   = input('New Item (60 char): ')
    entry_format = input('Format (20 char): ')
    entry_type = input('Type (20 char): ')
    entry_dep  = input('Dependencies (20 char): ')
    entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    json_contents[str(entry_id)] = {
        'Format':entry_format,
        'Description':entry_name,
        'Type':entry_type,
        'Dependency':entry_dep,
        'Date':entry_date
    }
    return json_contents

def removeEntry(json_contents):
    # Schedule entry removals for next list save
    # So accidental removals are reversable

    # Reshow all current entries
    showAll(json_contents)
    is_valid = False
    
    # Accept valid entries for ID only
    while not is_valid:
        id = input('Remove (ID) >> ')
        try:
            json_contents[id]['rm'] = True
            is_valid = True
        except:
            print('-tdl: Unrecognised ID - enter existing ID for removal')

    return json_contents

def forceRemoveEntry(json_contents):
    json_new = {}
    for key in json_contents.keys():
        try:
            temp = json_contents[key]['rm']
        except:
            json_new[key] = json_contents[key]
    return json_new

def ammendEntry(json_contents):
    """
    Routine for ammending existing records by id
    """
    today = datetime.now()

    is_valid = False
    while not is_valid:
        entry_id = input('Ammend (ID) >> ')
        # Search list for ID entered
        try:
            old_info = dict(json_contents[entry_id])
            is_valid = True
        except:
            print('-tdl: Unrecognised ID - enter existing ID for ammendment')
    # Get entry name as input and assemble date in readable format

    entry_type = input('*Type: ')
    if entry_type == '':
        entry_type = old_info['Type']
    entry_format = input('*Format: ')
    if entry_format == '':
        entry_format = old_info['Format']
    entry_name = input('*Item: ')
    if entry_name == '':
        entry_name = old_info['Description']
    entry_dep  = input('*Dependencies: ')
    if entry_dep == '':
        entry_dep = old_info['Dependency']
    entry_date = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    json_contents[entry_id] = {
        'Format':entry_format,
        'Description':entry_name,
        'Type':entry_type,
        'Dependency':entry_dep,
        'Date':entry_date
    }

    return json_contents

def showHelp():
    """
    Show help information
    """
    print(HELP)

def mapOldData():
    f = open('tdl_data.txt','r')
    content = f.readlines()
    f.close()

    json_dict = {}
    for line in content:
        line = line.replace('\n','').split(',')
        tid     = line[0]
        tformat = line[1]
        tdesc   = line[2]
        ttype   = line[3]
        tdep    = line[4]
        tdate   = line[5]

        json_dict[tid] = {
            'Format':tformat,
            'Description':tdesc,
            'Type':ttype,
            'Dependency':tdep,
            'Date':tdate
        }
    g = open('tdl_data.json','w')
    g.write(json.dumps(json_dict))
    g.close()

def saveData(json_contents, tdl_write):
    """ 
    Write tdl data to output file - json format
    """
    json_contents = forceRemoveEntry(json_contents)
    json_contents = cascade(json_contents)
    g = open(tdl_write,'w')
    g.write(json.dumps(json_contents))
    g.close() 
    return json_contents

def showKwargs(json_contents, cmd):
    """
    Routine for extracting kwarg information from user input cmd and displaying
    appropriate filters with showAll routine.
    """

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
    name, tpe, dep, ob = '','','',''
    for kw in kwargs:
        if 'name=' in kw:
            name = kw.replace('name=','')
        elif 'type=' in kw:
            tpe = kw.replace('type=','')
        elif 'dep=' in kw:
            dep = kw.replace('dep=','')
        elif 'orderby=' in kw:
            ob = kw.replace('orderby=','')
    showAll(json_contents, name=name, tpe=tpe, dep=dep, ob=ob)

if __name__ == '__main__':

    ## ----- Assemble data and backup paths -----

    path = os.getcwd()
    if len(sys.argv) > 1:
        tdl_data   = path + '/' + sys.argv[1] + '/data/tdl_data.json'
        tdl_backup = path + '/' + sys.argv[1] + '/data/tdl_backup.json'
    else:
        tdl_data   = path + '/data/tdl_data.json'
        tdl_backup = path + '/data/tdl_backup.json'

    ## ----- Get tdl data that currently exists -----

    if os.path.isfile(tdl_data):
        print('Found existing tdl data file')
    elif os.path.isfile(tdl_backup):
        os.system('cp {} {}'.format(tdl_backup, tdl_data))
        print('Retrieving backup tdl data')
    else:
        print('Creating new tdl data file')
        f = open(tdl_data,'w')
        f.close()

    f = open(tdl_data,'r')
    try:
        json_contents = json.load(f)
    except json.decoder.JSONDecodeError:
        json_contents = {}
        print('Current tdl data file is empty - creating blank list')
    f.close()

    # Welcome to manager
    print('\nTo Do List Manager v2.1 - dwest77\n')
    showAll(json_contents)
    # Entry for new fields
    cmd = ''
    while 'exit' not in cmd:
        cmd = input('>> ')

        # Show all entries command
        if 'show' in cmd:
            if cmd == 'show':
                showAll(json_contents)
            else:
                showKwargs(json_contents,cmd)
        # Add entry to list
        elif cmd == 'add':
            json_contents = addEntry(json_contents)
        # Remove entry from list
        elif cmd == 'rm':
            json_contents = removeEntry(json_contents)
        # Ammend existing entry by ID
        elif cmd == 'ammend':
            json_contents = ammendEntry(json_contents)
        elif cmd == 'help':
            showHelp()
        # Do nothing
        elif cmd == 'mod':
            mapOldData()
        elif cmd == '':
            pass
        # Save Entries
        elif cmd == 'reorder':
            json_contents = saveData(json_contents, tdl_data)
            showAll(json_contents)
            json_contents = reorder(json_contents)
            json_contents = saveData(json_contents, tdl_data)
        elif cmd == 'save':
            json_contents = saveData(json_contents, tdl_data)
        elif cmd == 'cascade':
            json_contents = cascade(json_contents)
        # Exit software
        elif 'exit' in cmd:
            print('Exiting')
        # Valid commands only
        else:
            print('-tdl: Unrecognised command - "{}"'.format(cmd))

    # Save data on shutdown unless specified otherwise
    if 'q' not in cmd:
        json_contents = saveData(json_contents, tdl_data)
        backup(tdl_data, tdl_backup)
        print('Shutdown and save complete')
    else:
        print('Shutdown (no save) complete')
