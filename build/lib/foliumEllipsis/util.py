import requests
from uuid import UUID
def validUuid(name, value, required):
    if not required and type(value) == type(None):
        return
    try:
        UUID(value, version=2)
    except:
        raise ValueError(name + ' must be of type string and be a uuid')
    return(value)

def validString(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type('x'):
        raise ValueError(name + 'must be of type string')
    return(value)

def get(url, token):

    if type(token) != type(None):
        if not '?' in url:
            url = url + '?token=' + token
        else:
            url = url + '&token=' + token
    if type(token) == type(None):
        r = requests.get(url)
    else:
        r = requests.get(url,  headers = {"Authorization": 'Bearer ' + token})
    if r.status_code != 200:
        raise ValueError(r.text)

    r = r.json()
    return r


def createStyleFunction(style, styleSheet):
    if style['method'] == 'fromColorProperty':
        functionString = '''function(f) {

                if(f.color){

                return {
                  "fill": true,
                  "weight": ''' + str(style['parameters']['width']) + ''',
                  "fillColor": f.color,
                  "color": f.color,
                  "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
                  "opacity":1
                };
                }else{
                return {
                  "fill": true,
                  "weight": ''' + str(style['parameters']['width']) + ''',
                  "fillColor": "''' + style['parameters']['defaultColor'] + '''",
                  "color": "''' + style['parameters']['defaultColor'] + '''",
                  "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
                  "opacity":1
                };

                }



            }'''

    if style['method'] == 'random':
        arr = [x for x in styleSheet['layers'] if x['type'] == 'fill'][0]['paint']['fill-color']
        arr = arr[2:len(arr) - 1]
        p = style['parameters']['property']
        values = []
        colors = []
        for i in range(len(arr)):
            if i % 2 == 0:
                values = values + [arr[i]]
            else:
                colors = colors + [arr[i]]

        ifs = ['if( f.' + p + '==' + str(x) + ')' for x in values]

        styles = ['''{
              "fill": true,
              "weight": ''' + str(style['parameters']['width']) + ''',
              "fillColor": "''' + c + '''",
              "color": "''' + c + '''",
              "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
              "opacity": 1
            }''' for c in colors]

        functionString = 'function(f){'
        i = 0
        for i in range(len(ifs)):
            functionString = functionString + ifs[i] + '{ return(' + styles[i] + ');}'

        functionString = functionString + '}'

    if style['method'] == 'singleColor':
        functionString = '''function(f) {
                return {
                  "fill": true,
                  "weight": ''' + str(style['parameters']['width']) + ''',
                  "fillColor": "''' + style['parameters']['color'] + '''",
                  "color": "''' + style['parameters']['color'] + '''",
                  "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
                  "opacity":1
                };      
            }'''
    if style['method'] == 'rules':
        rules = style['parameters']['rules']

        for i in range(len(rules)):
            if rules[i]['operator'] == '=':
                rules[i]['operator'] = '==='

        ifs = ['if( f.' + x['property'] + x['operator'] + str(x['value']) + ')' for x in rules]

        styles = ['''{
              "fill": true,
              "weight": ''' + str(style['parameters']['width']) + ''',
              "fillColor": "''' + x['color'] + '''",
              "color": "''' + x['color'] + '''",
              "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
              "opacity": 1
            }''' for x in rules]

        ifs = ifs + ['else']

        styles = styles + ['''{
              "fill": true,
              "weight": ''' + str(style['parameters']['width']) + ''',
              "fillColor": "''' + style['parameters']['defaultColor'] + '''",
              "color": "''' + style['parameters']['defaultColor'] + '''",
              "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
              "opacity": 1
            }''']

        functionString = 'function(f){'
        i = 0
        for i in range(len(ifs)):
            functionString = functionString + ifs[i] + '{ return(' + styles[i] + ');}'

        functionString = functionString + '}'

    if style['method'] == 'transitionPoints':
        transitionPoints = style['parameters']['transitionPoints']
        p = style['parameters']['property']
        ifs = ['if( f.' + p + '<' + str(x['value']) + ')' for x in transitionPoints]
        ifs[len(ifs) - 1] = 'else'

        styles = ['''{
              "fill": true,
              "weight": ''' + str(style['parameters']['width']) + ''',
              "fillColor": "''' + x['color'] + '''",
              "color": "''' + x['color'] + '''",
              "fillOpacity":''' + str(style['parameters']['alpha']) + ''',
              "opacity": 1
            }''' for x in transitionPoints]

        functionString = 'function(f){'
        i = 0
        for i in range(len(ifs)):
            functionString = functionString + ifs[i] + '{ return(' + styles[i] + ');}'

        functionString = functionString + '}'

    functionString = functionString.replace('\n', '')
    functionString = functionString.replace(' ', '')

    return functionString
