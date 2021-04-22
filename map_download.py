# Action to download a BSB .zip file from NOAA, extract its .KAP file,
# clip to its footprint and RGB-ify it.

import os
from zipfile import ZipFile
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QProgressDialog,QMessageBox
from qgis.core import QgsFileDownloader,QgsMemoryProviderUtils,QgsRasterLayer,QgsProject,QgsFeature,QgsWkbTypes
import processing

# set up variables from the feature that's being identified
chart = '[% CHART %]'
chart_num = '[% CHART_NUM %]'
footprintsLayer = QgsProject.instance().mapLayer('[% @layer_id %]')

# it is apparently necessary to query the layer to actually get the QgsFeature object in a Python action
features = list(footprintsLayer.getFeatures("CHART_NUM = '{}'".format(chart_num)))
feature = features[0]
download_url = feature['DWNLD_URL']

# set up assorted names and paths
storageDir = os.path.join(QgsProject.instance().homePath(),'NOAA-raster')
if not os.path.exists(storageDir):
    os.mkdir(storageDir)  # a place to do our work adjacent to the project
imagePath = os.path.join(storageDir, chart + '.zip')   # downloaded BSB archive
rasterPath = os.path.join(storageDir,'BSB_ROOT',chart,chart_num+'.KAP')   # raster file extracted from it
clippedName = chart_num+'_clipped'    # name of a temporary clipped layer
clippedPath = os.path.join(storageDir,clippedName+'.tif')   # the clipped file
rgbPath = os.path.join(storageDir,chart_num+'.tif')   # the final clipped RGB image file

# create the final raster layer once we have the file
def create_rgb_layer():
    rgbLayer = QgsRasterLayer(rgbPath, '[% CHART_NUM || ': ' || TITLE %]')
    QgsProject.instance().addMapLayer(rgbLayer)
    
# do all the processing needed and add the layer
def add_layer():
    QMessageBox.information(
        None,
        'Clip downloaded chart',
        'In the following dialog, just click Run, wait for the operation to complete, then click Close. Do not change any of the settings.')
    zipMember = 'BSB_ROOT/{}/{}.KAP'.format(chart,chart_num)
    zf = ZipFile(imagePath)
    zf.extract(zipMember, storageDir)

    # Copy the footprint from the NOAA feature layer to a temporary polygon masking layer.
    # The footprint is a MultiPolygon but we need a Polygon.
    maskLayer = QgsMemoryProviderUtils.createMemoryLayer(
                'Chart footprint', QgsFields(), QgsWkbTypes.Polygon,
                footprintsLayer.crs()
        )
    QgsProject.instance().addMapLayer(maskLayer)
    polygon = feature.geometry().coerceToType(QgsWkbTypes.Polygon)[0]
    mask = QgsFeature()
    mask.setGeometry(polygon)
    maskLayer.startEditing()
    maskLayer.addFeature(mask)
    maskLayer.commitChanges()

    # Perform the clipping using a standard algorithm dialog.
    params = {
        'INPUT': rasterPath,
        'MASK': maskLayer,
        'NODATA': 255,
        'OUTPUT': clippedPath
    }
    clippedResults = processing.execAlgorithmDialog('gdal:cliprasterbymasklayer', params)
    clippedLayer = None

    # Get the layer that was created.
    for layer in QgsProject.instance().mapLayersByName(clippedName):
        clippedLayer = layer
    if clippedLayer is None:
        raise Exception('Could not locate clipped layer ' + clippedName)

    QMessageBox.information(
        None,
        'Convert clipped chart to RGB',
        'The clipped chart will now be converted to a full RGB color space. This may take a moment.')

    # write that layer out using its rendering pipe, which causes it to become
    # a regular RGB layer so that it interpolates properly when zoomed out.
    writer = QgsRasterFileWriter(rgbPath)
    writer.writeRaster(clippedLayer.pipe(),
        int(clippedLayer.extent().width() / clippedLayer.rasterUnitsPerPixelX()),
        int(clippedLayer.extent().height() / clippedLayer.rasterUnitsPerPixelY()),
        clippedLayer.extent(),
        clippedLayer.crs(),
        clippedLayer.transformContext()
    )

    # Now create the final layer from the exported file
    create_rgb_layer()
    
    # remove our temporary stuff
    QgsProject.instance().removeMapLayer(maskLayer.id())
    QgsProject.instance().removeMapLayer(clippedLayer.id())
    os.remove(rasterPath)
    os.remove(clippedPath)
    os.remove(imagePath)

# Check if we already have an exported chart file in the expected place. If so, use it.
if os.path.exists(rgbPath):
    create_rgb_layer()
# Otherwise, download the BSB archive and do all the things.
else:
    # create a file downloader
    dl = QgsFileDownloader(QUrl(download_url), imagePath)
    prog = QProgressDialog('Downloading map...', 'Cancel', 0, 100)

    dl.downloadProgress.connect(lambda received,total: prog.setValue(received*100/total))
    prog.show()
    prog.canceled.connect(dl.cancelDownload)
    dl.downloadCompleted.connect(prog.reset)
    dl.downloadCompleted.connect(add_layer)
