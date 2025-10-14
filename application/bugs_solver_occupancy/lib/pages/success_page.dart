import 'package:flutter/material.dart';
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

      // 🔹 Top bar (Profile removed)
      appBar: AppBar(
        backgroundColor: const Color(0xFF222831),
        automaticallyImplyLeading: false,
        title: const Text(
          "Request",
          style: TextStyle(
            fontSize: 17,
            fontWeight: FontWeight.w500,
          ),
        ),
        foregroundColor: Colors.white,
      ),

      // ✅ Success Body
      body: Padding(
        padding: const EdgeInsets.only(top: 120.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: const [
            // ---------- Title ----------
            Text(
              "Manual Override Request",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.black,
                fontFamily: "IstokWeb",
              ),
            ),

            SizedBox(height: 10),

            // ---------- Subtitle ----------
            Text(
              "Request Submitted!",
              style: TextStyle(
                fontSize: 18,
                color: Colors.black87,
                fontWeight: FontWeight.w500,
                fontFamily: "IstokWeb",
              ),
            ),

            SizedBox(height: 45),

            // ✅ Bigger green check icon
            Icon(Icons.check_circle, color: Colors.green, size: 300),

            SizedBox(height: 40),

            // ---------- Info Text ----------
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 15),
              child: Text(
                "Please wait patiently to let the librarian review your request.",
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
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
