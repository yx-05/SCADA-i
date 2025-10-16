import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import '../services/mqtt_service.dart';
import 'profile_page.dart';

class OccupancyPage extends StatefulWidget {
  const OccupancyPage({super.key});

  @override
  State<OccupancyPage> createState() => _OccupancyPageState();
}

class _OccupancyPageState extends State<OccupancyPage> {
  String selectedRow = "Row A";
  final mqtt = MQTTService();
  Map<String, dynamic>? liveData;

  final Map<String, List<SeatStatus>> seatData = {
    "Row A": List.filled(4, SeatStatus.available),
    "Row B": List.filled(3, SeatStatus.available),
    "Row C": List.filled(2, SeatStatus.available),
    "Row D": List.filled(5, SeatStatus.available),
    "Row E": List.filled(2, SeatStatus.available),
    "Row F": List.filled(2, SeatStatus.available),
  };

  @override
  void initState() {
    super.initState();
    mqtt.connect();
    mqtt.dataStream.listen((data) {
      setState(() {
        liveData = data;
        if (data['rows'] != null) {
          final rows = data['rows'] as Map<String, dynamic>;
          for (final rowKey in rows.keys) {
            final rowList = (rows[rowKey] as List)
                .map((x) => x == 1 ? SeatStatus.occupied : SeatStatus.available)
                .toList();
            seatData["Row $rowKey"] = rowList;
          }
        } else if (data['occupancy'] != null) {
          final total = data['occupancy'] as int;
          final row = seatData["Row A"]!;
          for (int i = 0; i < row.length; i++) {
            row[i] = i < total ? SeatStatus.occupied : SeatStatus.available;
          }
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final key = selectedRow.trim();
    final currentSeats = seatData[key] ?? [];
    final int totalSeats = currentSeats.length;
    final int occupiedSeats =
        currentSeats.where((s) => s == SeatStatus.occupied).length;
    final double occupancy =
    totalSeats == 0 ? 0.0 : occupiedSeats / totalSeats;

    final double? temp = liveData?['temperature']?.toDouble();
    final int? liveOccupancy = liveData?['occupancy']?.toInt();

    return ScreenUtilInit(
      designSize: const Size(390, 844),
      minTextAdapt: true,
      builder: (context, child) => Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          backgroundColor: const Color(0xFF222831),
          automaticallyImplyLeading: false,
          title: Text(
            "Occupancy",
            style: TextStyle(fontSize: 17.sp, fontWeight: FontWeight.w500),
          ),
          foregroundColor: Colors.white,
          actions: [
            Padding(
              padding: EdgeInsets.only(right: 16.w),
              child: GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => const ProfilePage()),
                  );
                },
                child: Row(
                  children: [
                    Icon(Icons.person_outline,
                        color: Colors.white, size: 22.sp),
                    SizedBox(width: 5.w),
                    Text("Profile",
                        style: TextStyle(
                            color: Colors.white, fontSize: 15.sp)),
                  ],
                ),
              ),
            ),
          ],
        ),

        // ---------- Body ----------
        body: Padding(
          padding: EdgeInsets.all(20.w),
          child: SingleChildScrollView(
            child: Column(
              children: [
                // Dropdown
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 14.w),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20.r),
                    border: Border.all(color: Colors.black87, width: 2.w),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: selectedRow,
                      icon: Icon(Icons.keyboard_arrow_down,
                          color: Colors.black54, size: 24.sp),
                      dropdownColor: Colors.white,
                      style: TextStyle(
                          color: Colors.black54,
                          fontSize: 17.sp,
                          fontWeight: FontWeight.w500),
                      isExpanded: true,
                      items: const [
                        DropdownMenuItem(value: "Row A", child: Text("Row A")),
                        DropdownMenuItem(value: "Row B", child: Text("Row B")),
                        DropdownMenuItem(value: "Row C", child: Text("Row C")),
                        DropdownMenuItem(value: "Row D", child: Text("Row D")),
                        DropdownMenuItem(value: "Row E", child: Text("Row E")),
                        DropdownMenuItem(value: "Row F", child: Text("Row F")),
                      ],
                      onChanged: (value) =>
                          setState(() => selectedRow = value ?? "Row A"),
                    ),
                  ),
                ),
                SizedBox(height: 25.h),

                // Info Card
                Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFF5c5b63),
                    borderRadius: BorderRadius.circular(10.r),
                  ),
                  padding: EdgeInsets.all(12.w),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Icon(Icons.location_on, color: Colors.white, size: 20),
                          const SizedBox(width: 8),
                          Flexible( // 👈 prevents overflow
                            child: Text(
                              "Location: 365 Silent PC Room",
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 17,
                                fontWeight: FontWeight.w500,
                              ),
                              softWrap: true,
                              overflow: TextOverflow.fade, // fades gently if still long
                            ),
                          ),
                        ],
                      ),

                      SizedBox(height: 5.h),
                      Row(children: [
                        Icon(Icons.thermostat,
                            color: Colors.white, size: 20.sp),
                        SizedBox(width: 8.w),
                        Text(
                          "Temperature: ${temp?.toStringAsFixed(1) ?? '--'}°C",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 17.sp,
                              fontWeight: FontWeight.w500),
                        ),
                      ]),
                      SizedBox(height: 5.h),
                      Row(children: [
                        Icon(Icons.people, color: Colors.white, size: 20.sp),
                        SizedBox(width: 8.w),
                        Text(
                          "Occupancy: ${liveOccupancy ?? occupiedSeats}/$totalSeats",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 17.sp,
                              fontWeight: FontWeight.w500),
                        ),
                      ]),
                    ],
                  ),
                ),
                SizedBox(height: 25.h),

                // Seat Layout
                _fitCanvas(_buildRowLayout(selectedRow)),
                SizedBox(height: 22.h),


                // Status
                Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFF37353f),
                    borderRadius: BorderRadius.circular(10.r),
                  ),
                  padding:
                  EdgeInsets.symmetric(horizontal: 15.w, vertical: 10.h),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(selectedRow,
                          style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w600,
                              fontSize: 17.sp)),
                      SizedBox(height: 10.h),
                      LinearProgressIndicator(
                        value: occupancy,
                        backgroundColor: Colors.grey,
                        color: occupancy == 1.0
                            ? Colors.red
                            : (occupancy >= 0.5
                            ? Colors.yellow
                            : const Color(0xFF3cfb34)),
                        minHeight: 6.h,
                      ),
                      SizedBox(height: 10.h),
                      Text("${(occupancy * 100).toStringAsFixed(0)}% occupied",
                          style: TextStyle(
                              color: Colors.white70,
                              fontSize: 15.sp,
                              fontWeight: FontWeight.w500))
                    ],
                  ),
                ),
                SizedBox(height: 30.h),

                // Back Button
                SizedBox(
                  width: 350.w,
                  height: 65.h,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF222831),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.r),
                      ),
                    ),
                    onPressed: () => Navigator.pop(context),
                    child: Text(
                      "Back to Main Menu",
                      style: TextStyle(
                        fontSize: 19.sp,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // fixed-size canvas
  Widget _fitCanvas(Widget child) => Center(
    child: FittedBox(
      fit: BoxFit.contain,
      child: SizedBox(width: 390, height: 350, child: child),
    ),
  );

  // select correct row
  Widget _buildRowLayout(String row) {
    final s = seatData[row]!;
    switch (row) {
      case "Row A":
        return _buildRowA(s);
      case "Row B":
        return _buildRowB(s);
      case "Row C":
        return _buildRowC(s);
      case "Row D":
        return _buildRowD(s);
      case "Row E":
        return _buildRowE(s);
      case "Row F":
        return _buildRowF(s);
      default:
        return const SizedBox.shrink();
    }
  }

// Row layouts (unchanged positions)
  Widget _buildRowA(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Center(
      child: Transform.translate(
        offset: const Offset(60, 100),
        child: Transform.rotate(
          angle: -0.55,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _SeatWithTable(label: "A01", status: s[0]),
              SizedBox(width: 25.w),
              _SeatWithTable(label: "A02", status: s[1]),
              SizedBox(width: 25.w),
              _SeatWithTable(label: "A03", status: s[2]),
              SizedBox(width: 25.w),
              _SeatWithTable(label: "A04", status: s[3]),
            ],
          ),
        ),
      ),
    ),
  );


  Widget _buildRowB(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Stack(alignment: Alignment.center, children: [
      Transform.rotate(
        angle: -2.15,
        child: Row(mainAxisSize: MainAxisSize.min, children: const [
          _TableBox(),
          SizedBox(width: 6),
          _TableBox(),
        ]),
      ),
      Positioned(top: 73, left: 190, child: _SeatCircle(label: "B01", status: s[0])),
      Positioned(top: 145, right: 90, child: _SeatCircle(label: "B02", status: s[1])),
      Positioned(bottom: 20, left: 230, child: _SeatCircle(label: "B03", status: s[2])),
    ]),
  );

  Widget _buildRowC(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Row(mainAxisAlignment: MainAxisAlignment.center, children: const [
        _TableBox(),
        SizedBox(width: 20),
        _TableBox(),
      ]),
      SizedBox(height: 15.h),
      Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        _SeatCircle(label: "C01", status: s[0]),
        SizedBox(width: 35.w),
        _SeatCircle(label: "C02", status: s[1]),
      ]),
    ]),
  );

  Widget _buildRowD(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Stack(alignment: Alignment.center, children: [
      Positioned(
          top: 150,
          left: 110,
          child: Transform.rotate(
              angle: -0.6,
              child: Container(
                  height: 35,
                  width: 160,
                  decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(6)),
                  alignment: Alignment.center,
                  child: Text("TABLE",
                      style: TextStyle(
                          fontSize: 13.sp,
                          fontWeight: FontWeight.bold,
                          color: Colors.black54))))),
      Positioned(bottom: 50, left: 50, child: _SeatCircle(label: "D01", status: s[0])),
      Positioned(bottom: 155, left: 75, child: _SeatCircle(label: "D02", status: s[1])),
      Positioned(top: 65, left: 150, child: _SeatCircle(label: "D03", status: s[2])),
      Positioned(bottom: 30, right: 170, child: _SeatCircle(label: "D04", status: s[3])),
      Positioned(top: 180, right: 100, child: _SeatCircle(label: "D05", status: s[4])),
    ]),
  );

  Widget _buildRowE(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Stack(alignment: Alignment.center, children: [
      Positioned(
          top: 140,
          child: Transform.rotate(
              angle: 0.7,
              child: Row(mainAxisSize: MainAxisSize.min, children: const [
                _TableBox(),
                SizedBox(width: 8),
                _TableBox(),
              ]))),
      Positioned(bottom: 120, left: 90, child: _SeatCircle(label: "E01", status: s[0])),
      Positioned(bottom: 62, right: 170, child: _SeatCircle(label: "E02", status: s[1])),
    ]),
  );

  Widget _buildRowF(List<SeatStatus> s) => Container(
    decoration: BoxDecoration(
      color: const Color(0xFF4a4950),
      borderRadius: BorderRadius.circular(15.r),
    ),
    child: Stack(alignment: Alignment.center, children: [
      Positioned(
          top: 130,
          child: Transform.rotate(
              angle: 2.5,
              child: Row(mainAxisSize: MainAxisSize.min, children: const [
                _TableBox(),
                SizedBox(width: 8),
                _TableBox(),
              ]))),
      Positioned(left: 75, bottom: 170, child: _SeatCircle(label: "F01", status: s[0])),
      Positioned(right: 180, top: 40, child: _SeatCircle(label: "F02", status: s[1])),
    ]),
  );
}

/* ------------ Helper Widgets ------------ */
enum SeatStatus { available, occupied }

class _TableBox extends StatelessWidget {
  const _TableBox({super.key});
  @override
  Widget build(BuildContext context) => Container(
    height: 40,
    width: 80,
    alignment: Alignment.center,
    decoration: BoxDecoration(
        color: Colors.grey[300],
        borderRadius: BorderRadius.circular(6)),
    child: Text("TABLE",
        style: TextStyle(
            fontSize: 13.sp,
            fontWeight: FontWeight.bold,
            color: Colors.black54)),
  );
}

class _SeatCircle extends StatelessWidget {
  final String label;
  final SeatStatus? status;
  const _SeatCircle({super.key, required this.label, this.status});

  @override
  Widget build(BuildContext context) {
    final seatColor = status == SeatStatus.occupied
        ? const Color(0xFFc5c5c5)
        : const Color(0xFF3cfb34);
    return Column(children: [
      Container(
          height: 60,
          width: 60,
          decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: seatColor,
              border: Border.all(color: Colors.black54, width: 1.5)),
          child: Center(
              child: Text(label,
                  style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 16.sp,
                      color: Colors.black)))),
      SizedBox(height: 6.h),
      Text(label,
          style: TextStyle(
              fontSize: 14.sp,
              fontWeight: FontWeight.w500,
              color: Colors.white)),
    ]);
  }
}

class _SeatWithTable extends StatelessWidget {
  final String label;
  final SeatStatus status;
  const _SeatWithTable({required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    final seatColor = status == SeatStatus.occupied
        ? const Color(0xFFc5c5c5)
        : const Color(0xFF3cfb34);
    return Column(children: [
      Container(
        height: 35,
        width: 60,
        alignment: Alignment.center,
        decoration: BoxDecoration(
            color: Colors.grey[300], borderRadius: BorderRadius.circular(5)),
        child: Text("TABLE",
            style: TextStyle(
                fontSize: 13.sp,
                fontWeight: FontWeight.w700,
                color: Colors.black54)),
      ),
      SizedBox(height: 10.h),
      Container(
          height: 60,
          width: 60,
          decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: seatColor,
              border: Border.all(color: Colors.black54, width: 1.5)),
          child: Center(
              child: Text(label,
                  style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 16.sp,
                      color: Colors.black)))),
      SizedBox(height: 6.h),
      Text(label,
          style: TextStyle(
              fontSize: 14.sp,
              fontWeight: FontWeight.w500,
              color: Colors.white)),
    ]);
  }
}
