import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:8000')

while True:
    print('1. Add a note')
    print('2. Get notes')
    print('3. Search on Wikipedia')
    print('q. Quit')
    choice = input('Option: ')
    if choice == '1':
        topic = input('Topic: ')
        words = input('Note: ')
        timestamp = input('Timestamp: ')
        try: 
            print(server.addNote(topic, words, timestamp))
        except ConnectionError:
            print('Error: Unable not connect to server')
        except xmlrpc.client.Fault as error:
            print('Error:', error.faultString)

    elif choice == '2':
        topic = input('Topic: ')
        try:
            notes = server.getNotes(topic)
            if isinstance(notes, list):
                print('\n'.join(notes))
            else:
                print(notes)
        except ConnectionError:
            print('Error: Unable not connect to server')
        except xmlrpc.client.Fault as error:
            print('Error:', error.faultString)

    elif choice == '3':
        topic = input('Topic: ')
        term = input('Search term: ')
        try: 
            link = server.wiki(term)
            if link:
                timestamp = input('Timestamp: ')
                print(server.addNote(topic, link, timestamp))
            else:
                print('None found.')
        except ConnectionError:
            print('Error: Unable not connect to server')
        except xmlrpc.client.Fault as error:
            print('Error:', error.faultString)

    elif choice == 'q':
        break
    else:
        print('Invalid choice.')