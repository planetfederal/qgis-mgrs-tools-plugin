<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+8" simplifyLocal="1" simplifyMaxScale="1" readOnly="0" version="3.2.3-Bonn" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyAlgorithm="0" simplifyDrawingTol="1" labelsEnabled="0">
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol name="0" alpha="1" clip_to_extent="1" type="marker">
        <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="229,182,54,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"fid"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory penAlpha="255" enabled="0" height="15" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" maxScaleDenominator="1e+8" sizeType="MM" width="15" penColor="#000000" opacity="1" scaleBasedVisibility="0" lineSizeType="MM" backgroundAlpha="255" labelPlacementMethod="XHeight" scaleDependency="Area" minScaleDenominator="0" penWidth="0" sizeScale="3x:0,0,0,0,0,0" barWidth="5" backgroundColor="#ffffff" rotationOffset="270">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" obstacle="0" priority="0" zIndex="0" showAll="1" placement="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="EASTING">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NORTHING">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MGRS_compare">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MGRS">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="EASTING" index="1"/>
    <alias name="" field="NORTHING" index="2"/>
    <alias name="" field="MGRS_compare" index="3"/>
    <alias name="" field="MGRS" index="4"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="EASTING" applyOnUpdate="0" expression=""/>
    <default field="NORTHING" applyOnUpdate="0" expression=""/>
    <default field="MGRS_compare" applyOnUpdate="0" expression=""/>
    <default field="MGRS" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" field="fid" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="EASTING" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="NORTHING" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="MGRS_compare" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint constraints="0" field="MGRS" notnull_strength="0" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="fid" exp=""/>
    <constraint desc="" field="EASTING" exp=""/>
    <constraint desc="" field="NORTHING" exp=""/>
    <constraint desc="" field="MGRS_compare" exp=""/>
    <constraint desc="" field="MGRS" exp=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="EASTING" width="-1" type="field" hidden="0"/>
      <column name="NORTHING" width="-1" type="field" hidden="0"/>
      <column name="MGRS_compare" width="-1" type="field" hidden="0"/>
      <column name="MGRS" width="239" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="EASTING" editable="1"/>
    <field name="MGRS" editable="1"/>
    <field name="MGRS_compare" editable="1"/>
    <field name="NORTHING" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="EASTING"/>
    <field labelOnTop="0" name="MGRS"/>
    <field labelOnTop="0" name="MGRS_compare"/>
    <field labelOnTop="0" name="NORTHING"/>
    <field labelOnTop="0" name="fid"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles>
      <fieldstyle fieldname="MGRS">
        <style rule="@value != &quot;MGRS_compare&quot; || '0000000000'" background_color_alpha="255" text_color_alpha="0" name="" text_color="#000000" background_color="#ff0101">
          <font description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
        </style>
      </fieldstyle>
      <fieldstyle fieldname="MGRS_compare"/>
    </fieldstyles>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>fid</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
