DayOfWeek = (
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miercoles', 'Miercoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sabado', 'Sabado'),
    ('Domingo', 'Domingo'),
)

Hour = tuple([("%d:%s" % (x / 60, "00" if x % 60 == 0 else x % 60),
               "%d:%s" % (x / 60, "00" if x % 60 == 0 else x % 60))
              for x in range(0, 96 * 15, 15)])
