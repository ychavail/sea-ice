# chargement des packages
using ClimateTools, Glob, Shapefile, AxisArrays, ProgressMeter, Dates, NetCDF

# fichier de sortie de commentaires pendant la compilation
fileprint   = "/home/yanncha/GitHub/sea-ice/outputs_from_code/mask_adminQC.txt"
io          = open(fileprint,"a")

# shapefile pour masque sur les régions administrative québécoises
shpfile = "/home/yanncha/GitHub/sea-ice/masking/admin_QC.shp"
polyshp = read(shpfile,Shapefile.Handle)

# definition of regions to focus on with shapefiles
regions_name    = ["Montreal","Nord du Quebec","Gaspesie"]
regions_code    = ["MTL","NDQ","GAS"]
regions_number  = [18,20,6]

# variables to zoom in
path    = "/exec/yanncha/sea_ice/"
var     = ["pr"]
indice  = ["max1j"]
season  = ["SON","DJFM","AMJ"]

function extract_private(filein, ivar)

    data = ncread(filein, ivar)
    rlon = ncread(filein, "rlon")
    rlat = ncread(filein, "rlat")
    timev = ncread(filein, "time")
    longrid = ncread(filein, "lon")
    latgrid = ncread(filein, "lat")

    ds = Dataset(filein)

    dimension_dict = Dict(["lon" => "rlon", "lat" => "rlat"])

    timeattrib = Dict(ds["time"].attrib)

    timeattrib = Dict(["units"         => "days since 1850-1-1"
  "calendar"      => "365_day"
  "axis"          => "T"
  "long_name"     => "time"
  "standard_name" => "time"
  "bounds"        => "time_bnds"])

    grid_mapping = Dict(["grid_mapping" => "rotated_pole"])

    varattribs = Dict(["grid_mapping" => "rotated_pole"])

    dataax = AxisArray(data, Axis{Symbol(:rlon)}(rlon), Axis{Symbol(:rlat)}(rlat), Axis{:time}(timev))

    return ClimGrid(dataax, variable=ivar, longrid=longrid, latgrid=latgrid, dimension_dict=dimension_dict, grid_mapping=grid_mapping, timeattrib=timeattrib)


end

## LOOP ON REGIONS
for r = 1:length(regions_name)

    P = shapefile_coords_poly(polyshp.shapes[regions_number[r]])

    handle = open(shpfile, "r") do io
        read(io, Shapefile.Handle)
    end

    ## LOOP ON VARIABLES
    for v in var

        ## LOOP ON INDICES
        for i in indice

            ## LOOP ON SEASONS
            for s in season

                # define input and output files
                filein0      = string(path,v,"/",v,"_",i,"_",s,"_sorted0.nc")
                filein1      = string(path,v,"/",v,"_",i,"_",s,"_sorted1.nc")
                filein2      = string(path,v,"/",v,"_",i,"_",s,"_sorted2.nc")
                fileout0     = string(path,v,"/",v,"_",i,"_",s,"_sorted0_",regions_code[r],".nc")
                fileout1     = string(path,v,"/",v,"_",i,"_",s,"_sorted1_",regions_code[r],".nc")
                fileout2     = string(path,v,"/",v,"_",i,"_",s,"_sorted2_",regions_code[r],".nc")

                # masking data
                # var0 = load(filein0,i,poly=P)
                var0 = extract_private(filein0, i)
                var0 = spatialsubset(var0, P)
                write(var0, fileout0)
                var1 = extract_private(filein1, i)
                var1 = spatialsubset(var1, P)
                write(var1, fileout1)
                var2 = extract_private(filein2, i)
                var2 = spatialsubset(var2, P)
                write(var2, fileout2)
                # var1 = load(filein1,i,poly=P)
                # write(var1, fileout1)
                # var2 = load(filein2,i,poly=P)
                # write(var2, fileout2)
            end

        end
    end
end
