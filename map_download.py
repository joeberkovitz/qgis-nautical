# Action to download a BSB .zip file from NOAA, extract its .KAP file,
# clip to its footprint and RGB-ify it.

import os
from functools import partial
from zipfile import ZipFile
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QProgressDialog,QMessageBox
import processing
from qgis.utils import iface

# set up variables from the feature that's being identified
chart = '[% CHART %]'
chart_num = '[% CHART_NUM %]'
download_url = '[% DWNLD_URL %]'
geom_wkt = '[% geom_to_wkt($geometry) %]'
footprintsLayer = QgsProject.instance().mapLayer('[% @layer_id %]')

# set up assorted names and paths
storageDir = os.path.join(QgsProject.instance().homePath(),'NOAA-raster')
if not os.path.exists(storageDir):
    os.mkdir(storageDir)  # a place to do our work adjacent to the project
imagePath = os.path.join(storageDir, chart + '.zip')   # downloaded BSB archive
rasterPath = os.path.join(storageDir,'BSB_ROOT',chart,chart_num+'.KAP')   # raster file extracted from it
clippedPath = os.path.join(storageDir,chart_num+'.tif')   # the clipped file
workingDict = {}

prog = QProgressDialog('', 'Cancel', 0, 100)

# run a task in the background
def run_task(task, message):
    QgsApplication.taskManager().addTask(task)
    prog.setLabelText(message)
    prog.setValue(1)
    prog.show()

# run a processing algorithm as a task
def run_alg_task(algId, params, message, onFinish):
    alg = QgsApplication.instance().processingRegistry().algorithmById(algId)
    context = QgsProcessingContext()
    task = QgsProcessingAlgRunnerTask(alg, params, context)
    task.executed.connect(partial(onFinish, context))
    run_task(task, message)

# clip the chart to its footprint
def mask_chart_layer():
    with ZipFile(imagePath) as zf:
        zipMember = 'BSB_ROOT/{}/{}.KAP'.format(chart,chart_num)
        zf.extract(zipMember, storageDir)
    os.remove(imagePath)

    # Copy the footprint from the NOAA feature layer to a temporary polygon masking layer.
    # The footprint is a MultiPolygon but we need a Polygon, so we can't clip to it directly.
    maskLayer = QgsMemoryProviderUtils.createMemoryLayer(
                'Chart footprint', QgsFields(), QgsWkbTypes.Polygon,
                footprintsLayer.crs()
        )
    QgsProject.instance().addMapLayer(maskLayer)
    polygon = QgsGeometry.fromWkt(geom_wkt).coerceToType(QgsWkbTypes.Polygon)[0]
    mask = QgsFeature()
    mask.setGeometry(polygon)
    maskLayer.startEditing()
    maskLayer.addFeature(mask)
    maskLayer.commitChanges()
    workingDict['maskLayerId'] = maskLayer.id()

    # Perform the clipping using a standard algorithm dialog.
    run_alg_task(
        'gdal:cliprasterbymasklayer',
        {
            'INPUT': rasterPath,
            'MASK': maskLayer,
            'NODATA': 255,
            'TARGET_CRS': QgsProject.instance().crs(),
            'OUTPUT': clippedPath
        },
        'Clipping to chart boundary...',
        create_clipped_layer)


# create the final raster layer once we have the file
def create_clipped_layer(context, successful, results):
    if not successful:
        raise Exception(tr('Could not perform clipping operation.'))

    os.remove(rasterPath)
    QgsProject.instance().removeMapLayer(workingDict['maskLayerId'])

    add_clipped_layer()

def add_clipped_layer():
    clippedLayer = QgsRasterLayer(clippedPath, '[% CHART_NUM || ': ' || TITLE %]')
    iface.setActiveLayer(footprintsLayer)
    QgsProject.instance().addMapLayer(clippedLayer)
    prog.reset()
    

# Check if we already have an exported chart file in the expected place. If so, use it.
if os.path.exists(clippedPath):
    add_clipped_layer()
# Otherwise, download the BSB archive and do all the things.
else:
    # create a file downloader
    dl = QgsFileDownloader(QUrl(download_url), imagePath)
    dl.downloadProgress.connect(lambda received,total: prog.setValue(received*100/total))
    prog.setLabelText('Downloading map...')
    prog.show()
    prog.canceled.connect(dl.cancelDownload)
    dl.downloadCompleted.connect(mask_chart_layer)
