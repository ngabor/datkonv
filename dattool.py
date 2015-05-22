"""
Modul DAT (Digitális földmérési AlatTérkép) adatcsere-állományok
beolvasására és adataik kinyerésére.
0.2 verzió
Nagy Gábor, 2015
A modul a GNU GPL 3 feltételei szerint terjeszthető.
"""


objcs= { "AA":[ ("alappont_id","N",5), ("obj_fels","AN",4), ("pont_szam","AN",20), ("pont_id","N",8), ("vizsz_alland1","N",2), ("pontvedo","N",2), ("vizsz_alland2","N",2), ("v_mag2","N",8), ("vizsz_alland3","N",2), ("v_mag3","N",8), ("meghat_mod","N",2), ("szemely_id","N",8), ("all_datum","D",0), ("elozo_alappont_id","N",5), ("blokk_file","AN",12), ("megsz_datum","D",0), ("tar_hely","AN",50), ("digit_hely","AN",50), ("jelkulcs","N",3), ("munkater_id","N",6)],
         "AB":[ ("malapp_id","N",5), ("obj_fels","AN",4), ("mpont_szam","AN",20), ("pont_id","N",8), ("mag_alland","N",2), ("mag_allandfa","N",2), ("mag","N",8), ("meghat_mod","N",2), ("szemely_id","N",8), ("all_datum","D",0), ("elozo_malapp_id","N",5), ("blokk_file","AN",12), ("megsz_datum","D",0), ("tar_hely","AN",50), ("digit_hely","AN",50), ("jelkulcs","N",3), ("munkater_id","N",6)],
         "AC":[ ("rpont_id","N",6), ("obj_fels","AN",4), ("pont_szam","AN",20), ("pont_id","N",8), ("vizsz_alland","N",2), ("meghat_mod","N",2), ("meghat_datum","D",0), ("elozo_rpont_id","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6)],
         "BA":[ ("kozig_idba","N",5), ("obj_fels","AN",4), ("felulet_id","N",8), ("kozig_id","N",4), ("kozig_kp","N",4), ("ceg_id","N",6), ("elhat_jell","N",1), ("elhat_mod","N",1), ("nemz_nev1","AN",20), ("nemz_nev2","AN",20), ("elozo_kozig_idba","N",5), ("kep_file","AN",24), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BB":[ ("kozigal_id","N",6), ("obj_fels","AN",4), ("felulet_id","N",8), ("kozigal_nev","AN",20), ("kozid_id","N",4), ("l_datum","D",0), ("hatarozat","AN",20), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_kozigal_id","N",6), ("kep_file","AN",24), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BC":[ ("parcel_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("helyr_szam","AN",10), ("cim_id","N",8), ("fekves","N",1), ("kozter_jell","N",2), ("terulet","N",8), ("foldert","N",5), ("forg_ertek","N",6), ("szerv_tip","N",2), ("jogi_jelleg","N",3), ("jogallas","N",2), ("ceg_id","N",6), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_parcel_id","N",8), ("l_datum","D",0), ("hatarozat","AN",20), ("valt_jell","AN",20), ("tar_hely","AN",20), ("blokk_file","AN",12), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BD":[ ("parcel_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("helyr_szam","AN",10), ("cim_id","N",8), ("fekves","N",1), ("terulet","N",8), ("foldert","N",5), ("forg_ertek","N",6), ("szerv_tip","N",2), ("jogi_jelleg","N",3), ("jogallas","N",2), ("szemely_id","N",8), ("ceg_id","N",6), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_parcel_id","N",8), ("l_datum","D",0), ("hatarozat","AN",20), ("valt_jell","AN",20), ("tar_hely","AN",20), ("blokk_file","AN",12), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BE":[ ("alreszlet_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("alator","AN",3), ("helyr_szam","AN",10), ("terulet","N",8), ("foldert","N",5), ("muvel_ag","N",2), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_alreszlet_id","N",8), ("l_datum","D",0), ("hatarozat","AN",20), ("valt_jell","AN",20), ("tar_cim","AN",20), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BF":[ ("moszt_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("minoseg_oszt","N",2), ("muvel_ag","N",2), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_moszt_id","N",8), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "BG":[ ("eoi_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("alator_eoi","AN",4), ("helyr_szam","AN",10), ("cim_eoi","N",8), ("kozter_jell","N",2), ("terulet","N",6), ("forg_ertek","N",6), ("szerv_tip","N",2), ("jogi_jelleg","N",3), ("jogallas","N",2), ("eoi_helyiseg","N",2), ("eoi_tulform","N",2), ("szemely_id","N",8), ("ceg_id","N",6), ("elhat_jell","N",1), ("elhat_mod","N",1), ("elozo_eoi_id","N",8), ("l_datum","D",0), ("hatarozat","AN",20), ("valt_jell","AN",20), ("tar_hely","AN",20), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "CA":[ ("ep_id","N",8), ("obj_fels","AN",4), ("felulet_id","N",8), ("ep_cim_id","N",6), ("parcel_id","N",6), ("ep_sorsz","N",4), ("szintek","N",2), ("fugg_kiter","N",3), ("anyag","N",2), ("epulet_tip","N",2), ("epulet_alt","N",2), ("szemely_id","N",8), ("ceg_id","N",6), ("elozo_ep_id","N",8), ("blokk_file","AN",12), ("t_obj_attric","N",8), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "CB":[ ("eptart_id","N",8), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("ep_id","N",8), ("fugg_kiter","N",2), ("anyag","N",2), ("elozo_eptert_id","N",8), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "CC":[ ("kerit_id","N",6), ("obj_fels","AN",4), ("felulet_id","N",8), ("helyr_szam","AN",10), ("fugg_kiter","N",2), ("anyag","N",2), ("szemely_id","N",8), ("ceg_id","N",6), ("elozo_kerit_id","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "CD":[ ("terept_id","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("helyr_szam","AN",10), ("fugg_kiter","N",2), ("anyag","N",2), ("szemely_id1","N",8), ("ceg_id1","N",6), ("szemely_id2","N",8), ("ceg_id2","N",6), ("elozo_terept_id","N",5), ("blokk_file","AN",12), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "CE":[ ("szobor_id","N",4), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("helyr_szam","AN",10), ("kozter_nev","AN",5), ("fugg_kiter","N",2), ("anyag","N",2), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_szobor_id","N",4), ("blokk_file","AN",12), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "DA":[ ("kozut_az_id","N",4), ("obj_fels","AN",4), ("pont_id","N",8), ("szakag_sz","AN",10), ("kozuti_az","N",2), ("szak_nev","AN",5), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_kozut_az_id","N",4), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6)],
         "DB":[ ("kozl_let","N",6), ("obj_fels","AN",4), ("felulet_id","N",8), ("szak_nev","AN",5), ("pont_id","N",8), ("anyag_burk","N",2), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_kozl_let","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id2","N",8)],
         "DC":[ ("kozl_let","N",6), ("obj_fels","AN",4), ("felulet_id","N",8), ("szak_nev","AN",5), ("anyag_burk","N",2), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("pont_id1","N",8), ("pont_id2","N",8), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_kozl_let","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id3","N",8)],
         "DD":[ ("vasut_kp","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("szak_nev","AN",5), ("pont_id1","N",8), ("pont_id2","N",8), ("kereszt","N",1), ("obj_az","N",8), ("obj_fels1","AN",4), ("pont_id3","N",8), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_vasut_kp","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id4","N",8)],
         "DE":[ ("repter_id","N",3), ("obj_fels","AN",4), ("felulet_id","N",8), ("szak_nev","AN",5), ("repter_tip","N",2), ("repter_oszt","N",2), ("szak_nev","AN",5), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_repter_id","N",3), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "DF":[ ("mutargy","N",6), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("szak_nev","AN",5), ("athid_szerk","N",2), ("anyag_burk","N",2), ("athid_allapot","N",2), ("athid_akad","N",2), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_mutargy","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "DG":[ ("mutargy","N",6), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("szak_nev","AN",5), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_mutargy","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "EA":[ ("tavvez","N",5), ("obj_fels","AN",4), ("vonal_id","N",8), ("szak_nev","AN",5), ("ved_sav","N",3), ("korlat","N",3), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("pont_id1","N",8), ("pont_id2","N",8), ("kereszt","N",1), ("obj_az","N",6), ("obj_fels1","AN",4), ("pont_id3","N",8), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_tavvez","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id4","N",8)],
         "EB":[ ("mutargy","N",6), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("szak_nev","AN",5), ("ved_sav","N",3), ("korlat","N",3), ("jell_adat","N",3), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_mutargy","N",6), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "FA":[ ("viz","N",5), ("obj_fels","AN",4), ("felulet_id","N",8), ("vobj_fo_al","N",4), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("pont_id1","N",8), ("pont_id2","N",8), ("kereszt","N",1), ("obj_az","N",6), ("obj_fels1","AN",4), ("pont_id3","N",8), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_viz","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id4","N",8)],
         "FB":[ ("viz_kozmu","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("vobj_fo_al","N",4), ("ved_sav","N",3), ("korlat","N",3), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("pont_id1","N",8), ("pont_id2","N",8), ("kereszt","N",1), ("obj_az","N",6), ("obj_fels1","AN",4), ("pont_id3","N",8), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_viz_kozmu","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id4","N",8)],
         "FC":[ ("viz_mut","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("vobj_fo_al","N",4), ("korlat","N",3), ("jell_adat1","AN",4), ("jell_adat2","AN",4), ("jell_adat3","AN",4), ("ceg_id1","N",6), ("ceg_id2","N",6), ("elozo_viz_mut","N",5), ("mgsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "GA":[ ("szintvo","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("elozo_szintvo","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "GB":[ ("domb","N",5), ("obj_fels","AN",4), ("obj_kiterj","N",1), ("geo_ae_id","N",8), ("pont_id1","N",8), ("pont_id2","N",8), ("elozo_domb","N",5), ("megsz_datum","D",0), ("jelkulcs","N",3), ("munkater_id","N",6), ("pont_id","N",8)],
         "HA":[ ("munkater_id","N",6), ("obj_fels","AN",4), ("felulet_id","N",8), ("felm_tan","AN",150), ("mu_terv","AN",150), ("mu_leir","AN",150), ("torzskonyv","AN",150), ("forras","AN",150), ("munkareszek","AN",150), ("kezd_datum","D",0), ("felm_datum","D",0), ("hitel_datum","D",0), ("adatgy1","AN",1), ("adatgy2","AN",1), ("adatgy3","AN",1), ("ceg_id1","N",6), ("szemely_id1","N",8), ("munkater_ny_m","AN",20), ("ceg_id2","N",6), ("szemely_id2","N",8), ("munkater_ny_f","AN",20), ("ceg_id3","N",6), ("szemely_id3","N",8), ("munkater_ny_h","AN",20), ("munkater_id_knt","AN",12), ("szemely_id4","N",6), ("pont_id","N",8)],
         "HB":[ ("nyterulet","N",3), ("obj_fels","AN",4), ("felulet_id","N",8), ("nyt_nev","AN",30), ("ceg_id1","N",6), ("szemely_id2","N",8), ("kezd_datum","D",0), ("bef_datum","D",0), ("pont_id","N",8)],
         "HC":[ ("terseg","N",4), ("obj_fels","AN",4), ("felulet_id","N",8), ("ter_nev","AN",30), ("ceg_id1","N",6), ("ceg_id2","N",6), ("kezd_datum","D",0), ("szemely_id3","N",8), ("elozo_terseg","N",4), ("megsz_datum","D",0), ("pont_id","N",8)]}

objcskodl=list(objcs.keys())

objgeom={'AA':('P',3), 'AB':('P',3), 'AC':('P',3),
         'BA':('F',3), 'BB':('F',3), 'BC':('F',3), 'BD':('F',3), 'BE':('F',3), 'BF':('F',3), 'BG':('F',3),
         'CA':('F',3), 'CB':('X',3,4), 'CC':('F', 3), 'CD':('X',3,4), 'CE':('X',3,4),
         'DA':('P',3), 'DB':('F',3), 'DC':('F',3), 'DD':('X',3,4), 'DE':('F',3), 'DF':('X',3,4), 'DG':('X',3,4),
         'EA':('V',3), 'EB':('X',3,4),
         'FA':('F',3), 'FB':('X',3,4), 'FC':('X',3,4),
         'GA':('X',3,4), 'GB':('X',3,4),
         'HA':('F',3), 'HB':('F',3), 'HC':('F',3)}



def adat_formaz(adat, forma):
    if adat=='':
        return 'NULL'
    else:
        if forma[1]=='N':
            return str(adat)
        elif forma[1]=='AN':
            return "'"+str(adat)+"'"
        elif forma[1]=='D':
            if len(adat)<8:
                return 'NULL'
            return "'"+adat[0:4]+"."+adat[4:6]+"."+adat[6:8]+"'"
        else:
            print('Hibás adatleírás:',adat,forma)


def adat_sqldef(mezo):
    if mezo[1]=='N':
        return mezo[0]+" decimal("+str(mezo[2])+",0)"
    elif mezo[1]=='AN':
        return mezo[0]+" char("+str(mezo[2])+")"
    elif mezo[1]=='D':
        return mezo[0]+" date"
    else:
        print('Hibás adatleírás:',mezo)

def koord2wkt(koord, dim=2):
    wkt=str(koord[0])+' '+str(koord[1])
    if dim==3:
        wkt+=' '+str(koord[2])
    return wkt

def koord2wkt2d(koord):
    return str(koord[0])+' '+str(koord[1])

def koord2wkt3d(koord):
    return str(koord[0])+' '+str(koord[1])+' '+str(koord[2])

class Datfile:
    "Osztály egy DAT állomány kezelésére."
    def urit(self):
        "A Datfile objektum tartalmának kiürítése."
        self._cimrekord=[]
        self._pont={}
        self._von={}
        self._hatvon={}
        self._hatar={}
        self._felulet={}
        self._hattp={}
        self._attr={}
        for objcskod in objcskodl:
            self._attr[objcskod]=[]

    def __init__(self):
        "Új Datfile objektum létrehozása"
        self.urit()

    def beolvas(self, datfilenev, enc='latin-1'):
        "Egy DAT adatcsere-állomány adatainak beolvasása"
        datfile=open(datfilenev, 'r', encoding=enc)
        self.urit()
        tablanev=''
        for datsor in datfile:
            datmez=datsor.split('*')[:-1]
            if len(datmez)==1:
                tablanev=datmez[0]
            if tablanev=='':
                self._cimrekord=datmez
            elif tablanev=='T_PONT' and len(datmez)==6:
                if datmez[3]=='':
                    datmez[3]=0
                self._pont[int(datmez[0])]=(float(datmez[2]),
                                            float(datmez[1]),
                                            float(datmez[3]),
                                            datmez[4],
                                            datmez[5])
            elif tablanev=='T_VONAL' and len(datmez)==6:
                vonid=int(datmez[0])
                subid=int(datmez[1])
                if not vonid in self._von:
                    self._von[vonid]={}
                self._von[vonid][subid]=(int(datmez[2]),
                                         int(datmez[3]),
                                         datmez[4],
                                         datmez[5])
            elif tablanev=='T_HATARVONAL' and len(datmez)==6:
                hvid=int(datmez[0])
                subid=int(datmez[1])
                if not hvid in self._hatvon:
                    self._hatvon[hvid]={}
                self._hatvon[hvid][subid]=(int(datmez[2]),
                                           int(datmez[3]),
                                           datmez[4],
                                           datmez[5])
            elif tablanev=='T_HATAR' and len(datmez)==4:
                hatid=int(datmez[0])
                subid=int(datmez[1])
                if not hatid in self._hatar:
                    self._hatar[hatid]={}
                self._hatar[hatid][subid]=(int(datmez[2]),
                                           datmez[3])
            elif tablanev=='T_FELULET' and len(datmez)==4:
                felid=int(datmez[0])
                subid=int(datmez[1])
                if not felid in self._felulet:
                    self._felulet[felid]={}
                if not subid in self._felulet[felid]:
                    self._felulet[felid][subid]=[]
                self._felulet[felid][subid].append((int(datmez[2]),
                                                    datmez[3]))
            elif tablanev[0:10]=='T_OBJ_ATTR':
                objcskod=tablanev[10:12]
                if len(datmez)>1:
                    self._attr[objcskod].append(datmez)
        datfile.close()

    def ptkoord(self, ptid):
        "Egy pont koordinátáinak lekérdezése azonosítók alapján."
        if ptid in self._pont:
            return (self._pont[ptid][0], self._pont[ptid][1], self._pont[ptid][2])
        else:
            return False

    def ptwkt(self, ptid, dim=2):
        "Egy megatott azonosítójú pont WKT formátumban."
        if ptid in self._pont:
            return 'POINT('+koord2wkt(self._pont[ptid], dim)+')'
        else:
            return ''

    def vonptid(self, vonid):
        "Adott azonosítójú vonal töréspontjainak pontazonosítója egy listában."
        ret=[]
        if vonid in self._von:
            idl=sorted(self._von[vonid].keys())
            for i in idl:
                ret.append(self._von[vonid][i][0])
            ret.append(self._von[vonid][idl[-1]][1])
        return ret

    def vonptkoord(self, vonid):
        "Adott azonosítójú vonal töréspontjainak koordinátái egy listában."
        return list(map(self.ptkoord, self.vonptid(vonid)))

    def vonwkt(self, vonid, dim=2):
        "Egy megadott azonosítójú vonal WKT formátumban."
        if dim==2:
            wktfunc=koord2wkt2d
        else:
            wktfunc=koord2wkt3d
        return 'LINESTRING('+','.join(map(wktfunc, self.vonptkoord(vonid)))+')'

    def hatvonptid(self, hatvonid, irany='+'):
        "Adott azonosítójú határvonal töréspontjainak pontazonosítója egy listában."
        if irany=='+':
            revsort=False
            idxi=1
            idxn=0
        else:
            revsort=True
            idxi=0
            idxn=1
        ret=[]
        if hatvonid in self._hatvon:
            idl=sorted(self._hatvon[hatvonid].keys(), reverse=revsort)
            for i in idl:
                ret.append(self._hatvon[hatvonid][i][idxi])
            ret.append(self._hatvon[hatvonid][idl[-1]][idxn])
        return ret

    def hatarptid(self, hatid, zart=True):
        "Adott azonosítójú határ töréspontjainak pontazonosítója egy listában."
        ret=[]
        if hatid in self._hatar:
            for i in sorted(self._hatar[hatid].keys()):
                ret+=self.hatvonptid(self._hatar[hatid][i][0], irany=self._hatar[hatid][i][1])[:-1]
            if zart:
                ret+=ret[0:1]
        return ret

    def hatarptkoord(self, hatid, zart=True):
        "Adott azonosítójú határ töréspontjainak koordinátái egy listában"
        return list(map(self.ptkoord, self.hatarptid(hatid, zart)))

    def feluletpt(self, felid, zart=True):
        "Egy megadott azonosítójú felület pontjainak azonosítói"
        if not felid in self._felulet:
            return [[]]
        mpoli=[]
        for i in self._felulet[felid].keys():
            poli=[]
            for j in self._felulet[felid][i]:
                if j[1]=='+':
                    poli.append(self.hatarptid(j[0], zart))
            for j in self._felulet[felid][i]:
                if j[1]=='-':
                    poli.append(self.hatarptid(j[0], zart))
            mpoli.append(poli)
        return mpoli

    def feluletkoord(self, felid, zart=True):
        "Egy megadott azonosítójú felület pontjainak koordinátái"
        if not felid in self._felulet:
            return [[]]
        mpoli=[]
        for i in self._felulet[felid].keys():
            poli=[]
            for j in self._felulet[felid][i]:
                if j[1]=='+':
                    poli.append(self.hatarptkoord(j[0], zart))
            for j in self._felulet[felid][i]:
                if j[1]=='-':
                    poli.append(self.hatarptkoord(j[0], zart))
            mpoli.append(poli)
        return mpoli

    def feluletwkt(self, felid, dim=2, nomulti=False):
        "Egy megadott azonosítójú felület WKT formátumban."
        if dim==2:
            wktfunc=koord2wkt2d
        else:
            wktfunc=koord2wkt3d
        ptkoord=self.feluletkoord(felid)
        poliwktl=[]
        for poli in ptkoord:
            ringwktl=[]
            for ring in poli:
                ringwktl.append('('+','.join(map(wktfunc, ring))+')')
            poliwktl.append('('+', '.join(ringwktl)+')')
        if nomulti and len(poliwktl)==1:
            wkt='POLYGON'+poliwktl[0]+''
        else:
            wkt='MULTIPOLYGON('+','.join(poliwktl)+')'
        return wkt

    def attradat(self, objcskod):
        "Megadott kódú objektumcsoport attribútumtáblájának adatai"
        if objcskod in self._attr:
            return self._attr[objcskod]
        else:
            return [[]]

    def attr_lehetseges(self):
        "Az összes objektumcsoport kódja"
        return list(objcs.keys())

    def attr_nemures(self):
        "Az összes az állományban használt objektumcsoport kódja"
        return list(filter(lambda x: len(self._attr[x])>0,objcs.keys()))

    def createtbl(self, objcsop, tblnev, geomnev='geom', dim=2, geomindex='PostGIS', tobbgeom=True, srid=23700):
        "Egy adott kódú objektumcsoport tábláját létrehozó SQL utasítások"
        if not objcsop in self.attr_lehetseges():
            return "-- "+objcsop+" objektumcsoport nem létezik!"
        mezok=objcs[objcsop]
        if objcsop in self.attr_nemures():
            mintasor=self.attradat(objcsop)[0]
            if len(mezok)>len(mintasor):
                mezok=mezok[:len(mintasor)]
        coldefs=list(map(adat_sqldef, mezok))
        coldefs[0]+=" PRIMARY KEY"
        sqlstr="CREATE TABLE "+tblnev+" ("+", ".join(coldefs)+");\n"
        if dim in [2, 3]:
            geomtip=[]
            if mezok[2][0] in ['pont_id', 'pont_szam', 'mpont_szam']:
                geomtip=[('POINT', '')]
            elif mezok[2][0]=='vonal_id':
                geomtip=[('LINESTRING', '')]
            elif mezok[2][0]=='felulet_id':
                geomtip=[('MULTIPOLYGON', '')]
            elif mezok[2][0]=='obj_kiterj':
                if tobbgeom:
                    geomtip=[('POINT', '_pt'), ('LINESTRING', '_von'), ('MULTIPOLYGON', '_fel')]
                else:
                    geomtip=[('GEOMETRY', '')]
            if geomtip==[]: print(objcsop, mezok)
            for gtp in geomtip:
                sqlstr+="SELECT AddGeometryColumn('"+tblnev.lower()+"', '"+geomnev+gtp[1]+"', "+str(srid)+", '"+gtp[0]+"', "+str(dim)+");\n"
                if geomindex=='PostGIS':
                    sqlstr+="CREATE INDEX "+tblnev.lower()+"_"+geomnev+gtp[1]+" ON "+tblnev.lower()+" USING GIST ("+geomnev+gtp[1]+");\n"
                elif geomindex=='SpatiaLite':
                    sqlstr+="SELECT CreateSpatialIndex('"+tblnev.lower()+"','"+geomnev+gtp[1]+"');\n"
        return sqlstr

    def insertsor(self, objcsop, tblnev, adatsor, geomnev='geom', dim=2, tobbgeom=True, srid=23700):
        "Egy adott objektumcsoport egy objektumának adatait beszúró SQL utasítás"
        if not objcsop in self.attr_lehetseges():
            return "-- A "+objcsop+" objektumcsoport nem létezik!"
        if len(adatsor)<5:
            return "-- A "+objcsop+" objektumcsoport táblájába beszúrandó sor nem tartalmaz elég adatot!"
        mezok=objcs[objcsop]
        sor=adatsor
        if len(mezok)>len(sor):
            mezok=mezok[:len(sor)]
        if len(mezok)<len(sor):
            sor=sor[:len(mezok)]
        meznevek=[]
        adatok=[]
        for i in range(len(sor)):
            meznevek.append(mezok[i][0])
            adatok.append(adat_formaz(sor[i], mezok[i]))
        if dim in [2, 3]:
            gmeznev=geomnev
            if mezok[2][0]=='pont_id':
                wkt=self.ptwkt(int(sor[2]), dim=dim)
            if mezok[2][0] in ['pont_szam', 'mpont_szam']:
                wkt=self.ptwkt(int(sor[3]), dim=dim)
            elif mezok[2][0]=='vonal_id':
                wkt=self.vonwkt(int(sor[2]), dim=dim)
            elif mezok[2][0]=='felulet_id':
                wkt=self.feluletwkt(int(sor[2]), dim=dim)
            elif mezok[2][0]=='obj_kiterj':
                if int(sor[2])==1:
                    if tobbgeom:
                        gmeznev+='_pt'
                    wkt=self.ptwkt(int(sor[3]), dim=dim)
                elif int(sor[2])==2:
                    if tobbgeom:
                        gmeznev+='_von'
                    wkt=self.vonwkt(int(sor[3]), dim=dim)
                elif int(sor[2])==3:
                    if tobbgeom:
                        gmeznev+='_fel'
                    wkt=self.feluletwkt(int(sor[3]), dim=dim)
            meznevek.append(gmeznev)
            adatok.append("GeomFromEWKT('SRID="+str(srid)+";"+wkt+"')")
        return "INSERT INTO "+tblnev+" ("+", ".join(meznevek)+") VALUES ("+", ".join(adatok)+");"

    def insertsorok(self, objcsop, tblnev, geomnev='geom', dim=2, tobbgeom=True, srid=23700):
        "Egy adott objektumcsoport összes az állományban megtalálható elemét beszúró SQL utasítások"
        if not objcsop in self.attr_lehetseges():
            return "-- "+objcsop+" objektumcsoport nem létezik!"
        inssorok=[]
        for sor in self._attr[objcsop]:
            inssorok.append(self.insertsor(objcsop, tblnev, sor, geomnev=geomnev, dim=dim, tobbgeom=tobbgeom, srid=srid))
        return "\n".join(inssorok)
