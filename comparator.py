from tkinter import messagebox
from openpyxl import load_workbook
from collections import defaultdict
import pandas as pd



def start_comparison(sef_path, compare_path):
    print(f"Comparing files:\nLeft: {sef_path}\nRight: {compare_path}\n")
    
    # Load SEF workbook
    
    sef_file = pd.read_excel(sef_path)

    compare_file = pd.read_excel(compare_path)
    
    ime_kolone_id_sef = "ID fakture" if "ID fakture" in sef_file.columns else "ID efakture" if "ID efakture" in sef_file.columns else None
    if ime_kolone_id_sef is None:
        raise ValueError("Промени име колоне у 'ID fakture' или 'ID efakture' у SEF датотеци. И пробај поново.")

    ime_kolone_id_compare = "ID fakture" if "ID fakture" in compare_file.columns else "ID efakture" if "ID efakture" in compare_file.columns else None
    if ime_kolone_id_compare is None:
        raise ValueError("Промени име колоне у 'ID fakture' или 'ID efakture' у датотеци која се упоређује. И пробај поново.")

    sef_file[ime_kolone_id_sef]=sef_file[ime_kolone_id_sef].dropna().astype(str).replace(r"\.0$","",regex=True)
    compare_file[ime_kolone_id_compare]=compare_file[ime_kolone_id_compare].dropna().astype(str).replace(r"\.0$","",regex=True)
    
    
    map_sef_fakt_osnovica=sef_file.groupby(ime_kolone_id_sef)["Osnovica OS"].sum().to_dict()
    map_fakt_osnovica=compare_file.groupby(ime_kolone_id_compare)["Osnovica OS"].sum().to_dict()
    

    nepostojeci_kljucevi={ k: v for k, v in {**map_sef_fakt_osnovica,**map_fakt_osnovica}.items()
                          if k  not in map_sef_fakt_osnovica or k not in map_fakt_osnovica
                          }
    
    nepodudarni_kljucevi= {
        k: map_sef_fakt_osnovica[k] -map_fakt_osnovica[k]
        
        for k in map_sef_fakt_osnovica.keys() & map_fakt_osnovica.keys()
        if(map_sef_fakt_osnovica[k]!=map_fakt_osnovica[k])
    }
    print(nepostojeci_kljucevi)
    print(nepodudarni_kljucevi)
    return nepodudarni_kljucevi,nepostojeci_kljucevi

    # id_fakture_compare = compare_file[ime_kolone_id_compare].dropna().astype(int).astype(str).tolist() 
    # print(id_fakture_compare)