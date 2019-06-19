key = 'l.akT6fMzi5gG'
grupo = 6

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
'''

ambiente = 'dev'

lotes_minimos_materia_prima_propia = 4
lotes_minimos_materia_prima_ajena = 2
lotes_minimos_despacho = 3
delta_stock_minimo = 1.5

despacho_maximo = 30

almacenes_nuestro = [recepcion, despacho, almacen_general2, almacen_general1, pulmon, cocina]


skus_propios = ['1001', '1002', '1003', '1005', '1007', '1012', '1015', '1016']

stock_minimo = {
                '1301': 50,
                '1013': 300,
                '1310': 20,
                '1201': 250,
                '1209': 20,
                '1109': 50,
                '1309': 170,
                '1106': 400,
                '1114': 50,
                '1215': 20,
                '1115': 30,
                '1105': 50,
                '1216': 50,
                '1116': 250,
                '1110': 80,
                '1210': 150,
                '1112': 130,
                '1108': 10,
                '1407': 40,
                '1207': 20,
                '1107': 50,
                '1307': 170,
                '1211': 60
                }

stock_deseado_productos_intermedios = {
                                        '1101': 150,
                                        '1111': 50,
                                     }


produccion_otros = {
                    '1004': ['3', '4', '9', '10', '13', '14'],
                    '1006': ['2', '3', '4', '5', '7', '8'],
                    '1008': ['1', '5', '7', '9', '10', '14'],
                    '1009': ['1', '4', '8', '9', '12', '14'],
                    '1010': ['1', '2', '3', '9', '10', '13'],
                    '1011': ['2', '5', '7', '10', '11', '12'],
                    '1013': ['7', '9', '10', '11', '13', '14'],
                    '1014': ['2', '3', '4', '5', '8', '11'],
                    }


recetas = {
            '1101': {'1001': 8.0, '1003': 3.0, '1004': 2.0, '1002': 4.0},
            '1105': {'1005': 1.0},
            '1106': {'1006': 1.0},
            '1107': {'1007': 1.0},
            '1108': {'1008': 1.0},
            '1109': {'1009': 1.0},
            '1110': {'1010': 1.0},
            '1111': {'1011': 2.0},
            '1211': {'1111': 1.0},
            '1112': {'1012': 1.0},
            '1114': {'1014': 1.0},
            '1115': {'1015': 2.0},
            '1116': {'1016': 11.0},
            '1201': {'1101': 1.0},
            '1207': {'1007': 1.0},
            '1209': {'1009': 1.0},
            '1210': {'1010': 1.0},
            '1215': {'1015': 4.0},
            '1216': {'1016': 2.0},
            '1301': {'1101': 1.0},
            '1307': {'1007': 1.0},
            '1309': {'1009': 1.0},
            '1310': {'1010': 1.0},
            '1407': {'1007': 1.0},
            '10001': {'1201': 1.0, '1105': 1.0, '1210': 1.0, '1211': 1.0, '1116': 1.0},
            '10002': {'1201': 1.0, '1105': 1.0, '1013': 5.0, '1210': 1.0, '1116': 1.0},
            '10003': {'1201': 1.0, '1105': 1.0, '1013': 5.0, '1210': 1.0, '1211': 1.0, '1116': 1.0},
            '10004': {'1201': 1.0, '1106': 4.0, '1210': 1.0, '1211': 1.0, '1116': 1.0},
            '10005': {'1201': 1.0, '1106': 4.0, '1013': 5.0, '1210': 1.0, '1116': 1.0},
            '10006': {'1201': 1.0, '1210': 1.0, '1207': 1.0, '1211': 1.0, '1116': 1.0},
            '10007': {'1201': 1.0, '1013': 5.0, '1210': 1.0, '1107': 1.0, '1116': 1.0},
            '10008': {'1201': 1.0, '1109': 1.0, '1210': 1.0, '1211': 1.0, '1116': 1.0},
            '10009': {'1201': 1.0, '1109': 1.0, '1013': 5.0, '1210': 1.0, '1116': 1.0},
            '10010': {'1201': 1.0, '1106': 4.0, '1210': 1.0, '1110': 1.0, '1116': 1.0},
            '10011': {'1201': 1.0, '1106': 4.0, '1114': 1.0, '1110': 1.0, '1112': 1.0, '1116': 1.0},
            '10012': {'1201': 1.0, '1106': 4.0, '1110': 1.0, '1112': 1.0, '1108': 1.0, '1116': 1.0},
            '10013': {'1201': 1.0, '1106': 4.0, '1110': 1.0, '1112': 1.0, '1116': 1.0},
            '10014': {'1201': 1.0, '1105': 1.0, '1110': 1.0, '1112': 1.0, '1116': 1.0},
            '10015': {'1201': 1.0, '1109': 1.0, '1115': 1.0, '1110': 1.0, '1112': 1.0, '1116': 1.0},
            '10016': {'1201': 1.0, '1106': 4.0, '1110': 1.0, '1112': 1.0, '1107': 1.0, '1116': 1.0},
            '10017': {'1201': 1.0, '1110': 1.0, '1112': 1.0, '1107': 1.0, '1116': 1.0},
            '10018': {'1201': 1.0, '1105': 1.0, '1112': 1.0, '1407': 1.0, '1116': 1.0},
            '10019': {'1201': 1.0, '1106': 4.0, '1210': 1.0, '1116': 1.0, '1407': 1.0},
            '10020': {'1201': 1.0, '1116': 1.0, '1106': 4.0, '1112': 1.0, '1114': 1.0, '1407': 1.0},
            '10021': {'1201': 1.0, '1116': 1.0, '1109': 1.0, '1114': 1.0, '1407': 1.0},
            '10022': {'1201': 1.0, '1116': 1.0, '1107': 1.0, '1112': 1.0, '1210': 1.0, '1215': 1.0},
            '10023': {'1201': 1.0, '1116': 1.0, '1109': 1.0, '1112': 1.0, '1210': 1.0, '1215': 1.0},
            '10024': {'1201': 1.0, '1116': 1.0, '1210': 1.0, '1114': 1.0, '1115': 1.0, '1211': 1.0},
            '10025': {'1201': 1.0, '1116': 1.0, '1210': 1.0, '1114': 1.0, '1115': 1.0, '1013': 5.0},
            '20001': {'1301': 1.0, '1207': 1.0, '1310': 1.0, '1112': 1.0, '1216': 1.0},
            '20002': {'1301': 1.0, '1216': 1.0, '1106': 4.0},
            '20003': {'1301': 1.0, '1216': 1.0, '1207': 1.0},
            '20004': {'1301': 1.0, '1216': 1.0, '1209': 1.0},
            '20005': {'1301': 1.0, '1216': 1.0, '1209': 1.0, '1310': 1.0},
            '30001': {'1307': 3.0},
            '30002': {'1307': 4.0},
            '30003': {'1307': 5.0},
            '30004': {'1309': 3.0},
            '30005': {'1309': 4.0},
            '30006': {'1309': 5.0},
            '30007': {'1309': 2.0, '1307': 2.0},
            '30008': {'1309': 3.0, '1307': 3.0},

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
                    '1101': 10,
                    '1105': 10,
                    '1106': 100,
                    '1107': 11,
                    '1108': 6,
                    '1109': 12,
                    '1110': 6,
                    '1111': 2,
                    '1112': 20,
                    '1114': 4,
                    '1115': 8,
                    '1116': 10,
                    '1201': 10,
                    '1207': 12,
                    '1209': 14,
                    '1210': 9,
                    '1211': 10,
                    '1215': 8,
                    '1216': 10,
                    '1301': 5,
                    '1307': 11,
                    '1309': 11,
                    '1310': 12,
                    '1407': 14,
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

# Desarollo
id_grupos = {
            1: '5cbd31b7c445af0004739be3',
            2: '5cbd31b7c445af0004739be4',
            3: '5cbd31b7c445af0004739be5',
            4: '5cbd31b7c445af0004739be6',
            5: '5cbd31b7c445af0004739be7',
            6: '5cbd31b7c445af0004739be8',
            7: '5cbd31b7c445af0004739be9',
            8: '5cbd31b7c445af0004739bea',
            9: '5cbd31b7c445af0004739beb',
            10: '5cbd31b7c445af0004739bec',
            11: '5cbd31b7c445af0004739bed',
            12: '5cbd31b7c445af0004739bee',
            13: '5cbd31b7c445af0004739bef',
            14: '5cbd31b7c445af0004739bf0',
            }
'''
# Produccion
id_grupos = {
            1: '5cc66e378820160004a4c3bc',
            2: '5cc66e378820160004a4c3bd',
            3: '5cc66e378820160004a4c3be',
            4: '5cc66e378820160004a4c3bf',
            5: '5cc66e378820160004a4c3c0',
            6: '5cc66e378820160004a4c3c1',
            7: '5cc66e378820160004a4c3c2',
            8: '5cc66e378820160004a4c3c3',
            9: '5cc66e378820160004a4c3c4',
            10: '5cc66e378820160004a4c3c5',
            11: '5cc66e378820160004a4c3c6',
            12: '5cc66e378820160004a4c3c7',
            13: '5cc66e378820160004a4c3c8',
            14: '5cc66e378820160004a4c3c9',
            }
'''





stock_minimal = {
                '1001': 8*20+20,
                '1002': 4*20+20,
                '1003': 3*20+20,
                '1004': 2*20,

                '1005': 1*30+20,

                '1006': 1*30,

                '1007': 1*30*4+20,


                '1008': 1*30,
                '1009': 1*30*3,
                '1010': 1*30*3,
                '1011': 1*30,
                '1012': 1*30+20,
                '1014': 1*30,
                '1015': 2*30*2+20,
                '1016': 11*30*20,


                '1101': 100,
                '1111': 30,
                '1301': 50*0.7,
                '1013': 300*0.7,
                '1310': 20*0.7,
                '1201': 250*0.7,
                '1209': 20*0.7,
                '1109': 50*0.7,
                '1309': 170*0.7,
                '1106': 400*0.7,
                '1114': 50*0.7,
                '1215': 20*0.7,
                '1115': 30*0.7,
                '1105': 50*0.7,
                '1216': 50*0.7,
                '1116': 250*0.7,
                '1110': 80*0.7,
                '1210': 150*0.7,
                '1112': 130*0.7,
                '1108': 10*0.7,
                '1407': 40*0.7,
                '1207': 20*0.7,
                '1107': 50*0.7,
                '1307': 170*0.7,
                '1211': 60*0.7,
                }