key = 'l.akT6fMzi5gG'
grupo = 6
'''
#desarrollo
recepcion = "5cbd3ce444f67600049431d1"
despacho = '5cbd3ce444f67600049431d2'
almacen_general1 = '5cbd3ce444f67600049431d3'
almacen_general2 = '5cbd3ce444f67600049431d4'
pulmon = '5cbd3ce444f67600049431d5'
cocina = '5cbd3ce444f67600049431d6'
'''

#Produccion
recepcion = '5cc7b139a823b10004d8e6eb'
despacho = '5cc7b139a823b10004d8e6ec'
almacen_general1 = '5cc7b139a823b10004d8e6ed'
almacen_general2 = '5cc7b139a823b10004d8e6ee'
pulmon = '5cc7b139a823b10004d8e6ef'
cocina = '5cc7b139a823b10004d8e6f0'




lotes_minimos_materia_prima_propia = 20
lotes_minimos_materia_prima_ajena = 10
delta_stock_minimo = 2

almacenes_nuestro = [recepcion, despacho, almacen_general2, almacen_general1, pulmon, cocina]


skus_propios = ['1001', '1002', '1003','1007','1016']
skus_grupos = ['1004', '1005', '1006', '1008', '1009', '1010', '1011', '1012', '1013', '1014', '1015']
skus_produccion_propia = ['1107', '1207', '1307', '1407', '1116', '1216']

stock_minimo= {
                '1301' : 50,
                '1013' : 300,
                '1310' : 20,
                '1201' :250,
                '1209':20,
                '1109':50,
                '1309' :170,
                '1106' : 400,
                '1114' : 50,
                '1215' :20,
                '1115' : 30,
                '1105' :50,
                '1216' : 50,
                '1116' :250,
                '1110' :80,
                '1210' :150,
                '1112' : 130,
                '1108' :10,
                '1407': 40,
                '1207':20,
                '1107' :50,
                '1307' :170,
                '1211' :60
                }


produccion_otros = {
                    '1004' :[ '3','4','10'],
                    '1005' :[ '4','5','8'],
                    '1006' :['2','5','7'],
                    '1008' :[ '1','5','7'],
                    '1009' :[ '1','8','9'],
                    '1010' :['3','9','13'],
                    '1011' :[ '2','10','11'],
                    '1012' :['11','12','13'],
                    '1013' :[ '10','12','14'],
                    '1014' :[ '3','4','9'],
                    '1015' :[ '1','12','14'],
                    }


recetas = {
            '1101':{'1001': 8.0,'1003': 3.0,'1004': 2.0,'1002': 4.0},
            '1301':{'1101': 1.0},
            '1105':{'1005': 1.0},
            '1106':{'1006': 1.0},
            '1107':{'1007': 1.0},
            '1108':{'1008': 1.0},
            '1109':{'1009': 1.0},
            '1110':{'1010': 1.0},
            '1111':{'1011': 2.0},
            '1211':{'1111': 1.0},
            '1112':{'1012': 1.0},
            '1114':{'1014': 1.0},
            '1115':{'1015': 2.0},
            '1116':{'1016': 11.0},
            '1201':{'1101': 1.0},
            '1207':{'1007': 1.0},
            '1209':{'1009': 1.0},
            '1210':{'1010': 1.0},
            '1215':{'1015': 4.0},
            '1216':{'1016': 2.0},
            '1307':{'1007': 1.0},
            '1309':{'1009': 1.0},
            '1310':{'1010': 1.0},
            '1407':{'1007': 1.0},
            }

unidades_por_lote = {
                    '1001': 10,
                    '1002': 10,
                    '1003': 100,
                    '1004': 100,
                    '1005': 5,
                    '1006': 1,
                    '1007': 8,
                    '1008': 10,
                    '1009': 3,
                    '1010': 5,
                    '1011': 4,
                    '1012': 7,
                    '1013': 10,
                    '1014': 5,
                    '1015': 4,
                    '1016': 8,
                    '1101':10,
                    '1105':10,
                    '1106':100,
                    '1107':11,
                    '1108':6,
                    '1109':12,
                    '1110':6,
                    '1111':2,
                    '1112':20,
                    '1114':4,
                    '1115':8,
                    '1116':10,
                    '1201': 10,
                    '1207': 12,
                    '1209': 14,
                    '1210': 9,
                    '1211':10,
                    '1215':8,
                    '1216':10,
                    '1301':5,
                    '1307':11,
                    '1309':11,
                    '1310':12,
                    '1407':14,
                    }


nombres = {
            '1001':	'Arroz grano corto',
'1002':	'Vinagre de arroz',
'1003':	'Azúcar',
'1004':	'Sal',
'1005':	'Kanikama entero',
'1006':	'Camarón',
'1007': 'Filete de salmón',
'1008': 'Filete de salmón ahumado',
'1009': 'Filete de atún',
'1010': 'Palta',
'1011': 'Sésamo',
'1012': 'Queso crema',
'1013': 'Masago',
'1014': 'Cebollín entero',
'1015': 'Ciboulette entero',
'1016': 'Nori entero',
'1101': 'Arroz cocido',
'1105': 'Kanikama para roll',
'1106': 'Camarón cocido',
'1107': 'Salmón cortado para roll',
'1108': 'Salmón ahumado cortado para roll',
'1109': 'Atún cortado para roll',
'1110': 'Palta cortada para envoltura',
'1111': 'Sésamo tostado',
'1112': 'Queso crema para roll',
'1114': 'Cebollín cortado para roll',
'1115': 'Ciboulette picado para roll',
'1116': 'Nori entero cortado para roll',
'1201': 'Arroz cocido para roll',
'1207': 'Salmón cortado para nigiri',
'1209': 'Atún cortado para nigiri',
'1210': 'Palta cortada para roll',
'1211': 'Sésamo tostado para envoltura',
'1215': 'Ciboulette picado para envoltura',
'1216': 'Nori entero cortado para nigiri',
'1301': 'Arroz cocido para nigiri',
'1307': 'Salmón cortado para sashimi',
'1309': 'Atún cortado para sashimi',
'1310': 'Palta cortada para nigiri',
'1407': 'Salmón cortado para envoltura',

            }
