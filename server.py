import xmlrpc.server
import xml.etree.ElementTree as ET
import requests

class Notebook:
    def __init__(self):
        self.notes = ET.parse('db.xml')
    
    def addNote(self, topic, words, timestamp):
        notes = self.notes.getroot()
        note = notes.find("./note[@topic='{}']".format(topic))
        if note is None:
            note = ET.Element('note')
            note.set('topic', topic)
            notes.append(note)

        data = ET.Element('data')
        data.set('timestamp', timestamp)
        data.text = words
        note.append(data)
        self.notes.write('db.xml')
        return ('Note added')

    def getNotes(self, topic):
        notes = self.notes.getroot()
        note = notes.find("./note[@topic='{}']".format(topic))
        if note is None:
            return ('No such topic')
        else:
            d = note.findall('data')
            return ([data.text for data in d])
    
    def wiki(self, term):
        URL = 'https://en.wikipedia.org/w/api.php'
        params = {
            'action': 'opensearch',
            'namespace': 0,
            'search': term,
            'limit': 1,
            'format': 'json'
        }

        re = requests.get(url=URL, params=params)
        if re.status_code == 200:
            wiki = re.json()
            if len(wiki) > 1 and len(wiki[1]) > 0:
                link = wiki[2][0]
                link = 'Wikipedia link: ' + wiki[3][0]
                return link   
        return ('None found.')

def serve(port):
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', port))
    server.register_instance(Notebook())
    print('Server listening on port '+ str(port))
    server.serve_forever()

if __name__ == '__main__':
    serve(8000)