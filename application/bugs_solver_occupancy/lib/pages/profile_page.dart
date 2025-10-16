import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
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
        title: Text(
          "Profile",
          style: TextStyle(fontSize: 17.sp, fontWeight: FontWeight.w500),
        ),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(
              isEditing ? Icons.save : Icons.edit,
              color: Colors.white,
              size: 22.sp,
            ),
            onPressed: _toggleEdit,
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(20.w),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(height: 40.h),
              CircleAvatar(
                radius: 60.r,
                backgroundColor: const Color(0xFFEEEEEE),
                child: Icon(Icons.person, size: 70.sp, color: Colors.black54),
              ),
              SizedBox(height: 20.h),
              Text(
                "User Profile",
                style: TextStyle(
                  fontSize: 22.sp,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              SizedBox(height: 20.h),

              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor:
                  isEditing ? Colors.green[700] : const Color(0xFF222831),
                  padding:
                  EdgeInsets.symmetric(horizontal: 20.w, vertical: 12.h),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8.r)),
                ),
                icon: Icon(
                  isEditing ? Icons.save : Icons.edit,
                  color: Colors.white,
                  size: 22.sp,
                ),
                label: Text(
                  isEditing ? "Save Changes" : "Edit Profile",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16.sp,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                onPressed: _toggleEdit,
              ),

              SizedBox(height: 30.h),

              _profileBox(),

              SizedBox(height: 40.h),

              // ✅ Fixed Back Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF222831),
                    padding: EdgeInsets.symmetric(vertical: 14.h),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10.r),
                    ),
                  ),
                  onPressed: () async {
                    print("🟢 Back button pressed");
                    try {
                      await _saveProfileData();
                      print("✅ Data saved safely");
                    } catch (e) {
                      print("⚠️ SharedPreferences save error: $e");
                    }
                    await Future.delayed(const Duration(milliseconds: 300));
                    if (!mounted) return;
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(
                        builder: (_) => const MainScreen(),
                      ),
                    );
                  },
                  child: Text(
                    "Back to Main Menu",
                    style: TextStyle(
                      fontSize: 17.sp,
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
        borderRadius: BorderRadius.circular(10.r),
      ),
      padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 25.h),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _ProfileItem(
            label: "Student Name",
            controller: nameController,
            editable: isEditing,
          ),
          Divider(color: Colors.white54, thickness: 1.h),
          _ProfileItem(
            label: "Student ID",
            controller: idController,
            editable: isEditing,
          ),
          Divider(color: Colors.white54, thickness: 1.h),
          _ProfileItem(
            label: "Course",
            controller: courseController,
            editable: isEditing,
          ),
          Divider(color: Colors.white54, thickness: 1.h),
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
      padding: EdgeInsets.symmetric(vertical: 6.h),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 3,
            child: Text(
              label,
              style: TextStyle(
                color: Colors.white,
                fontSize: 16.sp,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Expanded(
            flex: 5,
            child: editable
                ? TextField(
              controller: controller,
              style: TextStyle(color: Colors.white, fontSize: 16.sp),
              decoration: InputDecoration(
                isDense: true,
                contentPadding: EdgeInsets.symmetric(
                    horizontal: 8.w, vertical: 6.h),
                enabledBorder: const UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white54),
                ),
                focusedBorder: const UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white),
                ),
              ),
            )
                : Text(
              controller.text,
              textAlign: TextAlign.right,
              style: TextStyle(
                color: Colors.white70,
                fontSize: 16.sp,
                fontWeight: FontWeight.w400,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
