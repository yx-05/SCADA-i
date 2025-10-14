import 'package:flutter/material.dart';
import 'success_page.dart';
import 'profile_page.dart'; // ✅ Added import for ProfilePage

class ManualOverridePage extends StatefulWidget {
  const ManualOverridePage({super.key});

  @override
  State<ManualOverridePage> createState() => _ManualOverridePageState();
}

class _ManualOverridePageState extends State<ManualOverridePage> {
  String? selectedHardware;
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController reasonController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      // 🔹 Full-width top bar
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

        // ✅ Make profile section clickable
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
                  Text(
                    "Profile",
                    style: TextStyle(color: Colors.white, fontSize: 15),
                  ),
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
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 20),
              const Text(
                "Manual Override Request",
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 25),

              // ---------- Dropdown ----------
              const Text(
                "Types of hardware",
                style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: Colors.black, width: 2),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: selectedHardware,
                    icon: const Icon(Icons.keyboard_arrow_down,
                        color: Colors.black54),
                    dropdownColor: Colors.white,
                    style: const TextStyle(
                      color: Colors.black87,
                      fontSize: 17,
                      fontWeight: FontWeight.w500,
                    ),
                    isExpanded: true,
                    alignment: Alignment.center,
                    hint: const Text(
                      "Types of hardware",
                      textAlign: TextAlign.center,
                    ),
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

              const SizedBox(height: 25),

              // ---------- Personal Info ----------
              const Text(
                "Personal Information",
                style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              const SizedBox(height: 10),

              _CustomTextField(
                hintText: "Enter Full Name",
                controller: nameController,
              ),
              const SizedBox(height: 12),
              _CustomTextField(
                hintText: "Enter Email",
                controller: emailController,
              ),

              const SizedBox(height: 25),

              // ---------- Reason ----------
              const Text(
                "Reason / Notes",
                style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87),
              ),
              const SizedBox(height: 8),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.black, width: 2),
                ),
                child: TextField(
                  controller: reasonController,
                  maxLines: 8,
                  decoration: const InputDecoration(
                    hintText: "Enter reason",
                    hintStyle: TextStyle(color: Colors.grey),
                    contentPadding:
                    EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                    border: InputBorder.none,
                  ),
                ),
              ),

              const SizedBox(height: 35),

              // ---------- Buttons ----------
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF222831),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 30, vertical: 12),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8)),
                    ),
                    onPressed: () {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const SuccessPage()),
                      );
                    },
                    child: const Text(
                      "Submit",
                      style: TextStyle(color: Colors.white, fontSize: 15),
                    ),
                  ),
                  const SizedBox(width: 15),
                  OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.black, width: 2),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 30, vertical: 12),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8)),
                    ),
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: const Text(
                      "Back",
                      style: TextStyle(color: Colors.black, fontSize: 15),
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
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.black, width: 2),
      ),
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
          hintText: hintText,
          hintStyle: const TextStyle(color: Colors.grey),
          border: InputBorder.none,
          contentPadding:
          const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        ),
      ),
    );
  }
}
