events = {
    'atl_100m': {
        'name': "100 metros planos",
        'sex': ['male', 'female'],
    },
    'atl_200m': {
        'name': '200 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_400m': {
        'name': '400 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_800m': {
        'name': '800 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_1500m': {
        'name': '1500 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_5000m': {
        'name': '5000 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_10000m': {
        'name': '10000 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_100v': {
        'name': '100 metros con vallas',
        'sex': ['female'],
    },
    'atl_110v': {
        'name': '110 metros con vallas',
        'sex': ['male'],
    },
    'atl_400v': {
        'name': '400 metros con vallas',
        'sex': ['male', 'female'],
    },
    'atl_3000m': {
        'name': '3000 metros con obstáculos',
        'sex': ['male', 'female'],
    },
    'atl_alt': {
        'name': 'Salto de altura',
        'sex': ['male', 'female'],
    },
    'atl_per': {
        'name': 'Salto con pértiga',
        'sex': ['male', 'female'],
    },
    'atl_lar': {
        'name': 'Salto largo',
        'sex': ['male', 'female'],
    },
    'atl_tri': {
        'name': 'Salto triple',
        'sex': ['male', 'female'],
    },
    'atl_bal': {
        'name': 'Lanzamiento de la bala',
        'sex': ['male', 'female'],
    },
    'atl_dis': {
        'name': 'Lanzamiento del disco',
        'sex': ['male', 'female'],
    },
    'atl_mar': {
        'name': 'Lanzamiento del martillo',
        'sex': ['male', 'female'],
    },
    'atl_jab': {
        'name': 'Lanzamiento de la jabalina',
        'sex': ['male', 'female'],
    },
    'atl_mat': {
        'name': 'Maratón',
        'sex': ['male', 'female'],
    },
    'atl_20km': {
        'name': 'Marcha 20 kilómetros',
        'sex': ['male', 'female'],
    },
    'atl_35km': {
        'name': 'Marcha 35 kilómetros',
        'sex': ['male', 'female'],
    },
    'atl_hep': {
        'name': 'Heptatlón',
        'sex': ['female'],
    },
    'atl_dec': {
        'name': 'atl_dec',
        'sex': ['male'],
    },
    'atl_4x100m': {
        'name': 'Relevo 4x100 metros planos',
        'sex': ['male', 'female'],
    },
    'atl_4x400m': {
        'name': 'Relevo 4x400 metros planos',
        'sex': ['male', 'female', 'mixed'],
    },
}


maximize_events = [
    'atl_alt', 'atl_per', 
    'atl_lar', 'atl_tri',
    'atl_bal', 'atl_dis', 
    'atl_jab', 'atl_mar',
    'atl_hep', 'atl_dec'
]


events_in_groups = [ 
    'atl_4x100m', 
    'atl_4x400m' 
]


event_params = {
    'atl_800m':{
        'female':{
            'alpha': 0,
            'bw': 1.5,
            'sim_times': 5000,
        }
    },
    'atl_tri':{
        'male':{
            'alpha': 0,
            'bw': 0.2,
            #'sim_times': None,
        }
    },
    'atl_dis':{
        'male':{
            'alpha': 0,
            'bw': 2,
            #'sim_times': 5000,
        }
    },
    'atl_mar':{
        'male':{
            'alpha': 0,
            'bw': None,
            # 'sim_times': None,
        },
        'male':{
            'alpha': 0,
            'bw': None,
            # 'sim_times': None,
        }
    },
    'atl_jab':{
        'male':{
            'alpha': 0,
            'bw': 1.6,
            #'sim_times': 5000,
        },        
        'female':{
            'alpha': 0,
            'bw': 1.6,
            # 'sim_times': None,
        }
    },
    'atl_400m':{
        'female':{
            'alpha': 0,
            'bw': 0.8,
            #'sim_times': 5000,
        }
    },
    'atl_4x400m':{
        'male':{
            'alpha': 1.3,
            'bw': 0.5,
            # 'sim_times': 6000,
        },
        'female':{
            'alpha': 1.3,
            'bw': 0.5,
            # 'sim_times': 6000,
        },
        'mixed':{
            'alpha': 0,
            'bw': 2,
            # 'sim_times': 6000,
        }
    },
    
    'atl_4x100m':{
        'male':{
            'alpha': 1.3,
            'bw': 1,
            #'sim_times': 5000,
        },
        'female':{
            'alpha': 1.3,
            'bw': 0.5,
            # 'sim_times': 6000,
        }
    },
    'atl_5000m':{
        'female':{
            'alpha': 1.3,
            'bw': 17,
            #'sim_times': 5,
        }
    },
    'atl_3000m':{
        'male':{
            'alpha': 1.3,
            'bw': None,
            #'sim_times': 7000,
        }
    },
    'atl_lar':{
        'male':{
            'alpha': 1.3,
            'bw': None,
            #'sim_times': 5000,
        }
    },
    'atl_100m':{
        'male':{
            'alpha': 0,
            'bw': None,
            #'sim_times': 5000,
        }
    },
    'atl_800m':{
        'male':{
            'alpha': 1.3,
            'bw': None,
            #'sim_times': 7000,
        }
    },
    'atl_per':{
        'female':{
            'alpha': 0,
            'bw': None,
            #'sim_times': 5000,
        }
    },
    'atl_10000m':{
        'female':{
            'alpha': 0,
            'bw': 10,
            #'sim_times': 5000,
        }
    },
    'atl_mat':{
        'female':{
            'alpha': 0,
            'bw': None,
            'sim_times': 5000,
        },
        'male':{
            'alpha': 0,
            'bw': None,
            'sim_times': 5000,
        }
    }
}