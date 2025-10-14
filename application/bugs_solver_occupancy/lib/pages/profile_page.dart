import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'main_screen.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  bool isEditing = false;

  final TextEditingController nameController =
  TextEditingController(text: "User");
  final TextEditingController idController =
  TextEditingController(text: "316XXXX");
  final TextEditingController courseController =
  TextEditingController(text: "Bachelor of Computer Science");
  final TextEditingController campusController =
  TextEditingController(text: "Monash University Malaysia");

  @override
  void initState() {
    super.initState();
    _loadProfileData();
  }

  // ✅ Load saved data safely
  Future<void> _loadProfileData() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      if (!mounted) return;
      setState(() {
        nameController.text = prefs.getString('userName') ?? "User";
        idController.text = prefs.getString('userID') ?? "316XXXX";
        courseController.text =
            prefs.getString('userCourse') ?? "Bachelor of Computer Science";
        campusController.text =
            prefs.getString('userCampus') ?? "Monash University Malaysia";
      });
    } catch (e) {
      print("⚠️ Error loading preferences: $e");
    }
  }

  // ✅ Save data safely
  Future<void> _saveProfileData() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('userName', nameController.text);
      await prefs.setString('userID', idController.text);
      await prefs.setString('userCourse', courseController.text);
      await prefs.setString('userCampus', campusController.text);
    } catch (e) {
      print("⚠️ Error saving preferences: $e");
    }
  }

  Future<void> _toggleEdit() async {
    final wasEditing = isEditing;
    setState(() => isEditing = !isEditing);

    if (wasEditing) {
      await _saveProfileData();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Profile information saved!"),
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: const Color(0xFF222831),
        automaticallyImplyLeading: false,
        title: const Text(
          "Profile",
          style: TextStyle(fontSize: 17, fontWeight: FontWeight.w500),
        ),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(isEditing ? Icons.save : Icons.edit, color: Colors.white),
            onPressed: _toggleEdit,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 40),
              const CircleAvatar(
                radius: 60,
                backgroundColor: Color(0xFFEEEEEE),
                child: Icon(Icons.person, size: 70, color: Colors.black54),
              ),
              const SizedBox(height: 20),
              const Text(
                "User Profile",
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 20),

              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor:
                  isEditing ? Colors.green[700] : const Color(0xFF222831),
                  padding:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8)),
                ),
                icon: Icon(
                  isEditing ? Icons.save : Icons.edit,
                  color: Colors.white,
                ),
                label: Text(
                  isEditing ? "Save Changes" : "Edit Profile",
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                onPressed: _toggleEdit,
              ),

              const SizedBox(height: 30),

              _profileBox(),

              const SizedBox(height: 40),

              // ✅ Fixed Back Button (safe + crash free)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF222831),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                  onPressed: () async {
                    print("🟢 Back button pressed");
                    try {
                      // Save first
                      await _saveProfileData();
                      print("✅ Data saved safely");
                    } catch (e) {
                      print("⚠️ SharedPreferences save error: $e");
                    }

                    // ✅ Give plugin time to close channel safely
                    await Future.delayed(const Duration(milliseconds: 300));

                    if (!mounted) return;

                    // ignore: use_build_context_synchronously
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(
                        builder: (_) => const MainScreen(),
                      ),
                    );
                  },
                  child: const Text(
                    "Back to Main Menu",
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w500,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _profileBox() {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: const Color(0xFF5c5b63),
        borderRadius: BorderRadius.circular(10),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 25),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _ProfileItem(
            label: "Student Name",
            controller: nameController,
            editable: isEditing,
          ),
          const Divider(color: Colors.white54),
          _ProfileItem(
            label: "Student ID",
            controller: idController,
            editable: isEditing,
          ),
          const Divider(color: Colors.white54),
          _ProfileItem(
            label: "Course",
            controller: courseController,
            editable: isEditing,
          ),
          const Divider(color: Colors.white54),
          _ProfileItem(
            label: "Campus",
            controller: campusController,
            editable: isEditing,
          ),
        ],
      ),
    );
  }
}

class _ProfileItem extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final bool editable;

  const _ProfileItem({
    required this.label,
    required this.controller,
    required this.editable,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 3,
            child: Text(
              label,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Expanded(
            flex: 5,
            child: editable
                ? TextField(
              controller: controller,
              style: const TextStyle(color: Colors.white, fontSize: 16),
              decoration: const InputDecoration(
                isDense: true,
                contentPadding:
                EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white54),
                ),
                focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white),
                ),
              ),
            )
                : Text(
              controller.text,
              textAlign: TextAlign.right,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 16,
                fontWeight: FontWeight.w400,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
