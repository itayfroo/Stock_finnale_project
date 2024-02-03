israeli_cities = [
    "Jerusalem",
    "Tel Aviv",
    "Haifa",
    "Rishon LeZion",
    "Petah Tikva",
    "Ashdod",
    "Netanya",
    "Beersheba",
    "Holon",
    "Bnei Brak",
    "Rehovot",
    "Bat Yam",
    "Kfar Saba",
    "Herzliya",
    "Modi'in",
    "Nazareth",
    "Eilat",
    "Acre",
    "Ramla",
    "Lod",
    "Tiberias",
    "Safed",
    "Dimona",
    "Yavne",
    "Ra'anana",
    "Kiryat Gat",
    "Hadera",
    "Nahariya",
    "Afula",
    "Kiryat Shmona",
    "Givatayim",
    "Ra's al-Ayn",
    "Ma'alot-Tarshiha",
    "Qalansawe",
    "Umm al-Fahm",
    "Kiryat Motzkin",
    "Tamra",
    "Yehud-Monosson",
    "Karmiel",
    "Netivot",
    "Sderot",
    "Arad",
    "Hod HaSharon",
    "Katzrin",
    "Rosh HaAyin",
    "Migdal HaEmek",
    "Beit Shemesh",
    "Qiryat Atta",
    "Qiryat Ono",
    "Or Yehuda",
    "Giv'at Shmuel",
    "Qiryat Bialik",
    "Kiryat Yam",
    "Et Tira",
    "Qiryat Mozkin",
    "Kiryat Malakhi",
    "Migdal Oz",
    "Lehavot HaBashan",
    "Yokneam",
    "Tirat Zvi",
    "Kafr Qara",
    "Elyakhin",
    "Kfar Sumei",
    "Zikhron Ya'akov",
    "Beit Yitzhak-Sha'ar Hefer",
    "Even Yehuda",
    "Tayibe",
    "Qiryat Gat",
    "Mazkeret Batya",
    "Pardesiyya",
    "Zefat",
    "Sakhnin",
    "Tirah",
    "Mevo Betar",
    "Tira",
    "Shatul",
    "Ar'arat an-Naqab",
    "Liman",
    "Tiberias",
    "Barta'a",
    "Zemer",
    "Shefa-'Amr",
    "Bene Ayish",
    "Tiberias",
    "Daliyat al-Karmel",
    "Pardes Hanna-Karkur",
    "Giv'atayim",
    "El'ad",
    "Sde Warburg",
    "Kafr Kanna",
    "Kafr Manda",
    "Kuseife",
    "Lehavim",
    "Kfar Yona",
    "Kfar Habad",
    "Kfar Aza",
    "Eilat",
    "Tzoran-Kadima",
    "Afula",
    "Petaẖ Tiqwa",
    "Netanya",
    "Bnei Brak",
    "Jaffa",
    "Ramat Gan",
    "Holon",
    "Rishon LeZion",
    "Bat Yam",
    "Ashdod",
    "Haifa",
    "Jerusalem",
    "Beer Sheba",
    "Hadera",
    "Modi'in",
    "Kfar Saba",
    "Be'er Sheva",
    "Hod HaSharon",
    "Ra'anana",
    "Herzliya",
    "Petah Tikva",
    "Qiryat Atta",
    "Rosh HaAyin",
    "Netivot",
    "Bet Shemesh",
    "Nazareth",
    "Ashkelon",
    "Rehovot",
    "Yavne",
    "Gedera",
    "Lod",
    "Qiryat Gat",
    "Ramat HaSharon",
    "Ramat-Gan",
    "Tiberias",
    "Dimona",
    "Kiryat Shmona",
    "Lachish",
    "Yeruham",
    "Sderot",
    "Arad",
    "Nahariya",
    "Karmiel",
    "Tamra",
    "Beit She'an",
    "Afula",
    "Qiryat Shemona",
    "Herzliya Pituah",
    "Mazkeret Batya",
    "Holon",
    "Beit Yehoshua",
    "Qiryat Tiv'on",
    "Yahud",
    "Reineh",
    "Kefar Habad",
    "Talmei Yosef",
    "Ne'ot HaKikar",
    "Kfar Pines",
    "Binyamina",
    "Yitzhar",
    "Kokhav Yair",
    "Betar Illit",
    "Yiron",
    "Savyon",
    "Karnei Shomron",
    "Kfar HaOranim",
    "Karnei Shomron",
    "Har Adar",
    "Yanuv",
    "Nirit",
    "Beit Arif",
    "Bareqet",
    "Kfar Monash",
    "Nili",
    "Talmon",
    "Ein Ayala",
    "Kfar Yedidia",
    "Pedu'el",
    "Tlamim",
    "Carmel City",
    "Re'im",
    "Kiryat Arba",
    "Alfe Menashe",
    "Roi",
    "Alon Shvut",
    "Ma'ale Levona",
    "Hinnanit",
    "Kiryat Netafim",
    "Sal'it",
    "Tomer",
    "Netiv HaAsara",
    "Nofim",
    "Barkan",
    "Talmei Bilu",
    "Nofit",
    "Neve Ziv",
    "Beit Aryeh",
    "Mevo Dotan",
    "Yitav",
    "Netzer Hazani",
    "Netzer Sereni",
    "Pnei Kedem",
    "Yakir",
    "Sde David",
    "Kfar Tavor",
    "Yated",
    "Nitzan",
    "Eshhar",
    "Aderet",
    "Ramat Magshimim",
    "Meir Shfeya",
    "Almagor",
    "Bnei Yehuda",
    "HaZor'im",
    "Leshem",
    "Ma'ale Michmas",
    "Mevo Horon",
    "Mevo Modi'im",
    "Modi'im Illit",
    "Nof Ayalon",
    "Nofit",
    "Paduel",
    "Poriya",
    "Ravid",
    "Ramat Rachel",
    "Shekef",
    "Susya",
    "Yarhiv",
    "Yavne'el",
    "Zohar",
    "Adirim",
    "Ahihud",
    "Ahuzam",
    "Alon HaGalil",
    "Aluma",
    "Amnun",
    "Amuka",
    "Ani'am",
    "Arbel",
    "Ar'ara",
    "Arraba",
    "Ashdot Ya'akov Ihud",
    "Ashdot Ya'akov Meuhad",
    "Asherat",
    "Atsmon",
    "Avdon",
    "Avi'el",
    "Avivim",
    "Avnei Eitan",
    "Ayanot",
    "Azor",
    "Bahan",
    "Bar Giora",
    "Bar Yohai",
    "Bar'am",
    "Barak",
    "Baraq",
    "Barqay",
    "Batsra",
    "Batzra",
    "Be'erotayim",
    "Be'er Tuvia",
    "Be'er Ya'akov",
    "Beka'ot",
    "Bene Ayish",
    "Bene Darom",
    "Bene Re'em",
    "Bene Zekharya",
    "Betzet",
    "Betzet",
    "Birki",
    "Birya",
    "Bizzaron",
    "Bnei Aish",
    "Bnei Atarot",
    "Bnei Barak",
    "Bnei Brak",
    "Bnei Darom",
    "Bnei Dror",
    "Bnei Efraim",
    "Bnei Yehuda",
    "Bnei Zion",
    "Boqeq",
    "Brosh",
    "Bruchin",
    "Bukata",
    "Burayka",
    "Bustan HaGalil"]