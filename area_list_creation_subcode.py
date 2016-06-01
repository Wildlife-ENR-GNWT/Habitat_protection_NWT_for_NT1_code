lst =[[u'Inuvialuit'],
 [u'Sahtu',
  [u'Travaillant Uplands', 18701.122195613283],
  [u'Colville Upland Lakes', 11281.026801281658],
  [u'Fort Anderson Trail Lakes', 21788.95194461923],
  [u'Bear Rock', 3284.9680132985027],
  [u'Turton Lake', 7869.474971823244],
  [u'Chick Lake', 3613.5271233481685],
  [u'Yamoga Rock', 9218.633725566599],
  [u'Mio Lake', 1891.2326240360096],
  [u'Doctor Lake', 2084.600281662335],
  [u'Three Day Lake', 3232.6995081011787],
  [u'Kelly and Lennie Lake', 20468.751234714447],
  [u'Sam McCrae Lake', 5937.580897602612],
  [u'Mountain River', 29664.128572607347],
  [u'Lac Des Bois', 52915.80188774555],
  [u'Tunago Lake', 11916.107535924424],
  [u'unknown', 745.9188985884523],
  [u'Kelly Lake Protected Area (Land Claim)', 27259.801426082617],
  [u'Willow Lake Wetlands', 24529.380470673226],
  [u'Lac a Jacques', 12309.609792631481],
  [u'Whitefish River', 143694.8471944613],
  [u'Mahoney Lake', 23221.475120529944],
  [u'Anderson River', 41476.073002984784],
  [u'Aubrey Dunedelatue', 66502.31196863293],
  [u'Johnny Hoe River (Teh Kaicho De)', 403643.1611147639],
  [u'Maunoir Dome', 55172.57639708355],
  [u'Oscar Lake', 7024.682502178451],
  [u'Lac Belot', 41467.66133753603],
  [u'Edannla', 216243.88177068497],
  [u'Fossil Lake', 18406.82705343613],
  [u'Sentinel Islands CZ', 2.9981130205776543],
  [u'Dene Di Gone', 1245.3230126791289],
  [u'Where the Wolf Crosses', 282.23595871118897],
  [u'Mackenzie River Islands', 4997.467253163532]],
 [u'North_Slave',
  [u'Habitat Management Zone', 9074.50738562512],
  [u'Traditional Use Zone', 158184.31245302453],
  [u'Cultural Heritage Zone', 465041.4641334341]],
 [u'Dehcho', [u'Johnny Hoe River (Teh Kaicho De)', 8069.058832664516]],
 [u'South_Slave'],
 [u'Gwichin',
  [u"Gwich'in permanent withdrawal", 11815.072126430852],
  [u'Heritage Conservation Zone', 13454.596693448282],
  [u"Gwich'in Conservation Zone", 248751.38541425252]],
 [u'Yukon']]

master_lst = []
for item in lst:
    if len(item) > 1:
        subitem = item[1:len(item)]
        for i in range(len(subitem)):
            Region = item[0]
            Area_Name = subitem[i][0]
            Type = "full"
            Area_Hectares = subitem[i][1]
            entry = [Region, Area_Name, Type, Area_Hectares]
            master_lst.append(entry)

# It works!
