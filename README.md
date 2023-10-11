# Ellipsis Drive Python Package

This package helps you to add Ellipsis Drive layers to your Folium map.

You can install this package using

`pip install foliumEllipsis`


## Examples

### Raster layer

To add a raster layer you can use the following code:
```
import folium as f
from folium_vectortilelayer import VectorTileLayer
from foliumEllipsis import addEllipsisRasterLayer

map = f.Map()
pathId = '93e1c322-f21e-4395-9566-51abf473d2b9'
ED_layer = addEllipsisRasterLayer(pathId)
ED_layer.add_to(map)
map
```
### Vector layer
To add a vector layer you can use the following code

```
import folium as f
from folium_vectortilelayer import VectorTileLayer
from foliumEllipsis import addEllipsisVectorLayer

map = f.Map()
pathId = '8a11c27b-74c3-4570-bcd0-64829f7cd311'
ED_layer = addEllipsisVectorLayer(pathId, style=styleId)
map.add_child(ED_layer)
map

```


## Documentation


#### Raster layer options

| Name        | Description                                |
| ----------- | ------------------------------------------ |
| pathId      | id of the path                             |
| timestampId | id of the timestamp                        |
| style       | id of the style or a dictionary describing it |
| zoom     | maxZoomlevel of the layer.    |
| token       | token of the user                          |

#### Vector layer options

| Name        | Description                                |
| ----------- | ------------------------------------------ |
| pathId      | id of the path                             |
| timestampId | id of the timestamp                        |
| style       | id of the style or a dictionary describing it |
| zoom     | maxZoomlevel of the layer     |
| token       | token of the user                          |




