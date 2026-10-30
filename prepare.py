"""Regenera DATA a partir de CSV privado agregado por escola e GeoJSON público.
Uso: python3 prepare.py escolas.csv estados.geojson 2025 > data-block.js
Substituir no index.html o bloco const DATA = JSON.parse(...).
Sempre auditar os totais com a Sinopse da edição antes de publicar.
"""
import csv,json,sys,hashlib,pathlib
src=pathlib.Path(sys.argv[1]);geo=json.load(open(sys.argv[2]));year=int(sys.argv[3]);g={};n=0
for r in csv.DictReader(src.open()):
 vals=[int(r[f] or 0) for f in ['QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND','QT_MAT_MED']]
 if vals[0]<=0:continue
 uf=int(r['CO_UF']);cat=int(float(r['TP_CATEGORIA_ESCOLA_PRIVADA'] or 0));band=max(v for v in [0,100,300,500,1000] if vals[0]>=v);key=(uf,cat,band)
 if key not in g:g[key]=[uf,cat,band,0,0,0,0,0]
 for i,v in enumerate(vals):g[key][3+i]+=v
 g[key][7]+=1;n+=1
rows=list(g.values())
if year==2025:
 assert n==41746 and sum(r[3] for r in rows)==9245384
 ce=[r for r in rows if r[0]==23];assert sum(r[7] for r in ce)==1686 and sum(r[3] for r in ce)==399969
 br300=[r for r in rows if r[2]>=300];assert sum(r[7] for r in br300)==8873 and sum(r[5]+r[6] for r in br300)==4114450
 ce300=[r for r in ce if r[2]>=300];assert sum(r[7] for r in ce300)==402 and sum(r[5]+r[6] for r in ce300)==175593
else:raise ValueError('Nova edição: substituir verificações por totais auditados antes de gerar.')
states=[];paths=[]
for f in geo['features']:
 p=f['properties'];id=int(p['cd_geocuf']);states.append({'id':id,'uf':p['sigla'],'name':p['nome']});polys=f['geometry']['coordinates'];polys=polys if f['geometry']['type']=='MultiPolygon' else [polys];d=''
 for poly in polys:
  for ring in poly:d+='M'+'L'.join(f'{(p[0]+74)*12.4:.1f},{(5.5-p[1])*12.4:.1f}' for p in ring)+'Z'
 paths.append({'id':id,'d':d})
meta={'year':year,'verified':'2026-10-30','rows':n,'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source':'https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip','sinopse':'https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-basica'}
d=json.dumps({'states':sorted(states,key=lambda x:x['uf']),'paths':paths,'meta':meta,'groups':rows},ensure_ascii=False,separators=(',',':'))
print('const DATA = JSON.parse([\n'+',\n'.join(json.dumps(d[i:i+500],ensure_ascii=False) for i in range(0,len(d),500))+'\n].join(""));')
