"""
Modul DAT (Digitális földmérési AlapTérkép) adatcsere-állományok
beolvasására és adataik kinyerésére.
1.0 verzió
Nagy Gábor, 2019
A modul a GNU GPL 3 feltételei szerint terjeszthető.
"""

import os
import json

tamogatott_datver=sorted([fl[3:11] for fl in os.listdir(os.path.dirname(__file__)) if fl[:3]=='dat' and fl.endswith('.json')])

def datver(datfilenev,  enc='latin-1'):
    """DAT állomány verziójának megállapítása"""
    dtf=open(datfilenev,  'r',  encoding=enc)
    cimrek=dtf.readline()
    cimmez=cimrek[:-1].split('*')[:-1]
    if len(cimmez)==7:
        return '19961227'
    elif len(cimmez)==9:
        return cimmez[8].split(' ')[0].replace('.', '')
    else:
        raise ValueError('Hibás címrekord')
    dtf.close()

def autover(filever):
    """A legjobban illeszkedő támogatott DAT verzió megállapítása"""
    nagyobbver=[v for v in tamogatott_datver if int(filever)<=int(v)]
    if len(nagyobbver)==0:
        return tamogatott_datver[-1]
    else:
        return nagyobbver[0]

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
        if len(mezo)==3:
            return mezo[0]+" decimal("+str(mezo[2])+",0)"
        elif len(mezo)==4:
            return mezo[0]+" decimal("+str(mezo[2])+","+str(mezo[3])+")"
        else:
            raise ValueError('Szabálytalan mezőlírás:'+str(mezo))
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


class DatSql:
    """Osztály a DAT adatokat fogadó adatbázis fajtájára és beállításaira"""
    
    def __init__(self,  dbtip='PostGIS', dbver=10.0, sfver=2.3, indextip='default',  nezettip='view'):
        if dbtip.lower()=='postgis':
            self._db='postgres'
            self._sfsql='postgis'
            if indextip.lower()=='noindex':
                self._spidx='noindex'
            elif indextip.lower() in ('gist',  'default'):
                self._spidx='GIST'
            elif indextip.lower()=='brin':
                self._spidx='BRIN'
            else:
                ValueError('A "'+indextip+'" típusú index a PostGIS adatbázisokban nem támogatott!')
        elif dbtip.lower()=='spatialite':
            self._db='sqlite'
            self._sfsql='spatialite'
            if indextip.lower()=='noindex':
                self._spidx='noindex'
            elif indextip.lower()=='default':
                self._spidx='default'
            else:
                ValueError('A "'+indextip+'" típusú index a SpatiaLite adatbázisokban nem támogatott!')
        elif dbtip.lower()=='geopackage':
            self._db='sqlite'
            self._sfsql='geopackage'
            raise ValueError('A GeoPackage pillanatnyilag még nem támogatott!')
        else:
            raise ValueError('A "'+dbtip+'" adatbázistípus nem támogatott!')
        self._dbver=float(dbver)
        self._sfver=float(sfver)
        self.set_nezettip(nezettip)
            
    def set_nezettip(self,  ujnezettip):
        """Új nézettípus beállítása"""
        if ujnezettip.lower()=='view':
            self._nezettip='view'
        elif ujnezettip.lower()[:5]=='mview' and self._db=='postgres':
            self._nezettip='mview'
            if ujnezettip.lower()=='mview+index':
                self._nezetidx=True
            else:
                self._nezetidx=False
        else:
            raise ValueError('Ismeretlen nézettípus a '+self._db+' adatbázishoz:"'+ujnezettip+'"')
            
    def createspatialindex(self,  tbl,  geomcol,  indexnev=None):
        """Egy térbeli indexet létrehozó SQL utasítás előállítása"""
        if indexnev==None:
            idxnev=tbl.replace('.', '_')+"_"+geomcol
        else:
            idxnev=indexnev
        if self._spidx=='noindex':
            return ''
        if self._sfsql=='postgis':
            return "CREATE INDEX "+idxnev+" ON "+tbl+" USING "+self._spidx+" ("+geomcol+");\n"
        if self._sfsql=='spatialite':
            return "SELECT CreateSpatialIndex('"+tbl+"', '"+geomcol+"');\n"
            
    def createspatialtable(self,  tbl,  normcols,  geomcols,  primkey=(1, )):
        """Egy (opcionálisan) térbeli adatokat is tartalmazó tábla létrehozását végző SQL utasítások előállítása"""
        addgeomfunc=not(self._sfsql=='postgis' and self._sfver>=2.3)
        coldefs=[adat_sqldef(mezo) for mezo in normcols]
        if not addgeomfunc:
            coldefs+=[gc[1]+" Geometry("+gc[0]+('', 'Z')[gc[2]-2]+","+str(gc[3])+")" for gc in geomcols]
        coldefs.append("PRIMARY KEY ("+", ".join([normcols[col-1][0] for col in primkey])+")")
        creastr="CREATE TABLE "+tbl+" ("+", ".join(coldefs)+");\n"
        if addgeomfunc:
            for gc in geomcols:
                creastr+="SELECT AddGeometryColumn('"+tbl+"', '"+gc[1]+"', "+str(gc[3])+", '"+gc[0]+"', "+str(gc[2])+");\n"
        for gc in geomcols:
            creastr+=self.createspatialindex(tbl,  gc[1])
        return creastr
        
    def createview(self,  vnev,  lekerdezes,  geomcols,  idxcols=[]):
        """Egy (opcionálisan) térbeli adatokat is tartalmazó nézet létrehozása"""
        if self._nezettip=='view':
            creastr="CREATE VIEW "+vnev+" AS "+lekerdezes+";\n"
        else:
            creastr="CREATE MATERIAL VIEW "+vnev+" AS "+lekerdezes+";\n"
        if self._nezettip=='mview+index':
            for idxcol in idxcols:
                creastr+="CREATE INDEX "+vnev+'_'+idxcol+" ON "+vnev+" ("+idxcol+");\n"
            for geomcol in geomcols:
                creastr+=self.createspatialindex(vnev,  geomcol)
        return creastr


class Datfile:
    """Osztály egy DAT állomány kezelésére."""
    
    def urit(self):
        """A Datfile objektum tartalmának kiürítése."""
        self._cimrekord=[]
        self._pont={}
        self._von={}
        self._hatvon={}
        self._hatar={}
        self._felulet={}
        self._hattp={}
        self._attr={}
        for objcskod in self.objcskodl:
            self._attr[objcskod]=[]

    def __init__(self,  datver='19961227'):
        """Új Datfile objektum létrehozása"""
        #Szabályzattól függő adatok beolvasása
        datszabfile=open(os.path.dirname(__file__)+'/dat'+datver+'.json')
        datszab=json.load(datszabfile)
        datszabfile.close()
        self.cimrekord=datszab['cimrekord']
        self.objcs=datszab['objcs']
        self.objgeom=datszab['objgeom']
        self.objpt=datszab['objpt']
        self.geomdefdim=datszab['geomdefdim']
        self.ptdefdim=datszab['ptdefdim']
        self.objcskodl=list(self.objcs.keys())
        #Egyéb adatok beállítása
        self.srid=23700
        #Az állomány adatait tároló attribútumok létrehozása vagy törlése
        self.urit()

    def beolvas(self, datfilenev, enc='latin-1'):
        """Egy DAT adatcsere-állomány adatainak beolvasása"""
        datfile=open(datfilenev, 'r', encoding=enc)
        self.urit()
        tablanev=''
        for datsor in datfile:
            datmez=datsor.split('*')[:-1]
            if len(datmez)==1:
                tablanev=datmez[0]
            elif tablanev=='':
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
        """Egy pont koordinátáinak lekérdezése azonosítók alapján."""
        if ptid in self._pont:
            return (self._pont[ptid][0], self._pont[ptid][1], self._pont[ptid][2])
        else:
            return False

    def ptwkt(self, ptid, dim=2):
        """Egy megatott azonosítójú pont WKT formátumban."""
        if ptid in self._pont:
            return 'POINT('+koord2wkt(self._pont[ptid], dim)+')'
        else:
            return ''

    def vonptid(self, vonid):
        """Adott azonosítójú vonal töréspontjainak pontazonosítója egy listában."""
        ret=[]
        if vonid in self._von:
            idl=sorted(self._von[vonid].keys())
            for i in idl:
                ret.append(self._von[vonid][i][0])
            ret.append(self._von[vonid][idl[-1]][1])
        return ret

    def vonptkoord(self, vonid):
        """Adott azonosítójú vonal töréspontjainak koordinátái egy listában."""
        return list(map(self.ptkoord, self.vonptid(vonid)))

    def vonwkt(self, vonid, dim=2):
        """Egy megadott azonosítójú vonal WKT formátumban."""
        if dim==2:
            wktfunc=koord2wkt2d
        else:
            wktfunc=koord2wkt3d
        return 'LINESTRING('+','.join(map(wktfunc, self.vonptkoord(vonid)))+')'

    def hatvonptid(self, hatvonid, irany='+'):
        """Adott azonosítójú határvonal töréspontjainak pontazonosítója egy listában."""
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
        """Adott azonosítójú határ töréspontjainak pontazonosítója egy listában."""
        ret=[]
        if hatid in self._hatar:
            for i in sorted(self._hatar[hatid].keys()):
                ret+=self.hatvonptid(self._hatar[hatid][i][0], irany=self._hatar[hatid][i][1])[:-1]
            if zart:
                ret+=ret[0:1]
        return ret

    def hatarptkoord(self, hatid, zart=True):
        """Adott azonosítójú határ töréspontjainak koordinátái egy listában"""
        return list(map(self.ptkoord, self.hatarptid(hatid, zart)))

    def feluletpt(self, felid, zart=True):
        """Egy megadott azonosítójú felület pontjainak azonosítói"""
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
        """Egy megadott azonosítójú felület pontjainak koordinátái"""
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
        """Egy megadott azonosítójú felület WKT formátumban."""
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
        """Megadott kódú objektumcsoport attribútumtáblájának adatai"""
        if objcskod in self._attr:
            return self._attr[objcskod]
        else:
            return [[]]

    def attr_lehetseges(self):
        """Az összes objektumcsoport kódja"""
        return list(self.objcskodl)

    def attr_nemures(self):
        """Az összes az állományban használt objektumcsoport kódja"""
        return list(filter(lambda x: len(self._attr[x])>0,self.objcskodl))

    def regi_createtbl(self, objcsop, tblnev, geomnev='geom', objdim='defdim', ptdim='defdim',  sfsql='PostGIS', tobbgeom='egybe', ptcol=None):
        """Egy adott kódú objektumcsoport tábláját vagy tábláit létrehozó SQL utasítások"""
        if not objcsop in self.attr_lehetseges():
            return "-- "+objcsop+" objektumcsoport nem létezik!"
        if tobbgeom.lower()[:10]=='kulontabla' and self.objgeom[objcsop][0]=='X':
            if tobbgeom.lower() in ('kulontabla/view',  'kulontabla/mview'):
                if tobbgeom.lower()=='kulontabla/mview' and sfsql.lower[:7]=='postgis':
                    viewmod=' MATERIALIZED '
                    viewidx='CREATE INDEX '+tblnev+'_'+geomnev+' ON '+tblnev+' USING GIST ('+geomnev+');\n'
                else:
                    viewmod=' '
                    viewidx=''
                creanezet='CREATE'+viewmod+'VIEW '+tblnev+' AS\nSELECT * FROM '+tblnev+'_pt\nUNION\nSELECT * FROM '+tblnev+'_von\nUNION\nSELECT * FROM '+tblnev+'_fel;\n'
            else:
                creanezet=''
            return self.createtbl(objcsop,  tblnev+'_pt',  tobbgeom='csakpt',  geomnev=geomnev,  objdim=objdim,  ptdim=ptdim,  sfsql=sfsql, ptcol=ptcol)+\
            self.createtbl(objcsop,  tblnev+'_von',  tobbgeom='csakvon',  geomnev=geomnev,  objdim=objdim,  ptdim=ptdim,  sfsql=sfsql, ptcol=ptcol)+\
            self.createtbl(objcsop,  tblnev+'_fel',  tobbgeom='csakfel',  geomnev=geomnev,  objdim=objdim,  ptdim=ptdim,  sfsql=sfsql, ptcol=ptcol)+creanezet+viewidx
        if objdim=='defdim':
            objkdim=self.geomdefdim[objcsop]
        elif objdim in (2, 3):
            objkdim=objdim
        else:
            ValueError('Szabálytalan érték az objektum koordinátáinak dimenziószámára:'+str(objdim))
        if ptdim=='defdim':
            ptkdim=self.ptdefdim[objcsop]
        elif ptdim in (0, 2, 3):
            ptkdim=ptdim
        else:
            ValueError('Szabálytalan érték az objektumhoz rendelt pont koordinátáinak dimenziószámára:'+str(ptdim))
        mezok=self.objcs[objcsop]
        if objcsop in self.attr_nemures():
            mintasor=self.attradat(objcsop)[0]
            if len(mezok)>len(mintasor):
                mezok=mezok[:len(mintasor)]
        coldefs=[adat_sqldef(mezo) for mezo in mezok]
        coldefs[0]+=" PRIMARY KEY"
        sqlstr="CREATE TABLE "+tblnev+" ("+", ".join(coldefs)+");\n"
        if self.objgeom[objcsop][0]=='P' or tobbgeom.lower()=='csakpt':
            geomtip=[('POINT',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='V' or tobbgeom.lower()=='csakvon':
            geomtip=[('LINESTRING',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='F' or tobbgeom.lower()=='csakfel':
            geomtip=[('MULTIPOLYGON',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='X':
            if tobbgeom.lower()[:11]=='kulonoszlop':
                geomtip=[('POINT', geomnev+'_pt',  objkdim,  self.srid),
                ('LINESTRING', geomnev+'_von',  objkdim,  self.srid),
                ('MULTIPOLYGON', geomnev+'_fel',  objkdim,  self.srid)]
            else:
                geomtip=[('GEOMETRY', geomnev,  objkdim,  self.srid)]
        if ptcol!=None and objcsop in self.objpt and ptkdim!=0:
            geomtip.append(('POINT',  ptcol,  ptkdim))
        for gtp in geomtip:
            sqlstr+="SELECT AddGeometryColumn('"+tblnev.lower()+"', '"+gtp[1]+"', "+str(self.srid)+", '"+gtp[0]+"', "+str(gtp[2])+");\n"
            if sfsql.lower()[:7]=='postgis':
                sqlstr+="CREATE INDEX "+tblnev.lower()+"_"+gtp[1]+" ON "+tblnev.lower()+" USING GIST ("+gtp[1]+");\n"
            elif sfsql.lower()[:10]=='spatialite':
                sqlstr+="SELECT CreateSpatialIndex('"+tblnev.lower()+"','"+gtp[1]+"');\n"
        if tobbgeom.lower() in ('egyben/view', 'egyben/mview') and self.objgeom[objcsop][0]=='X':
            if tobbgeom.lower()=='egyben/mview' and sfsql.lower()[:7]=='postgis':
                viewmod=' MATERIALIZED '
            else:
                viewmod=' '
            kiterjmez=self.objcs[objcsop][self.objgeom[objcsop][1]][0]
            sqlstr+='CREATE'+viewmod+'VIEW '+tblnev+'_pt  AS SELECT * FROM '+tblnev+' WHERE '+kiterjmez+'=1;\n'
            sqlstr+='CREATE'+viewmod+'VIEW '+tblnev+'_von AS SELECT * FROM '+tblnev+' WHERE '+kiterjmez+'=2;\n'
            sqlstr+='CREATE'+viewmod+'VIEW '+tblnev+'_fel AS SELECT * FROM '+tblnev+' WHERE '+kiterjmez+'=3;\n'
            if viewmod==' MATERIALIZED ':
                sqlstr+='CREATE INDEX '+tblnev+'_ptgeom  ON '+tblnev+'_pt  USING GIST ('+geomnev+');\n'
                sqlstr+='CREATE INDEX '+tblnev+'_vongeom ON '+tblnev+'_von USING GIST ('+geomnev+');\n'
                sqlstr+='CREATE INDEX '+tblnev+'_felgeom ON '+tblnev+'_fel USING GIST ('+geomnev+');\n'
        return sqlstr
        
    def createtbl(self, dbtipus,  objcsop, tblnev, geomnev='geom', objdim='defdim', ptdim='defdim', tobbgeom=('egyben', ),  ptcol=None):
        """Egy adott kódú objektumcsoport tábláját vagy tábláit létrehozó SQL utasítások"""
        if not objcsop in self.attr_lehetseges():
            return "-- "+objcsop+" objektumcsoport nem létezik!"
        if objdim=='defdim':
            objkdim=self.geomdefdim[objcsop]
        elif objdim in (2, 3):
            objkdim=int(objdim)
        else:
            ValueError('Szabálytalan érték az objektum koordinátáinak dimenziószámára:'+str(objdim))
        if ptdim=='defdim':
            ptkdim=self.ptdefdim[objcsop]
        elif ptdim in (0, 2, 3):
            ptkdim=ptdim
        else:
            ValueError('Szabálytalan érték az objektumhoz rendelt pont koordinátáinak dimenziószámára:'+str(ptdim))
        mezok=self.objcs[objcsop]
        if objcsop in self.attr_nemures():
            mintasor=self.attradat(objcsop)[0]
            if len(mezok)>len(mintasor):
                mezok=mezok[:len(mintasor)]
        if ptcol!=None and objcsop in self.objpt and ptkdim!=0:
            ptgeomdef=[('POINT',  ptcol,  ptkdim,  self.srid)]
        else:
            ptgeomdef=[]
        if tobbgeom[0].lower()=='kulontabla' and self.objgeom[objcsop][0]=='X':
            return dbtipus.createspatialtable(tblnev+'_pt',  mezok,  [('POINT',  geomnev,  objkdim,  self.srid)]+ptgeomdef)+\
            dbtipus.createspatialtable(tblnev+'_von',  mezok,  [('LINESTRING',  geomnev,  objkdim,  self.srid)]+ptgeomdef)+\
            dbtipus.createspatialtable(tblnev+'_fel',  mezok,  [('MULTIPOLYGON',  geomnev,  objkdim,  self.srid)]+ptgeomdef)
        if self.objgeom[objcsop][0]=='P':
            geomcols=[('POINT',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='V':
            geomcols=[('LINESTRING',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='F':
            geomcols=[('MULTIPOLYGON',  geomnev,  objkdim,  self.srid)]
        elif self.objgeom[objcsop][0]=='X':
            if tobbgeom[0].lower()=='kulonoszlop':
                geomcols=[('POINT', geomnev+'_pt',  objkdim,  self.srid),
                ('LINESTRING', geomnev+'_von',  objkdim,  self.srid),
                ('MULTIPOLYGON', geomnev+'_fel',  objkdim,  self.srid)]
            else:
                geomcols=[('GEOMETRY', geomnev,  objkdim,  self.srid)]
        return dbtipus.createspatialtable(tblnev,  mezok,  geomcols+ptgeomdef)

    def insertsor(self, objcsop, tblnev, adatsor, geomnev='geom', objdim='defdim', ptdim='defdim',  tobbgeom=('egyben', ), ptcol=None):
        """Egy adott objektumcsoport egy objektumának adatait beszúró SQL utasítás"""
        if objdim=='defdim':
            objkdim=self.geomdefdim[objcsop]
        elif objdim in (2, 3):
            objkdim=objdim
        else:
            ValueError('Szabálytalan érték az objektum koordinátáinak dimenziószámára:'+str(objdim))
        if ptdim=='defdim':
            ptkdim=self.ptdefdim[objcsop]
        elif ptdim in (0, 2, 3):
            ptkdim=ptdim
        else:
            ValueError('Szabálytalan érték az objektumhoz rendelt pont koordinátáinak dimenziószámára:'+str(ptdim))
        if not objcsop in self.attr_lehetseges():
            return "-- A "+objcsop+" objektumcsoport nem létezik!"
        if len(adatsor)<5:
            return "-- A "+objcsop+" objektumcsoport táblájába beszúrandó sor nem tartalmaz elég adatot!"
        mezok=self.objcs[objcsop]
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
        gmeznev=geomnev
        tblutan=''
        if self.objgeom[objcsop][0]=='P':
            wkt=self.ptwkt(int(sor[self.objgeom[objcsop][1]]), dim=objkdim)
        elif self.objgeom[objcsop][0]=='V':
            wkt=self.vonwkt(int(sor[self.objgeom[objcsop][1]]), dim=objkdim)
        elif self.objgeom[objcsop][0]=='F':
            wkt=self.feluletwkt(int(sor[self.objgeom[objcsop][1]]), dim=objkdim)
        elif self.objgeom[objcsop][0]=='X':
            if int(sor[self.objgeom[objcsop][1]])==1:
                if tobbgeom[0]=='kulonoszlop': gmeznev+='_pt'
                if tobbgeom[0]=='kulontabla': tblutan='_pt'
                wkt=self.ptwkt(int(sor[self.objgeom[objcsop][2]]), dim=objkdim)
            elif int(sor[self.objgeom[objcsop][1]])==2:
                if tobbgeom[0]=='kulonoszlop': gmeznev+='_von'
                if tobbgeom[0]=='kulontabla': tblutan='_von'
                wkt=self.vonwkt(int(sor[self.objgeom[objcsop][2]]), dim=objkdim)
            elif int(sor[self.objgeom[objcsop][1]])==3:
                if tobbgeom[0]=='kulonoszlop': gmeznev+='_fel'
                if tobbgeom[0]=='kulontabla': tblutan='_fel'
                wkt=self.feluletwkt(int(sor[self.objgeom[objcsop][2]]), dim=objkdim)
        meznevek.append(gmeznev)
        adatok.append("GeomFromEWKT('SRID="+str(self.srid)+";"+wkt+"')")
        if ptcol!=None and objcsop in self.objpt and ptkdim!=0:
            meznevek.append(ptcol)
            objptwkt=self.ptwkt(int(sor[self.objgeom[objcsop][1]]), dim=ptkdim)
            if objptwkt!='':
                adatok.append("GeomFromEWKT('SRID="+str(self.srid)+";"+objptwkt+"')")
            else:
                adatok.append("NULL")
        return "INSERT INTO "+tblnev+tblutan+" ("+", ".join(meznevek)+") VALUES ("+", ".join(adatok)+");"

    def insertsorok(self, objcsop, tblnev, geomnev='geom', objdim='defdim', ptdim='defdim',  tobbgeom='egybe', ptcol=None):
        """Egy adott objektumcsoport összes az állományban megtalálható elemét beszúró SQL utasítások"""
        if not objcsop in self.attr_lehetseges():
            return "-- "+objcsop+" objektumcsoport nem létezik!"
        inssorok=[]
        for sor in self._attr[objcsop]:
            inssorok.append(self.insertsor(objcsop, tblnev, sor, geomnev=geomnev, objdim=objdim, ptdim=ptdim,  tobbgeom=tobbgeom, ptcol=ptcol))
        return "\n".join(inssorok)
