## QGIS Resources for Mariners

This site contains a set of QGIS project files and associated documentation
for people seeking to create high quality nautical charts with QGIS. Some
projects are templates that can be downloaded and are immediately ready to
use, with no dependencies on other files in the GitHub repository. Others are
designed to be used in conjunction with resources in the repository.

The materials here were created by [Joe Berkovitz](https://www.joeberkovitz.com/contact/),
a sea kayaker based in Marblehead, MA.

## NOAA Raster Charts Template

This QGIS project includes useful components to get started creating
high-quality nautical charts based on NOAA raster marine charts. It includes
the following:

- **Data layers for making charts**. These include NOAA RNC marine charts,
satellite imagery, street maps and magnetic north lines among other things. The
resolution and scale of these layers depends on the scale at which they are
viewed. All data is downloaded over the internet so there is no need to get hold
of specific files for specific areas.

- **Sample chart layouts**.  A set of sample project layouts is ready-made for
duplication in 11x17 landscape and portrait. Each layout has a map, title,
scale bar, legend and lat/long grid.

**[Download NOAA-Template.qgz](NOAA-Template.qgz)**

## Quick guide to making raster charts

This guide describes how to:
- Download the QGIS program installer
- Open the NOAA-Template project in QGIS
- Use the QGIS map and layers to view areas of the world
- Make a layout of a specific chart
- Export a layout to a PDF file

QGIS is a very complex program and there is much more to discover about it
than this guide can describe. For detailed information, or where a question is not
answered here, please consult the
[QGIS Desktop User Guide](https://docs.qgis.org/3.16/en/docs/index.html).

### Download QGIS

QGIS makes intensive use of CPU and graphics, similar to a video game or
illustration program. You will need a MacOS, Windows or Linux computer that is
reasonably powerful, and a reasonably large high-resolution monitor. Multicore
with at least 4 GB of RAM is recommended. Your mileage may vary: see what
works.

Begin by downloading the QGIS application for your computer from
[download.qgis.org](https://download.qgis.org). Use the stable version, not
the bleeding-edge release. If you are on Windows use the Standalone Installer.

Also download the template project `NOAA-Template.qgz` described [above](#noaa-raster-charts-template) and copy it
to a new folder that you will be using to create your charts. You may wish to change its name also
since it will no longer be a template once you start changing it.

### Open the template project

Start the QGIS application and use **Project > Open...** to open the template project.
(In the future you can use **Open Recent >** as a shortcut.)

When you open the project up, in the center of the window you will see the
main map that QGIS uses, called the **Map View**. The next section describes
how to work with this view.

### Use the Map View and Layers

![Map View](/guide/images/MapView.png)

The **Map View** is where you choose areas of the world to look at and decide
what information you want to view, or make charts of. You can also create
routes and waypoints in this view.

A few important items in the view are circled above:

- At the top, the **Pan** tool (hand) lets you move the map around
laterally by clicking and dragging. To its right you can also see **Zoom In** and
**Zoom Out** tools.

- On the left side of the screen the **Layers panel** shows the set of layers
available for viewing in the map.

- On the bottom, the **Coordinates** box shows the lat/long of the mouse position.

- On the bottom, the **Scale** control displays and also controls the scale of the map view.

#### Pan and zoom the map

You can move the map from side to side and zoom in and out. Become familiar
with the way that this works and read the [QGIS documentation on the map view](https://docs.qgis.org/3.16/en/docs/user_manual/introduction/qgis_gui.html#map-view).

Whenever the **Pan** tool is selected you may click and drag the map using your
mouse to move it around. You can also drag the map without clicking by holding
down the spacebar at the same time, which is useful when you're using a tool
other than the Pan tool.

On a mouse that has a scroll wheel, the wheel lets you zoom in and out.
On trackpads, drag two fingers vertically up or down over the map to zoom in
and out. Hold down Command (Mac) or Alt (Windows) to zoom more slowly.

You can also type a scale directly into the **Scale** control at the bottom of the window.

#### Control the map layers

Similar to Adobe Illustrator and other drawing programs, QGIS maps display a
set of visual layers that can be independently turned on and off. These are
shown in the Layers panel at lower left. 

When you first open the template project, layers for marine charts and a
magnetic grid pertinent for Massachusetts are turned on. Each layer has its
own checkbox enabling it. Try checking and unchecking the various boxes to see
what the layers contain.

Layers included in the template project include:

- *NOAA Raster Charts* marine charts layer. These are tiled versions of the
NOAA printed charts that are  automatically downloaded from NOAA web servers.
You do not need to download any PDFs to see these.

- *NOAA Raster Chart Footprints* layer that shows the boundaries of numbered
NOAA nautical charts. This is useful if you actually want to grab the
corresponding PDF or reference it for someone else.

- *Google Maps satellite* imagery layer that is basically the same as Maps'
Satellite view. Very handy for seeing what areas actually look like.

- *OpenStreetMap* topo/street map view (similar to Google Maps' Default view).

- *Magnetic grids* showing magnetic north at various declinations in various
regions, currently limited to New England and the West Coast of the US. These were
created in QGIS by the author and are loaded from the Github website. To make
your own magnetic north grids, use the [Compass Routes plugin](#compass-routes-plugin).


- *Waypoints* showing general-purpose markers with labels.

- *Auto-labeled routes* for drawing automatically labeled route legs.

- *NOAA ENC Chart Prototype* experimental marine charts generated from digital
data. These are a prototype showing the direction that NOAA charts will take
in the future, as hand-produced nautical charts are being discontinued. NOAA
cautions that these maps are not yet ready to be used for navigation, but they
do reveal some features not shown in the traditional charts.

The order of the layers is important, as layers on top can obscure layers on
the bottom. They can be dragged around and reordered. They are also placed in
groups which can be turned on and off to control the visibility of every layer
inside the group.

For most purposes, the *Raster Charts* and one of the *Magnetic grids* layers
will give you a workable chart.

If you get lost and don't see anything in the map view, this can happen
because the layers that are turned on don't have any material in the area
where your map is pointed. To get your bearings, turn on the *OpenStreetMap*
layer (which covers the whole globe) and zoom out to figure out where you are.

### Make a chart using a QGIS Layout

The main map is just a way to inspect the map data in QGIS. It is not a chart.
To make a chart, you use a QGIS object called a **Layout**. Each layout is a
complete design for showing a map with all the associated information that goes
with it, such as scale bars, labels, a title, and so on. Once you have a layout,
it can then be exported to a PDF file.

Layouts are part of your project. Whenever you save the project, all of your defined
layouts are saved along with it.

The steps in making a layout are:

- Setting up the main map view and layers to show the information of interest
- Creating and naming the layout
- Panning, zooming and rotating the layout's map as desired
- Editing and adjusting the title, scale bars
- Adding any other decorations, such as descriptive text

#### Setting up the map to make a layout

If you've worked with the **Map View** already, this is pretty
straightforward. Pan and zoom the map so it shows approximately the area you
want to have in your chart, at about the right scale. The Map View does not
have to be perfect, because you will adjust all the details in the Layout
you are about to create. Just get it in the ballpark.

If you were making a chart of Salem Sound, your Main Map (with magnetic grid
for 14º W) might look like this:

![Map View before making layout](/guide/images/MapViewPreChart.png)

(A lot of the detail is missing, because QGIS is automatically using an
overview chart so as to keep everything readable on the screen. Don't worry,
the detail will be in the final chart!)

#### Creating your layout

To make your layout, you will copy an existing layout that is already set up, and then
plug in the area of interest.

In the main map view window choose **Project > Layout Manager...**. You'll see a window
like this appear:

![Layout Manager](/guide/images/LayoutManager.png)

There is one of each of these premade 11x17" layouts for each choice of
chart orientation (Portrait, Landscape) and each choice of scales (1:25K and 1:50K).
The scale choices differ only in the grid labels: 1:25K is labeled every
minute, while 1:50K is labeled every 2 minutes.

Pick the orientation you want, and click the **Duplicate...** button below the list.
You can give your new layout a name.

#### Syncing the layout to the main map

Now your layout will be open in its own window, but it will be showing the
wrong area: it will display whatever was originally put into the premade
layout. Your first step is to make it show the same area as the main map.

Begin by clicking the map to select it, and then open the **Item Properties**
tab in the panel on the right (circled in the figure below). Your layout
window should now look something like this:

![Layout](/guide/images/Layout.png)

Click the small red icon circled above, whose full name is **Set Map Extent to
match Main Canvas Extent**: a fancy way of saying, make this layout's map show
the same area as the main map. Click this button, and the map should change
to show the same area as the main map. If it doesn't, try clicking the blue
**Update Map Preview** icon just to its left.

#### Adjust the layout map to the exact position and scale you want.

Leaving the map selected, use the **Edit > Move Content** menu command to
choose the content scrolling tool. (Notice that this changes the selected tool
in the toolbar on the left of your screen: you can click the tool icon to
accomplish the same thing.)

Now your mouse/trackpad will pan and zoom what is _inside_ the selected
map (as opposed to zooming the view of your layout or dragging the map around
the page). Pan and zoom until you have everything just the way you want it.
You can also adjust the scale and map rotation by typing the values in the
Item Properties panel.

When you are done, use the **Edit > Select/Move Item** command to go back
to using your mouse to select and move items on the map.

#### Edit the labels, scale bar and anything else you want.

At this point you may drag the other items on the map anywhere you like, to
get them out of the way of things on the map that you would like to look at.

You can edit text and all other attributes of the current selected object in
the **Item Properties** panel at any time.

This is also the point at which you can add special text, markers, lines, etc.
that are unique to this layout (as opposed to shared with other layouts).

#### Export the layout to PDF

At this point, your chart is ready to export to PDF. Most likely it still does
not show the right level of detail though -- but still, no worries on that
score. (You can skip this step, but if you really want to preview the chart at
the level of detail in which it will appear on the final PDF, magnify the
layout view scale to 400% using the Scale box at the lower right of the
window, then use **Edit > Pan Layout** to move the layout around on the screen
to see how it looks at full scale.)

The last step is to export the finished layout to PDF using the **Layout >
Export as PDF…** menu command. You will specify the filename to which the PDF
is to be exported. This may take some time as many detailed images may need to
be downloaded; during this time, the program will likely be unresponsive. When
QGIS is done, it will display a green notice at the top of the layout window
and you will now have your finished chart as a PDF.

Here's [an example](/guide/charts/SalemSound.pdf). (It's a large file and you
may need to view it in Acrobat rather than in your web browser.)

### Adding markers or waypoints

To add markers to your mapping data that can appear in any layout that you
create, you can use the *Waypoints* layer in the template project.  In the
main map window, select this layer in the **Layers** panel by clicking it, and
use the menu command **Layer > Toggle Editing** to let you edit the layer.
Then use **Edit > Add Point Feature** (short cut Ctrl-. or Command-.) to
change the mouse to a tool that adds markers.

Click on the map to add features. You may enter an optional label with each one.
They look like this:

![Marker](/guide/images/Marker.png)

When you are done, you must save the waypoint data or it will go away when the
project is closed. To do this, click the small icon to the right of the layer
name in the Layers panel:

![Make Permanent](/guide/images/MakeLayerPermanent.png)

A dialog will appear that lets you specify a filename on your computer where
the waypoints will be saved. The circled "..." button below lets you choose
the folder and filename for the waypoint data.

![Save Scratch Layer](/guide/images/SaveScratchLayer.png)

This only has to be done once. In the future the project will remember where the
waypoint layer data is saved.

You can double click the layer name to edit various properties of how the
markers look, are colored, labeled, etc. These are quite involved and beyond
the scope of this guide but they are easy to experiment with.

### Adding route segments with compass bearings

To add route segments to your maps which are automatically labeled with the
distance and magnetic bearing, you can use one of the two *Routes* layers in
the project. Pick the appropriate magnetic variation for your area.

In the main map window, select this layer in the **Layers** panel by clicking it,
and use the menu command **Layer > Toggle Editing** to let you edit the layer.
Then use **Edit > Add Line Feature** (short cut Ctrl-. or Command-.) to change the
mouse to a tool that adds route segments.

To add each individual segment, you will need to carry out this sequence:
- left-click on the starting point,
- left-click on the finishing point,
- right-click anywhere on the map. (on a trackpad, this is a two-finger click usually. On single-button mouse computers, you will need to find out how you simulate a right click for your machine.)

The result looks like this:

![RouteSegments](/guide/images/RouteSegments.png)

As with [waypoints](#adding-waypoints) above, you must make your route layer
permanent and save its data on your computer or it will disappear as soon as
you close the project.

To make new auto-labeled compass route layers, please use the [Compass Routes plugin](#compass-routes-plugin).

### Compass Routes plugin

You can install the Compass Routes plugin in QGIS to make your own route layers
and magnetic north lines for any area with any magnetic variation.

The plugin is currently experimental. To install it, open up the Plugin Manager
using the **Plugins > Manage and Install Plugins...** menu command. First go
to the **Settings** tab and check the box labeled *Show also experimental plugins*.
Then go to the **Not Installed** tab and locate the Compass Routes plugin, then
install it.

Documentation for the plugin can be found [here](https://joeberkovitz.github.io/qgis-compass-routes).