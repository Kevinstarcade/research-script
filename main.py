import sqlite3
import pathlib

# --- VARIABLES --- #
FILENAME = "profs_directory.db"

# --- SUBROUTINES --- #
### INPUTS
def menu():
    """
    User selects how to interact with the database
    """

    print('''
1. View all professors
2. Select a professor
3. Add professor
4. EXIT
    ''')
    choice = int(input("> "))
    return choice

def profMenu():
    print('''
What would you like to do?
    1. Edit Info
    2. View Full Email
    3. Write email
    4. Delete Professor
    5. Go Back
    ''')
    choice = int(input("> "))
    return choice

def askProfInfo(currentInfo=()):
    """
    asks user for a professor's info.
    must contain a first name
    """
    if not currentInfo:
        name = input(f"Professor's Name: ")
        email = input(f"Email: ")
        link = input(f"UofA Profile Page: ")
        text = input(f"Text of Email Being Sent: ")

    else:
        curName, curEmail, curLink, curText = currentInfo

        name = input(f"Professor's Name ({curName}): ")
        email = input(f"Email ({curEmail}): ")
        link = input(f"UofA Profile Page ({curLink}): ")
        text = input(f"Text of Email Being Sent ({curText}): ")

        name = name if name else curName
        email = email if email else curEmail
        link = link if link else curLink
        text = text if text else curText

    if name:
        return (name, email, link, text)
    else:
        print("Entry must include a name. Please try again")

def addProf(conn, profInfo):
    """
    adds profInfo into the database

    Args:
        conn (): database object
        profInfo (tuple): containing (name, email, link, text)
    """

    c = conn.cursor()

    c.execute('''
            INSERT INTO
                professors (
                    name,
                    email,
                    link,
                    text
                )
            VALUES (
                ?, ?, ?, ?
            )
        ;''', profInfo)
        
    conn.commit()
    print(f"{profInfo[0]} successfully saved!")

def deleteProf(conn, ID):
    """
    Delete a professor from the database

    Args:
        ID (int): Primary Key
    """
    c = conn.cursor()

    prof = c.execute('''
        SELECT
            name
        FROM
            professors
        WHERE
            id = ?
    ;''', [ID]).fetchone()

    # DELETE
    c.execute('''
        DELETE FROM
            professors
        WHERE
            id = ?
    ;''', [ID])

    conn.commit()

    print(f"{prof[0]} is successfully deleted.")

### PROCESSING
def setup(conn):
    """
    Create the database table on first run
    """
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS
            professors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                link TEXT,
                text TEXT
            )
    ;''')

    conn.commit()

def selectProfByName(conn):
    searchName = input("Professor Name: ")

    c = conn.cursor()
    profs = c.execute('''
        SELECT
            *
        FROM
            professors
        WHERE
            name LIKE ?
    ;''', (f'%{searchName}%',)).fetchall()

    if len(profs) == 0:
        print("There are no professors with that name.")
    elif len(profs) == 1:
        profView(conn, profs[0])
    else:
        print("There are multiple professors matching that name.")
        for i, prof in enumerate(profs, start=1):
            print(f"{i}. {prof[1]}, email: {prof[2]}")
        choice = int(input("Select Prof: "))
        profView(conn, profs[choice-1])

### OUTPUTS
def displayAllProfs(conn):
    """
    prints out all professors nicely
    """
    c = conn.cursor()
    profs = c.execute('''
        SELECT
            name
        FROM
            professors
        ORDER BY
            name
    ;''').fetchall()

    for prof in profs:
        print(prof[0])

def displayResults(results):
    """
    display search results nicely

    Args:
        results (list): 2D array
    """
    for prof in results:
        ID, name, email, link, text = prof
        print(f"Viewing {name}")
        print(f"email: {email}")
        print(f"Profile Link: {link}")
        if text:
            print(f"Email Draft: {text[:100]}...")

def main():
    firstRun = True
    if (pathlib.Path.cwd() / FILENAME).exists():
        firstRun = False

    conn = sqlite3.connect(FILENAME)

    if firstRun:
        setup(conn)
        print("setup complete!")

    while True:
        operation = menu()

        if operation == 1: # view all profs
            displayAllProfs(conn)

        elif operation == 2: # select prof
            selectProfByName(conn)

        elif operation == 3: # add prof
            profInfo = askProfInfo()
            if profInfo:
                addProf(conn, profInfo)

        else:
            exit()

def profView(conn, info):
    while True:
        print("=" * 80)
        displayResults([info])
        operation = profMenu()

        if operation == 1: # Edit Info
            print("Enter new info (leave blank for no edit)")
            newInfo = askProfInfo(info[1:])
            if newInfo:
                info = (info[0], *newInfo)
                updateProf(conn, info)

        elif operation == 2: # View Full Email (WIP)
            pass

        elif operation == 3: # Write Email using AI (WIP)
            pass

        elif operation == 4: # Delete Professor
            selectProfByName(conn)

        else: # go back
            break


def updateProf(conn, info):
    """
    User updates a professor

    Args:
        ID (int): Primary Key
    """
    c = conn.cursor()

    c.execute('''
        UPDATE
            professors
        SET
            name = ?, 
            email = ?, 
            link = ?, 
            text = ?
        WHERE
            id = ?
    ;''', (*info[1:], info[0]))

    conn.commit()
    print(f"{info[1]} successfully updated!")

# --- MAIN PROGRAM CODE --- #
if __name__ == "__main__":
    main()