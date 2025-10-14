import 'dart:ui';
import 'package:flutter/material.dart';
import 'sign_up_screen.dart';
import 'login_screen.dart'; // 👈

/// Colors from your colors.xml:
/// background_colour: #222831, border_enter: #c4c4c4
const _bg = Color(0xFF222831);

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen>
    with SingleTickerProviderStateMixin {
  bool _showSignUp = false;
  bool _showLogin = false; // 👈

  @override
  Widget build(BuildContext context) {
    final signUpHeight = MediaQuery.of(context).size.height * .77;
    final loginHeight  = MediaQuery.of(context).size.height * .65;

    return Scaffold(
      backgroundColor: _bg,
      body: Stack(
        children: [
          // Main content
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 135),
                  const Text(
                    'Welcome =)',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    "Stay connected with all university hardware systems and control them easily from one dashboard.",
                    style: TextStyle(
                      fontSize: 15,
                      color: Color(0xFFDDDDDD),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  // Logo
                  SizedBox(
                    height: 200,
                    child: Center(
                      child: Image.asset(
                        'assets/removed_bg.png',
                        fit: BoxFit.contain,
                        errorBuilder: (_, __, ___) => const Icon(
                          Icons.image_outlined,
                          color: Colors.white24,
                          size: 120,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  // Create Account
                  BlurButton(
                    text: 'Create Account',
                    backgroundColor: Colors.white,
                    textColor: Colors.black,
                    onPressed: () => setState(() => _showSignUp = true),
                  ),
                  const SizedBox(height: 20),
                  // Log in
                  BlurOutlinedButton(
                    text: 'Log in',
                    backgroundColor: _bg,
                    textColor: Colors.white,
                    borderColor: Colors.white,
                    onPressed: () => setState(() => _showLogin = true),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ),

          // Dim background when any sheet is open
          if (_showSignUp || _showLogin)
            AnimatedOpacity(
              opacity: 1,
              duration: const Duration(milliseconds: 200),
              child: GestureDetector(
                onTap: () => setState(() {
                  _showSignUp = false;
                  _showLogin = false;
                }),
                child: Container(
                  color: Colors.black.withOpacity(0.5),
                ),
              ),
            ),

          // Slide-up SignUp bottom sheet
          AnimatedPositioned(
            duration: const Duration(milliseconds: 300),
            curve: Curves.fastOutSlowIn,
            left: 0,
            right: 0,
            bottom: _showSignUp ? 0 : -signUpHeight,
            height: signUpHeight,
            child: Material(
              color: Colors.transparent,
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
                ),
                child: ClipRRect(
                  borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(30)),
                  child: SignUpScreen(
                    onBack: () => setState(() => _showSignUp = false),
                    // When "Log In" tapped in SignUp
                    onGoToLogin: () async {
                      setState(() => _showSignUp = false);
                      await Future.delayed(const Duration(milliseconds: 650));
                      if (!mounted) return;
                      setState(() => _showLogin = true);
                    },
                  ),
                ),
              ),
            ),
          ),

          // Slide-up Login bottom sheet
          AnimatedPositioned(
            duration: const Duration(milliseconds: 300),
            curve: Curves.fastOutSlowIn,
            left: 0,
            right: 0,
            bottom: _showLogin ? 0 : -loginHeight,
            height: loginHeight,
            child: Material(
              color: Colors.transparent,
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
                ),
                child: ClipRRect(
                  borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(30)),
                  child: LoginScreen(
                    onBack: () => setState(() => _showLogin = false),
                    // 👇 NEW: When "Sign Up" tapped in Login
                    onGoToSignUp: () async {
                      setState(() => _showLogin = false);
                      await Future.delayed(const Duration(milliseconds: 650));
                      if (!mounted) return;
                      setState(() => _showSignUp = true);
                    },
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// Button that gently blurs its text when pressed (to mimic your Compose effect)
class BlurButton extends StatefulWidget {
  const BlurButton({
    super.key,
    required this.text,
    required this.backgroundColor,
    required this.textColor,
    required this.onPressed,
  });

  final String text;
  final Color backgroundColor;
  final Color textColor;
  final VoidCallback onPressed;

  @override
  State<BlurButton> createState() => _BlurButtonState();
}

class _BlurButtonState extends State<BlurButton> {
  bool _pressed = false;

  void _setPressed(bool v) {
    if (_pressed != v) setState(() => _pressed = v);
  }

  @override
  Widget build(BuildContext context) {
    return Listener(
      onPointerDown: (_) => _setPressed(true),
      onPointerUp: (_) => _setPressed(false),
      onPointerCancel: (_) => _setPressed(false),
      child: SizedBox(
        width: double.infinity,
        height: 46,
        child: FilledButton(
          style: FilledButton.styleFrom(
            backgroundColor: widget.backgroundColor,
            foregroundColor: widget.textColor,
            shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
            elevation: 20,
            shadowColor: Colors.black26,
          ),
          onPressed: widget.onPressed,
          child: ImageFiltered(
            imageFilter:
            ImageFilter.blur(sigmaX: _pressed ? 4 : 0, sigmaY: _pressed ? 4 : 0),
            child: Text(
              widget.text,
              style: TextStyle(
                fontSize: 16,
                color: widget.textColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class BlurOutlinedButton extends StatefulWidget {
  const BlurOutlinedButton({
    super.key,
    required this.text,
    required this.backgroundColor,
    required this.textColor,
    required this.borderColor,
    required this.onPressed,
  });

  final String text;
  final Color backgroundColor;
  final Color textColor;
  final Color borderColor;
  final VoidCallback onPressed;

  @override
  State<BlurOutlinedButton> createState() => _BlurOutlinedButtonState();
}

class _BlurOutlinedButtonState extends State<BlurOutlinedButton> {
  bool _pressed = false;

  void _setPressed(bool v) {
    if (_pressed != v) setState(() => _pressed = v);
  }

  @override
  Widget build(BuildContext context) {
    return Listener(
      onPointerDown: (_) => _setPressed(true),
      onPointerUp: (_) => _setPressed(false),
      onPointerCancel: (_) => _setPressed(false),
      child: SizedBox(
        width: double.infinity,
        height: 46,
        child: OutlinedButton(
          style: OutlinedButton.styleFrom(
            side: BorderSide(color: widget.borderColor, width: 2),
            foregroundColor: widget.textColor,
            backgroundColor: widget.backgroundColor,
            shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
            elevation: 20,
            shadowColor: Colors.black26,
          ),
          onPressed: widget.onPressed,
          child: ImageFiltered(
            imageFilter:
            ImageFilter.blur(sigmaX: _pressed ? 4 : 0, sigmaY: _pressed ? 4 : 0),
            child: Text(
              widget.text,
              style: TextStyle(
                fontSize: 16,
                color: widget.textColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
