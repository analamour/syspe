columnas = [
    {
        'name': 'id',
        'type': 'INT',
        'length': 10,
        'primary_key': True,
        'auto_increment': True,
        'not_null': True
    },
    {
        'name': 'nombre',
        'type': 'VARCHAR',
        'length': 32,
        'primary_key': False,
        'auto_increment': False,
        'not_null': True
    },
    {
        'name': 'apellidos',
        'type': 'VARCHAR',
        'length': 64,
        'primary_key': False,
        'auto_increment': False,
        'not_null': True
    },
    {
        'name': 'telefono',
        'type': 'VARCHAR',
        'length': 9,
        'primary_key': False,
        'auto_increment': False,
        'not_null': False
    },
    {
        'name': 'direccion',
        'type': 'VARCHAR',
        'length': 128,
        'primary_key': False,
        'auto_increment': False,
        'not_null': False
    }
]
