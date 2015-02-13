from pymel.core import *
import os
import maya.cmds as cmds
import functools

def createUI ( pWindowTitle, pApplyCallback):
    windowID = "cbox"

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    if cmds.windowPref(windowID, exists=True):
        cmds.windowPref(windowID, remove=True)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)

    cmds.columnLayout(columnAttach=('both', 5), columnWidth=400)
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,75), (2,300) ], columnOffset=[ (1,'right',3) ] )

    cmds.text(label='Description:') #1,1
    descField = cmds.textField(text='', width=300) #1,2

    cmds.setParent('..')
    
    #blank separator to make empty row before buttons

    cmds.separator(h=5, style='none')

    cmds.setParent('..')
    
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,200), (2,200)])

    cmds.button(label='Apply', width=100, command=functools.partial(pApplyCallback, descField))

    def cancelCallBack (*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label='Cancel', width=100, command=cancelCallBack)

    cmds.showWindow()

def applyCallback(pDescField, *pArgs):
    print 'Apply button pressed.'

    desc = cmds.textField(pDescField, query=True, text=True)
    if (len(desc) > 0):
        desc = "_"+desc
    print 'desc entered = %s' % (desc)


    path = sceneName()
    fileName = path.split('/')[-1].partition(".")[0]
    newFileName = fileName+"_0001"+".ma"
    incSaveFolder = "incrementalSave"
    fileFolder = os.path.abspath(os.path.join(path, os.pardir))
    incSaveFolderPath = os.path.join(fileFolder,incSaveFolder)
    projectSaveFolder = os.path.join(incSaveFolderPath, fileName)
    incSaveFilePath = os.path.join(projectSaveFolder, newFileName)
     
    if os.path.exists(incSaveFilePath):
        savedFiles = os.listdir(projectSaveFolder)
        savedFiles.sort()
        incFiles = []
        for i in savedFiles:
            if fileName in i:
                incFiles.append(i)
        lastFile = incFiles[len(incFiles)-1]
        name = lastFile.partition(".")[0]
        nameParts=name.split("_")
        newName=nameParts[0]+"_"+(str(int(nameParts[1])+1).zfill(4))+desc+".ma"
        incSaveFilePath = os.path.join(projectSaveFolder, newName)
        system.saveAs(incSaveFilePath)
        system.saveAs(path)
    else:
        os.makedirs(projectSaveFolder)
        system.saveAs(incSaveFilePath)
        system.saveAs(path)

    print 'File saved as: %s' % (newName)

createUI('Incremental Save - Add a description', applyCallback)
