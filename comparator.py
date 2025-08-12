from tkinter import messagebox
from openpyxl import load_workbook
from collections import defaultdict
import pandas as pd



def start_comparison(sef_path, compare_path):
    print(f"Comparing files:\nLeft: {sef_path}\nRight: {compare_path}\n")
    
    # Load SEF workbook
    
    sef_file = pd.read_excel(sef_path)

    compare_file = pd.read_excel(compare_path)
    
    ime_kolone_id_sef = "ID fakture" if "ID fakture" in sef_file.columns else "ID efakture" if "ID efakture" in sef_file.columns else "ID" if "ID" in sef_file.columns else None
    if ime_kolone_id_sef is None:
        raise ValueError("Промени име колоне у 'ID fakture' или 'ID efakture' у SEF датотеци. И пробај поново.")

    ime_kolone_id_compare = "ID fakture" if "ID fakture" in compare_file.columns else "ID efakture" if "ID efakture" in compare_file.columns else "ID" if "ID" in sef_file.columns else None
    if ime_kolone_id_compare is None:
        raise ValueError("Промени име колоне у 'ID fakture' или 'ID efakture' у датотеци која се упоређује. И пробај поново.")

    sef_file[ime_kolone_id_sef]=sef_file[ime_kolone_id_sef].dropna().astype(str).replace(r"\.0$","",regex=True)
    compare_file[ime_kolone_id_compare]=compare_file[ime_kolone_id_compare].dropna().astype(str).replace(r"\.0$","",regex=True)
    
    
    map_sef_fakt_osnovicaOS=sef_file.groupby(ime_kolone_id_sef)["Osnovica OS"].sum().to_dict()
    map_fakt_osnovicaOS=compare_file.groupby(ime_kolone_id_compare)["Osnovica OS"].sum().to_dict()
    
    map_sef_fakt_PDVOS=sef_file.groupby(ime_kolone_id_sef)["PDV OS"].sum().to_dict()
    map_fakt_PDVOS=compare_file.groupby(ime_kolone_id_compare)["PDV OS"].sum().to_dict()

    map_sef_fakt_osnovicaNS=sef_file.groupby(ime_kolone_id_sef)["Osnovica NS"].sum().to_dict()
    map_fakt_osnovicaNS=compare_file.groupby(ime_kolone_id_compare)["Osnovica NS"].sum().to_dict()

    map_sef_fakt_PDVNS=sef_file.groupby(ime_kolone_id_sef)["PDV NS"].sum().to_dict()
    map_fakt_PDVNS=compare_file.groupby(ime_kolone_id_compare)["PDV NS"].sum().to_dict()


    nepostojeci_kljucevi={ k: v for k, v in {**map_sef_fakt_osnovicaOS,**map_fakt_osnovicaOS}.items()
                          if k  not in map_sef_fakt_osnovicaOS or k not in map_fakt_osnovicaOS
                          }
    
    nepodudarni_kljucevi_osn_os= {
        k: map_sef_fakt_osnovicaOS[k] -map_fakt_osnovicaOS[k]
        
        for k in map_sef_fakt_osnovicaOS.keys() & map_fakt_osnovicaOS.keys()
        if(map_sef_fakt_osnovicaOS[k]!=map_fakt_osnovicaOS[k])
    }
    nepodudarni_kljucevi_pdv_os= {
        k: map_sef_fakt_PDVOS[k] -map_fakt_PDVOS[k]
        
        for k in map_sef_fakt_PDVOS.keys() & map_fakt_PDVOS.keys()
        if(map_sef_fakt_PDVOS[k]!=map_fakt_PDVOS[k])
    }
    
    nepodudarni_kljucevi_osn_ns= {
        k: map_sef_fakt_osnovicaNS[k] -map_fakt_osnovicaNS[k]
        
        for k in map_sef_fakt_osnovicaNS.keys() & map_fakt_osnovicaNS.keys()
        if(map_sef_fakt_osnovicaNS[k]!=map_fakt_osnovicaNS[k])
    }
    
    nepodudarni_kljucevi_pdv_ns= {
        k: map_sef_fakt_PDVNS[k] -map_fakt_PDVNS[k]
        
        for k in map_sef_fakt_PDVNS.keys() & map_fakt_PDVNS.keys()
        if(map_sef_fakt_PDVNS[k]!=map_fakt_PDVNS[k])
    }
    
    return nepodudarni_kljucevi_osn_os,nepodudarni_kljucevi_pdv_os,nepodudarni_kljucevi_osn_ns,nepodudarni_kljucevi_pdv_ns,nepostojeci_kljucevi

    # id_fakture_compare = compare_file[ime_kolone_id_compare].dropna().astype(int).astype(str).tolist() 
    # print(id_fakture_compare)