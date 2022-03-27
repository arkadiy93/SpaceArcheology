#Script needs to be run in Python 3.7 or 3.8. Re-write to jupyter notebook for use with ArcGIS Pro or test with final application.
import arcpy
import math
import os




def MSRM(resolution,min_size,max_size,scaling_factor,input_raster,output_name):  # MSRM

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")
    arcpy.CheckOutExtension("3D")

    #Calculate input parameters for MSRM
    i = math.floor(((min_size-resolution)/(2*resolution))**(1/scaling_factor))
    n = math.ceil(((max_size-resolution)/(2*resolution))**(1/scaling_factor))
    print(f"Minimum Size: {min_size}")
    print(f"Maximum Size: {max_size}")
    print(f"Scaling Factor: {scaling_factor}")
    print(f"Calculated i: {i}")
    print(f"Calculated n: {n}")
    raster = arcpy.Raster(input_raster)

    # Creates low pass filter rasters, subtracts filtered rasters from each other and sums up the differences according to MSRM algorithm. Deletes intermediate rasters as soon as they are not needed anymore.
    counter = 0
    for j in range(i, n+1):
        window_size = j**scaling_factor
        result = os.path.join(str(j))
        focal_statistics = result
        result = arcpy.ia.FocalStatistics(in_raster=raster, neighborhood="Rectangle " + str(window_size) + " " + str(window_size) + " MAP", statistics_type="MEAN", ignore_nodata="DATA", percentile_value=90)
        result.save(focal_statistics)
        if j == 2:
            output_raster = os.path.join(str(j-1) + "-" + str(j))
            arcpy.ddd.Minus(in_raster_or_constant1=str(j-1), in_raster_or_constant2=str(j), out_raster=output_raster)
            arcpy.Delete_management(j-1)
        elif j == 3:
            output_raster = os.path.join(str(j-1) + "-" + str(j))
            arcpy.ddd.Minus(in_raster_or_constant1=str(j-1), in_raster_or_constant2=str(j), out_raster=output_raster)
            arcpy.Delete_management(j - 1)
            counter += 1
            output_raster = os.path.join("summed" + str(counter))
            arcpy.ddd.Plus(in_raster_or_constant1=str(j - 2) + "-" + str(j - 1),
                           in_raster_or_constant2=str(j - 1) + "-" + str(j), out_raster=output_raster)
            arcpy.Delete_management(str(j - 2) + "-" + str(j - 1))
        elif j > 3:
            output_raster = os.path.join(str(j-1) + "-" + str(j))
            arcpy.ddd.Minus(in_raster_or_constant1=str(j - 1), in_raster_or_constant2=str(j), out_raster=output_raster)
            arcpy.Delete_management(j - 1)
            counter += 1
            output_raster = os.path.join("summed" + str(counter))
            arcpy.ddd.Plus(in_raster_or_constant1="summed" + str(counter - 1),
                           in_raster_or_constant2=str(j - 1) + "-" + str(j), out_raster=output_raster)
            arcpy.Delete_management(str(j - 2) + "-" + str(j - 1))
            arcpy.Delete_management("summed" + str(counter - 1))


    #Rescale sum based on number of low pass filter differences summed up.
    final_summed = "summed" + str(int(n-i-1))
    in_constant= round(float(1/(n-i)),4)
    arcpy.Times_3d(final_summed, in_constant, output_name)
    arcpy.Delete_management(final_summed)
    arcpy.Delete_management(str(n-1) + "-" + str(n))
    arcpy.Delete_management(str(n))




if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\tfive\OneDrive\Dokumenter\ArcGIS\Projects\Mound_Detection\Relief_Models\Temp", workspace=r"C:\Users\tfive\OneDrive\Dokumenter\ArcGIS\Projects\Mound_Detection\Relief_Models\Temp"):
