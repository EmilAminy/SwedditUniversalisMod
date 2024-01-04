input_file = open('00_tradenodes.txt', 'r')
new_file_content = ''
search_parameter = 'control={'

while True:
    line = input_file.readline()
    
    if line == '':
        with open('00_tradenodes-modified.txt', 'w') as f:
            f.write(new_file_content)
            f.close()
        print('textfile generated')
        break
    if search_parameter in line:
        line = input_file.readline()
        new_file_content = new_file_content + '		' + search_parameter + '\n' + '			'

        splitted_line = line.split()
        line_length = len(splitted_line)

        for x in range (0, line_length):
            coordinate = float(splitted_line[x])
            if (x % 2) == 0:
                coordinate = coordinate - 2304
                line = ''
            new_file_content = new_file_content + str(coordinate) + ' ' 
    new_file_content = new_file_content + str(line) + '\n'