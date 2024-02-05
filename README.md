# Simple CelShading Add-on for Blender

An extrame light-weighted [**Blender**](https://www.blender.org) add-on that can apply cel-shading materials to the objects. It also provides an one-button-solution to apply cel-shading materials to VRoid created models.

Note this project was initially coded for my personal Douga work, thus, the source code is not optimized and doesn't has complete error handling logic, when you see errors when using this add-on, please carefully read the user guide below to troubleshoot. 

This add-on only works in Eevee render engine.

## User Guide

### Installation
- Download the zip file `simple_celshading-v*.*.*.zip` from the [**release**](https://github.com/Xiaohan-Tian/celshading/releases) page
- Click menu item "Edit" -> "Preferences"
- Click "Add-on" on the left side of the "User Preferences" window
- Click "Install" button on the top-right of the "User Preferences" window
- Select the zip you just downloaded and click "Install Add-on" button on the bottom-right
- Once you made the selection, the "User Preferences" window will automatically filter out the add-on with the name `Simple CelShading *.*.*`, make sure the checkbox on the left side is checked
- Close the "User Preferences" window
- The add-on can be found in View3D -> Sidebar -> CelShading (or shortcut key `N` -> CelShading)

### Notes
If you need to apply CelShading to a PMX model imported by [**Blender MMD Tools**](https://github.com/UuuNyaa/blender_mmd_tools/tree/main), please make sure to perform the following 2 steps first:
- Select the model and click "Convert to Blender" button, this step will convert the MMD-like materials into "Principled BSDF" and "Image Texture"-based simple materials.
- Then click "Separated by Materials" button on the Blender MMD Tools, this step will allow you to select each component of the body individually.

After those 2 steps above, you can select different compoenents one by one to convert them into CelShading materials.

### Features

#### Convert to CelShading Material

This feature can convert the first material of the selected object into CelShading material.

Prerequisites:

- Selected object must has at least one material, and only the first material will be converted to CelShading material.
- The first material of the selected object must has either a "Principled BSDF" shader or a "Image Texture" node.

Usage:

- Select the object you would like to convert to CelShading.
- Click the "Convert to CelShading Material" button.

![Single Color CelShading](res/guide-01-convert-to-celshading-color.png?raw=true "Single Color CelShading")
![Texture CelShading](res/guide-01-convert-to-celshading-texture.png?raw=true "Texture CelShading")

Notes:

- The color difference between lighted portion and shadowed portion can be adjusted via the "Factor" attribute of the purple-boxed "Mix Shader" shader.
- The color of the shadow can be adjusted by changing the first color of the "Color Ramp" node in the red box.

![Adjust Parameters](res/guide-01-adjust-parameters.png?raw=true "Adjust Parameters")

#### Convert to Emission Material

This feature can convert the first meterial into a flat-color or a flat-image material which won't response to any light and shadow. 

Prerequisites:

- Selected object must has at least one material, and only the first material will be converted to CelShading material.
- The first material of the selected object must has either a "Principled BSDF" shader or a "Image Texture" node.

Usage:

- Select the object you would like to convert to CelShading.
- Click the "Convert to Emission Material" button.

![Emission Material](res/guide-02-emission.png?raw=true "Emission Material")

#### Create Outline

This feature can create an outline for the selected object. This effect can be usually seen in Cartoons and Animes.

Usage:

- Select the object.
- Click the "Create Outline" button.

![Outline](res/guide-03-outline.png?raw=true "Outline")

#### Create Welded Outline

This feature can create an outline for the selected object with an additional "Weld" modifier, this can resolve the disconnected outline issue that in some certain situation. But please note this mode not always works better than the general "Create Outline" feature.

Usage:

- Select the object.
- Click the "Create Welded Outline" button.

![Welded Outline](res/guide-04-welded-outline.png?raw=true "Welded Outline")

Note: The picture above shows the difference between regular outline and welded outline. Notice that the welded outline image shows on the right side resolved the disconnected outline issue the regular outline image on the left shows.

#### Create Sphere Normal Reference

This feature can create a sphere with similar size of the selected object at the same place, and perform the Normal Transfer from the newly created sphere to the selected object.

This can resolve uneven shadow issue normally can be observed on the character's face.

Usage:

- Select the object.
- Click the "Create Sphere Normal Reference" button.

![Normal Transfer](res/guide-05-normal-transfer.png?raw=true "Normal Transfer")

#### Auto Shading for VRoid Created Model (Experimental)

Note: this feature is a experimental feature.

For PMX models converted from the VRM files exported by [**VRoid**](https://vroid.com/en/studio), you can use this feature to convert all the components in the model in bulk. Note the original VRM model is not supported by this feature.

To use this feature, first use the "Import" function of the Blender MMD Tools to import the PMX model to the stage, then follow the Notes mentioned above click "Convert to Blender" button and "Separated by Materials" button.

Once you are done with the preparation, select the item directly contains all the body components from the Outliner view.

![Select container item from Outliner view](res/06-vroid-pmx-hierarchy.png?raw=true "Select container item from Outliner view")

In the example above, the imported PMX model has the name `Arcueid - Tsukihime - Demo`, by expanding the hierarchy in the Outliner View, you can find the item contains all the body component is `Arcueid - Tsukihime - Demo_arm`, thus, this is the item you should choose.

Once you has chosen the container object, click the "Auto Shading for VRoid Created Model" button, the whole model will be automatically converted to CelShading mode, and the face object will also be applied the Normal Transfer feature.

![Auto Shading for VRoid Created Model](res/guide-06-result.png?raw=true "Auto Shading for VRoid Created Model")

#### Auto Shading for VRoid Created Model w/Welded Outline (Experimental)

Note: this feature is a experimental feature.

Same with the "Auto Shading for VRoid Created Model" feature, the only difference is this feature will apply the welded outline to the model instead of regular outline.
