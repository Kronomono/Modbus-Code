
class Names:
    def get_name(self,index):
        self.index_to_name = {
            1: "Control Signal",2:"Control Signal LS2B",3:"Position",4:"Position LS2B",5:"Deviation",6:"Deviation LS2B",7:"Torque/Thrust",8:"Torque/Thrust LS2B",
            9:"Delta Pressure",10:"Open Pressure",11:"Close Pressure",12:"Pst Status",13:"Accumulator Pressure",14:"System Mode",15:"Last Event",16:"System Status",
            17:"Active Feedback",18:"Active Warnings",22:"Active Alarms",26:"Average Position Last 90 Days",27:"Average Position Last 90 Days LS2B",
            28:"Max Torque/Thrust Per Poll",29:"Max Torque/Thrust Per Poll LS2B",30:"Min Torque/ Thrust Per Poll",31:" Min Torque/Thurst Per Poll LS2B",
            32:"Max CW Torque Last 1hr",33:"Max CW Torque Last 1hr LS2B",34:"Min CW Torque Last 1hr",35:"Min CW Torque Last 1 hr LS2B",
            36:"Max CCW Torque Last 1hr",37:"Max CCW Torque Last 1hr  LS2B",38:"Min CCW Torque Last 1hr",39:"Min CCW Torque Last 1hr  LS2B",
            40:"Max CW Torque Last 4hr",41:"Max CW Torque Last 4hr  LS2B",42:"Min CW Torque Last 4hr",43:"Min CW Torque Last 4hr  LS2B",
            44:"Max CCW Torque Last 4hr",45:"Max CCW Torque Last 4 hr  LS2B",46:"Min CCW Torque Last 4hr",47:"Min CCW Torque Last 4hr  LS2B",
            48:"Max CW Torque Last 8hr",49:"Max CW Torque Last 8hr", 50:"Min CW Torque Last 8hr",51:"Min CW Torque Last 8hr  LS2B",52:"Max CCW Torque Last 8hr",
            53:"Max CCW Torque Last hr LS2B",54:"Min CCW Torque Last 8hr",55:"Min CCW Torque Last 8hr LS2B",56:"Max CW Torque Last 12hr",
            57:"Max CW Torque Last 12hr LS2B",58:"Min Cw Torque Last 12hr",59:"Min CW Torque Last 12hr LS2B",60:"Max CCW Torque Last 12hr",
            61:"Max CCW Torque Last 12hr  LS2B",62:"Min CCW Torque Last 12hr",63:"Min CCW Torque Last 12hr LS2B",64:"Max CW Torque Last 24 hr",
            65:"Max CW Torque Last 24hr LS2B",66:"Min CW Torque Last 24hr",67:"Min CW Torque Last 24hr LS2B",68:"Max CCW Torque Last 24hr",
            69:"Max CCW Torque Last 24hr LS2B",70:"Min CCW Torque Last 24hr",71:"Min CCW Torque Last 24hr LS2B",72:"Max Deviation Last 1hr",
            73:"Max Deviation Last 1hr LS2B",74:"Max Deviation Last 4hr",75:"Max Deviation Last 4hr LS2B",76:"Max Deviation Last 8hr",
            77:"Max Deviatoin Last 8hr LS2B",78:"Max Deviation Last 12hr",79:"Max Deviation Last 12hr LS2B",80:"Max Deviation Last 24hr",
            81:"Max Deviation Last 24hr LS2B",82:"Current Position Sensor Noise",83:"Actuator Drift Events Last 1hr",84:"Seating Events Last 1hr",85:"Primary Motor Starts Last 1hr",
            86:"Strokes Last 1hr",87:"Online Motor Starts Last 1hr",88:"Online Recharge Time Last 1hr",89:"Boost Motor Starts Last 1hr",
            90:"Actuator Drift Events Last 4hrs",91:"Seating Events Last 4hrs",92:"Primary Motor Starts Last 4hrs",93:"Strokes Last 4hrs",
            94:"Online Motor Starts Last 4hrs",95:"Online Recharge Time Last 4hrs",96:"Boost Motor Starts Last 4hrs",97:"Actuator Drift Events Last 8 hrs",
            98:"Seating Events Last 8hrs", 99:"Primary Motor Starts Last 8hrs",
            100:"Stroke Last 8hrs",101:"Online Motor Starts Last 8hrs",102:"Online Recharge Time Last 8hrs",103:"Boost Motor Starts Lst 8 hrs",
            104:"Actuator Drift Events Last 12hrs",105:"Seating Events Last 12hrs",106:"Primary Motor Starts Last 12hrs",107:"Strokes Last 12hrs",
            108:"Online Motor Starts Last 12hrs",109:"Online Recharge TIme Last 12hrs",110:"Boost Motor Starts Last 12hrs",111:"Actuator Drift Events Last 24hrs",
            112:"Seating Events last 24hrs",113:"Primary Motor Starts Last 24hrs",114:"Strokes Last 24hrs",115:"Online Motor Starts Last 24hrs",
            116:"Online Recharge Time Last 24hrs",117:"Boost Motor Starts Last 24hrs",118:"Position Low",119:"Position Low LS2B",
            120:"Position High",121:"Position High LS2B",122:"Position Low 2",123:"Position Low 2 LS2B",124:"Position High 2",125:"Position High 2 LS2B",
            126:"Signal Low",127:"Signal Low LS2B",128:"Signal High",129:"Signal High LS2B",130:"Failsafe Position",131:"Failsafe Position LS2B",
            132:"Min. Mod. Position",133:"Min. Mod. Position LS2B",134:"Calibrated Stroke",135:"Calibrated Stroke LS2B",136:"Booster Breakpoint",137:"Booster Breakpoint LS2B",
            138:"Deadband",139:"Deadband LS2B",140:"Speed Breakpoint",141:"Speed Breakpoint LS2B",142:"Surge Breakpoint",143:"Surge Breakpoint LS2B",
            144:"Surge Offpoint",145:"Surge Offpoint LS2B",146:"Relay 1 Setpoint",147:"Relay 1 Setpoint LS2B",148:"Relay 2 Setpoint",149:"Relay 2 Setpoint LS2B",
            150:"PST Increment",151:"PST Increment LS2B",152:"PST Large Increment",153:"PST Large Increment LS2B",154:"PST Signal Deviation",155:"PST Signal Deviation LS2B",
            156:"PST Offpoint",157:"PST Offpoint LS2B",158:"PST Target",159:"PST Target LS2B",160:"PST Max Target",161:"PST Max Target LS2B",
            162:"Transmitter Low",163:"Transmitter High",164:"Accumulator Recharge Time",
            165:"Accumulator Warning Pressure",166:"Accumulator Recharge Pressure",167:"Gain",168:"Max Down Speed",169:"Max Up Speed",170:"Max Manual Speed",
            171:"Delta Alarm Pressure",172:"Delta Warning Pressure",173:"PST Schedule Time",174:"PST Max RunTime",175:"Trip Mode",176:"Analog CS Enabled",
            177:"One-Contact Enabled",178:"Two-Contact Enabled",179:"Power-up Last Enabled",180:"Power-up Local Enabled",181:"Failsafe Position Enabled",
            182:"Failsafe In-Place Enabled",183:"Bumpless Transfer Enabled",184:"Minimum Modulation Enabled",185:"Solenoid Seating Enabled",
            186:"Contact Board Present",187:"Booster Motor Enabled",188:"Power Fail Accumulator Mode",189:"Power Fail In-Place Mode",190:"Accumulator Direction PL",
            191:"Accumulator Direction PH",192:"Two Speed Up/ Down Mode",193:"Two SPeed Breakpoint Mode",194:"Surge Enabled",195:"Surge Direction PL",
            196:"Surge Direction PH",197:"Surge Bi-Direction",198:"Mid-Point Relay Enabled",199:"Redundant CPU Present",200:"Reverse Acting Display",
            201:"Reverse Acting Transmitter",202:"PST Mode Contact Power",203:"PST MOde Signal Deviation",204:"PST Mode Schedule/Auto",205:"PSt Mode Contact Unpowered",
            206:"Model Character 1",207:"Model Character 2",208:"Model Character 3",209:"Model Character 4",210:"Model Character 5",211:"Model Character 6",
            212:"Model Character 7",213:"Model Character 8",214:"Model Character 9",215:"Model Character 10",216:"Model Character 11",217:"Model Character 12",
            218:"Model Character 13",219:"Model Character 14",220:"Model Character 15",221:"Model Character 16",222:"Model Character 17",223:"Model Character 18",
            224:"Model Character 19",225:"Model Character 20",226:"Model Character 21",227:"Model Character 22",228:"Model Character 23",229:"Model Character 24",
            230:"Model Character 25",231:"Tag Character 1",232:"Tag Character 2",233:"Tag Character 3",234:"Tag Character 4",235:"Tag Character 5",236:"Tag Character 6",
            237:"Tag Character 7",238:"Tag Character 8",239:"Tag Character 9",240:"Tag Character 10",241:"Tag Character 11",242:"Tag Character 12",243:"Tag Character 13",
            244:"Tag Character 14",245:"Tag Character 15",246:"Tag Character 16",247:"Tag Character 17",248:"Tag Character 18",249:"Tag Character 19",
            250:"Tag Character 20",251:"Tag Character 21",252:"Tag Character 22",253:"Tag Character 23",254:"Tag Character 24",255:"Tag Character 25",
            256:"Tag Character 26",257:"Tag Character 27",258:"Tag Character 28",259:"Tag Character 29",260:"Tag Character 30",261:"Tag Character 31",
            262:"Tag Character 32",263:"Serial Number Character 1",264:"Serial Number Character 2",265:"Serial Number Character 3",266:"Serial Number Character 4",
            267:"Serial Number Character 5",268:"Serial Number Character 6",269:"Serial Number Character 7",270:"Serial Number Character 8",
            271:"Serial Number Character 9",272:"Serial Number Character 10",273:"Serial Number Character 11",274:"Serial Number Character 12",
            275:"Serial Number Character 13",276:"Serial Number Character 14",277:"Software Version Character 1",278:"Software Version Character 2",
            279:"Software Version Character 3",280:"Software Version Character 4",281:"Software Version Character 5",282:"Software Version Character 6",
            283:"Software Version Character 7",284:"Software Version Character 8",285:"Software Version Character 9",286:"Software Version Character 10",
            287:"Software Version Character 11",288:"Software Version Character 12",289:"Software Version Character 13",290:"Software Version Character 14",
            291:"Display Version Character 1",292:"Display Version Character 2",293:"Display Version Character 3",294:"Display Version Character 4",
            295:"Display Version Character 5",296:"Display Version Character 6",297:"Display Version Character 7",298:"Display Version Character 8",
            299:"Display Version Character 9",300:"Display Version Character 10",301:"Display Version Character 11",302:"Display Version Character 12",
            303:"Display Version Character 13",304:"Display Version Character 14",305:"Current Day",306:"Current Month",307:"Current Year",308:"Current Hour",
            309:"Current Minute",310:"Current Second",311:"Commission Day",312:"Commission Month",313:"Commission Year",314:"Rated Rotation or Length",
            315:"Rated Rotation or Length LS2B",316:"Rated Output",317:"Rated Output LS2B",318:"Torque or Thrust",319:"Fault #1",320:"Fault #2",321:"Fault #3",
            322:"Fault #4",323:"Fault #5",324:"Fault #6",325:"Fault #7",326:"Fault #8",327:"Fault #9",328:"Fault #10",329:"Fault Time Stamp #1",330:"Fault Time Stamp #1 Next 2 Bytes",
            331:"Fault Time Stamp #1 Next 2 Bytes",332:"Fault Time Stamp #1 LS2B",333:"Fault Time Stamp #2",334:"Fault Time Stamp #2 Next 2 Bytes",
            335:"Fault Time Stamp #2 Next 2 Bytes",336:"Fault Time Stamp #2 LS2B",337:"Fault Time Stamp #3",338:"Fault Time Stamp #3 Next 2 Bytes",
            339:"Fault Time Stamp #3 Next 2 Bytes",340:"Fault Time Stamp #3 LS2B",341:"Fault Time Stamp #4",342:"Fault Time Stamp #4 Next 2 Bytes",
            343:"Fault Time Stamp #4 Next 2 Bytes",344:"Fault Time Stamp #4 LS2B",345:"Fault Time Stamp #5",346:"Fault Time Stamp #5 Next 2 Bytes",
            347:"Fault Time Stamp #5 Next 2 Bytes",348:"Fault Time Stamp #5 LS2B",349:"Fault Time Stamp #6",350:"Fault Time Stamp #6 Next 2 Bytes",
            351:"Fault Time Stamp #6 Next 2 Bytes",352:"Fault Time Stamp #6 LS2B",353:"Fault Time Stamp #7",354:"Fault Time Stamp #7 Next 2 Bytes",
            355:"Fault Time Stamp #7 Next 2 Bytes",356:"Fault Time Stamp #7 LS2B",357:"Fault Time Stamp #8",358:"Fault Time Stamp #8 Next 2 Bytes",
            359:"Fault Time Stamp #8 Next 2 Bytes",360:"Fault Time Stamp #8 LS2B",361:"Fault Time Stamp #9",362:"Fault Time Stamp #9 Next 2 Bytes",
            363:"Fault Time Stamp #9 Next 2 Bytes",364:"Fault Time Stamp #9 LS2B",
            365:"Fault Time Stamp #10",366:"Fault Time Stamp #10 Next 2 Bytes",367:"Fault Time Stamp #10 Next 2 Bytes",368:"Fault Time Stamp #10 LS2B",
            369:"Model Change #1",370:"Model Change #2",371:"Model Change #3",372:"Model Change #4",373:"Model Change #5",374:"Model Change #6",
            375:"Model Change #7",376:"Model Change #8",377:"Model Change #9",378:"Model Change #10",379:"Mode Change Time Stamp #1",
            380:"Mode Change Time Stamp #1 Next 2 Bytes",381:"Mode Change Time Stamp #1 Next 2 Bytes",382:"Mode Change Time Stamp #1 LS2B",
            383:"Mode Change Time Stamp #2",384:"Mode Change Time Stamp #2 Next 2 Bytes",385:"Mode Change Time Stamp #2 Next 2 Bytes",
            386:"Mode Change Time Stamp #2 LS2B",387:"Mode Change Time Stamp #3",388:"Mode Change Time Stamp #3 Next 2 Bytes",
            389:"Mode Change Time Stamp #3 Next 2 Bytes",390:"Mode Change Time Stamp #3 LS2B",391:"Mode Change Time Stamp #4",
            392:"Mode Change Time Stamp #4 Next 2 Bytes",393:"Mode Change Time Stamp #4 Next 2 Bytes",394:"Mode Change Time Stamp #4 LS2B",
            395:"Mode Change Time Stamp #5",396:"Mode Change Time Stamp #5 Next 2 Bytes",397:"Mode Change Time Stamp #5 Next 2 Bytes",
            398:"Mode Change Time Stamp #5 LS2B",399:"Mode Change Time Stamp #6",400:"Mode Change Time Stamp #6 Next 2 Bytes",
            401:"Mode Change Time Stamp #6 Next 2 Bytes",402:"Mode Change Time Stamp #6 LS2B",403:"Mode Change Time Stamp #7",
            404:"Mode Change Time Stamp #7 Next 2 Bytes",405:"Mode Change Time Stamp #7 Next 2 Bytes",406:"Mode Change Time Stamp #7 LS2B",
            407:"Mode Change Time Stamp #8",408:"Mode Change Time Stamp #8 Next 2 Bytes",409:"Mode Change Time Stamp #8 Next 2 Bytes",
            410:"Mode Change Time Stamp #8 LS2B",411:"Mode Change Time Stamp #9",412:"Mode Change Time Stamp #9 Next 2 Bytes",
            413:"Mode Change Time Stamp #9 Next 2 Bytes",414:"Mode Change Time Stamp #9 LS2B",
            415:"Mode Change Time Stamp #10",416:"Mode Change Time Stamp #10 Next 2 Bytes",417:"Mode Change Time Stamp #10 Next 2 Bytes",
            418:"Mode Change Time Stamp #10 LS2B",419:"Primary Servo Faults",420:"Dual Servo Faults",421:"Accumulator Servo Faults",
            422:"Boost Servo Faults",423:"Primary Stepper Faults",424:"Dual Stepper Faults",425:"Accumulator Stepper Faults",426:"Boost Induction Faults",
            427:"Dual Boost Induction Faults",428:"Primary Induction Faults",429:"Primary Feedback Bad",430:"Redundant Feedback Bad",431:"Control Signal Bad",
            432:"Stalls",433:"Direction Error",434:"+15V Failure",435:"-5V Failure",436:"Accumulator Pressure Bad",437:"Accumulator Pressure Low",
            438:"Output Limit Warning",439:"Accumulator Timeout",440:"Open Pressure Bad",441:"Closed Pressure Bad",442:"Seat Load Cylinder Feedback Bad",
            443:"Seat Load Cylinder Stop",444:"AC Voltage High",445:"Ac Voltage Low",446:"Clock Battery Low",447:"Output Limit Alarm",448:"Redundant Feedback Offset",
            449:"Invalid Hardware",450:"Invalid PST",451:"PST Time Elapsed",452:"Primary Servo Low Voltage  Faults",453:"Primary Servo Reokace Motor Faults",
            454:"Primary Servo Motor Temp Faults",455:"Primary Servo Resolver Faults",456:"Primary Servo Drive Temp Faults",457:"Primary Servo High Voltage Faults",
            458:"Primary Servo Overspeed Faults",459:"Primary Servo Motor Short Faults",460:"Primary Servo Replace Drive Faults",
            461:"Dual Servo Low Voltage Faults",462:"Dual Servo Replace Motor Faults",463:"Dual Servo Motor Temp Faults",464:"Dual Servo Resolver Faults",
            465:"Dual Servo Drive Temp Faults",466:"Dual Servo High Voltage Faults",467:"Dual Servo Overspeed Faults",468:"Dual Servo Motor Short Faults",
            469:"Dual Servo Replace Drive Faults",470:"Accumulator Servo Low Voltage Faults",471:"Accumulator Servo Replace Motor Faults",
            472:"Accumulator Servo Motor Temp Faults",473:"Accumulator Servo Resolver Faults",474:"Accumulator Servo Drive Temp Faults",
            475:"Accumulator Servo High Voltage Faults",476:"Accumulator Overspeed Faults",477:"Accumulator Servo Motor Short Faults",
            478:"Accumulator Servo Replace Drive Faults",479:"Boost Servo Low Voltage Faults",480:"Boost Servo Replace Motor Faults",
            481:"Boost Servo Motor Temp Faults",482:"Boost Servo Resolver Faults",483:"Boost Servo Resolver Faults",484:"Boost Servo High Voltage Faults",
            485:"Boost Servo Overspeed Faults",486:"Boost Servo Motor Short Faults",487:"Boost Servo Replace Drive Faults",488:"Comm Loss Faults",
            489:"Lifetime Primary Servo Faults",490:"Lifetime Dual Servo Faults",491:"Lifetime Accumulator Servo Faults",492:"Lifetime Boost Servo Faults",
            493:"Lifetime Primary Stepper Faults",494:"Lifetime Dual Stepper Faults",495:"Lifetime Accumulator Stepper Faults",
            496:"Lifetime Boost Induction Faults",497:"Lifetime Dual Boost Induction Faults",498:"Lifetime Primary Induction Faults",
            499:"Lifetime Primary Feedback Bad",500:"Lifetime Redundant Feedback Bad",501:"Lifetime Control Signal Bad",502:"Lifetime Stalls",
            503:"Lifetime Direction Error",504:"Lifetime +15V Failure",505:"Lifetime -5V Failure",506:"Lifetime Accumulator Pressure Bad",
            507:"Lifetime Accumulator Pressure Low",508:"Lifetime Output Limit Warning",509:"Lifetime Accumulator Timeout",510:"Lifetime Open Pressure Bad",
            511:"Lifetime Closed Pressure Bad",512:"Lifetime Seat Load Cylinder Feedback Bad",513:"Lifetime Seat Load Cylinder Stop",514:"Lifetime AC Voltage High",
            515:"Lifetime AC Voltage Low",516:"Lifetime Clock Battery Low",517:"Lifetime Output Limit Alarm",518:"Lifetime Redundant Feedback Offset",
            519:"Life Invalid Hardware",520:"Lifetime Invalid PST",521:"Lifetime PST Time Elapsed",522:"LifeTime Primary Servo Low Voltage Faults",
            523:"LifeTime Primary Servo Reokace Motor Faults",524:"Lifetime Primary Servo Motor Temp Faults",525:"Lifetime Primary Servo Resolver Faults",
            526:"Life Primary Servo Drive Temp Faults",527:"Lifetime primary Servo High Voltage Faults",528:"Lifetime Primary Servo Overspeed Faults",
            529:"Lifetime Primary Servo Motor Short Faults",530:"Lifetime Primary Servo Replace Drive Faults",531:"Lifetime Dual Servo Low Voltage Faults",
            532:"Lifetime Dual Servo Replace Motor Faults",533:"Lifetime Dual Servo Motor Temp Faults",534:"LifeTime Dual Servo resolver Faults",
            535:"Lifetime Dual Servo Drive Temp Faults",536:"Lifetime Dual Servo High Voltage Faults",537:"Lifetime Dual Servo Overspeed Faults",
            538:"Lifetime Dual Servo Motor Short Faults",539:"Lifetime Dual Servo Replace Drive Faults",540:"Lifetime Accumulator Servo Low Voltage Finds",
            541:"Lifetime Accumulator Servo Replace Motor Faults",542:"Lifetime Accumulator Servo Motor Temp Faults",543:"Lifetime Accumulator Servo Resolver Faults",
            544:"Lifetime Accumulator Servo Drive Temp Faults",545:"Lifetime Accumulator Servo High Voltage Faults",546:"Lifetime Accumulator Servo Overspeed Faults",
            547:"Lifetime Accumulator Servo Motor Short Faults",548:"Lifetime Accumulator Servo Replace Drive Faults",549:"Lifetime Boost Servo Low Voltage Faults",
            550:"Lifetime Boost Servo Replace Motor Faults",551:"Lifetime Boost Servo Motor Temp Faults",552:"Lifetime Boost Servo Reesolver Faults",
            553:"Lifetime Boost Servo Drive Temp Faults",554:"Lifetime Boost Servo High Voltage Faults",555:"Lifetime Boost Servo Overspeed Faults",
            556:"Lifetime Boost Servo Motor Short Faults",557:"Lifetime Boost Servo Replace Drive Faults",558:"Lifetime Comm Loss Faults",559:"Current Strokes 1K",
            560:"Current Strokes 1k LS2B",561:"Lifetime Strokes 1K",562:"Lifetime Strokes 1K LS2B",563:"Current Starts 1K",564:"Current Starts 1K LS2B",
            565:"Lifetime Starts 1K",566:"Lifetime Starts 1K LS2B",567:"Up Counter",568:"X3 Communication Active",569:"Host Write Enable",570:"Host Write Target",
            571:"Host Write Target LS2B"
        }
        return self.index_to_name.get(index, "No Name")
    def get_system_name(self, index):
        self.index_to_name = {1: "Auto Mode", 2: "Setup Mode",5: "Manual Mode"}
        return self.index_to_name.get(index,'Invalid Value')

    def get_status_name(self, index):
        self.index_to_name = {0: "Okay", 1: "Warning", 2: "Alarm"}
        return self.index_to_name.get(index, 'Invalid Value')

    def get_trip_name(self, index):
        self.index_to_name = {0: "Trip_OFF", 1: "TRIP_UNPOWERED_SOL", 2: "TRIP_POWERED_SOL",3:"TRIP_UNPOWERED_MOTOR_PL",
                              4:"TRIP_POWERED_MOTOR_PL",5:"TRIP_UNPOWERED_MOTOR_PH",6:"TRIP_POWERED_MOTOR_PH"}
        return self.index_to_name.get(index, 'Invalid Value')
    def get_error_name(self, index):
        self.index_to_name = {0:"NO_EVENT", 1:"PSRV_FAULT_EVENT",2:"DSRV_FAULT_EVENT",3:"ASRV_FAULT_EVENT",4:"BSRV_FAULT_EVENT",5:"PSTEP_FAULT_EVENT",
6:"DSTEP_FAULT_EVENT",7:"ASTEP_FAULT_EVENT",8:"BINDUC_FAULT_EVENT",9:"DBINDUC_FAULT_EVENT",10:"PINDUC_FAULT_EVENT",11:"MAIN_FB_BAD_EVENT",
12:"REDUN_FB_BAD_EVENT",13:"CS_BAD_EVENT",14:"STALL_EVENT",15:"DIR_ERROR_EVENT",16:"PLUS_15V_EVENT",17:"NEG_5V_EVENT",18:"APRESS_BAD_EVENT",
19:"APRESS_LOW_EVENT",20:"OUTPUT_WARNING_EVENT",21:"ACCUM_TIMEOUT_EVENT",22:"OPRESS_BAD_EVENT",23:"CPRESS_BAD_EVENT",24:"SLC_FB_BAD_EVENT",25:"SLC_STOP_EVENT",
26:"AC_HIGH_EVENT",27:"AC_LOW_EVENT",28:"CLK_BATT_LOW_EVENT",29:"OUTPUT_ALARM_EVENT",30:"FB_OFFSET_EVENT",31:"INVALID_HW_EVENT",32:"INVALID_PST_EVENT",
33:"PST_TIME_ELAPSED_EVENT",34:"PSRV_LOW_V_EVENT",35:"PSRV_MREPLACE_EVENT",36:"PSRV_MTEMP_EVENT",37:"PSRV_RFAULT_EVENT",38:"PSRV_DTEMP_EVENT",
39:"PSRV_HI_V_EVENT",40:"PSRV_OVERSPEED_EVENT",41:"PSRV_MSHORT_EVENT",42:"PSRV_DREPLACE_EVENT",43:"PSRV_UNUSED_EVENT",44:"DSRV_LOW_V_EVENT",45:"DSRV_MREPLACE_EVENT",
46:"DSRV_MTEMP_EVENT",47:"DSRV_RFAULT_EVENT",48:"DSRV_DTEMP_EVENT",49:"DSRV_HI_V_EVENT",50:"DSRV_OVERSPEED_EVENT",51:"DSRV_MSHORT_EVENT",52:"DSRV_DREPLACE_EVENT",
53:"DSRV_UNUSED_EVENT",54:"ASRV_LOW_V_EVENT",55:"ASRV_MREPLACE_EVENT",56:"ASRV_MTEMP_EVENT",57:"ASRV_RFAULT_EVENT",58:"ASRV_DTEMP_EVENT",59:"ASRV_HI_V_EVENT",
60:"ASRV_OVERSPEED_EVENT",61:"ASRV_MSHORT_EVENT",62:"ASRV_DREPLACE_EVENT",63:"ASRV_UNUSED_EVENT",64:"BSRV_LOW_V_EVENT",65:"BSRV_MREPLACE_EVENT",
66:"BSRV_MTEMP_EVENT",67:"BSRV_RFAULT_EVENT",68:"BSRV_DTEMP_EVENT",69:"BSRV_HI_V_EVENT",70:"BSRV_OVERSPEED_EVENT",71:"BSRV_MSHORT_EVENT",
72:"BSRV_DREPLACE_EVENT",73:"BSRV_UNUSED_EVENT",74:"COMM_LOSS_EVENT",129:"PSRV_FAULT_EVENT_CLEARED",130:"DSRV_FAULT_EVENT_CLEARED",131:"ASRV_FAULT_EVENT_CLEARED",
132:"BSRV_FAULT_EVENT_CLEARED",133:"PSTEP_FAULT_EVENT_CLEARED",134:"DSTEP_FAULT_EVENT_CLEARED",135:"ASTEP_FAULT_EVENT_CLEARED",136:"BINDUC_FAULT_EVENT_CLEARED",
137:"DBINDUC_FAULT_EVENT_CLEARED",138:"PINDUC_FAULT_EVENT_CLEARED",139:"MAIN_FB_BAD_EVENT_CLEARED",140:"REDUN_FB_BAD_EVENT_CLEARED",141:"CS_BAD_EVENT_CLEARED",
142:"STALL_EVENT_CLEARED",143:"DIR_ERROR_EVENT_CLEARED",144:"PLUS_15V_EVENT_CLEARED",145:"NEG_5V_EVENT_CLEARED",146:"APRESS_BAD_EVENT_CLEARED",147:"APRESS_LOW_EVENT_CLEARED",
148:"OUTPUT_WARNING_EVENT_CLEARED",149:"ACCUM_TIMEOUT_EVENT_CLEARED",150:"OPRESS_BAD_EVENT_CLEARED",151:"CPRESS_BAD_EVENT_CLEARED",152:"SLC_FB_BAD_EVENT_CLEARED",
153:"SLC_STOP_EVENT_CLEARED_CLEARED",154:"AC_HIGH_EVENT_CLEARED_CLEARED",155:"AC_LOW_EVENT_CLEARED",156:"CLK_BATT_LOW_EVENT_CLEARED",157:"OUTPUT_ALARM_EVENT_CLEARED",
158:"FB_OFFSET_EVENT_CLEARED",159:"INVALID_HW_EVENT_CLEARED",160:"INVALID_PST_EVENT_CLEARED",161:"PST_TIME_ELAPSED_EVENT_CLEARED",162:"PSRV_LOW_V_EVENT_CLEARED",
163:"PSRV_MREPLACE_EVENT_CLEARED",164:"PSRV_MTEMP_EVENT_CLEARED",165:"PSRV_RFAULT_EVENT_CLEARED",166:"PSRV_DTEMP_EVENT_CLEARED",167:"PSRV_HI_V_EVENT_CLEARED",
168:"PSRV_OVERSPEED_EVENT_CLEARED",169:"PSRV_MSHORT_EVENT_CLEARED",170:"PSRV_DREPLACE_EVENT_CLEARED",171:"PSRV_UNUSED_EVENT_CLEARED",172:"DSRV_LOW_V_EVENT_CLEARED",
173:"DSRV_MREPLACE_EVENT_CLEARED",174:"DSRV_MTEMP_EVENT_CLEARED",175:"DSRV_RFAULT_EVENT_CLEARED",176:"DSRV_DTEMP_EVENT_CLEARED",177:"DSRV_HI_V_EVENT_CLEARED",
178:"DSRV_OVERSPEED_EVENT_CLEARED",179:"DSRV_MSHORT_EVENT_CLEARED",180:"DSRV_DREPLACE_EVENT_CLEARED",181:"DSRV_UNUSED_EVENT_CLEARED",182:"ASRV_LOW_V_EVENT_CLEARED",
183:"ASRV_MREPLACE_EVENT_CLEARED",184:"ASRV_MTEMP_EVENT_CLEARED",185:"ASRV_RFAULT_EVENT_CLEARED",186:"ASRV_DTEMP_EVENT_CLEARED",187:"ASRV_HI_V_EVENT_CLEARED",
188:"ASRV_OVERSPEED_EVENT_CLEARED",189:"ASRV_MSHORT_EVENT_CLEARED",190:"ASRV_DREPLACE_EVENT_CLEARED",191:"ASRV_UNUSED_EVENT_CLEARED",192:"BSRV_LOW_V_EVENT_CLEARED",
193:"BSRV_MREPLACE_EVENT_CLEARED",194:"BSRV_MTEMP_EVENT_CLEARED",195:"BSRV_RFAULT_EVENT_CLEARED",196:"BSRV_DTEMP_EVENT_CLEARED",197:"BSRV_HI_V_EVENT_CLEARED",
198:"BSRV_OVERSPEED_EVENT_CLEARED",199:"BSRV_MSHORT_EVENT_CLEARED",200:"BSRV_DREPLACE_EVENT_CLEARED",201:"BSRV_UNUSED_EVENT_CLEARED",202:"COMM_LOSS_EVENT_CLEARED"}

        return self.index_to_name.get(index, 'Invalid Value')











