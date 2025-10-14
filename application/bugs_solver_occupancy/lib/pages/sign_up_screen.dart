import 'package:flutter/material.dart';

const _hint = Color(0xFFC4C4C4);
const _bg = Color(0xFF222831);
const fieldGap = SizedBox(height: 15);

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key, required this.onBack, required this.onGoToLogin,});
  final VoidCallback onBack;
  final VoidCallback onGoToLogin;

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _formKey = GlobalKey<FormState>();
  final _fullName = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _rememberMe = false;

  @override
  void dispose() {
    _fullName.dispose();
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // white card-like content (to match your Compose)
    return Scaffold(
      resizeToAvoidBottomInset: true, // 👈 allow content to move/scroll above keyboard
      backgroundColor: Colors.white,
      body: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
          child: Form(
            key: _formKey,
            child: SingleChildScrollView(
              padding: const EdgeInsets.only(bottom: 32), // 👈 ensures you can reach the bottom
              keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const SizedBox(height: 8),
                  const Text(
                    "Create Your Account Now !",
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w800,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    "The journey begins! Create your account to access and manage the university's hardware. Monitor devices, control systems, and track usage all from one dashboard.",
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),

                  // Full name
                  TextFormField(
                    controller: _fullName,
                    style: const TextStyle(fontSize: 15),
                    decoration: const InputDecoration(
                      labelText: 'Enter Full Name',
                      labelStyle: TextStyle(color: _hint, fontSize: 14),

                      // keep height stable
                      constraints: BoxConstraints(minHeight: 50),
                      contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 12),

                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        gapPadding: 4,
                      ),

                      errorStyle: TextStyle(fontSize: 12, height: 0.8, color: Colors.red),
                    ),
                    validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
                  ),
                  fieldGap,

                  // Email
                  TextFormField(
                    controller: _email,
                    style: const TextStyle(fontSize: 15),
                    decoration: const InputDecoration(
                      labelText: 'Enter Email',
                      labelStyle: TextStyle(color: _hint, fontSize: 14),

                      constraints: BoxConstraints(minHeight: 50),
                      contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 12),

                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        gapPadding: 4,
                      ),
                      errorStyle: TextStyle(fontSize: 12, height: 0.8, color: Colors.red),
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
                      contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 12),

                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        gapPadding: 4,
                      ),
                      errorStyle: TextStyle(fontSize: 12, height: 0.8, color: Colors.red),
                    ),
                    obscureText: true,
                    validator: (v) =>
                    (v != null && v.length >= 6) ? null : 'Min 6 characters',
                  ),
                  const SizedBox(height: 5),

                  Row(
                    children: [
                      Checkbox(
                        value: _rememberMe,
                        onChanged: (v) => setState(() => _rememberMe = v ?? false),
                        activeColor: Colors.black,
                      ),
                      const Text('Remember me', style: TextStyle(color: Colors.black)),
                    ],
                  ),
                  const SizedBox(height: 2),

                  // Get Started
                  SizedBox(
                    height: 48,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: const Color(0xFF222831),
                        foregroundColor: Colors.white,
                        side: const BorderSide(color: _bg, width: 1),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          // TODO: hook up your signup logic
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Account created!')),
                          );
                          widget.onBack();
                        } else {
                          setState(() {}); // refresh to show errors immediately
                        }
                      },
                      child: const Text(
                        'Get Started',
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
                        backgroundColor: const Color(0xFF222831),
                        foregroundColor: Colors.white,
                        side: const BorderSide(color: Colors.black, width: 1),
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
                  const SizedBox(height: 16),

                  // -------- Divider with "Sign up with" --------
                  Row(
                    children: const [
                      Expanded(child: Divider(thickness: 1, color: Colors.grey)),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8),
                        child: Text(
                          "Sign up with",
                          style: TextStyle(color: Colors.grey, fontSize: 14),
                        ),
                      ),
                      Expanded(child: Divider(thickness: 1, color: Colors.grey)),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // -------- Social row (Facebook + Google) --------
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
                  const SizedBox(height: 8),

                  // -------- Already have an account? Log In --------
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "Already have an account? ",
                        style: TextStyle(color: Colors.black, fontSize: 14),
                      ),
                      GestureDetector(
                        onTap: widget.onGoToLogin, // 👈 CHANGE: call parent
                        child: const Text(
                          "Log In",
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
