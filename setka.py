import ctypes

import maptype
import mapapi
import mapgdi
import mapsyst
import maperr
import seekapi
import rscapi
import sitapi
import maprscex

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def CreateGrid(hmap:maptype.HMAP,hobj: maptype.HOBJ) -> str:   #mmstep:ctypes.c_int
    result = 0
    retvalues = 0
    frame = maptype.DFRAME(0,0,0,0)
    subj = 0

    if hmap == 0:
        return 0
    
    hobj = mapapi.mapCreateObject(hmap)
    if hmap == 0:
       return 1
   
    # Запросить описание цвета палитры по индексу (index)
    MapCol = mapapi.mapGetMapColor(hmap, 202)
   
    # получить идентификатор (HRSC) для объекта карты
    hres_class = mapapi.mapGetRscIdentByObject(hobj)

    # Определить идентификатор открытой пользовательской карты
    hsite = sitapi.mapGetObjectSiteIdent(hmap, hobj)
    
    # Запросить идентификатор классификатора карты
    hrsc = rscapi.mapGetRscIdent(hmap, hsite)
    if hrsc ==0 :
       return 2 
    
    # Создать контекст (описание условий) поиска/отображения объектов карты
    hSelect = sitapi.mapCreateSiteSelectContext(hmap, hsite)
    if hSelect == 0 :
       return 3
   
    # Подсчитать сколько объектов удовлетворяет условиям обобщенного поиска
    seekcount = seekapi.mapTotalSeekObjectCount(hmap)
   
    # Инициализация списка выбранных объектов
    selected_objects = []
   
    flag = maptype.WO_FIRST
    while (seekapi.mapTotalSeekObject(hmap, hobj, flag) != 0):
        flag = maptype.WO_NEXT
        
    # Запросить уникальный номер объекта
    objKey = mapapi.mapObjectKey(hobj)
    if objKey == 0:
       return 4
   
    # Запросить порядковый номер объекта в карте
    ObjNumber = mapapi.mapObjectNumber(hobj)
    if ObjNumber == 0:
       return 9
   
    # Запросить (найти) последовательный номер объекта
    GetSiteObjNumbByKey = sitapi.mapGetSiteObjectNumberByKey(hmap, hsite, objKey)
    
    # Запросить уникальный идентификатор объекта по последовательному номеру объекта
    GetSiteObjeKeyByNumb = sitapi.mapGetSiteObjectKeyByNumber(hmap, hsite, GetSiteObjNumbByKey, 1)
    
    # Запросить индекс (внутренний код) объекта в классификаторе.
    ObjCode = mapapi.mapObjectCode(hobj)
   
    # Запросить номер слоя объекта ("Layer" = "Segment")
    LayerNumber = mapapi.mapSegmentNumber(hobj)
    if LayerNumber == 0:
       return 10
   
    # Запросить название слоя объекта ("Layer" = "Segment")
    SegmentName = mapsyst.WTEXT(1024)
    SegName = mapapi.mapSegmentNameUn(hobj, SegmentName, SegmentName.size())
    SegmentNametext = SegmentName.string()
   
    # Запросить характер локализации объекта
    ObjectLocal = mapapi.mapObjectLocal(hobj)
   
    # Запросить замкнутость объекта/подобъекта
    getExclSub = mapapi.mapGetExclusiveSubject(hobj, 0)
    if getExclSub == 0:
       return 5
   
    # Запросить габариты объекта в метрах (по метрике). Габариты вычисляются по координатам объекта при каждом запросе
    #ObjFrame = mapapi.mapObjectFrame(hobj,frame)
    mapapi.mapObjectFrame(hobj,ctypes.byref(frame))
    #if ObjFrame == 0:
     #  return 6

    # Запросить базовый масштаб карты
    getMapScale = mapapi.mapGetMapScale(hmap)
    if getMapScale == 0:
       return 6

    # Запросить классификационный код объекта
    ObjExc = mapapi.mapObjectExcode(hobj)
    
    # Запросить имя объекта по внутреннему  коду (порядковому номеру) объекта (с 1) в кодировке UNICODE
    RscObjName = mapsyst.WTEXT(1024)
    GetRscObjName = rscapi.mapGetRscObjectNameUnicode(hrsc, ObjCode, RscObjName, RscObjName.size())
    if GetRscObjName == 0:
       return 9
    GetRscObjNametext = RscObjName.string()
    
    # Запросить ключ объекта по внутреннему  коду (порядковому номеру) объекта (с 1) в кодировке UNICODE
    RscObjKey = mapsyst.WTEXT(1024)
    GetRscObjKey = rscapi.mapGetRscObjectKeyUn(hrsc, ObjCode, RscObjKey, RscObjKey.size())
    #if GetRscObjKey == 0:
    #   return 10
    GetRscObjKeytext = RscObjKey.string()
    #ObjCode_str = str(ObjCode)  # Преобразование числа в строку
    # Преобразуем строку в байты
    GetRscObjKeytext_bytes = GetRscObjKeytext.encode('ascii')
    
    # Запросить название объекта по порядковому номеру в заданном слое
    RscObjNameInLay = mapsyst.WTEXT(1024)
    RscObjNameInLayer = rscapi.mapGetRscObjectNameInLayerUn(hrsc, LayerNumber, ObjNumber, RscObjNameInLay, RscObjNameInLay.size())
    RscObjNameInLaytext = RscObjNameInLay.string()
    
    # Запросить код локализации объекта по внутреннему  коду (порядковому номеру) объекта (с 1)
    RscObjLocal = rscapi.mapGetRscObjectLocal(hrsc, ObjNumber)
    
    # Запросить номер слоя объекта по внутреннему коду (порядковому номеру) объекта (с 1)
    RscObjSegment = rscapi.mapGetRscObjectSegment(hrsc, ObjNumber)
    
    # Запросить условное название объекта
    objname = mapsyst.WTEXT(1024)
    Object_name = mapapi.mapObjectNameUn(hobj, objname, objname.size())
    if Object_name == 0:
        return 11
    objnametext = objname.string()
    
    # Запросить общее число объектов в листе
    ObjCount = mapapi.mapGetObjectCount(hmap, 1)

    # Запросить буквенно-цифровой код объекта по внутреннему коду (порядковому номеру) объекта (с 1) в кодировке UNICODE
    RscObjectCode = mapsyst.WTEXT(1024)
    RscObjectWCode = rscapi.mapGetRscObjectWCodeUn(hrsc, objKey, RscObjectCode, RscObjectCode.size())
    RscObjectWCodetext = RscObjectCode.string()
    
    # Запросить внешний код объекта по его буквенно-цифровому коду
    RscObjectCodeUn = mapsyst.WTEXT(1024)
    RscObjectWCodeUn = rscapi.mapGetRscObjectExcodeByWCode(hrsc, RscObjectCode)
    RscObjectWCodeUntext = RscObjectCodeUn.string()
    
    # Запросить идентификатор объекта (постоянное уникальное значение в пределах данного классификатора) по внутреннему  коду
    RscObjIdent = rscapi.mapGetRscObjectIdent(hrsc, ObjNumber)
    
    # Найти "основной" цвет изображения объекта
    RscObjBaseCol = rscapi.mapGetRscObjectBaseColor(hrsc, GetSiteObjNumbByKey, 0)
    
    # Установить/Запросить цвет фона отображаемой карты
    GetBackColor = mapapi.mapGetBackColor(hmap)
    
    # Вычисление габаритов объекта   
    #mapapi.mapGetTotalBorder(hmap,ctypes.byref(frame),maptype.PP_PLANE); # нужно узнать габариты объекта
    x1 = frame.X1
    y1 = frame.Y1
    x2 = frame.X2
    y2 = frame.Y2

    imglObj = mapgdi.IMGLINE(0,0)  
    imglObj.Thick = 100
    imglObj.Color = 0 
    
    #subj = subj + 1
    
    mapapi.mapRegisterDrawObject(hobj,LayerNumber,0)
    mapapi.mapAppendDraw(hobj,mapgdi.IMG_LINE,ctypes.cast(ctypes.byref(imglObj), ctypes.c_char_p))
    mapapi.mapAppendPointPlane(hobj,x1,y1,0)
    mapapi.mapAppendPointPlane(hobj,x2,y1,0)		   
    mapapi.mapAppendPointPlane(hobj,x2,y2,0)		   				   
    mapapi.mapAppendPointPlane(hobj,x1,y2,0)
    mapapi.mapAppendPointPlane(hobj,x1,y1,0)	
    
    # Нанесение подобъектов
    imglSobj = mapgdi.IMGSQUARE(0)  
    imglSobj.Color = MapCol  # нужно применить 47 

    x0 = x1
    step = 125 * mapapi.mapGetMapScale(hmap) / 1000.0
    steps = int(x0 / step)
    x0 = steps * step
    y0 = y1
    steps = int(y0 / step)
    y0 = steps * step
    yr = y2
    xt = x2
    x = x0
    y = y0
    
    # Счетчик создаваемых объектов
    copy_count = 0
    
    #Создание 16 отдельных объектов
    for i in range(4):
        for j in range(4):
            hwork = mapapi.mapCreateObject(hmap)
       
            flag = maptype.WO_FIRST
            while (seekapi.mapTotalSeekObject(hmap, hwork, flag) != 0):
                
                copy_count += 1
            
                # Запросить уникальный номер объекта
                objKeyHwork = mapapi.mapObjectKey(hwork)
            
                # Запросить (найти) последовательный номер объекта
                GetSiteObjNumbByKeyHwork = sitapi.mapGetSiteObjectNumberByKey(hmap, hsite, objKey)
            
                # Скопировать объект
                CopyRscObjHwork = rscapi.mapCopyRscObject(hrsc, ObjNumber)
            
                # Запросить порядковый номер объекта в карте
                ObjNumberHwork = mapapi.mapGetObjectNumber(hwork)
            
                # Запросить индекс (внутренний код) объекта в классификаторе.
                ObjCodeHwork = mapapi.mapObjectCode(hwork)
            
                # Запросить внешний код объекта по порядковому номеру (с 1)
                RscObjectExcodeHwork = rscapi.mapGetRscObjectExcode(hrsc, ObjNumberHwork)
            
                # Переопределить внешний код объекта
                UpdateRscObjeExcHwork = maprscex.mapUpdateRscObjectExcode(hrsc, RscObjectExcodeHwork, RscObjectExcodeHwork)

                mapapi.mapAppendPointPlane(hwork, x2 - i * step, y1 + j * step, 0)
                mapapi.mapAppendPointPlane(hwork, x2 - i * step - step, y1 + j * step, 0)
                mapapi.mapAppendPointPlane(hwork, x2 - i * step - step, y1 + j * step + step, 0)
                mapapi.mapAppendPointPlane(hwork, x2 - i * step, y1 + j * step + step, 0)
                mapapi.mapAppendPointPlane(hwork, x2 - i * step, y1 + j * step, 0)

                mapapi.mapAppendDraw(hwork, 135, ctypes.cast(ctypes.byref(imglSobj), ctypes.c_char_p))
                mapapi.mapAppendDraw(hwork,mapgdi.IMG_LINE,ctypes.cast(ctypes.byref(imglObj), ctypes.c_char_p))
                #mapapi.mapDescribeObject(hwork, ObjCodeHwork)

                # Удалить из объекта/подобъекта участок с точки number1 по точку number2
                DelPartObj = mapapi.mapDeletePartObject(hwork, 1, 5, 0)
                
                # Удалить заданную точку метрики
                DelPointObj = mapapi.mapDeletePointPlane(hwork, 11, 0)
                
                # Запросить последовательный номер кода семантической характеристики объекта (c 1)
                SemNum = mapapi.mapSemanticNumber(hwork, 801)
                
                # Запросить значение семантической характеристики объекта в UNICODE
                SemanticValue = mapsyst.WTEXT(128)
                Semantic_Value = mapapi.mapSemanticValuePro(hwork, SemNum, SemanticValue, SemanticValue.size(), 0)
                SemanticValuetext = SemanticValue.string()
                
                for s in range(1, copy_count+1):
                    new_value = SemanticValuetext + "-" + str(s)
                    # SemanticValue.string(new_value)
                    mapapi.mapSetSemanticValueUn(hwork, SemNum, mapsyst.WTEXT(new_value), len(new_value)) 

                flag = maptype.WO_NEXT
                
            mapapi.mapCommitObjectAsNew(hwork)   
            
    linecount = mapapi.mapPolyCount(hwork) 
    # Освободить ресурсы, связанные с копированием
    if CopyRscObjHwork != 0:
       mapapi.mapFreeObject(CopyRscObjHwork)
    if hwork != 0:
       mapapi.mapFreeObject(hwork)
    mapapi.mapShowMessage(mapsyst.WTEXT('Сформировано линий - ' + mapapi.IntToStr(linecount)), mapsyst.WTEXT('Построение сетки'))

    if hobj != 0:
       mapapi.mapFreeObject(hobj) 

    return retvalues