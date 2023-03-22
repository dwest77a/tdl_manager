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

HEADERS = ['Format','Type','Label','Current','Stage','Dependency','Date']

def getDataFormatted(file):
    f = open(file,'r')
    content = json.load(f)
    for key in content.keys():
        for head in HEADERS:
            try:
                temp = content[key][head]
            except:
                content[key][head] = ''
    return content

def getSortedIntKeys(mydict): # test with example dicts
    ## Sort integer dictionary keys into correct order of size

    raw  = mydict.keys()
    ints = []
    try:
        for key in raw:
            ints.append(int(key))
        return sorted(ints)
    except ValueError:
        print('Error: Invalid ID in dict')
        return sorted(raw)

def backup(tdl_data, tdl_backup):
    ## Copy tdl_data to backup file
    os.system(f'cp {tdl_data} {tdl_backup}')

def recombine(arr):
    ## Convert array to comma-separated string
    return ','.join(arr)

def reorder(json_contents, reorder_str=False): # test with example dicts and string
    ## Take a reorder string to rearrange old zoom ids into a new order,
    ## then reassign ids in that order.
    if reorder_str:
        new_pattern = reorder_str
    else:
        new_pattern = input("Reorder old IDs: ")

    # define new json dict
    new_p           = new_pattern.split(" ")
    json_contents_n = {}

    # Check for inconsistent new order with number of old ids
    if len(new_p) != len(json_contents):
        print('Not All IDs included in reassignment - exiting reorder')
        return json_contents

    for x, key in enumerate(getSortedIntKeys(json_contents)):
        new_key = new_p[x]
        json_contents_n[str(key)] = json_contents[new_key]

    return json_contents_n

def cascade(json_contents): # test with example dicts
    ## Reduce all ids and fill in gaps between integers
    json_new = {}
    json_con_keys = getSortedIntKeys(json_contents)
    for index, key in enumerate(json_con_keys):
        json_new[str(index)] = json_contents[str(key)]
    return json_new

def buffer(item, length): # test with strings
    ## Format a string to have a specific length and fill in additional whitespace
    buff = ''
    if len(item) >= length:
        item = item[:length]
    else:
        for x in range(0,length-len(item)):
            buff += ' '
    if '>' in item:
        return item.replace('>',buff) + ' '
    else:
        return str(item+buff)

def titleList(title=None):
    ## Print list headers with correct formatting
    today = datetime.now()
    now = today.strftime("%d/%m/%Y %H:%M:%S")
    print('')
    if title:
        print(title)
        print(buffer('',3),end="")
        print(buffer('Project',15),end="")
        print(buffer('Format',15),end="")
        print(buffer('Item',20),end="")
        print(buffer('Completion Step',60),end="")
        print(buffer('Stage',10),end="")
        print(buffer('Dependency',20),end="")
        print('Date Completed')
    else:
        print(f'To Do List: {now}')
        print(buffer('ID',3),end="")
        print(buffer('Project',15),end="")
        print(buffer('Format',15),end="")
        print(buffer('Item',20),end="")
        print(buffer('Current',60),end="")
        print(buffer('Stage',10),end="")
        print(buffer('Dependency',20),end="")
        print('Date')
    print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')

def showSelection(entry, id, name, tpe, dep, ob):
    outp = ''
    nfilter = (entry['Label'] == name or name == '')
    dfilter = (entry['Dependency'] == dep or dep == '')
    tfilter = (entry['Type'] == tpe or tpe == '')

    # Filter using kwargs for each item
    if nfilter or dfilter or tfilter:
    
        try:
            if entry['rm']:
                outp += '*'
        except:
            pass
            # entry['rm'] does not exist for most entries
        
        # Print each item with whitespace added via buffer
        outp += buffer(id,3) + \
                    buffer(entry['Type'],15) + \
                    buffer(entry['Format'],15) + \
                    buffer(entry['Label'],20) + \
                    buffer(entry['Current'],60) + \
                    buffer(entry['Stage'],10) + \
                    buffer(entry['Dependency'],20) + \
                    entry['Date'] + '\n'
    return outp

def showAll(json_contents, name='',tpe='', dep='', ob='', title=''):
    ## Show all list items in correct ordering and with specific flags

    # print list headers
    titleList(title=title)

    # For all entries, print data with correct formatting

    # New series of headings - normal, pending (dependencies), long term
    normal, pmeet, ongoing, pcheck = '','','', ''

    for id in json_contents.keys():
        entry = showSelection(json_contents[id], id, name, tpe, dep, ob)
        if 'LT' in json_contents[id]['Dependency']:
            ongoing += entry
        elif 'Meeting' in json_contents[id]['Dependency']:
            pmeet += entry
        elif json_contents[id]['Dependency'] not in ['--','']:
            pcheck += entry
        else:
            normal += entry
    # Display standard items
    print(normal)

    if pmeet != '':
        print('Pending a Meeting')
        print(pmeet)

    if pcheck != '':
        print('Pending Checks')
        print(pcheck)

    if ongoing != '':
        print('Ongoing Items')
        print(ongoing)

    print('')

def viewHistory(historyfile):
    title = 'History of Removed Items'
    f = open(historyfile,'r')
    content = f.readlines()
    f.close()
    json_contents = {}
    for x, line in enumerate(content):
        line = line.replace('true','False')
        item = eval(line.replace('\n',''))
        json_contents[str(x)] = item
    showAll(json_contents, title=title)

def addEntry(json_contents):
    ## Add new entry to json dict - take all relevant inputs from user
    today = datetime.now()
    # Extract most recent ID from latest entry
    entry_id = np.max(np.array(list(json_contents.keys()),dtype=int))+1

    # Get entry name as input and assemble date in readable format
    entry_type    = input('Project (15 char): ')
    entry_format  = input('Format (15 char): ')
    entry_label   = input('Item Label (20 char): ')
    entry_current = input('Current (60 char): ')
    entry_stage   = input('Stage (10 char): ')
    entry_dep     = input('Dependencies (20 char): ')
    entry_date    = today.strftime("%d/%m/%Y %H:%M:%S")

    # Assemble new entry str and append
    json_contents[str(entry_id)] = {
        'Format':entry_format,
        'Label':entry_label,
        'Current':entry_current,
        'Stage':entry_stage,
        'Type':entry_type,
        'Dependency':entry_dep,
        'Date':entry_date
    }
    return json_contents

def removeEntry(json_contents, id=''): # Test with id
    ## Schedule entry removals for next list save
    ## So accidental removals are reversable

    # Reshow all current entries

    is_valid = False
    
    # Accept valid entries for ID only
    while not is_valid:
        if id == '':
            id = input('Remove (ID) >> ')

        try:
            json_contents[id]['rm'] = True
            is_valid = True
        except:
            print('-tdl: Unrecognised ID - enter existing ID for removal')
            id = input('Remove (ID) >> ')

    return json_contents

def forceRemoveEntry(json_contents, path=None): # test with dict
    ## Copy all entries to a new dict
    ## Except for entries scheduled for removal
    json_hist = []
    json_new = {}
    for key in json_contents.keys():
        try:
            temp = json_contents[key]['rm']
            if not temp:
                json_new[key] = json_contents[key]
            else:
                json_contents[key]['Date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                json_hist.append(json_contents[key])
        except:
            json_new[key] = json_contents[key]
    if len(json_hist) > 0 and path:
        exportOldTasks(json_hist, path)
    return json_new

def exportOldTasks(history, tdl_path):
    # Add removed entries to an entry dump
    try:
        f = open(os.path.join(tdl_path,'history'),'r')
        content = ''.join(f.readlines())
        f.close()
    except FileNotFoundError:
        content = ''

    for entry in history:
        string = json.dumps(entry)
        content += string + '\n'
    try:
        f = open(os.path.join(tdl_path,'history'),'w')
        f.write(content)
        f.close()
    except FileNotFoundError:
        print(f'-tdl: Error saving to "history" - check {tdl_path} directory')

def ammendEntry(json_contents, id=None):
    ## Ammend existing entries with user input

    # Update alteration date to current date
    today = datetime.now()

    is_valid = False
    while not is_valid:
        if not id:
            entry_id = input('Ammend (ID) >> ')
        else:
            entry_id = id
        # Check ID is valid within dict
        try:
            old_info = dict(json_contents[entry_id])
            is_valid = True
        except:
            print('-tdl: Unrecognised ID - enter existing ID for ammendment')
            id = None
    
    # Get entry ammendments or set to old values if inputs are blank

    entry_type    = input('*Project: ')
    entry_format  = input('*Format: ')
    entry_label   = input('*Label: ')
    entry_current = input('*Current: ')
    entry_stage   = input('*Stage: ')
    entry_dep     = input('*Dependencies: ')

    if entry_type == '':
        entry_type = old_info['Type']
    if entry_format == '':
        entry_format = old_info['Format']
    if entry_label == '':
        entry_label = old_info['Label']
    if entry_current == '':
        entry_current = old_info['Current']
    if entry_stage == '':
        entry_stage = old_info['Stage']
    if entry_dep == '':
        entry_dep = old_info['Dependency']

    entry_date = old_info['Date']

    # Assemble new entry dict value
    json_contents[entry_id] = {
        'Format':entry_format,
        'Label':entry_label,
        'Current':entry_current,
        'Stage':entry_stage,
        'Type':entry_type,
        'Dependency':entry_dep,
        'Date':entry_date
    }

    return json_contents

def showHelp():
    ## Display help info from global string
    print(HELP)

def mapOldData():
    ## Map old list-style data to dict format in version 2
    ## - Deprecated since conversion is complete

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

def saveData(json_contents, tdl_write, tdl_path):
    ## Write json dict to file
    ## remove entries, cascade ids before saving.

    json_contents = forceRemoveEntry(json_contents, path=tdl_path)
    json_contents = cascade(json_contents)
    g = open(tdl_write,'w')
    g.write(json.dumps(json_contents))
    g.close() 
    return json_contents

def showKwargs(json_contents, cmd):
    ## Routine for extracting kwarg information from user input cmd and displaying
    ## appropriate filters with showAll routine.

    # Multiple kwargs extracted using char iteration
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
        historyfile = path + '/' + sys.argv[1] + '/data/history'
    else:
        tdl_data   = path + '/data/tdl_data.json'
        tdl_backup = path + '/data/tdl_backup.json'
        historyfile = path + '/data/history'

    tdl_path = tdl_data.replace('/tdl_data.json','')

    ## ----- Get tdl data that currently exists -----

    if os.path.isfile(tdl_data):
        print('Found existing tdl data file')
    elif os.path.isfile(tdl_backup):
        os.system(f'cp {tdl_backup} {tdl_data}')
        print('Retrieving backup tdl data')
    else:
        print('Creating new tdl data file')
        f = open(tdl_data,'w')
        f.close()

    try:
        json_contents = getDataFormatted(tdl_data)
    except json.decoder.JSONDecodeError:
        json_contents = {}
        print('Current tdl data file is empty - creating blank list')

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
        elif 'rm' in cmd:
            if cmd == 'rm':
                showAll(json_contents)
                json_contents = removeEntry(json_contents)
            else:
                id = cmd.split(' ')[1]
                json_contents = removeEntry(json_contents, id=id)
        # Ammend existing entry by ID
        elif 'ammend' in cmd:
            if cmd == 'ammend':
                json_contents = ammendEntry(json_contents)
            else:
                id = cmd.split(' ')[1]
                json_contents = ammendEntry(json_contents,id=id)
        elif cmd == 'help':
            showHelp()
        # Do nothing
        elif cmd == 'mod':
            mapOldData()
        elif cmd == 'history':
            if historyfile:
                viewHistory(historyfile)
            else:
                print('-tdl: No history file specified')
        elif cmd == '':
            pass
        # Save Entries
        elif cmd == 'reorder':
            json_contents = saveData(json_contents, tdl_data, tdl_path)
            showAll(json_contents)
            json_contents = reorder(json_contents)
            json_contents = saveData(json_contents, tdl_data, tdl_path)
        elif cmd == 'save':
            json_contents = saveData(json_contents, tdl_data, tdl_path)
        elif cmd == 'cascade':
            json_contents = cascade(json_contents)
        # Exit software
        elif 'exit' in cmd:
            print('Exiting')
        # Valid commands only
        else:
            print(f'-tdl: Unrecognised command - "{cmd}"')

    # Save data on shutdown unless specified otherwise
    if 'q' not in cmd:
        json_contents = saveData(json_contents, tdl_data, tdl_path)
        backup(tdl_data, tdl_backup)
        print('Shutdown and save complete')
    else:
        print('Shutdown (no save) complete')
