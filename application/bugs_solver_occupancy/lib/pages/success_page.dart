import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'main_screen.dart'; // 👈 back to main screen

class SuccessPage extends StatefulWidget {
  const SuccessPage({super.key});

  @override
  State<SuccessPage> createState() => _SuccessPageState();
}

class _SuccessPageState extends State<SuccessPage> {
  @override
  void initState() {
    super.initState();

    // ⏱️ Wait 3 seconds then go back to MainScreen
    Future.delayed(const Duration(seconds: 3), () {
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const MainScreen()),
            (route) => false,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      // 🔹 Top bar
      appBar: AppBar(
        backgroundColor: const Color(0xFF222831),
        automaticallyImplyLeading: false,
        title: Text(
          "Request",
          style: TextStyle(
            fontSize: 17.sp,
            fontWeight: FontWeight.w500,
          ),
        ),
        foregroundColor: Colors.white,
      ),

      // ✅ Success Body
      body: Padding(
        padding: EdgeInsets.only(top: 120.h),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // ---------- Title ----------
            Text(
              "Manual Override Request",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 28.sp,
                fontWeight: FontWeight.bold,
                color: Colors.black,
                fontFamily: "IstokWeb",
              ),
            ),

            SizedBox(height: 10.h),

            // ---------- Subtitle ----------
            Text(
              "Request Submitted!",
              style: TextStyle(
                fontSize: 18.sp,
                color: Colors.black87,
                fontWeight: FontWeight.w500,
                fontFamily: "IstokWeb",
              ),
            ),

            SizedBox(height: 45.h),

            // ✅ Bigger green check icon
            Icon(Icons.check_circle, color: Colors.green, size: 300.sp),

            SizedBox(height: 40.h),

            // ---------- Info Text ----------
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 15.w),
              child: Text(
                "Please wait patiently to let the librarian review your request.",
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18.sp,
                  color: Colors.black87,
                  height: 1.4,
                  fontFamily: "IstokWeb",
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
