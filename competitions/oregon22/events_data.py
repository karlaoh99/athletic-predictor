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
    'atl_800m':{
        'female':{
            'alpha': 0,
            'bandwidth': 1.5,
            'sim_times': 5000,
        }
    },
    'atl_tri':{
        'male':{
            'alpha': 0,
            'bandwidth': 0.2,
            #'sim_times': None,
        }
    },
    'atl_dis':{
        'male':{
            'alpha': 0,
            'bandwidth': 2,
            #'sim_times': 5000,
        }
    },
    'atl_mar':{
        'male':{
            'alpha': 0,
            'bandwidth': None,
            # 'sim_times': None,
        },
        'male':{
            'alpha': 0,
            'bandwidth': None,
            # 'sim_times': None,
        }
    },
    'atl_jab':{
        'male':{
            'alpha': 0,
            'bandwidth': 1.6,
            #'sim_times': 5000,
        },        
        'female':{
            'alpha': 0,
            'bandwidth': 1.6,
            # 'sim_times': None,
        }
    },
    'atl_400m':{
        'female':{
            'alpha': 0,
            'bandwidth': 0.8,
            #'sim_times': 5000,
        }
    },
    'atl_4x400m':{
        'male':{
            'alpha': 1.3,
            'bandwidth': 0.5,
            # 'sim_times': 6000,
        },
        'female':{
            'alpha': 1.3,
            'bandwidth': 0.5,
            # 'sim_times': 6000,
        },
        'mixed':{
            'alpha': 0,
            'bandwidth': 2,
            # 'sim_times': 6000,
        }
    },
    
    'atl_4x100m':{
        'male':{
            'alpha': 1.3,
            'bandwidth': 1,
            #'sim_times': 5000,
        },
        'female':{
            'alpha': 1.3,
            'bandwidth': 0.5,
            # 'sim_times': 6000,
        }
    },
    'atl_5000m':{
        'female':{
            'alpha': 1.3,
            'bandwidth': 17,
            #'sim_times': 5,
        }
    },
    'atl_3000m':{
        'male':{
            'alpha': 1.3,
            'bandwidth': None,
            #'sim_times': 7000,
        }
    },
    'atl_lar':{
        'male':{
            'alpha': 1.3,
            'bandwidth': None,
            #'sim_times': 5000,
        }
    },
    'atl_100m':{
        'male':{
            'alpha': 0,
            'bandwidth': None,
            #'sim_times': 5000,
        }
    },
    'atl_800m':{
        'male':{
            'alpha': 1.3,
            'bandwidth': None,
            #'sim_times': 7000,
        }
    },
    'atl_per':{
        'female':{
            'alpha': 0,
            'bandwidth': None,
            #'sim_times': 5000,
        }
    },
    'atl_10000m':{
        'female':{
            'alpha': 0,
            'bandwidth': 10,
            #'sim_times': 5000,
        }
    },
    'atl_mat':{
        'female':{
            'alpha': 0,
            'bandwidth': None,
            'sim_times': 5000,
        },
        'male':{
            'alpha': 0,
            'bandwidth': None,
            'sim_times': 5000,
        }
    }
}