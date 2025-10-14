import 'package:flutter/material.dart';
import '../services/mqtt_service.dart';
import 'profile_page.dart'; // for Profile navigation

class OccupancyPage extends StatefulWidget {
  const OccupancyPage({super.key});

  @override
  State<OccupancyPage> createState() => _OccupancyPageState();
}

class _OccupancyPageState extends State<OccupancyPage> {
  String selectedRow = "Row A";
  final mqtt = MQTTService();
  Map<String, dynamic>? liveData;

  // ✅ Default: all seats available
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

    // ✅ Listen for live MQTT data
    mqtt.dataStream.listen((data) {
      setState(() {
        liveData = data;

        // If IoT sends detailed seat data per row
        if (data['rows'] != null) {
          final rows = data['rows'] as Map<String, dynamic>;
          for (final rowKey in rows.keys) {
            final rowList = (rows[rowKey] as List)
                .map((x) => x == 1 ? SeatStatus.occupied : SeatStatus.available)
                .toList();
            seatData["Row $rowKey"] = rowList;
          }
        }

        // If only total occupancy number is sent (fallback demo)
        else if (data['occupancy'] != null) {
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

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: const Color(0xFF222831),
        automaticallyImplyLeading: false,
        title: const Text(
          "Occupancy",
          style: TextStyle(fontSize: 17, fontWeight: FontWeight.w500),
        ),
        foregroundColor: Colors.white,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const ProfilePage()),
                );
              },
              child: Row(
                children: const [
                  Icon(Icons.person_outline, color: Colors.white, size: 22),
                  SizedBox(width: 5),
                  Text("Profile",
                      style: TextStyle(color: Colors.white, fontSize: 15)),
                ],
              ),
            ),
          ),
        ],
      ),

      // ---------- Body ----------
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // ---------- Dropdown ----------
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.black87, width: 2),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: selectedRow,
                    icon: const Icon(Icons.keyboard_arrow_down,
                        color: Colors.black54),
                    dropdownColor: Colors.white,
                    style: const TextStyle(
                      color: Colors.black54,
                      fontSize: 17,
                      fontWeight: FontWeight.w500,
                    ),
                    isExpanded: true,
                    alignment: Alignment.center,
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
              const SizedBox(height: 25),

              // ---------- Info Card ----------
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF5c5b63),
                  borderRadius: BorderRadius.circular(10),
                ),
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(children: [
                      Icon(Icons.location_on, color: Colors.white, size: 20),
                      SizedBox(width: 8),
                      Text("Location: 365 Silent PC Room",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 17,
                              fontWeight: FontWeight.w500)),
                    ]),
                    const SizedBox(height: 5),
                    Row(children: [
                      const Icon(Icons.thermostat,
                          color: Colors.white, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        "Temperature: ${temp?.toStringAsFixed(1) ?? '--'}°C",
                        style: const TextStyle(
                            color: Colors.white,
                            fontSize: 17,
                            fontWeight: FontWeight.w500),
                      ),
                    ]),
                    const SizedBox(height: 5),
                    Row(children: [
                      const Icon(Icons.people, color: Colors.white, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        "Occupancy: ${liveOccupancy ?? occupiedSeats}/$totalSeats",
                        style: const TextStyle(
                            color: Colors.white,
                            fontSize: 17,
                            fontWeight: FontWeight.w500),
                      ),
                    ]),
                  ],
                ),
              ),
              const SizedBox(height: 25),

              // ---------- Layouts ----------
              _buildRowLayout(selectedRow),

              const SizedBox(height: 22),

              // ---------- Row Status ----------
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF37353f),
                  borderRadius: BorderRadius.circular(10),
                ),
                padding:
                const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(selectedRow,
                        style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w600,
                            fontSize: 17)),
                    const SizedBox(height: 10),
                    LinearProgressIndicator(
                      value: (liveOccupancy != null && totalSeats > 0)
                          ? (liveOccupancy! / totalSeats)
                          : occupancy,
                      backgroundColor: Colors.grey,
                      color: occupancy == 1.0
                          ? Colors.red
                          : (occupancy >= 0.5
                          ? Colors.yellow
                          : const Color(0xFF3cfb34)),
                      minHeight: 6,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "${(occupancy * 100).toStringAsFixed(0)}% occupied",
                      style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 15,
                          fontWeight: FontWeight.w500),
                    )
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // ---------- Back Button ----------
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF222831),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  onPressed: () => Navigator.pop(context),
                  child: const Text(
                    "Back to Main Menu",
                    style: TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w500,
                        color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ---------- Choose row layout ----------
  Widget _buildRowLayout(String row) {
    final seats = seatData[row]!;
    switch (row) {
      case "Row A":
        return _buildRowA(seats);
      case "Row B":
        return _buildRowB(seats);
      case "Row C":
        return _buildRowC(seats);
      case "Row D":
        return _buildRowD(seats);
      case "Row E":
        return _buildRowE(seats);
      case "Row F":
        return _buildRowF(seats);
      default:
        return const SizedBox.shrink();
    }
  }

  // ---------- Example: Row A ----------
  Widget _buildRowA(List<SeatStatus> seats) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Center(
      child: Transform.translate(
        offset: const Offset(60, 100),
        child: Transform.rotate(
          angle: -0.55,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _SeatWithTable(label: "A01", status: seats[0]),
              const SizedBox(width: 25),
              _SeatWithTable(label: "A02", status: seats[1]),
              const SizedBox(width: 25),
              _SeatWithTable(label: "A03", status: seats[2]),
              const SizedBox(width: 25),
              _SeatWithTable(label: "A04", status: seats[3]),
            ],
          ),
        ),
      ),
    ),
  );

  // ---------- Other Rows (B–F) ----------
  Widget _buildRowB(List<SeatStatus> s) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Stack(
      alignment: Alignment.center,
      clipBehavior: Clip.none,
      children: [
        Transform.rotate(
          angle: -2.15,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              _TableBox(),
              const SizedBox(width: 6),
              _TableBox(),
            ],
          ),
        ),
        Positioned(top: 73, left: 180, child: _SeatCircle(label: "B01", status: s[0])),
        Positioned(top: 145, right: 83, child: _SeatCircle(label: "B02", status: s[1])),
        Positioned(bottom: 20, left: 230, child: _SeatCircle(label: "B03", status: s[2])),
      ],
    ),
  );

  Widget _buildRowC(List<SeatStatus> s) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          _TableBox(),
          const SizedBox(width: 20),
          _TableBox(),
        ]),
        const SizedBox(height: 15),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          _SeatCircle(label: "C01", status: s[0]),
          const SizedBox(width: 35),
          _SeatCircle(label: "C02", status: s[1]),
        ]),
      ],
    ),
  );

  Widget _buildRowD(List<SeatStatus> s) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Stack(
      alignment: Alignment.center,
      clipBehavior: Clip.none,
      children: [
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
                borderRadius: BorderRadius.circular(6),
              ),
              alignment: Alignment.center,
              child: const Text("TABLE",
                  style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: Colors.black54)),
            ),
          ),
        ),
        Positioned(bottom: 50, left: 50, child: _SeatCircle(label: "D01", status: s[0])),
        Positioned(bottom: 155, left: 75, child: _SeatCircle(label: "D02", status: s[1])),
        Positioned(top: 65, left: 150, child: _SeatCircle(label: "D03", status: s[2])),
        Positioned(bottom: 30, right: 170, child: _SeatCircle(label: "D04", status: s[3])),
        Positioned(top: 180, right: 100, child: _SeatCircle(label: "D05", status: s[4])),
      ],
    ),
  );

  Widget _buildRowE(List<SeatStatus> s) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Stack(
      alignment: Alignment.center,
      clipBehavior: Clip.none,
      children: [
        Positioned(
          top: 140,
          child: Transform.rotate(
            angle: 0.7,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _TableBox(),
                const SizedBox(width: 8),
                _TableBox(),
              ],
            ),
          ),
        ),
        Positioned(bottom: 120, left: 80, child: _SeatCircle(label: "E01", status: s[0])),
        Positioned(bottom: 60, right: 160, child: _SeatCircle(label: "E02", status: s[1])),
      ],
    ),
  );

  Widget _buildRowF(List<SeatStatus> s) => Container(
    width: double.infinity,
    height: 350,
    decoration: _layoutBox(),
    child: Stack(
      alignment: Alignment.center,
      clipBehavior: Clip.none,
      children: [
        Positioned(
          top: 130,
          child: Transform.rotate(
            angle: 2.5,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _TableBox(),
                const SizedBox(width: 8),
                _TableBox(),
              ],
            ),
          ),
        ),
        Positioned(left: 75, bottom: 170, child: _SeatCircle(label: "F01", status: s[0])),
        Positioned(right: 170, top: 40, child: _SeatCircle(label: "F02", status: s[1])),
      ],
    ),
  );

  BoxDecoration _layoutBox() => BoxDecoration(
    color: const Color(0xFF4a4950),
    borderRadius: BorderRadius.circular(16),
  );
}

/* ------------ Helper Widgets ------------ */
enum SeatStatus { available, occupied }

class _TableBox extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 40,
      width: 80,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: Colors.grey[300],
        borderRadius: BorderRadius.circular(6),
      ),
      child: const Text(
        "TABLE",
        style: TextStyle(
          fontSize: 13,
          fontWeight: FontWeight.bold,
          color: Colors.black54,
        ),
      ),
    );
  }
}

class _SeatWithTable extends StatelessWidget {
  final String label;
  final SeatStatus status;
  const _SeatWithTable({required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    final bool hasPerson = status == SeatStatus.occupied;
    final Color seatColor =
    hasPerson ? const Color(0xFFc5c5c5) : const Color(0xFF3cfb34);

    return Column(
      children: [
        Container(
          height: 35,
          width: 60,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(5),
          ),
          child: const Text("TABLE",
              style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: Colors.black54)),
        ),
        const SizedBox(height: 10),
        Container(
          height: 60,
          width: 60,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: seatColor,
            border: Border.all(color: Colors.black54, width: 1.5),
          ),
          child: hasPerson
              ? const Icon(Icons.person, size: 30, color: Colors.black)
              : Center(
              child: Text(label,
                  style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 16,
                      color: Colors.black))),
        ),
        const SizedBox(height: 6),
        Text(label,
            style: const TextStyle(
                fontSize: 14, fontWeight: FontWeight.w500, color: Colors.white)),
      ],
    );
  }
}

class _SeatCircle extends StatelessWidget {
  final String label;
  final SeatStatus status;
  const _SeatCircle({required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    final bool hasPerson = status == SeatStatus.occupied;
    final Color seatColor =
    hasPerson ? const Color(0xFFc5c5c5) : const Color(0xFF3cfb34);

    return Column(
      children: [
        Container(
          height: 60,
          width: 60,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: seatColor,
            border: Border.all(color: Colors.black54, width: 1.5),
          ),
          child: hasPerson
              ? const Icon(Icons.person, size: 30, color: Colors.black)
              : Center(
              child: Text(label,
                  style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 16,
                      color: Colors.black))),
        ),
        const SizedBox(height: 6),
        Text(label,
            style: const TextStyle(
                fontSize: 14, fontWeight: FontWeight.w500, color: Colors.white)),
      ],
    );
  }
}
