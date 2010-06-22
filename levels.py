# C = Nut
# P = Normal platform
# L = Slope going left
# R = Slope going right
# B = Enemy
# Q = Normal block
# F = Falling block
# S = Spring
# . = Nothing
# Y = Moving platform going UP
# U = Moving platform going DOWN
# I = Moving platform going RIGHT
# O = Moving platform going LEFT


BLANK = [
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
list("............................................................"),
]

LEVEL1 = [
list("...................."),
list("...................."),
list("...................."),
list("............CC......"),
list("CC..........CC...CC."),
list("CC...............CC."),
list("....U....B..PP....B."),
list("PR.....LPP..PP..PPPP"),
list("PPPP...PPP......PPPP"),
]

LEVEL2 = [
list(".............................."),
list(".............................."),
list(".............................."),
list(".............................."),
list("......CCC.B.CC...CCC.........."),
list("......CCC...CC...CPPR.....CC.."),
list("CCC....B........CCPPPRB...CC.B"),
list("PPP.B.PPP...PP..PPPPPPR.....LP"),
list("PPPPPPPPP...PP..PPPPPPP...PPPP"),
]

LEVEL3 = [
list("............................................................"),
list("............................................................"),
list("......C....................................................."),
list("..PP..QC...................................................."),
list("PPPP...QC........CBB.............BBB.Q...........CCC....CC.."),
list("PPP.....Q.......CLPP......CC.....QQQQQ.CC........CCC....CC.."),
list("PP..........CCCCLPPP......PRCCCPP......PPC........B.....BB.."),
list("............PPPPPPPP......PPPPPPP......PPPC.....LPPPR...PP.."),
list("............PPPPPPPP..S...PPPPPPP......PPPP...PPPPPPPPPPPPPP"),
]

LEVEL4 = [
list(".......................B...................................."),
list("....................CC................CC...................."),
list("..............CCC...CC................PRC..................."),
list(".........B....CCC...BB................PPRCB................."),
list(".......CLPP...PPP..BPP................PPPPP.....CC.........."),
list("......CLPPP...PPP..PPP........CC.....SQQQPPQ.CC..B.........."),
list("....CCLPPPP........PPP.......CPPRB..QQQ..QQQ.CC.PRB.......CC"),
list("P...PPPPPPP..............CC..PPPPR.........Q....PPRB...CCLPP"),
list("PP..PPPPPPP..............PP..PPPPP.........PPPPPPPPR..LPPPPP"),
]

LEVEL5 = [
list("............................................................................CCC..........................."),
list("............................................................................CCC...BCCCC..................."),
list("..............................B......CCC..CCC..........B.....................B....PPPPPP...CC............."),
list(".............................BQ......CCC..CCC.........B............B........PPP...PPPPPPP..CC...........CC"),
list(".............CCC.............QQ.......BB.............CC...CC......CC........PPPP...B..QPPP..BB..........CC"),
list("......B.CCC..CCC...........CCCCC.....QQQ..QQQ........QQ...CC.....CLP.....CC...PP.CCC..QPPPPPPPR...CCC...BB"),
list("CCCLPR..CCC.BQQQ..........CLPPPRCCBBQPPQQQPPQ.....CCCQ..........CLPPR....CC......PPP..QPPQPPPPP...CCC..LPP"),
list("PPPPPPP...BBPPPPPRB..B...CLPPPPPPPQQQPPP..PPPPP...QQQQ....PP...CLPPPPR......B.B..PPP..QPPPPPQPPR......LPPP"),
list("PPPPPPPPPPPPPPPPPPPPPP...PPPPPPPPPPPPPPP..PPPPP...........PPPPPPPPPPPP..PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"),
]

LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5]
