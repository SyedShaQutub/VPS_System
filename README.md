# VPS_System
Creation of Validation parameter space system for 3D scenes to test algorithms running on Autonomous cars. Visualized using blender.


/* requirements:*/
 * Blender 2.8X
    Blender addons (sun position addon - can be located in repository)
    In blender goto edit->preferences->addons and locate the addon fodler to install. 
    
/* Python packages to be installed in blender's python enviroment: */
 *Shapely
 *Pandas
 *numpy
 *tqdm

    Installation for Windows:
    
        Blender - download 2.8x version from blender.org
        locate to blender installation - ../2.8x/python/bin/: .\python.exe -m pip install --proxy=http://ipaddrss:port PACKAGE --user
            --user is optional if you dont have admin rights
            --proxy is optional if system is not connected through proxy server
        
        
    Installation for Ubuntu:
        Blender - snap install blender --classic
        locate to blender installation - ~/blender/blender-2.82-linux64/2.8x/python/bin : ./python3.7m -m pip install PACKAGE
    
    
Command to execute the blender script located in vps engine:
    sudo blender /scene_content/graphics/city_models/PolygonCity/test/obj/includes_all_polygons/poly_changed_MAT.blend --background --python /vps_engine/scene_creation_2.81/scene_launch.py
