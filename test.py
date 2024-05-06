import arcpy
import pythonaddins

def get_unique_name(base_name):
    """Generate a unique layer name by appending numeric suffixes"""
    name = base_name
    count = 1
    while arcpy.Exists(name):
        name = "{}_{}".format(base_name, count)
        count += 1
    return name

mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)

selected_layer = None

for layer in layers:
    if layer.getSelectionSet():
        selected_layer = layer
        break

if not selected_layer:
    pythonaddins.MessageBox("Select features to get coordinates", "Info", 0)

layer_name = get_unique_name('vertices')
srid = arcpy.Describe(selected_layer).spatialReference

# if arcpy.Exists(r'in_memory\vertices'):
# arcpy.Delete_management(r'in_memory\vertices')

arcpy.CreateFeatureclass_management('in_memory', layer_name, "POINT", spatial_reference=srid)
arcpy.AddField_management(layer_name, "longitude", "DOUBLE")
arcpy.AddField_management(layer_name, "latitude", "DOUBLE")

edit = arcpy.da.Editor('in_memory')
edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.InsertCursor(layer_name, ["SHAPE@", "longitude", "latitude"]) as cursor:
    for row in arcpy.da.SearchCursor(selected_layer, ["SHAPE@"]):
        shape = row[0]
        if shape is not None:
            if shape.type == "multipoint":
                for point in shape:
                    if shape is not None:
                        x, y = point.X, point.Y
                        cursor.insertRow([point, x, y])
            elif shape.type == "polygon" or shape.type == "multipolygon":
                for part in shape:
                    point_count = len(part)
                    for i, point in enumerate(part):
                        if point is not None:
                            if i == point_count - 1 and part[0].X == point.X and part[0].Y == point.Y:
                                continue
                            else:
                                x, y = point.X, point.Y
                                cursor.insertRow([point, x, y])
            elif shape.type == "polyline" or shape.type == "multilinestring":
                for part in shape:
                    for point in part:
                        if point is not None:
                            x, y = point.X, point.Y
                            cursor.insertRow([point, x, y])
            elif shape.type == "point":
                if shape.firstPoint is not None:
                    x, y = shape.firstPoint.X, shape.firstPoint.Y
                    cursor.insertRow([shape, x, y])

edit.stopEditing(True)
del mxd

# show labels
lyr = arcpy.mapping.Layer(layer_name)
lyr.showLabels = True
lyr.labelClasses[0].expression = '"X: " & [longitude] & " " & vbCrLf & "Y: " & [latitude]'
arcpy.RefreshActiveView()