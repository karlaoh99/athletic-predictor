events = {
    'atl_100m': {
        'name': "100 metros planos",
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_200m': {
        'name': '200 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_400m': {
        'name': '400 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_800m': {
        'name': '800 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_1500m': {
        'name': '1500 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_5000m': {
        'name': '5000 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_10000m': {
        'name': '10000 metros planos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_100v': {
        'name': '100 metros con vallas',
        'sex': ['female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_110v': {
        'name': '110 metros con vallas',
        'sex': ['male'],
        'maximize': False,
        'in_group': False,
    },
    'atl_400v': {
        'name': '400 metros con vallas',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_3000m': {
        'name': '3000 metros con obstáculos',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_alt': {
        'name': 'Salto de altura',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_per': {
        'name': 'Salto con pértiga',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_lar': {
        'name': 'Salto largo',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_tri': {
        'name': 'Salto triple',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_bal': {
        'name': 'Lanzamiento de la bala',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_dis': {
        'name': 'Lanzamiento del disco',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_mar': {
        'name': 'Lanzamiento del martillo',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_jab': {
        'name': 'Lanzamiento de la jabalina',
        'sex': ['male', 'female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_mat': {
        'name': 'Maratón',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_20km': {
        'name': 'Marcha 20 kilómetros',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_35km': {
        'name': 'Marcha 35 kilómetros',
        'sex': ['male', 'female'],
        'maximize': False,
        'in_group': False,
    },
    'atl_hep': {
        'name': 'Heptatlón',
        'sex': ['female'],
        'maximize': True,
        'in_group': False,
    },
    'atl_dec': {
        'name': 'atl_dec',
        'sex': ['male'],
        'maximize': True,
        'in_group': False,
    },
    # 'atl_4x100m': {
    #     'name': 'Relevo 4x100 metros planos',
    #     'sex': ['male', 'female'],
    #     'maximize': False,
    #     'in_group': True,
    # },
    # 'atl_4x400m': {
    #     'name': 'Relevo 4x400 metros planos',
    #     'sex': ['male', 'female', 'mixed'],
    #     'maximize': False,
    #     'in_group': True,
    # },
}

event_params = {
    "atl_dec": {
        "male": {
            "bandwidth": 228.03123232323233,
            "alpha": 0.02,
            "sim_times": 9000
        }
    },
    "atl_hep": {
        "female": {
            "bandwidth": 600.0007474747474,
            "alpha": 0.02,
            "sim_times": 6000
        }
    },
    "atl_35km": { ##### AUN NO SE HA CALCULADO
        "male": {
            "bandwidth": 1,
            "alpha": 0.01,
            "sim_times": 8000
        }
    },
    "atl_20km": {
        "male": {
            "bandwidth": 252.4098181818182,
            "alpha": 0.22,
            "sim_times": 6000
        },
        "female": {
            "bandwidth": 0.001,
            "alpha": 0.1,
            "sim_times": 2000
        }
    },
    "atl_mat": {
        "male": {
            "bandwidth": 1030.0,
            "alpha": 0.01,
            "sim_times": 1000
        },
        "female": {
            "bandwidth": 0.001,
            "alpha": 0.01,
            "sim_times": 1000
        }
    },
    "atl_jab": {
        "male": {
            "bandwidth": 14.532555555555556,
            "alpha": 0.08,
            "sim_times": 8000
        },
        "female": {
            "bandwidth": 9.861,
            "alpha": 0.61,
            "sim_times": 2000
        }
    },
    "atl_mar": {
        "male": {
            "bandwidth": 12.337858585858585,
            "alpha": 0.46,
            "sim_times": 4000
        },
        "female": {
            "bandwidth": 6.424575757575758,
            "alpha": 0.36,
            "sim_times": 5000
        }
    },
    "atl_lar": {
        "male": {
            "bandwidth": 1.5116464646464645,
            "alpha": 0.72,
            "sim_times": 9000
        },
        "female": {
            "bandwidth": 0.9482727272727274,
            "alpha": 0.6,
            "sim_times": 5000
        }
    },
    "atl_tri": {
        "male": {
            "bandwidth": 3.023222222222222,
            "alpha": 0.28,
            "sim_times": 5000
        },
        "female": {
            "bandwidth": 1.698151515151515,
            "alpha": 0.3,
            "sim_times": 9000
        }
    },
    "atl_bal": {
        "male": {
            "bandwidth": 8.000333333333334,
            "alpha": 0.84,
            "sim_times": 2000
        },
        "female": {
            "bandwidth": 3.1327979797979797,
            "alpha": 0.21,
            "sim_times": 4000
        }
    },
    "atl_dis": {
        "male": {
            "bandwidth": 12.941,
            "alpha": 0.81,
            "sim_times": 5000
        },
        "female": {
            "bandwidth": 10.169454545454544,
            "alpha": 0.04,
            "sim_times": 3000
        }
    },
    "atl_per": {
        "male": {
            "bandwidth": 0.9980202020202021,
            "alpha": 0.34,
            "sim_times": 10000
        },
        "female": {
            "bandwidth": 1.0056060606060606,
            "alpha": 0.27,
            "sim_times": 3000
        }
    },
    "atl_alt": {
        "male": {
            "bandwidth": 0.25839393939393934,
            "alpha": 0.22,
            "sim_times": 3000
        },
        "female": {
            "bandwidth": 0.24473737373737375,
            "alpha": 0.0,
            "sim_times": 9000
        }
    },
    "atl_3000m": {
        "male": {
            "bandwidth": 18.194161616161622,
            "alpha": 0.14,
            "sim_times": 6000
        },
        "female": {
            "bandwidth": 45.924737373737344,
            "alpha": 0.1,
            "sim_times": 10000
        }
    },
    "atl_400v": {
        "male": {
            "bandwidth": 4.8644343434343424,
            "alpha": 0.44,
            "sim_times": 7000
        },
        "female": {
            "bandwidth": 3.731151515151515,
            "alpha": 0.3,
            "sim_times": 4000
        }
    },
    "atl_110v": {
        "male": {
            "bandwidth": 4.4500101010101005,
            "alpha": 0.28,
            "sim_times": 10000
        }
    },
    "atl_100v": {
        "female": {
            "bandwidth": 0.42493939393939395,
            "alpha": 0.79,
            "sim_times": 1000
        }
    },
    "atl_10000m": {
        "male": {
            "bandwidth": 3.603606060606061,
            "alpha": 0.0,
            "sim_times": 1000
        },
        "female": {
            "bandwidth": 194.71809090909093,
            "alpha": 0.04,
            "sim_times": 8000
        }
    },
    "atl_5000m": {
        "male": {
            "bandwidth": 54.221626262626266,
            "alpha": 0.1,
            "sim_times": 9000
        },
        "female": {
            "bandwidth": 1.1547272727272724,
            "alpha": 0.21,
            "sim_times": 8000
        }
    },
    "atl_1500m": {
        "male": {
            "bandwidth": 12.228939393939392,
            "alpha": 0.01,
            "sim_times": 7000
        },
        "female": {
            "bandwidth": 22.235343434343438,
            "alpha": 0.29,
            "sim_times": 2000
        }
    },
    "atl_800m": {
        "male": {
            "bandwidth": 3.596414141414141,
            "alpha": 0.35000000000000003,
            "sim_times": 7000
        },
        "female": {
            "bandwidth": 0.6017979797979799,
            "alpha": 0.31,
            "sim_times": 10000
        }
    },
    "atl_400m": {
        "male": {
            "bandwidth": 0.001,
            "alpha": 0.21,
            "sim_times": 6000
        },
        "female": {
            "bandwidth": 1.3997777777777778,
            "alpha": 0.29,
            "sim_times": 6000
        }
    },
    "atl_200m": {
        "male": {
            "bandwidth": 1.3375555555555556,
            "alpha": 0.67,
            "sim_times": 7000
        },
        "female": {
            "bandwidth": 0.7990606060606062,
            "alpha": 0.04,
            "sim_times": 5000
        }
    },
    "atl_100m": {
        "male": {
            "bandwidth": 0.7606969696969698,
            "alpha": 0.52,
            "sim_times": 7000
        },
        "female": {
            "bandwidth": 0.5039696969696971,
            "alpha": 0.55,
            "sim_times": 7000
        }
    }
}

# event_params = {
#     'atl_800m':{
#         'female':{
#             'alpha': 0,
#             'bandwidth': 1.5,
#             'sim_times': 5000,
#         }
#     },
#     'atl_tri':{
#         'male':{
#             'alpha': 0,
#             'bandwidth': 0.2,
#             #'sim_times': None,
#         }
#     },
#     'atl_dis':{
#         'male':{
#             'alpha': 0,
#             'bandwidth': 2,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_mar':{
#         'male':{
#             'alpha': 0,
#             'bandwidth': None,
#             # 'sim_times': None,
#         },
#         'male':{
#             'alpha': 0,
#             'bandwidth': None,
#             # 'sim_times': None,
#         }
#     },
#     'atl_jab':{
#         'male':{
#             'alpha': 0,
#             'bandwidth': 1.6,
#             #'sim_times': 5000,
#         },        
#         'female':{
#             'alpha': 0,
#             'bandwidth': 1.6,
#             # 'sim_times': None,
#         }
#     },
#     'atl_400m':{
#         'female':{
#             'alpha': 0,
#             'bandwidth': 0.8,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_4x400m':{
#         'male':{
#             'alpha': 1.3,
#             'bandwidth': 0.5,
#             # 'sim_times': 6000,
#         },
#         'female':{
#             'alpha': 1.3,
#             'bandwidth': 0.5,
#             # 'sim_times': 6000,
#         },
#         'mixed':{
#             'alpha': 0,
#             'bandwidth': 2,
#             # 'sim_times': 6000,
#         }
#     },
    
#     'atl_4x100m':{
#         'male':{
#             'alpha': 1.3,
#             'bandwidth': 1,
#             #'sim_times': 5000,
#         },
#         'female':{
#             'alpha': 1.3,
#             'bandwidth': 0.5,
#             # 'sim_times': 6000,
#         }
#     },
#     'atl_5000m':{
#         'female':{
#             'alpha': 1.3,
#             'bandwidth': 17,
#             #'sim_times': 5,
#         }
#     },
#     'atl_3000m':{
#         'male':{
#             'alpha': 1.3,
#             'bandwidth': None,
#             #'sim_times': 7000,
#         }
#     },
#     'atl_lar':{
#         'male':{
#             'alpha': 1.3,
#             'bandwidth': None,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_100m':{
#         'male':{
#             'alpha': 0,
#             'bandwidth': None,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_800m':{
#         'male':{
#             'alpha': 1.3,
#             'bandwidth': None,
#             #'sim_times': 7000,
#         }
#     },
#     'atl_per':{
#         'female':{
#             'alpha': 0,
#             'bandwidth': None,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_10000m':{
#         'female':{
#             'alpha': 0,
#             'bandwidth': 10,
#             #'sim_times': 5000,
#         }
#     },
#     'atl_mat':{
#         'female':{
#             'alpha': 0,
#             'bandwidth': None,
#             'sim_times': 5000,
#         },
#         'male':{
#             'alpha': 0,
#             'bandwidth': None,
#             'sim_times': 5000,
#         }
#     }
# }