import 'package:flutter/material.dart';
import 'main_screen.dart';

const _hint = Color(0xFFC4C4C4);
const _bg = Color(0xFF222831);
const fieldGap = SizedBox(height: 15);

class LoginScreen extends StatefulWidget {
  const LoginScreen({
    super.key,
    required this.onBack,
    required this.onGoToSignUp,
  });

  final VoidCallback onBack;
  final VoidCallback onGoToSignUp;

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _password = TextEditingController();

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  void _login() {
    if (_formKey.currentState!.validate()) {
      // 👉 Navigate to MainScreen
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const MainScreen()),
      );
    } else {
      setState(() {}); // re-render with errors
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: Colors.white,
      body: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
          child: Form(
            key: _formKey,
            child: SingleChildScrollView(
              padding: const EdgeInsets.only(bottom: 32),
              keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const SizedBox(height: 8),
                  const Text(
                    "Welcome Back !",
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w800,
                      color: Colors.black,
                      fontFamily: 'Inter',
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    "The journey continues! Log in to control your university hardware.",
                    style: TextStyle(fontSize: 14, color: Colors.black),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),

                  // Email
                  TextFormField(
                    controller: _email,
                    style: const TextStyle(fontSize: 15),
                    decoration: const InputDecoration(
                      labelText: 'Enter Email',
                      labelStyle: TextStyle(color: _hint, fontSize: 14),
                      constraints: BoxConstraints(minHeight: 50),
                      contentPadding:
                      EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        gapPadding: 4,
                      ),
                      errorStyle: TextStyle(
                          fontSize: 12, height: 0.8, color: Colors.red),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Required';
                      final re = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
                      return re.hasMatch(v) ? null : 'Enter a valid email';
                    },
                  ),
                  fieldGap,

                  // Password
                  TextFormField(
                    controller: _password,
                    style: const TextStyle(fontSize: 15),
                    decoration: const InputDecoration(
                      labelText: 'Enter Password',
                      labelStyle: TextStyle(color: _hint, fontSize: 14),
                      constraints: BoxConstraints(minHeight: 50),
                      contentPadding:
                      EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        gapPadding: 4,
                      ),
                      errorStyle: TextStyle(
                          fontSize: 12, height: 0.8, color: Colors.red),
                    ),
                    obscureText: true,
                    validator: (v) =>
                    (v != null && v.length >= 6) ? null : 'Min 6 characters',
                  ),
                  const SizedBox(height: 18),

                  // Log In
                  SizedBox(
                    height: 48,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: _bg,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      onPressed: _login,
                      child: const Text(
                        'Log In',
                        style: TextStyle(fontSize: 16, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Back
                  SizedBox(
                    height: 48,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: _bg,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      onPressed: widget.onBack,
                      child: const Text(
                        'Back',
                        style: TextStyle(fontSize: 16, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Divider
                  Row(
                    children: const [
                      Expanded(child: Divider(thickness: 1, color: Colors.grey)),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8),
                        child: Text(
                          "Sign in with",
                          style: TextStyle(color: Colors.grey, fontSize: 14),
                        ),
                      ),
                      Expanded(child: Divider(thickness: 1, color: Colors.grey)),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Social
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/facebook_icon.png',
                          height: 45,
                          errorBuilder: (_, __, ___) =>
                          const Icon(Icons.facebook_outlined),
                        ),
                      ),
                      const SizedBox(width: 24),
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/google_icon.png',
                          height: 44,
                          errorBuilder: (_, __, ___) =>
                          const Icon(Icons.g_mobiledata),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Go to Sign Up
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "Don't have an account? ",
                        style: TextStyle(color: Colors.black, fontSize: 15),
                      ),
                      GestureDetector(
                        onTap: widget.onGoToSignUp,
                        child: const Text(
                          "Sign Up",
                          style: TextStyle(
                            color: Colors.blue,
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            decoration: TextDecoration.underline,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
