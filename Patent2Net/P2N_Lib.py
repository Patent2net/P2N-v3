# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 08:50:16 2014
All in one low level functions
@author: dreymond
"""
IPCRCodes = {'A': 'HUMAN NECESSITIES', 'B': 'PERFORMING OPERATIONS; TRANSPORTING', 'C': 'CHEMISTRY; METALLURGY',
             'D': 'TEXTILES; PAPER', 'E': 'FIXED CONSTRUCTIONS', 'F': 'MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING',
             'G': ' PHYSICS', 'H': 'ELECTRICITY'}
Status = ['A', 'B', 'C', 'U', 'Y', 'Z', 'M', 'P', 'S',
          'L', 'R', 'T', 'W', 'E', 'F', 'G', 'H', 'I', 'N', 'X']
SchemeVersion = '20140101'
#    A – First publication level
#    B – Second publication level
#    C – Third publication level
# Group 2 – Use for utility model documents having a numbering series other than the documents of Group 1:
#    U – First publication level
#    Y – Second publication level
#    Z – Third publication level
# Group 3 – Use for special series of patent documents as specified below:
#    M – Medicament patent documents (e.g., documents previously published by FR)
#    P – Plant patent documents (e.g., published by US)
#    S – Design patent documents (e.g., published by US)
# Group 4 – Use for special types of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 3, above, as specified below:
#    L – Documents, not covered by the letter code W, relating to patent documents and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#    R – Separately published search reports
#    T – Publication, for information or other purposes, of the translation of the whole or part of a patent document already published by another office or organization
#    W – Documents relating to utility model documents falling in Group 2 and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
# Group 5 – Use for series of patent documents not covered by Groups 1 to 4, above:
#    E – First publication level
#    F – Second publication level
#    G – Third publication level
# Group 6 – Use for series of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 5, above, according to the special requirements of each industrial property office:
#    H
#    I
# Group 7 – Other (see paragraph 2, above):
#    N – Non-patent literature documents
#    X ]

import codecs
import datetime
import os
import re

import requests
from jinja2 import Environment, FileSystemLoader


def AnnonceProgres(Appli, valActu, valMax):
    if valActu and valMax:
        valActu = "%.2f" % valActu 
        try:
            requests.get('http://localhost:5000/announce?appli=%s&ValActu=%s&valMax=%s' %(Appli, valActu, valMax) )
        except:
            pass
    else:
        pass # must be a error
#☻    print ('annnonce envoyée: ', pipo)

def AnnonceLog(Appli, texte):

    try:
        requests.get('http://localhost:5000/announce?appli=%s&log=%s' %(Appli+'Log', texte) )
    except:
        pass


def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT de l'arborescence"""
    import os
    listeFicFR = []
    listeFicEN = []
    listeFicUNK = []
    for root, subFolders, files in os.walk(rep):

        if len(subFolders)>0:
            for sousRep in subFolders:
                temporar = GenereListeFichiers(rep+'//'+sousRep)
                listeFicFR.extend(temporar[0])
                listeFicEN.extend(temporar[1])
                listeFicUNK.extend(temporar[2])
        else:
            for fichier in files:
                if fichier.endswith('.txt') and fichier.startswith('fr'):
                    listeFicFR.append(root+'//'+fichier)
                elif fichier.endswith('.txt') and fichier.startswith('en'):
                    listeFicEN.append(root+'//'+fichier)
                else:
                    if fichier.endswith('.txt'):
                        listeFicUNK.append(root+'//'+fichier)
                
    return (list(set(listeFicFR)), list(set(listeFicEN)), list(set(listeFicUNK)))


def Normalise(listeFic):
    """Necessary becaus in OPSGatentsPAtents, I didn't care about abstracts name,
    there is a missing '-' in name creation: should be LANG-PatentNum.txt"""
    cpt = 0    
    for fic in listeFic:
        if fic.count('Abstracts')>0:
            tmp = fic.split('//')
            nomDeFic = tmp[len(tmp)-1]
            NouveauNom = nomDeFic[0:2].replace('-', '')  +'-'+ nomDeFic[2:].replace('-', '')

            try:
                os.rename(fic, fic.replace(nomDeFic, NouveauNom))
                cpt+=1
            except:
                pass
    print(cpt, " Abstracts files Names normalized") 

def coupeEnMots(texte):
    "returns a list of words cleaned from punctuation, digits and other signs"
    if isinstance(texte, list):
        texte = ' '.join(texte)
    texte = texte.lower()
    res = re.sub('["\'<>]', ' ', texte)  # on vire une partie de la ponctuation
    res = re.sub('\d', ' ', res)  # extraction des chiffres
    res = re.findall('\w+', res, re.UNICODE)  # extraction des lettres seulement
    return res


def LectureFichier(fic):
    """read the file, and return purged from coupeEnMots content if lenght is greater thar arbitrary value, here 5"""
    with open(fic) as fi:
            lect = fi.read()
            if len(' '.join(coupeEnMots(lect)))> 5: #arbitrary
                contenu =lect +'\n'
                return contenu
            else:
                return None
                
def complete(listeFic, lang, det):
   
    resum = [fi for fi in set(listeFic) if fi.count(det)>0]
#    desc = [fi for fi in set(listeFic) if fi.count('description')>0]
#    autres = [fi for fi in set(listeFic) if fi not in resum and fi not in desc]
    dejaVu = []
    Ignore = 0

    Contenu = """"""
    for fichier in set(resum):
        dejaVu.append(fichier)
        if LectureFichier(fichier) is not None:
            Contenu+=LectureFichier(fichier)
        else:
            Ignore+=1
#            tmp = fichier.name.split('//')
            
#        if FicResume in resum:
#            dejaVu.append(FicResume)
#            if LectureFichier(FicResume) is not None:
#                Contenu+=LectureFichier(FicResume)
#            else:
#                Ignore+=1
#        FicRevend= fichier.replace('description', 'claims')
#        if FicRevend in autres:
#            dejaVu.append(FicRevend)
#            if LectureFichier(FicRevend) is not None:
#                Contenu+=LectureFichier(FicRevend)
#            else:
#                Ignore+=1
#                
#    for fichier in set(autres):
#        
#        if fichier not in dejaVu:
#            dejaVu.append(FicResume)
#            if LectureFichier(fichier) is not None:
#                Contenu+=LectureFichier(fichier)
#            else:
#                Ignore+=1
    print(len(set(resum)), "fichiers "+det+ " à traiter en langage : ", lang)
    print(len(dejaVu), " fichiers "+det+ " traités", end=' ')
    if Ignore >0:
        print(" et ", Ignore, " fichier(s) ignores")

    return Contenu

                
def complete2(listeFic, lang, det):
   
    resum = [fi for fi in set(listeFic) if fi.count(det)>0]
    dejaVu = []
    Ignore = 0

    Contenu = """"""
    for fichier in set(resum):
        dejaVu.append(fichier)
        if LectureFichier(fichier) is not None:
            temporar=LectureFichier(fichier)
            #cleaning temporarrary this should be done at gathering process
            temp = temporar.split('\n')[1].strip()
            if temp not in Contenu:
                temporar = temporar.replace('*Pays', '*Country')
                temporar = temporar.replace('*Contenu_Abstract ', '')
                temporar = temporar.replace('*Nom', '*Label')
                temporar = temporar.replace('*Deposant_', '*Applicant_')
                temporar = temporar.replace('*CIB1_ ', '*CIB1_empty ')
                temporar = temporar.replace('*CIB3_ ', '*CIB3_empty ')
                temporar = temporar.replace('*CIB4_ ', '*CIB4_empty ')
                temporar = temporar.replace('_empty*', '_empty *')
                temporar = temporar.replace('*Applicant_ ', '*Applicant_empty ')
                temporar = temporar.replace('*Country_ ', '*Country_empty ')
                temporar = temporar.replace('*Label_ ', '*Label_empty ')
                Contenu += temporar
            else:
                Ignore+=1
                
            
        else:
            Ignore+=1
    print(len(set(resum)), "fichiers "+det+ " à traiter en langage : ", lang)
    print(len(dejaVu), " fichiers "+det+ " traités", end=' ')
    if Ignore >0:
        print(" et ", Ignore, " fichier(s) ignores (non dédoublés)")

    return Contenu

def isMaj(car):
    if car.lower() != car:
        return True
    else:
        return False


def ReturnBoolean(string):
    if string.count('True') > 0 or string.count('true') > 0:
        return True  # to gather contents
    else:
        return False


def CleanPatent(dico):

    if isinstance(dico, dict):
        res = dict()
        lstCle = list(dico.keys())
        for cle in lstCle:
            if isinstance(dico[cle], list):
                if len(dico[cle]) == 1:
                    if isinstance(dico[cle][0], list):
                        if len(dico[cle][0]) > 1:
                            res[cle] = CleanPatent(dico[cle][0])
                        else:
                            res[cle] = str(CleanPatent(dico[cle][0][0]))
                    else:
                        res[cle] = str(CleanPatent(dico[cle][0]))
                elif len(dico[cle]) > 1:
                    tempo = []
                    for content in dico[cle]:
                        if CleanPatent(content) not in tempo:
                            tempo.append(CleanPatent(content))
                    res[cle] = tempo  # print "hum"
                else:
                    res[cle] = ''
            elif dico[cle] == 'N/A':
                res[cle] = ''
            elif isinstance(dico[cle], dict):
                res[cle] = CleanPatent(dico[cle])
            else:
                res[cle] = CleanPatent(dico[cle])
        return res
    elif isinstance(dico, list):
        if len(dico) == 1:
            return CleanPatent(dico[0])
        else:
            res = []
            for ent in dico:
                temp = CleanPatent(ent)

                if temp is not None and len(temp) > 0:
                    res.append(temp)
            return res
    elif isinstance(dico, str) or isinstance(dico, str):
        return dico


def getStatus2(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['kind']
    return ''


def getClassif(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['IPCR11']
    return ''


def getCitations(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            if 'Citations' in Brev:
                return Brev['Citations']
            else:
                return 0
    return 0


def getFamilyLenght(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            if 'family lenght' in Brev:
                return Brev['family lenght']
            else:
                return 0
    return 0


def getPrior(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['prior']
    return ''


def getActiveIndicator(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['priority-active-indicator']
    return 0


def getRepresentative(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['representative']
    return 0


def UnNest3(NestedList):
    res = []
    if isinstance(NestedList, list):
        for con in NestedList:
            if isinstance(con, list):
                res.extend(UnNest3([x for x in con if x is not None]))
            elif con is not None:
                res.append(con)
            else:
                pass
    else:
        res.append(NestedList)
    return res


def UnNest(liste):
    #assert isinstance(liste, list)
    if liste is not None:
        if isinstance(liste, list):
            if len(liste) > 1:
                temp = []
                for cont in liste:
                    if isinstance(cont, list) and cont is not None:
                        tempo = []

                        for contenu in cont:
                            if contenu is not None:
                                if contenu != '' and contenu != '':
                                    Tpr = UnNest(contenu)
                                    if Tpr != '':
                                        tempo.append(Tpr)
                        if len(tempo) > 0:
                            temp.extend(tempo)
                    elif cont is not None:
                        if cont != '' and cont != '':
                            temp.append(cont)
                    else:
                        pass
                return temp
            elif len(liste) == 1:
                if isinstance(liste[0], list):
                    return UnNest(liste[0])
                elif len(liste[0]) > 0:
                    return liste[0]
                else:
                    return ''
            else:
                return ''

        else:
            return liste
    else:
        return ''


def DecoupeOnTheFly(dico, filt):
    "same as decoupe2 "
    " keys of filt shoud be excluded"
    #import cPickle
    Res = dict()
    import copy
    lstCle = [cle for cle in list(dico.keys()) if cle not in filt]

    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]
    for cle in KeyCheck:
        if len(dico[cle]) == 1:
            if dico[cle][0] is not None:
                if isinstance(dico[cle][0], int) or len(dico[cle][0]) > 0:
                    dico[cle] = dico[cle][0]
                else:
                    dico[cle] = ""
            else:
                dico[cle] = ""
        elif len(dico[cle]) == 0:
            dico[cle] = ""
        else:
            dico[cle] = [cont for cont in dico[cle] if cont != '']
    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]
    for cle in KeyCheck:
        Porar = flatten(dico[cle])
        Porar2 = []
        for truc in Porar:
            if truc is not None:
                truc = truc.replace(',', '')
                truc = truc.replace('  ', ' ')
                if truc not in Porar2:
                    Porar2.append(truc)

        # not in dico[cle]] #try to avoid repetition... multiples values detected from OPS fields
        dico[cle] = Porar2

    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]

    # cPickle.dump(nb, fichier) # saving number of entries
    # initialization ; copping monovaluated values
    import networkx as nx

    Result = []

    for cle in [key for key in lstCle if key not in KeyCheck]:
        Res[cle] = dico[cle]

    if len(KeyCheck) == 0:

        return [copy.copy(dico)]
    else:
        temp = [dico[key] for key in KeyCheck]

        if len(KeyCheck) == 1:
            for val in flatten(temp):
                Res[KeyCheck[0]] = val
                #pickle.dump(copy.deepcopy(Res), fic)

#                buf = buffer(Resul,0)
                Result.append(copy.copy(Res))
            return Result

        else:
            #    nb = prod([len(temp[i]) for i in range(len(temp))])
            G = nx.DiGraph()
            for ind in range(len(temp) - 1):
                for noeud1 in temp[ind]:
                    for noeud2 in temp[ind + 1]:
                        # adding key for similar values in differents keys
                        G.add_edge(noeud1 + KeyCheck[ind], noeud2 + KeyCheck[ind + 1])

            for noeud in dico[KeyCheck[0]]:
                for noeud2 in dico[KeyCheck[len(KeyCheck) - 1]]:
                    try:
                        for path in nx.all_simple_paths(G, noeud + KeyCheck[0], noeud2 + KeyCheck[len(KeyCheck) - 1]):
                            ind = 0
                            for cle in KeyCheck:
                                Res[cle] = path[ind].replace(cle, '')
                                ind += 1
                            Result.append(copy.copy(Res))
                    except:
                        print()
            return Result


def Decoupe2(dico, filt):
    "same as decoupe but with more cleaned values in entrance"
    Res = dict()
    lstCle = [cle for cle in list(dico.keys()) if cle not in filt]
    KeyCheck = [key for key in lstCle if isinstance(dico[key], list) and len(dico[key]) > 0]
    for key in KeyCheck:
        if len(dico[key]) == 1:
            dico[key] = dico[key][0]
            if isinstance(dico[key], list) and len(dico[key]) == 1:
                dico[key] = dico[key][0]
                KeyCheck.remove(key)
        if len(dico[key]) == 0:
            KeyCheck.remove(key)
        if len(dico[key]) == 1 and key in KeyCheck:
            dico[key] = dico[key][0]
            if not isinstance(dico[key], list):
                KeyCheck.remove(key)
#        if key in KeyCheck and isinstance(dico[key], list) and len(dico[key])==1:
#                print "again ?????"
    KeyCheck = [key for key in lstCle if isinstance(dico[key], list) and len(dico[key]) > 1]
#    for key in KeyCheck:
#        if len(dico[key]) == 1:
#            dico[key] = dico[key][0]
#            if not isinstance(dico[key], list):
#                KeyCheck.remove(key)
    # caculating nombre of monovaluated entries
    KeyCheck = [key for key in KeyCheck if key not in filt]
    nb = prod([len(dico[cle]) for cle in KeyCheck])

    # initialization ; copping monovaluated values
    for k in range(nb):
        Res[k] = dict()
        for cle in lstCle:
            if cle not in KeyCheck:
                Res[k][cle] = dico[cle]
    # for each multivaluated entry, copying  each value as needed

    for cle in KeyCheck:
        num = 0
        for content in dico[cle]:
            for nombre in range(nb / len(dico[cle])):
                Res[(nb / len(dico[cle])) * num + nombre][cle] = content
            num += 1

#    for pat in Res.keys():
#        if len([cle for cle in dico.keys() if cle not in Res[pat].keys()]):
#            print "is no good"
    return Res


def ExtraitContenuDict(dico, listeCle):
    if len(listeCle) == 1:
        if listeCle[0].isdigit():
            return dico[int(listeCle[0])]  # hope it is in keys....
        else:
            return dico[listeCle[0]]
    elif listeCle[0].isdigit():
        return ExtraitContenuDict(dico[int(listeCle[0])], listeCle[1:])
    else:
        return ExtraitContenuDict(dico[listeCle[0]], listeCle[1:])


def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


def flatten_dict(d, separator='****'):
    from collections import OrderedDict as dict
    import collections
    final = dict()

    def _flatten_dict(obj, parent_keys=[]):
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, collections.Mapping):
                _flatten_dict(v, parent_keys + [k])
            elif isinstance(v, list):
                cpt = 0
                for sub in v:
                    _flatten_dict(sub, parent_keys + [k + separator + str(cpt)])
                    cpt += 1
            else:
                key = separator.join(parent_keys + [k])
                final[key] = v
    _flatten_dict(d)
    return final


def Decoupe3(dico, filt, fic):
    "same as decoupe2 but with disk saving for each entry"
    #import cPickle
    Res = dict()
    lstCle = [cle for cle in list(dico.keys()) if cle not in filt]

    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]
    for cle in KeyCheck:
        if len(dico[cle]) == 1:
            if dico[cle][0] is not None and len(dico[cle][0]) > 0:
                dico[cle] = dico[cle][0]
            else:
                dico[cle] = ""
        elif len(dico[cle]) == 0:
            dico[cle] = ""
        else:
            dico[cle] = [cont for cont in dico[cle] if cont != '']
    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]
    for cle in KeyCheck:
        dico[cle] = flatten(dico[cle])

    KeyCheck = [key for key in lstCle if isinstance(dico[key], list)]
#

    # cPickle.dump(nb, fichier) # saving number of entries
    # initialization ; copping monovaluated values
    import networkx as nx

    import pickle as pickle
    nb = 0
    #Resul = []

    for cle in [key for key in lstCle if key not in KeyCheck]:
        Res[cle] = dico[cle]

    if len(KeyCheck) == 0:

        pickle.dump(Res, fic, protocol=-1)
        return 1
    else:
        temp = [dico[key] for key in KeyCheck]
        if len(KeyCheck) == 1:
            for val in temp:
                Res[KeyCheck[0]] = val
                #pickle.dump(copy.deepcopy(Res), fic)

#                buf = buffer(Resul,0)
                pickle.dump(Res, fic, protocol=-1)
            return len(temp)

        else:
            #    nb = prod([len(temp[i]) for i in range(len(temp))])
            G = nx.DiGraph()
            for ind in range(len(temp) - 1):
                for noeud1 in temp[ind]:
                    for noeud2 in temp[ind + 1]:
                        # adding key for similar values in differents keys
                        G.add_edge(noeud1 + KeyCheck[ind], noeud2 + KeyCheck[ind + 1])

            for noeud in dico[KeyCheck[0]]:
                for noeud2 in dico[KeyCheck[len(KeyCheck) - 1]]:
                    for path in nx.all_simple_paths(G, noeud + KeyCheck[0], noeud2 + KeyCheck[len(KeyCheck) - 1]):
                        ind = 0
                        for cle in KeyCheck:
                            Res[cle] = path[ind].replace(cle, '')
                            ind += 1

                        nb += 1
                        pickle.dump(Res, fic, protocol=-1)  # copy.deepcopy(Res)


#    for k in range(nb):
#        Res = dict()
#        for cle in [key for key in lstCle if key not in KeyCheck]:
#            #if cle not in KeyCheck:
#                Res[cle] = dico[cle]
#    # for each multivaluated entry, copying  each value as needed
#
#        for cle2 in KeyCheck:
#            num = 0
#            for content in dico[cle2]:
#                tempo = KeyCheck
#                tempo.remove(cle2)
#                for nombre in range(nb/len(dico[cle2])):
#                    Res[cle2] = content
#
#                    for rest in tempo:
#                        Res(tempo)
#                num+=1
#            cPickle.dump(Res, fichier)

#    for pat in Res.keys():
#        if len([cle for cle in dico.keys() if cle not in Res[pat].keys()]):
#            print "is no good"
    # print nb, '--->', len(Solu)
    return nb


def ApparieListe2(lst1):
    """Explose the list lst to produce a list of pairs"""
    if isinstance(lst1, list) and len(lst1) > 2:
        Res = [[lst1[0], num] for num in lst1[1:]]
        if len(lst1[1:]) > 2:
            Res.extend(ApparieListe2(lst1[1:]))
            return Res
        elif len(lst1[1:]) == 2:
            Res.append([lst1[1], lst1[2]])
            return Res
        else:
            return Res
    elif len(lst1) == 2:
        return [[lst1[0], lst1[1]]]
    else:
        return lst1


def ComputeTempoNom(noeud):
    tempoNom = ""
    for car in noeud:
        if len(tempoNom) == 0:
            tempoNom += car
        else:
            if isMaj(car):
                tempoNom += ' ' + car
            else:
                tempoNom += car
    return tempoNom


def Decoupe(dico):
    """will return a list of dictionnary patents monovaluated as long as the product of multivalued entries"""
    Res = dict()
    remp = dict()
    lstCle = list(dico.keys())
    # comment added in V2: should be no reasons for cleaning now
#    dico = CleanPatent(dico)
#    for cle in lstCle:
#        if isinstance(dico[cle], list):
#            temp = [CleanPatent(k) for k in dico[cle] if k != 'N/A' and k != None and k!='']
#            if len(temp) ==1:
#                if isinstance(temp[0], list) and len(temp[0])>1:
#                    remp[cle] = UnNest(temp[0])
#                else:
#                    pass
#            if len(temp) ==0:
#                pass
#            else:
#                remp[cle] = temp
#        else:
#            pass
    i = 1
    # calculating combinatory results. Each list multiplies others...
    nombre = prod([i * len(remp[cle])
                   for cle in list(remp.keys()) if isinstance(remp[cle], list) and len(remp[cle]) != 0])
    # preparing result dictionnary
    for num in range(nombre):
        Res[num] = dict()
        for cle in lstCle:
            if cle not in list(remp.keys()):  # unique content, not list for these keys
                Res[num][cle] = dico[cle]
    # for keys that dico[keys] are lists
    for cle2 in list(remp.keys()):
        cpt = 0
        for content in remp[cle2] * (nombre / len(remp[cle2])):
            # for each content, write it this entry
            Res[cpt][cle2] = content
            # copy also others content for each content from different key
            # for this entry (cpt)
            for cle3 in list(remp.keys()):
                if cle3 != cle2:
                    for content2 in remp[cle3]:
                        Res[cpt][cle3] = content2
            # next entry # this should stop at en end of resultset
            cpt += 1

#            elif len(remp[cle])>0:
#                Res[num][cle] = remp[cle][num % len(remp[cle])]
#            else:
#                Res[num][cle] = dico[cle]
#    retour=[]
#    for k in Res.keys():
#        if Res[k] not in retour:
#            retour.append(Res[k])
    for bre in Res:
        for cle in lstCle:
            if isinstance(Res[bre][cle], list):
                print("pas glop")  # this should not append
    return Res


def SeparateCountryField(pat):
    if "Inventor-Country" in list(pat.keys()):
        if len(pat["Inventor-Country"]) > 0:
            return pat  # no changes
    if "Applicant-Country" in list(pat.keys()):
        if len(pat["Applicant-Country"]) > 0:
            return pat  # no changes

    PaysInv = []  # new field
    PaysApp = []
    brev = pat
    if not isinstance(pat, dict):
        print("pas gloup")
    if brev['inventor'] is not None:

        if isinstance(brev['inventor'], list):
            tempoInv = []
            for inv in brev['inventor']:
                tempPaysInv = inv.split('[')
                if isinstance(tempPaysInv, list):
                    for kk in range(1, len(tempPaysInv), 2):
                        PaysInv.append(tempPaysInv[kk].replace(']', ''))
                    tempoInv.append(tempPaysInv[0].strip())
                else:
                    tempoInv.append(tempPaysInv.strip())
            brev["inventor"] = tempoInv

        else:
            tempPaysInv = brev['inventor'].split('[')
            if isinstance(tempPaysInv, list):
                for kk in range(1, len(tempPaysInv), 2):
                    PaysInv.append(tempPaysInv[kk].replace(']', ''))
                brev["inventor"] = tempPaysInv[0].strip()
            else:
                tempoInv.append(tempPaysInv.strip())
    if brev['applicant'] is not None:

        if isinstance(brev['applicant'], list):
            tempoApp = []
            for APP in brev['applicant']:
                tempPaysApp = APP.split('[')
                if isinstance(tempPaysApp, list):
                    for kk in range(1, len(tempPaysApp), 2):
                        PaysApp.append(tempPaysApp[kk].replace(']', ''))
                    tempoApp.append(tempPaysApp[0].strip())
                else:
                    tempoApp.append(tempPaysApp.strip())
            brev["applicant"] = tempoApp
        else:

            tempPaysApp = brev['applicant'].split('[')
            if isinstance(tempPaysApp, list):
                for kk in range(1, len(tempPaysApp), 2):
                    PaysApp.append(tempPaysApp[kk].replace(']', ''))
                brev["applicant"] = tempPaysApp[0].strip()
            else:
                brev["applicant"] = tempPaysApp.strip()
    brev["Inventor-Country"] = list(set(PaysInv))
    brev["Applicant-Country"] = list(set(PaysApp))
    if isinstance(brev["Inventor-Country"], list) and len(brev["Inventor-Country"]) == 0:
        brev["Inventor-Country"] = ""
    if isinstance(brev["Applicant-Country"], list) and len(brev["Applicant-Country"]) == 0:
        brev["Applicant-Country"] = ""
    return brev


def CleanPatentOthers(brev):
    tempo = dict()
    import bs4
    for cle in list(brev.keys()):
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in list(tempoClass.keys()):
                            if cle2 == 'classification':
                                if cle2 in tempo and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif cle2 in tempo and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in list(tempo.keys()):
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
#                                if tempoClass[cle2] not in tempo2[cle2]:
#                                    tempo2[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
                            else:
                                tempo[cle2] = []
#                                tempo[cle2].append(tempoClass[cle2])
#                                tempo2[cle2].append(tempoClass[cle2])

                else:
                    temp = [str(a) for a in brev[cle]]
                    tempo[cle] = temp

            elif cle == 'titre':
                temp = str(brev[cle]).replace('[', '').replace(']', '').lower().capitalize()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle == 'date' and brev['date'] is not None:
                try:
                    tempo[cle] = str(brev['date'].year) + '-' + \
                        str(brev['date'].month) + '-' + str(brev['date'].day)
                except:
                    tempo[cle] = brev['date'][0:4]
                # tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle == 'classification' and brev['classification'] != '':
                tempoClass = ExtractClassificationSimple2(brev['classification'])
                for cle in list(tempoClass.keys()):
                    if cle in list(tempo.keys()) and tempoClass[cle] not in tempo[cle]:
                        if tempoClass[cle] != 'N/A':
                            tempo[cle].append(tempoClass[cle])
                    elif tempoClass[cle] != 'N/A':
                        tempo[cle] = []
                        tempo[cle].append(tempoClass[cle])
                    else:
                        tempo[cle] = ''
            elif isinstance(brev[cle], dict):
                tempo[cle] = brev[cle]

            else:
                temp = str(brev[cle])  # .replace('[','').replace(']', '')
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

        else:
            tempo[cle] = ''

    return tempo


def CleanPatentOthers2(brev):
    tempo = dict()
    import bs4
    for cle in list(brev.keys()):
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in list(tempoClass.keys()):
                            if cle2 == 'classification':
                                if cle2 in tempo and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif cle2 in tempo and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in list(tempo.keys()):
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
#                                if tempoClass[cle2] not in tempo2[cle2]:
#                                    tempo2[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
                            else:
                                tempo[cle2] = []
#                                tempo[cle2].append(tempoClass[cle2])
#                                tempo2[cle2].append(tempoClass[cle2])

                else:
                    temp = [str(a) for a in brev[cle]]
                    tempo[cle] = temp

            elif cle == 'titre':
                temp = str(brev[cle]).replace('[', '').replace(']', '').lower().capitalize()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle == 'date' and brev['date'] is not None:
                try:
                    # this the only diff with cleanPatentOther +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                    tempo[cle] = str(brev['date'].year)
                except:
                    tempo[cle] = brev['date'][0:4]
                # tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle == 'classification' and brev['classification'] != '':
                tempoClass = ExtractClassificationSimple2(brev['classification'])
                for cle in list(tempoClass.keys()):
                    if cle in list(tempo.keys()) and tempoClass[cle] not in tempo[cle]:
                        if tempoClass[cle] != 'N/A':
                            tempo[cle].append(tempoClass[cle])
                    elif tempoClass[cle] != 'N/A':
                        tempo[cle] = []
                        tempo[cle].append(tempoClass[cle])
                    else:
                        tempo[cle] = ''
            elif isinstance(brev[cle], dict):
                tempo[cle] = brev[cle]

            else:
                temp = str(brev[cle])  # .replace('[','').replace(']', '')
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

        else:
            tempo[cle] = ''

    return tempo


def prod(liste):
    Res = 1
    for k in liste:
        Res = Res * k
    return Res


def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud


def symbole(IPC):
    if len(IPC) == 1:
        return IPC
    if len(IPC) == 3:
        return IPC
    if len(IPC) == 4:
        return IPC

    subclass = IPC[0:4]
    if IPC.count('/') > 0:
        maingroup = IPC[4:].split('/')[0]
        subgroup = IPC[4:].split('/')[1]
    elif len(IPC) == 14:
        maingroup = IPC[4:8]
        subgroup = IPC[8:]
    elif len(IPC) > 4 and len(IPC) < 14:
        maingroup = IPC[4:]
        subgroup = ''
    else:
        #        print "not good symbol", IPC
        return ''
    maingroup = re.sub("^0+", "", maingroup)
    maingroup = (4 - len(maingroup)) * '0' + maingroup
    subgroup = subgroup + (6 - len(subgroup)) * '0'
    return subclass + maingroup + subgroup


def ContractList(liste):

    res = []
    for Ens in liste:
        if isinstance(Ens, list):
            for u in Ens:
                if u not in res:
                    res.append(u)
        elif isinstance(Ens, str):
            if Ens not in res:
                res.append(Ens)
        else:
            return liste
    return res


def ExtractClassificationSimple(data):
    res = []
    if data is not None:
        if isinstance(data, list) and len(data) == 1:
            data = data[0]
        elif isinstance(data, list):
            for classi in data:
                res.append(ExtractClassificationSimple(classi))
        if type(data) == type("") or type(data) == type(""):
            Resultat = dict()
            Resultat['classification'] = data
            data = data.replace(' ', '', data.count(' '))
            Resultat['IPCR11'] = data

            Resultat['IPCR1'] = data[0]
            if len(data) > 2:
                Resultat['IPCR3'] = data[0:3]
            else:
                Resultat['IPCR3'] = ''
            if len(data) > 4:
                Resultat['IPCR4'] = data[0:4]
                if not Resultat['IPCR4'][3].isalpha():  # consistency control
                    Resultat['IPCR4'] = ''

            else:
                Resultat['IPCR4'] = ''
            if data.count('/') > 0:
                Resultat['IPCR7'] = data.split('/')[0]
            else:
                Resultat['IPCR7'] = ''
            Resultat['status'] = data[len(data) - 1:]
            if Resultat['status'] not in Status or data[len(data) - 2].isalpha():
                Resultat['status'] = data[len(data) - 2:]
                if Resultat['status'][0] not in Status:
                    Resultat['status'] = ''
                else:
                    Resultat['IPCR11'] = data[0:len(data) - 2]
            else:
                Resultat['IPCR11'] = data[0:len(data) - 1]
            if Resultat['IPCR11'][len(Resultat['IPCR11']) - 2:len(Resultat['IPCR11'])].count('0') > 1:
                # consistency check : if result endswith 0, means that is an IPCR7
                Resultat['IPCR11'] = ''

            res = Resultat
        else:
            print("should not be here, pb in classification content")
    else:
        print("should not be here, pb in classification content")
    return res


def ExtractClassificationSimple2(data):
    res = []
    if data is not None and data != '':
        if isinstance(data, list) and len(data) == 1:
            data = data[0]
        elif isinstance(data, list):  # strange assertion here... 30/09/15
            print("paté")  # assert isinstance(data, list)
        if type(data) == type("") or type(data) == type(""):
            Resultat = dict()

            data = data.replace(' ', '', data.count(' '))
            # checking last two caracter some contains status data...
            if data[len(data) - 2].isalpha():
                Resultat['IPCR11'] = data[0:len(data) - 2]
            elif data[len(data) - 1].isalpha():
                Resultat['IPCR11'] = data[0:len(data) - 1]
            else:
                Resultat['IPCR11'] = data

           #Resultat['classification'] = Resultat['IPCR11']
            Resultat['IPCR1'] = data[0]
            if len(data) > 2:
                Resultat['IPCR3'] = data[0:3]
            else:
                Resultat['IPCR3'] = ''
            if len(data) > 4:
                Resultat['IPCR4'] = data[0:4]
                if not Resultat['IPCR4'][3].isalpha():  # consistency control
                    Resultat['IPCR4'] = ''

            else:
                Resultat['IPCR4'] = ''
            if data.count('/') > 0:
                Resultat['IPCR7'] = data.split('/')[0]
            else:
                Resultat['IPCR7'] = ''
            if Resultat['IPCR11'][len(Resultat['IPCR11']) - 2:len(Resultat['IPCR11'])].count('0') > 1:
                # Resultat['IPCR7']+'00' # consistency check : if result endswith 0, means that is an IPCR7
                Resultat['IPCR11'] = ""

            res = Resultat
        else:
            print("should not be here, pb in classification content")
    else:
        resultat = dict()
        for ipc in ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']:
            resultat[ipc] = ''
        res = resultat
    return res


def ExtractEquiv(data):
    if isinstance(data, list):
        return [ExtractEquiv(donne) for donne in data]
    else:
        return data['publication-reference']['document-id']['doc-number']['$']


def ExtractAbstract(ch):
    tempo = ch
    TXT = dict()
    if isinstance(tempo, list):
        for abst in tempo:
            if '@lang' in abst:
                lang = abst['@lang']
            if 'p' in abst:
                if isinstance(abst['p'], list):
                    for para in abst['p']:
                        if lang in TXT:
                            TXT[lang] += para['$'] + '\n'
                        else:
                            TXT[lang] = para['$'] + '\n'
                else:
                    TXT[lang] = abst['p']['$']
    else:
        if '@lang' in tempo:
            lang = tempo['@lang']
        if 'p' in tempo:
            if isinstance(tempo['p'], list):
                for para in tempo['p']:

                    if lang in TXT:
                        TXT[lang] += para['$'] + '\n'
                    else:
                        TXT[lang] = para['$'] + '\n'
            else:
                TXT[lang] = tempo['p']['$'] + '\n'
    return TXT


def ExtractClassification2(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None:
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple2(te)
                    for cle in list(tempo.keys()):
                        if cle in res:
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple2(classif)
                    for cle in list(tempo.keys()):
                        if cle in res:
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, str) or isinstance(data, str):
            tempo = ExtractClassificationSimple2(data)
            for cle in list(tempo.keys()):
                if cle in res:
                    if tempo[cle] not in res[cle]:
                        res[cle].append(tempo[cle])
                else:
                    res[cle] = []
                    res[cle].append(tempo[cle])
        else:
            print("should not be here, pb in classification content")
    else:
        resultat = dict()
        for ipc in ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
# if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
# for cle in res[0].keys():
##                    resu[cle] = []
# for dic in res:
# for cle in dic.keys():
# resu[cle].append(dic[cle])
# for cle in resu.keys():
# if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res


def ExtractSubReferenceP(content):
    refsP = ""
    if 'patcit' in content:  # patents
        try:
            # arbitrary choice of epodoc... What if not present I don't know
            refsP = content['patcit']['document-id'][0]['doc-number']['$']
        except:
            # arbitrary choice of epodoc... What if not present I don't know
            refsP = content['patcit']['document-id']['doc-number']['$']
    return refsP


def ExtractSubReferenceO(content):
    refsO = ""
    if 'nplcit' in content:  # Others
        refsO = content['nplcit']['text']['$']
    return refsO


def ExtractReference(pat):
    if "references-cited" in str(pat):
        citing = pat['bibliographic-data']['references-cited']['citation']
        if isinstance(citing, list):
            refP = [ExtractSubReferenceP(cit) for cit in citing]
            refO = [ExtractSubReferenceO(cit) for cit in citing]

        else:
            refP = [ExtractSubReferenceP(citing)]
            refO = [ExtractSubReferenceP(citing)]
        return refP, refO
    else:
        return ["", ""]


def ExtractSubCPC(content):
    # content must be in list : patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data'][u'patent-classifications'][u'patent-classification']
    # entering with patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']
    if '@scheme' in content['classification-scheme']:
        if content['classification-scheme']['@scheme'] == 'CPC':
            # u'classification-value': {u'$': u'I'}, u'section': {u'$': u'F'}, u'subclass': {u'$': u'V'}, u'main-group': {u'$': u'3'}, u'class': {u'$': u'21'}, u'subgroup'
            return content['section']['$'] + content['class']['$'] + \
                content['subclass']['$'] + content['main-group']['$'] + \
                '/' + content['subgroup']['$']
        else:
            pass
            # print "no CPC "
    else:
        return 'empty'


def ExtractCPC(pat):
    if 'patent-classifications' in str(pat):
        con = pat['bibliographic-data']['patent-classifications']['patent-classification']
        if isinstance(con, list):
            CPC = [ExtractSubCPC(co) for co in con]
        else:
            CPC = [ExtractSubCPC(con)]
        return CPC
    else:
        return 'empty'


def ExtractClassification(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None and data != '':
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple(te)
                    for cle in list(tempo.keys()):
                        if cle in res:
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple(classif)
                    for cle in list(tempo.keys()):
                        if cle in res:
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, str) or isinstance(data, str):
            tempo = ExtractClassificationSimple(data)
            for cle in list(tempo.keys()):
                if cle in res:
                    if tempo[cle] not in res[cle]:
                        res[cle].append(tempo[cle])
                else:
                    res[cle] = []
                    res[cle].append(tempo[cle])
        else:
            print("should not be here, pb in classification content")
    else:
        resultat = dict()
        for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
# if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
# for cle in res[0].keys():
##                    resu[cle] = []
# for dic in res:
# for cle in dic.keys():
# resu[cle].append(dic[cle])
# for cle in resu.keys():
# if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res


def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """
    import matplotlib
    import numpy as np
    if type(cmap) == str:
        cmap = matplotlib.colors.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki])
                      for i in range(N + 1)]
    # Return colormap object.

    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)


def FormateGephi(chaine):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase."""
    #mem = chaine
    chaine = str(chaine)
    assert(isinstance(chaine, str))

    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = FormateGephi(ch)
                res.append(temp)
            return res
        else:
            chaine = chaine.title()
            chaine = chaine.replace(' ', '', chaine.count(' '))
            try:
                chaine = chaine.decode('latin1')
                chaine = chaine.encode('utf8')
                return chaine
            except:
                try:
                    chaine = chaine.decode('cp1252')
                    chaine = chaine.encode('utf8')
                    return chaine
                except:
                    # print "unicode problem in formate"
                    #                print chaine
                    pass
            if chaine.count('[') > 0:
                return chaine.split('[')[0]
            else:
                return chaine
    else:
        return ''


def Formate(chaine, pays):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase.
        Vire le pays le cas échéant"""
    #mem = chaine
    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = Formate(ch, pays)
                res.append(temp)
            return res
#        elif len(pays) >0:
#            if chaine.count(' '+pays) >0 or chaine.count('[pays]') >0:
#                temp = chaine.replace(pays, '')
#                if temp.count('[]') >0:
#                    temp = temp.replace('[]', '')
#                chaine = temp.strip()
#        chaine = chaine.lower()
#        chaine = chaine.encode('utf8')
#        chaine = chaine.title()
#        chaine = chaine.replace(' ', '', chaine.count(' '))
#        chaine = chaine.replace(u'\xe2\x80\x82', '', chaine.count(u'\xe2\x80\x82'))
#        chaine = chaine.replace(u'\xe2', '', chaine.count(u'\xe2'))
#        chaine = chaine.replace(u'\x80', '', chaine.count(u'\x80'))
#        chaine = chaine.replace(u'\x82', '', chaine.count(u'\x82'))
#        chaine = chaine.replace(u'\xe9', '', chaine.count(u'\xe9'))
#        chaine = chaine.replace(u'\xd6', '', chaine.count(u'\xd6'))
#        chaine = chaine.replace(u'\xd2', '', chaine.count(u'\xd2'))
#        chaine = chaine.replace(u'\xf6', '', chaine.count(u'\xf6'))
#        chaine = chaine.replace(u'\xfc', '', chaine.count(u'\xfc'))
#        chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
#        chaine = chaine.replace(u'\xe1', '', chaine.count(u'\xe1'))
#        chaine = chaine.replace(u'\xf3', '', chaine.count(u'\xf3'))
#        chaine = chaine.replace(u'\xed', '', chaine.count(u'\xed'))
#        chaine = chaine.replace(u'\xe4', '', chaine.count(u'\xe4'))
#        chaine = chaine.replace(u'\xe7', '', chaine.count(u'\xe7'))
#        chaine = chaine.replace(u'\xfa', '', chaine.count(u'\xfa'))
#        chaine = chaine.replace(u'\xf1', '', chaine.count(u'\xf1'))

        try:
            chaine = chaine.decode('latin1')
            chaine = chaine.encode('utf8')
            return chaine
        except:
            try:
                chaine = chaine.decode('cp1252')
                chaine = chaine.encode('utf8')
                return chaine
            except:
                #                print "unicode problem in formate"
                #                print chaine
                pass
        #chaine = quote(chaine)
    #    table[chaine] = mem
#        import urllib
#        chaine = urllib.quote(chaine.replace(u'\u2002', ''), safe='[]')
        return str(chaine, 'utf8', 'ignore')
    else:
        return ''


def genAppar(lstBrev, p1, p2):
    res = []
#    if p1 != p2:
    if lstBrev is not None:
        if p1 in list(lstBrev[0].keys()) and p2 in list(lstBrev[0].keys()):
            for Brev in lstBrev:
                if Brev[p1] is not None and Brev[p2] is not None:
                    if Brev[p1] != 'N/A' and Brev[p2] != 'N/A':
                        if type(Brev[p1]) == type("") and type(Brev[p2]) == type(""):
                            temp = [Brev[p1], Brev[p2], Brev['date']]
                            res.append(temp)
                        elif type(Brev[p1]) == type("") and type(Brev[p2]) == type([]):
                            for k in Brev[p2]:
                                try:
                                    temp = [Brev[p1], k, Brev['date']]
                                    res.append(temp)
                                except:
                                    try:
                                        temp = [Brev[p1], str(
                                            k, 'cp1252', "replace"), Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [Brev[p1], str(
                                                k, 'latin1', "replace"), Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [Brev[p1], str(
                                                    k, 'utf8', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                print("first unicode exception in genAppar")
                        elif type(Brev[p1]) == type([]) and type(Brev[p2]) == type(""):
                            for k in Brev[p1]:
                                try:
                                    temp = [k, Brev[p2], Brev['date']]
                                    res.append(temp)
                                except:
                                    try:
                                        temp = [str(k, 'utf8', "replace"),
                                                Brev[p2], Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [str(k, 'latin1', "replace"),
                                                    Brev[p2], Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [str(k, 'cp1252', "replace"),
                                                        Brev[p2], Brev['date']]
                                                res.append(temp)
                                            except:
                                                print("unicode exception")

                        else:
                            for k1 in Brev[p1]:
                                cpt = Brev[p1].index(k1)
                                for i in range(cpt, len(Brev[p2])):
                                    # if k1 != Brev[p2][i]:
                                    try:
                                        temp = [k1, Brev[p2][i], Brev['date']]
                                        res.append(temp)
                                    except:  # cases of k1 is unicode and Brev not and vice et versa not TREATEN !!!
                                        try:
                                            temp = [str(k1, 'utf8', "replace"), str(
                                                Brev[p2][i], 'utf8', "replace"), Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [str(k1, 'latin1', "replace"), str(
                                                    Brev[p2][i], 'latin1', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [str(k1, 'cp1252', "replace"), str(
                                                        Brev[p2][i], 'cp1252', "replace"), Brev['date']]
                                                    res.append(temp)
                                                except:
                                                    print("another unicode exception")


#    else:
#        if lstBrev is not None:
#            if p1 in lstBrev[0].keys():
#                for Brev in lstBrev:
#                    if Brev[p1] is not None:
#                        if type(Brev[p1]) == type(u""):
#                            temp = [Brev[p1], Brev[p2], Brev['date']]
#                            res.append(temp)
#                        else:
#                            for k in Brev[p1]:
#                                for k2 in Brev[p1]:
#                                    if k != k2:
#                                        temp = [k, k2, Brev['date']]
#                                        res.append(temp)
    return res


def genAppar2(lstBrev, p1, p2):
    res = []
#    if p1 != p2:
    if lstBrev is not None:
        if p1 in list(lstBrev[0].keys()) and p2 in list(lstBrev[0].keys()):
            for Brev in lstBrev:
                if isinstance(Brev['date'], list):
                    Brev['date'] = Brev['date'][0]
                if isinstance(Brev[p1], str) or isinstance(Brev[p1], str):
                    if isinstance(Brev[p2], str) or isinstance(Brev[p2], str):
                        temp = [Brev[p1], Brev[p2], Brev['date']]
                        res.append(temp)
                    elif isinstance(Brev[p2], list):
                        for prop in Brev[p2]:
                            tempo = [Brev[p1], prop, Brev['date']]
                            res.append(tempo)
                    else:
                        print("I dont know what to do")

                elif isinstance(Brev[p1], list):
                    for prop1 in Brev[p1]:
                        if isinstance(Brev[p2], str) or isinstance(Brev[p2], str):
                            temp = [prop1, Brev[p2], Brev['date']]
                            res.append(temp)
                        elif isinstance(Brev[p2], list):
                            for prop in Brev[p2]:
                                tempo = [prop1, prop, Brev['date']]
                                res.append(tempo)
                        else:
                            print("I dont know what to do, many times")

    return res


def MakePonderateAndProp(pair, Date, propo, pondere, destroy):

    if isinstance(pair[0], list):
        for u in pair[0]:
            propo, pondere, destroy = MakePonderateAndProp(
                (u, pair[1], pair[2]), Date, propo, pondere, destroy)
    elif isinstance(pair[1], list):
        for u in pair[1]:
            propo, pondere, destroy = MakePonderateAndProp(
                (pair[0], u, pair[2]), Date, propo, pondere, destroy)
    elif (Date, pair[0], pair[1]) in list(pondere.keys()):
        pondere[(Date, pair[0], pair[1])] += 1
    elif pair[0] != pair[1]:
        pondere[(Date, pair[0], pair[1])] = 1
        propo[(pair[0], pair[1])] = (Date, pair[2])
    else:
        destroy.append((Date, pair))

    return propo, pondere, destroy


def GenereDateLiens(net):
    DateNoeud = dict()
    for lien in net:
        n1, n2, dat, pipo = lien
        if isinstance(dat, list):
            datum = dat[0]
        else:
            datum = dat
        if isinstance(n1, list) and isinstance(n2, list):
            for kk in n1:
                if kk in DateNoeud and datum not in DateNoeud[kk]:

                    DateNoeud[kk].append(dat)
                elif kk not in DateNoeud:
                    DateNoeud[kk] = [datum]
            for kk in n2:
                if kk in DateNoeud and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif kk not in DateNoeud:
                    DateNoeud[kk] = [datum]

        elif isinstance(n1, list) and not isinstance(n2, list):
            for kk in n1:
                if kk in DateNoeud and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif kk not in DateNoeud:
                    DateNoeud[kk] = [datum]
                if n2 in DateNoeud and datum not in DateNoeud[n2]:
                    DateNoeud[n2].append(dat)
                elif n2 not in DateNoeud:
                    DateNoeud[n2] = [datum]
        elif not isinstance(n1, list) and isinstance(n2, list):
            for kk in n2:
                if kk in DateNoeud and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif kk not in DateNoeud:
                    DateNoeud[kk] = [datum]
                if n1 in DateNoeud and datum not in DateNoeud[n1]:
                    DateNoeud[n1].append(dat)
                elif n1 not in DateNoeud:
                    DateNoeud[n1] = [datum]
        else:
            if n1 in DateNoeud and datum not in DateNoeud[n1]:
                DateNoeud[n1].append(dat)
            elif n1 not in DateNoeud:
                DateNoeud[n1] = [datum]
            if n2 in DateNoeud and datum not in DateNoeud[n2]:
                DateNoeud[n2].append(dat)
            elif n2 not in DateNoeud:
                DateNoeud[n2] = [datum]
    return DateNoeud


def GenereReseaux3(G, ListeNode, PatentList, apparie, dynamic):
    reseau = []

    today = datetime.datetime.now().date().isoformat()
    for appar in list(apparie.keys()):
        tempo = [appar]
        reseautemp = [(u + tempo)
                      for u in genAppar2(PatentList, apparie[appar][0], apparie[appar][1])]
        for k in reseautemp:
            if k not in reseau:
                reseau.append(k)
    Pondere = dict()
    Prop = dict()
    destroy = []
    DateLien = dict()
    # cleaning
    tempo = []
    # should be clean now
#    for pair in reseau:
#
#        if isinstance(pair[0], list):
#            if not isinstance(pair[1], list):
#                for ll in pair[0]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        tempo.append( [ll, pair[1], pair[2]])
#            else:
#                for ll in pair[0]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        for uu in pair[1]:
#                            if uu != 'N/A' and uu != 'UNKNOWN':
#                                tempo.append( [ll, uu, pair[2]])
#        elif isinstance(pair[1], list):
#            for ll in pair[1]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        tempo.append( [pair[0], ll, pair[2]])
#        else:
#            tempo.append(pair)

    # unnesting things
    for pair in reseau:
        for ind in range(len(pair)):
            if isinstance(pair[ind], list):
                if len(pair[ind]) == 1:
                    pair[ind] = pair[ind][0]
                else:
                    # print "paté pair ", pair
                    pass
        try:
            if isinstance(pair[2], list):
                dateUnic = pair[2][0]
                if dateUnic in DateLien:
                    DateLien[dateUnic].append((pair[0], pair[1], pair[3]))
                else:
                    DateLien[dateUnic] = [(pair[0], pair[1], pair[3])]
            else:
                if pair[2] in DateLien:
                    DateLien[pair[2]].append((pair[0], pair[1], pair[3]))
                else:
                    DateLien[pair[2]] = [(pair[0], pair[1], pair[3])]
        except:
            print("why ?")
    lstDate = list(DateLien.keys())
    lstDate.sort()

    cmt = 0
    for Date in lstDate:
        for pair in DateLien[Date]:
            Prop, Pondere, destroy = MakePonderateAndProp(pair, Date, Prop, Pondere, destroy)
        if len(destroy) > 0:
            for uu in destroy:
                try:
                    DateLien[uu[0]].remove(uu[1])
                except:
                    cmt += 1
                    # print uu[1]
    # print "compteur des exceptions = ", cmt
    for k in list(Pondere.keys()):
        source = k[1]
        target = k[2]
        try:
            G.add_edge(ListeNode.index(source), ListeNode.index(
                target), attr_dict={'weight': Pondere[k]})
        except:
            pass
    for ed in G.edges():
        if (ListeNode[ed[0]], ListeNode[ed[1]]) in list(Prop.keys()):
            date = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][0]
            G.edge[ed[0]][ed[1]]['rel'] = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]
            # G.edge[ed[0]][ed[1]] ['time'] = [(1, date.isoformat(), today)] #version simple
            #number = len([u for u in Prop.keys() if u[0] == ListeNode[ed[0]] and u[1] == ListeNode[ed[1]] and Prop[(date, ListeNode[ed[0]], ListeNode[ed[1]])][0] <= date])
            liste = [u for u in list(Prop.keys()) if u[0] == ListeNode[ed[0]]
                     and u[1] == ListeNode[ed[1]]]
            lienExist = [u for u in liste if Prop[u][0] <= date]

            G.edge[ed[0]][ed[1]]['time'] = [(len(lienExist), date, today)]  # version simple
            G.edge[ed[0]][ed[1]]['deb'] = date  # .isoformat()
            G.edge[ed[0]][ed[1]]['fin'] = today
#            # setting time weight attribute for each node
#            #defining existing dates before current edge date
#            datesExists =[u for u in lstDate if u<date]
#            # retreiving node apparition in edges before current date
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] or u[1] == ListeNode[ed[0]] and Prop[u][0] in datesExists]
#
#            #counting those relative to same kind of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]]) +1 #adding 1 for current occur
#            #should be divided by number of relation types in the network ?????
#            # and how compute it here...
#            #setting node time attribute
#            if not G.node[ed[0]].has_key('time'):#source
#                G.node[ed[0]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear,  date.isoformat(), today) not in G.node[ed[0]]['time']:
#                    G.node[ed[0]]['time'].append((numAppear,  date.isoformat(), today))
#            #same process for target node
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[1]] or u[1] == ListeNode[ed[1]] and Prop[u][0] in datesExists]
#
#            #counting those relative to same king of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]])+1 #adding 1 for current occur
# setting node time attribute
#            if not G.node[ed[1]].has_key('time'):#source
#                G.node[ed[1]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear, date.isoformat(), today) not in G.node[ed[1]]['time']:
#                    G.node[ed[1]]['time'].append((numAppear,  date.isoformat(), today))
        else:
            print("this should not append")
        datesExists = [u for u in lstDate if datetime.date(
            int(u.split('-')[0]), int(u.split('-')[1]), int(u.split('-')[2])) < datetime.date.today()]
        lstAppear = [u for u in list(Prop.keys()) if u[0] == ListeNode[ed[0]] or u[1] ==
                     ListeNode[ed[0]] and Prop[u][0] in datesExists]
        G.edge[ed[0]][ed[1]]['NormedWeight'] = float(
            G.edge[ed[0]][ed[1]]['weight'] * 100) / len(lstAppear)

        # updating datetime, endate is the next startdate
#            listDate = []
#            for entry in G.node[ed[0]]['time']:
#                listDate.append(entry[1])
#            if len(listDate) > 1:
#                listDate.sort()
#                tempoRes = []
#                for i in G.node[ed[0]]['time']:
#                    ind = listDate.index(i[1])
#                    if ind + 1 in range(len(listDate)):
#                        tempo = (i[0], i[1], listDate[ind + 1]) #end time is set to next one
#                    else:
#                        tempo = (i[0], i[1], today)
#                    tempoRes.append(tempo)
#                G.node[ed[0]]['time'] = tempoRes

    return G, reseau, Prop


def FindFather(noeud, liste):
    for k in liste:
        if noeud.count(k) > 0:
            return k
    print(noeud)
    return


def GenereListeSansDate(ListeBrevet, prop):
    """renvoie la liste des données associées à la propriété pour la liste de dictionnaires"
    """
    res = []

    for brev in ListeBrevet:
        if type(brev[prop]) == type([]):
            for k in brev[prop]:
                if k not in res:
                    res.append(k)
        elif brev[prop] not in res:
            res.append(brev[prop])
    #res = set([u for u in res])
    return res


def UniClean(ch):

    #    try: # this work in script but not compiled !!!!
    #        string = ch.translate('utf8')
    #        string = string.decode('utf8', 'ignore')
    #        return string
    #    except:
    #        try:
    #            string = ch.translate('latin1')
    #            string = string.decode('utf8', 'ignore')
    #            return string
    #        except:
    if ch is not None:
        if isinstance(ch, list):
            return [UniClean(cont) for cont in ch]
        elif isinstance(ch, list) and len(ch) == 1:
            return [UniClean(ch[0])]
        elif isinstance(ch, str) or isinstance(ch, str):
            # Issue #7 - by cvanderlei in 21-dec-2016
            try:
                string = ch.replace('\xa0', '')
                string = string.replace('\xa1', '')
                string = string.replace('\xa2', '')
                string = string.replace('\xa3', '')
                string = string.replace('\xa4', '')
                string = string.replace('\xa5', '')
                string = string.replace('\xa6', '')
                string = string.replace('\xa7', '')
                string = string.replace('\xa8', '')
                string = string.replace('\xa9', '')
                string = string.replace('\xb0', '')
                string = string.replace('\xb1', '')
                string = string.replace('\xb2', '')
                string = string.replace('\xb3', '')
                string = string.replace('\xb4', '')
                string = string.replace('\xb5', '')
                string = string.replace('\xb6', '')
                string = string.replace('\xb7', '')
                string = string.replace('\xb8', '')
                string = string.replace('\xb9', '')
                string = string.replace('\xc0', '')
                string = string.replace('\xc1', '')
                string = string.replace('\xc2', '')
                string = string.replace('\xc3', '')
                string = string.replace('\xc4', '')
                string = string.replace('\xc5', '')
                string = string.replace('\xc6', '')
                string = string.replace('\xc7', '')
                string = string.replace('\xc8', '')
                string = string.replace('\xc9', '')
                string = string.replace('\xd0', '')
                string = string.replace('\xd1', '')
                string = string.replace('\xd2', '')
                string = string.replace('\xd3', '')
                string = string.replace('\xd4', '')
                string = string.replace('\xd5', '')
                string = string.replace('\xd6', '')
                string = string.replace('\xd7', '')
                string = string.replace('\xd8', '')
                string = string.replace('\xd9', '')
                string = string.replace('\xe0', '')
                string = string.replace('\xe1', '')
                string = string.replace('\xe2', '')
                string = string.replace('\xe3', '')
                string = string.replace('\xe4', '')
                string = string.replace('\xe5', '')
                string = string.replace('\xe6', '')
                string = string.replace('\xe7', '')
                string = string.replace('\xe8', '')
                string = string.replace('\xe9', '')
                string = string.replace('\xf0', '')
                string = string.replace('\xf1', '')
                string = string.replace('\xf2', '')
                string = string.replace('\xf3', '')
                string = string.replace('\xf4', '')
                string = string.replace('\xf5', '')
                string = string.replace('\xf6', '')
                string = string.replace('\xf7', '')
                string = string.replace('\xf8', '')
                string = string.replace('\xf9', '')
                string = string.replace('\xaa', '')
                string = string.replace('\xab', '')
                string = string.replace('\xac', '')
                string = string.replace('\xad', '')
                string = string.replace('\xae', '')
                string = string.replace('\xaf', '')
                string = string.replace('\xba', '')
                string = string.replace('\xbb', '')
                string = string.replace('\xbc', '')
                string = string.replace('\xbd', '')
                string = string.replace('\xbe', '')
                string = string.replace('\xbf', '')
                string = string.replace('\xca', '')
                string = string.replace('\xcb', '')
                string = string.replace('\xcc', '')
                string = string.replace('\xcd', '')
                string = string.replace('\xce', '')
                string = string.replace('\xcf', '')
                string = string.replace('\xda', '')
                string = string.replace('\xdb', '')
                string = string.replace('\xdc', '')
                string = string.replace('\xdd', '')
                string = string.replace('\xde', '')
                string = string.replace('\xdf', '')
                string = string.replace('\xea', '')
                string = string.replace('\xeb', '')
                string = string.replace('\xec', '')
                string = string.replace('\xed', '')
                string = string.replace('\xee', '')
                string = string.replace('\xef', '')
                string = string.replace('\xfa', '')
                string = string.replace('\xfb', '')
                string = string.replace('\xfc', '')
                string = string.replace('\xfd', '')
                string = string.replace('\xfe', '')
                string = string.replace('\xff', '')
            except UnicodeDecodeError:
                string = ch
            return string
        else:
            print("what kind of thing is that ch", ch)
    return 'empty'


def quote(string):
    import urllib.parse, urllib.error

    string = UniClean(string)
    return urllib.parse.quote(string, safe='/\\())')


def Initialize(bool1, bool2):
    if bool1 and bool2:
        return 0
    else:
        return "All"



def decoupParagraphEnPhrases(paragraph):
    """returns the paragraph splited in phrases ignoring specifics titles. To be completed"""
    import re
    finsDePhrase = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  M\.   )    # Don't end sentence on "M."
        (?<!  Mme\.   )    # Don't end sentence on "Mme."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """,
                              re.IGNORECASE | re.VERBOSE)
    listeDePhrases = finsDePhrase.split(paragraph)
    return [ph for ph in listeDePhrases if ph]  # non vides


def Update(dicoUpdated, dico):
    for cle in list(dicoUpdated.keys()):
        if cle in list(dico.keys()):
            if isinstance(dicoUpdated, list):
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
            else:
                dicoUpdated[cle] = [dicoUpdated[cle]]
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
        else:
            pass
    return dicoUpdated


def PreExtractPatentsData(patentBib, client, contentPath):

    if 'exchange-documents' in list(patentBib.keys()):
        if isinstance(patentBib['exchange-documents'], dict):
            # patentBib=patentBib[u'exchange-documents'] génère un merdier inconsistance de données !!!
            return ExtractPatentsData(patentBib, client, contentPath)
        elif isinstance(patentBib['exchange-documents'], list):
            PatList = []
            for patBib in patentBib['exchange-documents']:
                PatList.extend(ExtractPatentsData(patBib, client, contentPath))
            return PatList
    else:
        return ExtractPatentsData(patentBib, client, contentPath)


def ExtractPatentsData(patentBib, client, contentPath):
    from epo_ops.models import Docdb
    from epo_ops.models import Epodoc
    #               hum this is unclear for all situations in OPS... in previous check
    # Gathering citing doc according to this patent
    AbstractsPath = contentPath + '//' + 'FamiliesAbstract'
    BP = []  # the list of families patents
    datEquiv = False  # for equivalents research
    if 'exchange-document' in list(patentBib.keys()) and isinstance(patentBib['exchange-document'], dict):
        tempoPat = ProcessBiblio(patentBib['exchange-document'])
        lstCitants = []
        try:
            # , brevet[u'document-id'][u'kind']['$']))
            tempo3 = ('publication', Epodoc(tempoPat['label']))
            dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
            patentEquiv = dataEquiv.json()
            dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
            tempoPat['equivalents'] = SearchEquiv(dataEquiv)
        except:
            temp = ('publication', Docdb(tempoPat['label'][2:],
                                         tempoPat['label'][0:1], tempoPat['kind']))
            try:
                dataEquiv = client.published_data(*temp, endpoint='equivalents')  # use DbDoc
                patentEquiv = dataEquiv.json()
                dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                tempoPat['equivalents'] = SearchEquiv(dataEquiv)
            except:
                tempoPat['equivalents'] = 'empty'
                # print "no equivalents"
        tempoPat, YetGathered, BP = ExtractPatent(tempoPat, contentPath, [])
        request = 'ct=' + tempoPat['label']

        lstCitants, nbCitants = PatentCitersSearch(client, request)
        if 'publication-reference' in list(patentBib.keys()):
            patents = patentBib['publication-reference']
            if isinstance(patents, list):
                for k in patents:
                    lstCitants.extend(ProcessCitingDoc(k))
            else:  # sometimes its a sole patent
                lstCitants.extend(ProcessCitingDoc(patents))
        

        tempoPat['CitedBy'] = list(set(lstCitants))
        tempoPat['Citations'] = len(list(set(lstCitants)))
        MakeIram(tempoPat, tempoPat['label'], patentBib, AbstractsPath)
        return tempoPat

    elif 'exchange-document' in list(patentBib.keys()) and isinstance(patentBib['exchange-document'], list):
        for patent in patentBib['exchange-document']:
            patentList = []
            tempoPat = ProcessBiblio(patent)

            if tempoPat is not None:
                try:
                    # , brevet[u'document-id'][u'kind']['$']))
                    tempo3 = ('publication', Epodoc(tempoPat['label']))

                    dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                    datEquiv = True
                except:
                    try:
                        # , brevet[u'document-id'][u'kind']['$']))
                        tempo3 = ('publication', Docdb(
                            tempoPat['label'][2:]), tempoPat['country'][0], tempoPat['kind'])

                        dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                    except:
                        print("no equivalents...")
                if datEquiv:
                    patentEquiv = dataEquiv.json()
                    dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                    tempoPat['equivalents'] = SearchEquiv(dataEquiv)
                else:
                    tempoPat['equivalents'] = 'empty'
                tempoPat, YetGathered, BP = ExtractPatent(tempoPat, contentPath, BP)
                MakeIram(tempoPat, tempoPat['label'], patentBib, AbstractsPath)
                request = 'ct=' + tempoPat['label']

                lstCitants, nbCitants = PatentCitersSearch(client, request)

                tempoPat['CitedBy'] = lstCitants
                tempoPat['Citations'] = nbCitants
                patentList.append(tempoPat)
        return patentList
    else:
       # print "application found, At this time P2N do not handle it"
        return None
#    else: #list of patents but at upper level GRRRR
#        for patents in patentBib[u'ops:world-patent-data'][u'exchange-documents']:
#            tempoPat = ProcessBiblio(patents[u'exchange-document'])
#            #if None not in tempo.values():
#
#            if tempoPat is not None:
#                try:
#                    tempo3 = ('publication', Epodoc(tempoPat['label']))#, brevet[u'document-id'][u'kind']['$']))
#                    dataEquiv = client.published_data(*tempo3, endpoint = 'equivalents')
#                    datEquiv = True
#                except:
#                    try:
#                        tempo3 = ('publication', Docdb(tempoPat['label'][2:]), tempoPat['country'][0], tempoPat['kind'])#, brevet[u'document-id'][u'kind']['$']))
#                        dataEquiv = client.published_data(*tempo3, endpoint = 'equivalents')
#                    except:
#                        print "no equivalents..."
#                if datEquiv:
#                    patentEquiv = dataEquiv.json()
#                    dataEquiv = patentEquiv[u'ops:world-patent-data'][u'ops:equivalents-inquiry'][ u'ops:inquiry-result']
#                    tempoPat['equivalents'] = SearchEquiv(dataEquiv)
#                else:
#                    tempoPat['equivalents'] = 'empty'
#                tempoPat, YetGathered, BP = ExtractPatent(tempoPat, ContentsPath, BP)
#                request = 'ct='+ tempoPat['label']
#                lstCitants, nbCitants = PatentCitersSearch(client, request)
#                tempoPat['CitedBy'] = lstCitants
#                tempoPat['Citations'] = nbCitants
#                return BP
#            else:
#                return []


def GatherPatentsData(brevet, client, ContentsPath, AbstractsPath, PatIgnored, BP):
    from epo_ops.models import Docdb
    from epo_ops.models import Epodoc
    temp = ('publication', Docdb(brevet['document-id']['doc-number']['$'],
                                 brevet['document-id']['country']['$'], brevet['document-id']['kind']['$']))
    # , brevet[u'document-id'][u'kind']['$']))
    temp2 = ('publication', Epodoc(brevet['document-id']['country']
                                   ['$'] + brevet['document-id']['doc-number']['$']))
    # nameOfPatent for file system save (abstract, claims...)
    ndb = brevet['document-id']['country']['$'] + brevet['document-id']['doc-number']['$']

    try:  # trying Epodoc first, unused due to response format (multi document instead of one only)
        data = client.published_data(*temp2, endpoint='biblio')
        patentBib = data.json()
        try:
            data2 = client.published_data(*temp, endpoint='biblio')
            patentBibtemp = data.json()
            patentBibtemp2 = data2.json()
             # terrible approx here... quantity of data is better !!!!
            if len(str(patentBibtemp)) > len(str(patentBibtemp2)):
                patentBib = patentBibtemp                          # should check instead the presence of all fields of data
            else:
                patentBib = patentBibtemp2
        except:
            #print('noDocDb')
            patentBib = data.json()
    except:
        try:
            data = client.published_data(*temp, endpoint='biblio')
            patentBib = data.json()
        except:
            #print('patent ignored ', ndb)
            AnnonceLog(Appli = 'p2n_gather_biblio', texte= "Patent label ignored " +ndb)
            PatIgnored += 1
            return None
    # the next line generates an error when debugging line by line (Celso)
    if data.ok:
        #               hum this is unclear for all situations in OPS... in previous check
        # Gathering citing doc according to this patent

        datEquiv = False  # for equivalents research
        if isinstance(patentBib['ops:world-patent-data']['exchange-documents'], dict):
            if isinstance(patentBib['ops:world-patent-data']['exchange-documents']['exchange-document'], dict):
                tempoPat = ProcessBiblio(
                    patentBib['ops:world-patent-data']['exchange-documents']['exchange-document'])
                try:
                    # , brevet[u'document-id'][u'kind']['$']))
                    tempo3 = ('publication', Epodoc(tempoPat['label']))
                    dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                    patentEquiv = dataEquiv.json()
                    dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                    tempoPat['equivalents'] = SearchEquiv(dataEquiv)
                except:

                    try:
                        dataEquiv = client.published_data(
                            *temp, endpoint='equivalents')  # use DbDoc
                        patentEquiv = dataEquiv.json()
                        dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                        tempoPat['equivalents'] = SearchEquiv(dataEquiv)
                    except:
                        tempoPat['equivalents'] = 'empty'
                        #print("no equivalents")
                tempoPat, YetGathered, BP = ExtractPatent(tempoPat, ContentsPath, BP)
                request = 'ct=' + brevet['document-id']['country']['$'] + \
                    brevet['document-id']['doc-number']['$']

                lstCitants, nbCitants = PatentCitersSearch(client, request)
                tempoPat['CitedBy'] = lstCitants
                tempoPat['Citations'] = nbCitants
                #store the abstract in IramuTeq format
                MakeIram(tempoPat, ndb, patentBib, AbstractsPath)
                BP[len(BP) - 1] = tempoPat
                return BP

            elif isinstance(patentBib['ops:world-patent-data']['exchange-documents']['exchange-document'], list):
                for patent in patentBib['ops:world-patent-data']['exchange-documents']['exchange-document']:
                    tempoPat = ProcessBiblio(patent)

                    if tempoPat is not None:
                        try:
                            # , brevet[u'document-id'][u'kind']['$']))
                            tempo3 = ('publication', Epodoc(tempoPat['label']))

                            dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                            datEquiv = True
                        except:
                            try:
                                # , brevet[u'document-id'][u'kind']['$']))
                                tempo3 = ('publication', Docdb(
                                    tempoPat['label'][2:]), tempoPat['country'][0], tempoPat['kind'])

                                dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                            except:
                                pass
                                #print("no equivalents...")
                        if datEquiv:
                            patentEquiv = dataEquiv.json()
                            dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                            tempoPat['equivalents'] = SearchEquiv(dataEquiv)
                        else:
                            tempoPat['equivalents'] = 'empty'
                        tempoPat, YetGathered, BP = ExtractPatent(tempoPat, ContentsPath, BP)
                        MakeIram(tempoPat, ndb, patentBib, AbstractsPath)
                        request = 'ct=' + tempoPat['label']

                        lstCitants, nbCitants = PatentCitersSearch(client, request)

                        tempoPat['CitedBy'] = lstCitants
                        tempoPat['Citations'] = nbCitants
                        BP[len(BP) - 1] = tempoPat
                        return BP

        else:  # list of patents but at upper level GRRRR
            for patents in patentBib['ops:world-patent-data']['exchange-documents']:
                tempoPat = ProcessBiblio(patents['exchange-document'])
                # if None not in tempo.values():

                if tempoPat is not None:
                    try:
                        # , brevet[u'document-id'][u'kind']['$']))
                        tempo3 = ('publication', Epodoc(tempoPat['label']))
                        dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                        datEquiv = True
                    except:
                        try:
                            # , brevet[u'document-id'][u'kind']['$']))
                            tempo3 = ('publication', Docdb(
                                tempoPat['label'][2:]), tempoPat['country'][0], tempoPat['kind'])
                            dataEquiv = client.published_data(*tempo3, endpoint='equivalents')
                        except:
                            pass
                            #print("no equivalents...")
                    if datEquiv:
                        patentEquiv = dataEquiv.json()
                        dataEquiv = patentEquiv['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']
                        tempoPat['equivalents'] = SearchEquiv(dataEquiv)
                    else:
                        tempoPat['equivalents'] = 'empty'
                    tempoPat, YetGathered, BP = ExtractPatent(tempoPat, ContentsPath, BP)
                    request = 'ct=' + tempoPat['label']
                    lstCitants, nbCitants = PatentCitersSearch(client, request)
                    tempoPat['CitedBy'] = lstCitants
                    tempoPat['Citations'] = nbCitants
                    BP[len(BP) - 1] = tempoPat
                    return BP
                else:
                    return


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input


def LoadBiblioFile(rep, name):
    # new       12/12/05
    import pickle
    # name=name.title()  #change here in pre version 4. No title case
    DataBrevets = dict()
    DataBrevets['brevets'] = []
    if "Description" + name in os.listdir(rep):
        with open(rep + '//Description' + name, 'rb') as fic:
            Descript = pickle.load(fic, encoding='utf-8')
            DataBrevets['ficBrevets'] = Descript['ficBrevets']
            DataBrevets['requete'] = Descript['requete']
    else:
        DataBrevets['ficBrevets']  =""
        DataBrevets['requete'] = ""  # may be a pass is enought
    with open(rep + '//' + name, 'rb') as fic:
        while 1:
            try:
                DataBrevets['brevets'].append(pickle.load(fic))
            except EOFError:
                break
    return DataBrevets


def ExtractPatent(pat, ResultContentsPath, BiblioPatents):
    DejaLa = [bre['label'] for bre in BiblioPatents]

    if None not in list(pat.values()):
        # if Brev['label'] == Brev["prior"]: # just using primary patents not all the family
        if isinstance(pat['classification'], list):
            for classif in pat['classification']:
                tempo2 = ExtractClassificationSimple2(classif)
                for cle in list(tempo2.keys()):
                    if cle in list(pat.keys()) and tempo2[cle] not in pat[cle]:
                        if pat[cle] == '':
                            pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    else:
                        pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    if pat[cle].count(',') > 0:
                        print(pat[cle])  # hum, strage state
        else:
            tempo2 = ExtractClassificationSimple2(pat['classification'])
            for cle in list(tempo2.keys()):
                if cle in list(pat.keys()) and tempo2[cle] not in pat[cle]:
                    if pat[cle] == '':
                        pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                else:
                    pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                if pat[cle].count(',') > 0:
                    print(pat[cle])  # hum, strage state

                    #                print classif
        pat = SeparateCountryField(pat)
#        for clekey in pat.keys():
#            if isinstance(pat[clekey], list):
#                pat[clekey] = UnNest(pat[clekey])

        if pat['label'] in DejaLa:  # checking multiples status
            tempor = [patent for patent in BiblioPatents if patent['label']
                      == pat["label"]][0]  # should be unique
            BiblioPatents.remove(tempor)
            tempor = Update(tempor, pat)
#                for key in tempor.keys():
#                    if isinstance(tempor[key], list):
#                        tempor[key] = UnNest(tempor[key])
#                tempor = CleanPatent(tempor)
            BiblioPatents.append(tempor)  # CleanPatent( suppressed here V.2

        else:
            #            for key in pat.keys():
            #                if isinstance(pat[key], list):
            #                    pat[key] =  UnNest(pat[key])
            #pat = CleanPatent(pat)
            BiblioPatents.append(pat)
            DejaLa.append(pat['label'])
        return pat, DejaLa, BiblioPatents
    else:  # None values avoiding this patent
        print("None value for patent", pat['label'])
        print("consider revising")
        if 'label' in pat:
            DejaLa.append(pat['label'])
        return None, DejaLa, BiblioPatents


def RetrouveLangue(liste, patentBib):
    dico = dict()
    compt = 0
    langue = 'en'  # by default
    while compt < len(liste):
        if liste[compt].count('@lang') > 0:
            langue = ExtraitContenuDict(patentBib, liste[compt].split('****'))
            dico[langue] = []
            compt += 1
        else:
            dico[langue].append(ExtraitContenuDict(patentBib, liste[compt].split('****')))
            compt += 1
    return dico


def MakeIram(patent, FileName, patentBibData, AbstractPath):
    if isinstance(patent['IPCR1'], list):
        CIB1 = '-'.join(dat for dat in patent['IPCR1'])
    else:
        CIB1 = patent['IPCR1']
    if isinstance(patent['IPCR3'], list):
        CIB3 = '-'.join(dat for dat in patent['IPCR3'])
    else:
        CIB3 = patent['IPCR3']
    if isinstance(patent['IPCR4'], list):
        CIB4 = '-'.join(dat for dat in patent['IPCR4'])
    else:
        CIB4 = patent['IPCR4']
 # Issue #6 - by cvanderlei in 21-dec-2016
    if 'year' in patent:
        if isinstance(patent['year'], list):
            Year = patent['year'][0]
        else:
            Year = patent['year']
    else:
        Year = 'empty'
    kindIra = patent['kind']
    invCountIra = '-'.join(dat for dat in patent['Inventor-Country'])
    appCountIra = '-'.join(dat for dat in patent['Applicant-Country'])

    IRAM = '**** *Label_' + FileName + ' *Country_' + patent['country'][0] + ' *CIB3_' + CIB3 + ' *CIB1_' + CIB1 + \
        ' *CIB4_' + CIB4 + ' *Date_' + str(Year) + ' *Applicant_' + \
        UniClean('-'.join(coupeEnMots(patent['applicant'])))[0:12]
    IRAM = IRAM + ' *Kind_' + kindIra + ' *InventCountry_' + \
        invCountIra + ' *ApplCountry_' + appCountIra + ' '
    IRAM = IRAM.replace('_ ', '_empty ', IRAM.count('_ ')) + '\n'
    TXT = dict()
    # hack for compatibility when calling this function from familly gathering
    if 'ops:world-patent-data' not in list(patentBibData.keys()):
        patentBibData['ops:world-patent-data'] = dict()
        patentBibData['ops:world-patent-data']['exchange-documents'] = dict()
        patentBibData['ops:world-patent-data']['exchange-documents']['exchange-document'] = patentBibData['exchange-document']
    if isinstance(patentBibData['ops:world-patent-data']['exchange-documents']['exchange-document'], list):
        for tempo in patentBibData['ops:world-patent-data']['exchange-documents']['exchange-document']:
            if 'abstract' in tempo:
                txtTemp = ExtractAbstract(tempo['abstract'])
                for cleLang in txtTemp:
                    if cleLang in TXT:
                        TXT[cleLang] += txtTemp[cleLang]
                    else:
                        TXT[cleLang] = txtTemp[cleLang]

    else:
        if 'abstract' in patentBibData['ops:world-patent-data']['exchange-documents']['exchange-document']:
            TXT = ExtractAbstract(patentBibData['ops:world-patent-data']
                                  ['exchange-documents']['exchange-document']['abstract'])
            for lang in list(TXT.keys()):
                EcritContenu(IRAM + TXT[lang], AbstractPath + '//' + lang + '-' + FileName + '.txt')
    return


def MakeIram2(patent, FileName, patentBibData, SavePath, contenu):
    contenu = contenu.lower()
    if isinstance(patent['IPCR1'], list):
        CIB1 = '-'.join(dat for dat in patent['IPCR1'])
    else:
        CIB1 = patent['IPCR1']

    if isinstance(patent['IPCR3'], list):
        CIB3 = '-'.join(dat for dat in patent['IPCR3'])
    else:
        CIB3 = patent['IPCR3']
    if isinstance(patent['IPCR4'], list):
        CIB4 = '-'.join(dat for dat in patent['IPCR4'])
    else:
        CIB4 = patent['IPCR4']
 # Issue #6 - by cvanderlei in 21-dec-2016
    if 'year' in patent:
        if isinstance(patent['year'], list):
            Year = patent['year'][0]
        else:
            Year = patent['year']
    else:
        Year = 'empty'

    if isinstance(patent['kind'], list):
        kindIra = '-'.join(dat for dat in patent['kind'])
    else:
        kindIra = patent['kind']

    invCountIra = '-'.join(dat for dat in patent['Inventor-Country'])
    appCountIra = '-'.join(dat for dat in patent['Applicant-Country'])

    IRAM = '**** *Label_' + FileName + ' *Country_' + patent['country'][0] + ' *CIB3_' + CIB3 + ' *CIB1_' + CIB1 + \
        ' *CIB4_' + CIB4 + ' *Date_' + str(Year) + ' *Applicant_' + \
        UniClean('-'.join(coupeEnMots(patent['applicant'])))[0:12]
    IRAM = IRAM + ' *Kind_' + kindIra + ' *InventCountry_' + \
        invCountIra + ' *ApplCountry_' + appCountIra + ' '

    IRAM = IRAM.replace('_ ', '_empty ', IRAM.count('_ ')) + '\n'
    Contenu = flatten_dict(patentBibData)
    CleList = [cle for cle in list(Contenu.keys()) if cle.lower().count(contenu) > 0]
    CleList = [cle for cle in CleList if contenu in cle.split('****')]
#                        resu = ExtraitContenuDict(patentCont, temp)
    TXT = RetrouveLangue(CleList, patentBibData)
    
    for lang in list(TXT.keys()):
        # Issue #6 - by cvanderlei in 6-jan-2017
        try:
            EcritContenu(IRAM + '\n'.join(TXT[lang]), SavePath + lang + '-' + FileName)
        except UnicodeDecodeError:
            print ('Error unicode when writing patent file', patent)
            pass
#        if len(TXT.keys())>0:
#            nb = 1
#        else:
#            nb = 0
    return list(TXT.keys())
def MakeIram3(patent, FileName, patentBibData, SavePath, contenu):
    #30/04 adding the return of obstract content in dict form
    contenu = contenu.lower()
    if isinstance(patent['IPCR1'], list):
        CIB1 = '-'.join(dat for dat in patent['IPCR1'])
    else:
        CIB1 = patent['IPCR1']

    if isinstance(patent['IPCR3'], list):
        CIB3 = '-'.join(dat for dat in patent['IPCR3'])
    else:
        CIB3 = patent['IPCR3']
    if isinstance(patent['IPCR4'], list):
        CIB4 = '-'.join(dat for dat in patent['IPCR4'])
    else:
        CIB4 = patent['IPCR4']
 # Issue #6 - by cvanderlei in 21-dec-2016
    if 'year' in patent:
        if isinstance(patent['year'], list):
            Year = patent['year'][0]
        else:
            Year = patent['year']
    else:
        Year = 'empty'

    if isinstance(patent['kind'], list):
        kindIra = '-'.join(dat for dat in patent['kind'])
    else:
        kindIra = patent['kind']

    invCountIra = '-'.join(dat for dat in patent['Inventor-Country'])
    appCountIra = '-'.join(dat for dat in patent['Applicant-Country'])

    IRAM = '**** *Label_' + FileName + ' *Country_' + patent['country'][0] + ' *CIB3_' + CIB3 + ' *CIB1_' + CIB1 + \
        ' *CIB4_' + CIB4 + ' *Date_' + str(Year) + ' *Applicant_' + \
        UniClean('-'.join(coupeEnMots(patent['applicant'])))[0:12]
    IRAM = IRAM + ' *Kind_' + kindIra + ' *InventCountry_' + \
        invCountIra + ' *ApplCountry_' + appCountIra + ' '

    IRAM = IRAM.replace('_ ', '_empty ', IRAM.count('_ ')) + '\n'
    Contenu = flatten_dict(patentBibData)
    CleList = [cle for cle in list(Contenu.keys()) if cle.lower().count(contenu) > 0]
    CleList = [cle for cle in CleList if contenu in cle.split('****')]
#                        resu = ExtraitContenuDict(patentCont, temp)
    TXT = RetrouveLangue(CleList, patentBibData)
    
    for lang in list(TXT.keys()):
        # Issue #6 - by cvanderlei in 6-jan-2017
        try:
            
            EcritContenu(IRAM + '\n'.join(TXT[lang]), SavePath + lang + '-' + FileName)
        except UnicodeDecodeError:
            print ('Error unicode when writing patent file', patent)
            pass
#        if len(TXT.keys())>0:
#            nb = 1
#        else:
#            nb = 0
    return TXT


def MakeIram4(patent,  patentBibData, contenu):
    #30/04 adding the return of obstract content in dict form
    #no saving data step... used by acad
    contenu = contenu.lower()
    if isinstance(patent['IPCR1'], list):
        CIB1 = '-'.join(dat for dat in patent['IPCR1'])
    else:
        CIB1 = patent['IPCR1']

    if isinstance(patent['IPCR3'], list):
        CIB3 = '-'.join(dat for dat in patent['IPCR3'])
    else:
        CIB3 = patent['IPCR3']
    if isinstance(patent['IPCR4'], list):
        CIB4 = '-'.join(dat for dat in patent['IPCR4'])
    else:
        CIB4 = patent['IPCR4']
 # Issue #6 - by cvanderlei in 21-dec-2016
    if 'year' in patent:
        if isinstance(patent['year'], list):
            Year = patent['year'][0]
        else:
            Year = patent['year']
    else:
        Year = 'empty'

    if isinstance(patent['kind'], list):
        kindIra = '-'.join(dat for dat in patent['kind'])
    else:
        kindIra = patent['kind']

    invCountIra = '-'.join(dat for dat in patent['Inventor-Country'])
    appCountIra = '-'.join(dat for dat in patent['Applicant-Country'])

    IRAM = '**** *Label_' + patent['label'] + ' *Country_' + patent['country'][0] + ' *CIB3_' + CIB3 + ' *CIB1_' + CIB1 + \
        ' *CIB4_' + CIB4 + ' *Date_' + str(Year) + ' *Applicant_' + \
        UniClean('-'.join(coupeEnMots(patent['applicant'])))[0:12]
    IRAM = IRAM + ' *Kind_' + kindIra + ' *InventCountry_' + \
        invCountIra + ' *ApplCountry_' + appCountIra + ' '

    IRAM = IRAM.replace('_ ', '_empty ', IRAM.count('_ ')) + '\n'
    Contenu = flatten_dict(patentBibData)
    CleList = [cle for cle in list(Contenu.keys()) if cle.lower().count(contenu) > 0]
    CleList = [cle for cle in CleList if contenu in cle.split('****')]
#                        resu = ExtraitContenuDict(patentCont, temp)
    TXT = RetrouveLangue(CleList, patentBibData)
    
#        if len(TXT.keys())>0:
#            nb = 1
#        else:
#            nb = 0
    return TXT

def GetFamilly(client, brev, rep):
    #from OPS2NetUtils2 import ExtractClassificationSimple2, SeparateCountryField, ExtractAbstract, UniClean
    from epo_ops.models import Epodoc, Docdb
    import datetime
    ResultContentsPath = rep
    lstres = []
    comptExcept = 0

#    try:
#        url ='http://ops.epo.org/3.1/rest-services/family/publication/docdb/' +brev['label'] +'/biblio'
#data6 = client.family(reference_type='publication', input=Epodoc(brev['label']), constituents=['biblio'])
#    data.request.url data.request.body
#        data = requests.get(url, headers = headers)
    dico = None
    try:
        data = client.family('publication', Epodoc(brev['label']), 'biblio')
        data = data.json()
        dico = data['ops:world-patent-data']['ops:patent-family']['ops:family-member']
        #PatentDataFam[brev['label']] = dict()
        if isinstance(dico, dict):  # type(dico) == type(dict()):
            dico = [dico]
        cpt = 1
    except:
        try:
            data = client.family('publication', Docdb(
                brev['label'][2:], brev['label'][0:2], brev['kind']))
            data = data.json()
            dico = data['ops:world-patent-data']['ops:patent-family']['ops:family-member']
            #PatentDataFam[brev['label']] = dict()
            if isinstance(dico, dict):  # type(dico) == type(dict()):
                dico = [dico]
            cpt = 1
        except:
            # IF WE ARE HERE? i SUPPOSE THAT EQUIVALENTS PATENTS SHOULD BE CHECKED
            # found error on ops client... try to bypass by direct access
            import requests
            from requests.structures import CaseInsensitiveDict
            url = "http://ops.epo.org/3.2/rest-services/family/publication/docdb/" + label
            headers = CaseInsensitiveDict()
            # headers["Accept"] = "application/json"
            headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
            if not client.access_token.is_expired:
                headers["Authorization"] = "Bearer " + client.access_token.token  #
            else:
                client = epo_ops.Client(key, secret)
                client.accept_type = 'application/json'
                headers["Authorization"] = "Bearer " + client.access_token.token
            headers['Content-Type'] = 'text/plain;charset=utf-8'
            try:
                data = requests.get(url, headers=headers)
            except:
                url = "http://ops.epo.org/3.2/rest-services/family/publication/epodoc/" + label
                try:
                    data = requests.get(url, headers=headers)
                except:
                    print("Not Found ", label)
                    dico = None
            try:
                data = data.json()
            except:
                data = xmltodict.parse(data.text)
            dico = data['ops:world-patent-data']['ops:patent-family']['ops:family-member']


    if dico is not None:

        for donnee in dico:
            Go = True
#            Brevet=dict(dict(dict(dict())))
#            Brevet[u'ops:world-patent-data'] =dict()
#            Brevet[u'ops:world-patent-data']['ops:biblio-search'] =dict()
#            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] =dict()
#            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = donnee #hum no sure that it is a good way
#            PatentData = dict()
#            Req = Brevet
            PatentData = PreExtractPatentsData(donnee, client, rep)
            if PatentData is not None:
                PatentData['references'] = len(PatentData['CitP']) + len(PatentData['CitO'])
#               try:
#                    if u'references-cited' in donnee[u'exchange-document'][u'bibliographic-data'].keys():
#                        if "citation"  in donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'].keys():
#                            PatentData[u'references'] = len(donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'][u'citation'])
#                    else:
#                        PatentData[u'references'] = 0
#                except:
#                    PatentData[u'references'] = 0

                # it is may be an Application patent. Hence, no CIB, no citation... so I should avoid it
    #                        print " *********************************   "

                # if cpt == 1:#not the first one !!!!
                try:
                    if isinstance(donnee['priority-claim'], dict):
                        if donnee['priority-claim']['priority-active-indicator']['$'] == 'YES':
                            PatentData['priority-active-indicator'] = 1
                    else:
                        for don in donnee['priority-claim']:
                            if don['priority-active-indicator']['$'] == 'YES':
                                PatentData['priority-active-indicator'] += 1
                except:
                    PatentData['priority-active-indicator'] = 0
                    # should check what is "active indicator" for patent
                try:
                    if donnee['application-reference']['@is-representative'] == 'YES':
                        PatentData['representative'] = 1
    #                            PatentData['representative'] = True
                except:
                    PatentData['representative'] = 0
                    # should check what is reprensentativeness for patent :-/

                PatentData['family lenght'] = len(dico)
# Issue #6 - by cvanderlei in 21-dec-2016
                if 'dateDate' in PatentData and 'date' in PatentData:
                    if not isinstance(PatentData['dateDate'], datetime.date) and PatentData['date'] is not None:
                        PatentData['dateDate'] = datetime.date(int(PatentData['dateDate'].split('-')[0]),
                                                               int(PatentData['dateDate'].split(
                                                                   '-')[1]),
                                                               int(PatentData['dateDate'].split('-')[2]))

#            for cle in PatentData.keys():
#                if isinstance(PatentData[cle], list):
#                    if len(PatentData[cle]) == 1:
#                        PatentData[cle] == PatentData[cle][0] #UnNesting
#            if None not in PatentData.values():
#                IRAM = '**** *Label_' + PatentData[u'label'] +' *Country_'+PatentData[u'country']+ ' *CIB3_'+'-'.join(PatentData[u'IPCR3']) + ' *CIB1_'+'-'.join(PatentData[u'IPCR1']) + ' *CIB4_'+'-'.join(PatentData[u'IPCR4']) + ' *Date_' + str(PatentData[u'dateDate'].year) + ' *Applicant_'+'-'.join(coupeEnMots(str(PatentData[u'applicant'])))
#                TXT=dict()
#                if isinstance(donnee[u'exchange-document'], list):
#                    for tempo in donnee[u'exchange-document']:
#                        if tempo.has_key('abstract'):
#                            txtTemp = ExtractAbstract(tempo['abstract'])
#                            for cleLang in txtTemp:
#                                if TXT.has_key(cleLang):
#                                    TXT[cleLang] += txtTemp[cleLang]
#                                else:
#                                    TXT[cleLang] = txtTemp[cleLang]
#                else:
#                  if donnee[u'exchange-document'].has_key('abstract'):
#                      TXT = ExtractAbstract(donnee[u'exchange-document'][u'abstract'])
#                for lang in TXT.keys():
#                    EcritContenu(IRAM + ' *Contenu_Abstract \n' + TXT[lang], ResultContentsPath+'//FamiliesAbstracts//'+lang+'-'+PatentData['label']+'.txt')
#
                lstres.append(PatentData)
                cpt += 1
            else:
                pass
#            else:
# print "hum... missing values... avoiding this patent"
#                #print "Cleaning data"
#                for key in PatentData.keys():
#                    if isinstance(PatentData[key], list):
#                        if len(PatentData[key])==1:
#                            PatentData[key] = PatentData[key][0]
#                    elif isinstance(PatentData[key], unicode):
#                        pass
#                    elif isinstance(PatentData[key], unicode):
#                        PatentData[key] = unicode(PatentData[key])
#                    else:
#                        PatentData[key] = u''

        datemin = datetime.date(3000, 1, 1)
        # hum retrieving the first patent of the family.... This hack is confusing. Info should be in EPO data...
        for brevet in lstres:
            # Issue #6 - by cvanderlei in 30-dec-2016
            if 'representative' in brevet and 'dateDate' in brevet:
                if brevet['dateDate'] < datemin:
                    datemin = brevet['dateDate']
                    prior = brevet['label']
            else:
                print("hum... no representative... unconsistent data")
        if 'prior' not in locals():
            prior = brev['label']
        for brevet in lstres:
            brevet['prior'] = prior
    return lstres #why do I have to add that here ? 30/06/2019 ????? it seemed to work before
#        print "exceptions ", comptExcept
#        print len(lstres), ' patents added'

# def RecupAbstract(dico):
#    res = dict()
#    if u'@lang' in dico.keys():
#        if dico[u'@lang'].count(u'fr')>0:
#            res[u'resume'] = dico[u'p']
#        else:
#            res[u'abstract'] = dico[u'p']
#        return res
#    else:
#        res['abs'] = dico[u'p']
#        return res
    # elif u'abstract' in str(dico):
    #   print "where is the key? \n", dico


def EcritContenu(contenu, fic):
    with open(fic, 'wb') as ficW:
        ficW.write(contenu.encode('utf8'))
        return 'OK'


def MakeText(Thing):
    res = ''
    if isinstance(Thing, list):
        for thing in Thing:
            res += MakeText(thing)
    elif isinstance(Thing, dict):
        if '$' in list(Thing.keys()):
            if isinstance(Thing['$'], str) or isinstance(Thing['$'], str):
                return Thing['$'] + '\n'
            elif isinstance(Thing['$'], list):
                for thing in Thing['$']:
                    res += MakeText(thing) + '\n'
            else:
                print("I don't know what to do")

        if 'p' in list(Thing.keys()):
            if isinstance(Thing['p'], str) or isinstance(Thing['p'], str):
                return Thing['p']
            elif isinstance(Thing['p'], list):
                for thing in Thing['p']:
                    res += MakeText(thing)
            else:
                print("I don't know what to do")

        elif 'claims' in str(thing):
            try:
                res = MakeText(Thing['claims']['claim']['claim-text'])
            except:
                print(list(Thing.keys()))
        else:
            print("what else ?")
    else:
        print("I don't know what to do")
    return res
    #not fun


def ExtractPubliRefs(OpsRes):
    if isinstance(OpsRes, list):
        return [ExtractPubliRefs(cont) for cont in OpsRes]
    elif isinstance(OpsRes, dict):
        if 'document-id' in list(OpsRes.keys()):
            return ExtractPubliRefs(OpsRes['document-id'])
        else:
            if OpsRes['@document-id-type'] == 'epodoc':
                return OpsRes['doc-number']['$']
            else:
                country = OpsRes['country']['$']
                number = OpsRes['doc-number']['$']
                return country + number
    return None


def ProcessCitingDoc(opsRes):
    if len(opsRes) > 1:
        if opsRes['document-id']['@document-id-type'] == 'docdb':
            country = opsRes['document-id']['country']['$']
            # opsRes[u'document-id'][u'kind']['$']
            number = opsRes['document-id']['doc-number']['$']
        elif opsRes['document-id']['@document-id-type'] == 'epodoc':
            country = opsRes['document-id']['country']['$']
            number = opsRes['document-id']['doc-number']['$']
        return [country + number]
    else:
        return ''


def PatentCitersSearch(client, requete, deb=1, fin=1):
    requete = requete.replace('/', '\\')
    Brevets = []
    nbTrouv = 0
    try:
        data = client.published_data_search(requete, deb, fin)
        if data and data.ok:
            STOP = False
            cpt = 0
            data = data.json()
            nbTrouv = int(data['ops:world-patent-data']['ops:biblio-search']['@total-result-count'])
            if nbTrouv > 0:
                while len(Brevets) < nbTrouv and not STOP:
                    data = client.published_data_search(
                        requete, deb + cpt * 25, fin + (cpt + 1) * 25)
                    cpt += 1
                    data = data.json()
                    patents = data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['ops:publication-reference']
                    if isinstance(patents, list):
                        for k in patents:
                            Brevets.extend(ProcessCitingDoc(k))
                    else:  # sometimes its a sole patent
                        Brevets.extend(ProcessCitingDoc(patents))
                        STOP = True
        else:
            print("request not correct, cql language only")
            return None
    except:
        print("citations not found for", requete)
    return Brevets, nbTrouv


def PatentSearch(client, requete, deb=1, fin=1):
    # requete = requete.replace('/', '\\') #hum changed here for IPC search...
    # dont know repercutions... 15/09/2015
    data = client.published_data_search(requete, deb, fin)
    Brevets = []

    if data.ok:
        data = data.json()
        nbTrouv = int(data['ops:world-patent-data']['ops:biblio-search']['@total-result-count'])
        if nbTrouv > 0:
            patents = data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['ops:publication-reference']
            if isinstance(patents, list):
                for k in patents:
                    if k not in Brevets:
                        Brevets.append(k)

            else:  # sometimes its a sole patent
                if patents not in Brevets:
                    Brevets.append(patents)
    else:
        print("no result")
        Brevets = []
        # return None
    return Brevets, nbTrouv


def NiceName(content):
    assert isinstance(content, list)
    ContentNice = [FormateGephi(toto).strip() for toto in content]
#    if isinstance(content, list):
#
#    elif isinstance(content, unicode): # we should never enter here
#        print "content is not a list"
#        ContentNice = FormateGephi(content)
#                #applicant[Brev['applicant']] = FormateGephi(memo)
#    else:
#        ContentNice = u''
    return ContentNice


def UrlIPCRBuild(ipc):
    # if not isinstance(ipc, list):
    #     IPCR = [IPCR]
    try:
        url = ['https://www.wipo.int/classifications/ipc/ipcpub/?notion=scheme&version='+
               SchemeVersion + '&symbol=' + symbole(ipc) + 
        '&menulang=en&lang=en&viewmode=f&fipcpc=no&showdeleted=yes&indexes=no&headings=yes&notes=yes&direction=o2n&initial='+ ipc[0]+'&cwid=none&tree=no&searchmode=smart']
    except:
        url = ['empty']
    return url


def UrlInventorBuild(inventor):
    if not isinstance(inventor, list):
        if inventor.count(' ') == 0:
            inventor = [ComputeTempoNom(inventor)]
        else:
            inventor = [inventor]

    try:
        url = ['http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN=' +
               quote('"' + tempoNom.split('[')[0].strip() + '"') + '&locale=en_EP&DB=EPODOC' for tempoNom in inventor]
    except:
        url = ['empty']
    return url


def UrlApplicantBuild(applicant):
    if not isinstance(applicant, list):
        if not applicant.count(" ") == 0:
            applicant = [applicant]
        else:
            applicant = [ComputeTempoNom(applicant)]
    try:
        url = ['http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN=' +
               quote('"' + tempoNom.split('[')[0].strip() + '"') + '&locale=en_EP&DB=EPODOC' for tempoNom in applicant]
    except:
        url = ['empty']
    return url


def UrlPatent(patLabel):
    if isinstance(patLabel, list):
        url = ["http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query=" +
               pat + "&locale=en_EP&DB=EPODOC" for pat in patLabel]
    else:
        url = ["http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query=" +
               patLabel + "&locale=en_EP&DB=EPODOC"]
    return url


def formateDate(dat):
    return dat[0:4] + '-' + dat[4:6] + '-' + dat[6:8]


def ProcessBiblio(pat):
    PatentData = dict()

    if "priority-claims" in list(pat['bibliographic-data'].keys()):
        PriorDate = ExtractPriorDate(pat)
        if isinstance(PriorDate, list) and len(PriorDate) > 0:
            PatentData['prior-Date'] = [formateDate(dates) for dates in PriorDate]
            PatentData['prior-dateDate'] = [datetime.date(
                int(dat[0:4]), int(dat[4:6]), int(dat[6:8])) for dat in PriorDate]
        else:
            PatentData['prior-Date'] = []
            PatentData['prior-dateDate'] = []
    else:
        PatentData['prior-Date'] = []
        PatentData['prior-dateDate'] = []
    if "country" in list(pat.keys()):
        PatentData['label'] = pat["country"]['$'] + pat['doc-number']['$']
    else:
        PatentData['label'] = pat['@country'] + pat['@doc-number']
    try:
        PatentData['inventor'] = UniClean(ExtraitParties(pat, 'inventor', 'epodoc'))

    except:
        PatentData['inventor'] = ['empty']
    try:
        if isinstance(PatentData['inventor'], str):
            PatentData['inventor'] = [PatentData['inventor']]
        PatentData['inventor-nice'] = NiceName(PatentData['inventor'])
    except:
        PatentData['inventor-nice'] = ['empty']
    try:
        PatentData['applicant'] = UniClean(ExtraitParties(pat, 'applicant', 'epodoc'))
        if isinstance(PatentData['applicant'], str):
            PatentData['applicant'] = [PatentData['applicant']]

    except:
        PatentData['applicant'] = ['empty']
    try:

        PatentData['applicant-nice'] = NiceName(PatentData['applicant'])
    except:
        PatentData['applicant-nice'] = ['empty']
    try:
        PatentData['title'] = UniClean(ExtraitTitleEn(pat))
    except:
        PatentData['title'] = 'empty'
    try:
        PatentData['country'] = ExtraitCountry(pat)
    except:
        PatentData['country'] = ['empty']
    try:
        PatentData['kind'] = ExtraitKind(pat)
    except:
        PatentData['kind'] = ['empty']
    date = ExtractionDate(pat)

    try:
        PatentData['classification'] = UnNest2List(ExtraitIPCR2(pat))
    except:
        PatentData['classification'] = ''
    if 'bibliographic-data' in list(pat.keys()):
        if 'references-cited' in list(pat['bibliographic-data'].keys()):
            PatentData['CitO'] = []  # Externatl/Other citations by The patent
            PatentData['CitP'] = []  # Patent citations by THe Patent
            if 'citation' in list(pat['bibliographic-data']['references-cited'].keys()):

                if isinstance(pat['bibliographic-data']['references-cited']['citation'], list):
                    # is-citing

                    for cit in pat['bibliographic-data']['references-cited']['citation']:
                        if 'patcit' in list(cit.keys()):
                            # patent ref
                            # Issue #6 - by cvanderlei in 6-jan-2017
                            if 'document-id' in cit['patcit']:
                                if isinstance(cit['patcit']['document-id'], list):
                                    # patents citations of patents
                                    PatentData['CitP'].append(
                                        cit['patcit']['document-id'][0]['doc-number']['$'])
                                else:
                                    # this may mix Epodoc numbers and docDb
                                    PatentData['CitP'].append(
                                        cit['patcit']['document-id']['doc-number']['$'])
                        if 'nplcit' in list(cit.keys()):
                            # external ref
                            if isinstance(cit['nplcit'], list):
                                for ref in cit['nplcit']:
                                    PatentData['CitO'].append(ref['text']['$'])

                        if len(set(cit.keys()) - {'@cited-phase', 'patcit', '@sequence', '@office', '@cited-by', 'category', 'nplcit'}) > 0:
                            print()
                else:
                    if 'patcit' in list(pat['bibliographic-data']['references-cited']['citation'].keys()):
                        # Issue #6 - by cvanderlei in 6-jan-2017
                        if 'document-id' in pat['bibliographic-data']['references-cited']['citation']['patcit']:
                            if isinstance(pat['bibliographic-data']['references-cited']['citation']['patcit']['document-id'], list):
                                PatentData['CitP'] = [pat['bibliographic-data']['references-cited']
                                                       ['citation']['patcit']['document-id'][0]['doc-number']['$']]
                            else:  # this may mix Epodoc numbers and docDb
                                PatentData['CitP'] = [pat['bibliographic-data']['references-cited']
                                                       ['citation']['patcit']['document-id']['doc-number']['$']]

                    elif 'nplcit' in list(pat['bibliographic-data']['references-cited']['citation'].keys()):
                        # "extern refs"
                        PatentData['CitO'].append(
                            pat['bibliographic-data']['references-cited']['citation']['nplcit']['text']['$'])
                    if len(set(pat['bibliographic-data']['references-cited']['citation'].keys()) - {'@cited-phase', '@office', 'patcit', 'category', '@sequence', '@cited-by', 'nplcit'}) > 0:
                        print()

            if len(set(pat['bibliographic-data']['references-cited'].keys()) - {'citation'}) > 0:
                print()

        else:
            pass
    try:
        PatentData['CPC'] = ExtractCPC(pat)
    except:
        PatentData['CPC'] = ['']

    if 'CitP' not in list(PatentData.keys()):  # arbitrary, what about other cases, we are here for consistency between families and normal cases
        try:
            PatentData['CitP'], PatentData['CitO'] = ExtractReference(pat)
        except:
            PatentData['CitP'], PatentData['CitO'] = [[], []]
    PatentData['references'] = len(PatentData['CitP']) + len(PatentData['CitO'])
    try:
        if pat['priority-claim']['priority-active-indicator']['$'] == 'YES':
            PatentData['priority-active-indicator'] = 1
    except:
        PatentData['priority-active-indicator'] = 0
        pass  # should check what is "active indicator" for patent
    try:
        if pat['bibliographic-data']['application-reference']['@is-representative'] == 'YES':
            PatentData['representative'] = 1
#                            PatentData['representative'] = True

    except:
        try:
            # epodoc, docdb, original... if one is missing, biais
            PatentData['application-ref'] = len(pat['bibliographic-data']
                                                 ['application-reference']['document-id']) / 3.0
        except:
            PatentData['application-ref'] = 0  # no application
        PatentData['representative'] = 0
    try:
        PatentData['publication-ref'] = pat['bibliographic-data']['publication-reference']
    except:
        PatentData['publication-ref'] = 0

    # doing some cleaning
        # transforming dates string in dates
    if date is not None and date != '':  # THE PUBLICATION DATEs
        if isinstance(date, list):
            for dates in date:
                PatentData['dateDate'] = datetime.date(
                    int(dates[0:4]), int(dates[4:6]), int(dates[6:]))
                PatentData['date'] = [str(dates[0:4]) + '-' +
                                       str(dates[4:6]) + '-' + str(dates[6:])]
                PatentData['year'] = [str(dates[0:4])]
        else:
            print("should not append")
#        print "patent date", PatentData['date']
    elif date == []:
        tempodate = datetime.date(datetime.date.today().year + 2, 1, 1)  # adding two year arbitrary
        PatentData['dateDate'] = [tempodate]
        PatentData['date'] = [str(tempodate.year) + '-' +
                               str(tempodate.month) + '-' + str(tempodate.day)]
    else:
        print("no date")

        # cleaning classsications
    # unesting everything
#    for cle in PatentData.keys():
#        if isinstance(PatentData[cle], list):
#            PatentData[cle] = UnNest2List(PatentData[cle])
    PatentData.pop('publication-ref')
    return PatentData


def SearchEquiv(data):

    if data != "":
        temporar = ExtractEquiv(data)
        if isinstance(temporar, list):
            return temporar
        else:
            return [temporar]
    else:
        return []

#
# def Clean(truc):
#    if type(truc) == type(u''):
#        temp = truc.translate('utf8')
#        return  [temp]
#    if isinstance(truc, list):
#        if len(truc)>1:
#            return [Clean(u) for u in truc]
#        else:
#            return Clean(truc[0])
#    else:
#        return truc    # no changes
#


def ExtractPriorDate(Brev):
    # this extract the priority date as done in previous version... (again)
    # this time added the fact that dates can be lists... depending on steps documents
    ResDate = []

    if 'bibliographic-data' in list(Brev.keys()):
        if 'priority-claims' in list(Brev['bibliographic-data'].keys()):
            if 'priority-claim' in list(Brev['bibliographic-data']['priority-claims'].keys()):
                if isinstance(Brev['bibliographic-data']['priority-claims']['priority-claim'], list):

                    for tempo in Brev['bibliographic-data']['priority-claims']['priority-claim']:
                        if isinstance(tempo['document-id'], list):
                            for content in tempo['document-id']:
                                if 'date' in list(content.keys()):
                                    ResDate.append(content['date']['$'])
                                else:
                                    pass
                        elif 'date' in list(tempo['document-id'].keys()):
                            ResDate.append(tempo['document-id']['date']['$'])
                        else:
                            pass
                elif isinstance(Brev['bibliographic-data']['priority-claims']
                                ['priority-claim']['document-id'], list):
                    for content in Brev['bibliographic-data']['priority-claims']['priority-claim']['document-id']:
                        if 'date' in list(content.keys()):
                            ResDate.append(content['date']['$'])
                        else:
                            pass
                else:
                    try:
                        ResDate.append(Brev['bibliographic-data']['priority-claims']
                                       ['priority-claim']['document-id']['date']['$'])
                    except:
                        print("***********PRIORITY date problem*************************")
                        print(Brev['bibliographic-data']['priority-claims']['priority-claim'])
                        print("************************************")

    return ResDate


def ExtractionDate(Brev):
    # this extract the publication date not the priority date as done in previous version...
    ResDate = []
    if 'bibliographic-data' in list(Brev.keys()):
        if 'publication-reference' in list(Brev['bibliographic-data'].keys()):
            if 'document-id' in list(Brev['bibliographic-data']['publication-reference'].keys()):
                tempo = Brev['bibliographic-data']['publication-reference']['document-id']
                if isinstance(tempo, dict):
                    if 'date' in list(tempo.keys()):
                        return [tempo['date']['$']]
                    else:
                        #                        print "bad date", tempo
                        return []
                elif isinstance(tempo, list):
                    for content in tempo:
                        if 'date' in list(content.keys()):
                            ResDate.append(content['date']['$'])
                        else:
                            #                        print "bad date", tempo
                            pass
                    return ResDate  # first on should be good

                # again retrocompatibility


def ExtraitKind(Brev):
    if '@kind' in list(Brev.keys()):
        return Brev['@kind']
    else:  # retro ompatibility
        try:
            return Brev['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['@kind']
        except:
            #            print 'something bad, Kind'
            return None


def ExtraitTitleEn(Brev):
    if 'bibliographic-data' in list(Brev.keys()):
        if isinstance(Brev['bibliographic-data']['invention-title'], dict):
            return Brev['bibliographic-data']['invention-title']['$']
        else:  # list are use for multilanguage title support
            # just taking the first one
            return Brev['bibliographic-data']['invention-title'][0]['$']
    else:  # retro ompatibility
        try:
            return Brev['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title'][0]['$']
        except:
            try:
                return Brev['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title']['$']
            except:
                #                print 'something bad, title'
                return None


def ExtraitCountry(Brev):
    if '@country' in list(Brev.keys()):
        return [Brev['@country']]
    else:  # again retrocompatibility
        try:
            return [Brev['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['@country']]
        except:
            #            print 'something bad, country'
            return None


def AlphaTest(chain):
    for let in chain:
        if let.isdigit():
            return False
    return True
#


def UnNest2List(thing):
    CoolType = [str, str, int, float]
    if type(thing) in CoolType:
        return thing
    else:
        res = []
        for tt in thing:
            if type(tt) in CoolType:
                res.append(tt)
            else:
                for k in tt:
                    tempo = UnNest2List(k)
                    if type(tempo) in CoolType:
                        if tempo not in res:
                            res.append(tempo)
                    else:
                        for ttt in tempo:
                            res.append(UnNest2List(ttt))
        return res


def ExtraitClassification(DicoOuLst):
    if type(DicoOuLst) == type(dict()):
        temp = DicoOuLst['section']['$'] + DicoOuLst['class']['$'] + DicoOuLst['subclass']['$'] + \
            DicoOuLst['main-group']['$'] + '/' + DicoOuLst['subgroup']['$'] + \
            ' ' + DicoOuLst['classification-value']['$']
        return temp
    else:
        res = []
        for Dico in DicoOuLst:
            temp = Dico['section']['$'] + Dico['class']['$'] + Dico['subclass']['$'] + \
                Dico['main-group']['$'] + '/' + Dico['subgroup']['$'] + \
                ' ' + Dico['classification-value']['$']
#    section, class, subclass, main-group / subgroup Classif value
            res.append(temp)
    return res


def ExtraitIPCR2(Brevet):
    res = []
    if 'bibliographic-data' in list(Brevet.keys()):
        if 'classifications-ipcr' in list(Brevet['bibliographic-data'].keys()):
            if 'classification-ipcr' in list(Brevet['bibliographic-data']['classifications-ipcr'].keys()):
                tempo = Brevet['bibliographic-data']['classifications-ipcr']['classification-ipcr']
                if isinstance(tempo, dict):
                    if "text" in list(tempo.keys()):
                        classTemp = tempo['text']['$'].replace(' ', '')
                        if AlphaTest(classTemp[len(classTemp) - 2:len(classTemp)]):
                            res.append(classTemp[:len(classTemp) - 2])
                        else:
                            res.append(classTemp)
                for classif in tempo:
                    if isinstance(classif, dict):
                        if "text" in list(classif.keys()):
                            classTemp = classif['text']['$'].replace(' ', '')
                            if AlphaTest(classTemp[len(classTemp) - 2:len(classTemp)]):
                                res.append(classTemp[:len(classTemp) - 2])
                            else:
                                res.append(classTemp)

                return res
        elif 'classification-ipc' in list(Brevet['bibliographic-data'].keys()):
            if 'text' in list(Brevet['bibliographic-data']['classification-ipc'].keys()):
                res.append(Brevet['bibliographic-data']['classification-ipc']['text']['$'])
                return res
        else:
            return None

    else:  # retrocomp
        try:
            Brev = Brevet['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'][
                'exchange-document']['bibliographic-data']['classifications-ipcr']['classification-ipcr']
        except:
            #            print 'something bad, IPCR'
            try:
                return ExtraitClassification(Brevet['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['bibliographic-data']['patent-classifications']['patent-classification'])
            except:
                return None
        if type(Brev) == type(list()):
            for clas in Brev:
                res.append(clas['text']['$'])
            return res
        else:
            return Brev['text']['$']


def ExtraitParties(Brev, content, Format):
    res = []
    if 'bibliographic-data' in list(Brev.keys()):
        Brev = Brev['bibliographic-data']['parties']
    else:  # for retrocompatibility, should be cleaned
        try:
            Brev = Brev['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document']['bibliographic-data']['parties']
        except:
            return None
    if content + 's' in Brev:
        for truc in Brev[content + 's'][content]:
            if truc['@data-format'] == Format:
                res.append(truc[content + '-name']['name']['$'].replace('\\u2002', ' '))
    else:
        return None
    if isinstance(res, list):
        return res
    else:
        return [res]


def NomBrevet(Brev):
    """extracts the invention title of a patent bibliographic data"""
    try:
        if 'ops:world-patent-data' in Brev:
            Brev = Brev['ops:world-patent-data']
            if 'exchange-documents' in Brev:
                Brev = Brev['exchange-documents']
                if 'exchange-document' in Brev:
                    Brev = Brev['exchange-document']
                    if 'bibliographic-data' in Brev:
                        Brev = Brev['bibliographic-data']
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
        if 'invention-title' in Brev:
            if type(Brev['invention-title']) == type(''):
                return Brev['invention-title']
            elif type(Brev['invention-title']) == type(dict()):
                if '$' in Brev['invention-title']:
                    return Brev['invention-title']['$']
            else:
                titre = []
                for tit in Brev['invention-title']:
                    if '$' in tit:
                        titre.append(tit['$'])
                return titre
        else:
            return None
    except:
        return None


def wo(CollectName, GlobalPath, WindowOpenFlag=True):
    def window_open(url):
        url = url.replace('*CollectName*', CollectName)
        has_path = os.path.exists(os.path.join(GlobalPath, CollectName, url))
        # print 'URL', url, GlobalPath, has_path
        if has_path:
            full_url = '%s/%s' % (CollectName, url)
            if WindowOpenFlag:
                return "window.open('%s', '_blank');" % full_url
            else:
                return full_url
        # print('404 file, skipping url for ', url)
        return ""
    return window_open

def direct(CollectName, GlobalPath, WindowOpenFlag=True):
    def window_open(url):
        url = url.replace('*CollectName*', CollectName)
        has_path = os.path.exists(os.path.join(GlobalPath, CollectName, url))
        # print 'URL', url, GlobalPath, has_path
        if has_path:
            full_url = '%s' % (CollectName, url)
            if WindowOpenFlag:
                return "window.open('%s', '_blank');" % full_url
            else:
                return full_url
        # print('404 file, skipping url for ', url)
        return ""
    return window_open


def u(CollectName, GlobalPath):
    return wo(CollectName, GlobalPath, WindowOpenFlag=False)


def RenderTemplate(name, dest, **context):
    handler = codecs.open(dest, 'w', 'utf8')
    env = Environment(loader=FileSystemLoader('templates'))
    if ('CollectName' in context):
        env.globals['wo'] = wo(context['CollectName'], context['GlobalPath'])
        env.globals['u'] = u(context['CollectName'], context['GlobalPath'])
        env.globals['direct'] = direct(context['CollectName'], context['GlobalPath'])
    handler.write(env.get_template(name).render(**context))
    handler.close()

#############
# tests unitaires
##################
# print ExtractClassification('C10B 01/123')

#DureeBrevet = 20
#SchemeVersion = '20140101'
#
#ListeBrevet = []
#import datetime, os
#today = datetime.datetime.now().date().isoformat()
#dateMini = today
#dateMax = datetime.datetime(1700, 1, 1).isoformat()
#import networkx as nx
#G = nx.DiGraph()
#ResultPath = 'BiblioPatents'
#ResultGephiPath = 'GephiFiles'
#
#Brev = dict()
#
#Brev ["pays"] = u"fr"
#Brev["inventor"] = [u"Me", u"My colleague"]
#Brev["applicant"]= [u'Universite de Toulon']
#Brev["classification"] = u'C101/24A1'
#Brev ["label"] = u'3209934'
#Brev ["date"] = datetime.date(2014,01, 01)
#
#
# if type(Brev['classification']) == type ([]):
#            temp = dict()
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                temp[key] = []
#            for classif in Brev['classification']:
#                temp['classification'].append(classif.replace(' ', '', classif.count(' ')))
#                temp['IPCR1'].append(classif[0])
#                if len(classif) > 2:
#                    temp['IPCR3'].append(unicode(classif[0:2]))
#                else:
#                    temp['IPCR3'].append('')
#                if len(classif) > 4:
#                    temp['IPCR4'].append(unicode(classif[0:3]))
#                else:
#                    temp['IPCR4'].append('')
#                if classif.count('/') > 0:
#                    temp['IPCR7'].append(unicode(classif.split('/')[0]))
#                else:
#                    temp['IPCR7'].append('')
#                temp['IPCR11'].append(unicode(classif[0:len(classif)-2]))
#
#                temp['status'].append(unicode(classif[len(classif)-1]))
#                if temp['status'] not in Status:
#                     temp['status']=unicode(classif[len(Brev['classification'])-2])
#                     if temp['status'] not in Status:
#                         temp['status'] = 'N/A'
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                if type(temp[key]) == type([]):
#                    Brev[key] = list(set(temp[key]))
#                else:
#                    Brev[key] = temp[key]
#
# elif Brev['classification'] is not None:
#            Brev['classification'] = Brev['classification'].replace(' ', '', Brev['classification'].count(' '))
#
#            Brev['IPCR1']=(Brev['classification'][0])
#            if len(Brev['classification']) > 2:
#                Brev['IPCR3']=(Brev['classification'][0:3])
#            else:
#                Brev['IPCR3'] = ''
#            if len(Brev['classification']) > 4:
#                Brev['IPCR4']=(Brev['classification'][0:4])
#            else:
#                Brev['IPCR4'] = ''
#            if Brev['classification'].count('/') >0:
#                Brev['IPCR7']=(Brev['classification'].split('/')[0])
#            else:
#                Brev['IPCR7'] = ''
#            Brev['IPCR11']=(Brev['classification'][0:len(Brev['classification'])-2])
#            Brev['status']=(Brev['classification'][len(Brev['classification'])-1:])
#            if Brev['status'] not in Status:
#                 Brev['status']=(Brev['classification'][len(Brev['classification'])-2])
#                 if Brev['status'] not in Status:
#                     Brev['status'] = 'N/A'
#
# else:
#            for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                Brev[ipc] = 'N/A'
#
# ListeBrevet.append(Brev)
# print
#Pays = set([(u) for u in GenereListeSansDate(ListeBrevet, 'pays')])
#Inventeurs = set([(u) for u in GenereListeSansDate(ListeBrevet, 'inventor')])
#LabelBrevet = set([(u) for u in GenereListeSansDate(ListeBrevet, 'label')])
#Applicant = set([(u) for u in GenereListeSansDate(ListeBrevet, 'applicant')])
#Classification = set([(u) for u in GenereListeSansDate(ListeBrevet, 'classification')])
#IPCR1 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR1')])
#IPCR3 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR3')])
#IPCR4 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR4')])
#IPCR7 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR7')])
#IPCR11 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR11')])
#status = set([(u) for u in GenereListeSansDate(ListeBrevet, 'status')])
#listelistes = []
# listelistes.append(list(Pays))
# listelistes.append(list(Inventeurs))
# listelistes.append(list(LabelBrevet))
# listelistes.append(list(Applicant))
# listelistes.append(Classification)
# listelistes.append(list(IPCR1))
# listelistes.append(list(IPCR3))
# listelistes.append(list(IPCR4))
# listelistes.append(list(IPCR7))
# listelistes.append(list(IPCR11))
# listelistes.append(list(status))
#
#ListeNoeuds =[]
# for liste in listelistes:
#        ListeNoeuds += [u for u in liste if u not in ListeNoeuds]
# try:
#    ListeNoeuds.remove('N/A')
# except:
#    pass
#
#
#
#appariement = dict()
# print listelistes
#lstCrit= ['inventor', 'label', 'applicant', 'pays', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']
# for i in lstCrit:
#        for j in lstCrit:
#
#            appariement[change(i)+'-'+change(j)] = [i,j]
#
# for Brev in ListeBrevet:
#        if 'date' not in Brev.keys():
#            print Brev
#            Brev['date'] = datetime.date(3000, 1, 1)
#
#G, reseau = GenereReseaux3(G, ListeNoeuds, ListeBrevet, appariement, True)
#
#DateNoeud = dict()
# for lien in reseau:
#        n1, n2, dat, pipo = lien
#        if DateNoeud.has_key(n1):
#            DateNoeud[n1].append(dat)
#        else:
#            DateNoeud[n1] = [dat]
#        if DateNoeud.has_key(n2):
#            DateNoeud[n2].append(dat)
#        else:
#            DateNoeud[n2] = [dat]
#
# print
#attr = dict()
#liendureseau = [(u, v) for u,v,b ,z in reseau]
#LinkedNodes = []
# for k in liendureseau:
#    LinkedNodes.append(k[0])
#    LinkedNodes.append(k[1])
#
# for noeud in ListeNoeuds:
#
#    if noeud is not None:
#        if noeud in Pays:
#            attr['label'] = 'pays'
#            attr['url'] = ''
# elif noeud in Classification:
##                attr['label'] = 'IPCR'
# if noeud.count('/') > 0:
##                    ind = noeud[4:].index('/')
##                    mask = 4 - ind
##                    mask2 = len(noeud[5+ind:len(noeud)-2])
##
# attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]+str(0)*mask+noeud[4:4+ind]+noeud[5+ind:len(noeud)-2]+'000' + (3-mask2)*str('0')
# else:
# attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]
#        elif noeud in Inventeurs:
#
#            attr['label'] = 'Inventeur'
#            attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+quote(noeud)+'&locale=en_EP&DB=EPODOC'
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=IN:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=38&viewOption=All'
#        elif noeud in LabelBrevet:
#            attr['label'] = 'Brevet'
#            attr['Class'] = getClassif(noeud, ListeBrevet)
#            if attr['Class'] is not None:
#                attr['ReductedClass'] = getClassif(noeud, ListeBrevet)[0:4]
#                tempotemp = "http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+noeud+"&locale=en_EP&DB=EPODOC"
#
#                attr['url'] = tempotemp
#            else:
#                attr['ReductedClass'] = ""
#        elif noeud in Applicant:
#            attr['label'] = 'Applicant'
#            attr['url'] ='http://worldwide.espacenet.com/searchResuldengue-grupos.jsonts?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote(noeud)
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=PA:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=123897&viewOption=All'
#        elif noeud in IPCR1:
#            if noeud in IPCRCodes.keys():
#                attr['label'] = 'IPCR1'
#                attr['name'] = IPCRCodes[noeud]
#                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#            else:
#                pass #node is may be a status node
#        elif noeud in IPCR7:
#            attr['label'] = 'IPCR7'
#            attr['url'] =  'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#
#        elif noeud in IPCR3:
#            attr['label'] = 'IPCR3'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#        elif noeud in IPCR4:
#            attr['label'] = 'IPCR4'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#
#        elif noeud in IPCR11:
#            attr['label'] = 'IPCR11'
#            attr['url'] = ''
#        elif noeud in status:
#            attr['label'] = 'status'
#
#        if noeud in ListeNoeuds:
#            G.add_node(ListeNoeuds.index(noeud))
#
#            G.node[ListeNoeuds.index(noeud)]['label'] = noeud
#
#            G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
#            G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
#            G.node[ListeNoeuds.index(noeud)]['weight'] = LinkedNodes.count(noeud)
#            G.node[ListeNoeuds.index(noeud)]['start'] = min(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            G.node[ListeNoeuds.index(noeud)]['end'] = max(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            if dateMini > G.node[ListeNoeuds.index(noeud)]['start']:
#                dateMini = G.node[ListeNoeuds.index(noeud)]['start']
#            if dateMax < G.node[ListeNoeuds.index(noeud)]['end']:
#                dateMax = G.node[ListeNoeuds.index(noeud)]['end']
#
#            if len(G.node[ListeNoeuds.index(noeud)]['time']) >1:
#                lst = [u[1] for u in G.node[ListeNoeuds.index(noeud)]['time']]
#                lst.sort()
#                lsttemp = []
#                cpt=0
#                for kk in range(len(lst)):
#                    for nb in range(len(G.node[ListeNoeuds.index(noeud)]['time'])):
#                        if G.node[ListeNoeuds.index(noeud)]['time'][nb][1] == lst[kk]:
#                            if G.node[ListeNoeuds.index(noeud)]['time'][nb] not in lsttemp:
#                                if cpt>0:
#
#                                    lsttemp[cpt-1] = (lsttemp[cpt-1][0], lsttemp[cpt-1][1], G.node[ListeNoeuds.index(noeud)]['time'][nb][1] )#enddate is startdate of current datetime
#                                lsttemp.append(G.node[ListeNoeuds.index(noeud)]['time'][nb])
#                                cpt+=1
#                G.node[ListeNoeuds.index(noeud)]['time'] = lsttemp
#            G.node[ListeNoeuds.index(noeud)]['deb'] = G.node[ListeNoeuds.index(noeud)]['start']
#            G.node[ListeNoeuds.index(noeud)]['fin']= dateMax#G.node[ListeNoeuds.index(noeud)]['end']
#            G.node[ListeNoeuds.index(noeud)]['val'] = sum([u[0] for u in G.node[ListeNoeuds.index(noeud)]['time']])
#            del(G.node[ListeNoeuds.index(noeud)]['end'])
#            del(G.node[ListeNoeuds.index(noeud)]['start'])
#            del(G.node[ListeNoeuds.index(noeud)]['weight'])
#            if noeud not in IPCR1:
#                pass
#            else:
#                G.node[ListeNoeuds.index(noeud)]['label'] = noeud + '-' +attr['name']
#        else:
#            print "on devrait pas être là, never", noeud
#            #G.node[ListeNoeuds.index(noeud)]['end'] = ExtraitMinDate(G.node[ListeNoeuds.index(noeud)]) + DureeBrevet
#            #G.node[ListeNoeuds.index(noeud)]['start'] =
#        G.graph['defaultedgetype'] = "directed"
#        G.graph['timeformat'] = "date"
#        G.graph['mode'] = "dynamic"
#        G.graph['start'] = dateMini
#        G.graph['end'] = dateMax
#
#
#ndf = 'test'
#nx.write_gexf(G, ResultGephiPath+'\\'+ndf + ".gexf", version='1.2draft')
#fic = open(ResultGephiPath+'\\'+ndf+'.gexf', 'r')
##
# Next is a hack to correct the bad writing of the header of the gexf file
# with dynamics properties
#fictemp=open(ResultGephiPath+'\\'+"Good"+ndf+'.gexf', 'w')
# fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
#  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
#<attributes class="edge" mode="static">
#  <attribute id="6" title="deb" type="string" />
#  <attribute id="7" title="fin" type="string" />
#  <attribute id="8" title="rel" type="string" />
#    </attributes>
#    <attributes class="edge" mode="dynamic">
#  <attribute id="9" title="time" type="integer" />
#</attributes>
#<attributes class="node" mode="static">
#  <attribute id="0" title="category" type="string" />
#  <attribute id="1" title="val" type="integer" />
#  <attribute id="3" title="url" type="string" />
#  <attribute id="4" title="deb" type="string" />
#  <attribute id="5" title="fin" type="string" />
#</attributes>
#    <attributes class="node" mode="dynamic">
#        <attribute id="2" title="time" type="integer" />
#    </attributes>
#""")
#ecrit  =False
# for lig in fic.readlines():
#    if lig.count('<nodes>'):
#        ecrit = True
#    if ecrit:
#        fictemp.write(lig)
# fictemp.close()
# fic.close()
# os.remove(ResultGephiPath+'\\'+ndf+'.gexf')
#
#os.rename(ResultGephiPath+'\\'+"Good"+ndf+'.gexf', ResultGephiPath+'\\'+ndf+'.gexf')
# print "Network file writen in ",  ResultGephiPath+' directory.\n See file: '+ndf + ".gexf"
