import 'package:flutter/material.dart';
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

    // 🟢 Load saved user name
    _loadUserName();

    // 🛰️ Connect to MQTT broker when app starts
    final mqtt = MQTTService();
    mqtt.connect();
  }


  // ✅ Load only user name safely with a short delay
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
                margin: const EdgeInsets.only(top: 15),
                color: const Color(0xFF222831),
                padding:
                const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Main Menu",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Row(
                      children: [
                        const Icon(Icons.mail_outline,
                            color: Colors.white, size: 25),
                        const SizedBox(width: 10),

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
                            children: const [
                              Text(
                                "Profile",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 17,
                                ),
                              ),
                              SizedBox(width: 20),
                              CircleAvatar(
                                radius: 20,
                                backgroundColor: Colors.white,
                                child: Icon(
                                  Icons.person_outline,
                                  color: Colors.black,
                                  size: 30,
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

              const SizedBox(height: 40),

              // 🔸 Profile Section
              const Center(
                child: CircleAvatar(
                  radius: 40,
                  child: Icon(Icons.person, size: 50),
                ),
              ),
              const SizedBox(height: 10),

              // ✅ Only show dynamic welcome name
              Text(
                "Welcome back, $userName!",
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 30),

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
                            builder: (context) => const ManualOverridePage()),
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

              const SizedBox(height: 70),

              // 🔸 Latest News Section
              Container(
                width: double.infinity,
                decoration: const BoxDecoration(
                  color: Color(0xFF222831),
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(30),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black26,
                      offset: Offset(0, -2),
                      blurRadius: 8,
                    ),
                  ],
                ),
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text(
                      "Latest News",
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 20),
                    _NewsCard(
                      imagePath: "assets/library.jpg",
                      title: "Say No to Seat-Hogging Initiative",
                      link:
                      "https://www.monash.edu.my/library/about/news/2025/articles/say-no-to-seat-hogging",
                    ),
                    SizedBox(height: 20),
                    _NewsCard(
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
          Icon(icon, size: 50, color: Colors.black),
          const SizedBox(height: 6),
          Text(
            label,
            style: const TextStyle(fontSize: 15),
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
          borderRadius: BorderRadius.circular(12),
          child: Image.asset(
            imagePath,
            width: double.infinity,
            fit: BoxFit.contain,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          title,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w600,
            fontSize: 14,
          ),
        ),
        if (link != null)
          GestureDetector(
            onTap: () async {
              final uri = Uri.parse(link!);
              await launchUrl(uri, mode: LaunchMode.externalApplication);
            },
            child: const Text(
              "See More >",
              style: TextStyle(
                color: Colors.white70,
                fontSize: 14,
                fontWeight: FontWeight.w500,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
      ],
    );
  }
}
