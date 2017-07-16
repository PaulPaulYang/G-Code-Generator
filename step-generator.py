# -*- coding: UTF-8 -*- 
#!/usr/bin/env python
version = 'PY.1.4.1'
# python face.py
# Dec 4 2007
# Face G-Code Generator for LinuxCNC

from Tkinter import *
from tkFileDialog import *
from math import *
from SimpleDialog import *
from ConfigParser import *
from decimal import *
import tkMessageBox
import os




class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width=700, height=400, bd=1)
        self.grid()
        self.createMenu()
        self.createWidgets()
        
    def createMenu(self):
        #Create the Menu base
        self.menu = Menu(self)
        #Add the Menu
        self.master.config(menu=self.menu)
        #Create our File menu
        self.FileMenu = Menu(self.menu)
        #Add our Menu to the Base Menu
        self.menu.add_cascade(label='File', menu=self.FileMenu)
        #Add items to the menu
        self.FileMenu.add_command(label='New', command=self.Simple)
        self.FileMenu.add_command(label='Open', command=self.Simple)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Quit', command=self.quit)
        
        self.EditMenu = Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.EditMenu)
        self.EditMenu.add_command(label='Copy', command=self.CopyClpBd)
        self.EditMenu.add_command(label='Select All', command=self.SelectAllText)
        self.EditMenu.add_command(label='Delete All', command=self.ClearTextBox)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label='Preferences', command=self.Simple)
        self.EditMenu.add_command(label='NC Directory', command=self.NcFileDirectory)
        
        self.HelpMenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.HelpMenu)
        self.HelpMenu.add_command(label='Help Info', command=self.HelpInfo)
        self.HelpMenu.add_command(label='About', command=self.HelpAbout)

    def createWidgets(self):
        
        self.sp1 = Label(self)
        self.sp1.grid(row=0)

        
        self.st1 = Label(self, text='进给轴起始值 ')
        self.st1.grid(row=1, column=0, sticky=E)
        self.StartVar = StringVar()
        self.Start = Entry(self, width=10, textvariable=self.StartVar)
        self.Start.grid(row=1, column=1, sticky=W)

        self.st1a = Label(self, text='进给轴终止值 ')
        self.st1a.grid(row=2, column=0, sticky=E)
        self.StopVar = StringVar()
        self.Stop = Entry(self, width=10, textvariable=self.StopVar)
        self.Stop.grid(row=2, column=1, sticky=W)


        self.st2 = Label(self, text='每次切削量 ')
        self.st2.grid(row=3, column=0, sticky=E)
        self.DepthOfCutVar = StringVar()
        self.DepthOfCut = Entry(self, width=10, textvariable=self.DepthOfCutVar)
        self.DepthOfCut.grid(row=3, column=1, sticky=W)


        self.st4 = Label(self, text='Z轴安全高度')
        self.st4.grid(row=4, column=0, sticky=E)
        self.ZsafeVar = StringVar()
        self.Zsafe = Entry(self, width=10, textvariable=self.ZsafeVar)
        self.Zsafe.grid(row=4, column=1, sticky=W)
        self.ZsafeVar.set(10)

       

        
        self.st6 = Label(self, text='进给速率 Feedrate ')
        self.st6.grid(row=1, column=2, sticky=E)
        self.FeedrateVar = StringVar()
        self.Feedrate = Entry(self, width=10, textvariable=self.FeedrateVar)
        self.Feedrate.grid(row=1, column=3, sticky=W)
        self.FeedrateVar.set(440)

        self.st7 = Label(self, text='M3 主轴速度 RPM ')
        self.st7.grid(row=2, column=2, sticky=E)
        self.SpindleRPMVar = StringVar()
        self.SpindleRPM = Entry(self, width=10, textvariable=self.SpindleRPMVar)
        self.SpindleRPM.grid(row=2, column=3, sticky=W)
        self.SpindleRPMVar.set(600)

        self.st3 = Label(self, text='总共切削量 ')
        self.st3.grid(row=3, column=2, sticky=E)
        self.TotalToRemoveVar = StringVar()
        self.TotalToRemove = Entry(self, width=10, textvariable=self.TotalToRemoveVar, state='readonly')
        self.TotalToRemove.grid(row=3, column=3, sticky=W)



        self.st9=Label(self,text='进给轴')
        self.st9.grid(row=1,column=5)
        XYZOptions=[('Z轴',2),('X轴',3),('Y轴',4)]
        self.XYZVar=IntVar()
        for text, value in XYZOptions:
            Radiobutton(self, text=text,value=value,
                variable=self.XYZVar,indicatoron=0,width=11,)\
                .grid(row=value, column=5)
        self.XYZVar.set(2)



        
        self.spacer3 = Label(self, text='')
        self.spacer3.grid(row=6, column=0, columnspan=4)

        self.spacer3 = Label(self, text='')
        self.spacer3.grid(row=7, column=0, columnspan=4)
        
        self.g_code = Text(self,width=30,height=30,bd=3)
        self.g_code.grid(row=9, column=0, columnspan=5, sticky=E+W+N+S)
        self.tbscroll = Scrollbar(self,command = self.g_code.yview)
        self.tbscroll.grid(row=9, column=5, sticky=N+S+W)
        self.g_code.configure(yscrollcommand = self.tbscroll.set) 

        self.sp4 = Label(self)
        self.sp4.grid(row=10)
        

               


               
        self.GenButton = Button(self, text='生成 G-Code',command=self.GenCode)
        self.GenButton.grid(row=10, column=0)
        
        self.CopyButton = Button(self, text='Select All & Copy',command=self.SelectCopy)
        self.CopyButton.grid(row=10, column=1)
        
        self.WriteButton = Button(self, text='Write to File',command=self.WriteToFile)
        self.WriteButton.grid(row=10, column=2)

        self.CopyButton = Button(self, text='清空输出',command=self.ClearOutput)
        self.CopyButton.grid(row=10, column=3)

        self.CopyButton = Button(self, text='Quit',command=self.quit)
        self.CopyButton.grid(row=10, column=5)
   





    def GenCode(self):
        """ Generate the G-Code for facing a part 
        assume that the part is at X0 to X+, Y0 to Y+"""
        D=Decimal
        # Calculate the start position 1/2 the tool diameter + 0.100 in X and Stepover in Y





        self.Step = self.FToD(self.DepthOfCutVar.get())
        
        self.Start = float(self.StartVar.get())
        self.Stop = float(self.StopVar.get())
        #for debug
        # print ("The value of self.Start = ",self.Start)
        # print ("The value of self.Stop = ",self.Stop)
        # print ("The value of FToD.self.Start = ",self.FToD(self.StartVar.get()))
        # print ("The value of FToD.self.Stop = ",self.FToD(self.StopVar.get()))
        #for debug
        self.Total = abs(self.Stop - self.Start)


        if len(self.DepthOfCutVar.get())>0:
            # self.Y_Step = self.FToD(self.DepthOfCutVar.get())
            self.NumOfSteps = self.Total / float(self.DepthOfCutVar.get())
            if self.Total % float(self.DepthOfCutVar.get()) > 0:
                self.NumOfSteps = self.NumOfSteps + 1
        else:
            self.Step = 0
            self.NumOfSteps = 1
        #for debug
        # print ("The value of self.NumOfSteps = ",int(self.NumOfSteps))
        #for debug
        self.Position = self.Start

        self.TotalToRemoveVar.set(self.Total)



        # Generate the G-Codes

        self.g_code.insert(END, 'G21 ')
        if len(self.SpindleRPMVar.get())>0:
            self.g_code.insert(END, 'S%i ' %(self.FToD(self.SpindleRPMVar.get())))
            self.g_code.insert(END, 'M3 ')
        if len(self.FeedrateVar.get())>0:
            self.g_code.insert(END, 'F%s\n' % (self.FeedrateVar.get()))
        self.g_code.insert(END, 'G0 Z%s\n'  % (self.ZsafeVar.get()))
        # self.g_code.insert(END, 'G0 X0 Y0\n')
        # self.g_code.insert(END, 'G0 X%.4f Y%.4f\n' %(self.X_Start, self.Y_Start))
        self.g_code.insert(END, 'G1 Z%.4f\n' %(self.Position))
        for i in range(int(self.NumOfSteps)):            
            # self.g_code.insert(END, 'Debug X_Total%.4f X_Postion%.4f X_Step%.4f\n' %(self.X_Total, self.X_Position, self.X_Step))
            if self.Step>0 and abs(self.Stop - self.Position)>= self.Step:
                if (self.Stop < self.Start):
                    self.Position = self.Position - float(self.Step)
                else:
                    self.Position = self.Position + float(self.Step)        
            else:
                self.Position = self.Stop  

            if self.XYZVar.get()==2:   #进给Z
                self.g_code.insert(END, 'G1 Z%.4f\n' % (self.Position))

            if self.XYZVar.get()==3:  #进给X
                self.g_code.insert(END, 'G1 X%.4f\n' % (self.Position))

            if self.XYZVar.get()==4:  #进给Y
                self.g_code.insert(END, 'G1 Y%.4f\n' % (self.Position))
            
            self.g_code.insert(END, 'M98 P1107 L1\n')

        self.g_code.insert(END, 'G0 Z%s\n'  % (self.ZsafeVar.get()))
        if len(self.SpindleRPMVar.get())>0:
            self.g_code.insert(END, 'M5\n')
        self.g_code.insert(END, 'G0 X0.0000 Y0.0000\nM30\n')
 #Begin of subprograme 
        self.g_code.insert(END, 'O1107\n')
        self.g_code.insert(END, '(sub programe start)\n')
        self.g_code.insert(END, '(......)\n')
        self.g_code.insert(END, '(sub programe stop)\n')
        self.g_code.insert(END, 'M99\nM30\n')


    def FToD(self,s): # Float To Decimal
        """
        Returns a decimal with 4 place precision
        valid imputs are any fraction, whole number space fraction
        or decimal string. The input must be a string!
        """
        s=s.strip(' ') # remove any leading and trailing spaces
        D=Decimal # Save typing
        P=D('0.0001') # Set the precision wanted
        if ' ' in s: # if it is a whole number with a fraction
            w,f=s.split(' ',1)
            w=w.strip(' ') # make sure there are no extra spaces
            f=f.strip(' ')
            n,d=f.split('/',1)
            return D(D(n)/D(d)+D(w)).quantize(P)
        elif '/' in s: # if it is just a fraction
            n,d=s.split('/',1)
            return D(D(n)/D(d)).quantize(P)
        return D(s).quantize(P) # if it is a decimal number already

    def GetIniData(self,FileName,SectionName,OptionName):
        """
        Returns the data in the file, section, option if it exists
        of an .ini type file created with ConfigParser.write()
        If the file is not found or a section or an option is not found
        returns an exception
        """
        self.cp=ConfigParser()
        try:
            self.cp.readfp(open(FileName,'r'))
            try:
                self.cp.has_section(SectionName)
                try:
                    IniData=self.cp.get(SectionName,OptionName)
                except ConfigParser.NoOptionError:
                    raise Exception,'NoOptionError'
            except ConfigParser.NoSectionError:
                raise Exception,'NoSectionError'
        except IOError:
            raise Exception,'NoFileError'
        return IniData
        
    def WriteIniData(self,FileName,SectionName,OptionName,OptionData):
        """
        Pass the file name, section name, option name and option data
        When complete returns 'sucess'
        """
        self.cp=ConfigParser()
        try:
            self.fn=open(FileName,'a')
        except IOError:
            self.fn=open(FileName,'w')
        if not self.cp.has_section(SectionName):
            self.cp.add_section(SectionName)
        self.cp.set(SectionName,OptionName,OptionData)
        self.cp.write(self.fn)
        self.fn.close()

    def GetDirectory(self):
        self.DirName = askdirectory(initialdir='/home',title='Please select a directory')
        if len(self.DirName) > 0:
            return self.DirName 
       
    def CopyClpBd(self):
        self.g_code.clipboard_clear()
        self.g_code.clipboard_append(self.g_code.get(0.0, END))

    def WriteToFile(self):
        try:
            self.NcDir = self.GetIniData('face.ini','Directories','NcFiles')
            self.NewFileName = asksaveasfile(initialdir=self.NcDir,mode='w', \
                master=self.master,title='Create NC File',defaultextension='.ngc')
            self.NewFileName.write(self.g_code.get(0.0, END))
            self.NewFileName.close()
        except:
            tkMessageBox.showinfo('Missing INI', 'You must set the\n' \
                'NC File Directory\n' \
                'before saving a file.\n' \
                'Go to Edit/NC Directory\n' \
                'in the menu to set this option')            

    def NcFileDirectory(self):
        DirName = self.GetDirectory()
        if len(DirName)>0:
            self.WriteIniData('face.ini','Directories','NcFiles',DirName)

    def Simple(self):
        tkMessageBox.showinfo('Feature', 'Sorry this Feature has\nnot been programmed yet.')

    def ClearTextBox(self):
        self.g_code.delete(1.0,END)

    def SelectAllText(self):
        self.g_code.tag_add(SEL, '1.0', END)

    def SelectCopy(self):
        self.SelectAllText()
        self.CopyClpBd()

    def ClearOutput(self):
        self.SelectAllText()
        self.ClearTextBox()      

    def HelpInfo(self):
        SimpleDialog(self,
            text='Required fields are:\n'
            'Part Width & Length,\n'
            'Amount to Remove,\n'
            'and Feedrate\n'
            'Fractions can be entered in most fields',
            buttons=['Ok'],
            default=0,
            title='User Info').go()
    def HelpAbout(self):
        tkMessageBox.showinfo('Help About', 'Programmed by\n'
            'Big John T (AKA John Thornton)\n'
            'Rick Calder\n'
            'Brad Hanken\n'
            'Version ' + version)




app = Application()
app.master.title('Facing G-Code Generator Version ' + version)
app.mainloop()

