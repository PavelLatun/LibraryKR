from enum import Enum


class Actions(Enum):
    Exit = "exit"
    AddBook = "add"
    RemoveBook = "remove"
    EditBook = "edit"
    FindBook = "find"
    PrintAt = "print"
    PrintAll = "print all"
    Back = "back"
    Undo = "undo"

    SetAuthor = "author"
    SetYear = "year"
    SetTitle = "title"
    ClearParams = "clear"

    SetId = "id"

    Execute = "execute"

    Return = "Что-нибудь"
