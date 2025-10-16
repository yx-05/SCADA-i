import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'occupancy_page.dart';
import 'manual_override_page.dart';
import 'welcome_screen.dart';
import 'profile_page.dart';
import '../services/mqtt_service.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  String userName = "User";

  @override
  void initState() {
    super.initState();
    _loadUserName();

    // 🛰️ Connect to MQTT broker when app starts
    final mqtt = MQTTService();
    mqtt.connect();
  }

  Future<void> _loadUserName() async {
    await Future.delayed(const Duration(milliseconds: 150));
    try {
      final prefs = await SharedPreferences.getInstance();
      setState(() {
        userName = prefs.getString('userName') ?? "User";
      });
      print("🟢 Loaded userName: $userName");
    } catch (e) {
      print("⚠️ Error loading SharedPreferences: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 🔸 Top bar
              Container(
                margin: EdgeInsets.only(top: 15.h),
                color: const Color(0xFF222831),
                padding:
                EdgeInsets.symmetric(horizontal: 16.w, vertical: 12.h),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Main Menu",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 17.sp,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Row(
                      children: [
                        Icon(Icons.mail_outline,
                            color: Colors.white, size: 25.sp),
                        SizedBox(width: 10.w),

                        // 👇 Profile clickable area
                        GestureDetector(
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const ProfilePage()),
                            ).then((result) async {
                              await _loadUserName(); // ✅ Reload name only
                            });
                          },
                          child: Row(
                            children: [
                              Text(
                                "Profile",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 17.sp,
                                ),
                              ),
                              SizedBox(width: 20.w),
                              CircleAvatar(
                                radius: 20.r,
                                backgroundColor: Colors.white,
                                child: Icon(
                                  Icons.person_outline,
                                  color: Colors.black,
                                  size: 30.sp,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              SizedBox(height: 40.h),

              // 🔸 Profile Section
              Center(
                child: CircleAvatar(
                  radius: 40.r,
                  child: Icon(Icons.person, size: 50.sp),
                ),
              ),
              SizedBox(height: 10.h),

              // ✅ Only show dynamic welcome name
              Text(
                "Welcome back, $userName!",
                style: TextStyle(
                  fontSize: 18.sp,
                  fontWeight: FontWeight.w600,
                ),
                textAlign: TextAlign.center,
              ),

              SizedBox(height: 30.h),

              // 🔹 Menu icons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _MenuIcon(
                    icon: Icons.event_seat,
                    label: "Occupancy",
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const OccupancyPage()),
                      );
                    },
                  ),
                  _MenuIcon(
                    icon: Icons.list_alt,
                    label: "Manual Override\nRequest",
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                            const ManualOverridePage()),
                      );
                    },
                  ),
                  _MenuIcon(
                    icon: Icons.logout,
                    label: "Log Out",
                    onTap: () {
                      Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const WelcomeScreen()),
                            (route) => false,
                      );
                    },
                  ),
                ],
              ),

              SizedBox(height: 70.h),

              // 🔸 Latest News Section
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF222831),
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(30.r),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black26,
                      offset: Offset(0, -2.h),
                      blurRadius: 8.r,
                    ),
                  ],
                ),
                padding: EdgeInsets.all(20.w),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Latest News",
                      style: TextStyle(
                        fontSize: 18.sp,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 20.h),
                    const _NewsCard(
                      imagePath: "assets/library.jpg",
                      title: "Say No to Seat-Hogging Initiative",
                      link:
                      "https://www.monash.edu.my/library/about/news/2025/articles/say-no-to-seat-hogging",
                    ),
                    SizedBox(height: 20.h),
                    const _NewsCard(
                      imagePath: "assets/opening_hour.jpg",
                      title: "Heriot-Watt University's Library Update",
                      link: "https://www.instagram.com/hwumisnews",
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// 🔹 Menu icon widget
class _MenuIcon extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback? onTap;

  const _MenuIcon({
    required this.icon,
    required this.label,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Icon(icon, size: 50.sp, color: Colors.black),
          SizedBox(height: 6.h),
          Text(
            label,
            style: TextStyle(fontSize: 15.sp),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

// 🔹 News Card Widget
class _NewsCard extends StatelessWidget {
  final String imagePath;
  final String title;
  final String? link;

  const _NewsCard({
    required this.imagePath,
    required this.title,
    this.link,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(12.r),
          child: Image.asset(
            imagePath,
            width: double.infinity,
            fit: BoxFit.contain,
          ),
        ),
        SizedBox(height: 6.h),
        Text(
          title,
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w600,
            fontSize: 14.sp,
          ),
        ),
        if (link != null)
          GestureDetector(
            onTap: () async {
              final uri = Uri.parse(link!);
              await launchUrl(uri, mode: LaunchMode.externalApplication);
            },
            child: Text(
              "See More >",
              style: TextStyle(
                color: Colors.white70,
                fontSize: 14.sp,
                fontWeight: FontWeight.w500,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
      ],
    );
  }
}
