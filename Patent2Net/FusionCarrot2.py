# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 07:53:30 2014

@author: dreymond
"""
import os
import codecs
import cPickle
import bs4
from xml.sax.saxutils import escape

from P2N_Lib import LoadBiblioFile
from P2N_Config import LoadConfig

configFile = LoadConfig()
requete = configFile.requete
IsEnableScript = configFile.FusionCarrot2
GatherFamilly = configFile.GatherFamilly

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
    print cpt, " Abstracts files Names normalized"


def coupeEnMots(texte):
    "renvoie une liste de mots propres des signes de ponctuation et autres cochonneries"
    texte= texte.lower()
    import re
    res = re.sub('['+"[]?!"+']', ' ', texte) # on vire la ponctuation
    res = re.sub('\d', ' ', res) # extraction des chiffres #numeric are avoided
    res = re.findall('\w+', res, re.UNICODE) # extraction des lettres seulement #only letters, no symbols
    return res

def LectureFichier2(fic):
    """read the file, and return purged from coupeEnMots content if lenght is greater thar arbitrary value, here 5"""
    """cleans also Iramuteq Variables"""
    with codecs.open(fic, "r", 'utf8') as fichier:
#            import bs4 as bs
#            bs.UnicodeDammit.contains_replacement_characters = True

            fi = fichier.readlines()
            #cpt = 0
#            try:
#                fi
#                #tempo = bs.UnicodeDammit.detwingle(fi)
#            except:
#                fi = ""
#                cpt +=1
#                print "loupés ", cpt
#
            meta = ''.join([lig for lig in fi if lig.startswith('****')])
            try:
                for ligne in fi:
                    if not ligne.startswith('****'):
                        try:
                            pipo = ligne.encode('utf8')
                            pipo = pipo.decode('utf8')
                            lect = ''.join(ligne+'\n')
                        except:
                            lect=''
                            pass

            except:
                lect=''
            if len(' '.join(coupeEnMots(lect)))> 5: #arbitrary
                contenu =lect
                return contenu, meta
            else:
                return None, None



def complete3(listeFic, lang, det, Brevets):

    resum = [fi for fi in set(listeFic) if fi.count('//'+det+'//')>0]
    dejaVu = []
    Ignore = 0
    dejaVu2 = []
     #as given in Carro2 input xml format
     #http://download.carrot2.org/head/3.11.0-SNAPSHOT/manual/#section.architecture.input-xml
    Contenu = """<?xml version="1.0" encoding='UTF-8'?>\n"""
    Contenu += "<searchresult>\n"
    Contenu += "<query>"+requete+"</query>\n"
    cmpt = 0

    for fichier in set(resum):
        dejaVu.append(fichier)
        tempo, meta =LectureFichier2(fichier)
        if tempo is not None and meta is not None:
            try:
                Label = meta.split('Label_')[1].split(' ')[0]
                Brev = [ele for ele in Brevets if ele['label'] == Label]
                if len(Brev) ==1:
                    if isinstance(Brev[0], dict):
                        try:
                            Brev[0]['title'].decode('utf8')
                            titre = bs4.BeautifulSoup(Brev[0]['title'], "lxml").text
                        except:
                            titre = Label


                        url = "http://worldwide.espacenet.com/searchResults?compact=false&amp;ST=singleline&amp;query="+Label+"&amp;locale=en_EP&amp;DB=EPODOC"
                        cmpt += 1
                        try:
                            Content = bs4.BeautifulSoup(tempo, "lxml").text
                            #soupe =  bs4.BeautifulSoup(Content.prettify(Content))
                            tempo = Content#.encode('utf8')
                            # tempo=tempo.replace('&lt;', u'>')
                            # tempo=tempo.replace('&', '&amp;')
                            if tempo not in dejaVu2:
                                dejaVu2.append(tempo)
                                Contenu+=u'<document id="%s">\n' %cmpt
                                Contenu+=u'<title>%s</title>\n' % escape(titre)
                                Contenu+=u'<url>%s</url>\n' % url

                                Contenu+=u'<snippet>%s</snippet>\n' %escape(unicode(tempo))
                                Contenu+=u"</document>\n"
                        except:
                            #print #bad encoding should be here
                            Ignore+=1
                    else:
                        pass # is this really bibliographic data ?

                else:
                    Ignore+=1
            except:
                Ignore+=1
                pass
            #cleaning temporarrary this should be done at gathering process
#            temp = tempo.split('\n')[1].strip()

        else:
            Ignore+=1
    print len(set(resum)), "fichiers "+det+ " à traiter en langage : ", lang
    print cmpt, " fichiers "+det+ " traités",
    if Ignore >0:
        print " et ", Ignore, " fichier(s) ignores (non dédoublés)"
    Contenu += u"</searchresult>"

    return Contenu.lower()


if IsEnableScript:
    Rep = configFile.ResultContentsPath
    Bib = configFile.ResultBiblioPath

    prefixes = [""]
    if GatherFamilly:
        prefixes.append("Families")

    for prefix in prefixes:
        ndf = prefix + configFile.ndf

        if 'Description'+ndf in os.listdir(Bib): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            DataBrevet = LoadBiblioFile(Bib, ndf)
            LstBrevet = DataBrevet['brevets']
        else: #Retrocompatibility
            print "please use Comptatibilizer"

        try:
            os.makedirs(Rep+"//Carrot2")
        except:
            #directory exists
            pass
        temporar = GenereListeFichiers(Rep)
        for det in ['Abstract', 'Claims', 'Description']:
            ind = 0
            for lang in ['FR', 'EN', 'UNK']:
                NomResult = lang+'_'+det.replace('Abstracts', '') + '_' + ndf+'.xml' # det.replace('Abstracts', '') this command is for old old mispelling :-(.. I think)
                ficRes = codecs.open(Rep+'//Carrot2//'+NomResult, "w", 'utf8')
                ficRes.write(complete3(temporar[ind], lang, prefix+det, LstBrevet))
                ind+=1
                ficRes.close()
