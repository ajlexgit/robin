LOW_RESOLUTION = 1
HIGH_RESOLUTION = 2

# Разрешения экрана для селектбоксов
RESOLUTIONS = [
    (LOW_RESOLUTION, '17 дюймов'),
    (HIGH_RESOLUTION, '20 дюймов'),
]

# Максимальная ширина экрана для перехода на следующее разрешение (для JS)
RESOLUTION_WIDTHS = {
    LOW_RESOLUTION: (0, 1360),
    HIGH_RESOLUTION: (1361, None),
}