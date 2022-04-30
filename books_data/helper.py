import csv
file = open('books_data\\books_new.csv')
csvreader = csv.reader(file)
next(csvreader, None)

file1 = open("books data\\data.csv", "a")  # append mode


for row in csvreader:
    # rows.append(row)
    print(row[0],row[1],row[2])
    file1.write(f"{row[0]}; {row[1]}; {row[2]} \n")

file.close()
file1.close()