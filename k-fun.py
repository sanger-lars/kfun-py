import wx, sys
import __data as data


# hent config.txt
cfg = data.read_config()
if cfg == 'null':
    print('ingen config.txt fil !!!')
    sys.exit()

# hent data.json
arr = data.read_data_json('data.json')
if arr == 'null':
    print('ingen data !!!')
    #sys.exit()


STI = cfg['sti']
try:
    if cfg['font_size']:
        pointStor = cfg['font_size']
except:
    pointStor = 10


class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)

        self.basicGUI()
    

    def basicGUI(self):
        # Menu
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        gemItem = fileButton.Append(wx.ID_FILE, 'gem data', '\tLav data.json ')
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit\tCtrl+Q', '\tExit program')
        menuBar.Append(fileButton, 'File')
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.gem_data, gemItem)
        self.Bind(wx.EVT_MENU, self.quit, exitItem)
        self.Centre()
        self.Show(True)
        self.SetFont(font)
        
        # Status-bar
        global besked
        besked = self.CreateStatusBar(style=0)
        #besked.SetStatusStyles([wx.ALIGN_CENTER_VERTICAL])
        besked.SetForegroundColour(wx.RED)
        besked.SetStatusText("\tStatus-bar ")
        
        # Søgefeldt
        self.editname = wx.TextCtrl(self, value="Kim Larsen", pos=(50, 60), size=(200,-1) )
        self.editname.Bind(wx.EVT_KEY_DOWN, self.key_check)
        
        # Søge-knap
        self.button =wx.Button(self, label="Søg", pos=(260, 60))
        self.Bind(wx.EVT_BUTTON, self.find_sang,self.button)

        # sang-liste
        self.list = wx.ListCtrl(self, size = (500,500), pos=(10, 100), style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Sange", width=500)

        # Check om data er hentet
        if arr == 'null' or arr['sange'] == []: self.list.Append(["Der er ikke hentet nogen data.json fil !!!"])
        else: self.list.Append(["Der er hentet "+str(len(arr['sange']))+" sange ialt."])


    def key_check(self, event):
        """Hvis Enter eller Return kør find_sang."""
        if event.GetKeyCode() in [370, 13]:
            self.find_sang(event)
        else:
            event.Skip()
            return
    

    def find_sang(self, event):
        tekst = self.editname.GetValue()
        global dataobj
        self.list.DeleteAllItems()
        if arr == 'null' or arr['sange'] == []: self.list.Append(["Der er ikke hentet nogen data.json fil !!!"])
        else:
            dataobj = data.find_sang(arr, tekst)
            self.vis_besked("Der er fundet "+str(len(dataobj['liste']))+ " sange.")
            self.list.Append(["     Der er fundet "+str(len(dataobj['liste']))+ " sange."])
            for item in dataobj['liste']:
                self.list.Append([item])

            self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDragInit)


    def onDragInit(self, event):
        fdo = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex() -1
        filename = STI+dataobj['links'][id]+"/"+dataobj['liste'][id]
        filename = filename.replace("/", "\\")
        fdo.AddFile(filename)
        print(filename)
        
        dropSource = wx.DropSource(obj)
        dropSource.SetData(fdo)
        result = dropSource.DoDragDrop()


    def quit(self, e):
        sys.exit()


    def vis_besked(self, tekst, color=wx.WHITE):
        besked.SetBackgroundColour(color)
        besked.SetStatusText("\t"+tekst)
        besked.SetBackgroundColour(wx.WHITE)


    def gem_data(self, e):
        self.vis_besked("Vent venligst mens data genereres. ", wx.YELLOW )
        data.gem(STI)
        global arr
        arr = data.read_data_json()
        self.list.DeleteAllItems()
        self.vis_besked("data.json er nu genereret og hentet.", wx.GREEN)
        self.list.Append(["data.json er nu genereret og hentet."])
        self.list.Append([str(len(arr['sange']))+" sange ialt."])


if __name__ == "__main__":
    app = wx.App()
    global font
    font=wx.Font(pointSize=pointStor, family=wx.FONTFAMILY_DEFAULT, 
        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, underline=False,
        faceName="", encoding=wx.FONTENCODING_DEFAULT)
    windowClass(None, title='Fun-Liste Python', size=(600,750))
    app.MainLoop()



