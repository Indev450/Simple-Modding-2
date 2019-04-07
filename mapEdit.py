import json
# its don't work. I will try fix it... someday...
command = ''
level = ['']
spawn = [0,0,0]
current = 0

('w','s','n','spawn')

def readCommand(command):
    global level
    global spawn
    global current

    tmpword = ''
    words = command.split()
    print(words)
    
    for word in words:
        
        if tmpword == 'w':
            for i in range(int(word)):
                level[current] += '-'
            tmpword = ''
        if tmpword == 's':
            for i in range(int(word)):
                level[current] += ' '
            tmpword = ''
        if tmpword == 'n':
            current += 1
            level.append('')
            tmpword = ''
            
        if word == 'w':
            tmpword = 'w'
            continue
        if word == 's':
            tmpword = 's'
            continue
        if word == 'n':
            tmpword = 'n'
            continue

while True:
    commands = input('>>> ')
    if commands == 'end':
        break
    else:
        readCommand(commands)

print(level)
file = open(input('Map name >>> ') + '.json', 'w')
data = {
    'level':level
    }
json.dump(data, file)
file.close()
