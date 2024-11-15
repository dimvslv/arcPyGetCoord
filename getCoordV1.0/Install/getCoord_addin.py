import arcpy
import pythonaddins

class Tool1(object):
    """Implementation for getCoord_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.

    def onClick(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        layers = arcpy.mapping.ListLayers(mxd)

        for layer in layers:
            if layer.getSelectionSet():
                selected_layer = layer
                break

        if not selected_layer:
            pythonaddins.MessageBox("Select features to get coordinates", "Info", 0)

        srid = arcpy.Describe(selected_layer).spatialReference

        if arcpy.Exists(r'in_memory\vertices'):
            arcpy.Delete_management(r'in_memory\vertices')

        arcpy.CreateFeatureclass_management('in_memory', 'vertices', "POINT", spatial_reference=srid)
        arcpy.AddField_management('vertices', "longitude", "DOUBLE")
        arcpy.AddField_management('vertices', "latitude", "DOUBLE")

        edit = arcpy.da.Editor('in_memory')
        edit.startEditing(False, True)
        edit.startOperation()

        with arcpy.da.InsertCursor('vertices', ["SHAPE@", "longitude", "latitude"]) as cursor:
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
                            for point in part:
                                if point is not None:
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
        lyr = arcpy.mapping.Layer('vertices')
        lyr.showLabels = True
        lyr.labelClasses[0].expression = '"X: " & [longitude] & " " & vbCrLf & "Y: " & [latitude]'
	arcpy.RefreshActiveView()
