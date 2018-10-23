#file: InventoryManagement
#Steven Luu Student ID# 400084241
#1XA3 Final Project: Inventory Management
#Date: April 09 2017

#import basic tkinter GUI
from tkinter import * 
from tkinter import ttk

#import file dialog which allows user to select/save a file
from tkinter.filedialog import askopenfilename,asksaveasfilename

#import message boxes
from tkinter import messagebox

#Item class that contains the 5 attributes of an item
class Item:

  #assign attributes of the object
  def __init__(self,itemNumber,itemQuantity,itemName,itemLocation,itemDescription):
    self.number=itemNumber
    self.quantity=itemQuantity
    self.name=itemName
    self.location=itemLocation
    self.description=itemDescription

  #Gets and Sets for each attribute
  def GetNumber(self):
    return self.number

  def GetQuantity(self):
    return self.quantity

  def GetName(self):
    return self.name

  def GetLocation(self):
    return self.location

  def GetDescription(self):
    return self.description

  def SetQuantity(self,x):
    self.quantity=x

  def SetName(self,x):
    self.name=x

  def SetLocation(self,x):
    self.location=x

  def SetDescription(self,x):
    self.description=x

#empty list that will store all Item objects 
items=[]

#checks if the number and quantity are natural numbers (including 0)
def checkEntries():
    assert isinstance(eval(tempNumber.get()),int)
    assert isinstance(eval(tempQuantity.get()),int)
    assert eval(tempNumber.get())>=0
    assert eval(tempQuantity.get())>=0

#deletes anything typed on all entry boxes and sets its respective text variable blank
def clearEntries():
  numberEntry.delete(0,'end')
  quantityEntry.delete(0,'end')
  tempNumber.set(0)
  tempQuantity.set(0)
  numberEntry.delete(0,'end')
  quantityEntry.delete(0,'end')
  tempName.set('')
  tempLocation.set('')
  tempDescription.set('')

#creates a new item when the 'New' button is pressed (it must have a specified number and quantity)
#the list is then sorted to ascending order based on item number
def newItem():
  #try catch is used to grab any errors with entering wrong infomation. A message box will prompt accordingly
  try:
    checkEntries()
    items.append(Item(eval(tempNumber.get()),eval(tempQuantity.get()),tempName.get(),tempLocation.get(),tempDescription.get()))
    mergeSort(items)
    clearEntries()
    messagebox.showinfo(title='Inventory Management',message='Item successfully added!')
  except:
    messagebox.showinfo(title='Inventory Management',message='Please fill in all valid entries')
  
#deletes an item from the items list
def deleteItem():
  scan=False #boolean is used to prompt with an error messagebox only if it couldn't find anything
  #enumerate for loop that searches for a specific item number and pops it from the list
  for i,item in enumerate(items):
    if item.GetNumber()==eval(tempNumber.get()):
      scan=True
      #confirmation message box, if the user clicks yes then the if statement is true (and vice versa)
      if messagebox.askquestion(title='Confirmation',message='Are you sure?'):
        items.pop(i)
        messagebox.showinfo(title='Inventory Management',message='Item deleted successfully') #prompt user that deletion was successful
  if scan==False:
    messagebox.showinfo(message='Could not find item with specified item number')

#searches an item based on its item number. If an item is found it will display the rest of the item's attributes on the entry boxes
def searchItem():
  #binary search is used to quickly find the item number's position in the list
  value=binarySearch(eval(tempNumber.get()),items)
  #fill in the entry boxes if the binary search has found the item (-1 means it did not find an item)
  if value != -1:
    tempQuantity.set(items[value].GetQuantity())
    tempName.set(items[value].GetName())
    tempLocation.set(items[value].GetLocation())
    tempDescription.set(items[value].GetDescription())
  #prompt user that there isn't an item with that item number
  else:
    messagebox.showinfo(message='Could not find item with specified item number')

#modified binary search for finding the position of an item based off its item number
def binarySearch(x,nums):
  low=0
  high=len(nums)-1
  while low <= high:
    mid=(low+high)//2
    item=nums[mid].GetNumber() #.GetNumber() is used because item number is all we're looking for in the object
    if x==item:
      return mid
    elif x < item:
      high=mid-1
    else:
      low=mid+1
  return -1

#merge lst1 and lst2 to lst3
def merge(lst1,lst2,lst3):
  #these indexes keep track of current position in each list
  i1,i2,i3=0,0,0
  n1,n2=len(lst1),len(lst2)

  #loop while both lst1 and lst2 have more items
  while i1<n1 and i2<n2:
    if lst1[i1].GetNumber()<lst2[i2].GetNumber():
      lst3[i3]=lst1[i1]
      i1+=1
    else:
      lst3[i3]=lst2[i2]
      i2+=1
    i3+=1

  #copy remaining items (if any) from lst1
  while i1<n1:
    lst3[i3]=lst1[i1]
    i1+=1
    i3+=1

  #copy remaining items (if any) from lst2
  while i2<n2:
    lst3[i3]=lst2[i2]
    i2+=1
    i3+=1

#Puts the items in ascending order, a more simple way of sorting however would be just: items.sort(key=lambda x: x.GetNumber())
def mergeSort(items):
  n=len(items)
  #Do nothing if items contains 0 or 1 items
  if n>1:
    #split in to two sublists
    m=n//2
    items1,items2=items[:m],items[m:]
    #recursively sort each piece
    mergeSort(items1)
    mergeSort(items2)
    #merge the sorted pieces back into original list
    merge(items1,items2,items)

#searches if such number is in the items list, if so then update all its values based on what the user wrote in the entry boxes
def updateItem():
  #try/catch is used to find errors for entering number and quantity entry boxes incorrectly
  try:
    checkEntries()
    value=binarySearch(eval(tempNumber.get()),items)
    #update an item's attributes if the binary search found an item, otherwise prompt the user that the item is not in the items list
    if value != -1:
      items[value].SetQuantity(tempQuantity.get())
      items[value].SetName(tempName.get())
      items[value].SetLocation(tempLocation.get())
      items[value].SetDescription(tempDescription.get())
      messagebox.showinfo(title='Inventory Management',message='Item updated successfully.') #prompt user that the update was successful
    else:
      messagebox.showinfo(message='Could not find item with specified item number') 
  except:
    messagebox.showinfo(message='Please use correct formatting')

#load a txt file (prompts with an error if file selected isn't) containing item(s). Must be in the format in the example used in the Project Outline
def loadItem():
  path=askopenfilename() #finds the file path of the file being loaded
  #try catch is used to make sure the program doesn't crash if the user selects an incorrect file type or if the text file is formmated incorrectly
  try:
    myFile=open(path,'r') #file input
    #reads the text file one line at a time (since every line is an item)
    for line in myFile.readlines():
      l=line.split(',') #split the string into a list of strings. A new element is made every comma
      #set the entry text variables to be based off the list of strings and create a new item (essentially the same code from newItem()
      tempNumber.set(l[0])
      tempQuantity.set(l[1])
      tempName.set(l[2])
      tempLocation.set(l[3])
      tempDescription.set(l[4])
      checkEntries()
      items.append(Item(eval(tempNumber.get()),eval(tempQuantity.get()),tempName.get(),tempLocation.get(),tempDescription.get()))
      mergeSort(items) #sort the list of items
    #If all goes well, clear the entries and prompt the user that the information was successfully imported
    clearEntries()
    myFile.close()
    messagebox.showinfo(title='Inventory Management',message='Successfully imported items')
  except:
    clearEntries()
    messagebox.showinfo(title='Error',message='Incorrect file or formatting of text in file')

#save all items in the list as a text file
def saveItem():
  path=asksaveasfilename(defaultextension=".txt") #find the user's preferred place to save
  #try catch is used in case the user tries to save in a filetype that isn't .txt
  try:
    myFile=open(path,'w') #file output
    #write a line of text for every item in the list
    for item in items:
      item.SetDescription(item.GetDescription().replace('\n','')) #this is implemented to prevent any blank lines when printing
      print(str(item.GetNumber())+','+str(item.GetQuantity())+','+item.GetName()+','+item.GetLocation()+','+item.GetDescription(),file=myFile)
    myFile.close()
    messagebox.showinfo(title='Inventory Management',message='Successfully saved items')
  except:
    messagebox.showinfo(title='Error',message='Save Failed')

#the update button will only be enabled if all entry boxes are filled with something
def checkUpdateState():
  if tempNumber.get() and tempQuantity.get() and tempName.get() and tempLocation.get() and tempDescription.get():
    updateButton.config(state=NORMAL)
  else:
    updateButton.config(state=DISABLED)

#default GUI
root=Tk()
root.title('Inventory Management')
mainframe = ttk.Frame(root,padding='5 5 5 5')
mainframe.grid(column=0,row=0,sticky='NWES')
mainframe.grid_rowconfigure(0,weight=1)
mainframe.grid_columnconfigure(0,weight=1)

#all variables, labels and entry boxes for the 5 attributes in an item
#.trace is a method that runs a function everytime the entry box's text variable is changed
#Lambda x,y,z is used to prevent it from running at the start of the program. x,y,z parameters aren't used but are required for lambda to work in this case
tempNumber=StringVar()
tempNumber.trace('w',lambda x,y,z:checkUpdateState())
numberLabel=ttk.Label(mainframe,text="Item Number: ",background='red')
numberLabel.grid(column=0,row=0,sticky=(W,E))
numberEntry=ttk.Entry(mainframe,text=tempNumber,width=15)
numberEntry.grid(column=1,row=0)

tempQuantity=StringVar()
tempQuantity.trace('w',lambda x,y,z:checkUpdateState())
quantityLabel=ttk.Label(mainframe,text="Item Quantity: ",background='yellow')
quantityLabel.grid(column=0,row=1,sticky=(W,E))
quantityEntry=ttk.Entry(mainframe,text=tempQuantity,width=15)
quantityEntry.grid(column=1,row=1)

tempName=StringVar()
tempName.trace('w',lambda x,y,z:checkUpdateState())
nameLabel=ttk.Label(mainframe,text="Item Name: ",background='green')
nameLabel.grid(column=0,row=2,sticky=(W,E))
nameEntry=ttk.Entry(mainframe,text=tempName,width=15)
nameEntry.grid(column=1,row=2)

tempLocation=StringVar()
tempLocation.trace('w',lambda x,y,z:checkUpdateState())
locationLabel=ttk.Label(mainframe,text="Item Location: ",background='blue')
locationLabel.grid(column=0,row=3,sticky=(W,E))
locationEntry=ttk.Entry(mainframe,text=tempLocation)
locationEntry.grid(column=1,row=3,columnspan=3,sticky=(W,E))

tempDescription=StringVar()
tempDescription.trace('w',lambda x,y,z:checkUpdateState())
descriptionLabel=ttk.Label(mainframe,text="Item Description: ",background='purple')
descriptionLabel.grid(column=0,row=4,sticky=(W,E))
descriptionEntry=ttk.Entry(mainframe,text=tempDescription)
descriptionEntry.grid(column=1,row=4,columnspan=3,sticky=(W,E))

#all buttons for the 5 attributes in an item. They are commanded to their respective purpose
newButton=ttk.Button(mainframe,text='New',command=lambda:newItem())
newButton.grid(column=2,row=0)

deleteButton=ttk.Button(mainframe,text='Delete',command=lambda:deleteItem())
deleteButton.grid(column=2,row=1)

searchButton=ttk.Button(mainframe,text='Search',command=lambda:searchItem())
searchButton.grid(column=2,row=2)

updateButton=ttk.Button(mainframe,text='Update',state=DISABLED,command=lambda:updateItem())
updateButton.grid(column=3,row=0)

loadButton=ttk.Button(mainframe,text='Load',command=lambda:loadItem())
loadButton.grid(column=3,row=1)

saveButton=ttk.Button(mainframe,text='Save',command=lambda:saveItem())
saveButton.grid(column=3,row=2)

root.mainloop()
