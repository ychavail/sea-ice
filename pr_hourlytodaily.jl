# chargement des packages
using ClimateTools, Glob, Shapefile, AxisArrays, ProgressMeter, Dates

# shapefile pour masque sur le QC
shpfile = "/home/yanncha/GitHub/sea-ice/masking/prov_la_p_geo83_f.shp"
polyshp = read(shpfile,Shapefile.Handle)
P = shapefile_coords_poly(polyshp.shapes[498])

# initialisation
prefix = "/klmx1/leduc/climex-core-qc/"
repout = "/exec/yanncha/sea_ice/pr/daily/"
years = [2095:2099]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
# "kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi",
sims = ["kdj","kdk", "kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx", "kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek", "kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]


# fichier de sortie de commentaires pendant la compilation
fileprint   = "/home/yanncha/GitHub/sea-ice/outputs_from_code/pr_hourlytodaily.txt"
io          = open(fileprint,"a")

# boucle sur les vecteurs d'années
for vec_years in years
    # boucle sur les simulations ClimEx
    for isim in sims

        fileout = string(repout,"pr_daily_",isim,"_",vec_years[1],"-",vec_years[end],".nc")

        nfiles = length(vec_years)*length(months)
        prday = Array{ClimGrid}(undef, nfiles)
        datesort = Array{DateTimeNoLeap}(undef, nfiles)
        global Cout = []

        # boucle sur les fichiers mensuels
        global z = 1
        for iyear in vec_years
            for imonth in months
                files = glob("*pr_*nc", string(prefix,isim,"/series/",iyear,imonth,"/"))
                io          = open(fileprint,"a")
                println(io, files)
                close(io)
                println(files)
                pr = load(files[1], "pr", poly=P)
                prday[z] = daysum(pr)
                datesort[z] = get_timevec(prday[z])[1]
                global z += 1
            end
        end

        # tri selon l'axe des temps
        #idx = sortperm(datesort)
        #rday = prday[idx]

        # écriture d'un fichier par simulation
        for imod = 1:nfiles
            if imod == 1
                global Cout = prday[imod]
            else
                global Cout = merge(Cout, prday[imod])
            end
            # next!(p)
        end
        write(Cout, fileout)
    end
end
