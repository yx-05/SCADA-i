import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import '../services/mqtt_service.dart';
import 'success_page.dart';
import 'profile_page.dart';

class ManualOverridePage extends StatefulWidget {
  const ManualOverridePage({super.key});

  @override
  State<ManualOverridePage> createState() => _ManualOverridePageState();
}

class _ManualOverridePageState extends State<ManualOverridePage> {
  final mqtt = MQTTService(); // ✅ use same MQTT instance

  String? selectedHardware;
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController changeController = TextEditingController();
  final TextEditingController reasonController = TextEditingController();

  bool isSubmitting = false;

  @override
  void initState() {
    super.initState();
    mqtt.connect();

    mqtt.dataStream.listen((data) {
      if (!mounted) return;
      final topic = data['topic'] ?? "";

      if (topic.contains("manual_override/response")) {
        final status = data['status'];

        if (status == "approved") {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const SuccessPage()),
          );
        } else if (status == "rejected") {
          _showResultDialog("Your override request was rejected by the IoT system.");
        } else {
          _showResultDialog("Received unknown response: $status");
        }
      }
    });
  }

  @override
  void dispose() {
    mqtt.disconnect();
    super.dispose();
  }

  void _showResultDialog(String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Result"),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("OK"),
          ),
        ],
      ),
    );
  }

  void _submitRequest() {
    if (selectedHardware == null ||
        nameController.text.isEmpty ||
        emailController.text.isEmpty ||
        changeController.text.isEmpty ||
        reasonController.text.isEmpty) {
      _showResultDialog("Please fill in all fields before submitting.");
      return;
    }

    setState(() => isSubmitting = true);

    final request = {
      "hardware": selectedHardware,
      "name": nameController.text,
      "email": emailController.text,
      "change": changeController.text,
      "reason": reasonController.text,
      "timestamp": DateTime.now().toIso8601String(),
    };

    mqtt.publish('room/365/manual_override/request', request);

    _showResultDialog("Request sent to IoT system. Awaiting response...");
    setState(() => isSubmitting = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      appBar: AppBar(
        backgroundColor: const Color(0xFF222831),
        automaticallyImplyLeading: false,
        title: Text(
          "Request",
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
                  MaterialPageRoute(builder: (_) => const ProfilePage()),
                );
              },
              child: Row(
                children: [
                  Icon(Icons.person_outline, color: Colors.white, size: 22.sp),
                  SizedBox(width: 5.w),
                  Text("Profile",
                      style: TextStyle(color: Colors.white, fontSize: 15.sp)),
                ],
              ),
            ),
          ),
        ],
      ),

      body: Padding(
        padding: EdgeInsets.all(20.w),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(height: 20.h),
              Text(
                "Manual Override Request",
                textAlign: TextAlign.center,
                style: TextStyle(
                    fontSize: 20.sp,
                    fontWeight: FontWeight.bold,
                    color: Colors.black87),
              ),
              SizedBox(height: 25.h),

              // ---------- Hardware Dropdown ----------
              Text(
                "Types of hardware",
                style: TextStyle(
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              SizedBox(height: 8.h),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 14.w),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: Colors.black, width: 2.w),
                  borderRadius: BorderRadius.circular(20.r),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: selectedHardware,
                    icon: Icon(Icons.keyboard_arrow_down,
                        color: Colors.black54, size: 24.sp),
                    dropdownColor: Colors.white,
                    style: TextStyle(
                        color: Colors.black87,
                        fontSize: 17.sp,
                        fontWeight: FontWeight.w500),
                    isExpanded: true,
                    alignment: Alignment.center,
                    hint: Text("Select hardware type",
                        style: TextStyle(fontSize: 16.sp)),
                    items: const [
                      DropdownMenuItem(
                        value: "Computer",
                        alignment: Alignment.center,
                        child: Text("Computer", textAlign: TextAlign.center),
                      ),
                      DropdownMenuItem(
                        value: "AC Unit",
                        alignment: Alignment.center,
                        child: Text("AC Unit", textAlign: TextAlign.center),
                      ),
                      DropdownMenuItem(
                        value: "Light",
                        alignment: Alignment.center,
                        child: Text("Light", textAlign: TextAlign.center),
                      ),
                    ],
                    onChanged: (value) {
                      setState(() => selectedHardware = value);
                    },
                  ),
                ),
              ),

              SizedBox(height: 25.h),

              // ---------- Personal Info ----------
              Text(
                "Personal Information",
                style: TextStyle(
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              SizedBox(height: 10.h),
              _CustomTextField(
                hintText: "Enter Full Name",
                controller: nameController,
              ),
              SizedBox(height: 12.h),
              _CustomTextField(
                hintText: "Enter Email",
                controller: emailController,
              ),
              SizedBox(height: 25.h),

              // ---------- Change / Action ----------
              Text(
                "Change / Action to Perform",
                style: TextStyle(
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              SizedBox(height: 8.h),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10.r),
                  border: Border.all(color: Colors.black, width: 2.w),
                ),
                child: TextField(
                  controller: changeController,
                  maxLines: 3,
                  decoration: InputDecoration(
                    hintText:
                    "e.g., Turn off all PCs, set AC from 25°C to 29°C, dim lights, etc.",
                    hintStyle: TextStyle(color: Colors.grey, fontSize: 14.sp),
                    contentPadding:
                    EdgeInsets.symmetric(horizontal: 12.w, vertical: 12.h),
                    border: InputBorder.none,
                  ),
                ),
              ),

              SizedBox(height: 25.h),

              // ---------- Reason ----------
              Text(
                "Reason / Notes",
                style: TextStyle(
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              SizedBox(height: 8.h),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10.r),
                  border: Border.all(color: Colors.black, width: 2.w),
                ),
                child: TextField(
                  controller: reasonController,
                  maxLines: 5,
                  decoration: InputDecoration(
                    hintText: "Enter reason for this change request",
                    hintStyle: TextStyle(color: Colors.grey, fontSize: 14.sp),
                    contentPadding:
                    EdgeInsets.symmetric(horizontal: 12.w, vertical: 12.h),
                    border: InputBorder.none,
                  ),
                ),
              ),

              SizedBox(height: 35.h),

              // ---------- Buttons ----------
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF222831),
                      padding: EdgeInsets.symmetric(
                          horizontal: 30.w, vertical: 12.h),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.r)),
                    ),
                    onPressed: isSubmitting ? null : _submitRequest,
                    child: Text(
                      "Submit",
                      style: TextStyle(color: Colors.white, fontSize: 15.sp),
                    ),
                  ),
                  SizedBox(width: 15.w),
                  OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      side: BorderSide(color: Colors.black, width: 2.w),
                      padding: EdgeInsets.symmetric(
                          horizontal: 30.w, vertical: 12.h),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.r)),
                    ),
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: Text(
                      "Back",
                      style: TextStyle(color: Colors.black, fontSize: 15.sp),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/* ------------ Helper Widget ------------ */
class _CustomTextField extends StatelessWidget {
  final String hintText;
  final TextEditingController controller;

  const _CustomTextField({
    required this.hintText,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10.r),
        border: Border.all(color: Colors.black, width: 2.w),
      ),
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
          hintText: hintText,
          hintStyle: TextStyle(color: Colors.grey, fontSize: 14.sp),
          border: InputBorder.none,
          contentPadding:
          EdgeInsets.symmetric(horizontal: 12.w, vertical: 12.h),
        ),
      ),
    );
  }
}
