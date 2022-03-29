import inspect


class OptionsKeys:
    ts_select = 'ts_select'
    ts_target = 'ts_target'
    value_range = 'value_range'
    ts_labels = 'ts_labels'
    ts_enable = 'ts_enable'


class Colors:

    class Favorites:
        black = 'black'
        blue = 'blue'
        brown = 'brown'
        cyan = 'cyan'
        darkblue = 'darkblue'
        darkcyan = 'darkcyan'
        darkgreen = 'darkgreen'
        darkmagenta = 'darkmagenta'
        darkorange = 'darkorange'
        darkorchid = 'darkorchid'
        darkred = 'darkred'
        darkviolet = 'darkviolet'
        gold = 'gold'
        magenta = 'magenta'
        maroon = 'maroon'
        orange = 'orange'
        purple = 'purple'
        red = 'red'

        @classmethod
        def get_list(cls):
            return [c[0] for c in filter(lambda m: not m[0].startswith('_') and type(m[1]) == str,
                                         inspect.getmembers(cls))]

    # aliceblue
    # antiquewhite
    # aqua
    # aquamarine
    # azure
    # beige
    # bisque
    black = 'black'
    # blanchedalmond
    blue = 'blue'
    # blueviolet
    brown = 'brown'
    # burlywood
    # cadetblue
    # chartreuse
    # chocolate
    # coral
    # cornflowerblue
    # cornsilk
    # crimson
    cyan = 'cyan'
    darkblue = 'darkblue'
    darkcyan = 'darkcyan'
    # darkgoldenrod
    darkgray = 'darkgray'
    darkgreen = 'darkgreen'
    darkgrey = 'darkgrey'
    # darkkhaki
    darkmagenta = 'darkmagenta'
    # darkolivegreen
    darkorange = 'darkorange'
    darkorchid = 'darkorchid'
    darkred = 'darkred'
    darksalmon = 'darksalmon'
    # darkseagreen
    # darkslateblue
    # darkslategray
    # darkslategrey
    # darkturquoise
    darkviolet = 'darkviolet'
    # deeppink
    # deepskyblue
    # dimgray
    # dimgrey
    # dodgerblue
    # firebrick
    # floralwhite
    # forestgreen
    # fuchsia
    # gainsboro
    # ghostwhite
    gold = 'gold'
    # goldenrod
    gray = 'gray'
    green = 'green'
    greenyellow = 'greenyellow'
    grey = 'grey'
    # honeydew
    # hotpink
    # indianred
    # indigo
    # ivory
    # khaki
    # lavender
    # lavenderblush
    # lawngreen
    # lemonchiffon
    lightblue = 'lightblue'
    # lightcoral
    lightcyan = 'lightcyan'
    lightgoldenrodyellow = 'lightgoldenrodyellow'
    # lightgray
    lightgreen = 'lightgreen'
    lightgrey = 'lightgrey'
    lightpink = 'lightpink'
    lightsalmon = 'lightsalmon'
    # lightseagreen
    # lightskyblue
    # lightslategray
    # lightslategrey
    lightsteelblue = 'lightsteelblue'
    lightyellow = 'lightyellow'
    lime = 'lime'
    limegreen = 'limegreen'
    # linen
    magenta = 'magenta'
    maroon = 'maroon'
    # mediumaquamarine
    # mediumblue
    # mediumorchid
    # mediumpurple
    # mediumseagreen
    # mediumslateblue
    # mediumspringgreen
    # mediumturquoise
    # mediumvioletred
    # midnightblue
    # mintcream
    # mistyrose
    # moccasin
    # navajowhite
    # navy
    # oldlace
    # olive
    # olivedrab
    orange= 'orange'
    # orangered
    # orchid
    palegoldenrod = 'palegoldenrod'
    # palegreen
    # paleturquoise
    # palevioletred
    # papayawhip
    # peachpuff
    # peru
    pink = 'pink'
    # plum
    # powderblue
    purple = 'purple'
    red = 'red'
    # rosybrown
    # royalblue
    # saddlebrown
    salmon = 'salmon'
    # sandybrown
    # seagreen
    # seashell
    # sienna
    silver = 'silver'
    # skyblue
    # slateblue
    # slategray
    # slategrey
    # snow
    # springgreen
    steelblue = 'steelblue'
    # tan
    # teal
    # thistle
    # tomato
    # transparent
    # turquoise
    violet = 'violet'
    # wheat
    # white
    # whitesmoke
    yellow = 'yellow'
    yellowgreen = 'yellowgreen'

    FULL_LIST = [
        'aliceblue',
        'antiquewhite',
        'aqua',
        'aquamarine',
        'azure',
        'beige',
        'bisque',
        'black',
        'blanchedalmond',
        'blue',
        'blueviolet',
        'brown',
        'burlywood',
        'cadetblue',
        'chartreuse',
        'chocolate',
        'coral',
        'cornflowerblue',
        'cornsilk',
        'crimson',
        'cyan',
        'darkblue',
        'darkcyan',
        'darkgoldenrod',
        'darkgray',
        'darkgreen',
        'darkgrey',
        'darkkhaki',
        'darkmagenta',
        'darkolivegreen',
        'darkorange',
        'darkorchid',
        'darkred',
        'darksalmon',
        'darkseagreen',
        'darkslateblue',
        'darkslategray',
        'darkslategrey',
        'darkturquoise',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'dimgray',
        'dimgrey',
        'dodgerblue',
        'firebrick',
        'floralwhite',
        'forestgreen',
        'fuchsia',
        'gainsboro',
        'ghostwhite',
        'gold',
        'goldenrod',
        'gray',
        'green',
        'greenyellow',
        'grey',
        'honeydew',
        'hotpink',
        'indianred',
        'indigo',
        'ivory',
        'khaki',
        'lavender',
        'lavenderblush',
        'lawngreen',
        'lemonchiffon',
        'lightblue',
        'lightcoral',
        'lightcyan',
        'lightgoldenrodyellow',
        'lightgray',
        'lightgreen',
        'lightgrey',
        'lightpink',
        'lightsalmon',
        'lightseagreen',
        'lightskyblue',
        'lightslategray',
        'lightslategrey',
        'lightsteelblue',
        'lightyellow',
        'lime',
        'limegreen',
        'linen',
        'magenta',
        'maroon',
        'mediumaquamarine',
        'mediumblue',
        'mediumorchid',
        'mediumpurple',
        'mediumseagreen',
        'mediumslateblue',
        'mediumspringgreen',
        'mediumturquoise',
        'mediumvioletred',
        'midnightblue',
        'mintcream',
        'mistyrose',
        'moccasin',
        'navajowhite',
        'navy',
        'oldlace',
        'olive',
        'olivedrab',
        'orange',
        'orangered',
        'orchid',
        'palegoldenrod',
        'palegreen',
        'paleturquoise',
        'palevioletred',
        'papayawhip',
        'peachpuff',
        'peru',
        'pink',
        'plum',
        'powderblue',
        'purple',
        'red',
        'rosybrown',
        'royalblue',
        'saddlebrown',
        'salmon',
        'sandybrown',
        'seagreen',
        'seashell',
        'sienna',
        'silver',
        'skyblue',
        'slateblue',
        'slategray',
        'slategrey',
        'snow',
        'springgreen',
        'steelblue',
        'tan',
        'teal',
        'thistle',
        'tomato',
        'transparent',
        'turquoise',
        'violet',
        'wheat',
        'white',
        'whitesmoke',
        'yellow',
        'yellowgreen'
    ]

