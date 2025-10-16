import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'main_screen.dart';

const _hint = Color(0xFFC4C4C4);
const _bg = Color(0xFF222831);

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
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const MainScreen()),
      );
    } else {
      setState(() {});
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
          padding: EdgeInsets.fromLTRB(16.w, 24.h, 16.w, 16.h),
          child: Form(
            key: _formKey,
            child: SingleChildScrollView(
              padding: EdgeInsets.only(bottom: 32.h),
              keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  SizedBox(height: 8.h),
                  Text(
                    "Welcome Back !",
                    style: TextStyle(
                      fontSize: 24.sp,
                      fontWeight: FontWeight.w800,
                      color: Colors.black,
                      fontFamily: 'Inter',
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10.h),
                  Text(
                    "The journey continues! Log in to control your university hardware.",
                    style: TextStyle(fontSize: 14.sp, color: Colors.black),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16.h),

                  // Email Field
                  TextFormField(
                    controller: _email,
                    style: TextStyle(fontSize: 15.sp),
                    decoration: InputDecoration(
                      labelText: 'Enter Email',
                      labelStyle: TextStyle(color: _hint, fontSize: 14.sp),
                      constraints: BoxConstraints(minHeight: 50.h),
                      contentPadding:
                      EdgeInsets.symmetric(vertical: 10.h, horizontal: 12.w),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.r)),
                        gapPadding: 4.w,
                      ),
                      errorStyle: TextStyle(
                        fontSize: 12.sp,
                        height: 0.8,
                        color: Colors.red,
                      ),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Required';
                      final re = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
                      return re.hasMatch(v) ? null : 'Enter a valid email';
                    },
                  ),
                  SizedBox(height: 15.h),

                  // Password Field
                  TextFormField(
                    controller: _password,
                    style: TextStyle(fontSize: 15.sp),
                    decoration: InputDecoration(
                      labelText: 'Enter Password',
                      labelStyle: TextStyle(color: _hint, fontSize: 14.sp),
                      constraints: BoxConstraints(minHeight: 50.h),
                      contentPadding:
                      EdgeInsets.symmetric(vertical: 10.h, horizontal: 12.w),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.r)),
                        gapPadding: 4.w,
                      ),
                      errorStyle: TextStyle(
                        fontSize: 12.sp,
                        height: 0.8,
                        color: Colors.red,
                      ),
                    ),
                    obscureText: true,
                    validator: (v) =>
                    (v != null && v.length >= 6) ? null : 'Min 6 characters',
                  ),
                  SizedBox(height: 18.h),

                  // Log In Button
                  SizedBox(
                    height: 48.h,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: _bg,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30.r),
                        ),
                      ),
                      onPressed: _login,
                      child: Text(
                        'Log In',
                        style:
                        TextStyle(fontSize: 16.sp, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  SizedBox(height: 12.h),

                  // Back Button
                  SizedBox(
                    height: 48.h,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: _bg,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30.r),
                        ),
                      ),
                      onPressed: widget.onBack,
                      child: Text(
                        'Back',
                        style:
                        TextStyle(fontSize: 16.sp, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  SizedBox(height: 20.h),

                  // Divider
                  Row(
                    children: [
                      Expanded(
                          child:
                          Divider(thickness: 1.h, color: Colors.grey)),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8.w),
                        child: Text(
                          "Sign in with",
                          style:
                          TextStyle(color: Colors.grey, fontSize: 14.sp),
                        ),
                      ),
                      Expanded(
                          child:
                          Divider(thickness: 1.h, color: Colors.grey)),
                    ],
                  ),
                  SizedBox(height: 12.h),

                  // Social Icons
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/facebook_icon.png',
                          height: 45.h,
                          errorBuilder: (_, __, ___) =>
                          const Icon(Icons.facebook_outlined),
                        ),
                      ),
                      SizedBox(width: 24.w),
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/google_icon.png',
                          height: 44.h,
                          errorBuilder: (_, __, ___) =>
                          const Icon(Icons.g_mobiledata),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12.h),

                  // Sign Up Link
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "Don't have an account? ",
                        style: TextStyle(
                            color: Colors.black, fontSize: 15.sp),
                      ),
                      GestureDetector(
                        onTap: widget.onGoToSignUp,
                        child: Text(
                          "Sign Up",
                          style: TextStyle(
                            color: Colors.blue,
                            fontSize: 14.sp,
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
