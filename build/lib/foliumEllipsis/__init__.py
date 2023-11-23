import folium as f

#from folium_vectortilelayer import VectorTileLayer
from folium_vectorgrid import VectorGridProtobuf

import json
from foliumEllipsis.util import get
from foliumEllipsis.util import  createStyleFunction
from foliumEllipsis.util import validUuid
from foliumEllipsis.util import validString

#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*

__version__ = '0.0.5'
apiUrl = 'https://api.ellipsis-drive.com/v3'


def addEllipsisVectorLayer( pathId, layerName = 'layer', timestampId=None, style=None, zoom = None, token = None):
    pathId = validUuid('pathId', pathId, True )
    token = validString('token', token, False)

    metadata_url = apiUrl + '/path/' + pathId

    metadata = get(metadata_url, token)

    if type(timestampId) == type(None) or type(style) == type(None) or type(zoom) == type(None):
        if 'vector' != metadata['type']:
            raise ValueError('Given pathId is of type ' + metadata['type'] + ' but must be of type vector.')
        ts = [x for x in metadata['vector']['timestamps'] if x['status'] == 'active']
        if type(timestampId) == type(None):
            if len(ts) == 0:
                raise ValueError('This layer does not contain any active timestamps.')
            timestampId = ts[0]['id']
        t = [t for t in metadata['vector']['timestamps'] if t['id'] == timestampId  ][0]
        if t['status'] != 'active':
            raise ValueError('Given timestamp is not active')
        if not t['precompute']['hasVectorTiles']:
            raise ValueError('vector tiles are still being computed, please wait a few more moments.')
        if type(zoom) == type(None):
            zoom = t['precompute']['vectorTileZoom']
        if type(style) == type(None):
            style = [ s for s in metadata['vector']['styles'] if s['default']][0]['id']



    timestampId = validUuid('timestampId', timestampId, True )
    styleFromUuid = None
    try:
        validUuid('style', pathId, True )
        styleFromUuid = True
    except:
        try:
            json.dumps(style)
            styleFromUuid = False
        except:
            raise ValueError("style must be either a uuid or json object")

    url = apiUrl + '/ogc/mvt/' + pathId + '/{z}/{x}/{y}?timestampId=' + timestampId

    if type(token) !=type(None):
        url = url + '&token=' + token


    if styleFromUuid:
        style = [s for s in metadata['vector']['styles'] if s['id'] == style]
        if len(style) == 0:
            raise ValueError('style id not found')

        style = style[0]

    styleSheet = None
    if style['method'] == 'random':
        style_url = apiUrl +  "/ogc/mvt/" + pathId + "/styleSheet?timestampId=" + timestampId + "&style=" + json.dumps(style) + "&zoom=21"
        styleSheet = get(style_url, token)

    functionString = createStyleFunction(style, styleSheet)
    options = '''{
      "layers": ["layer"],
    "minZoom": 0,
    "maxZoom": 21,
    "minDetailZoom": 0,
    "maxDetailZoom": ''' + str(zoom) + ''',            
      "vectorTileLayerStyles": {
        "layer": ''' + functionString +  '''
      }
    }'''
    vc = VectorGridProtobuf(url, layerName, options)
    return vc



def addEllipsisRasterLayer( pathId, timestampId=None, style=None, zoom = None, token = None):

    pathId = validUuid('pathId', pathId, True )
    token = validString('token', token, False)


    if type(timestampId) == type(None) or type(style) == type(None) or type(zoom) == type(None):
        metadata_url = apiUrl + '/path/' + pathId
        metadata = get(metadata_url, token)
        if 'raster' != metadata['type']:
            raise ValueError('Given pathId is of type ' + metadata['type'] + ' but must be of type raster.')
        ts = [x for x in metadata['raster']['timestamps'] if x['status'] == 'active']
        if type(timestampId) == type(None):
            if len(ts) == 0:
                raise ValueError('This layer does not contain any active timestamps.')
            timestampId = ts[0]['id']
        t = [t for t in metadata['raster']['timestamps'] if t['id'] == timestampId  ][0]
        if t['status'] != 'active':
            raise ValueError('Given timestamp is not active')
        if type(zoom) == type(None):
            zoom = t['zoom']
        if type(style) == type(None):
            style = [ s for s in metadata['raster']['styles'] if s['default']][0]['id']



    timestampId = validUuid('timestampId', timestampId, True )

    try:
        validUuid('style', pathId, True )
    except:
        try:
            json.dumps(style)
        except:
            raise ValueError("style must be either a uuid or json object")

    url = apiUrl + '/path/' + pathId + '/raster/timestamp/' + timestampId + '/tile/{z}/{x}/{y}?style=' + style

    if type(token) !=type(None):
        url = url + '&token=' + token
    raster_layer = f.raster_layers.TileLayer(tiles=url, attr='ED', max_native_zoom=zoom)

    return raster_layer



