import geopandas as gpd
import pandas as pd

# Little helper function for later



############
# Import pre-cleaned HIFLD polygons
############

def string_punc(test_str):

    punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""

    try:

        test_str = str(test_str).lower()
        # print(test_str)
        for ele in test_str:
            if ele in punc:
                test_str = test_str.replace(ele, "")
        processed_lst = []
        for word in test_str.split():
            if word not in ["the", "at", "in", "and", "of"]:
                processed_lst.append(word)

        test_str = " ".join(processed_lst)
        test_str = test_str.replace(" ", "")
        return test_str.lower()
    except:
        return "Null"

#import the geo_df and master_df
geo_df = gpd.read_file("../../20_intermediate_files/10_HIFLD_campus_polygons.geojson")
master_df = pd.read_csv( "../../00_source_data/PlusOne_College_Demographic_Data/SLSV Master Campus Sheet - Master Sheet.csv",
    header=1,
)
print("Original Master:", len(master_df))

#applying the string punctuations
master_df["preprocessed_name"] = master_df["School Name"].apply(string_punc)
geo_df["preprocessed_name"] = geo_df["preprocessed_name"].apply(string_punc)
master_df=master_df.drop_duplicates()
master_df = master_df[
    ~master_df["preprocessed_name"].str.contains(
        "policy|law|phd|graduate|grad|health|medicine|medical"
        "|music|business|nursing|film|art|arts|design|commerce",
        regex=True,
    )
]

#Helping to remove the Many to Many Match
master_df=master_df[master_df['IPED ID']!='Hawaii Community College']
master_df=master_df[master_df['IPED ID']!='485263.00']
master_df=master_df[master_df['IPED ID']!='101949.00']
master_df = master_df[master_df['IPED ID'] != '155636.00']

geo_df = geo_df.loc[~geo_df.duplicated(['preprocessed_name', "STATE"])]

geo_df=geo_df[geo_df['UNIQUEID']!='459082']
geo_df=geo_df[geo_df['UNIQUEID']!='241128']

print("Updated Master:", len(master_df))


# Hand subs
subs = [
    ("AL", "georgecwallacecommunitycollege", "georgecwallacecommunitycollegedothan"),
    ("AL", "jfdrakestatetechnicalcollege", "jfdrakestatecommunitytechnicalcollege"),
    ("AL", "troyuniversityalabama", "troyuniversity"),
    ("AL", "wallacecommunitycollegeselma", "georgecwallacestatecommunitycollegeselma"),
    ("AL","hcouncilltrenholmstatetechnicalcollegepatterson","trenholmstatetechnicalcollege")
    ("AL","universityalabamasystemoffice","universityalabamatuscaloosa")
    ("AR","arkansasstateuniversitymaincampus","arkansasstateuniversity")
    ("AR","collegeouachitas","collegequachitas")
    ("AR","cossatotcommunitycollegeuniversityarkansas","cossatotcommunitycollege")
    ("AR","southernarkansasuniversitymaincampus","southernarkansasuniversity")
    ("AR","southernarkansasuniversitytech","southernarkansasuniversitytechnical")
    ("AR","universityarkansascommunitycollegebatesville","universityarkansasccbatesville")
    ("AR","universityarkansascommunitycollegemorrilton","universityarkansasccmorrilton")
    ("AR","universityarkansas","universityarkansasfayetteville")
    ("AR","universityarkansascommunitycollegehope","universityarkansashope")
    ("AZ","arizonastateuniversitytempe","arizonastateuniversity")
    ("AZ","cochisecountycommunitycollegedistrict","cochisecollegecommunitycollegedistrict")
    ("AZ","riosaladocollege","riosaladocommunitycollege")
    ("CA","universityarizonasouth","universityarizonasierravista")
    ("CA","alliantinternationaluniversitysandiego","alliantinternationaluniversity")
    ("CA","californiastateuniversitymaritimeacademy","californiamaritimeacademy")
    ("CA","californiapolytechnicstateuniversitysanluisobispo","californiapolytechnicstateuniversity")
    ("CA","cerrocosocommunitycollege","cerrocososkerncommunitycollegedistrict")
    ("CA","chicagoschoolprofessionalpsychologylosangeles","chicagoschoolprofessionalpsychology")
    ("CA","cogswellcollege","cogswellpolytechnicalcollege")
    ("CA","concordiauniversityirvine","concordiauniversity")
    ("CA","cuestacollege","cuestacommunitycollege")
    ("CA","elcaminocommunitycollegedistrict","elcaminocollege")
    ("CA","featherrivercommunitycollegedistrict","featherrivercollege")
    ("CA","goldengateuniversitysanfrancisco","goldengateuniversity")
    ("CA","humphreysuniversitystocktonmodestocampuses","humphreyscollege")
    ("CA","losangelesortcollegevannuyscampus","losangelesortcollegelosangelescampus")
    ("CA","mercedcollege","mercedcommunitycollege")
    ("CA","mtsanantoniocollege","mountsanantoniocollege")
    ("CA","mtsanjacintocommunitycollegedistrict","mountsanjacintocollege")
    ("CA","palomarcollege","palomarcommunitycollege")
    ("CA","samuelmerrittuniversity","samuelmerrittcollege")
    ("CO","coloradostateuniversityfortcollins","coloradostateuniversity")
    ("CO","coloradotechnicaluniversitycoloradosprings","coloradotechnicaluniversity")
    ("CO","universitycoloradodenveranschutzmedicalcampus","universitycoloradodenver")
    ("CO","westernstatecoloradouniversity","westerncoloradouniversity")
    ("CT","middlesexcommunitycollege","middlesexcommunitycollegeconnecticut")
    ("CT","stvincentscollege","saintvincentscollege")
    ("FL","baptistcollegeflorida","baptistcollege")
    ("FL","carlosalbizuuniversitymiami","carlosalbizuuniversitymiamicampus")
    ("FL","embryriddleaeronauticaluniversitydaytonabeach","embryriddleaeronauticaluniversity")
    ("FL","embryriddleaeronauticaluniversityworldwide","embryriddleaeronauticaluniversityworldwidecampus")
    ("FL","flaglercollegestaugustine","flaglercollege")
    ("FL","herzinguniversitywinterpark","herzinguniversityorlando")
    ("FL","palmbeachatlanticuniversity","palmbeachatlanticcollege")
    ("FL","saintjohnsriverstatecollege","stjohnsriverstatecollege")
    ("FL","universitysouthfloridamaincampus","universitysouthflorida")
    ("GA","bainbridgestatecollege","bainbridgecollege")
    ("GA","emoryuniversityoxfordcollege","emoryuniversityoxford")
    ("GA","reinhardtuniversity","reinhardtcollege")
    ("GA","southuniversitysavannah","southuniversity")
    ("HI","universityhawaiimanoa","universityhawai ªimƒÅnoa")
    ("IA","briarcliffuniversity","briarcliffcollege")
    ("IA","gracelanduniversitylamoni","gracelanduniversity")
    ("IA","iowawesleyanuniversity","iowawesleyancollege")
    ("IA","northeastiowacommunitycollege","northeastiowacommunitycollegecalmar")
    ("IA","palmercollegechiropractic","palmercollege")
    ("IA","westerniowatechcommunitycollege","westerniowatechnicalcommunitycollege")
    ("ID","stevenshenagercollege","stevenshenagerboise")
    ("IL","chicagoschoolprofessionalpsychologychicago","chicagoschoolprofessionalpsychology")
    ("IL","citycollegeschicagoharrystrumancollege","citychicagoharrystrumancollege")
    ("IL","citycollegeschicagokennedykingcollege","citychicagokennedykingcollege")
    ("IL","citycollegeschicagomalcolmxcollege","citychicagomalcolmxcollege")
    ("IL","citycollegeschicagooliveharveycollege","citychicagooliveharveycollege")
    ("IL","citycollegeschicagorichardjdaleycollege","citychicagorichardjdaleycollege")
    ("IL","citycollegeschicagowilburwrightcollege","citychicagowrightcollege")
    ("IL","concordiauniversitychicago","concordiauniversity")
    ("IL","greenvilleuniversity","greenvillecollege")
    ("IL","midwesternuniversitydownersgrove","midwesternuniversity")
    ("IL","robertmorrisuniversityillinois","robertmorrisuniversity")
    ("IL","rockforduniversity","rockfordcollege")
    ("IL","wheatoncollege","wheatoncollegeillinois")
    ("IN","bethelcollegeindiana","bethelcollege")
    ("IN","calumetcollegesaintjoseph","calumetcollegestjoseph")
    ("IN","gracecollegetheologicalseminary","gracecollege")
    ("IN","indianawesleyanuniversitymarion","indianawesleyanuniversity")
    ("IN","purdueuniversitymaincampus","purdueuniversitywestlafayette")
    ("IN","saintmaryofthewoodscollege","saintmarywoods")
    ("IN","universitysaintfrancisfortwayne","universitysaintfrancis")
    ("KS","bethelcollegenorthnewton","bethelcollege")
    ("KS","newmanuniversity","newmanuniversitywichita")
    ("KS","ottawauniversityottawa","ottawauniversity")
    ("KS","sewardcountycommunitycollege","sewardcommunitycollege")
    ("KY","beckfieldcollegeflorence","beckfieldcollege")
    ("KY","elizabethtowncommunitytechnicalcollege","elizabethtowncommunitycollege")
    ("KY","hazardcommunitytechnicalcollege","hazardcommunitycollege")
    ("KY","kentuckychristianuniversity","kentuckychristiancollege")
    ("KY","maysvillecommunitytechnicalcollege","maysvillecommunitycollege")
    ("KY","southeastkentuckycommunitytechnicalcollege","southeastcommunitycollege")
    ("LA","centrallouisianatechnicalcommunitycollege","centrallouisianatechnicalcollege")
    ("LA","herzinguniversitykenner","herzinguniversityneworleans")
    ("LA","louisianastateuniversityagriculturalmechanicalcollege","louisianastateuniversitybatonrouge")
    ("LA","northshoretechnicalcommunitycollege","northshoretechnicalcollege")
    ("LA","northwesternstateuniversitylouisiana","northwesternstateuniversity")
    ("LA","tulaneuniversitylouisiana","tulaneuniversity")
    ("MA", "laselluniversity", "lasellcollege")
    ("MA", "middlesexcommunitycollegemassachusetts", "middlesexcommunitycollege")
    ("MA", "wheatoncollegemassachusetts", "wheatoncollege")
    ("MD", "cecilcommunitycollege", "cecilcollege")
    ("MD", "universitymarylandglobalcampus", "universitymarylanduniversitycollege")
    ("MI", "cornerstonecollege", "cornerstoneuniversity")
    ("MI", "saintclaircountycommunitycollege", "stclaircountycommunitycollege")
    ("MN", "anokaramseycommunitycollegecoonsrapids", "anokaramseycommunitycollege")
    ("MN", "betheluniversityminnesota", "betheluniversity")
    ("MN", "centrallakescollege", "centrallakescollegebrainerd")
    ("MN", "centrallakescollegestaplescampus", "centrallakescollegebrainerdstaplescampus")
    ("MN", "collegestscholastica", "collegesaintscholastica")
    ("MN", "concordiacollege", "concordiacollegemoorhead")
    ("MN", "mesabirangecommunitytechnicalcollegeeveleth", "mesabirangecommunitytechnicalcollegeevelethcampus")
    ("MN", "mesabirangecommunitytechnicalcollegevirginia", "mesabirangecollege")
    ("MN", "minneapoliscollege", "minneapoliscollegeartdesign")
    ("MN", "minnesotastatecommunitytechnicalcollegedetroitlakes", "minnesotastatecommunitytechnicalcollegedetroitlakescampus")
    ("MN", "minnesotastatecommunitytechnicalcollegemoorhead", "minnesotastatecommunitytechnicalcollegemoorheadcampus")
    ("MN", "minnesotawestcommunitytechnicalcollegejackson", "minnesotawestcommunitytechnicalcollegejacksoncampus")
    ("MN", "minnesotawestcommunitytechnicalcollegepipestone", "minnesotawestcommunitytechnicalcollegepipestonecampus")
    ("MN", "pinetechnicalcollege", "pinetechnicalcommunitycollege")
    ("MN", "ridgewatercollegehutchinson", "ridgewatercollegehutchinsoncampus")
    ("MN", "riverlandcommunitycollegeowatonna", "riverlandcommunitycollegeowatonnacampus")
    ("MN", "southcentralcollegefaribault", "southcentralcollegefaribaultcampus")
    ("MN", "stcatherineuniversitystpaul", "stcatherineuniversity")
    ("MO", "avilacollege", "avilauniversity")
    ("MO", "barnesjewishcollege", "barnesjewishcollegegoldfarbschoolnursing")
    ("MO", "centralmethodistuniversity", "centralmethodistuniversitycollegegraduateextendedstudies")
    ("MO", "columbiacollegemo", "columbiacollege")
    ("MO", "evangelcollege", "evangeluniversity")
    ("MO", "maryvilleuniversity", "maryvilleuniversitysaintlouis")
    ("MO", "metropolitancommunitycollege", "metropolitancommunitycollegekansascity")
    ("MO", "missouristateuniversity", "missouristateuniversityspringfield")
    ("MO", "saintlouiscommunitycollegeforestpark", "saintlouiscommunitycollegeforestparkcampus")
    ("MO", "saintlouiscommunitycollegemeramec", "saintlouiscommunitycollegemerameccampus")
    ("MO", "threeriverscommunitycollege", "threeriverscollege")
    ("MO", "williamjewelcollege", "williamjewellcollege")
    ("MS", "mississippigulfcoastcollegegautier", "mississippigulfcoastcommunitycollegejacksoncountycampus")
    ("MS", "mississippigulfcoastcollegegulfport", "mississippigulfcoastcommunitycollegejeffersondaviscampus")
    ("MS", "mississippigulfcoastcollegeperkinston", "mississippigulfcoastcommunitycollege")
    ("MT", "montanastateuniversitybozeman", "montanastateuniversity")
    ("MT", "montanatechnicaluniversitymontana", "montanatechnologicaluniversity")
    ("NC", "collegeabemarle", "collegealbemarle")
    ("NC", "cravencountycommunitycollege", "cravencommunitycollege")
    ("NC", "methodistcollege", "methodistuniversity")
    ("NC", "northcarolinastateuniversity", "northcarolinastateuniversityraleigh")
    ("NC", "pfeiffercollege", "pfeifferuniversity")
    ("NC", "southeasternbaptisttheologicalsem", "southeasternbaptisttheologicalseminary")
    ("NC", "wingatecollege", "wingateuniversity")
    ("ND", "northdakotastateuniversity", "northdakotastateuniversitymaincampus")
    ("NE", "centralcommunitycollegegrandisland", "centralcommunitycollege")
    ("NE", "concordiauniversity", "concordiauniversitynebraska")
    ("NE", "doaneuniversity", "doaneuniversityartssciences")
    ("NE", "metrocommunitycollege", "metropolitancommunitycollegeareasouthomahacampus")
    ("NE", "nebraskamethodistcollege", "nebraskamethodistcollegenursingalliedhealth")
    ("NE", "southeastcommunitycollegebeatrice", "southeastcommunitycollegeareabeatricecampus")
    ("NE", "southeastcommunitycollegelincoln", "southeastcommunitycollegeareaeducationsquarecampus")
    ("NE", "southeastcommunitycollegemilford", "southeastcommunitycollegeareamilfordcampus")
    ("NE", "westernnebraskacommunitycollegesidney", "westernnebraskacommunitycollegesidneycampus")
    ("NH", "universitynewhampshire", "universitynewhampshiremaincampus")
    ("NJ", "berkeleycollege", "berkeleycollegewoodlandpark")
    ("NJ", "collegestelizabeth", "collegesaintelizabeth")
    ("NJ", "fairleighdickinsonuniversity", "fairleighdickinsonuniversitymetropolitancampus")
    ("NJ", "feliciancollege", "felicianuniversity")
    ("NJ", "hudsoncommunitycollege", "hudsoncountycommunitycollege")
    ("NJ", "middlesexcountycollege", "middlesexcountycommunitycollege")
    ("NJ", "ramapocollege", "ramapocollegenewjersey")
    ("NJ", "newjerseycityuniversity", "newjerseycityuniversity")
    ("NM", "easternnewmexicouniversity", "easternnewmexicouniversitymaincampus")
    ("NM", "easternnewmexicouniversityruidosocampus", "easternnewmexicouniversityroswellcampus")
    ("NM", "navajotechnicalcollege", "navajotechnicaluniversity")
    ("NM", "newmexicostateuniversity", "newmexicostateuniversitymaincampus")
    ("NM", "universitynewmexico", "universitynewmexicomaincampus")
    ("NV", "tourouniversity", "tourouniversitynevada")
    ("NY", "americanacademymcallisterinstitute", "americanacademymcallisterinstitutefuneralservice")
    ("NY", "columbiauniversity", "columbiauniversitycitynewyork")
    ("NY", "concordiacollege", "concordiacollegenewyork")
    ("NY", "cooperunion", "cooperunionforadvancementscienceart")
    ("NY", "cunybaruchcollege", "cunybernardmbaruchcollege")
    ("NY", "cunyjohnjaycollege", "cunyjohnjaycollegecriminaljustice")
    ("NY", "dominicancollege", "dominicancollegeblauvelt")
    ("NY", "mariacollege", "mariacollegealbany")
    ("NY", "mildredelleyschool", "mildredelleyschoolalbanycampus")
    ("NY", "monroecollegenewrochelle", "monroecollegenewrochellecampus")
    ("NY", "nazarethcollegerochester", "nazarethcollege")
    ("NY", "paceuniversitypleasantville", "paceuniversitynewyorkpleasantvillecampus")
    ("NY", "paceuniversitywhiteplains", "paceuniversitynewyorkschoollawcampus")
    ("NY", "paulsmithscollege", "paulsmithscollegeartsscience")
    ("NY", "prattinstitute", "prattinstitutemain")
    ("NY", "stellacharlesguttmancommunitycollegecuny", "stellacharlesguttmancommunitycollege")
    ("NY", "stjohnfishercollege", "saintjohnfishercollege")
    ("NY", "stjohnsuniversity", "stjohnsuniversitynewyork")
    ("NY", "stjosephscollege", "stjosephscollegenewyork")
    ("NY", "sunyalfredstatecollege", "sunycollegetechnologyalfred")
    ("NY", "sunycollegecortland", "sunycortland")
    ("NY", "sunycollegefredonia", "sunyfredonia")
    ("NY", "sunycollegeoneonta", "sunyoneonta")
    ("NY", "sunycollegepurchase", "sunypurchasecollege")
    ("NY", "sunymaritimecollegefortschulyler", "sunymaritimecollege")
    ("OH", "bowlinggreenstateuniversity", "bowlinggreenstateuniversitymaincampus")
    ("OH", "cincinnatistatetechnicalcollege", "cincinnatistatetechnicalcommunitycollege")
    ("OH", "cuyahogacommunitycollege", "cuyahogacommunitycollegedistrict")
    ("OH", "edisoncommunitycollege", "edisonstatecommunitycollege")
    ("OH", "franciscanuniversity", "franciscanuniversitysteubenville")
    ("OH", "hockingtechnicalcollege", "hockingcollege")
    ("OH", "kentstateuniversity", "kentstateuniversitykent")
    ("OH", "miamiuniversity", "miamiuniversityoxford")
    ("OH", "miamiuniversityregionals", "miamiuniversityhamilton")
    ("OH", "mountstjosephuniversity", "mountsaintjosephuniversity")
    ("OH", "muskingumcollege", "muskingumuniversity")
    ("OH", "northcentraltechnicalcollege", "northcentralstatecollege")
    ("OH", "ohiostateuniversity", "ohiostateuniversitymaincampus")
    ("OH", "ohiostateuniversitylima", "ohiostateuniversitylimacampus")
    ("OH", "ohiostateuniversitymansfield", "ohiostateuniversitymansfieldcampus")
    ("OH", "ohiostateuniversitymarion", "ohiostateuniversitymarioncampus")
    ("OH", "ohiostateuniversitynewark", "ohiostateuniversitynewarkcampus")
    ("OH", "ohiouniversity", "ohiouniversitymaincampus")
    ("OH", "universityakron", "universityakronmaincampus")
    ("OH", "unioninstitute", "unioninstituteuniversity")
    ("OH", "universitycincinnati", "universitycincinnatimaincampus")
    ("OH", "wrightstateuniversity", "wrightstateuniversitymaincampus")
    ("OH", "miamiuniversityhamilton", "miamiuniversityhamilton")
    ("OK", "oklahomastateuniversitystillwater", "oklahomastateuniversitymaincampus")
    ("OK", "universityoklahoma", "universityoklahomanormancampus")
    ("OR", "concordiauniversity", "concordiauniversityportland")
    ("OR", "klamathcollege", "klamathcommunitycollege")
    ("OR", "linfieldcollege", "linfieldcollegemcminnvillecampus")
    ("OR", "warnerpacificcollege", "warnerpacificuniversity")
    ("PA", "cairnuniversity", "cairnuniversitylanghorne")
    ("PA", "eaststroudsburguniversity", "eaststroudsburguniversitypennsylvania")
    ("PA", "gwynedmercyuniversity", "gwyneddmercyuniversity")
    ("PA", "immaculatacollege", "immaculatauniversity")
    ("PA", "indianauniversitypennsylvania", "indianauniversitypennsylvaniamaincampus")
    ("PA", "kutztownuniversity", "kutztownuniversitypennsylvania")
    ("PA", "larochecollege", "larocheuniversity")
    ("PA", "lehighcountycommunitycollege", "lehighcarboncommunitycollege")
    ("PA", "misercordiauniversity", "misericordiauniversity")
    ("PA", "northhamptoncommunitycollege", "northamptoncountyareacommunitycollege")
    ("PA", "pennsylvaniastateuniversity", "pennsylvaniastateuniversitymaincampus")
    ("PA", "saintfranciscollege", "saintfrancisuniversity")
    ("PA", "shippensburguniversity", "shippensburguniversitypennsylvania")
    ("PA", "slipperyrockuniversity", "slipperyrockuniversitypennsylvania")
    ("PA", "universitypittsburgh", "universitypittsburghpittsburghcampus")
    ("PA", "universitysciencesphiladelphia", "universitysciences")
    ("PA", "waynesburgcollege", "waynesburguniversity")
    ("PA", "westchesteruniversity", "westchesteruniversitypennsylvania")
    ("PA", "wideneruniversitychester", "wideneruniversity")
    ("PA", "yorkcountyschooltechnology", "yticareerinstituteyork")
    ("RI", "johnstonwalesuniversity", "johnsonwalesuniversityprovidence")
    ("RI", "salvereginacollege", "salvereginauniversity")
    ("SC", "citadel", "citadelmilitarycollegesouthcarolina")
    ("SD", "augustanacollege", "augustanauniversity")
    ("TN", "bryancollege", "bryancollegedayton")
    ("TN", "tennesseewesleyancollege", "tennesseewesleyanuniversity")
    ("TN", "tusculumcollege", "tusculumuniversity")
    ("TX", "austincommunitycollege", "austincommunitycollegedistrict")
    ("TX", "baptistuniversityamericas", "baptisthealthsystemschoolhealthprofessions")
    ("TX", "collegebiblicalstudies", "collegebiblicalstudieshouston")
    ("TX", "collincountycommunitycollege", "collincountycommunitycollegedistrict")
    ("TX", "jacksonvillecollege", "jacksonvillecollegemaincampus")
    ("TX", "sanjacintocollege", "sanjacintocommunitycollege")
    ("TX", "sulrossuniversity", "sulrossstateuniversity")
    ("TX", "tarrantcountycollege", "tarrantcountycollegedistrict")
    ("TX", "texasamuniversity", "texasamuniversitycollegestation")
    ("TX", "texasstatetechnicalcollegewaco", "texasstatetechnicalcollege")
    ("TX", "universitysaintthomas", "universitystthomas")
    ("TX", "vernonregionaljuniorcollege", "vernoncollege")
    ("UT", "ameritechcollegeheathcaredraper", "ameritechcollegedraper")
    ("UT", "brighamyounguniversity", "brighamyounguniversityprovo")
    ("UT", "davisappliedtechnologycollege", "davistechnicalcollege")
    ("UT", "stevenshenagerstgeorge", "stevenshenagercollegestgeorgeutahcampus")
    ("UT", "stevenshenagerindependenceuniversity", "stevenshenagercollege")
    ("UT", "westminstercollegesaltlake", "westminstercollege")
    ("VA", "bridgewateruniversity", "bridgewatercollege")
    ("VA", "dabneylancastercommunitycollege", "dabneyslancastercommunitycollege")
    ("VA", "hollinscollege", "hollinsuniversity")
    ("VA", "universityvirginia", "universityvirginiamaincampus")
    ("VA", "virginiauniversitylynchburg", "universitylynchburg")
    ("VT", "castletonstatecollege", "castletonuniversity")
    ("VT", "marlborocollege", "marlborocollegegraduateprofessionalstudies")
    ("VT", "stmichaelscollege", "saintmichaelscollege")
    ("WA", "greenrivercommunitycollege", "greenrivercollege")
    ("WA", "highlinecommunitycollege", "highlinecollege")
    ("WA", "piercecollegedistrict", "piercecollegefortsteilacoom")
    ("WA", "universitywashingtonbothell", "universitywashingtonbothellcampus")
    ("WA", "universitywashingtonseattle", "universitywashingtonseattlecampus")
    ("WA", "universitywashingtontacoma", "universitywashingtontacomacampus")
    ("WA", "washingtonstateuniversitypullman", "washingtonstateuniversity")
    ("WA", "yakimavalleycommunitycollege", "yakimavalleycollege")
    ("WI", "concordiauniversity", "concordiauniversitywisconsin")
    ("WI", "eastwestuniversity", "eastwesthealingartsinstitutemilwaukee")
    ("WI", "universitywisconsinbaraboo", "universitywisconsincollegesbaraboosaukcounty")
    ("WI", "universitywisconsinbarron", "universitywisconsincollegesbarroncounty")
    ("WI", "universitywisconsinfonddulac", "universitywisconsincollegesfonddulac")
    ("WI", "universitywisconsinfoxvalley", "universitywisconsincollegesfoxvalley")
    ("WI", "universitywisconsinmanitowoc", "universitywisconsincollegesmanitowoc")
    ("WI", "universitywisconsinmarathon", "universitywisconsincollegesmarathoncounty")
    ("WI", "universitywisconsinmarshfield", "universitywisconsincollegesmarshfieldwoodcounty")
    ("WI", "universitywisconsinrock", "universitywisconsincollegesrockcounty")
    ("WI", "universitywisconsinsheboygan", "universitywisconsincollegessheboygan")
    ("WI", "universitywisconsinwashington", "universitywisconsincollegeswashingtoncounty")
    ("WI", "universitywisconsinwaukesha", "universitywisconsincollegeswaukesha")
    ("WI", "wisconsinindianheadtechnicalcollegeashland", "wisconsinindianheadtechnicalcollegeashlandcampus")
    ("WI", "wisconsinindianheadtechnicalcollegenewrichmond", "wisconsinindianheadtechnicalcollegenewrichmondcampus")
    ("WI", "wisconsinindianheadtechnicalcollegericelake", "wisconsinindianheadtechnicalcollegericelakecampus")
    ("WI", "wisconsinindianheadtechnicalcollegesuperior", "wisconsinindianheadtechnicalcollegesuperiorcampus")
    ("WV", "easternwestvirginiacommunitytechcollege", "easternwestvirginiacommunitytechnicalcollege")
    ("WV", "fairmontstatecollege", "fairmontstateuniversity")
    ("WV", "westlibertycountycommunitycollege", "westlibertyuniversity")
    ("WV", "westvirginiawesleyan", "westvirginiawesleyancollege")

]

for s in subs:
    master_df.loc[
        (master_df.State == s[0]) & (master_df.preprocessed_name == s[1]),
        "preprocessed_name",
    ] = s[2]


print("Length of Master Table:", len(master_df))
merged_data = geo_df.merge(
    master_df,
    left_on = ['preprocessed_name', 'STATE'],
    right_on = ['preprocessed_name', 'State'],
    how="inner",
    indicator=True,
    validate='1:1'
)

# Drop do inner -- do outer, check
# results so you can see what happened,
# then drop
merged_data._merge.value_counts()

final_data = merged_data[merged_data._merge == "both"]

print("Length of Merged Table:", len(final_data))

final_data = final_data.drop_duplicates(subset="NAME", keep="first")

# This you now get as a full dataset (without this run time)
# from your `merged_data._merge == "left"` or `merged_data._merge == "right"`
# results
# not_merged = set(master_df["preprocessed_name"]) - set(final_data["preprocessed_name"])
# not_merged = not_merged.tolist()

not_merged = merged_data[merged_data._merge != "both"]
not_merged = pd.DataFrame(not_merged)
not_merged.to_csv("../../20_intermediate_files/15_polygons_not_merged_w_demographics.csv")

print("Length of Merged Table without duplicates:", len(final_data))

final_data = final_data.drop("_merge", axis="columns")
final_data.to_file("../../20_intermediate_files/20_campus_polygons_w_demographics.geojson")


