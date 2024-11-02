from pathlib import Path
import re
import os

class FileHandler:
  def __init__(self, path):
    self.path = path
    self.file_path = Path(self.path)
    self.cur_dir = os.getcwd()
    self.nameList = self.createTempFile()
    self.addNameToList()
    self.file_dict = {}

  def addNameToList(self):  # add all the file names in the list.txt file
    listFile = open(self.nameList, 'w')
    for file in self.file_path.iterdir():
      remove_number = re.sub(r'^[^A-Za-z]+', '', file.name)
      listFile.write(f"{remove_number}\n")
    listFile.close()

  def remove_number(self):
    for name in self.file_path.iterdir():

      _, *splittedName = name.name.split("-")
      if not _.isdigit():
        continue
      freshName = ' '.join(splittedName[1::])
      self.nameRemover(name, freshName)

  def nameRemover(self,old_file_path, changedName):  #changes the name of the pdf files
    old_file = Path(old_file_path)
    new_file = old_file.with_name(changedName)  # Change the file name
    old_file.rename(new_file)

  def makeDict(self):
    textFile = open(self.nameList, 'r')
    count = 1
    for line in textFile.readlines():
      file = self.fixListName(line)
      name = file.split(' ')
      if name[0].isdigit():
        order = int(name[0])
      else:
        order = count
      name = ' '.join(name[1::])
      self.file_dict[order] = name
      count += 1

  def fixListName(self,text):
    text = text.strip('\n')
    text = re.sub(r'[^A-Za-z0-9]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()
    
  def createTempFile(self):  #creates a text file "list.txt" 
    tempPath = self.cur_dir
    listFilePath = f"{tempPath}\\list.txt"
    newPath = open(listFilePath, 'w')
    newPath.close()
    return listFilePath
  
  def nameFixed(self,filename): #removes any number, symbols or extra space
    
    filename = re.sub(r'[^A-Za-z]', ' ', filename)
    filename = re.sub(r'(?<!^)([A-Z])', r' \1', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename
  
  def nameChanger(self,old_file_path,order_number):  #changes the name of the pdf files
    old_file = Path(old_file_path)
    old_seq_remove = re.sub(r'^[^A-Za-z]+', '', old_file.name)
    new_file = old_file.with_name(f"{order_number}-{old_seq_remove}")  # Change the file name
    old_file.rename(new_file)
    
  def matcher(self,filename):  # matches the file name with the with files name
    filename = self.nameFixed(filename)
    match = re.match(r'(\w+[-_]?\w*)\s+(\w+[-_]?\w*)\s', filename)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return None

  def main(self):  #main function that handles grouping and doing everything
    if len(self.file_dict) == 0:
      self.makeDict()

    for file in self.file_path.iterdir():
      from_file = self.matcher(file.name)
      if not from_file:
        continue
      for order_number, name_list in self.file_dict.items():
        new_name = self.matcher(name_list)
        if not new_name: 
          continue

        if from_file.lower() == new_name.lower():
          self.nameChanger(file,order_number)

if __name__ == "__main__":
  # filePath = input("Enter the folder path: ")
  filePath = r"E:\Papers\papers"
  fileHandler = FileHandler(filePath)
  gptInput = input("[Y] if you changed the 'list.txt' file with gpt review:")
  if gptInput.lower() == 'y':
    fileHandler.main()
    print("File names have been changed.")
  else:
    print("Execution filed")
  # fileHandler.remove_number()