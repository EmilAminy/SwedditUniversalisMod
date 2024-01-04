input_file = open('ambient_object.txt', 'r')
new_file_content = ''
search_parameter = 'position={'

while True:
    line = input_file.readline()
    
    if line == '':
        with open('ambient_object-modified.txt', 'w') as f:
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
            if coordinate == float(splitted_line[0]):
                coordinate = coordinate - 2304
            line = ''
            if coordinate == float(splitted_line[line_length-1]):
                new_file_content = new_file_content + str(coordinate) + '\n'
            else:
                new_file_content = new_file_content + str(coordinate) + ' '
    new_file_content = new_file_content + str(line)