# Simple CelShading Add-on for Blender

An extremely lightweight [**Blender**](https://www.blender.org) add-on that can apply cel-shading materials to objects. It also provides a one-button solution for applying cel-shading materials to VRoid created models (needs to be converted to PMX format).

Please note that this project was initially coded for my personal Douga work. As a result, the source code is not optimized and lacks complete error handling logic. If you encounter errors when using this add-on, please carefully read the user guide below to troubleshoot.

This add-on only works with the Eevee render engine.

## User Guide

### Installation
- Download the zip file `simple_celshading-v*.*.*.zip` from the [**release**](https://github.com/Xiaohan-Tian/celshading/releases) page.
- Click on the "Edit" menu -> "Preferences."
- In the "User Preferences" window, select "Add-on" on the left side.
- Click the "Install" button in the top-right corner of the "User Preferences" window.
- Choose the zip file you just downloaded and click the "Install Add-on" button at the bottom-right.
- Once you've made the selection, the "User Preferences" window will automatically display the add-on named `Simple CelShading *.*.*`. Ensure that the checkbox on the left side is checked.
- Close the "User Preferences" window.
- You can find the add-on in View3D -> Sidebar -> CelShading (or use the shortcut key `N` -> CelShading).

### Notes
If you need to apply CelShading to a PMX model imported by [**Blender MMD Tools**](https://github.com/UuuNyaa/blender_mmd_tools/tree/main), please make sure to perform the following two steps first:
- Select the model and click the "Convert to Blender" button. This step will convert the MMD-like materials into "Principled BSDF" and "Image Texture"-based simple materials.
- Then click the "Separated by Materials" button in Blender MMD Tools. This step will allow you to select each component of the body individually.

After completing these two steps, you can select different components one by one to convert them into CelShading materials.

### Features

#### Convert to CelShading Material

This feature can convert the first material of the selected object into a CelShading material.

Prerequisites:

- The selected object must have at least one material, and only the first material will be converted to a CelShading material.
- The first material of the selected object must have either a "Principled BSDF" shader or an "Image Texture" node.

Usage:

- Select the object you would like to convert to CelShading.
- Click the "Convert to CelShading Material" button.

![Single Color CelShading](res/guide-01-convert-to-celshading-color.png?raw=true "Single Color CelShading")
![Texture CelShading](res/guide-01-convert-to-celshading-texture.png?raw=true "Texture CelShading")

Notes:

- You can adjust the color difference between the lighted portion and shadowed portion via the "Factor" attribute of the purple-boxed "Mix Shader" shader.
- The color of the shadow can be adjusted by changing the first color of the "Color Ramp" node in the red box.

![Adjust Parameters](res/guide-01-adjust-parameters.png?raw=true "Adjust Parameters")

#### Convert to Emission Material

This feature can convert the first material into a flat-color or flat-image material that won't respond to any light or shadow.

Prerequisites:

- The selected object must have at least one material, and only the first material will be converted to a CelShading material.
- The first material of the selected object must have either a "Principled BSDF" shader or an "Image Texture" node.

Usage:

- Select the object you would like to convert to CelShading.
- Click the "Convert to Emission Material" button.

![Emission Material](res/guide-02-emission.png?raw=true "Emission Material")

#### Create Outline

This feature can create an outline for the selected object, a common effect seen in cartoons and anime.

Usage:

- Select the object.
- Click the "Create Outline" button.

![Outline](res/guide-03-outline.png?raw=true "Outline")

#### Create Welded Outline

This feature can create an outline for the selected object with an additional "Weld" modifier, which can resolve the disconnected outline issue in certain situations. Please note that this mode does not always work better than the general "Create Outline" feature.

Usage:

- Select the object.
- Click the "Create Welded Outline" button.

![Welded Outline](res/guide-04-welded-outline.png?raw=true "Welded Outline")

Note: The picture above shows the difference between a regular outline and a welded outline. Notice that the welded outline image on the right side resolved the disconnected outline issue, while the regular outline image on the left does not.

#### Create Sphere Normal Reference

This feature can create a sphere with a similar size as the selected object at the same place, and perform the Normal Transfer from the newly created sphere to the selected object. This can resolve uneven shadow issues typically observed on a character's face.

Usage:

- Select the object.
- Click the "Create Sphere Normal Reference" button.

![Normal Transfer](res/guide-05-normal-transfer.png?raw=true "Normal Transfer")

#### Auto Shading for VRoid Created Model (Experimental)

Note: This feature is experimental.

For PMX models converted from the VRM files exported by [**VRoid**](https://vroid.com/en/studio), you can use this feature to convert all the components in the model in bulk. Please note that the original VRM model is not supported by this feature.

To use this feature, first use the "Import" function of the Blender MMD Tools to import the PMX model to the stage. Then follow the notes mentioned above to click the "Convert to Blender" button and "Separated by Materials" button.

Once you are done with the preparation, select the item that directly contains all the body components from the Outliner view.

![Select container item from Outliner view](res/06-vroid-pmx-hierarchy.png?raw=true "Select container item from Outliner view")

In the example above, the imported PMX model has the name `Arcueid - Tsukihime - Demo`. By expanding the hierarchy in the Outliner View, you can find the item that contains all the body components, which is `Arcueid - Tsukihime - Demo_arm`. Thus, this is the item you should choose.

Once you have chosen the container object, click the "Auto Shading for VRoid Created Model" button, and the whole model will be automatically converted to CelShading mode, with the face object also applying the Normal Transfer feature.

![Auto Shading for VRoid Created Model](res/guide-06-result.png?raw=true "Auto Shading for VRoid Created Model")

#### Auto Shading for VRoid Created Model w/Welded Outline (Experimental)

Note: This feature is experimental.

Same as the "Auto Shading for VRoid Created Model" feature, the only difference is this feature will apply the welded outline to the model instead of regular outline.

## Credits
- The add-on is developed by me and is licensed under the MIT License.
- The PMX Model "Arcueid" was created by me, and the original character was designed by TYPE-MOON in their work "Tsukihime."
- The PMX Model "Saber" was created by me, and the original character was designed by TYPE-MOON in their work "Fate/stay night."
- All the 3D scenes depicted in the images within this document were created by me.

