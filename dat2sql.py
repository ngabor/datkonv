#!/usr/bin/env python3
"""
Program DAT adatcsere állományok adatainak
az OGC Simple Feature SQL szabványa szerint
működő adatbázisokba töltésére.
0.2 verzió
Nagy Gábor, 2015
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
parser.add_argument("--tobbgeom", default=False, help="kiterjedésenkénti külön geometriai oszlop ott, ahol többféle kiterjedése is lehet az objektumnak")
parser.add_argument("--geomidx", default='PostGIS', help="a geometriai index típusa")
args = parser.parse_args()

dtf=Datfile()
dtf.beolvas(args.datfile)

objcsopok=set(dtf.attr_nemures())-{'HA'}
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


sqlf=open(args.sqlfile,'w')
print("BEGIN;", file=sqlf)
for objcsop in sorted(ocs):
    if objcsop in ocs3D:
        dim=3
    else:
        dim=2
    print(dtf.createtbl(objcsop, args.tbl_elotag+objcsop+args.tbl_utotag, dim=dim, geomnev=args.geom_neve, tobbgeom=args.tobbgeom, geomindex=args.geomidx), file=sqlf)
    print(dtf.insertsorok(objcsop, args.tbl_elotag+objcsop+args.tbl_utotag, dim=dim, geomnev=args.geom_neve, tobbgeom=args.tobbgeom), file=sqlf)
print("COMMIT;", file=sqlf)
sqlf.close()
