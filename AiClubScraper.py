from bs4 import BeautifulSoup
import os
import datetime
import PyPDF2

directory = '' #insert directory of files to read here



#--------------------------------functions --------------------------------

def html_reader(HTMLFile): 


    #gets a list of paragraphs in a singular HTML File, and returns it


    global counter

    HTML_paragraphs_list = []

    content = HTMLFile.read() # gets content of file

    soup = BeautifulSoup(content,"html.parser") # using beautiful soup to be able to navigate & easily identify P tags in the html content

    for i in soup.findAll('p'): # finds and loops through each <p> tag in the html
        counter+=1
        if len(i) < 5 or  "cookie" in i: #here it filters for any sentence we don't want. Currently only short words & sentences containing 'cookie', however can be expanded and finetuned
            pass
        else:
            print("new append")
            print(i)
            HTML_paragraphs_list.append(i.getText().replace("\n", "").replace("\t", "")) # if paragraph is deemed as valid, we add it to a list
    
    return HTML_paragraphs_list #return the list of paragraphs in the html file

def pdf_reader(PDFFile): 


    #gets a list of paragraphs in a singular PDF File, and returns it


    with open(PDFFile, 'rb') as pdf: #opens the passed in pdf file
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_paragraphs_list = []

        for page in reader.pages: #goes per page in the pdf
            content = page.extract_text() #extracts all the text present in the page in one go. does not sort by paragraphs.
            
            pdf_paragraphs_list.append(content) #adds the text to a list
    
    return pdf_paragraphs_list #returns a list of all the content present in a pdf file



#--------------------------------main code------------------------------------

total_paragraph_list = []
counter = 0

for filename in os.listdir(directory): # gets the name of each file in the directory, and loops through each one
    print(filename)
    print("new file opened")
    f = os.path.join(directory, filename) # gets the full path of the file by joining the directory inputted above & file name into one path

    if os.path.isfile(f): # checking if it is a file

        if "html" in filename: #checking if the file is an html file
            
            HTMLFile = open(f,encoding="utf-8")
            total_paragraph_list.extend(html_reader(HTMLFile)) #calls html reader, which extracts paragraphs from an html file. Then adds on the returned list from function onto an overall list of paragraphs

        if "pdf" in filename: #checking if the file is a pdf file

            total_paragraph_list.extend(pdf_reader(f)) #calls html reader, which extracts paragraphs from an html file. Then adds on the returned list from function onto an overall list of paragraphs
            
print(counter," added") # prints the number of sentences added

unique_id = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S') #gets the current time
with open("Paragraphs {0}.txt".format(unique_id), "w", encoding='utf-8') as output: #writes each sentence spaced apart in a new txt document with the current time in its' name, to seperate each text document written
    for i in total_paragraph_list: #loops through list of all paragraphs to add them one by one
        output.write(str(i))
        output.write("\n\n")
    
