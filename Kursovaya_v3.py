# -*- coding: utf-8 -*-
"""
Created on Sun May  7 16:39:56 2023

@author: user
"""

import os

import time

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo


import random
#from random import random, randrange, randint

# Для потока
import threading

# Флаг для работы потока
isWorking = False

# Для потока
import threading
import time

import tkinter as tk
from contextlib import redirect_stdout



#====================================================================
# Вспомогательный класс для вывода текста в окно
class TextWrapper:
    text_field: tk.Text

    def __init__(self, text_field: tk.Text):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(tk.END, text)

    def flush(self):
        self.text_field.update()
#====================================================================



#====================================================================
# Класс параметры, для хранени параметров
class Parametrs:
    # Конструктор
    def __init__(self, depthRemove, countOfTakts
                 , countOFPages, lenBuffer
                 , timeSleep, countDeletes
                 , flagDelete, countAdd):
        
        # Количество тактов между удалением
        # Глубина удаления
        self.DepthRemove = depthRemove
        
        # Количество тактов в моделе, которое будет пройдено
        self.CountOfTakts = countOfTakts
        
        # Количество страниц в моделе
        self.CountOFPages = countOFPages
        
        # Длина буфера для одной страницы ("глубина старения")
        self.LenBuffer = lenBuffer 
        
        # Время задержки
        self.TimeSleep = timeSleep
        
        # Количество удалений за один раз
        self.CountDeletes = countDeletes
        
        # Добавление новой страницы при удалении старой
        self.FlagDelete = flagDelete
        
        # Количество добавлений новых страниц
        self.CountAdd = countAdd
#====================================================================


#====================================================================
# Класс страница памяти
# Содержит в себе внутренний возрст страницы для работы программы
# и возраст в виде списка для отображения на экране
class Page:

    # Конструктор
    def __init__(self, id, LenBuffer):
        self.id = id                    # Id страницы
        #self.age = 0                   # возраст
        self.listAge = []               # Возраст в виде списка 0 и 1
        #self.listAge.append(0)          # Добавляем начальное значение
        self.lenBuffer = LenBuffer      # Максимальная длина буфера (спсика возраста)

    # К странице не обратились на такте
    def skip_page(self):
        #self.age = 0
        #self.listAge.append(0)
        self.listAge.append(0)
        # Удаляем первый элемент, если буффер достиг предела
        if(len(self.listAge) >= self.lenBuffer):
            self.listAge.pop(0)

    # К странице обратились на такте
    def age_page(self):
        
        # Увеличиваем возраст
        #self.age += 1
        
        # Увеличиваем отображаемый возраст
        self.listAge.append(1)
        
        # Удаляем первый элемент, если буффер достиг предела
        if(len(self.listAge) >= self.lenBuffer):
            self.listAge.pop(0)

    
    # Вернуть список обращений в виде float
    def get_age_in_float(self):
        tempString = ""
        for i in range(0, len(self.listAge)):
            tempString += str(self.listAge[i])
        if(len(tempString) == 0):
            tempString = "0"
        return float(tempString)
    
    # Вернуть список обращений в виде string
    def get_age_in_string(self):
        tempString = ""
        for i in range(0, len(self.listAge)):
            tempString += str(self.listAge[i])
        return tempString
    
#====================================================================



#====================================================================
# Класс память
class Memory:
    
    # Конструктор памяти
    def __init__(self, MyParametrs):
        # Список страниц в памяти
        self.pages = []
        
        # Все внешние вводимые параметры
        self.params = MyParametrs
        
        # Максимальный размер текущей памяти
        #self.size = size
        
        # Текущий id для создания страниц
        self.currentId = 0
        
        # Длина буффера у страницы
        #self.LenBuffer = lenBuffer
        
        # Количество тактов между удалением
        #self.count_of_takts_for_delete = CountDel
        
        # Создаем нужное количество страниц
        self.add_page(self.params.CountOFPages)
        
    
    # Добавить новую страницу
    def add_page(self, count):
        for i in range(0, count):
            page = Page(self.currentId, self.params.LenBuffer)
            #page.skip_page()
            self.currentId += 1
            
            if len(self.pages) < self.params.CountOFPages:
                self.pages.append(page)
                print("", file=TextWrapper(text))
                print(f"СТРАНИЦА ДОБАВЛЕНА: Page ID: {page.id}, Age: {page.listAge}", file=TextWrapper(text))
                print("", file=TextWrapper(text))
            else:
                #oldest_page = sorted(self.pages, key=lambda page: page.age, reverse=True)[0]
                oldest_page = self.find_old()
                self.pages.remove(oldest_page)
                self.pages.append(page)
                print("", file=TextWrapper(text))
                print(f"СТРАНИЦА ДОБАВЛЕНА: Page ID: {page.id}, Age: {page.listAge}", file=TextWrapper(text))
                print("", file=TextWrapper(text))
    
    # Напечатать все страницы в консоль
    def print_pages(self):
        for page in self.pages:
            string = page.get_age_in_string()
            print(f"Page ID: {page.id}, Age: {page.listAge}", file=TextWrapper(text))
            #print(f"Page ID: {page.id}, Age: {string}", file=TextWrapper(text))

    # Применение маски старения к страницам
    def age_pages(self, ListIndex):
        #for page in self.pages:
        for i in range(0, len(ListIndex)):
            if (ListIndex[i] == 1):
                self.pages[i].age_page()
            else:
                self.pages[i].skip_page()

    # Ищет самую старую страницу и возвращает её
    def find_old(self):
        if (len(self.pages) > 0):
            
            floatList =[]
            #idList = []
            for i in range(0, len(self.pages)):
                floatList.append(self.pages[i].get_age_in_float())
                #idList.append(self.pages[i].id)
            
            minimum = floatList[0]
            #minId = 0
            minPage = self.pages[0]
            for i in range(0, len(floatList)):
                if (floatList[i] < minimum):
                    minimum = floatList[i]
                    minPage = self.pages[i]
                    #minId = idList[i]
            
            return minPage
        else:
            return None

    # Эмуляция алгоритма "старения"
    def Emulation(self):
        
        global thread_stop
        
        # Текущий такт, используется для удаления
        currentTakt = 0
    
        # Очистка поля вывода перед новой эмуляцией
        text.delete(1.0, END)    
    
        # Основной цикл по количеству тактов
        #for i in range(0, self.params.CountOfTakts):
        i = 0
        while(len(self.pages) > 0 and i < self.params.CountOfTakts):
            
            if (thread_stop == True):
                showerror("Error", "The process is stopped! ") 
                break
            
            # Если страниц больше нет, то завершаем цикл
            if(len(self.pages) == 0):
                break
            
            # Получить новую маску
            NewMask = CreateMaskForTakt(len(self.pages))
            
            # Применить текущую маску для столбца
            self.age_pages(NewMask)
            
            # Вывести в консоль страницы
            print("Такт: ", i, "   Маска: ", NewMask, file=TextWrapper(text))
            
            # Вывести все страницы
            self.print_pages()
            print("",file=TextWrapper(text))
            
            # Перелис вниз в поле вывода
            text.see(tk.END)
            
            # Задержка времени
            #time.sleep(1)
            time.sleep(self.params.TimeSleep)
            
            # Проверка номера такта и удаление
            currentTakt += 1
            #if(currentTakt == self.count_of_takts_for_delete):
            if(currentTakt == self.params.DepthRemove):
                self.remove_pages(self.params.CountDeletes)
                currentTakt = 0
                if (self.params.FlagDelete == True):
                    self.add_page(self.params.CountAdd)
                    #print(i)
            
            i+=1
        # Перелис вниз в поле вывода
        text.see(tk.END)
            

    # удалить страницы
    def remove_pages(self, count):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #if (len(self.pages) <= count):
        #    self.pages.clear()
        #    print("ВСЕ СТРАНИЦЫ БЫЛИ УДАЛЕНЫ!", file=TextWrapper(text))
        for i in range(0, count):
            oldest_page = self.find_old()
            #print(f"Page ID: {page.id}, Age: {page.listAge}", file=TextWrapper(text))
            if(oldest_page != None):
                print("", file=TextWrapper(text))
                print(f"СТРАНИЦА УДАЛЕНА: Page ID: {oldest_page.id}, Age: {oldest_page.listAge}", file=TextWrapper(text))
                print("", file=TextWrapper(text))
                self.pages.remove(oldest_page)
        """
        while True:
            time.sleep(interval)
            oldest_page = sorted(self.pages, key=lambda page: page.age, reverse=True)[0]
            self.pages.remove(oldest_page)
            print(f"Page ID {oldest_page.id} removed due to age.")
        """
        
#====================================================================

thread_stop = False

def StopProcess():
    global thread_stop
    thread_stop = True


#==================================================================
# Запуск потока с функцией main
def mainInThread():
    global isWorking
    global thread_stop
    thread_stop = False
    
    if (isWorking == False):
        
        x = threading.Thread(target=main, args=())
        x.start()
    else:
        showerror("Error", "The process is working! ")    
#==================================================================



#==================================================================
# Функция main
def main():
    global isWorking

    # Флаг во время работы, чтобы не создавать новые потоки
    isWorking = True
    
    # Конфигурируем класс с параметрами
    params = Parametrs(int(entryDepthRemove.get())
                       , int(entryCountOfTakts.get())
                       , int(entryCountOFPages.get())
                       , int(entryLenBuffer.get())
                       , float(entryTimeSleep.get())
                       , int(entryCountDeletes.get())
                       , color.get()
                       , int(entryCountAdd.get()))
    
    # Создаем память с введенными параметрами
    memory = Memory(params) 

    # Эмулируем алгоритм "старение"     
    memory.Emulation()
    
    # Выводим уведомление о завершении работы алгоритма
    showinfo("Work", "Work is end!")
    isWorking = False

#==================================================================



#==================================================================
# Функция создания маски для одного такта
# Передается длянна создаваемого списака
# Список содеожит случайные 0 и 1
def CreateMaskForTakt(lengthOfMask):
    
    maska = []
    
    for i in range(lengthOfMask):
        maska.append(random.randint(0, 1))
    
    return maska
#==================================================================




#==================================================================
window = Tk()
window.title("Model of memory - 'Aging'")
window.geometry("650x680") 
 


#==============================================================================
text = tk.Text(window)
text.grid(row=1, column=0)
#==============================================================================

#print("Hello!!!!", file=TextWrapper(text))
#, padding=[8, 10]
frame = ttk.Frame(borderwidth=5, relief=SOLID)
frame.grid(row=2, column=0, sticky=W+E, padx=0, pady=10)

#==============================================================================
LabelNameCol = ttk.Label(text="Результат работы метода:", font=("Arial", 12), background="White")
#labelNameCol.pack(padx=70)
LabelNameCol.grid(row=0, column=0)
#==============================================================================




#==============================================================================
LabelCountOfTakts = ttk.Label(text="Количество тактов:", font=("Arial", 12))
LabelCountOfTakts.grid(row=3, column=0, sticky=W, padx=10, pady=10)

entryCountOfTakts = ttk.Entry()
entryCountOfTakts.grid(row=4, column=0, columnspan=3, sticky=W, padx=10)
entryCountOfTakts.insert(0, "22")
#==============================================================================



#==============================================================================
LabelDepthRemove = ttk.Label(text="Количество тактов между удалением:", font=("Arial", 12))
LabelDepthRemove.grid(row=3, column=0, sticky=S, padx=10, pady=10)

entryDepthRemove = ttk.Entry()
entryDepthRemove.grid(row=4, column=0, columnspan=3, sticky=S, padx=10)
entryDepthRemove.insert(0, "3")
#==============================================================================



#==============================================================================
LabelCountOFPages = ttk.Label(text="Максимум страниц:", font=("Arial", 12))
LabelCountOFPages.grid(row=3, column=0, sticky=E, padx=10, pady=10)

entryCountOFPages = ttk.Entry()
entryCountOFPages.grid(row=4, column=0, columnspan=3, sticky=E, padx=10)
entryCountOFPages.insert(0, "6")
#==============================================================================



#==============================================================================
LabelLenBuffer = ttk.Label(text="Длина счетчика страницы:", font=("Arial", 12))
LabelLenBuffer.grid(row=5, column=0, sticky=W, padx=10, pady=10)

entryLenBuffer = ttk.Entry()
entryLenBuffer.grid(row=6, column=0, columnspan=3, sticky=W, padx=10)
entryLenBuffer.insert(0, "8")
#==============================================================================



#==============================================================================
LabelTimeSleep = ttk.Label(text="Задержка в секундах:", font=("Arial", 12))
LabelTimeSleep.grid(row=5, column=0, sticky=E, padx=10, pady=10)

entryTimeSleep = ttk.Entry()
entryTimeSleep.grid(row=6, column=0, columnspan=3, sticky=E, padx=10)
entryTimeSleep.insert(0, "1")
#==============================================================================



#==============================================================================
LabelCountDeletes = ttk.Label(text="Количество удалений за раз:", font=("Arial", 12))
LabelCountDeletes.grid(row=5, column=0, sticky=S, padx=10, pady=10)

entryCountDeletes = ttk.Entry()
entryCountDeletes.grid(row=6, column=0, columnspan=3, sticky=S, padx=10)
entryCountDeletes.insert(0, "1")
#==============================================================================


#==============================================================================
color = BooleanVar()
color.set(0)


rbColor = Radiobutton(text = "Добавлять новую страницу:", variable=color, value=1)
rbColor.grid(column=0, row=7, sticky=W, padx=10, pady=10)

rbGray = Radiobutton(text = "Не добавлять новую страницу", variable=color, value=0)
rbGray.grid(column=0, row=8, sticky=W, padx=10, pady=0)
#==============================================================================


#==============================================================================

#if(color.get() == True):

LabelCountAdd = ttk.Label(text="Количество добавлений за раз:", font=("Arial", 12))
LabelCountAdd.grid(row=7, column=0, sticky=S, padx=10, pady=10)


entryCountAdd = ttk.Entry()
entryCountAdd.grid(row=8, column=0, columnspan=3, sticky=S, padx=10)
entryCountAdd.insert(0, "1")
#==============================================================================


#==============================================================================
btnRecogn = Button(window, text="Старт", background="Aqua", command=mainInThread, font=("Arial Bold", 14))
btnRecogn.grid(column=0, row=15, sticky=S, padx=10, pady=10)
#==============================================================================
 

#==============================================================================
btnPause = Button(window, text="Остановка", background="Red", command=StopProcess, font=("Arial Bold", 14))
btnPause.grid(column=0, row=15, sticky=E, padx=10, pady=10)
#==============================================================================

 
window.mainloop()
#==================================================================








