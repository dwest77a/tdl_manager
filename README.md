# tdl_manager
A simple python tool for managing To Do Lists
Updated 21/09/2022

## Future Additions:
 - Add priority to List items, then able to sort by priority
 - Add progress percentage/fraction - string entry

## Example diagram
```mermaid
classDiagram
    tdlman <|-- tdl_data
    tdlman <|-- tdl_backup
    tdl_data <|-- tdl_entry
    tdl_backup <|-- tdl_entry
    tdl_entry: str name 
    tdl_entry: str project
    tdl_entry: int id
    tdl_entry: datetime date
    tdl_entry: str dependencies
```