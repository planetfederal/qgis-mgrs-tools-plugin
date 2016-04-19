.. (c) 2016 Boundless, http://boundlessgeo.com
   This code is licensed under the GPL 2.0 license.

Usage
=====

The *MGRS tools plugin* contains two tools:

* :ref:`mgrs-map-tool`
* :ref:`zoom-to-mgrs`

.. note::

   The Military Grid Reference System (MGRS) was created as a geocoordinate standard used by NATO militaries for locating points on the earth. MGRS coordinates are given as single string composed of a pattern of letters and numbers and represent a grid square. The coordinates can be given with different precision levels, representing squares with different side sizes (100Km, 10km, 1km, 100m, 10m, 1m).

   For more information about the MGRS system use the following the `link <https://en.wikipedia.org/wiki/Military_grid_reference_system)>`_.

.. _mgrs-map-tool:

MGRS Map Tool
-------------

To use the *MGRS map tool*, go to :menuselection:`Plugins --> MGRS --> MGRS map tool` or use the *MGRS map tool* button available in the :guilabel:`Plugin Toolbar`.  

The *MGRS map tool* will get activated. Now, when you move your mouse cursor over the QGIS map canvas, the corresponding MGRS coordinates will be displayed in the QGIS status bar (bottom left).

.. figure:: img/statusbar.png

   QGIS status bar showing the coordinate of the mouse cursor position.
   
Besides, with the *MGRS map tool* activated, the user can also click anywhere in the map canvas to get the MGRS coordinate (at 1m precision) copied to the clipboard.

.. _zoom-to-mgrs:
   
Zoom to MGRS coordinate
-----------------------

The *Zoom to MGRS coordinate* tool will allow you to zoom the map canvas to a given MGRS coordinate.

The *Zoom to MGRS coordinate* tool is accessed trough the :guilabel:`MGRS Coordinate Zoom` panel. If the panel is not active yet, go to :menuselection:`Plugins --> MGRS` and click :guilabel:`Zoom to MGRS coordinate`.

Insert the desired MGRS coordinate in the :guilabel:`MGRS coordinate` field (The coordinates can be inserted at any level of precision, from 100 km to 1 m), and press the :guilabel:`Zoom to` button. The map canvas will be centered and zoomed to the corresponding MGRS grid square, and a marker will be added to the corresponding position.

.. figure:: img/zoomto.png

   Map Canvas centered on inserted MGRS coordinate

To remove the marker, click the :guilabel:`Remove marker button` in the :guilabel:`MGRS Coordinate Zoom panel`
