from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.base import EventLoop
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
import time
import json

#Fechas y numeros de colores
def GetActualTime():
    ActualYear = time.strftime("%y")
    ActualMonth = time.strftime("%m")
    ActualDay = time.strftime("%d")
    if len(str(ActualMonth)) == 1:
        Month = f"0{ActualMonth}"
    else:
        Month = ActualMonth
    if len(str(ActualDay)) == 1:
        Day = f"0{ActualDay}"
    else:
        Day = ActualDay
    return int(f"20{ActualYear}{Month}{Day}")
def ConvertDate(year, month, day):
    if len(str(month)) == 1:
        Month = f"0{month}"
    else:
        Month = month
    if len(str(day)) == 1:
        Day = f"0{day}"
    else:
        Day = day
    return int(f"{year}{Month}{Day}")
def NumberColor(number):
    if number < 0:
        return f"[color=#e00d0d]{number}[/color]"
    elif number > 0:
        return f"[color=#0ee619]{number}[/color]"
    else: 
        return f"[color=#0d88e0]{number}[/color]"
def PrettyDate():
    ActualYear = time.strftime("%y")
    ActualMonth = time.strftime("%m")
    ActualDay = time.strftime("%d")
    return f"{ActualMonth}/{ActualDay}/{ActualYear}"
def PrettyTime():
    ActualHour = time.strftime("%H")
    ActualMinute = time.strftime("%M")
    ActualSecond = time.strftime("%S")
    return f"{ActualHour}:{ActualMinute}:{ActualSecond}"

#Guardado de datos
def SaveData(data, file):
    try:
        with open(file, "r") as file_object:
            JsonData = json.loads(file_object.read())
            file_object.close()
    except:
        JsonData = {}
    with open(file, "w") as f:
        JsonData.update(data)
        f.write(json.dumps(JsonData))
        f.close()
def GetData(dataKey, file):
    with open(file, "r") as file_object:
        JsonData = json.loads(file_object.read())
        file_object.close()
    return JsonData[dataKey]

#Languaje
Setting = "database/Setting.json"
try:
    Lang = GetData("Lang", Setting)
except:
    Lang = "ENG"
    SaveData({"Lang": Lang}, Setting)
LangWords = GetData(Lang, "database/LANGS.json")
del Lang

#Widgets
class MDMyButtton(MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x= 0.8
        self.font_size= 24
        self.pos_hint= {"center_x" : 0.5, "center_y": 0.5}
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding= 10
        self.spacing= 10
class MDMyCard(MDCard, RoundedRectangularElevationBehavior):
    text = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint= {'center_x': 0.5, 'center_y': 0.5}
        self.elevation= 15
        self.padding= 5
        self.spacing= 5
        self.radius= [25]
class MDBasicLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size= 48
        self.halign= 'center'
class MDMyLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y= None
        self.height= self.texture_size[1]
        self.padding_y= 15
class CategoryCard(MDMyCard, ButtonBehavior, TouchBehavior):
    indexNum = StringProperty()
    CategoryName = StringProperty()
    Percentage = StringProperty()
    Amount = StringProperty()
    def __init__(self, **kwargs):
        global LangWords
        self.LangWords = LangWords
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": self.LangWords["ChangePercentage"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=self.indexNum: self.ChangePercentage(x),
            },{
                "text": self.LangWords["Remove"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=self.indexNum: self.Remove(x),
            }
        ]
        self.Menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
        )
        self.orientation = "vertical"
        self.size_hint= (None, 1)
        self.width = 350
        self.add_widget(MDBasicLabel(text=self.CategoryName))
        self.add_widget(MDBasicLabel(text=self.Percentage))
        self.add_widget(MDBasicLabel(text=self.Amount))
    def on_long_touch(self, *args):
        self.Menu.open()
    def ChangePercentage(self, ID):
        App.ChangePercentageCard(ID)
        self.Menu.dismiss()
    def Remove(self, ID):
        App.RemoveCategoryCard(ID)
        self.Menu.dismiss()

#ScreenMAnager
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
    def on_key(self, window, key, *args):
        Screen = self.current_screen.name
        if key == 27:  #Back button android
            if Screen == "login_screen" or Screen == "main_screen":
                return False
            elif Screen == "create_category" or Screen == "registrer_action" or Screen == "registrer_theme":
                App.changeToScreen("main_screen", "right")
                return True

#Screens
class WelcomeScreen(MDScreen):
    pass
class MainScreen(MDScreen):
    pass
class CreateCategory(MDScreen):
    pass
class RegristerAction(MDScreen):
    pass
class RegristerThemes(MDScreen):
    pass
class SettingsScreen(MDScreen):
    pass

Builder.load_file("Money.kv")

class MainApp(MDApp):
    dialog = None
    title = "Money"
    def build(self):
        global LangWords, Setting
        self.LangWords = LangWords
        #ScreemManager
        self.sm = ScreenManagement()
        self.sm.add_widget(WelcomeScreen(name='login_screen'))
        self.sm.add_widget(MainScreen(name='main_screen', on_pre_enter=self.MainScreenEnter))
        self.sm.add_widget(CreateCategory(name="create_category", on_pre_enter=self.CreateCategoryEnter))
        self.sm.add_widget(RegristerAction(name="registrer_action", on_pre_enter=self.RegristerActionEnter))
        self.sm.add_widget(RegristerThemes(name="registrer_theme", on_pre_enter=self.RegristerThemesEnter))
        self.sm.add_widget(SettingsScreen(name="Settings"))

        self.Creator = True

        #Files
        self.Current = "database/Current.json"
        self.Database = "database/Database.json"
        self.Setting = Setting

        #Theme
        try:
            DarkMode = GetData("DarkMode", self.Setting)
        except:
            DarkMode = "Light"
            SaveData({"DarkMode": DarkMode}, self.Setting)
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = DarkMode
        del DarkMode
        
        #Cargar categorias, temas, dinero, y current
        try:
            self.Categorys = GetData("Categorys", self.Database)
        except:
            self.Categorys = []
            SaveData({"Categorys": self.Categorys}, self.Database)
        self.AddCategorysButton = MDIconButton(
            icon="card-plus",
            )
        self.AddCategorysButton.bind(on_release=self.createNewCardCategory)
        try:
            self.Themes = GetData("Themes", self.Database)
        except:
            self.Themes = []
            SaveData({"Themes": self.Themes}, self.Database)
        try:
            self.TotalMoney = GetData("Total", self.Database)
        except:
            self.TotalMoney = 0
            SaveData({"Total": self.TotalMoney}, self.Database)
        try:
            self.ListActionsMoney = GetData("Current", self.Current)
        except:
            self.ListActionsMoney = []
            SaveData({"Current": self.ListActionsMoney}, self.Current)

        #Menu
        menu_items = []
        for i in [(self.LangWords["AddTheme"], True), (self.LangWords["Subtract"], False), (self.LangWords["Preference"], "o")]:
            menu_items.append({
                "text": i[0],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.EditThemesMoneyCallback(x),
            })
        self.ActualTheme = (self.LangWords["AddTheme"], True)
        self.MoneyEditTopics = MDDropdownMenu(
            caller=self.sm.get_screen("registrer_theme").ids.drop_item,
            items=menu_items,
            width_mult=4,
        )

        self.MoneyTopics = MDDropdownMenu(
            caller=self.sm.get_screen("registrer_action").ids.drop_item,
            width_mult=4,
        )
        self.MoneyCategorys = MDDropdownMenu(
            caller=self.sm.get_screen("registrer_action").ids.drop_item_category,
            width_mult=4,
        )

        #Datatable
        rowsNumAmount = 25
        self.EditCostumersTable = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data = [
                ("ID", dp(5)),
                (self.LangWords["Category"], dp(30)),
                (self.LangWords["Amount"], dp(30)),
            ],
            rows_num = rowsNumAmount,
        )
        self.sm.get_screen("main_screen").ids.datatable.add_widget(self.EditCostumersTable)

        rowsNumAmountTitle = 25
        self.EditTitleTable = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data = [
                (self.LangWords["Name"], dp(30)),
                (self.LangWords["Action"], dp(25)),
            ],
            rows_num = rowsNumAmountTitle,
            check=True,
        )
        self.sm.get_screen("registrer_theme").ids.datatable.add_widget(self.EditTitleTable)

        #Buttons
        self.CreatorButton = MDMyButtton(
            text= self.LangWords["CreateCategory"]
        )
        self.CreatorButton.bind(on_release=self.createCardCategory)
        self.EditorButton = MDMyButtton(
            text= self.LangWords["EditCategory"]
        )
        self.EditorButton.bind(on_release=self.ModifyCardCategory)
        return self.sm
    def on_start(self):
        try:
            self.UserName = GetData("User", self.Database)["Name"]
        except:
            self.UserName = ""
        if not self.UserName == "":
            self.changeToScreen("main_screen")
    def NextMain(self):
        Name = self.sm.get_screen("login_screen").ids.name
        if self.ConfirmData([Name], "string"):
            SaveData({"User":{"Name":Name.text}}, self.Database)
            self.UserName = Name.text
            self.changeToScreen("main_screen")
    def changeToScreen(self, screen, direction="left"):
        self.root.current = screen
        self.root.transition.direction = direction
    def showWaring(self, text):
        dialog = MDDialog(
            text=text,
            radius=[20, 7, 20, 7],
        )
        dialog.open()
    def ConfirmData(self, ListData, DataType):
        SendRequest = True
        for i in ListData:
            if i.text == "":
                i.helper_text = "Campo obligatorio"
                i.helper_text_mode = "on_error"
                i.error = True
                SendRequest = False
            else:
                try:
                    if DataType == "int":
                        int(i.text)
                    elif DataType == "float":
                        float(i.text)
                    elif DataType == "string":
                        str(i.text)
                except:
                    i.helper_text = "Campo incorrecto"
                    i.helper_text_mode = "on_error"
                    i.error = True
                    SendRequest = False
        return SendRequest
    def ReloadMainTopis(self):
        menu_items_money = []
        for i in self.Themes:
            menu_items_money.append({
                "text": i[0],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.EditThemesCallback(x),
            })
        menu_items_money.append({
            "text": self.LangWords["Other"],
            "viewclass": "OneLineListItem",
            "on_release": lambda x=(self.LangWords["Other"], "o"): self.EditThemesCallback(x),
        })
        self.ActualThemeMoney = (self.LangWords["Other"], "o")
        self.MoneyTopics.items = menu_items_money

        menu_items_categorys = []
        for i in self.Categorys:
            menu_items_categorys.append({
                "text": i[0],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.EditCategoryCallback(x),
            })
        menu_items_categorys.append({
            "text": self.LangWords["All"],
            "viewclass": "OneLineListItem",
            "on_release": lambda x=False: self.EditCategoryCallback(x),
        })
        self.actualCategory = [False]
        self.MoneyCategorys.items = menu_items_categorys
    #MainScreen
    def MainScreenEnter(self, instance=""):
        #Bienvenido
        self.ReloadCardCategorys()
        Welcome = self.sm.get_screen("main_screen").ids.welcome
        Hour = int(time.strftime("%H"))
        Total = self.sm.get_screen("main_screen").ids.money
        if Hour >= 5 and Hour <= 12:
            Welcome.text = self.LangWords["Morning"] + self.UserName
        elif Hour >= 13 and Hour <= 20:
            Welcome.text = self.LangWords["Afternoon"] + self.UserName
        else:
            Welcome.text = self.LangWords["Night"] + self.UserName
        Total.text = f"Total: {self.TotalMoney}"
    def ReloadCardCategorys(self):
        try:
            for i in self.ListCategoryCards:
                try:
                    self.sm.get_screen("main_screen").ids.scroll.remove_widget(i)
                except:
                    pass
        except:
            pass
        self.ListCategoryCards = []
        num = 0
        if len(self.Categorys) == 0:
            try:
                self.sm.get_screen("main_screen").ids.scroll.add_widget(self.AddCategorysButton)
            except:
                pass
        else:
            try:
                self.sm.get_screen("main_screen").ids.scroll.remove_widget(self.AddCategorysButton)
            except:
                pass
            for i in self.Categorys:
                ActualCard = CategoryCard(CategoryName=i[0], Percentage=str(i[1])+"%", Amount=str(i[2])+"$", indexNum=str(num))
                num = num + 1
                self.ListCategoryCards.append(ActualCard)
                self.sm.get_screen("main_screen").ids.scroll.add_widget(ActualCard)
            try:
                self.sm.get_screen("main_screen").ids.scroll.add_widget(self.AddCategorysButton)
            except:
                pass
    #CategoryCreator
    def CreateCategoryEnter(self, instance=""):
        Percetange = 0
        info = self.sm.get_screen("create_category").ids.info
        info.text = ""
        if self.Creator:
            try:
                self.sm.get_screen("create_category").ids.buttons.add_widget(self.CreatorButton)
            except:
                pass
            try:
                self.sm.get_screen("create_category").ids.buttons.remove_widget(self.EditorButton)
            except:
                pass
            if not len(self.Categorys) == 0:
                self.sm.get_screen("create_category").ids.title.text = self.LangWords["CreateCard"]
                for i in self.Categorys:
                    Percetange += int(i[1])
                Percetange = 100 - Percetange
                if Percetange > 0:
                    self.CreatorButton.disabled = False
                    info.text = self.LangWords["RestPercentage"] + f"{Percetange}%"
                    self.sm.get_screen("create_category").ids.percentage.max = Percetange
                    self.sm.get_screen("create_category").ids.percentage.disabled = False
                else:
                    self.CreatorButton.disabled = True
                    info.text = self.LangWords["NoPercentage"]
                    self.sm.get_screen("create_category").ids.percentage.max = 100
                    self.sm.get_screen("create_category").ids.percentage.disabled = True
        else:
            try:
                self.sm.get_screen("create_category").ids.buttons.remove_widget(self.CreatorButton)
            except:
                pass
            try:
                self.sm.get_screen("create_category").ids.buttons.add_widget(self.EditorButton)
            except:
                pass
            self.EditorButton.disabled = False
            Name = self.Categorys[int(self.IDCARD)][0]
            self.sm.get_screen("create_category").ids.category.text = Name
            self.EditorButton.bind(on_release=self.ModifyCardCategory)
            for i in self.Categorys:
                Percetange += int(i[1])
            Percetange = (100 - Percetange) + int(self.Categorys[int(self.IDCARD)][1])
            self.sm.get_screen("create_category").ids.percentage.max = Percetange
            self.sm.get_screen("create_category").ids.percentage.disabled = False
        self.Creator = True
    def ModifyCardCategory(self, instance=""):
        category = self.sm.get_screen("create_category").ids.category
        percentage = self.sm.get_screen("create_category").ids.percentage
        self.IDCARD
        if self.ConfirmData([category], "string"):
            Money = self.Categorys[int(self.IDCARD)][2]
            self.Categorys[int(self.IDCARD)] = [category.text, percentage.value, Money]
            SaveData({"Categorys": self.Categorys}, self.Database)
            category.text = ""
            percentage.value = 1
            self.changeToScreen("main_screen", "right")
    def createNewCardCategory(self, instance=""):
        self.changeToScreen("create_category")
    def createCardCategory(self, instance=""):
        category = self.sm.get_screen("create_category").ids.category
        percentage = self.sm.get_screen("create_category").ids.percentage
        if self.ConfirmData([category], "string"):
            self.Categorys.append([category.text, percentage.value, 0])
            SaveData({"Categorys": self.Categorys}, self.Database)
            category.text = ""
            percentage.value = 1
            self.changeToScreen("main_screen", "right")
    def ChangePercentageCard(self, ID):
        self.Creator = False
        self.IDCARD = ID
        self.sm.get_screen("create_category").ids.percentage.value = int(self.Categorys[int(self.IDCARD)][1])
        self.changeToScreen("create_category")
    def RemoveCategoryCard(self, ID):
        del self.Categorys[int(ID)]
        SaveData({"Categorys": self.Categorys}, self.Database)
        self.ReloadCardCategorys()
    def Reset(self):
        SaveData({"Lang": "ENG"}, self.Setting)
        SaveData({"DarkMode": "Light"}, self.Setting)
        SaveData({"User":{"Name":""}}, self.Database)
        SaveData({"Categorys": []}, self.Database)
        SaveData({"Themes": []}, self.Database)
        SaveData({"Actions": []}, self.Database)
        SaveData({"Total": 0}, self.Database)
        SaveData({"NextID": 0}, self.Current)
        SaveData({"Current": []}, self.Current)
    #RegistrerActions
    def RegristerActionEnter(self, instance=""):
        self.ReloadMainTopis()
        self.sm.get_screen("registrer_action").ids.drop_item_category.text = self.LangWords["Category"]
        self.sm.get_screen("registrer_action").ids.drop_item.text = self.LangWords["Other"]
        self.sm.get_screen("registrer_action").ids.name.text = ""
        self.sm.get_screen("registrer_action").ids.description.text = ""
        self.sm.get_screen("registrer_action").ids.amount.text = ""
    def EditCategoryCallback(self, x):
        self.actualCategory = x
        if x == False:  #Todas las categorias
            self.sm.get_screen("registrer_action").ids.drop_item_category.text = self.LangWords["All"]
        else:   #Categoria
            self.sm.get_screen("registrer_action").ids.drop_item_category.text = x[0]
        self.MoneyCategorys.dismiss()
    def EditThemesCallback(self, x):
        self.ActualThemeMoney = x
        self.sm.get_screen("registrer_action").ids.drop_item.text = x[0]
        if x[1] == "o":
            self.sm.get_screen("registrer_action").ids.amount.hint_text = self.LangWords["Amount"] + "(0)"
        elif x[1] == True:
            self.sm.get_screen("registrer_action").ids.amount.hint_text = self.LangWords["Amount"] + "(+)"
        else:
            self.sm.get_screen("registrer_action").ids.amount.hint_text = self.LangWords["Amount"] + "(-)"
        self.MoneyTopics.dismiss()
    def MakeAction(self):
        Name = self.sm.get_screen("registrer_action").ids.name
        Descripcion = self.sm.get_screen("registrer_action").ids.description
        Amount = self.sm.get_screen("registrer_action").ids.amount
        if self.ConfirmData([Name, Descripcion], "string") and self.ConfirmData([Amount], "float"):
            #NextID
            try:
                NextID = GetData("NextID", self.Current)
            except:
                NextID = 0
                SaveData({"NextID": NextID}, self.Current)

            #SafeAction
            Action = {
                "ID": NextID,
                "Name": Name.text,
                "Category": self.actualCategory,
                "Descripcion": Descripcion.text,
                "Amount": Amount.text,
                "Title": self.ActualThemeMoney,
                "Date": GetActualTime(),
                "PrettyDate": PrettyDate(),
                "PrettyTime": PrettyTime(),
            }
            print(Action)
            self.ListActionsMoney.append(Action)
            SaveData({"Current": self.ListActionsMoney}, self.Current)

            #Agregarlo al total
            if not Action["Title"][1]:
                self.TotalMoney = self.TotalMoney - float(Action["Amount"])
            else:
                self.TotalMoney = self.TotalMoney + float(Action["Amount"])
            SaveData({"Total": self.TotalMoney}, self.Database)

            #Ponerlo en las categorias
            if Action["Category"] == False:
                IndexNum = 0
                for i in self.Categorys:
                    Percentage = int(i[1])
                    if not Action["Title"][1]:
                        self.Categorys[IndexNum][2] = self.Categorys[IndexNum][2] - (Percentage*float(Amount.text))/100
                    else:
                        self.Categorys[IndexNum][2] = self.Categorys[IndexNum][2] + (Percentage*float(Amount.text))/100
                    IndexNum = IndexNum+1
            else:
                Index = self.Categorys.index(Action["Category"])
                if not Action["Title"][1]:
                    self.Categorys[Index][2] = self.Categorys[Index][2] - float(Amount.text)
                else:
                    self.Categorys[Index][2] = self.Categorys[Index][2] + float(Amount.text)
            SaveData({"Categorys": self.Categorys}, self.Database)

            #Safe NextID
            NextID = NextID + 1
            SaveData({"NextID": NextID}, self.Current)
            self.changeToScreen("main_screen", "right")
    def UnmakeLastAction(self):
        pass
    #RegistrerThemes
    def RegristerThemesEnter(self, instance=""):
        self.ReloadMainTopis()
        self.UploadThemes()
    def AddTheme(self):
        SendRequest = True
        Name = self.sm.get_screen("registrer_theme").ids.name
        for i in self.Themes:
            if Name.text == i[0]:
                SendRequest = False
                self.showWaring(self.LangWords["WordAlredyExist"])
        if self.ConfirmData([Name], "string") and SendRequest:
            self.Themes.append((Name.text, self.ActualTheme[1]))
            SaveData({"Themes": self.Themes}, self.Database)
            self.UploadThemes()
    def RemoveTheme(self):
        print(self.EditTitleTable.get_row_checks())
        for a in self.Themes:
            for b in self.EditTitleTable.get_row_checks():
                if a[0] == b[0]:
                    del self.Themes[self.Themes.index(a)]
        SaveData({"Themes": self.Themes}, self.Database)
        self.UploadThemes()
    def EditThemesMoneyCallback(self, x):
        self.ActualTheme = x
        self.sm.get_screen("registrer_theme").ids.drop_item.text = x[0]
        self.MoneyEditTopics.dismiss()
    def UploadThemes(self):
        RowData = []
        for i in self.Themes:
            if i[1] == "o":
                temp = ("cash", [0.5, 0.5, 0.5, 1], self.LangWords["Preference"])
            elif i[1]:
                temp = ("cash-plus", [0, 1, 0, 1], self.LangWords["AddTheme"])
            else:
                temp = ("cash-minus", [1, 0, 0, 1], self.LangWords["Subtract"])
            RowData.append((i[0], temp))
        if len(RowData) == 1:
            RowData.append(("", ""))
        self.EditTitleTable.row_data = RowData
App = MainApp()
App.run()