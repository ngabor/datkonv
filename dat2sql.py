#!/usr/bin/env python3
"""
Program DAT adatcsere állományok adatainak
az OGC Simple Feature SQL szabványa szerint
működő adatbázisokba töltésére.
1.0 verzió
Nagy Gábor, 2019
A program a GNU GPL 3 feltételei szerint terjeszthető.
"""

from dattool import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("datfile", help="a belovasandó DAT állomány")
parser.add_argument("sqlfile", help="a létrehozandó SQL állomány")
parser.add_argument("--kihagy", help="objektumcsoportok kihagyása (kódok vesszővel tagolt listában)")
parser.add_argument("--objcsop", help="csak a megadott objektumcsoportok konvertálása (kódok vesszővel tagolt listában)")
parser.add_argument("--def2D", default=False, action="store_true", help="alapértelmezetten 2D objektumok készítése")
parser.add_argument("--def3D", default=False, action="store_true", help="alapértelmezetten 3D objektumok készítése")
parser.add_argument("--objcs2D", help="megadott objektumcsoportok az alapértelmezéstől eltérően 2D objektumokkal")
parser.add_argument("--objcs3D", help="megadott objektumcsoportok az alapértelmezéstől eltérően 3D objektumokkal")
parser.add_argument("--tbl_elotag", default="t_obj_attr", help="a tábla nevében az objektumcsoport kódja elé fűzendő szöveg")
parser.add_argument("--tbl_utotag", default="", help="a tábla nevében az objektumcsoport kódja után fűzendő szöveg")
parser.add_argument("--geom_neve", default="geom", help="a geometriát tartalmazó oszlop neve")
parser.add_argument("--tobbgeom", default='kulonoszlop', help="a többféle kiterjedésű objektumokat is tartalmazó táblák kezelésének elve: egyben, kulonoszlop, kulontabla")
parser.add_argument("--ptgeom_neve", default=None, help="az objektumokhoz másodlagosan tartozó pont (geokód, címkoordináta, stb.) oszlopának neve")
parser.add_argument("--dbtip", default='PostGIS', help="az SF-SQL adatbázis típusa: PostGIS, Spatialite")
parser.add_argument("--spidx",  default='default',  help="a térbeli index típusa")
parser.add_argument("--nezettip",  default='view',  help="a nézetek típusa: view, mview")
parser.add_argument("--datver",  default='auto',  help="a dat állomány verziója: auto vagy pontos verziószám")
args = parser.parse_args()

if args.datver=='auto':
    dtver=autover(datver(args.datfile))
else:
    if args.datver in tamogatott_datver:
        dtver=args.datver
    else:
        raise ValueError('Nem támogatott DAT verziószám:'+args.datver)

dtf=Datfile(datver=dtver)
dtf.beolvas(args.datfile)

objcsopok=set(dtf.attr_nemures())
if not args.objcsop==None:
    ocs=set(args.objcsop.upper().split(','))&objcsopok
else:
    ocs=objcsopok
if not args.kihagy==None:
    ocs=ocs-set(args.kihagy.upper().split(','))

if args.def3D:
    ocs3D=ocs
else:
    ocs3D=set()
if not args.objcs3D==None:
    ocs3D=ocs3D|set(args.objcs3D.upper().split(','))
if not args.objcs2D==None:
    ocs3D=ocs3D-set(args.objcs2D.upper().split(','))

if args.tobbgeom.lower()=='egyben':
    tobbgeom=('egyben', )
elif args.tobbgeom.lower()=='kulonoszlop':
    tobbgeom=('kulonoszlop', )
elif args.tobbgeom.lower()=='kulontabla':
    tobbgeom=('kulontabla', )
else:
    raise ValueError('A --tobbgeom kapcsolónak szabálytalan érték lett megadva:'+args.tobbgeom)

dbpar=DatSql(dbtip=args.dbtip,  indextip=args.spidx)

sqlf=open(args.sqlfile,'w')
print('-- A dat2sql.py programmal előállított SQL állomány',  file=sqlf)
print('--          A forrás DAT állomány:'+args.datfile,  file=sqlf)
print('-- A forrás DAT állomány verziója:'+datver(args.datfile),  file=sqlf)
print('--         Alkalmazott DAT verzió:'+dtver,  file=sqlf)
for objcsop in sorted(ocs):
    if objcsop in ocs3D:
        dim=3
    else:
        dim=2
    print(dtf.createtbl(dbpar,  objcsop, args.tbl_elotag+objcsop+args.tbl_utotag, objdim=dim, geomnev=args.geom_neve, tobbgeom=tobbgeom, ptcol=args.ptgeom_neve), file=sqlf)
print("BEGIN;", file=sqlf)
for objcsop in sorted(ocs):
    if objcsop in ocs3D:
        dim=3
    else:
        dim=2
    print(dtf.insertsorok(objcsop, args.tbl_elotag+objcsop+args.tbl_utotag, objdim=dim, geomnev=args.geom_neve, tobbgeom=tobbgeom,  ptcol=args.ptgeom_neve), file=sqlf)
print("COMMIT;", file=sqlf)
sqlf.close()
